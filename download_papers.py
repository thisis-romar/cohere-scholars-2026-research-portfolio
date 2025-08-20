#!/usr/bin/env python3
"""
Cohere Labs Scholars Program 2026 - Paper Download Script

This script downloads all 28 eligible papers from the Scholars Program
and organizes them into appropriate category folders with proper naming.

Author: Emblem Projects
Date: August 19, 2025
"""

import os
import requests
import time
from pathlib import Path
from urllib.parse import urlparse
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('paper_download.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class PaperDownloader:
    """Downloads and organizes Cohere Labs Scholars Program papers."""
    
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self.papers_dir = self.base_dir / "01-PAPERS"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Paper definitions organized by category
        self.papers = {
            "Multilingual": [
                {
                    "title": "NeoBabel: A Multilingual Open Tower for Visual Generation",
                    "url": "https://arxiv.org/pdf/2507.06137.pdf",
                    "filename": "NeoBabel_Multilingual_Open_Tower_Visual_Generation.pdf"
                },
                {
                    "title": "One Tokenizer To Rule Them All: Emergent Language Plasticity via Multilingual Tokenizers",
                    "url": "https://arxiv.org/pdf/2506.10766.pdf",
                    "filename": "One_Tokenizer_Rule_Them_All_Multilingual_Tokenizers.pdf"
                },
                {
                    "title": "The State of Multilingual LLM Safety Research: From Measuring the Language Gap to Mitigating It",
                    "url": "https://arxiv.org/pdf/2505.24119.pdf",
                    "filename": "State_Multilingual_LLM_Safety_Research.pdf"
                },
                {
                    "title": "Déjà Vu: Multilingual LLM Evaluation through the Lens of Machine Translation Evaluation",
                    "url": "https://arxiv.org/pdf/2504.11829.pdf",
                    "filename": "Deja_Vu_Multilingual_LLM_Evaluation_MT.pdf"
                },
                {
                    "title": "Aya Expanse: Combining Research Breakthroughs for a New Multilingual Frontier",
                    "url": "https://arxiv.org/pdf/2412.04261.pdf",
                    "filename": "Aya_Expanse_Research_Breakthroughs_Multilingual.pdf"
                },
                {
                    "title": "M-RewardBench: Evaluating Reward Models in Multilingual Settings",
                    "url": "https://arxiv.org/pdf/2410.15522.pdf",
                    "filename": "M_RewardBench_Evaluating_Reward_Models_Multilingual.pdf"
                },
                {
                    "title": "MURI: High-Quality Instruction Tuning Datasets for Low-Resource Languages via Reverse Instructions",
                    "url": "https://arxiv.org/pdf/2409.12958.pdf",
                    "filename": "MURI_High_Quality_Instruction_Tuning_Low_Resource.pdf"
                }
            ],
            "Evaluation": [
                {
                    "title": "Reality Check: A New Evaluation Ecosystem Is Necessary to Understand AI's Real World Effects",
                    "url": "https://arxiv.org/pdf/2505.18893.pdf",
                    "filename": "Reality_Check_New_Evaluation_Ecosystem_AI.pdf"
                },
                {
                    "title": "The Leaderboard Illusion",
                    "url": "https://arxiv.org/pdf/2504.20879.pdf",
                    "filename": "The_Leaderboard_Illusion.pdf"
                },
                {
                    "title": "Kaleidoscope: Exams for Multilingual Vision Evaluation",
                    "url": "https://arxiv.org/pdf/2504.07072.pdf",
                    "filename": "Kaleidoscope_Exams_Multilingual_Vision_Evaluation.pdf"
                },
                {
                    "title": "From Tools to Teammates: Evaluating LLMs in Multi-Session Coding Interactions",
                    "url": "https://arxiv.org/pdf/2502.13791.pdf",
                    "filename": "From_Tools_Teammates_LLMs_Multi_Session_Coding.pdf"
                },
                {
                    "title": "Global MMLU",
                    "url": "https://arxiv.org/pdf/2412.03304.pdf",
                    "filename": "Global_MMLU.pdf"
                },
                {
                    "title": "INCLUDE: Evaluating Multilingual Language Understanding with Regional Knowledge",
                    "url": "https://arxiv.org/pdf/2411.19799.pdf",
                    "filename": "INCLUDE_Evaluating_Multilingual_Regional_Knowledge.pdf"
                }
            ],
            "Inference": [
                {
                    "title": "When Life Gives You Samples: The Benefits of Scaling up Inference Compute for Multilingual LLMs",
                    "url": "https://arxiv.org/pdf/2506.20544.pdf",
                    "filename": "When_Life_Gives_Samples_Scaling_Inference_Multilingual.pdf"
                },
                {
                    "title": "Treasure Hunt: Real-time Targeting of the Long Tail using Training-Time Markers",
                    "url": "https://arxiv.org/pdf/2506.14702.pdf",
                    "filename": "Treasure_Hunt_Real_Time_Long_Tail_Training_Markers.pdf"
                },
                {
                    "title": "Crosslingual Reasoning through Test-Time Scaling",
                    "url": "https://arxiv.org/pdf/2505.05408.pdf",
                    "filename": "Crosslingual_Reasoning_Test_Time_Scaling.pdf"
                },
                {
                    "title": "BAM! Just Like That: Simple and Efficient Parameter Upcycling for Mixture of Experts",
                    "url": "https://proceedings.neurips.cc/paper_files/paper/2024/file/665bb142d4b9f55660cb89bb56a66fe1-Paper-Conference.pdf",
                    "filename": "BAM_Simple_Efficient_Parameter_Upcycling_MoE.pdf"
                },
                {
                    "title": "Nexus: Specialization meets Adaptability for Efficiently Training Mixture of Experts",
                    "url": "https://arxiv.org/pdf/2408.15901.pdf",
                    "filename": "Nexus_Specialization_Adaptability_Training_MoE.pdf"
                }
            ],
            "Multimodal": [
                {
                    "title": "Aya Vision: Advancing the Frontier of Multilingual Multimodality",
                    "url": "https://arxiv.org/pdf/2505.08751.pdf",
                    "filename": "Aya_Vision_Advancing_Multilingual_Multimodality.pdf"
                }
                # NeoBabel is cross-listed, already in Multilingual folder
            ],
            "Data-Training": [
                {
                    "title": "How to Improve the Robustness of Closed-Source Models on NLI",
                    "url": "https://arxiv.org/pdf/2505.20209.pdf",
                    "filename": "Improve_Robustness_Closed_Source_Models_NLI.pdf"
                },
                {
                    "title": "Diversify and Conquer: Diversity-Centric Data Selection with Iterative Refinement",
                    "url": "https://arxiv.org/pdf/2409.11378.pdf",
                    "filename": "Diversify_Conquer_Data_Selection_Iterative_Refinement.pdf"
                },
                {
                    "title": "Bridging the Data Provenance Gap Across Text, Speech, and Video",
                    "url": "https://www.dataprovenance.org/Multimodal_Data_Provenance.pdf",
                    "filename": "Bridging_Data_Provenance_Gap_Text_Speech_Video.pdf"
                }
            ],
            "Model-Merging": [
                {
                    "title": "If You Can't Use Them, Recycle Them",
                    "url": "https://arxiv.org/pdf/2412.04144.pdf",
                    "filename": "If_You_Cant_Use_Them_Recycle_Them.pdf"
                },
                {
                    "title": "Mix Data or Merge Models? Optimizing for Diverse Multi-Task Learning",
                    "url": "https://arxiv.org/pdf/2410.10801.pdf",
                    "filename": "Mix_Data_Merge_Models_Multi_Task_Learning.pdf"
                },
                {
                    "title": "Investigating Continual Pretraining in Large Language Models: Insights and Implications",
                    "url": "https://arxiv.org/pdf/2402.17400.pdf",
                    "filename": "Investigating_Continual_Pretraining_LLMs.pdf"
                }
            ],
            "Preference-Personalization": [
                {
                    "title": "When Personalization Meets Reality: A Multi-Faceted Analysis of Personalized Preference Learning",
                    "url": "https://arxiv.org/pdf/2502.19158.pdf",
                    "filename": "When_Personalization_Meets_Reality_Preference_Learning.pdf"
                },
                {
                    "title": "A Post-trainer's Guide to Multilingual Training Data: Uncovering Cross-lingual Transfer Dynamics",
                    "url": "https://arxiv.org/pdf/2504.16677.pdf",
                    "filename": "Post_Trainer_Guide_Multilingual_Training_Data.pdf"
                }
            ]
        }
    
    def download_paper(self, category: str, paper: dict) -> bool:
        """Download a single paper with error handling and retry logic."""
        category_dir = self.papers_dir / category
        category_dir.mkdir(exist_ok=True)
        
        file_path = category_dir / paper["filename"]
        
        # Skip if already downloaded
        if file_path.exists():
            logger.info(f"✅ Already exists: {paper['filename']}")
            return True
        
        logger.info(f"📥 Downloading: {paper['title']}")
        
        try:
            # Download with retry logic
            for attempt in range(3):
                try:
                    response = self.session.get(paper["url"], timeout=30, stream=True)
                    response.raise_for_status()
                    
                    # Check if response is actually a PDF
                    content_type = response.headers.get('content-type', '')
                    if 'application/pdf' not in content_type and 'pdf' not in content_type:
                        logger.warning(f"⚠️  Response may not be PDF: {content_type}")
                    
                    # Save file
                    with open(file_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                    
                    # Verify file size
                    if file_path.stat().st_size < 1024:  # Less than 1KB probably failed
                        raise ValueError("Downloaded file too small")
                    
                    logger.info(f"✅ Downloaded: {paper['filename']} ({file_path.stat().st_size:,} bytes)")
                    return True
                    
                except Exception as e:
                    if attempt < 2:  # Retry
                        logger.warning(f"⚠️  Attempt {attempt + 1} failed: {e}. Retrying...")
                        time.sleep(2)
                        continue
                    else:
                        raise e
                        
        except Exception as e:
            logger.error(f"❌ Failed to download {paper['title']}: {e}")
            if file_path.exists():
                file_path.unlink()  # Remove partial file
            return False
        
        return False
    
    def download_all_papers(self):
        """Download all papers organized by category."""
        logger.info("🚀 Starting Cohere Labs Scholars Program paper downloads...")
        
        total_papers = sum(len(papers) for papers in self.papers.values())
        downloaded = 0
        failed = []
        
        for category, papers in self.papers.items():
            logger.info(f"\n📁 Category: {category} ({len(papers)} papers)")
            
            for paper in papers:
                if self.download_paper(category, paper):
                    downloaded += 1
                else:
                    failed.append(f"{category}/{paper['filename']}")
                
                # Small delay between downloads
                time.sleep(1)
        
        # Summary
        logger.info(f"\n📊 Download Summary:")
        logger.info(f"✅ Successfully downloaded: {downloaded}/{total_papers}")
        
        if failed:
            logger.info(f"❌ Failed downloads: {len(failed)}")
            for paper in failed:
                logger.info(f"   - {paper}")
        else:
            logger.info("🎉 All papers downloaded successfully!")
    
    def create_paper_index(self):
        """Create an index file listing all downloaded papers."""
        index_file = self.base_dir / "PAPER_INDEX.md"
        
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write("# Cohere Labs Scholars Program 2026 - Paper Index\n\n")
            f.write("## 📚 Downloaded Papers by Category\n\n")
            
            for category, papers in self.papers.items():
                f.write(f"### {category} ({len(papers)} papers)\n\n")
                
                for i, paper in enumerate(papers, 1):
                    file_path = self.papers_dir / category / paper["filename"]
                    status = "✅" if file_path.exists() else "❌"
                    
                    f.write(f"{i}. **{paper['title']}** {status}\n")
                    f.write(f"   - File: `{paper['filename']}`\n")
                    f.write(f"   - URL: {paper['url']}\n\n")
            
            f.write("---\n")
            f.write(f"*Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}*\n")
        
        logger.info(f"📄 Created paper index: {index_file}")


def main():
    """Main execution function."""
    base_dir = Path(__file__).parent
    downloader = PaperDownloader(base_dir)
    
    # Download all papers
    downloader.download_all_papers()
    
    # Create index
    downloader.create_paper_index()
    
    logger.info("🎓 Cohere Labs Scholars Program setup complete!")


if __name__ == "__main__":
    main()
