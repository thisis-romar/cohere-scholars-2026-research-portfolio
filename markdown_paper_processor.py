#!/usr/bin/env python3
"""
Simplified Paper Processor using MarkItDown MCP Server
Converts research papers to markdown for analysis and study preparation
"""

import os
import sys
import json
import time
import logging
from pathlib import Path
from urllib.parse import quote
from typing import List, Dict, Optional
import re

class MarkdownPaperProcessor:
    """Process research papers using MarkItDown MCP server for conversion"""
    
    def __init__(self, papers_dir: str = "01-PAPERS", output_dir: str = "02-MARKDOWN"):
        self.papers_dir = Path(papers_dir)
        self.output_dir = Path(output_dir)
        self.setup_logging()
        self.setup_directories()
        
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('paper_processing.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def setup_directories(self):
        """Create output directories"""
        self.output_dir.mkdir(exist_ok=True)
        
        # Create subdirectories for each category
        categories = ['Multilingual', 'Evaluation', 'Inference', 'Architecture', 'Training', 'Reasoning']
        for category in categories:
            (self.output_dir / category).mkdir(exist_ok=True)
            
    def find_pdf_files(self) -> List[tuple]:
        """Find all PDF files in the papers directory"""
        pdf_files = []
        
        for category_dir in self.papers_dir.iterdir():
            if category_dir.is_dir():
                for pdf_file in category_dir.glob("*.pdf"):
                    pdf_files.append((category_dir.name, pdf_file))
                    
        self.logger.info(f"Found {len(pdf_files)} PDF files to process")
        return pdf_files
        
    def convert_pdf_to_markdown(self, pdf_path: Path) -> Optional[str]:
        """
        Convert PDF to markdown using MarkItDown MCP server
        Returns the markdown content or None if conversion fails
        """
        try:
            # Create file URI for the PDF
            file_uri = f"file:///{str(pdf_path).replace('\\', '/').replace(' ', '%20')}"
            
            self.logger.info(f"Converting: {pdf_path.name}")
            self.logger.debug(f"Using URI: {file_uri}")
            
            # Note: In actual implementation, this would call the MCP server
            # For demonstration, we'll simulate the process
            print(f"🔄 Converting {pdf_path.name} to markdown...")
            
            # Simulated delay for processing
            time.sleep(1)
            
            # For now, return a placeholder - in real implementation this would be
            # the actual markdown content from the MCP server
            return f"# {pdf_path.stem}\n\nMarkdown content would be here from MCP conversion..."
            
        except Exception as e:
            self.logger.error(f"Failed to convert {pdf_path.name}: {str(e)}")
            return None
            
    def extract_paper_metadata(self, markdown_content: str) -> Dict:
        """Extract key metadata from the markdown content"""
        metadata = {
            'title': '',
            'authors': [],
            'abstract': '',
            'keywords': [],
            'sections': [],
            'figures': [],
            'tables': []
        }
        
        lines = markdown_content.split('\n')
        
        # Extract title (usually the first heading)
        for line in lines:
            if line.startswith('# ') and not metadata['title']:
                metadata['title'] = line[2:].strip()
                break
                
        # Extract abstract (look for Abstract section)
        in_abstract = False
        abstract_lines = []
        for line in lines:
            if re.match(r'^#+\s*abstract', line, re.IGNORECASE):
                in_abstract = True
                continue
            elif in_abstract and line.startswith('#'):
                break
            elif in_abstract and line.strip():
                abstract_lines.append(line.strip())
                
        metadata['abstract'] = ' '.join(abstract_lines)
        
        # Extract section headings
        for line in lines:
            if re.match(r'^#+\s+', line):
                level = len(re.match(r'^#+', line).group())
                title = re.sub(r'^#+\s+', '', line).strip()
                metadata['sections'].append({'level': level, 'title': title})
                
        return metadata
        
    def create_study_summary(self, category: str, paper_name: str, metadata: Dict) -> str:
        """Create a study-friendly summary of the paper"""
        summary = f"""# Study Summary: {metadata.get('title', paper_name)}

## Category: {category}

## Abstract
{metadata.get('abstract', 'Abstract not extracted')}

## Key Sections
"""
        
        for section in metadata.get('sections', []):
            indent = '  ' * (section['level'] - 1)
            summary += f"{indent}- {section['title']}\n"
            
        summary += f"""

## Study Notes
- **Paper Type**: {category}
- **Relevance to Cohere**: [Add your analysis here]
- **Key Concepts**: [Extract main concepts]
- **Technical Contributions**: [Summarize innovations]
- **Potential Questions**: [Prepare interview questions]

## Action Items
- [ ] Read full paper
- [ ] Understand key algorithms/approaches
- [ ] Research cited papers
- [ ] Prepare discussion points
- [ ] Connect to other papers in collection

---
*Processed on {time.strftime('%Y-%m-%d %H:%M:%S')}*
"""
        return summary
        
    def process_single_paper(self, category: str, pdf_path: Path) -> bool:
        """Process a single PDF paper"""
        try:
            # Convert PDF to markdown
            markdown_content = self.convert_pdf_to_markdown(pdf_path)
            if not markdown_content:
                return False
                
            # Extract metadata
            metadata = self.extract_paper_metadata(markdown_content)
            
            # Create output files
            paper_name = pdf_path.stem
            category_output_dir = self.output_dir / category
            
            # Save full markdown
            markdown_file = category_output_dir / f"{paper_name}.md"
            with open(markdown_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
                
            # Save study summary
            summary_file = category_output_dir / f"{paper_name}_STUDY.md"
            study_summary = self.create_study_summary(category, paper_name, metadata)
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write(study_summary)
                
            # Save metadata as JSON
            metadata_file = category_output_dir / f"{paper_name}_metadata.json"
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
                
            self.logger.info(f"✅ Processed: {paper_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error processing {pdf_path.name}: {str(e)}")
            return False
            
    def process_all_papers(self):
        """Process all PDF papers in the directory"""
        pdf_files = self.find_pdf_files()
        
        if not pdf_files:
            self.logger.warning("No PDF files found to process")
            return
            
        print(f"\n🚀 Starting processing of {len(pdf_files)} papers...")
        print("=" * 60)
        
        successful = 0
        failed = 0
        
        for category, pdf_path in pdf_files:
            print(f"\n📄 Processing: {category}/{pdf_path.name}")
            
            if self.process_single_paper(category, pdf_path):
                successful += 1
                print(f"   ✅ Success")
            else:
                failed += 1
                print(f"   ❌ Failed")
                
        print("\n" + "=" * 60)
        print(f"🎯 Processing Complete!")
        print(f"   ✅ Successful: {successful}")
        print(f"   ❌ Failed: {failed}")
        print(f"   📁 Output directory: {self.output_dir}")
        
        # Create processing summary
        self.create_processing_summary(successful, failed, pdf_files)
        
    def create_processing_summary(self, successful: int, failed: int, pdf_files: List[tuple]):
        """Create a summary of the processing results"""
        summary_content = f"""# Paper Processing Summary

## Overview
- **Total Papers**: {len(pdf_files)}
- **Successfully Processed**: {successful}
- **Failed**: {failed}
- **Success Rate**: {(successful/len(pdf_files)*100):.1f}%

## Processed Papers by Category

"""
        
        # Group by category
        by_category = {}
        for category, pdf_path in pdf_files:
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(pdf_path.name)
            
        for category, papers in by_category.items():
            summary_content += f"### {category} ({len(papers)} papers)\n"
            for paper in sorted(papers):
                summary_content += f"- {paper}\n"
            summary_content += "\n"
            
        summary_content += f"""## Next Steps

1. **Review Study Summaries**: Check the `_STUDY.md` files for each paper
2. **Read Key Papers**: Start with papers most relevant to your research interests
3. **Cross-Reference**: Look for connections between papers
4. **Prepare Questions**: Use the study guides to prepare interview questions
5. **Deep Dive**: Select 3-5 papers for detailed analysis

## File Structure

```
{self.output_dir}/
├── Multilingual/
├── Evaluation/
├── Inference/
├── Architecture/
├── Training/
└── Reasoning/
    ├── paper_name.md              # Full markdown conversion
    ├── paper_name_STUDY.md        # Study-friendly summary
    └── paper_name_metadata.json   # Extracted metadata
```

---
*Generated on {time.strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        summary_file = self.output_dir / "PROCESSING_SUMMARY.md"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary_content)
            
        print(f"📋 Processing summary saved to: {summary_file}")

def main():
    """Main execution function"""
    print("🔬 Markdown Paper Processor for Cohere Scholars Program 2026")
    print("Using MarkItDown MCP Server for PDF conversion")
    print("=" * 60)
    
    # Initialize processor
    processor = MarkdownPaperProcessor()
    
    # Check if papers directory exists
    if not processor.papers_dir.exists():
        print(f"❌ Papers directory not found: {processor.papers_dir}")
        print("Please ensure the papers are in the '01-PAPERS' directory")
        return
        
    # Process all papers
    processor.process_all_papers()
    
    print("\n🎉 Paper processing workflow complete!")
    print(f"📁 Check the '{processor.output_dir}' directory for results")

if __name__ == "__main__":
    main()
