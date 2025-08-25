#!/usr/bin/env python3
"""
Batch PDF to Markdown Converter
Processes all PDFs in a directory using validated conversion methods

Features:
- Processes all PDFs in input directory
- Uses best available conversion method
- Creates organized output structure
- Provides progress tracking and quality metrics
- Generates summary report of all conversions

Usage:
    python batch_convert_all_pdfs.py --input-dir "01-PAPERS" --output-dir "03-PROCESSED-RAW"
    python batch_convert_all_pdfs.py --input-dir "01-PAPERS" --output-dir "03-PROCESSED-RAW" --compare
"""

import argparse
import os
import sys
from pathlib import Path
import json
from datetime import datetime
import time

# Import our validated converter
sys.path.append(str(Path(__file__).parent))
from validated_pdf_to_markdown_converter import PDFToMarkdownConverter

def find_all_pdfs(input_dir):
    """Find all PDF files in input directory"""
    pdf_files = []
    input_path = Path(input_dir)
    
    if not input_path.exists():
        print(f"❌ Input directory not found: {input_dir}")
        return []
    
    # Find all PDFs recursively
    for pdf_file in input_path.rglob("*.pdf"):
        if pdf_file.is_file():
            pdf_files.append(pdf_file)
    
    return sorted(pdf_files)

def create_output_structure(output_dir):
    """Create organized output directory structure"""
    output_path = Path(output_dir)
    
    # Create main directories
    dirs_to_create = [
        output_path,
        output_path / "01-RAW-CONVERSIONS",
        output_path / "02-COMPARISON-REPORTS", 
        output_path / "03-BATCH-SUMMARIES"
    ]
    
    for dir_path in dirs_to_create:
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"📁 Created directory: {dir_path}")
    
    return output_path

def process_batch(pdf_files, output_dir, compare_methods=False):
    """Process batch of PDF files"""
    converter = PDFToMarkdownConverter()
    output_path = Path(output_dir)
    
    results = {
        "batch_info": {
            "timestamp": datetime.now().isoformat(),
            "total_files": len(pdf_files),
            "compare_methods": compare_methods
        },
        "conversions": [],
        "summary": {
            "successful": 0,
            "failed": 0,
            "total_processing_time": 0,
            "methods_used": {}
        }
    }
    
    print(f"\n🔄 Starting batch conversion of {len(pdf_files)} PDFs...")
    print(f"📤 Output directory: {output_dir}")
    print(f"🔍 Compare methods: {compare_methods}")
    print("=" * 60)
    
    start_time = time.time()
    
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"\n[{i}/{len(pdf_files)}] Processing: {pdf_file.name}")
        print("-" * 40)
        
        file_start_time = time.time()
        
        try:
            # Convert PDF
            conversion_result = converter.convert_and_save(
                str(pdf_file),
                compare_methods=compare_methods
            )
            
            if conversion_result and conversion_result.get("success"):
                # Move files to organized structure
                markdown_file = Path(conversion_result["markdown_file"])
                organized_md_path = output_path / "01-RAW-CONVERSIONS" / markdown_file.name
                
                # Move markdown file
                if markdown_file.exists():
                    markdown_file.rename(organized_md_path)
                    conversion_result["markdown_file"] = str(organized_md_path)
                
                # Move comparison report if exists
                if "comparison_file" in conversion_result:
                    comparison_file = Path(conversion_result["comparison_file"])
                    if comparison_file.exists():
                        organized_comp_path = output_path / "02-COMPARISON-REPORTS" / comparison_file.name
                        comparison_file.rename(organized_comp_path)
                        conversion_result["comparison_file"] = str(organized_comp_path)
                
                file_time = time.time() - file_start_time
                conversion_result["processing_time"] = round(file_time, 2)
                
                # Update summary
                results["summary"]["successful"] += 1
                method_used = conversion_result.get("method_used", "unknown")
                results["summary"]["methods_used"][method_used] = results["summary"]["methods_used"].get(method_used, 0) + 1
                
                print(f"✅ Success! Method: {method_used}")
                print(f"📄 Output: {organized_md_path.name}")
                print(f"⏱️  Time: {file_time:.1f}s")
                
            else:
                results["summary"]["failed"] += 1
                conversion_result = {
                    "success": False,
                    "error": "Conversion failed"
                }
                print("❌ Conversion failed")
        
        except Exception as e:
            results["summary"]["failed"] += 1
            conversion_result = {
                "success": False,
                "error": str(e)
            }
            print(f"❌ Error: {e}")
        
        # Add to results
        results["conversions"].append({
            "input_file": str(pdf_file),
            "file_size_mb": round(pdf_file.stat().st_size / 1024 / 1024, 2),
            **conversion_result
        })
    
    # Calculate total time
    total_time = time.time() - start_time
    results["summary"]["total_processing_time"] = round(total_time, 2)
    
    return results

