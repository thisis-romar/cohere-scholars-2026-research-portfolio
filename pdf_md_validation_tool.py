#!/usr/bin/env python3
"""
PDF-to-MD Content Validation Tool
=================================

Comprehensive validation system to ensure PDF content is accurately preserved 
in Markdown format including tables, images, mathematical notation, and 
structured academic content.

Key Features:
- PDF content extraction and parsing
- Markdown structure analysis
- Table preservation validation
- Image reference verification
- Mathematical notation comparison
- Academic formatting integrity check
- Detailed validation reporting

Usage:
    python pdf_md_validation_tool.py --source-dir "01-PAPERS" --target-dir "02-MARKDOWN" --converted-dir "converted_output"
"""

import os
import sys
import re
import json
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import argparse

# PDF processing libraries
try:
    import PyPDF2
    import pdfplumber
except ImportError:
    print("Installing required PDF processing libraries...")
    os.system("pip install PyPDF2 pdfplumber")
    import PyPDF2
    import pdfplumber

# Text processing libraries
try:
    import markdown
    from fuzzywuzzy import fuzz
    import nltk
    from nltk.tokenize import sent_tokenize, word_tokenize
except ImportError:
    print("Installing required text processing libraries...")
    os.system("pip install markdown fuzzywuzzy nltk python-Levenshtein")
    import markdown
    from fuzzywuzzy import fuzz
    import nltk
    
# Ensure NLTK data is downloaded
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

@dataclass
class ValidationResult:
    """Container for validation results"""
    file_pair: str
    text_similarity: float
    table_count_match: bool
    image_ref_count: int
    math_notation_match: bool
    structure_integrity: float
    issues: List[str]
    recommendations: List[str]
    validation_score: float

class PDFContentExtractor:
    """Extract and analyze content from PDF files"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def extract_text_content(self, pdf_path: str) -> Dict[str, Any]:
        """Extract text content from PDF using multiple methods"""
        content = {
            'text': '',
            'pages': [],
            'tables': [],
            'images': [],
            'metadata': {}
        }
        
        try:
            # Method 1: PyPDF2 for basic text extraction
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                content['metadata'] = {
                    'pages': len(pdf_reader.pages),
                    'title': getattr(pdf_reader.metadata, 'title', ''),
                    'author': getattr(pdf_reader.metadata, 'author', '')
                }
                
                for page_num, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()
                    content['pages'].append(page_text)
                    content['text'] += page_text + '\n'
            
            # Method 2: pdfplumber for enhanced extraction
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    # Extract tables
                    tables = page.extract_tables()
                    if tables:
                        content['tables'].extend([{
                            'page': page_num + 1,
                            'table_data': table,
                            'rows': len(table),
                            'cols': len(table[0]) if table else 0
                        } for table in tables])
                    
                    # Extract images
                    if hasattr(page, 'images'):
                        images = page.images
                        content['images'].extend([{
                            'page': page_num + 1,
                            'bbox': img['bbox'] if 'bbox' in img else None,
                            'size': (img.get('width', 0), img.get('height', 0))
                        } for img in images])
        
        except Exception as e:
            self.logger.error(f"Error extracting PDF content from {pdf_path}: {e}")
        
        return content
    
    def identify_mathematical_notation(self, text: str) -> List[str]:
        """Identify mathematical notation patterns in text"""
        math_patterns = [
            r'\$[^$]+\$',  # LaTeX inline math
            r'\$\$[^$]+\$\$',  # LaTeX display math
            r'\\[a-zA-Z]+\{[^}]*\}',  # LaTeX commands
            r'[0-9]+\.[0-9]+',  # Decimal numbers
            r'[a-zA-Z]\^[0-9]+',  # Superscripts
            r'[a-zA-Z]_[0-9]+',  # Subscripts
            r'≤|≥|≠|±|∞|∑|∏|∫',  # Mathematical symbols
        ]
        
        found_math = []
        for pattern in math_patterns:
            matches = re.findall(pattern, text)
            found_math.extend(matches)
        
        return found_math

class MarkdownContentAnalyzer:
    """Analyze and validate Markdown content structure"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def parse_markdown_content(self, md_path: str) -> Dict[str, Any]:
        """Parse Markdown content and extract structural elements"""
        content = {
            'text': '',
            'headers': [],
            'tables': [],
            'images': [],
            'links': [],
            'code_blocks': [],
            'lists': [],
            'metadata': {}
        }
        
        try:
            with open(md_path, 'r', encoding='utf-8') as file:
                md_text = file.read()
                content['text'] = md_text
                
                # Extract headers
                headers = re.findall(r'^(#{1,6})\s+(.+)$', md_text, re.MULTILINE)
                content['headers'] = [{'level': len(h[0]), 'text': h[1]} for h in headers]
                
                # Extract tables (Markdown table format)
                table_pattern = r'\|[^|\n]*\|[^|\n]*\|'
                tables = re.findall(table_pattern, md_text)
                content['tables'] = [{
                    'row_data': table.strip(),
                    'columns': len(table.split('|')) - 2  # Subtract empty start/end
                } for table in tables]
                
                # Extract images
                img_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
                images = re.findall(img_pattern, md_text)
                content['images'] = [{'alt': img[0], 'src': img[1]} for img in images]
                
                # Extract links
                link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
                links = re.findall(link_pattern, md_text)
                content['links'] = [{'text': link[0], 'url': link[1]} for link in links]
                
                # Extract code blocks
                code_pattern = r'```[^`]*```'
                code_blocks = re.findall(code_pattern, md_text, re.DOTALL)
                content['code_blocks'] = code_blocks
                
                # Extract lists
                list_pattern = r'^[-*+]\s+.+$'
                lists = re.findall(list_pattern, md_text, re.MULTILINE)
                content['lists'] = lists
                
                # Basic metadata
                content['metadata'] = {
                    'char_count': len(md_text),
                    'word_count': len(md_text.split()),
                    'line_count': len(md_text.split('\n'))
                }
        
        except Exception as e:
            self.logger.error(f"Error parsing Markdown content from {md_path}: {e}")
        
        return content

