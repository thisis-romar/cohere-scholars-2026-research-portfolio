# M-REWARDBENCH: Evaluating Reward Models in Multilingual Settings

**Authors:** Srishti Gureja♦¹ Lester James V. Miranda♦² Shayekh Bin Islam♦³,⁵ Rishabh Maheshwary♦⁴ Drishti Sharma⁵ Gusti Winata⁵ Nathan Lambert² Sebastian Ruder⁶* Sara Hooker¹ Marzieh Fadaee¹

**Affiliations:** ¹Cohere Labs ²Allen Institute for AI ³KAIST ⁴ServiceNow ⁵Cohere Labs Community ⁶Meta  
**Contact:** {srishtigureja,marzieh}@cohere.com | Website: m-rewardbench.github.io

## Abstract

Reward models (RMs) have driven the state-of-the-art performance of LLMs today by enabling the integration of human feedback into the language modeling process. However, RMs are primarily trained and evaluated in English, and their capabilities in multilingual settings remain largely understudied. 

In this work, we conduct a systematic evaluation of several reward models in multilingual settings. We first construct the **first-of-its-kind multilingual RM evaluation benchmark, M-REWARDBENCH**, consisting of **2.87k preference instances for 23 typologically diverse languages**, that tests the chat, safety, reasoning, and translation capabilities of RMs. We then rigorously evaluate a wide range of reward models on M-REWARDBENCH, offering fresh insights into their performance across diverse languages. 

**Key Findings:**
- **Significant performance gap** between English and non-English languages (up to 13% drop)
- **RM preferences change substantially** from one language to another
- **Translation quality positively correlates** with RM performance
- **High-resource languages** consistently outperform low-resource languages

We release the M-REWARDBENCH dataset and codebase to facilitate better understanding of RM evaluation in multilingual settings.

## 1. Introduction

Reward models (RMs) are central to aligning state-of-the-art large language models with human preferences. They serve as an oracle that reflects preferred human values and enables steering language models towards safety, reasoning, and instruction-following capabilities. As LLMs permeate daily life and are used worldwide, it is crucial to understand how their building blocks behave beyond resource-rich languages such as English or Chinese.

### The Multilingual Evaluation Gap

Despite their crucial role, reward model development and evaluation remain sparse, especially in multilingual contexts. This is partly due to the limited work extending preference alignment to multilingual settings. The few evaluations to date, such as RewardBench and RMB, are in English and do not cover tasks related to multilinguality such as translating from one language to another or answering user requests that involve cultural nuance.

### Our Contributions

We seek to fill this gap by curating resources and conducting a systematic evaluation of state-of-the-art reward models in multilingual settings:

1. **Bridge the resource gap** by curating M-REWARDBENCH, a massively multilingual preference evaluation dataset in 23 languages across 5 tasks
2. **Close the evaluation gap** by evaluating a wide range of both proprietary and open-source reward models 
3. **Provide analyses and insights** on multilingual robustness and the impact of translation quality on RM performance

## 2. M-REWARDBENCH: Multilingual Benchmark Design

### 2.1 Design Philosophy

Our benchmark evaluates RMs on both:
- **General-purpose capabilities** in diverse languages (Chat, Safety, Reasoning)
- **Multilingual-specific knowledge** (Translation tasks)

### 2.2 Dataset Construction

**Language Selection:** 23 typologically diverse languages including:
- **8 unique scripts:** Latin, Cyrillic, Arabic, Hebrew, Devanagari, Greek, Japanese, Hangul
- **8 language families:** Indo-European, Sino-Tibetan, Afro-Asiatic, Turkic, Japonic, Koreanic, Austronesian, Austroasiatic
- **12 unique language subgroups**

**Dataset Statistics:**
- **Total:** 2.87k preference instances
- **General-purpose:** Chat (296), Chat-Hard (407), Safety (736), Reasoning (1,430)
- **Translation:** 400 instances across Chinese↔English and German↔English

### 2.3 Translation and Quality Control

**Translation Pipeline:**
1. **Automatic Translation:** Google Translate API (superior performance over alternatives)
2. **Human Validation:** Native speaker review and filtering
3. **Quality Filtering:** Remove English-specific concepts and translation errors

**Translation Task Design:**
- **TRANSLATION-EASY:** Clear quality differences between chosen/rejected responses
- **TRANSLATION-HARD:** Subtle quality differences requiring nuanced judgment
- **Four directions:** de→en, zh→en, en→de, en→zh

## 3. Experimental Framework

### 3.1 Reward Model Types Evaluated

**25 representative models** across three categories:

1. **Generative RMs:** LLaMA 3.1 Instruct, Aya Expanse (LLM-as-a-Judge)
2. **Classifier RMs:** Eurus RM 7B, Tülu 2.5 13B RM (explicit reward scoring)
3. **Implicit RMs:** Zephyr 7B, Tülu 2 DPO (DPO-trained models)

