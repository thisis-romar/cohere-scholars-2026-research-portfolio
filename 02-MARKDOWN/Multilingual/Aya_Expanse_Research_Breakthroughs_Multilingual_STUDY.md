# Aya Expanse: Combining Research Breakthroughs for a New Multilingual Frontier

**Authors:** John Dang, Shivalika Singh, Daniel D'souza, Arash Ahmadian, Alejandro Salamanca, Madeline Smith, Aidan Peppin, Sungjin Hong, Manoj Govindassamy, Terrence Zhao, Sandra Kublik, Meor Amer, Viraat Aryabumi, Jon Ander Campos, Yi-Chern Tan, Tom Kocmi, Florian Strub, Nathan Grinsztajn, Yannis Flet-Berliac, Acyr Locatelli, Hangyu Lin, Dwarak Talupuru, Bharat Venkitesh, David Cairuz, Bowen Yang, Tim Chung, Wei-Yin Ko, Sylvie Shang Shi, Amir Shukayev, Sammie Bae, Aleksandra Piktus, Roman Castagné, Felipe Cruz-Salinas, Eddie Kim, Lucas Crawhall-Stein, Adrien Morisot, Sudip Roy, Phil Blunsom, Ivan Zhang, Aidan Gomez, Nick Frosst, Marzieh Fadaee, Beyza Ermis, Ahmet Üstün, and Sara Hooker

**Affiliation:** Cohere For AI, Cohere

## Abstract

We introduce the Aya Expanse model family, a new generation of 8B and 32B parameter multilingual language models, aiming to address the critical challenge of developing highly performant multilingual models that match or surpass the capabilities of monolingual models. By leveraging several years of research at Cohere For AI and Cohere, including advancements in data arbitrage, multilingual preference training, and model merging, Aya Expanse sets a new state-of-the-art in multilingual performance. Our evaluations on the Arena-Hard-Auto dataset, translated into 23 languages, demonstrate that Aya Expanse 8B and 32B outperform leading open-weight models in their respective parameter classes, including Gemma 2, Qwen 2.5, and Llama 3.1, achieving up to a 76.6% win-rate. Notably, Aya Expanse 32B outperforms Llama 3.1 70B, a model with twice as many parameters, achieving a 54.0% win-rate. In this short technical report, we present extended evaluation results for the Aya Expanse model family and release their open-weights, together with a new multilingual evaluation dataset m-ArenaHard.

**Model Links:**
- Aya Expanse 8B: https://hf.co/CohereForAI/aya-expanse-8b
- Aya Expanse 32B: https://hf.co/CohereForAI/aya-expanse-32b
- m-ArenaHard Dataset: https://hf.co/datasets/CohereForAI/m-ArenaHard

## 1. Introduction

We introduce the Aya Expanse, a family of multilingual instruction-tuned language models that support 23 languages, built upon the recent Cohere's Command series. Developed by Cohere For AI and Cohere, the Aya Expanse models are an open-weights release of both 8-billion and 32-billion parameters that address the significant challenge of developing high-performance multilingual models that can rival their monolingual counterparts.

Despite notable advancements in large language models, there remains a stark gap in the performance of models across multiple languages. Models achieve superior performance on languages that they are trained on, however, this leads to biases against languages unseen during training, and critical safety and security flaws for all users. Furthermore, languages that the models are not optimized for, require more tokens due to poor tokenization, leading to higher latency and cost which limits the use of this technology even further.

The Aya Expanse model family seeks to mitigate this gap through a suite of innovative methodologies, including:
- **Multilingual data arbitrage** - strategically sampling from a pool of teacher models
- **Multilingual preference optimization and safety tuning** - enhancing model alignment across languages  
- **Model merging** - leveraging cross-lingual transfer and diversity

In direct head-to-head win rate evaluations across 23 languages, Aya Expanse 8B and 32B models outperform the similar-sized leading open-weight models by up to 76.6% win-rates against Gemma 2 9B and 27B, Qwen 2.5 7B and 32B, Mistral models, and Llama 3.1 8B and 70B – even though the Llama's largest variant includes over twice as many parameters than our 32B.

## 2. Post-Training Recipe

Our post-training recipe for Aya Expanse leverages critical details from research papers we have released. We briefly describe these core drivers of performance below:

### 2.1 Synthetic Data Generation through Data Arbitrage

The use of synthetic data has become increasingly central to the development of LLMs, particularly as model training has exhausted current data sources. However, for multilingual data, especially with low-resource languages, there are few good examples of teacher models, creating an extra added challenge to leveraging synthetic data.