class ContentValidator:
    """Main validation engine for comparing PDF and Markdown content"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.pdf_extractor = PDFContentExtractor()
        self.md_analyzer = MarkdownContentAnalyzer()
    
    def calculate_text_similarity(self, pdf_text: str, md_text: str) -> float:
        """Calculate text similarity between PDF and Markdown content"""
        # Clean and normalize text for comparison
        pdf_clean = self._clean_text(pdf_text)
        md_clean = self._clean_text(md_text)
        
        # Use fuzzy matching for similarity
        similarity = fuzz.ratio(pdf_clean, md_clean) / 100.0
        
        return similarity
    
    def _clean_text(self, text: str) -> str:
        """Clean text for comparison by removing formatting artifacts"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters that might be artifacts
        text = re.sub(r'[^\w\s.,!?;:()\-]', '', text)
        # Convert to lowercase for comparison
        text = text.lower().strip()
        return text
    
    def validate_table_preservation(self, pdf_content: Dict, md_content: Dict) -> Tuple[bool, List[str]]:
        """Validate that tables are properly preserved in Markdown"""
        issues = []
        
        pdf_table_count = len(pdf_content.get('tables', []))
        md_table_count = len(md_content.get('tables', []))
        
        if pdf_table_count == 0 and md_table_count == 0:
            return True, []
        
        if pdf_table_count != md_table_count:
            issues.append(f"Table count mismatch: PDF has {pdf_table_count}, MD has {md_table_count}")
        
        # Detailed table structure comparison
        for i, pdf_table in enumerate(pdf_content.get('tables', [])):
            if i < len(md_content.get('tables', [])):
                md_table = md_content['tables'][i]
                
                if pdf_table.get('rows', 0) > 0:
                    if 'columns' in md_table and pdf_table.get('cols', 0) != md_table['columns']:
                        issues.append(f"Table {i+1} column mismatch: PDF has {pdf_table.get('cols', 0)}, MD has {md_table['columns']}")
            else:
                issues.append(f"PDF table {i+1} not found in Markdown")
        
        return len(issues) == 0, issues
    
    def validate_image_references(self, pdf_content: Dict, md_content: Dict) -> Tuple[int, List[str]]:
        """Validate image references between PDF and Markdown"""
        issues = []
        
        pdf_image_count = len(pdf_content.get('images', []))
        md_image_count = len(md_content.get('images', []))
        
        if pdf_image_count != md_image_count:
            issues.append(f"Image count mismatch: PDF has {pdf_image_count}, MD has {md_image_count}")
        
        # Check if MD images have valid references
        for i, img in enumerate(md_content.get('images', [])):
            if not img.get('src'):
                issues.append(f"Image {i+1} in MD has no source reference")
            elif not img.get('alt'):
                issues.append(f"Image {i+1} in MD has no alt text")
        
        return md_image_count, issues
    
    def validate_mathematical_notation(self, pdf_text: str, md_text: str) -> Tuple[bool, List[str]]:
        """Validate mathematical notation preservation"""
        issues = []
        
        pdf_math = self.pdf_extractor.identify_mathematical_notation(pdf_text)
        md_math = self.pdf_extractor.identify_mathematical_notation(md_text)
        
        if len(pdf_math) != len(md_math):
            issues.append(f"Mathematical notation count mismatch: PDF has {len(pdf_math)}, MD has {len(md_math)}")
        
        # Check for common mathematical notation preservation
        math_symbols = ['±', '≤', '≥', '≠', '∞', '∑', '∏', '∫']
        for symbol in math_symbols:
            pdf_count = pdf_text.count(symbol)
            md_count = md_text.count(symbol)
            if pdf_count != md_count:
                issues.append(f"Math symbol '{symbol}' count mismatch: PDF has {pdf_count}, MD has {md_count}")
        
        return len(issues) == 0, issues
    
    def calculate_structure_integrity(self, pdf_content: Dict, md_content: Dict) -> float:
        """Calculate overall structural integrity score"""
        scores = []
        
        # Header structure score (0-1)
        if md_content.get('headers'):
            header_score = min(1.0, len(md_content['headers']) / 10)  # Assume ~10 headers is good
            scores.append(header_score)
        
        # Content length score (0-1)
        pdf_length = len(pdf_content.get('text', ''))
        md_length = len(md_content.get('text', ''))
        if pdf_length > 0:
            length_score = min(1.0, md_length / pdf_length)
            scores.append(length_score)
        
        # Table preservation score (0-1)
        pdf_tables = len(pdf_content.get('tables', []))
        md_tables = len(md_content.get('tables', []))
        if pdf_tables > 0:
            table_score = min(1.0, md_tables / pdf_tables)
            scores.append(table_score)
        
        return sum(scores) / len(scores) if scores else 0.0
    
    def validate_file_pair(self, pdf_path: str, md_path: str) -> ValidationResult:
        """Validate a PDF-Markdown file pair"""
        self.logger.info(f"Validating: {pdf_path} -> {md_path}")
        
        # Extract content from both files
        pdf_content = self.pdf_extractor.extract_text_content(pdf_path)
        md_content = self.md_analyzer.parse_markdown_content(md_path)
        
        # Perform validations
        text_similarity = self.calculate_text_similarity(
            pdf_content.get('text', ''), 
            md_content.get('text', '')
        )
        
        table_match, table_issues = self.validate_table_preservation(pdf_content, md_content)
        image_count, image_issues = self.validate_image_references(pdf_content, md_content)
        math_match, math_issues = self.validate_mathematical_notation(
            pdf_content.get('text', ''), 
            md_content.get('text', '')
        )
        
        structure_score = self.calculate_structure_integrity(pdf_content, md_content)
        
        # Compile all issues
        all_issues = table_issues + image_issues + math_issues
        
        # Generate recommendations
        recommendations = []
        if text_similarity < 0.8:
            recommendations.append("Consider reviewing text extraction - significant content differences detected")
        if not table_match:
            recommendations.append("Review table conversion process - structure may be lost")
        if image_count == 0 and len(pdf_content.get('images', [])) > 0:
            recommendations.append("Add image references to maintain document completeness")
        if structure_score < 0.7:
            recommendations.append("Improve structural preservation - headers and organization may be incomplete")
        
        # Calculate overall validation score
        validation_score = (
            text_similarity * 0.4 + 
            (1.0 if table_match else 0.0) * 0.2 + 
            (1.0 if math_match else 0.0) * 0.2 + 
            structure_score * 0.2
        )
        
        return ValidationResult(
            file_pair=f"{os.path.basename(pdf_path)} -> {os.path.basename(md_path)}",
            text_similarity=text_similarity,
            table_count_match=table_match,
            image_ref_count=image_count,
            math_notation_match=math_match,
            structure_integrity=structure_score,
            issues=all_issues,
            recommendations=recommendations,
            validation_score=validation_score
        )

