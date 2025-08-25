# Word-for-Word PDF to Markdown Converter
# Validated implementation using multiple high-accuracy libraries

import os
import sys
import logging
from pathlib import Path
from typing import Optional, Dict, Any
import json
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PDFToMarkdownConverter:
    """
    Comprehensive PDF to Markdown converter using validated libraries
    Ensures word-for-word conversion with maximum accuracy
    """
    
    def __init__(self, output_dir: str = "converted_output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Track available converters
        self.available_converters = []
        self._check_dependencies()
    
    def _check_dependencies(self):
        """Check which conversion libraries are available"""
        
        # Check Marker (highest accuracy)
        try:
            import marker
            self.available_converters.append("marker")
            logger.info("✅ Marker available (highest accuracy)")
        except ImportError:
            logger.warning("❌ Marker not available. Install with: pip install marker-pdf")
        
        # Check MarkItDown (Microsoft)
        try:
            import markitdown
            self.available_converters.append("markitdown")
            logger.info("✅ MarkItDown available (Microsoft)")
        except ImportError:
            logger.warning("❌ MarkItDown not available. Install with: pip install markitdown")
        
        # Check Unstructured
        try:
            import unstructured
            self.available_converters.append("unstructured")
            logger.info("✅ Unstructured available")
        except ImportError:
            logger.warning("❌ Unstructured not available. Install with: pip install 'unstructured[all-docs]'")
        
        # Check PyMuPDF4LLM
        try:
            import pymupdf4llm
            self.available_converters.append("pymupdf4llm")
            logger.info("✅ PyMuPDF4LLM available")
        except ImportError:
            logger.warning("❌ PyMuPDF4LLM not available. Install with: pip install pymupdf4llm")
        
        if not self.available_converters:
            logger.error("❌ No conversion libraries available! Install at least one.")
            raise RuntimeError("No PDF conversion libraries available")
    
    def convert_with_marker(self, pdf_path: str) -> Dict[str, Any]:
        """
        Convert using Marker (highest accuracy - 95.67% benchmark)
        """
        try:
            from marker.converters.pdf import PdfConverter
            from marker.models import create_model_dict
            from marker.output import text_from_rendered
            
            logger.info(f"🎯 Converting with Marker: {pdf_path}")
            
            converter = PdfConverter(
                artifact_dict=create_model_dict(),
            )
            
            rendered = converter(pdf_path)
            text, metadata, images = text_from_rendered(rendered)
            
            return {
                "method": "marker",
                "text": text,
                "metadata": metadata,
                "images": images,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"❌ Marker conversion failed: {e}")
            return {"method": "marker", "success": False, "error": str(e)}
    
    def convert_with_markitdown(self, pdf_path: str) -> Dict[str, Any]:
        """
        Convert using Microsoft MarkItDown (what we're currently using)
        """
        try:
            from markitdown import MarkItDown
            
            logger.info(f"🔧 Converting with MarkItDown: {pdf_path}")
            
            md = MarkItDown()
            result = md.convert(pdf_path)
            
            return {
                "method": "markitdown",
                "text": result.text_content,
                "metadata": {"title": getattr(result, 'title', 'Unknown')},
                "success": True
            }
            
        except Exception as e:
            logger.error(f"❌ MarkItDown conversion failed: {e}")
            return {"method": "markitdown", "success": False, "error": str(e)}
    
    def convert_with_unstructured(self, pdf_path: str) -> Dict[str, Any]:
        """
        Convert using Unstructured (enterprise-grade)
        """
        try:
            from unstructured.partition.auto import partition
            
            logger.info(f"🏢 Converting with Unstructured: {pdf_path}")
            
            elements = partition(filename=pdf_path)
            text = "\n\n".join([str(el) for el in elements])
            
            return {
                "method": "unstructured",
                "text": text,
                "metadata": {"elements_count": len(elements)},
                "success": True
            }
            
        except Exception as e:
            logger.error(f"❌ Unstructured conversion failed: {e}")
            return {"method": "unstructured", "success": False, "error": str(e)}
    
    def convert_with_pymupdf4llm(self, pdf_path: str) -> Dict[str, Any]:
        """
        Convert using PyMuPDF4LLM (optimized for LLMs)
        """
        try:
            import pymupdf4llm
            
            logger.info(f"📚 Converting with PyMuPDF4LLM: {pdf_path}")
            
            text = pymupdf4llm.to_markdown(pdf_path)
            
            return {
                "method": "pymupdf4llm",
                "text": text,
                "metadata": {"source": "pymupdf4llm"},
                "success": True
            }
            
        except Exception as e:
            logger.error(f"❌ PyMuPDF4LLM conversion failed: {e}")
            return {"method": "pymupdf4llm", "success": False, "error": str(e)}
    
    def convert_pdf(self, pdf_path: str, method: str = "auto") -> Dict[str, Any]:
        """
        Convert PDF to markdown using specified method or auto-select best available
        
        Args:
            pdf_path: Path to PDF file
            method: Conversion method ("auto", "marker", "markitdown", "unstructured", "pymupdf4llm")
        
        Returns:
            Dictionary with conversion results
        """
        
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        # Auto-select best available method
        if method == "auto":
            if "marker" in self.available_converters:
                method = "marker"  # Highest accuracy
            elif "markitdown" in self.available_converters:
                method = "markitdown"  # Microsoft, reliable
            elif "pymupdf4llm" in self.available_converters:
                method = "pymupdf4llm"  # Good for academic papers
            elif "unstructured" in self.available_converters:
                method = "unstructured"  # Enterprise grade
            else:
                raise RuntimeError("No conversion methods available")
        
        # Execute conversion
        if method == "marker" and "marker" in self.available_converters:
            result = self.convert_with_marker(pdf_path)
        elif method == "markitdown" and "markitdown" in self.available_converters:
            result = self.convert_with_markitdown(pdf_path)
        elif method == "unstructured" and "unstructured" in self.available_converters:
            result = self.convert_with_unstructured(pdf_path)
        elif method == "pymupdf4llm" and "pymupdf4llm" in self.available_converters:
            result = self.convert_with_pymupdf4llm(pdf_path)
        else:
            raise ValueError(f"Method '{method}' not available. Available: {self.available_converters}")
        
        return result
    
    def convert_and_save(self, pdf_path: str, method: str = "auto", compare_methods: bool = False) -> str:
        """
        Convert PDF and save to markdown file
        
        Args:
            pdf_path: Path to PDF file
            method: Conversion method
            compare_methods: If True, try all available methods and save comparison
        
        Returns:
            Path to saved markdown file
        """
        
        pdf_name = Path(pdf_path).stem
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if compare_methods:
            # Try all available methods and compare
            results = {}
            for conv_method in self.available_converters:
                try:
                    result = self.convert_pdf(pdf_path, conv_method)
                    if result["success"]:
                        results[conv_method] = result
                        logger.info(f"✅ {conv_method}: {len(result['text'])} chars")
                    else:
                        logger.warning(f"❌ {conv_method}: {result.get('error', 'Unknown error')}")
                except Exception as e:
                    logger.warning(f"❌ {conv_method}: {e}")
            
            # Save comparison report
            comparison_file = self.output_dir / f"{pdf_name}_comparison_{timestamp}.json"
            with open(comparison_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "pdf_path": pdf_path,
                    "timestamp": timestamp,
                    "results": {k: {
                        "method": v["method"],
                        "text_length": len(v["text"]),
                        "metadata": v["metadata"],
                        "success": v["success"]
                    } for k, v in results.items()}
                }, f, indent=2)
            
            logger.info(f"📊 Comparison saved: {comparison_file}")
            
            # Use the best result (prefer marker, then markitdown, etc.)
            best_method = None
            for preferred in ["marker", "markitdown", "pymupdf4llm", "unstructured"]:
                if preferred in results:
                    best_method = preferred
                    break
            
            if best_method:
                result = results[best_method]
                logger.info(f"🏆 Using best result from: {best_method}")
            else:
                raise RuntimeError("No successful conversions")
        
        else:
            # Single method conversion
            result = self.convert_pdf(pdf_path, method)
            if not result["success"]:
                raise RuntimeError(f"Conversion failed: {result.get('error', 'Unknown error')}")
        
        # Save markdown file
        output_file = self.output_dir / f"{pdf_name}_RAW_CONVERSION_{result['method']}_{timestamp}.md"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# Raw PDF Conversion: {pdf_name}\n\n")
            f.write(f"**Source**: {pdf_path}\n")
            f.write(f"**Method**: {result['method']}\n")
            f.write(f"**Converted**: {timestamp}\n")
            f.write(f"**Length**: {len(result['text'])} characters\n\n")
            f.write("---\n\n")
            f.write(result['text'])
        
        logger.info(f"💾 Saved: {output_file}")
        return str(output_file)

def main():
    """Command line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Word-for-word PDF to Markdown converter")
    parser.add_argument("pdf_path", help="Path to PDF file")
    parser.add_argument("--method", default="auto", 
                       choices=["auto", "marker", "markitdown", "unstructured", "pymupdf4llm"],
                       help="Conversion method")
    parser.add_argument("--compare", action="store_true", 
                       help="Compare all available methods")
    parser.add_argument("--output-dir", default="converted_output",
                       help="Output directory")
    
    args = parser.parse_args()
    
    try:
        converter = PDFToMarkdownConverter(args.output_dir)
        
        print(f"\n🚀 Converting PDF: {args.pdf_path}")
        print(f"📋 Available methods: {converter.available_converters}")
        
        output_file = converter.convert_and_save(
            args.pdf_path, 
            method=args.method,
            compare_methods=args.compare
        )
        
        print(f"\n✅ Conversion complete!")
        print(f"📄 Output: {output_file}")
        
    except Exception as e:
        logger.error(f"❌ Conversion failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
