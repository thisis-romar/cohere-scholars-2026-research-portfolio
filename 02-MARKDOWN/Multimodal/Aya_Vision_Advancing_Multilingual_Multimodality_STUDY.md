# Aya Vision: Advancing the Frontier of Multilingual Multimodality

**Authors:** Saurabh Dash, Yiyang Nan, John Dang, Arash Ahmadian, Shivalika Singh, Madeline Smith, Bharat Venkitesh, Vlad Shmyhlo, Viraat Aryabumi, Walter Beller-Morales, Jeremy Pekmez, Jason Ozuzu, Pierre Richemond, Acyr Locatelli, Nick Frosst, Phil Blunsom, Aidan Gomez, Ivan Zhang, Marzieh Fadaee, Manoj Govindassamy, Sudip Roy, Matthias Gallé, Beyza Ermis, Ahmet Üstün, and Sara Hooker

**Affiliation:** Cohere Labs, Cohere

## Abstract

Building multimodal language models is fundamentally challenging: it requires aligning vision and language modalities, curating high-quality instruction data, and avoiding the degradation of existing text-only capabilities once vision is introduced. These difficulties are further magnified in the multilingual setting, where the need for multimodal data in different languages exacerbates existing data scarcity, machine translation often distorts meaning, and catastrophic forgetting is more pronounced. 

To address these challenges, we introduce **novel techniques spanning both data and modeling**:

1. **Synthetic annotation framework** that curates high-quality, diverse multilingual multimodal instruction data
2. **Cross-modal model merging technique** that mitigates catastrophic forgetting while enhancing multimodal performance

**Key Results:**
- **Aya-Vision-8B** achieves best-in-class performance compared to strong multimodal models (Qwen-2.5-VL-7B, Pixtral-12B, Llama-3.2-90B-Vision) with up to 79% win rate
- **Aya-Vision-32B** outperforms models more than twice its size (Molmo-72B, LLaMA-3.2-90B-Vision) with win rates up to 72.4%

**Model Links:**
- Aya-Vision-8B: https://huggingface.co/CohereLabs/aya-vision-8B
- Aya-Vision-32B: https://huggingface.co/CohereLabs/aya-vision-32B
- AyaVisionBench: https://huggingface.co/datasets/CohereLabs/AyaVisionBench

## 1. Introduction

Although multimodal large language models (MLLMs) have demonstrated remarkable success in jointly reasoning over various modalities, their performance remains predominantly confined to English. This linguistic limitation represents a substantial bottleneck in advancing multilingual AI, restricting global accessibility and impact.

### Key Challenges Addressed

**1. Data Scarcity Challenge:**
- High-quality multimodal instruction-tuning datasets are scarce and primarily English-focused
- Existing datasets contain short, simplistic, task-oriented image-text pairs inadequate for conversational scenarios
- Machine translation introduces "translationese" artifacts, biases, and fails to capture cultural nuances

**2. Catastrophic Forgetting Challenge:**
- Integrating vision modalities commonly results in catastrophic forgetting of language skills
- This decay is amplified when expanding coverage across multiple languages
- Traditional approaches using data mixtures prove insufficient for maintaining text capabilities

**3. Evaluation Gap:**
- Existing multimodal benchmarks emphasize academic-style, multiple-choice tasks
- Few benchmarks support complex, open-ended interactions
- Multilingual multimodal evaluation remains largely unexplored

### Our Contributions

1. **State-of-the-art multilingual multimodal LLMs:** Aya-Vision-8B and 32B models covering 23 languages
2. **Novel synthetic annotation framework:** Combines synthetic data distillation, automated translation, and context-aware rephrasing
3. **Cross-modal model merging:** Training-free approach that recovers text capabilities while enhancing multimodal performance
4. **Comprehensive evaluation suite:** AyaVisionBench and m-WildVision for real-world multilingual multimodal evaluation

## 2. Multilingual Multimodal Data Framework

### 2.1 Data Collection

We constructed a diverse English-language multimodal instruction-tuning corpus from established open-source resources:

