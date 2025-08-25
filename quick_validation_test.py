#!/usr/bin/env python3
"""
PDF-to-MD Validation Tool - Simple Test Version
==============================================

Quick test of core validation functionality with minimal dependencies.
"""

import os
import sys
from pathlib import Path
import re
from datetime import datetime

def simple_text_similarity(text1, text2):
    """Calculate basic text similarity"""
    # Convert to lowercase and remove extra whitespace
    text1_clean = re.sub(r'\s+', ' ', text1.lower().strip())
    text2_clean = re.sub(r'\s+', ' ', text2.lower().strip())
    
    # Basic word overlap similarity
    words1 = set(text1_clean.split())
    words2 = set(text2_clean.split())
    
    if not words1 and not words2:
        return 1.0
    if not words1 or not words2:
        return 0.0
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    return len(intersection) / len(union) if union else 0.0

def extract_pdf_text_simple(pdf_path):
    """Extract text using basic PyPDF2"""
    try:
        import PyPDF2
        
        text = ""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        
        return text
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
        return ""

def analyze_markdown_content(md_path):
    """Analyze Markdown content"""
    try:
        with open(md_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        analysis = {
            'text': content,
            'char_count': len(content),
            'word_count': len(content.split()),
            'line_count': len(content.split('\n')),
            'headers': len(re.findall(r'^#{1,6}\s+', content, re.MULTILINE)),
            'tables': len(re.findall(r'\|.*\|', content)),
            'images': len(re.findall(r'!\[.*?\]\(.*?\)', content)),
            'links': len(re.findall(r'\[.*?\]\(.*?\)', content))
        }
        
        return analysis
    except Exception as e:
        print(f"Error reading Markdown {md_path}: {e}")
        return None

def validate_file_pair(pdf_path, md_path):
    """Validate a single PDF-MD pair"""
    print(f"\n📄 Validating: {os.path.basename(pdf_path)} -> {os.path.basename(md_path)}")
    
    # Extract content
    pdf_text = extract_pdf_text_simple(pdf_path)
    md_analysis = analyze_markdown_content(md_path)
    
    if not md_analysis:
        return None
    
    # Calculate similarity
    similarity = simple_text_similarity(pdf_text, md_analysis['text'])
    
    # Length comparison
    pdf_words = len(pdf_text.split()) if pdf_text else 0
    md_words = md_analysis['word_count']
    
    length_ratio = min(md_words / pdf_words, 1.0) if pdf_words > 0 else 0.0
    
    # Overall score
    overall_score = (similarity * 0.6 + length_ratio * 0.4)
    
    result = {
        'pdf_words': pdf_words,
        'md_words': md_words,
        'similarity': similarity,
        'length_ratio': length_ratio,
        'overall_score': overall_score,
        'headers': md_analysis['headers'],
        'tables': md_analysis['tables'],
        'images': md_analysis['images'],
        'links': md_analysis['links']
    }
    
    # Display results
    print(f"  📊 Text Similarity: {similarity:.3f}")
    print(f"  📝 Length Ratio: {length_ratio:.3f} ({pdf_words} -> {md_words} words)")
    print(f"  🏗️  Structure: {md_analysis['headers']} headers, {md_analysis['tables']} tables, {md_analysis['images']} images")
    print(f"  ⭐ Overall Score: {overall_score:.3f}")
    
    return result

def find_file_pairs(source_dir, converted_dir, max_files=None):
    """Find PDF-MD file pairs"""
    pairs = []
    source_path = Path(source_dir)
    converted_path = Path(converted_dir)
    
    for pdf_file in source_path.rglob("*.pdf"):
        pdf_name = pdf_file.stem
        
        # Look for corresponding MD file
        md_candidates = list(converted_path.glob(f"*{pdf_name}*.md"))
        
        if md_candidates:
            pairs.append((str(pdf_file), str(md_candidates[0])))
    
    if max_files:
        pairs = pairs[:max_files]
    
    return pairs

def main():
    """Main validation function"""
    print("🔍 PDF-to-MD Quick Validation Test")
    print("=" * 50)
    
    # Configuration
    source_dir = "01-PAPERS"
    converted_dir = "converted_output"
    max_files = 10  # Test with more files for comprehensive assessment
    
    # Find file pairs
    pairs = find_file_pairs(source_dir, converted_dir, max_files)
    
    if not pairs:
        print("❌ No PDF-MD file pairs found!")
        return
    
    print(f"📁 Found {len(pairs)} file pairs to validate")
    
    # Validate each pair
    results = []
    for i, (pdf_path, md_path) in enumerate(pairs, 1):
        print(f"\n[{i}/{len(pairs)}]", end="")
        result = validate_file_pair(pdf_path, md_path)
        if result:
            results.append(result)
    
    # Summary
    if results:
        avg_similarity = sum(r['similarity'] for r in results) / len(results)
        avg_score = sum(r['overall_score'] for r in results) / len(results)
        
        print(f"\n" + "="*50)
        print(f"📈 SUMMARY RESULTS")
        print(f"  Files Processed: {len(results)}")
        print(f"  Average Similarity: {avg_similarity:.3f}")
        print(f"  Average Overall Score: {avg_score:.3f}")
        print(f"  Grade: {'A' if avg_score > 0.8 else 'B' if avg_score > 0.6 else 'C' if avg_score > 0.4 else 'D'}")
    
    print(f"\n✅ Validation test complete!")

if __name__ == "__main__":
    main()
