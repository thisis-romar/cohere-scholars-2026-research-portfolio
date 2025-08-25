#!/usr/bin/env python3
"""
MarkItDown-Powered Paper Processor
Practical implementation using MarkItDown MCP server for PDF conversion

Author: Emblem Projects
Date: August 19, 2025
Purpose: Convert research PDFs to analyzable markdown and extract concepts
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

class MarkItDownPaperProcessor:
    """
    Practical paper processor using MarkItDown MCP server.
    Focuses on immediate value with existing tools.
    """
    
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self.papers_dir = self.base_dir / "01-PAPERS"
        self.output_dir = self.base_dir / "03-RESOURCES" / "Processed-Papers"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create output subdirectories
        (self.output_dir / "Markdown").mkdir(exist_ok=True)
        (self.output_dir / "Summaries").mkdir(exist_ok=True)
        (self.output_dir / "Concepts").mkdir(exist_ok=True)
        (self.output_dir / "Study-Notes").mkdir(exist_ok=True)
    
    def convert_pdf_with_markitdown(self, pdf_path: Path) -> str:
        """
        Convert PDF to markdown using MarkItDown MCP server.
        This is the core function that will use the actual MCP call.
        """
        print(f"📄 Converting {pdf_path.name} with MarkItDown...")
        
        # This will be the actual MCP call - for now showing structure
        # markdown_content = mcp_markitdown_convert_to_markdown(str(pdf_path))
        
        # For demonstration, create a structured template
        paper_title = pdf_path.stem.replace('_', ' ').title()
        
        markdown_content = f"""# {paper_title}

**Category**: {pdf_path.parent.name}  
**File**: {pdf_path.name}  
**Processed**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Abstract

[Abstract content will be extracted here by MarkItDown]

## 1. Introduction

[Introduction and background will be extracted here]

## 2. Related Work

[Literature review section will be extracted here]

## 3. Methodology

[Technical approach and implementation details will be extracted here]

### 3.1 Model Architecture
[Architecture details]

### 3.2 Training Process
[Training methodology]

### 3.3 Evaluation Setup
[Evaluation framework]

## 4. Experiments

[Experimental setup and configuration will be extracted here]

### 4.1 Datasets
[Dataset descriptions]

### 4.2 Baselines
[Baseline comparisons]

### 4.3 Metrics
[Evaluation metrics]

## 5. Results

[Performance results and analysis will be extracted here]

### 5.1 Main Results
[Primary findings]

### 5.2 Ablation Studies
[Component analysis]

### 5.3 Analysis
[Result interpretation]

## 6. Discussion

[Discussion and implications will be extracted here]

## 7. Conclusion

[Conclusions and future work will be extracted here]

## References

[Reference list will be extracted here]

---

**Note**: This is a template structure. The actual MarkItDown conversion will populate these sections with the real paper content, including:
- Extracted text from all sections
- Tables converted to markdown format
- Image descriptions and captions
- Mathematical equations (where possible)
- Preserved document structure and hierarchy

