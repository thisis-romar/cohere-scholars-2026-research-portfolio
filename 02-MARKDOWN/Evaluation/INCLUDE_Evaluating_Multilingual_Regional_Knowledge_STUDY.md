# INCLUDE: Evaluating Multilingual Language Understanding with Regional Knowledge - Research Analysis

## Executive Summary

**Paper Title:** INCLUDE: Evaluating Multilingual Language Understanding with Regional Knowledge  
**Lead Institution:** EPFL, Cohere For AI, ETH Zurich  
**Research Type:** Multilingual Regional Knowledge Evaluation Benchmark  
**Key Innovation:** Largest collection of regional knowledge evaluation data with 197,243 QA pairs across 44 languages from local exam sources  

This research represents a crucial complement to our Global-MMLU analysis, extending cultural bias evaluation into comprehensive regional knowledge assessment while establishing new standards for authentic multilingual evaluation.

---

## 1. Research Significance & Strategic Alignment

### 1.1 Critical Problem Address
- **Regional Knowledge Gap:** Current multilingual benchmarks ignore cultural and regional knowledge contexts where LLMs would actually be deployed
- **Translation Artifacts:** Machine-translated datasets contain translationese and fail to capture regional nuances
- **Evaluation Authenticity:** Need for evaluation in actual language environments rather than artificial translated contexts
- **Digital Divide Perpetuation:** Lack of high-quality multilingual evaluation resources inhibits LLM development for underserved communities

### 1.2 Perfect Strategic Synergy with Global-MMLU
**Complementary Research Focus:**
- **Global-MMLU:** Cultural bias detection and mitigation in evaluation frameworks
- **INCLUDE:** Regional knowledge assessment with authentic multilingual content
- **Combined Impact:** Comprehensive evaluation methodology covering both cultural sensitivity and regional authenticity

**Shared Methodological Excellence:**
- **Community-Driven Data Collection:** Native speaker involvement ensuring authenticity
- **Professional Quality Standards:** Rigorous annotation and verification processes
- **Cultural Awareness Integration:** Recognition of language-culture relationships
- **Cohere For AI Leadership:** Direct institutional alignment and mission synergy

---

## 2. Methodological Innovation & Scale

### 2.1 Unprecedented Data Collection Framework
**Massive Scale Achievement:**
- **197,243 QA Pairs:** Largest multilingual exam dataset to date
- **44 Languages Covered:** 15 scripts across 52 countries
- **1,926 Examination Sources:** Academic, professional, and regional license exams
- **60.2% Novel Content:** Newly collected regional sources not previously published

**Three-Tier Exam Classification:**
1. **Academic Exams:** Multi-level education (middle school → university) including national entrance exams
2. **Professional Certifications:** Industry-specific regulatory body examinations (medical, legal practice licensing)
3. **Regional Licenses:** Local authority qualifications (driving, marine licenses)

### 2.2 Regional Knowledge Taxonomy
**Four-Dimensional Classification System:**
```
Knowledge Categories:
1. Region-Agnostic (34.4%): Universal knowledge independent of location
2. Explicitly Regional (18.8%): Legal, regulatory, procedural knowledge
3. Cultural (16.4%): Historical, social, cultural context knowledge  
4. Implicitly Regional (30.4%): Business practices and contextual variations
```

**Quality Assurance Infrastructure:**
- **Native Speaker Verification:** Co-author community providing local expertise
- **Multi-Format Processing:** PDF, JavaScript HTML form extraction pipelines
- **Manual Correction Protocols:** Human verification for extraction accuracy
- **Metadata Enrichment:** Academic level, topic classification, country origin annotation

---

## 3. Experimental Design & Evaluation Framework

### 3.1 Comprehensive Model Assessment
**Evaluation Scale:**
- **15 State-of-the-Art Models:** GPT-4o, Llama-3.1 (8B/70B), Aya-Expanse (8B/32B), Qwen2.5 (7B/14B), Mistral-7B, Gemma-7B variants
- **Multiple Prompting Strategies:** 5-shot, zero-shot CoT, in-language vs. English prompts, regional context prefixes
- **INCLUDE-BASE:** 22,635 QA pairs (12% of full dataset) for comprehensive evaluation
- **INCLUDE-LITE:** 10,770 samples (6% of full dataset) for resource-constrained assessment