We demonstrate that these limitations can be addressed through "**data arbitrage**" – strategically sampling from a pool of teacher models. This approach challenges the traditional reliance on a single-teacher model for generating synthetic data. Instead, data arbitrage leverages performance variations among a pool of models.

**Key Innovation:** In Reward-Based Routing, for each prompt in a given language, we generate completions from all models in the pool and score them using the reward model. The completion with the highest score is chosen as the final completion for that prompt.

**Results:** Aya Expanse 8B model, even at the SFT stage trained with Multilingual Arbitrage, had over 9.1% improvement in win-rate measured against Gemma 2 9B compared to the previous Aya 23 model.

### 2.2 Iterative Multilingual Preference Training

Following supervised fine-tuning, alignment to human preferences is a key step for training today's state-of-the-art LLMs. Although heavily adopted, preference training is already challenging in a monolingual setting. Maximizing gains from preference training in a multilingual setting introduces even more challenges:

- The vast majority of existing preference datasets are exclusively English
- The few existing multilingual preference datasets are often of low-quality
- Modeling many diverse languages simultaneously is a difficult optimization problem

**Our Approach:** We leverage a novel synthetic data generation technique to construct high-quality multilingual preference data pairs by contrasting in-language completions from a highly performant multilingual LLM with lower quality completions translated from English.

**Training Pipeline:**
1. **Offline preference training:** Train on data curated by taking the highest and lowest reward responses from the Arbitrage stage
2. **Online iterative DPO:** Sample multiple online generations, rank with internal Reward Model, train on preference pairs
3. **3 iterations optimal:** Going beyond 3 iterations led to minimal gains at the cost of additional re-tuning

**Results:** For Aya Expanse 8B, the combination of offline and online preference training led to 7.1% additional gains in win rate against Gemma 2 9B.

### 2.3 Model Merging

A reappearing problem throughout any post-training pipeline is choosing the right data mixtures for training. Merging multiple models is an alternative approach for enabling complex multi-tasking at a reduced aggregate computational cost.

**Strategy for Diversity:** To maximize diversity between checkpoints while ensuring high performance:
- Train models for different language families
- Take advantage of cross-lingual transfer benefits
- Include shared languages across clusters (English, Spanish, French) for robustness

**Merging Techniques Tested:**
- Weighted linear averaging (most consistent - used throughout pipeline)
- SLERP
- TIES-merging  
- DARE-TIES

**Scale Effect:** We observed significantly larger gains from merging at the 32B scale compared to the 8B scale – up to 3x improvement.

## 3. Model Architecture and Experimental Details

The Aya Expanse model family is based on the recent Cohere Command series which are pre-trained using a data mixture that includes texts from **23 languages**: Arabic, Chinese (simplified & traditional), Czech, Dutch, English, French, German, Greek, Hebrew, Hindi, Indonesian, Italian, Japanese, Korean, Persian, Polish, Portuguese, Romanian, Russian, Spanish, Turkish, Ukrainian and Vietnamese.

**Technical Specifications:**
- **8B model:** Maximum context length of 8K
- **32B model:** Maximum context length of 128K  
- **Architecture:** SwiGLU activation function, RoPE positional embeddings, grouped-query attention
- **Chat template:** Special tokens for roles (user, chatbot) and chat turns

## 4. Multilingual Evaluation

We follow the comprehensive evaluation framework with 8 datasets across 6 task categories for up to 23 languages:

### 4.1 Evaluation Categories

1. **Preference Evaluation:**
   - **Multilingual ArenaHard:** 500 English LMARENA Arena-Hard-Auto prompts translated into 22 languages
   - **Dolly Evaluation Sets:** Machine-translated and human-edited test sets

2. **Discriminative Tasks:**
   - XWinograd, XCOPA, XStoryCloze (zero-shot evaluation)

3. **General Language Understanding:**
   - **Global-MMLU:** 13,062 questions across 57 tasks covering STEM, humanities, social sciences (5-shot)
   - **INCLUDE:** 22,637 questions from local academic/professional exams in 44 languages

4. **Multilingual Mathematical Reasoning:**
   - **MGSM:** 250 problems from GSM8K translated into 10 languages (5-shot CoT)

5. **Machine Translation:**
   - **FLORES-200:** All 22 languages ↔ English translation

### 4.2 Model Comparisons

**Benchmark Models:**
- **Aya 23 (8B and 35B):** Previous generation models
- **Llama-3.1-Instruct (8B and 70B):** July 2024 release with DPO alignment
- **Gemma-2-IT (9B and 27B):** June 2024 release with RLHF
- **Ministral-8B-Instruct-2410:** Multilingual 8B model from Mistral AI
- **Mixtral-8x22B-Instruct-v0.1:** Sparse MoE model (141B total, 39B active)
- **Qwen-2.5-Instruct (7B and 32B):** September 2024 release supporting 29 languages

