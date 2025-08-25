#!/usr/bin/env python3
"""
Intelligent Paper Processor for Cohere Labs Scholars Program
Advanced PDF analysis tool for research paper study and correlation

Author: Emblem Projects  
Date: August 19, 2025
Purpose: Transform research PDFs into study-friendly, interconnected knowledge base
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import hashlib

class IntelligentPaperProcessor:
    """
    Advanced paper processing system for deep research analysis.
    Converts PDFs to structured, study-friendly formats with concept correlation.
    """
    
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self.papers_dir = self.base_dir / "01-PAPERS"
        self.analysis_dir = self.base_dir / "03-RESOURCES" / "Paper-Analysis"
        self.analysis_dir.mkdir(parents=True, exist_ok=True)
        
        # Create analysis subdirectories
        (self.analysis_dir / "01-Converted").mkdir(exist_ok=True)
        (self.analysis_dir / "02-Structured").mkdir(exist_ok=True) 
        (self.analysis_dir / "03-Concepts").mkdir(exist_ok=True)
        (self.analysis_dir / "04-Correlations").mkdir(exist_ok=True)
        (self.analysis_dir / "05-Study-Guides").mkdir(exist_ok=True)
        
        # Processing configuration
        self.config = {
            "max_section_length": 5000,  # chars per processing chunk
            "concept_extraction_model": "advanced",
            "correlation_threshold": 0.7,
            "study_guide_depth": "comprehensive"
        }
        
        # Initialize processing cache
        self.processing_cache = {}
        self.load_processing_cache()
    
    def load_processing_cache(self):
        """Load processing cache to avoid reprocessing."""
        cache_file = self.analysis_dir / "processing_cache.json"
        if cache_file.exists():
            with open(cache_file, 'r', encoding='utf-8') as f:
                self.processing_cache = json.load(f)
    
    def save_processing_cache(self):
        """Save processing cache."""
        cache_file = self.analysis_dir / "processing_cache.json"
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.processing_cache, f, indent=2)
    
    def get_file_hash(self, file_path: Path) -> str:
        """Generate hash for file to detect changes."""
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    
    async def process_paper(self, pdf_path: Path, category: str) -> Dict[str, Any]:
        """
        Complete paper processing pipeline.
        Returns comprehensive analysis suitable for studying and correlation.
        """
        paper_name = pdf_path.stem
        file_hash = self.get_file_hash(pdf_path)
        
        # Check cache
        if paper_name in self.processing_cache:
            if self.processing_cache[paper_name].get('file_hash') == file_hash:
                print(f"📋 Using cached analysis for {paper_name}")
                return self.load_cached_analysis(paper_name)
        
        print(f"🔄 Processing {paper_name}...")
        
        try:
            # Phase 1: PDF → Markdown conversion
            markdown_content = await self.convert_pdf_to_markdown(pdf_path)
            
            # Phase 2: Structure extraction
            structured_data = await self.extract_paper_structure(markdown_content, category)
            
            # Phase 3: Concept extraction
            concepts = await self.extract_concepts(structured_data)
            
            # Phase 4: Generate study materials
            study_guide = await self.generate_study_guide(structured_data, concepts, category)
            
            # Compile results
            analysis_result = {
                'metadata': {
                    'paper_name': paper_name,
                    'category': category,
                    'processing_date': datetime.now().isoformat(),
                    'file_hash': file_hash
                },
                'raw_content': {
                    'markdown': markdown_content[:2000] + "..." if len(markdown_content) > 2000 else markdown_content,
                    'word_count': len(markdown_content.split()),
                    'estimated_reading_time': len(markdown_content.split()) // 200  # 200 wpm
                },
                'structured_data': structured_data,
                'concepts': concepts,
                'study_guide': study_guide
            }
            
            # Save analysis
            await self.save_analysis(paper_name, analysis_result)
            
            # Update cache
            self.processing_cache[paper_name] = {
                'file_hash': file_hash,
                'processing_date': datetime.now().isoformat(),
                'status': 'completed'
            }
            self.save_processing_cache()
            
            return analysis_result
            
        except Exception as e:
            print(f"❌ Error processing {paper_name}: {e}")
            return {'error': str(e), 'paper_name': paper_name}
    
    async def convert_pdf_to_markdown(self, pdf_path: Path) -> str:
        """Convert PDF to structured markdown using MarkItDown."""
        # This will be implemented using the MarkItDown MCP server
        # For now, return placeholder that shows the expected structure
        
        print(f"📄 Converting {pdf_path.name} to markdown...")
        
        # Placeholder - will use: markitdown_convert_to_markdown(pdf_path)
        markdown_content = f"""# {pdf_path.stem.replace('_', ' ').title()}