### 3.2 Language Exposure Analysis
**Three-Tier Language Categorization:**
1. **Trained on Language:** Languages explicitly included in model pretraining
2. **Trained on Script:** Languages sharing scripts with pretraining languages
3. **Neither:** Completely unseen languages and scripts

**Performance Pattern Discovery:**
- **Script-Based Transfer:** Shared scripts enable cross-lingual knowledge transfer
- **Language Family Effects:** Topologically similar languages benefit from cross-lingual transfer
- **Unique Script Challenges:** Models often perform worse than random on completely unseen scripts

---

## 4. Key Research Findings

### 4.1 Model Performance Hierarchies
**Top-Tier Performance:**
- **GPT-4o:** 77.1% accuracy across all domains and languages
- **Chain-of-Thought Benefits:** Significant improvements in Professional and STEM exams
- **Humanities/Licenses:** Minimal CoT improvements, suggesting reasoning vs. knowledge requirements

**Scale-Performance Correlation:**
- **Aya-Expanse:** 32B model outperforms 8B by ~12% average improvement
- **Qwen2.5:** 14B model shows ~7% improvement over 7B counterpart
- **Training Data Consistency:** Performance gains attributed to model size rather than data differences

### 4.2 Regional Knowledge Performance Patterns
**Domain-Specific Challenges:**
- **Professional Certifications:** Particular difficulty for GPT-4o (average 68.6% accuracy)
- **Persian Certifications:** Notable weakness (43.2% vs. 66%+ on Geography/Sociology)
- **Greek Medical Licenses:** Performance gap (54.1% vs. 71.3% general accuracy)

**Historical Knowledge Analysis:**
- **Regional vs. Global History:** Consistent better performance on general history compared to region-specific historical knowledge
- **Cultural Knowledge Deficits:** Model limitations in culturally-specific historical contexts
- **Universal Pattern:** Observed across all languages except Telugu

### 4.3 Multilingual Evaluation Challenges
**Format Consistency Issues:**
- **Language-Dependent Output Patterns:** Models generate different response formats across languages
- **Generation Length Sensitivity:** 3.1% average improvement when increasing output window from 50 to 512 tokens
- **Extreme Variability:** Some languages show +17.2% improvement (Uzbek), +13.1% (Armenian), +12.9% (Malayalam)

**Instruction Language Effects:**
- **English Prompt Benefits:** Modest ~1.5% improvement across models
- **Format Error Reduction:** Significant changes in response consistency without improving regional knowledge understanding
- **Evaluation Standardization Challenges:** Need for language-aware evaluation protocols

---

## 5. Technical Implementation Excellence

### 5.1 Data Quality Infrastructure
**Extraction Pipeline Sophistication:**
- **Multi-Format Processing:** Automated extraction from PDFs, JavaScript forms, various document types
- **Human-in-the-Loop Validation:** Native speaker verification and manual correction
- **Context Preservation:** Reading comprehension samples include reference text in question fields
- **Image/Table Filtering:** Quality control removing non-textual dependencies

**Benchmark Curation Strategy:**
- **INCLUDE-BASE Design:** 500 regional knowledge + 50 STEM samples per language maximum
- **INCLUDE-LITE Optimization:** 250 samples per language, region-specific domain focus
- **Four-Option Standardization:** Consistency with MMLU evaluation protocols

### 5.2 Evaluation Infrastructure
**Comprehensive Assessment Framework:**
- **Multiple Prompting Configurations:** In-language/English instructions, regional context prefixes
- **Hardware Optimization:** Single A100 GPU evaluation (~4 hours for INCLUDE-BASE)
- **Deterministic Output:** Temperature 0 for reproducible results
- **Context Window Scaling:** 40 tokens (smaller models) to 1024 tokens (CoT reasoning)