def save_batch_summary(results, output_dir):
    """Save comprehensive batch summary"""
    output_path = Path(output_dir)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save detailed JSON report
    summary_file = output_path / "03-BATCH-SUMMARIES" / f"batch_summary_{timestamp}.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Create human-readable summary
    readable_summary = output_path / "03-BATCH-SUMMARIES" / f"batch_summary_{timestamp}.md"
    
    summary_md = f"""# Batch PDF Conversion Summary
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Overview
- **Total Files Processed:** {results['batch_info']['total_files']}
- **Successful Conversions:** {results['summary']['successful']}
- **Failed Conversions:** {results['summary']['failed']}
- **Success Rate:** {(results['summary']['successful'] / results['batch_info']['total_files'] * 100):.1f}%
- **Total Processing Time:** {results['summary']['total_processing_time']:.1f} seconds
- **Average Time per File:** {(results['summary']['total_processing_time'] / results['batch_info']['total_files']):.1f} seconds

## Methods Used
"""
    
    for method, count in results['summary']['methods_used'].items():
        percentage = (count / results['summary']['successful'] * 100) if results['summary']['successful'] > 0 else 0
        summary_md += f"- **{method}:** {count} files ({percentage:.1f}%)\n"
    
    summary_md += "\n## File Processing Details\n"
    
    for conv in results['conversions']:
        status = "✅" if conv.get('success', False) else "❌"
        filename = Path(conv['input_file']).name
        method = conv.get('method_used', 'N/A')
        time_taken = conv.get('processing_time', 0)
        file_size = conv.get('file_size_mb', 0)
        
        summary_md += f"- {status} **{filename}** | {method} | {time_taken:.1f}s | {file_size:.1f}MB\n"
    
    if results['summary']['failed'] > 0:
        summary_md += "\n## Failed Conversions\n"
        for conv in results['conversions']:
            if not conv.get('success', False):
                filename = Path(conv['input_file']).name
                error = conv.get('error', 'Unknown error')
                summary_md += f"- ❌ **{filename}:** {error}\n"
    
    with open(readable_summary, 'w', encoding='utf-8') as f:
        f.write(summary_md)
    
    print(f"\n📊 Batch summary saved:")
    print(f"  📄 Detailed report: {summary_file.name}")
    print(f"  📖 Readable summary: {readable_summary.name}")
    
    return summary_file, readable_summary

def main():
    parser = argparse.ArgumentParser(description="Batch convert PDFs to Markdown using validated methods")
    parser.add_argument("--input-dir", required=True, help="Directory containing PDF files")
    parser.add_argument("--output-dir", required=True, help="Directory for output files")
    parser.add_argument("--compare", action="store_true", help="Compare multiple conversion methods")
    parser.add_argument("--pattern", default="*.pdf", help="File pattern to match (default: *.pdf)")
    
    args = parser.parse_args()
    
    print("🔄 Batch PDF to Markdown Converter")
    print("=" * 50)
    
    # Find all PDFs
    pdf_files = find_all_pdfs(args.input_dir)
    
    if not pdf_files:
        print(f"❌ No PDF files found in: {args.input_dir}")
        return 1
    
    print(f"📚 Found {len(pdf_files)} PDF files")
    
    # Create output structure
    output_path = create_output_structure(args.output_dir)
    
    # Process batch
    results = process_batch(pdf_files, args.output_dir, args.compare)
    
    # Save summary
    save_batch_summary(results, args.output_dir)
    
    # Final report
    print("\n" + "=" * 60)
    print("🎉 BATCH CONVERSION COMPLETE")
    print("=" * 60)
    print(f"✅ Successful: {results['summary']['successful']}/{results['batch_info']['total_files']}")
    print(f"❌ Failed: {results['summary']['failed']}/{results['batch_info']['total_files']}")
    print(f"⏱️  Total time: {results['summary']['total_processing_time']:.1f}s")
    print(f"📁 Output location: {output_path}")
    
    if results['summary']['failed'] > 0:
        print(f"\n⚠️  {results['summary']['failed']} files failed conversion - check summary for details")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