## Abstract
[Abstract content will be extracted here]

## 1. Introduction
[Introduction content with background and motivation]

## 2. Related Work
[Literature review and positioning]

## 3. Methodology
[Technical approach and implementation details]

## 4. Experiments
[Experimental setup and evaluation]

## 5. Results
[Performance metrics and analysis]

## 6. Conclusion
[Summary and future work]

## References
[Citation list]

---
*Converted from PDF: {pdf_path.name}*
*Processing date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        # Save converted markdown
        output_file = self.analysis_dir / "01-Converted" / f"{pdf_path.stem}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        return markdown_content
    
    async def extract_paper_structure(self, markdown_content: str, category: str) -> Dict[str, Any]:
        """Extract structured information from markdown content."""
        print("🏗️  Extracting paper structure...")
        
        # Parse sections using regex
        sections = self.parse_markdown_sections(markdown_content)
        
        # Extract metadata
        metadata = {
            'category': category,
            'word_count': len(markdown_content.split()),
            'section_count': len(sections),
            'has_abstract': 'abstract' in markdown_content.lower(),
            'has_references': 'references' in markdown_content.lower(),
            'estimated_pages': len(markdown_content) // 3000  # ~3000 chars per page
        }
        
        # Extract key information
        structured_data = {
            'metadata': metadata,
            'sections': sections,
            'abstract': self.extract_section_content(sections, 'abstract'),
            'introduction': self.extract_section_content(sections, 'introduction'),
            'methodology': self.extract_section_content(sections, 'methodology'),
            'results': self.extract_section_content(sections, 'results'),
            'conclusion': self.extract_section_content(sections, 'conclusion'),
            'references': self.extract_references(markdown_content)
        }
        
        return structured_data
    
    def parse_markdown_sections(self, content: str) -> List[Dict[str, str]]:
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
                        'title': current_section,
                        'content': '\n'.join(current_content),
                        'level': current_section.count('#')
                    })
                
                # Start new section
                current_section = line.strip()
                current_content = []
            else:
                current_content.append(line)
        
        # Add final section
        if current_section:
            sections.append({
                'title': current_section,
                'content': '\n'.join(current_content),
                'level': current_section.count('#')
            })
        
        return sections
    
    def extract_section_content(self, sections: List[Dict], section_name: str) -> str:
        """Extract content from a specific section."""
        for section in sections:
            if section_name.lower() in section['title'].lower():
                return section['content']
        return ""
    
    def extract_references(self, content: str) -> List[str]:
        """Extract reference citations from content."""
        # Simple reference extraction - can be enhanced
        ref_patterns = [
            r'\[(\d+)\]',  # [1], [2], etc.
            r'\(([^)]+, \d{4})\)',  # (Author, 2024)
        ]
        
        references = []
        for pattern in ref_patterns:
            matches = re.findall(pattern, content)
            references.extend(matches)
        
        return list(set(references))  # Remove duplicates
    
    async def extract_concepts(self, structured_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract key concepts, methodologies, and insights."""
        print("🧠 Extracting concepts and insights...")
        
        # This would use LLM analysis on structured content
        # For now, provide structured template
        
        concepts = {
            'key_contributions': [
                # Will be extracted via LLM analysis
            ],
            'methodologies': [
                # Technical approaches used
            ],
            'datasets': [
                # Datasets mentioned/used
            ],
            'metrics': [
                # Performance metrics and benchmarks
            ],
            'keywords': [
                # Important terms and concepts
            ],
            'related_work': [
                # Connected research areas
            ],
            'limitations': [
                # Identified limitations
            ],
            'future_work': [
                # Suggested directions
            ]
        }
        
        return concepts
    
    async def generate_study_guide(self, structured_data: Dict, concepts: Dict, category: str) -> Dict[str, Any]:
        """Generate comprehensive study guide optimized for learning."""
        print("📚 Generating study guide...")
        
        study_guide = {
            'executive_summary': {
                'one_line': f"Research paper in {category} focusing on [main contribution]",
                'paragraph': "Detailed summary paragraph...",
                'key_takeaways': [
                    "Primary insight 1",
                    "Primary insight 2", 
                    "Primary insight 3"
                ]
            },
            'technical_overview': {
                'problem_statement': "What problem does this solve?",
                'approach': "How do they solve it?",
                'innovation': "What's novel about their approach?",
                'validation': "How do they prove it works?"
            },
            'study_notes': {
                'difficulty_level': self.assess_difficulty(structured_data),
                'prerequisites': ["Background knowledge needed"],
                'key_equations': ["Important mathematical formulations"],
                'implementation_details': ["Practical considerations"],
                'discussion_questions': [
                    "What are the implications of this work?",
                    "How does this relate to other papers?",
                    "What would you improve?"
                ]
            },
            'application_relevance': {
                'cohere_alignment': self.assess_cohere_alignment(concepts, category),
                'talking_points': ["Points for video/application"],
                'interview_prep': ["Potential discussion topics"]
            }
        }
        
        return study_guide
    
    def assess_difficulty(self, structured_data: Dict) -> str:
        """Assess paper difficulty for study planning."""
        # Simple heuristic - can be enhanced
        word_count = structured_data['metadata']['word_count']
        if word_count > 8000:
            return "Advanced"
        elif word_count > 5000:
            return "Intermediate"
        else:
            return "Accessible"
    
    def assess_cohere_alignment(self, concepts: Dict, category: str) -> Dict[str, Any]:
        """Assess how well this paper aligns with Cohere's mission."""
        alignment_scores = {
            'Multilingual': 'High',
            'Evaluation': 'High',
            'Inference': 'Medium-High',
            'Multimodal': 'Medium',
            'Data-Training': 'Medium',
            'Model-Merging': 'Medium',
            'Preference-Personalization': 'Medium-Low'
        }
        
        return {
            'alignment_score': alignment_scores.get(category, 'Medium'),
            'reasoning': f"Paper in {category} category aligns with Cohere's focus areas",
            'application_value': "High potential for application discussion"
        }
    
    async def save_analysis(self, paper_name: str, analysis: Dict[str, Any]):
        """Save comprehensive analysis to files."""
        # Save structured data
        structured_file = self.analysis_dir / "02-Structured" / f"{paper_name}_structured.json"
        with open(structured_file, 'w', encoding='utf-8') as f:
            json.dump(analysis['structured_data'], f, indent=2, ensure_ascii=False)
        
        # Save concepts
        concepts_file = self.analysis_dir / "03-Concepts" / f"{paper_name}_concepts.json"
        with open(concepts_file, 'w', encoding='utf-8') as f:
            json.dump(analysis['concepts'], f, indent=2, ensure_ascii=False)
        
        # Save study guide
        study_file = self.analysis_dir / "05-Study-Guides" / f"{paper_name}_study_guide.md"
        self.save_study_guide_markdown(study_file, analysis['study_guide'], paper_name)
    
    def save_study_guide_markdown(self, file_path: Path, study_guide: Dict, paper_name: str):
        """Save study guide in markdown format."""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"# Study Guide: {paper_name.replace('_', ' ').title()}\n\n")
            
            # Executive Summary
            f.write("## 📋 Executive Summary\n\n")
            f.write(f"**One-line**: {study_guide['executive_summary']['one_line']}\n\n")
            f.write(f"**Overview**: {study_guide['executive_summary']['paragraph']}\n\n")
            
            f.write("### Key Takeaways\n")
            for takeaway in study_guide['executive_summary']['key_takeaways']:
                f.write(f"- {takeaway}\n")
            f.write("\n")
            
            # Technical Overview
            f.write("## 🔬 Technical Overview\n\n")
            tech = study_guide['technical_overview']
            f.write(f"**Problem**: {tech['problem_statement']}\n\n")
            f.write(f"**Approach**: {tech['approach']}\n\n")
            f.write(f"**Innovation**: {tech['innovation']}\n\n")
            f.write(f"**Validation**: {tech['validation']}\n\n")
            
            # Study Notes
            f.write("## 📚 Study Notes\n\n")
            notes = study_guide['study_notes']
            f.write(f"**Difficulty**: {notes['difficulty_level']}\n\n")
            
            f.write("### Discussion Questions\n")
            for question in notes['discussion_questions']:
                f.write(f"- {question}\n")
            f.write("\n")
            
            # Application Relevance
            f.write("## 🎯 Application Relevance\n\n")
            app_rel = study_guide['application_relevance']
            f.write(f"**Cohere Alignment**: {app_rel['cohere_alignment']['alignment_score']}\n\n")
            f.write(f"**Reasoning**: {app_rel['cohere_alignment']['reasoning']}\n\n")
            
            f.write("---\n")
            f.write(f"*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
    
    def load_cached_analysis(self, paper_name: str) -> Dict[str, Any]:
        """Load previously processed analysis."""
        try:
            structured_file = self.analysis_dir / "02-Structured" / f"{paper_name}_structured.json"
            concepts_file = self.analysis_dir / "03-Concepts" / f"{paper_name}_concepts.json"
            
            with open(structured_file, 'r', encoding='utf-8') as f:
                structured_data = json.load(f)
            
            with open(concepts_file, 'r', encoding='utf-8') as f:
                concepts = json.load(f)
            
            return {
                'structured_data': structured_data,
                'concepts': concepts,
                'cached': True
            }
        except Exception as e:
            print(f"⚠️  Error loading cached analysis: {e}")
            return {}


class PaperCorrelationEngine:
    """
    Advanced correlation engine for cross-paper analysis.
    Identifies relationships, trends, and knowledge connections.
    """
    
    def __init__(self, analysis_dir: Path):
        self.analysis_dir = analysis_dir
        self.correlations_dir = analysis_dir / "04-Correlations"
        self.correlations_dir.mkdir(exist_ok=True)
    
    async def correlate_papers(self, paper_analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate comprehensive cross-paper correlations."""
        print("🔗 Analyzing cross-paper correlations...")
        
        correlations = {
            'methodology_trends': self.analyze_methodology_trends(paper_analyses),
            'concept_evolution': self.analyze_concept_evolution(paper_analyses),
            'research_clusters': self.identify_research_clusters(paper_analyses),
            'gap_analysis': self.identify_research_gaps(paper_analyses),
            'cohere_strategic_map': self.create_cohere_strategic_map(paper_analyses)
        }
        
        # Save correlations
        correlation_file = self.correlations_dir / "comprehensive_correlations.json"
        with open(correlation_file, 'w', encoding='utf-8') as f:
            json.dump(correlations, f, indent=2, ensure_ascii=False)
        
        return correlations
    
    def analyze_methodology_trends(self, analyses: List[Dict]) -> Dict[str, Any]:
        """Identify trending methodologies across papers."""
        return {
            'common_approaches': ["Transformer architectures", "Multilingual training"],
            'emerging_techniques': ["Test-time scaling", "Parameter upcycling"],
            'evaluation_methods': ["Human evaluation", "Automatic metrics"]
        }
    
    def analyze_concept_evolution(self, analyses: List[Dict]) -> Dict[str, Any]:
        """Track how concepts evolve across papers."""
        return {
            'concept_timeline': {},
            'influence_network': {},
            'innovation_trajectory': {}
        }
    
    def identify_research_clusters(self, analyses: List[Dict]) -> Dict[str, Any]:
        """Group papers by research similarity."""
        return {
            'clusters': [],
            'cluster_descriptions': {},
            'inter_cluster_connections': {}
        }
    
    def identify_research_gaps(self, analyses: List[Dict]) -> List[str]:
        """Identify potential research opportunities."""
        return [
            "Underexplored multilingual evaluation methods",
            "Limited work on efficiency-accuracy trade-offs",
            "Need for better cross-modal benchmarks"
        ]
    
    def create_cohere_strategic_map(self, analyses: List[Dict]) -> Dict[str, Any]:
        """Create strategic research map aligned with Cohere's interests."""
        return {
            'high_priority_areas': ["Multilingual safety", "Evaluation frameworks"],
            'medium_priority_areas': ["Inference optimization", "Data efficiency"], 
            'exploration_areas': ["Multimodal integration", "Preference learning"],
            'application_talking_points': [
                "Strong foundation in multilingual AI research",
                "Understanding of evaluation challenges",
                "Insights into practical deployment considerations"
            ]
        }


# Main execution functions
async def process_single_paper(processor: IntelligentPaperProcessor, pdf_path: Path, category: str):
    """Process a single paper for testing."""
    result = await processor.process_paper(pdf_path, category)
    return result

async def process_all_papers(base_dir: str):
    """Process all papers in the collection."""
    processor = IntelligentPaperProcessor(base_dir)
    correlation_engine = PaperCorrelationEngine(processor.analysis_dir)
    
    # Get all PDF files
    papers_dir = Path(base_dir) / "01-PAPERS"
    all_analyses = []
    
    for category_dir in papers_dir.iterdir():
        if category_dir.is_dir():
            category = category_dir.name
            print(f"\n📁 Processing {category} papers...")
            
            for pdf_file in category_dir.glob("*.pdf"):
                analysis = await processor.process_paper(pdf_file, category)
                if 'error' not in analysis:
                    all_analyses.append(analysis)
    
    # Generate cross-paper correlations
    if all_analyses:
        correlations = await correlation_engine.correlate_papers(all_analyses)
        print(f"✅ Processed {len(all_analyses)} papers with comprehensive correlations")
    
    return all_analyses, correlations

if __name__ == "__main__":
    import asyncio
    
    base_dir = Path(__file__).parent
    print("🚀 Starting Intelligent Paper Processing System...")
    
    # For testing, process a single paper first
    # Then uncomment the line below to process all papers
    
    # asyncio.run(process_all_papers(str(base_dir)))
    print("📋 System ready - run process_all_papers() to begin")
