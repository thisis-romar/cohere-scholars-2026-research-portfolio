#!/usr/bin/env python3
"""
Extract Verbatim Papers from Raw Conversions
Creates clean verbatim markdown files from timestamped raw conversions

Purpose: 
- Extract verbatim paper content from converted_output/ RAW_CONVERSION files
- Create clean [Paper_Name].md files in proper 02-MARKDOWN/[Category]/ directories
- Maintain the actual paper content alongside _STUDY.md files
- Remove conversion metadata headers for clean verbatim content

Usage:
    python extract_verbatim_papers.py
"""

import os
import re
from pathlib import Path
import json

def find_raw_conversions():
    """Find all RAW_CONVERSION files in converted_output"""
    converted_dir = Path("converted_output")
    raw_files = []
    
    if not converted_dir.exists():
        print("❌ converted_output directory not found")
        return []
    
    for file in converted_dir.glob("*RAW_CONVERSION*.md"):
        raw_files.append(file)
    
    return sorted(raw_files)

def extract_clean_content(raw_file_path):
    """Extract clean paper content, removing conversion metadata"""
    with open(raw_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the end of metadata section (after the "---" line)
    lines = content.split('\n')
    content_start = 0
    
    # Look for the metadata separator and actual paper start
    for i, line in enumerate(lines):
        if line.strip() == "---" and i > 0:
            content_start = i + 1
            break
        # Alternative: look for actual paper title patterns
        if line.startswith("# ") and "Raw PDF Conversion" not in line:
            content_start = i
            break
    
    # Extract clean content (skip metadata header)
    clean_content = '\n'.join(lines[content_start:]).strip()
    
    return clean_content

def determine_paper_category(paper_name):
    """Determine which category directory the paper belongs to"""
    # Map papers to their categories based on existing structure
    category_mapping = {
        # Multilingual papers
        'Aya_Expanse': 'Multilingual',
        'Aya_Vision': 'Multimodal',  # Cross-listed
        'Deja_Vu_Multilingual': 'Multilingual', 
        'M_RewardBench': 'Multilingual',
        'MURI_High_Quality': 'Multilingual',
        'NeoBabel': 'Multilingual',  # Also Multimodal
        'One_Tokenizer': 'Multilingual',
        'State_Multilingual': 'Multilingual',
        
        # Evaluation papers  
        'From_Tools_Teammates': 'Evaluation',
        'Global_MMLU': 'Evaluation',
        'INCLUDE_Evaluating': 'Evaluation',
        'Kaleidoscope': 'Evaluation',
        'Reality_Check': 'Evaluation',
        'Leaderboard_Illusion': 'Evaluation',
        
        # Inference papers
        'When_Life_Gives': 'Inference',
        'Treasure_Hunt': 'Inference', 
        'Crosslingual_Reasoning': 'Inference',
        'BAM_Just_Like': 'Inference',
        'Nexus_Specialization': 'Inference',
        
        # Data/Training papers
        'Improve_Robustness': 'Data-Training',
        'Diversify_Conquer': 'Data-Training',
        'Bridging_Data_Provenance': 'Data-Training',
        
        # Model Merging papers
        'If_You_Cant_Use': 'Model-Merging',
        'Mix_Data_Merge': 'Model-Merging', 
        'Investigating_Continual': 'Model-Merging',
        
        # Preference papers
        'When_Personalization': 'Preference-Personalization',
        'Post_Trainer_Guide': 'Preference-Personalization'
    }
    
    # Find matching category
    for key, category in category_mapping.items():
        if key in paper_name:
            return category
    
    # Default fallback
    return 'Architecture'  # Default category for unmapped papers

def clean_paper_name(raw_filename):
    """Extract clean paper name from raw filename"""
    # Remove RAW_CONVERSION and timestamp suffix
    name = raw_filename.replace('_RAW_CONVERSION_markitdown', '').replace('_RAW_CONVERSION_marker', '')
    # Remove timestamp pattern
    name = re.sub(r'_\d{8}_\d{6}', '', name)
    # Remove .md extension if present
    name = name.replace('.md', '')
    return name

def create_verbatim_file(raw_file, output_dir):
    """Create clean verbatim markdown file from raw conversion"""
    raw_filename = raw_file.stem
    clean_name = clean_paper_name(raw_filename)
    category = determine_paper_category(clean_name)
    
    # Create category directory
    category_dir = Path(output_dir) / category
    category_dir.mkdir(parents=True, exist_ok=True)
    
    # Extract clean content
    clean_content = extract_clean_content(raw_file)
    
    # Create output filename
    output_file = category_dir / f"{clean_name}.md"
    
    # Write clean verbatim content
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(clean_content)
    
    return output_file, len(clean_content)

def main():
    """Main extraction process"""
    print("🔍 Finding RAW_CONVERSION files...")
    raw_files = find_raw_conversions()
    
    if not raw_files:
        print("❌ No RAW_CONVERSION files found in converted_output/")
        return
    
    print(f"📄 Found {len(raw_files)} RAW_CONVERSION files")
    
    output_dir = "02-MARKDOWN"
    extracted_files = []
    total_size = 0
    
    print(f"\n🔧 Extracting verbatim content to {output_dir}/...")
    
    for raw_file in raw_files:
        try:
            output_file, content_size = create_verbatim_file(raw_file, output_dir)
            extracted_files.append({
                'source': str(raw_file),
                'output': str(output_file),
                'size': content_size
            })
            total_size += content_size
            print(f"✅ {raw_file.name} → {output_file.relative_to(Path(output_dir))}")
            
        except Exception as e:
            print(f"❌ Failed to process {raw_file.name}: {e}")
    
    # Generate summary
    print(f"\n📊 Extraction Summary:")
    print(f"   • Files processed: {len(raw_files)}")
    print(f"   • Files extracted: {len(extracted_files)}")
    print(f"   • Total content size: {total_size:,} characters")
    print(f"   • Average file size: {total_size // len(extracted_files) if extracted_files else 0:,} characters")
    
    # Save detailed report
    report = {
        'timestamp': '2025-08-26',
        'source_directory': 'converted_output',
        'output_directory': output_dir,
        'files_processed': len(raw_files),
        'files_extracted': len(extracted_files),
        'total_content_size': total_size,
        'extracted_files': extracted_files
    }
    
    with open('verbatim_extraction_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n✅ Verbatim extraction complete!")
    print(f"📋 Detailed report saved to: verbatim_extraction_report.json")
    print(f"\n🎯 Next steps:")
    print(f"   • Check 02-MARKDOWN/[Category]/ directories for verbatim .md files")
    print(f"   • Verify content quality and formatting")
    print(f"   • Commit new verbatim files to repository")

if __name__ == "__main__":
    main()