## 5. Results

### 5.1 Pairwise Model Comparisons for Open-ended Generations

**m-ArenaHard Win Rates:**
- **Aya Expanse 8B:** Up to 70.6% win rate vs Llama-3.1 8B
- **Aya Expanse 32B:** Up to 76.6% win rate vs Mixtral 8x22B
- **Remarkable Achievement:** Aya Expanse 32B achieves 54.0% win rate against Llama-3.1 70B (twice as many parameters)

**Dolly Win Rates:**
- **Aya Expanse 8B:** Up to 83.9% win rate vs Llama-3.1 8B  
- **Aya Expanse 32B:** Up to 89.9% win rate vs Mixtral 8x22B

**Language Consistency:** Aya Expanse models outperform competitors across all 23 languages individually, including English, showing equitable multilingual improvement without sacrificing high-resource language performance.

**Step-by-Step Improvement:**
- **Multilingual Arbitrage (SFT):** 9.1% improvement over Aya 23
- **Model Merging:** Additional 5.1% improvement  
- **Preference Training:** Additional 7.1% improvement
- **Total:** 20.3% increase in win rate vs Gemma 2 9B compared to Aya 23

### 5.2 Multilingual Language Understanding

**Discriminative Benchmarks:**
- **8B class:** Aya Expanse 8B (70.3 accuracy) competitive with leading models
- **32B class:** Aya Expanse 32B (72.6 accuracy) very competitive with similar parameter models

**Global-MMLU:**
- **8B:** 53.7 accuracy, competitive with Llama 3.1 (54.5)
- **32B:** 66.9 accuracy, close to Gemma 2 27B (68.3)

**INCLUDE Improvement:**
- **8B:** 3.2 accuracy improvement over Aya 23 (37.2 vs 34.0)
- **32B:** 5.7 accuracy improvement over Aya 23 (51.4 vs 45.7)

### 5.3 Multilingual Mathematical Reasoning (MGSM)

**Outstanding Performance - Largest Improvement Area:**
- **Aya Expanse 8B:** 67.0 accuracy (over 2x improvement from Aya 23's 36.5)
- **Aya Expanse 32B:** 73.4 accuracy (19.7 point increase from Aya 23's 53.7)

**Competitive Ranking:**
- Aya Expanse 8B outperforms all other 8B parameter class models
- Aya Expanse 32B outperforms Qwen 2.5 32B and Gemma 2 27B
- Only Llama 3.1 70B (78.0) performs better than Aya Expanse 32B, but has twice the parameters

### 5.4 Machine Translation (FLORES)

**Best-in-Class Performance:**
- **8B:** Aya Expanse 8B achieves highest performance with 57.2 chrF++ and 93.2 xCOMET
- **32B:** Aya Expanse 32B achieves top performance with 58.8 chrF++ and 93.5 xCOMET

**Significant Improvements:**
- Outperforms Gemma 2 9B by 1.4 xCOMET score (equivalent to +2.9 BLEU effect size)
- Maintains leadership even against models with many more parameters

## 6. Conclusion

The Aya Expanse model family represents a significant advancement in multilingual AI, addressing the critical gap between monolingual and multilingual model performance. Through innovative methodologies including:

1. **Multilingual data arbitrage** for strategic synthetic data generation
2. **Multilingual preference optimization** with offline and online training
3. **Model merging** leveraging cross-lingual transfer

**Key Achievements:**
- Sets new state-of-the-art in multilingual performance across 23 languages
- Outperforms models with significantly more parameters (Aya Expanse 32B > Llama 3.1 70B)
- Demonstrates consistent improvement across all language pairs
- Provides open-weights release to accelerate multilingual AI research

**Impact:** By making these model weights publicly available along with the m-ArenaHard dataset, we aim to contribute to future research and advance the crucial mission of inclusive language technologies.

---

## Research Significance for Cohere Scholars Application

This paper represents the cutting-edge of multilingual AI research from Cohere For AI, demonstrating:

1. **Technical Innovation:** Novel approaches to multilingual model training that outperform traditional methods
2. **Global Impact:** Focus on inclusive AI that serves all languages equitably
3. **Open Science:** Commitment to releasing models and datasets for community benefit
4. **Research Excellence:** Rigorous evaluation across multiple benchmarks and languages
5. **Scalable Solutions:** Techniques that work across different model sizes and can be applied broadly

The methodologies and insights from this research directly inform best practices for developing equitable, high-performance multilingual AI systems that can serve global communities effectively.