class ValidationReporter:
    """Generate comprehensive validation reports"""
    
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.logger = logging.getLogger(__name__)
    
    def generate_summary_report(self, results: List[ValidationResult]) -> str:
        """Generate summary validation report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.output_dir / f"validation_summary_{timestamp}.md"
        
        # Calculate summary statistics
        total_files = len(results)
        avg_text_similarity = sum(r.text_similarity for r in results) / total_files
        avg_validation_score = sum(r.validation_score for r in results) / total_files
        table_preservation_rate = sum(1 for r in results if r.table_count_match) / total_files
        math_preservation_rate = sum(1 for r in results if r.math_notation_match) / total_files
        
        # Generate report content
        report_content = f"""# PDF-to-Markdown Validation Report

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Total Files Validated:** {total_files}

## Summary Statistics

| Metric | Score | Grade |
|--------|-------|-------|
| Average Text Similarity | {avg_text_similarity:.3f} | {'A' if avg_text_similarity > 0.9 else 'B' if avg_text_similarity > 0.8 else 'C' if avg_text_similarity > 0.7 else 'D'} |
| Table Preservation Rate | {table_preservation_rate:.3f} | {'A' if table_preservation_rate > 0.9 else 'B' if table_preservation_rate > 0.8 else 'C' if table_preservation_rate > 0.7 else 'D'} |
| Mathematical Notation Preservation | {math_preservation_rate:.3f} | {'A' if math_preservation_rate > 0.9 else 'B' if math_preservation_rate > 0.8 else 'C' if math_preservation_rate > 0.7 else 'D'} |
| Overall Validation Score | {avg_validation_score:.3f} | {'A' if avg_validation_score > 0.9 else 'B' if avg_validation_score > 0.8 else 'C' if avg_validation_score > 0.7 else 'D'} |