**Data Contamination Mitigation:**
- **MinK%++ Analysis:** Training data detection using WikiMIA benchmark methods
- **Contamination Rates:** Aya-8B (2%), XGLM-7B (17%), Qwen-2.5-7B (13%), LLaMA-3.1-8B (29%)
- **Incremental Release Strategy:** Held-back dataset for future contamination analysis
- **PDF/Textbook Sources:** Less likely to appear in web-based training data

---

## 6. Regional Knowledge Insights

### 6.1 Language Resource Impact
**Resource-Performance Correlation:**
```
Language Categories:
- High-Resource (18 languages): Better overall performance, stable across domains
- Mid-Resource (11 languages): Moderate performance with some transfer benefits  
- Low-Resource (13 languages): Significant challenges, often below random performance
```

**Script Transfer Validation:**
- **Aya-Expanse-32B:** 44.1% accuracy on script-shared languages
- **Qwen2.5-7B:** 51.7% accuracy on script-aligned languages  
- **Transfer Limitations:** Performance drops dramatically for unique scripts

### 6.2 Academic Domain Performance
**Subject-Specific Patterns:**
- **STEM Challenges:** Mathematics and Chemistry showing lowest average accuracies
- **Professional Domain Difficulty:** Medical/legal certifications requiring specialized regional knowledge
- **Humanities Variation:** Performance depends heavily on cultural vs. universal content

**Regional Knowledge Dependencies:**
- **Explicitly Regional:** Legal, regulatory knowledge showing significant performance gaps
- **Cultural Content:** Historical, social context requiring local understanding
- **Implicitly Regional:** Business practices varying by regional implementation

---

## 7. Implications for Responsible AI Development

### 7.1 Multilingual Evaluation Reform
**Critical Recommendations:**
1. **Abandon Translation-Based Evaluation:** Move toward region-authentic assessment frameworks
2. **Local Content Prioritization:** Develop evaluation using native sources rather than translations
3. **Regional Knowledge Integration:** Assess models on knowledge relevant to deployment environments
4. **Community Engagement:** Involve native speakers in evaluation development and validation

### 7.2 Digital Equity Advancement
**Underserved Community Impact:**
- **Authentic Assessment:** Evaluation in actual cultural and linguistic contexts
- **Regional Relevance:** Questions reflecting real-world knowledge requirements
- **Professional Application:** Assessment of domain-specific capabilities needed for practical deployment
- **Cultural Preservation:** Recognition of linguistic diversity in evaluation frameworks

### 7.3 Model Development Guidance
**Training Data Implications:**
- **Regional Knowledge Gaps:** Models lacking knowledge for specific deployment regions
- **Cultural Bias Recognition:** Performance variations reflecting training data cultural skews
- **Professional Domain Needs:** Specialized knowledge requirements for real-world applications
- **Language Resource Allocation:** Investment priorities for underrepresented languages

---

## 8. Strategic Position for Cohere Scholars Program

### 8.1 Perfect Research Portfolio Synergy
**Dual Evaluation Excellence:**
- **Global-MMLU:** Cultural bias detection and mitigation methodology
- **INCLUDE:** Regional knowledge assessment with authentic multilingual content
- **Combined Narrative:** "Comprehensive evaluation expertise spanning cultural sensitivity + regional authenticity"

**Cohere For AI Institutional Alignment:**
- **Direct Collaboration:** Multiple Cohere For AI affiliations across both papers
- **Mission Synergy:** Responsible global AI development through equitable evaluation
- **Community Engagement:** Participatory research approaches prioritizing underserved communities
- **Technical Excellence:** Professional-grade methodology and implementation standards

### 8.2 Research Impact Demonstration
**Methodological Innovation:**
- **Largest Scale Achievement:** Most comprehensive multilingual regional knowledge dataset
- **Quality-First Approach:** Native speaker verification and professional annotation standards
- **Cultural Authenticity:** Evaluation reflecting actual deployment environments
- **Open Science Commitment:** Community release with incremental contamination mitigation

