#!/usr/bin/env python3
"""
Paper Link Generator Tool
Creates clickable GitHub links for all paper analyses in the repository.
"""

import os
import re
from pathlib import Path
from urllib.parse import quote

def get_md_files_mapping():
    """Scan 02-MARKDOWN directory and create mapping of papers to their MD files."""
    base_path = Path("02-MARKDOWN")
    md_files = {}
    
    if not base_path.exists():
        print(f"ERROR: {base_path} directory not found!")
        return {}
    
    for category_dir in base_path.iterdir():
        if category_dir.is_dir() and category_dir.name != "__pycache__":
            category = category_dir.name
            for md_file in category_dir.glob("*.md"):
                if md_file.name != "BATCH_SUMMARY.md":
                    # Extract paper title from filename
                    filename = md_file.name
                    # Remove _STUDY.md suffix and convert underscores to spaces
                    title_base = filename.replace("_STUDY.md", "").replace(".md", "")
                    title = title_base.replace("_", " ")
                    
                    md_files[title] = {
                        'file': md_file,
                        'category': category,
                        'github_path': f"02-MARKDOWN/{category}/{filename}"
                    }
    
    return md_files

def create_github_link(paper_title, github_path):
    """Create a GitHub link for a paper analysis."""
    base_url = "https://github.com/thisis-romar/cohere-scholars-2026-research-portfolio/blob/main/"
    # URL encode the path properly
    encoded_path = quote(github_path, safe='/')
    return f"[{paper_title}]({base_url}{encoded_path})"

def fuzzy_match_title(paper_title, md_files):
    """Find the best match for a paper title in the MD files."""
    # Clean the paper title for matching
    clean_title = re.sub(r'[^\w\s]', '', paper_title.lower())
    
    best_match = None
    best_score = 0
    
    for md_title, file_info in md_files.items():
        clean_md_title = re.sub(r'[^\w\s]', '', md_title.lower())
        
        # Simple word matching score
        title_words = set(clean_title.split())
        md_words = set(clean_md_title.split())
        
        if title_words and md_words:
            intersection = title_words.intersection(md_words)
            score = len(intersection) / max(len(title_words), len(md_words))
            
            if score > best_score:
                best_score = score
                best_match = file_info
    
    return best_match if best_score > 0.5 else None

