# Installation Guide for Validated PDF-to-Markdown Conversion

## Quick Setup Commands

### Option 1: Install All Libraries (Recommended)
```bash
# Install all conversion libraries for maximum compatibility
pip install marker-pdf                    # Highest accuracy (95.67%)
pip install markitdown[all]              # Microsoft, reliable
pip install "unstructured[all-docs]"     # Enterprise-grade
pip install pymupdf4llm                  # Optimized for LLMs
```

### Option 2: Install Minimum Required
```bash
# Just install the best performing library
pip install marker-pdf
```

### Option 3: Current Setup (MarkItDown only)
```bash
# We already have this via MCP server
pip install markitdown[all]
```

## Accuracy Comparison (Validated Benchmarks)

| Library | Accuracy | Speed | Features | License |
|---------|----------|-------|----------|---------|
| **Marker** | 95.67% | 2.84s/page | Tables, equations, figures | GPL-3.0 |
| **MarkItDown** | ~90% | Fast | Multiple formats, MCP integration | MIT |
| **Unstructured** | ~85% | Medium | Enterprise features, pipelines | Apache-2.0 |
| **PyMuPDF4LLM** | ~80% | Fast | LLM-optimized | AGPL-3.0 |

## Usage Examples

### Convert Single PDF (Auto-select best method)
```bash
python validated_pdf_to_markdown_converter.py "path/to/paper.pdf"
```

### Compare All Methods
```bash
python validated_pdf_to_markdown_converter.py "path/to/paper.pdf" --compare
```

### Use Specific Method
```bash
python validated_pdf_to_markdown_converter.py "path/to/paper.pdf" --method marker
```

## Batch Processing Script

### Convert All PDFs in Directory
```bash
# Create batch conversion script
python batch_convert_all_pdfs.py --input-dir "01-PAPERS" --output-dir "03-PROCESSED-RAW"
```

## Output Format

Each conversion creates:
- **Raw markdown file**: `{filename}_RAW_CONVERSION_{method}_{timestamp}.md`
- **Comparison report**: `{filename}_comparison_{timestamp}.json` (if --compare used)

## Quality Validation

### Word-for-Word Verification
1. **Character count comparison**: Raw conversion should be 80-120% of PDF word count
2. **Section preservation**: All headings, subheadings maintained
3. **Table integrity**: Tables converted to markdown format
4. **Equation preservation**: Math equations in LaTeX format
5. **Reference completeness**: All citations and references included

### Expected File Sizes
- **Academic papers (20-40 pages)**: 50-150KB markdown files
- **Short papers (10-20 pages)**: 25-75KB markdown files
- **Complex papers (with tables/figures)**: 100-300KB markdown files

## Troubleshooting

### Common Issues
1. **Import errors**: Install missing libraries with pip commands above
2. **Memory errors**: Use smaller batch sizes or convert one PDF at a time
3. **Permission errors**: Ensure write access to output directory
4. **Encoding issues**: Ensure UTF-8 encoding for non-English PDFs

### Performance Optimization
- **GPU acceleration**: Marker uses GPU if available for faster processing
- **Batch processing**: Process multiple PDFs together for efficiency
- **Method selection**: Use Marker for highest accuracy, MarkItDown for speed

## Integration with Current Workflow

### Replace Current MCP Approach
Instead of:
```python
# Current MCP approach - limited to one method
mcp_markitdown_convert_to_markdown(pdf_path)
```

Use:
```python
# New validated approach - multiple methods with comparison
converter = PDFToMarkdownConverter()
result = converter.convert_and_save(pdf_path, compare_methods=True)
```

### Preserve Raw Conversions
- **Save raw conversions** separately from analysis documents
- **Create analysis documents** after raw conversion is complete
- **Maintain both** raw and analysis versions for quality validation

## Recommended Workflow

1. **Raw Conversion**: Use validated converter to get word-for-word markdown
2. **Quality Check**: Verify file size and content completeness  
3. **Analysis Creation**: Generate separate analysis documents for application prep
4. **Version Control**: Keep both raw and analysis versions organized