- **Cauldron:** Large-scale collection of 50 vision-language datasets (~30M samples)
- **PixMo:** Comprehensive dataset spanning seven multimodal tasks (~6M samples)
- **Additional sources:** SlideVQA, PDFVQA, ScreenQA

**Final dataset:** ~2.29M samples across 9 task categories:
- Visual Question Answering (24.5%)
- OCR/Document Understanding (21.4%)
- Chart/Figure Analysis (12.6%)
- Captioning (9.6%)
- Table Comprehension (9.2%)
- Logical Reasoning (11.0%)
- 2-Image Comparison (10.4%)
- Textbook Questions (0.9%)
- Screenshot→Code (0.4%)

### 2.2 Distillation-based Recaptioning

**Problem:** Original datasets exhibit limited linguistic diversity and constrained stylistic variation, with average caption length of just 14.2 words.

**Solution:** Generate synthetic alternatives using task-specific prompt templates for teacher models:
- **Reasoning tasks:** Structured prompts eliciting step-by-step explanations
- **Captioning prompts:** Emphasis on detailed, informative descriptions
- **VQA prompts:** Designed for accurate, image-grounded answers

**Impact Metrics:**
- Average word count: 14.2 → 100.1
- Token count: 27.2 → 140.8
- Lexical diversity (MTLD): 11.0 → 61.2

### 2.3 Two-Stage Filtering Pipeline

**Stage 1: Keyword-based filtering**
- Identifies common failure modes (refusals, repeated phrases)
- Flags samples for regeneration or removal

**Stage 2: LLM-based semantic filtering**
- Uses command-r-plus-08-2024 for semantic verification
- Ensures recaptions don't alter underlying meaning
- Overall error rate: 3.2% (62,370 samples removed)

### 2.4 Hybrid Translation Pipeline

**Challenge:** Balance between language coverage and translation quality, especially for low-resource languages.

**Our Approach:**
1. **Machine Translation:** NLLB-3.3B model for 22 languages
2. **LLM Post-editing:** command-r-plus-08-2024 for refinement and artifact correction

**Quality Improvement:**
- NLLB baseline COMET score: 0.7455
- After post-editing: 0.8293
- **Improvement:** +0.08 COMET points (substantial quality gain)

## 3. Cross-Modal Model Merging

### 3.1 The Catastrophic Forgetting Problem

**Challenge:** Multimodal training typically degrades text-only performance, even with 10% text data inclusion in training mixtures.

**Traditional Approach Limitations:**
- Data mixture optimization requires extensive ablations
- Reintroducing text data can lead to overfitting
- Multi-stage post-training can cause instability

### 3.2 Our Cross-Modal Merging Solution

**Key Insight:** Since multimodal models are initialized from preference-tuned LLM checkpoints, they share optimization trajectories, making them amenable to merging.

**Method:** Linear interpolation between text-only LLM and multimodal LLM backbone:

```
W_merged = α·W_mm-LLM + (1-α)·W_text-LLM
```

**Results:**
- **Text performance recovery:** Up to 50.2% improvement in text win-rates
- **Multimodal enhancement:** Up to 20.5% improvement in vision win-rates
- **Scale effect:** Significantly larger gains at 32B scale (up to 3x vs 8B)

### 3.3 Training Data Composition

**Final mixture (2.75M samples):**
1. **Synthetically re-annotated English data (35%):** High-quality recaptioned content
2. **Multilingual datasets (31%):** Translated and refined content across 22 languages
3. **High-quality original datasets (34%):** Selected for syntactic accuracy requirements

## 4. Architecture and Training

### 4.1 Model Architecture

**Vision Encoder:**
- **8B model:** siglip2-so400m-patch14-384 (reduced activation footprint)
- **32B model:** siglip2-so400m-patch16-512 (higher resolution)

**Image Processing:**
- Arbitrary resolution support via aspect-ratio-preserving resizing
- Up to 12 non-overlapping tiles + thumbnail
- Pixel Shuffle downsampling (4x reduction in tokens)
- Maximum tokens: 2,197 (8B) / 3,328 (32B)