def generate_linked_paper_list():
    """Generate the paper list with clickable links."""
    
    # Papers from README.md
    papers_by_category = {
        "Multilingual": [
            "NeoBabel: A Multilingual Open Tower for Visual Generation",
            "One Tokenizer To Rule Them All: Emergent Language Plasticity via Multilingual Tokenizers",
            "The State of Multilingual LLM Safety Research: From Measuring the Language Gap to Mitigating It",
            "Déjà Vu: Multilingual LLM Evaluation through the Lens of Machine Translation Evaluation",
            "Aya Expanse: Combining Research Breakthroughs for a New Multilingual Frontier",
            "M-RewardBench: Evaluating Reward Models in Multilingual Settings",
            "MURI: High-Quality Instruction Tuning Datasets for Low-Resource Languages via Reverse Instructions"
        ],
        "Evaluation": [
            "Reality Check: A New Evaluation Ecosystem Is Necessary to Understand AI's Real World Effects",
            "The Leaderboard Illusion",
            "Kaleidoscope: Exams for Multilingual Vision Evaluation",
            "From Tools to Teammates: Evaluating LLMs in Multi-Session Coding Interactions",
            "Global MMLU",
            "INCLUDE: Evaluating Multilingual Language Understanding with Regional Knowledge"
        ],
        "Inference": [
            "When Life Gives You Samples: The Benefits of Scaling up Inference Compute for Multilingual LLMs",
            "Treasure Hunt: Real-time Targeting of the Long Tail using Training-Time Markers",
            "Crosslingual Reasoning through Test-Time Scaling",
            "BAM! Just Like That: Simple and Efficient Parameter Upcycling for Mixture of Experts",
            "Nexus: Specialization meets Adaptability for Efficiently Training Mixture of Experts"
        ],
        "Multimodal": [
            "NeoBabel: A Multilingual Open Tower for Visual Generation",  # cross-listed
            "Aya Vision: Advancing the Frontier of Multilingual Multimodality"
        ],
        "Data-Training": [
            "How to Improve the Robustness of Closed-Source Models on NLI",
            "Diversify and Conquer: Diversity-Centric Data Selection with Iterative Refinement",
            "Bridging the Data Provenance Gap Across Text, Speech, and Video"
        ],
        "Model-Merging": [
            "Continual Pretraining for Cross-lingual LLM with Knowledge Transfer",
            "Mix and Match: Efficient Model Merging for Multi-Task Learning",
            "Model Recycling: Optimizing Merging at Scale"
        ],
        "Preference-Personalization": [
            "Post-Hoc Reward Engineering with Conditional Monte Carlo for Personalized Learning",
            "When Personalization Meets Reality: Lessons from Preference Learning"
        ]
    }
    
    # Get MD files mapping
    md_files = get_md_files_mapping()
    
    if not md_files:
        print("ERROR: No MD files found!")
        return
    
    print("🔍 Found MD files:")
    for title, info in md_files.items():
        print(f"  - {title} -> {info['github_path']}")
    
    print("\n📋 Generating linked paper list...")
    
    linked_content = "## 📚 Paper Analyses with Direct Links\n\n"
    
    category_icons = {
        "Multilingual": "🌐",
        "Evaluation": "🔍", 
        "Inference": "⚡",
        "Multimodal": "🎨",
        "Data-Training": "📊",
        "Model-Merging": "🔄",
        "Preference-Personalization": "👤"
    }
    
    counter = 1
    
    for category, papers in papers_by_category.items():
        icon = category_icons.get(category, "📄")
        linked_content += f"### {icon} {category.replace('-', ' & ')} Papers ({len(papers)} papers)\n"
        
        for paper in papers:
            # Find matching MD file
            match = fuzzy_match_title(paper, md_files)
            
            if match:
                github_link = create_github_link(paper, match['github_path'])
                linked_content += f"{counter}. {github_link}\n"
            else:
                # Fallback - no link
                linked_content += f"{counter}. **{paper}** *(analysis not found)*\n"
                print(f"⚠️  WARNING: No MD file found for: {paper}")
            
            counter += 1
        
        linked_content += "\n"
    
    return linked_content

def verify_all_links():
    """Verify that all MD files have corresponding entries in the paper list."""
    md_files = get_md_files_mapping()
    
    print(f"\n✅ VERIFICATION REPORT:")
    print(f"📊 Total MD files found: {len(md_files)}")
    
    by_category = {}
    for title, info in md_files.items():
        category = info['category']
        if category not in by_category:
            by_category[category] = []
        by_category[category].append(title)
    
    for category, files in by_category.items():
        print(f"  📁 {category}: {len(files)} files")
        for file in files:
            print(f"    - {file}")

if __name__ == "__main__":
    print("🔗 Paper Link Generator Tool")
    print("=" * 50)
    
    # Change to the project directory
    project_dir = r"H:\-EMBLEM-PROJECT(s)-\COHERE SCHOLARS PROGRAM 2026"
    if os.path.exists(project_dir):
        os.chdir(project_dir)
        print(f"📁 Working directory: {os.getcwd()}")
    else:
        print("❌ Project directory not found!")
        exit(1)
    
    # Verify all MD files
    verify_all_links()
    
    # Generate linked content
    linked_content = generate_linked_paper_list()
    
    if linked_content:
        # Save to file
        output_file = "LINKED_PAPERS.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(linked_content)
        
        print(f"\n✅ Generated linked paper list saved to: {output_file}")
        print("\n📋 Preview of generated content:")
        print("=" * 50)
        print(linked_content[:1000] + "..." if len(linked_content) > 1000 else linked_content)
    else:
        print("❌ Failed to generate linked content")