**Practical Application:**
- **Industry Standard Potential:** INCLUDE positioned as authentic multilingual evaluation benchmark
- **Developer Guidance:** Clear insights for improving multilingual model regional capabilities
- **Policy Implications:** Evidence for investment priorities in underrepresented language resources
- **Community Impact:** Tools enabling equitable AI development across diverse regions

---

## 9. Technical Excellence Validation

### 9.1 Experimental Rigor
**Comprehensive Model Coverage:**
- **Scale Diversity:** 7B to 70B+ parameter models across multiple architectures
- **Multilingual Specialists:** Aya-Expanse family, language-specific optimizations
- **Prompting Strategy Exploration:** Multiple instruction languages and context configurations
- **Evaluation Framework Validation:** Harness-Eval consistency confirmation

**Statistical Validation:**
- **Inter-Rater Reliability:** Multiple native speaker verification for data quality
- **Performance Correlation Analysis:** R² scores validating benchmark relationships
- **Error Analysis:** Manual investigation of failure modes across 150 examples
- **Contamination Detection:** MinK%++ methodology for training data leakage assessment

### 9.2 Reproducibility Standards
**Implementation Transparency:**
- **Hardware Specifications:** Single A100 GPU requirements with timing estimates
- **Hyperparameter Documentation:** Temperature, context windows, decoding configurations
- **Evaluation Protocol:** Standardized assessment procedures with harness framework
- **Data Release Strategy:** Incremental publication with contamination prevention

**Community Accessibility:**
- **Multiple Subset Releases:** INCLUDE-BASE and INCLUDE-LITE for different resource levels
- **Documentation Standards:** Comprehensive metadata and annotation procedures
- **Evaluation Infrastructure:** Ready-to-use assessment frameworks
- **Future-Proofing:** Held-out datasets for longitudinal contamination analysis

---

## 10. Conclusion: Regional Knowledge Evaluation Revolution

This research establishes a new paradigm for multilingual AI evaluation, moving beyond naive translation approaches to authentic regional knowledge assessment. The creation of INCLUDE represents the largest and most comprehensive effort to evaluate multilingual models in their intended deployment contexts, providing critical insights for responsible AI development.

**Key Achievements:**
1. **Authentic Multilingual Assessment:** 197,243 QA pairs from native regional sources across 44 languages
2. **Regional Knowledge Taxonomy:** Four-dimensional classification enabling systematic analysis of cultural/regional dependencies
3. **Comprehensive Model Analysis:** 15 state-of-the-art models across multiple evaluation configurations
4. **Community-Driven Quality:** Native speaker verification ensuring cultural authenticity and linguistic accuracy

**Strategic Impact:**
- **Evaluation Methodology:** Fundamental shift from translation-based to authenticity-based assessment
- **Digital Equity:** Tools enabling equitable AI development for underserved linguistic communities
- **Research Foundation:** Baseline for future multilingual regional knowledge evaluation
- **Industry Standards:** Potential benchmark adoption for responsible multilingual AI development

**Research Excellence Indicators:**
- **Scale Achievement:** Largest multilingual regional knowledge dataset ever created
- **Quality Standards:** Professional native speaker verification and annotation
- **Methodological Innovation:** Novel regional knowledge taxonomy and evaluation framework
- **Community Impact:** Direct utility for responsible AI development across diverse deployment contexts

This work exemplifies the intersection of technical rigor, cultural authenticity, and global equity that defines responsible AI research, perfectly complementing our Global-MMLU analysis to create a comprehensive evaluation methodology expertise portfolio. Together, these papers demonstrate the cultural sensitivity, technical excellence, and methodological innovation essential for developing AI systems that serve all of humanity equitably.

**Perfect Narrative for Cohere Scholars Program:**
The combination of Global-MMLU (cultural bias detection) + INCLUDE (regional knowledge authenticity) creates an ideal demonstration of comprehensive evaluation methodology expertise aligned with Cohere's mission of responsible global AI development.