**Processing Information**:
- Source PDF: {pdf_path}
- Conversion Method: MarkItDown MCP Server
- Processing Date: {datetime.now().isoformat()}
"""
        
        return markdown_content
    
    def extract_key_information(self, markdown_content: str, category: str) -> Dict[str, Any]:
        """Extract structured information from markdown content."""
        
        # Parse sections
        sections = self._parse_sections(markdown_content)
        
        # Extract key components
        key_info = {
            'metadata': {
                'category': category,
                'word_count': len(markdown_content.split()),
                'section_count': len(sections),
                'processing_date': datetime.now().isoformat()
            },
            'structure': {
                'sections': [s['title'] for s in sections],
                'has_abstract': any('abstract' in s['title'].lower() for s in sections),
                'has_methodology': any('method' in s['title'].lower() for s in sections),
                'has_results': any('result' in s['title'].lower() for s in sections),
                'has_conclusion': any('conclusion' in s['title'].lower() for s in sections)
            },
            'content': {
                'abstract': self._extract_section_by_name(sections, 'abstract'),
                'introduction': self._extract_section_by_name(sections, 'introduction'),
                'methodology': self._extract_section_by_name(sections, 'method'),
                'results': self._extract_section_by_name(sections, 'result'),
                'conclusion': self._extract_section_by_name(sections, 'conclusion')
            },
            'extracted_elements': {
                'tables': self._extract_tables(markdown_content),
                'figures': self._extract_figures(markdown_content),
                'equations': self._extract_equations(markdown_content),
                'citations': self._extract_citations(markdown_content)
            }
        }
        
        return key_info
    
    def _parse_sections(self, content: str) -> List[Dict[str, str]]:
        """Parse markdown headers to identify sections."""
        sections = []
        lines = content.split('\n')
        current_section = None
        current_content = []
        
        for line in lines:
            if re.match(r'^#{1,6}\s+', line):
                # Save previous section
                if current_section:
                    sections.append({
                        'title': current_section.strip('#').strip(),
                        'content': '\n'.join(current_content).strip(),
                        'level': len(re.match(r'^#+', current_section).group())
                    })
                
                # Start new section
                current_section = line
                current_content = []
            else:
                current_content.append(line)
        
        # Add final section
        if current_section:
            sections.append({
                'title': current_section.strip('#').strip(),
                'content': '\n'.join(current_content).strip(),
                'level': len(re.match(r'^#+', current_section).group())
            })
        
        return sections
    
    def _extract_section_by_name(self, sections: List[Dict], name: str) -> str:
        """Extract content from a specific section by name."""
        for section in sections:
            if name.lower() in section['title'].lower():
                return section['content']
        return ""
    
    def _extract_tables(self, content: str) -> List[str]:
        """Extract markdown tables."""
        table_pattern = r'\|.*\|.*\n\|[-\s|:]+\|.*\n(\|.*\|.*\n)*'
        tables = re.findall(table_pattern, content, re.MULTILINE)
        return tables
    
    def _extract_figures(self, content: str) -> List[str]:
        """Extract figure references and descriptions."""
        fig_patterns = [
            r'!\[([^\]]*)\]\([^)]+\)',  # ![alt text](url)
            r'Figure \d+[:\.]?\s*([^\n]+)',  # Figure 1: description
            r'Fig\. \d+[:\.]?\s*([^\n]+)'   # Fig. 1: description
        ]
        
        figures = []
        for pattern in fig_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            figures.extend(matches)
        
        return figures
    
    def _extract_equations(self, content: str) -> List[str]:
        """Extract mathematical equations (LaTeX format)."""
        eq_patterns = [
            r'\$\$([^$]+)\$\$',  # $$equation$$
            r'\$([^$]+)\$',      # $equation$
            r'\\begin\{equation\}(.*?)\\end\{equation\}',  # LaTeX equations
        ]
        
        equations = []
        for pattern in eq_patterns:
            matches = re.findall(pattern, content, re.DOTALL)
            equations.extend(matches)
        
        return equations
    
    def _extract_citations(self, content: str) -> List[str]:
        """Extract citation patterns."""
        citation_patterns = [
            r'\[(\d+)\]',  # [1], [2], etc.
            r'\(([A-Za-z]+(?:\s+et\s+al\.?)?,?\s+\d{4}[a-z]?)\)',  # (Author, 2024)
            r'([A-Za-z]+\s+et\s+al\.\s+\(\d{4}\))',  # Author et al. (2024)
        ]
        
        citations = []
        for pattern in citation_patterns:
            matches = re.findall(pattern, content)
            citations.extend(matches)
        
        return list(set(citations))  # Remove duplicates
    
    def generate_concept_summary(self, key_info: Dict[str, Any], paper_name: str) -> Dict[str, Any]:
        """Generate concept summary for study purposes."""
        
        category = key_info['metadata']['category']
        
        # Create concept summary based on extracted information
        concept_summary = {
            'paper_info': {
                'name': paper_name,
                'category': category,
                'estimated_reading_time': key_info['metadata']['word_count'] // 200,  # 200 wpm
                'complexity': self._assess_complexity(key_info),
                'structure_quality': self._assess_structure_quality(key_info['structure'])
            },
            'key_concepts': {
                'main_contribution': self._extract_main_contribution(key_info),
                'methodology_type': self._identify_methodology_type(key_info),
                'evaluation_approach': self._identify_evaluation_approach(key_info),
                'datasets_used': self._identify_datasets(key_info),
                'performance_metrics': self._identify_metrics(key_info)
            },
            'study_guidance': {
                'focus_areas': self._generate_focus_areas(category),
                'key_questions': self._generate_study_questions(category, key_info),
                'related_concepts': self._identify_related_concepts(category),
                'application_relevance': self._assess_cohere_relevance(category)
            },
            'practical_insights': {
                'technical_innovations': [],
                'implementation_notes': [],
                'limitations_mentioned': [],
                'future_directions': []
            }
        }
        
        return concept_summary
    
    def _assess_complexity(self, key_info: Dict) -> str:
        """Assess paper complexity for study planning."""
        word_count = key_info['metadata']['word_count']
        has_methodology = key_info['structure']['has_methodology']
        equation_count = len(key_info['extracted_elements']['equations'])
        
        if word_count > 8000 and has_methodology and equation_count > 5:
            return "High"
        elif word_count > 5000 and (has_methodology or equation_count > 2):
            return "Medium"
        else:
            return "Accessible"
    
    def _assess_structure_quality(self, structure: Dict) -> str:
        """Assess how well-structured the paper is."""
        required_sections = ['has_abstract', 'has_methodology', 'has_results', 'has_conclusion']
        present_sections = sum(structure[section] for section in required_sections)
        
        if present_sections >= 3:
            return "Well-structured"
        elif present_sections >= 2:
            return "Moderately-structured"
        else:
            return "Basic-structure"
    
    def _extract_main_contribution(self, key_info: Dict) -> str:
        """Extract main contribution from abstract/introduction."""
        abstract = key_info['content']['abstract']
        introduction = key_info['content']['introduction']
        
        # Simple heuristic - look for contribution indicators
        contribution_indicators = [
            "we propose", "we present", "we introduce", "we develop",
            "this paper", "our approach", "our method", "our contribution"
        ]
        
        text_to_search = (abstract + " " + introduction).lower()
        
        for indicator in contribution_indicators:
            if indicator in text_to_search:
                return f"Paper presents a novel approach (detected: '{indicator}')"
        
        return "Contribution to be analyzed from full text"
    
    def _identify_methodology_type(self, key_info: Dict) -> str:
        """Identify the type of methodology used."""
        methodology_text = key_info['content']['methodology'].lower()
        
        method_types = {
            'transformer': ['transformer', 'attention', 'bert', 'gpt'],
            'neural_network': ['neural', 'network', 'deep learning'],
            'statistical': ['statistical', 'probability', 'bayesian'],
            'optimization': ['optimization', 'gradient', 'training'],
            'evaluation': ['evaluation', 'benchmark', 'metric', 'assessment']
        }
        
        detected_types = []
        for method_type, keywords in method_types.items():
            if any(keyword in methodology_text for keyword in keywords):
                detected_types.append(method_type)
        
        return ', '.join(detected_types) if detected_types else "To be analyzed"
    
    def _identify_evaluation_approach(self, key_info: Dict) -> str:
        """Identify evaluation methodology."""
        results_text = key_info['content']['results'].lower()
        
        eval_approaches = {
            'human_evaluation': ['human', 'annotator', 'manual'],
            'automatic_metrics': ['bleu', 'rouge', 'accuracy', 'f1'],
            'benchmark': ['benchmark', 'dataset', 'test set'],
            'ablation': ['ablation', 'component', 'analysis']
        }
        
        detected_approaches = []
        for approach, keywords in eval_approaches.items():
            if any(keyword in results_text for keyword in keywords):
                detected_approaches.append(approach)
        
        return ', '.join(detected_approaches) if detected_approaches else "Standard evaluation"
    
    def _identify_datasets(self, key_info: Dict) -> List[str]:
        """Identify datasets mentioned in the paper."""
        content = ' '.join([
            key_info['content']['methodology'],
            key_info['content']['results']
        ]).lower()
        
        # Common dataset names
        dataset_patterns = [
            r'\b([A-Z][A-Za-z]*\d+[A-Za-z]*)\b',  # GLUE, WMT14, etc.
            r'\b([A-Z]{3,})\b',  # Common dataset acronyms
        ]
        
        datasets = []
        for pattern in dataset_patterns:
            matches = re.findall(pattern, content)
            datasets.extend(matches)
        
        # Filter common false positives
        false_positives = ['PDF', 'API', 'URL', 'GPU', 'CPU', 'RAM']
        datasets = [d for d in datasets if d not in false_positives]
        
        return list(set(datasets))[:5]  # Top 5 unique datasets
    
    def _identify_metrics(self, key_info: Dict) -> List[str]:
        """Identify performance metrics used."""
        results_text = key_info['content']['results'].lower()
        
        common_metrics = [
            'accuracy', 'precision', 'recall', 'f1', 'bleu', 'rouge',
            'perplexity', 'loss', 'error rate', 'auc', 'map'
        ]
        
        found_metrics = []
        for metric in common_metrics:
            if metric in results_text:
                found_metrics.append(metric)
        
        return found_metrics
    
    def _generate_focus_areas(self, category: str) -> List[str]:
        """Generate study focus areas based on category."""
        focus_map = {
            'Multilingual': [
                'Cross-lingual transfer mechanisms',
                'Language-specific vs universal representations',
                'Multilingual evaluation challenges'
            ],
            'Evaluation': [
                'Evaluation methodology design',
                'Metric selection and interpretation',
                'Bias detection in evaluation'
            ],
            'Inference': [
                'Computational efficiency techniques',
                'Speed vs accuracy trade-offs',
                'Deployment considerations'
            ],
            'Multimodal': [
                'Cross-modal alignment strategies',
                'Fusion techniques',
                'Multimodal evaluation approaches'
            ],
            'Data-Training': [
                'Data quality and selection',
                'Training stability techniques',
                'Curriculum learning approaches'
            ],
            'Model-Merging': [
                'Parameter combination strategies',
                'Knowledge transfer methods',
                'Multi-task optimization'
            ],
            'Preference-Personalization': [
                'User preference modeling',
                'Personalization vs generalization',
                'Preference learning techniques'
            ]
        }
        
        return focus_map.get(category, ['General ML concepts', 'Technical innovation', 'Practical applications'])
    
    def _generate_study_questions(self, category: str, key_info: Dict) -> List[str]:
        """Generate study questions for the paper."""
        base_questions = [
            "What is the main problem this paper addresses?",
            "How does their approach differ from existing methods?",
            "What are the key technical innovations?",
            "How do they validate their approach?",
            "What are the limitations and future work directions?"
        ]
        
        category_specific = {
            'Multilingual': [
                "How do they handle language-specific challenges?",
                "What cross-lingual transfer techniques are used?"
            ],
            'Evaluation': [
                "What evaluation metrics do they propose or use?",
                "How do they address evaluation biases?"
            ],
            'Inference': [
                "What efficiency improvements do they achieve?",
                "How do they balance speed and accuracy?"
            ]
        }
        
        questions = base_questions.copy()
        if category in category_specific:
            questions.extend(category_specific[category])
        
        return questions
    
    def _identify_related_concepts(self, category: str) -> List[str]:
        """Identify related concepts for broader understanding."""
        concept_map = {
            'Multilingual': [
                'Transfer learning', 'Zero-shot learning', 'Cross-lingual embeddings',
                'Language modeling', 'Tokenization strategies'
            ],
            'Evaluation': [
                'Benchmark design', 'Metric development', 'Human evaluation',
                'Statistical significance', 'Bias measurement'
            ],
            'Inference': [
                'Model compression', 'Quantization', 'Pruning',
                'Knowledge distillation', 'Edge deployment'
            ],
            'Multimodal': [
                'Vision-language models', 'Cross-modal attention',
                'Multimodal fusion', 'Representation learning'
            ]
        }
        
        return concept_map.get(category, ['Machine learning', 'Deep learning', 'AI systems'])
    
    def _assess_cohere_relevance(self, category: str) -> Dict[str, str]:
        """Assess relevance to Cohere's mission and application."""
        relevance_map = {
            'Multilingual': {
                'relevance': 'Very High',
                'reason': 'Direct alignment with Cohere\'s multilingual AI mission',
                'application_value': 'Excellent talking point for video and application'
            },
            'Evaluation': {
                'relevance': 'High',
                'reason': 'Critical for understanding AI system performance and safety',
                'application_value': 'Shows understanding of responsible AI development'
            },
            'Inference': {
                'relevance': 'Medium-High',
                'reason': 'Important for practical deployment of large language models',
                'application_value': 'Demonstrates practical deployment considerations'
            },
            'Multimodal': {
                'relevance': 'Medium',
                'reason': 'Growing area of interest for comprehensive AI systems',
                'application_value': 'Shows awareness of emerging AI capabilities'
            }
        }
        
        default_relevance = {
            'relevance': 'Medium',
            'reason': 'Contributes to broader AI/ML understanding',
            'application_value': 'Adds to technical depth and research breadth'
        }
        
        return relevance_map.get(category, default_relevance)
    
    def process_paper(self, pdf_path: Path) -> Dict[str, Any]:
        """Complete processing pipeline for a single paper."""
        paper_name = pdf_path.stem
        category = pdf_path.parent.name
        
        print(f"🔄 Processing {paper_name} ({category})...")
        
        try:
            # Step 1: Convert PDF to markdown
            markdown_content = self.convert_pdf_with_markitdown(pdf_path)
            
            # Step 2: Extract key information
            key_info = self.extract_key_information(markdown_content, category)
            
            # Step 3: Generate concept summary
            concept_summary = self.generate_concept_summary(key_info, paper_name)
            
            # Step 4: Save outputs
            self.save_outputs(paper_name, markdown_content, key_info, concept_summary)
            
            print(f"✅ Completed processing {paper_name}")
            
            return {
                'success': True,
                'paper_name': paper_name,
                'category': category,
                'key_info': key_info,
                'concept_summary': concept_summary
            }
            
        except Exception as e:
            print(f"❌ Error processing {paper_name}: {e}")
            return {
                'success': False,
                'paper_name': paper_name,
                'error': str(e)
            }
    
    def save_outputs(self, paper_name: str, markdown_content: str, key_info: Dict, concept_summary: Dict):
        """Save all processing outputs."""
        
        # Save markdown
        markdown_file = self.output_dir / "Markdown" / f"{paper_name}.md"
        with open(markdown_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        # Save structured information
        info_file = self.output_dir / "Summaries" / f"{paper_name}_info.json"
        with open(info_file, 'w', encoding='utf-8') as f:
            json.dump(key_info, f, indent=2, ensure_ascii=False)
        
        # Save concept summary
        concept_file = self.output_dir / "Concepts" / f"{paper_name}_concepts.json"
        with open(concept_file, 'w', encoding='utf-8') as f:
            json.dump(concept_summary, f, indent=2, ensure_ascii=False)
        
        # Save study notes
        self.save_study_notes(paper_name, concept_summary)
    
    def save_study_notes(self, paper_name: str, concept_summary: Dict):
        """Save human-readable study notes."""
        study_file = self.output_dir / "Study-Notes" / f"{paper_name}_study_notes.md"
        
        with open(study_file, 'w', encoding='utf-8') as f:
            cs = concept_summary
            
            f.write(f"# Study Notes: {paper_name.replace('_', ' ').title()}\n\n")
            
            # Paper Information
            f.write("## 📋 Paper Information\n\n")
            f.write(f"**Category**: {cs['paper_info']['category']}\n")
            f.write(f"**Estimated Reading Time**: {cs['paper_info']['estimated_reading_time']} minutes\n")
            f.write(f"**Complexity**: {cs['paper_info']['complexity']}\n")
            f.write(f"**Structure Quality**: {cs['paper_info']['structure_quality']}\n\n")
            
            # Key Concepts
            f.write("## 🔑 Key Concepts\n\n")
            f.write(f"**Main Contribution**: {cs['key_concepts']['main_contribution']}\n")
            f.write(f"**Methodology**: {cs['key_concepts']['methodology_type']}\n")
            f.write(f"**Evaluation**: {cs['key_concepts']['evaluation_approach']}\n\n")
            
            if cs['key_concepts']['datasets_used']:
                f.write("**Datasets**: " + ", ".join(cs['key_concepts']['datasets_used']) + "\n")
            if cs['key_concepts']['performance_metrics']:
                f.write("**Metrics**: " + ", ".join(cs['key_concepts']['performance_metrics']) + "\n")
            f.write("\n")
            
            # Study Guidance
            f.write("## 📚 Study Guidance\n\n")
            f.write("### Focus Areas\n")
            for area in cs['study_guidance']['focus_areas']:
                f.write(f"- {area}\n")
            f.write("\n")
            
            f.write("### Key Questions\n")
            for question in cs['study_guidance']['key_questions']:
                f.write(f"- {question}\n")
            f.write("\n")
            
            f.write("### Related Concepts\n")
            for concept in cs['study_guidance']['related_concepts']:
                f.write(f"- {concept}\n")
            f.write("\n")
            
            # Application Relevance
            f.write("## 🎯 Application Relevance\n\n")
            app_rel = cs['study_guidance']['application_relevance']
            f.write(f"**Cohere Relevance**: {app_rel['relevance']}\n")
            f.write(f"**Reasoning**: {app_rel['reason']}\n")
            f.write(f"**Application Value**: {app_rel['application_value']}\n\n")
            
            f.write("## 📝 Notes Section\n\n")
            f.write("*Add your personal notes and insights here while studying*\n\n")
            f.write("### Key Insights\n")
            f.write("- \n\n")
            f.write("### Questions for Further Research\n")
            f.write("- \n\n")
            f.write("### Connection to Other Papers\n")
            f.write("- \n\n")
            
            f.write("---\n")
            f.write(f"*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")


def main():
    """Main execution function for testing."""
    base_dir = Path(__file__).parent
    processor = MarkItDownPaperProcessor(str(base_dir))
    
    print("🚀 MarkItDown Paper Processor Ready!")
    print("📋 To process papers:")
    print("   1. Single paper: processor.process_paper(Path('path/to/paper.pdf'))")
    print("   2. All papers: See process_all_papers() function below")
    
    return processor

def process_all_papers():
    """Process all papers in the collection."""
    base_dir = Path(__file__).parent
    processor = MarkItDownPaperProcessor(str(base_dir))
    
    papers_dir = base_dir / "01-PAPERS"
    results = []
    
    print(f"🔄 Processing all papers in {papers_dir}...")
    
    for category_dir in papers_dir.iterdir():
        if category_dir.is_dir():
            print(f"\n📁 Processing {category_dir.name} papers...")
            
            for pdf_file in category_dir.glob("*.pdf"):
                result = processor.process_paper(pdf_file)
                results.append(result)
    
    # Summary
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    print(f"\n📊 Processing Complete!")
    print(f"✅ Successful: {len(successful)}")
    print(f"❌ Failed: {len(failed)}")
    
    if failed:
        print("Failed papers:")
        for fail in failed:
            print(f"  - {fail['paper_name']}: {fail['error']}")
    
    return results

if __name__ == "__main__":
    processor = main()