**Vision-Language Connector:**
- 2-layer MLP with SwiGLU activation
- **8B:** 190M parameters
- **32B:** 428M parameters

**Language Model:**
- **8B:** Command-R7B + Aya Expanse post-training
- **32B:** Aya-Expanse-32B

### 4.2 Training Pipeline

**Stage 1: Vision-Language Alignment**
- Freeze vision encoder and language model
- Train only connector with high learning rate
- **8B:** 9.7k steps, LR 10^-4
- **32B:** 19k steps, LR 10^-3

**Stage 2: Visual Instruction Fine-tuning**
- Train connector + LLM, freeze vision encoder
- Batch size: 128, 31k iterations
- **8B:** LR 10^-4
- **32B:** LR 5×10^-4

## 5. Evaluation Framework

### 5.1 Novel Benchmarks Introduced

**AyaVisionBench:**
- 135 image-question pairs × 23 languages = 3,105 total samples
- 9 diverse task categories covering real-world scenarios
- Human-verified translations and reference answers
- Focuses on generative, open-ended instruction following

**m-WildVision:**
- Multilingual extension of WildVision-Bench
- 22 languages beyond English
- Real-world user interaction scenarios
- Practical, context-rich evaluation

### 5.2 Comprehensive Evaluation Suite

**Multimodal Academic Benchmarks:**
- xMMMU (7 languages), MaXM (7 languages)
- CVQA (31 languages), MTVQA (9 languages)
- Kaleidoscope (18 languages)

**Text-Only Benchmarks:**
- m-ArenaHard (23 languages), MGSM (10 languages)
- Global MMLU-Lite (42 languages), FLORES (22 languages)

**Evaluation Protocol:**
- VLM-as-a-Judge using claude-3-7-sonnet-20250219
- Pairwise comparisons for preference evaluation
- Focus on human-centric dimensions: relevance, fluency, engagement

## 6. Results Analysis

### 6.1 Multimodal Performance

**Aya-Vision-8B vs Competitors:**
- **vs Qwen-2.5-VL-7B:** 55.7% win rate on m-ArenaHard
- **vs Gemma-Flash-1.5-8B:** 69.3% win rate average
- **vs Pixtral-12B:** 55.7% win rate average
- **vs Llama-3.2-11B-Vision:** Best-in-class performance

**Aya-Vision-32B vs Larger Models:**
- **vs Llama-3.2-90B-Vision:** 54.0% win rate (despite 2.8x parameter difference)
- **vs Molmo-72B:** 72.4% win rate (despite 2.25x parameter difference)
- **vs Qwen-2.5-VL-72B:** 50.9% win rate (despite 2.25x parameter difference)

### 6.2 Cross-Modal Merging Impact

**Text Performance Recovery:**
- Aya-Vision-8B: +50.2% improvement in text win-rates
- Aya-Vision-32B: +30.1% improvement in text win-rates

**Multimodal Performance Enhancement:**
- Aya-Vision-8B: +20.5% improvement in vision win-rates  
- Aya-Vision-32B: +15.3% improvement in vision win-rates

### 6.3 Language-Specific Performance

**Consistent Excellence Across Languages:**
- Strong performance maintained across all 23 supported languages
- No significant degradation in low-resource languages
- Effective cross-lingual transfer demonstrated

### 6.4 Academic Benchmark Results

**Multilingual Mathematical Reasoning (MGSM):**
- Aya-Vision-8B: 67.0% accuracy (best in 8B class)
- Aya-Vision-32B: 73.4% accuracy (competitive with much larger models)

**Machine Translation (FLORES):**
- Aya-Vision-8B: 57.2 chrF++, 93.2 xCOMET (best in class)
- Aya-Vision-32B: 58.8 chrF++, 93.5 xCOMET (best in class)

## 7. Technical Innovations Deep Dive

### 7.1 Context-Aware Rephrasing

**Innovation:** Replace naive translation with specialized translation model + LLM correction pipeline.