**Parameter Range:** 3B to 104B parameters

### 3.2 Evaluation Methodology

**Scoring Metric:** Accuracy-based evaluation comparing RM preferences to human-chosen references

**Evaluation Strategy:** Type-specific approaches following RewardBench conventions:
- **Weighted averaging** across subsets based on prompt counts
- **Language-specific scoring** for detailed analysis
- **Cross-lingual consistency** measured via Cohen's κ

## 4. Key Results and Findings

### 4.1 Performance Gap Analysis

**Dramatic English vs. Multilingual Performance Drop:**
- **Maximum drop:** 13% for some models
- **Average drop:** 3% for Generative RMs, 8%+ for Classifier and Implicit RMs
- **Strong correlation (r=0.92)** between English and multilingual performance

**Model Type Performance:**
- **Generative RMs:** Superior multilingual capabilities, lower variance across languages
- **Classifier RMs:** Moderate multilingual degradation  
- **Implicit RMs:** Highest performance drops, least consistent across languages

### 4.2 Category-Specific Performance

**Performance Drop by Category:**
- **Chat:** Most significant degradation for non-Generative RMs
- **Chat-Hard:** Universal decline (average 5.96% drop)
- **Safety & Reasoning:** Smaller declines due to objective ground truth
- **Translation:** New dimension revealing multilingual-specific capabilities

### 4.3 Cross-Lingual Consistency

**Label Agreement Analysis:**
- **No model achieves perfect agreement (κ=1)** between English and other languages
- **High-performing models ≠ most consistent models**
- **Chat category:** Highest disagreement rates
- **Safety/Reasoning:** More consistent due to verifiable answers

### 4.4 Translation Task Performance

**Direction Effects:**
- **English→Other:** Generally better performance than Other→English
- **Task Difficulty:** Consistent drop from Easy to Hard translations
- **Language-Specific Patterns:** German and Chinese show different directional preferences

## 5. Multilingual Analysis Deep Dive

### 5.1 Translation Quality Impact

**Google Translate vs. NLLB 3.3B Comparison:**
- **1-3% performance improvement** with higher-quality translation
- **Generative RMs benefit most** from translation quality
- **Implicit RMs show highest sensitivity** to translation differences

### 5.2 Linguistic Dimension Analysis

**Resource Availability Impact:**
- **Higher-resource languages consistently outperform** lower-resource languages
- **Class-5 languages (highest resources):** Best performance
- **Class-3 languages (lowest resources):** Poorest performance

**Language Family Effects:**
- **Indo-European & Sino-Tibetan:** Highest scores (~67.5%)
- **Afro-Asiatic & Turkic:** Lower scores (~62.5%)
- **Training data availability correlation** with family performance

**Script Type Influence:**
- **Latin & Cyrillic scripts:** Best performance (~67.5%)
- **Prevalence in high-resource languages** drives superior results
- **Script familiarity affects** RM evaluation capabilities

### 5.3 Language-Specific Performance

**Performance Range:**
- **Highest:** Portuguese (68.7%)
- **Lowest:** Arabic (62.8%)
- **Range:** ~6% difference across languages

## 6. Human Evaluation Validation

### 6.1 Translation Quality Preservation

**Native Speaker Validation Results:**
- **Before refinement:** 80-86% agreement with original preferences
- **After refinement:** 94-98% agreement with original preferences
- **High-quality preservation** of preference judgments across languages

### 6.2 Cultural Preference Variations

**Observed Phenomena:**
- **Preference inversions** between English and other languages
- **Cultural nuance impacts** on response appropriateness
- **Context-dependent variations** in human judgment

## 7. Technical Innovations and Methodological Advances

### 7.1 Benchmark Design Innovations

**Comprehensive Coverage:**
- **First multilingual RM benchmark** spanning 23 languages
- **Novel translation task evaluation** for multilingual capabilities
- **Rigorous quality control** with human validation

**Scalable Methodology:**
- **Automated translation pipeline** with quality filtering
- **Multiple difficulty levels** for nuanced evaluation
- **Cross-lingual consistency metrics** for robustness assessment

### 7.2 Evaluation Framework Advances

**Multi-Type RM Assessment:**
- **Unified evaluation** across Generative, Classifier, and Implicit RMs
- **Type-specific scoring** adapted to different architectures
- **Comparative analysis** revealing architectural strengths/weaknesses

**Linguistic Analysis Framework:**
- **Systematic categorization** by resource availability, family, script
- **Statistical correlation analysis** between linguistic features and performance
- **Cultural preference exploration** through human evaluation

## 8. Implications for AI Safety and Alignment

### 8.1 Global AI Safety Considerations