## Detailed Results

| File Pair | Text Sim | Tables | Images | Math | Structure | Score | Issues |
|-----------|----------|--------|--------|------|-----------|-------|--------|
"""
        
        for result in sorted(results, key=lambda x: x.validation_score, reverse=True):
            report_content += f"| {result.file_pair} | {result.text_similarity:.3f} | {'✓' if result.table_count_match else '✗'} | {result.image_ref_count} | {'✓' if result.math_notation_match else '✗'} | {result.structure_integrity:.3f} | {result.validation_score:.3f} | {len(result.issues)} |\n"
        
        # Add recommendations section
        report_content += "\n## Recommendations\n\n"
        all_recommendations = set()
        for result in results:
            all_recommendations.update(result.recommendations)
        
        for i, rec in enumerate(sorted(all_recommendations), 1):
            report_content += f"{i}. {rec}\n"
        
        # Add issues summary
        report_content += "\n## Common Issues\n\n"
        all_issues = []
        for result in results:
            all_issues.extend(result.issues)
        
        issue_counts = {}
        for issue in all_issues:
            issue_type = issue.split(':')[0]
            issue_counts[issue_type] = issue_counts.get(issue_type, 0) + 1
        
        for issue_type, count in sorted(issue_counts.items(), key=lambda x: x[1], reverse=True):
            report_content += f"- **{issue_type}:** {count} occurrences\n"
        
        # Write report
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        self.logger.info(f"Summary report generated: {report_path}")
        return str(report_path)
    
    def generate_detailed_report(self, result: ValidationResult) -> str:
        """Generate detailed report for a single file pair"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = re.sub(r'[^\w\-_.]', '_', result.file_pair)
        report_path = self.output_dir / f"detailed_{safe_filename}_{timestamp}.md"
        
        report_content = f"""# Detailed Validation Report

**File Pair:** {result.file_pair}  
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Validation Scores

- **Text Similarity:** {result.text_similarity:.3f}
- **Table Preservation:** {'✓ Passed' if result.table_count_match else '✗ Failed'}
- **Image References:** {result.image_ref_count} found
- **Mathematical Notation:** {'✓ Preserved' if result.math_notation_match else '✗ Issues found'}
- **Structure Integrity:** {result.structure_integrity:.3f}
- **Overall Score:** {result.validation_score:.3f}

## Issues Identified

"""
        
        if result.issues:
            for i, issue in enumerate(result.issues, 1):
                report_content += f"{i}. {issue}\n"
        else:
            report_content += "No issues identified.\n"
        
        report_content += "\n## Recommendations\n\n"
        
        if result.recommendations:
            for i, rec in enumerate(result.recommendations, 1):
                report_content += f"{i}. {rec}\n"
        else:
            report_content += "No specific recommendations.\n"
        
        # Write detailed report
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        return str(report_path)