**Benefits:**
- Removes systematic translationese artifacts
- Preserves cultural and contextual nuances
- Maintains semantic fidelity across languages
- 11.24% improvement over NLLB-3.3B baseline

### 7.2 Cross-Modal Model Merging Theory

**Theoretical Foundation:**
- Shared optimization trajectories enable effective merging
- Cross-lingual transfer provides diversity while maintaining performance
- Linear interpolation proves most consistent across scales

**Practical Implementation:**
- No additional training required
- Preserves vision encoder and alignment layers from multimodal model
- Scales effectively (3x better gains at 32B vs 8B)

### 7.3 Synthetic Data Quality Control

**Multi-layered Validation:**
1. Task-specific prompt engineering for quality
2. Keyword-based filtering for obvious failures
3. LLM-based semantic verification for subtle errors
4. Human verification for benchmark data

**Quality Metrics:**
- Error rate reduction: 3.2% overall filtering
- Lexical diversity improvement: 11.0 → 61.2 MTLD
- Natural conversation capability enhancement

## 8. Broader Impact and Future Directions

### 8.1 Advancing Multilingual AI Equity

**Global Accessibility:**
- Serves 23 languages spoken by half the world's population
- Reduces English-centric bias in multimodal AI
- Enables culturally-aware AI interactions

**Research Democratization:**
- Open-weight model release
- Comprehensive benchmark suite for community use
- Reproducible methodology for other language families

### 8.2 Technical Paradigm Shifts

**Data-Efficient Training:**
- Cross-modal merging reduces need for massive multimodal datasets
- Synthetic annotation framework scalable to new languages
- Training-free capability enhancement

**Evaluation Methodology:**
- Focus on real-world, conversational evaluation
- Human-centric quality metrics
- Multilingual benchmark standardization

### 8.3 Future Research Directions

**Immediate Extensions:**
- Extension to more language families
- Integration with reasoning capabilities
- Enhanced cultural understanding

**Long-term Vision:**
- Universal multilingual multimodal understanding
- Real-time cross-cultural communication
- Equitable AI access across global communities

## 9. Conclusion

Aya Vision represents a significant advancement in multilingual multimodal AI, demonstrating that it's possible to achieve state-of-the-art performance across languages and modalities without massive computational resources. Our key innovations:

1. **Hybrid synthetic data framework** that addresses multilingual data scarcity while maintaining quality
2. **Cross-modal model merging** that efficiently preserves text capabilities while enhancing multimodal performance
3. **Comprehensive evaluation methodology** that prioritizes real-world applicability

**Impact:** By releasing open-weight models and comprehensive benchmarks, we accelerate progress toward truly global, equitable AI systems that serve diverse linguistic communities with equal capability.

---

## Research Significance for Cohere Scholars Application

This research exemplifies the cutting-edge intersection of multilingual and multimodal AI that represents the future of human-computer interaction:

### 1. Technical Excellence
- **Novel methodologies:** Context-aware rephrasing and cross-modal merging represent genuine innovations
- **Scalable solutions:** Techniques that work across model sizes and can be applied to new language families
- **Rigorous evaluation:** Comprehensive benchmarking with focus on real-world applicability

### 2. Global Impact Alignment
- **Equity-focused design:** Explicit focus on reducing English-centric bias in AI systems
- **Cultural sensitivity:** Recognition that translation alone is insufficient for true multilingual AI
- **Accessibility advancement:** Making advanced AI capabilities available to diverse global communities

### 3. Research Leadership
- **Open science commitment:** Release of models, datasets, and benchmarks for community benefit
- **Methodological rigor:** Multi-stage validation and human verification processes
- **Performance excellence:** State-of-the-art results across multiple evaluation frameworks

### 4. Future-Oriented Vision
- **Paradigm advancement:** Moving beyond English-only multimodal AI toward truly global systems
- **Efficient innovation:** Achieving superior results with smaller, more efficient models
- **Sustainable scaling:** Training-free techniques that reduce computational requirements

This work demonstrates deep understanding of the challenges and opportunities in developing AI systems that can serve global communities effectively and equitably.