**Multilingual Alignment Challenges:**
- **Preference variation** across cultural contexts
- **Language-specific safety** considerations
- **Cultural value representation** in reward models

**Equity and Fairness Issues:**
- **Performance disparities** across language communities
- **Resource availability bias** in model capabilities
- **Digital divide implications** for global AI access

### 8.2 Technical Development Recommendations

**Improved Training Strategies:**
- **Multilingual preference data** collection and curation
- **Cross-lingual consistency** optimization techniques
- **Cultural sensitivity** in preference annotation

**Evaluation Best Practices:**
- **Mandatory multilingual evaluation** for global deployment
- **Resource-aware benchmarking** for fair comparison
- **Cultural context consideration** in preference assessment

## 9. Future Research Directions

### 9.1 Benchmark Extensions

**Language Coverage Expansion:**
- **Additional language families** and scripts
- **Low-resource language focus** for inclusivity
- **Cultural preference datasets** for nuanced evaluation

**Task Diversification:**
- **Culture-specific tasks** beyond translation
- **Contextual preference evaluation** across domains
- **Real-world deployment** scenario testing

### 9.2 Model Development

**Multilingual RM Architecture:**
- **Native multilingual training** approaches
- **Cross-lingual transfer** optimization
- **Cultural adaptation** mechanisms

**Alignment Methodology:**
- **Multilingual RLHF** techniques
- **Cross-cultural preference** learning
- **Global value alignment** frameworks

## 10. Limitations and Considerations

### 10.1 Current Limitations

**Scope Constraints:**
- **23 languages** (fraction of world's linguistic diversity)
- **Automatic translation reliance** vs. human-written translations
- **Generalization to downstream** performance unclear

**Evaluation Constraints:**
- **Cultural preference oversimplification** in current benchmark
- **Limited cultural context** representation
- **Scalability challenges** for global deployment

### 10.2 Ethical Considerations

**Cultural Sensitivity:**
- **Western-centric bias** in preference foundations
- **Cultural value representation** challenges
- **Global perspective inclusion** in future development

**Responsible Development:**
- **Transparent limitation** acknowledgment
- **Community input** incorporation
- **Iterative improvement** based on global feedback

## 11. Conclusion

M-REWARDBENCH represents a significant advancement in multilingual AI evaluation, revealing critical gaps in current reward model capabilities across languages. Our systematic evaluation of 25 reward models across 23 languages demonstrates that:

1. **Substantial performance gaps** exist between English and non-English languages
2. **Model architecture significantly impacts** multilingual robustness
3. **Translation quality and resource availability** strongly correlate with performance
4. **Cultural and linguistic diversity** requires specialized evaluation approaches

**Impact for Global AI Development:**
- **Mandatory multilingual evaluation** for responsible deployment
- **Architectural innovations** needed for equitable performance
- **Cultural sensitivity** integration in preference learning
- **Resource investment** in underrepresented language communities

By releasing M-REWARDBENCH, we provide the research community with essential tools for developing more equitable, globally-capable reward models that can serve diverse linguistic communities with equal effectiveness.

---

## Research Significance for Cohere Scholars Application

This research represents the cutting edge of AI safety and alignment research in multilingual contexts, demonstrating several critical competencies:

### 1. AI Safety Leadership
- **Reward Model Evaluation:** Deep understanding of RLHF and preference learning systems
- **Multilingual Alignment:** Recognition that AI safety extends beyond English-centric evaluation
- **Systematic Evaluation:** Rigorous methodology for assessing AI systems across diverse contexts
- **Bias Detection:** Identification of systematic biases affecting global AI deployment

### 2. Technical Excellence
- **Benchmark Innovation:** Creation of first-of-its-kind multilingual evaluation framework
- **Comprehensive Analysis:** 25 models × 23 languages × multiple task categories
- **Statistical Rigor:** Advanced metrics (Cohen's κ) for cross-lingual consistency analysis
- **Architectural Understanding:** Comparative analysis across Generative, Classifier, and Implicit RMs

### 3. Global Impact Focus
- **Equity-Centered Research:** Explicit focus on addressing digital divides and language disparities
- **Cultural Sensitivity:** Recognition of cultural variation in human preferences
- **Resource Democratization:** Open-source release of benchmark and evaluation tools
- **Community Building:** Collaborative authorship spanning academic and industry institutions

### 4. Research Leadership
- **Problem Identification:** Recognition of critical gap in multilingual RM evaluation
- **Solution Development:** Comprehensive benchmark addressing real-world deployment needs
- **Community Impact:** First author on foundational research enabling future developments
- **Interdisciplinary Approach:** Integration of linguistics, machine learning, and cultural studies

This work demonstrates exactly the kind of forward-thinking, globally-conscious AI research that aligns perfectly with Cohere's mission of building AI systems that serve all of humanity equitably and safely.