class ValidationOrchestrator:
    """Main orchestrator for the validation process"""
    
    def __init__(self, source_dir: str, target_dir: str, converted_dir: str, output_dir: str = "validation_reports"):
        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir)
        self.converted_dir = Path(converted_dir)
        self.output_dir = Path(output_dir)
        
        self.validator = ContentValidator()
        self.reporter = ValidationReporter(str(self.output_dir))
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.output_dir / 'validation.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def find_file_pairs(self) -> List[Tuple[str, str]]:
        """Find matching PDF and Markdown file pairs"""
        pairs = []
        
        # Look for PDF files in source directory
        for pdf_path in self.source_dir.rglob("*.pdf"):
            # Try to find corresponding MD file in converted directory first
            pdf_name = pdf_path.stem
            
            # Look for raw conversion files first
            converted_candidates = list(self.converted_dir.glob(f"*{pdf_name}*.md"))
            if converted_candidates:
                md_path = converted_candidates[0]  # Use first match
                pairs.append((str(pdf_path), str(md_path)))
                continue
            
            # Fallback to analysis files in target directory
            target_candidates = list(self.target_dir.rglob(f"*{pdf_name}*.md"))
            if target_candidates:
                md_path = target_candidates[0]  # Use first match
                pairs.append((str(pdf_path), str(md_path)))
        
        self.logger.info(f"Found {len(pairs)} PDF-MD file pairs for validation")
        return pairs
    
    def run_validation(self, max_files: Optional[int] = None) -> List[ValidationResult]:
        """Run validation on all file pairs"""
        pairs = self.find_file_pairs()
        
        if max_files:
            pairs = pairs[:max_files]
            self.logger.info(f"Limiting validation to {max_files} files")
        
        results = []
        
        for i, (pdf_path, md_path) in enumerate(pairs, 1):
            self.logger.info(f"Processing {i}/{len(pairs)}: {os.path.basename(pdf_path)}")
            
            try:
                result = self.validator.validate_file_pair(pdf_path, md_path)
                results.append(result)
                
                # Generate detailed report for files with issues
                if result.issues or result.validation_score < 0.8:
                    self.reporter.generate_detailed_report(result)
                
            except Exception as e:
                self.logger.error(f"Error validating {pdf_path}: {e}")
                continue
        
        # Generate summary report
        if results:
            summary_path = self.reporter.generate_summary_report(results)
            self.logger.info(f"Validation complete. Summary: {summary_path}")
        
        return results

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="PDF-to-MD Content Validation Tool")
    parser.add_argument("--source-dir", default="01-PAPERS", help="Directory containing PDF files")
    parser.add_argument("--target-dir", default="02-MARKDOWN", help="Directory containing MD analysis files")
    parser.add_argument("--converted-dir", default="converted_output", help="Directory containing raw MD conversion files")
    parser.add_argument("--output-dir", default="validation_reports", help="Output directory for reports")
    parser.add_argument("--max-files", type=int, help="Maximum number of files to validate")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    
    args = parser.parse_args()
    
    # Initialize orchestrator
    orchestrator = ValidationOrchestrator(
        source_dir=args.source_dir,
        target_dir=args.target_dir,
        converted_dir=args.converted_dir,
        output_dir=args.output_dir
    )
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    print("🔍 PDF-to-MD Content Validation Tool")
    print("=" * 50)
    print(f"Source PDFs: {args.source_dir}")
    print(f"Target MDs: {args.target_dir}")
    print(f"Converted MDs: {args.converted_dir}")
    print(f"Output: {args.output_dir}")
    print()
    
    # Run validation
    try:
        results = orchestrator.run_validation(max_files=args.max_files)
        
        if results:
            avg_score = sum(r.validation_score for r in results) / len(results)
            print(f"\n✅ Validation complete!")
            print(f"📊 Files processed: {len(results)}")
            print(f"📈 Average validation score: {avg_score:.3f}")
            print(f"📁 Reports saved to: {args.output_dir}")
        else:
            print("\n❌ No files were successfully validated.")
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Validation interrupted by user.")
    except Exception as e:
        print(f"\n❌ Validation failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
