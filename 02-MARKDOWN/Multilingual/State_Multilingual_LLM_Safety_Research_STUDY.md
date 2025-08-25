# The State of Multilingual LLM Safety Research: From Measuring the Language Gap to Mitigating It

**Authors:** Zheng-Xin Yong¹, Beyza Ermis², Marzieh Fadaee², Stephen H. Bach¹, Julia Kreutzer²

**Affiliations:** ¹Brown University, ²Cohere Labs  
**Contact:** Zheng-Xin Yong (contact.yong@brown.edu), Julia Kreutzer (juliakreutzer@cohere.com)

## Abstract

This paper presents a comprehensive analysis of the linguistic diversity of LLM safety research, highlighting the English-centric nature of the field. Through a **systematic review of nearly 300 publications from 2020–2024** across major NLP conferences and workshops at *ACL, we identify a **significant and growing language gap** in LLM safety research, with even high-resource non-English languages receiving minimal attention.

**Key Findings:**
- **English-centric dominance:** Even high-resource languages like Chinese receive 10x less research than English
- **Growing gap:** The language disparity has **widened significantly over time** (from 5 in 2020 to 83 in 2024)
- **"Herd mentality":** Non-English languages are rarely studied individually but as part of large multilingual evaluations
- **Documentation gaps:** 50.6% of English-only research fails to mention language limitations

**Critical Safety Implications:**
- Several commercial LLMs demonstrate **significantly weaker safety performance** in non-English languages
- Content filtered in English contexts **passes through safety guardrails** in other languages
- **Cultural and linguistic variations** in harmful content create blind spots in current safety frameworks

To motivate future research into multilingual safety, we provide concrete recommendations and pose **three future directions:** safety evaluation, training data generation, and crosslingual safety generalization.

## 1. Introduction: The Global Safety Imperative

The rapid advancement of large language models (LLMs) has transformed AI capabilities across healthcare, education, and media content generation. As these systems deploy globally across diverse linguistic communities, ensuring their **safe and secure operation across linguistic and cultural contexts** has emerged as a critical research imperative.

### The Multilingual Safety Challenge

While significant progress has been made in developing safety mechanisms for high-resource languages, particularly English, the **multilingual dimensions of LLM safety remain considerably underexplored**. This creates potentially dangerous blind spots in safety frameworks and raises fundamental questions about the **equitable distribution of AI benefits and risks**.

**Cultural Complexity Beyond Translation:**
Multilingual LLM safety encompasses challenges that extend well beyond simple translation of existing safety techniques. Languages differ not only in vocabulary and grammar but also in:
- **Cultural connotations** and social norms
- **Metaphorical expressions** and cultural references  
- **Taboos and sensitive topics** varying by cultural context
- **Context-dependent harmfulness** (content harmless in one culture may be deeply offensive in another)

**Real-World Examples:**
- **"Banana" in South-East Asia:** Refers to "yellow on the outside, white on the inside" - used to disparage people of Asian descent perceived as adopting Western cultural values
- **Chinese word "屌":** Literally "dick" but can be both offensive (swear word) and non-offensive (praise for remarkable talent)

### Current State of Vulnerability

Several commercial LLMs have demonstrated **significantly weaker safety performance** when prompted in non-English languages, producing harmful content that would be filtered in English contexts. This creates **uneven safety landscapes** with potentially severe consequences for marginalized linguistic communities.

**Commercial LLM Safety Gaps:**
- **Chatbot Arena Analysis:** 20 of 24 top-ranking LLMs have multilingual support
- **Safety Training Reality:** Only 5 reported multilingual safety alignment training
- **Deployment vs. Safety Gap:** Wide multilingual capabilities vs. limited safety alignment

## 2. Systematic Survey Methodology

### 2.1 Research Design

**Comprehensive Coverage:**
- **Venue Focus:** All *ACL venues (conferences and workshops) - most linguistically diverse NLP venues
- **Time Span:** 2020-2024 (5 years of publications)
- **Scale:** Nearly 300 LLM safety publications analyzed
- **Keyword Filtering:** "safe" and "safety" in abstracts for representative coverage

**Safety Taxonomy:**
1. **Jailbreaking attacks:** Adversarial prompts bypassing safety guardrails
2. **Toxicity and bias:** Harmful content and stereotypical bias in outputs
3. **Factuality and hallucination:** Nonsensical, unfaithful, factually incorrect content
4. **AI privacy:** Memorization, private data leakage, unlearning
5. **Policy:** Governance frameworks, regulatory approaches, ethical guidelines
6. **LLM alignment:** RLHF algorithms spanning multiple safety subtopics
7. **Not related to safety:** Non-safety work filtered out

### 2.2 Annotation Framework

**Language Documentation Analysis:**
- **Languages Studied:** Manual annotation of all languages addressed in each work
- **Documentation Practice:** Whether papers explicitly mention languages studied ("Bender's Rule")
- **Categories:** Monolingual English, monolingual non-English, multilingual (2+ languages)

**Quality Assurance:**
- **Inter-annotator Agreement:** 0.80-0.96 across categories (high consistency)
- **Multiple Validation Rounds:** 4×20 pairwise agreement studies
- **Dataset Release:** Annotations publicly available for research community

## 3. The Language Gap: Critical Findings

### 3.1 English-Centric Dominance

**Overwhelming English Dominance:**
- **English frequency:** Nearly 10x higher than Chinese (second most studied language)
- **Gap Trajectory:** Widening significantly over time (5 papers difference in 2020 → 83 papers in 2024)
- **Proportional Imbalance:** English-only publications consistently outnumber multilingual work
- **Absolute Growth:** While both categories grew, increase disproportionately concentrated in English-only research

**Language Hierarchy:**
1. **English (eng):** Overwhelming dominance, primarily studied in isolation
2. **Chinese (zho):** Second highest but 10x less representation
3. **Arabic (ara), Spanish (spa):** Moderate representation, mainly in multilingual studies
4. **Under-resourced languages (Swahili, Telugu):** Minimal representation in broad multilingual evaluations
5. **Extreme cases (Afrikaans):** Single paper coverage across ~30 languages

### 3.2 "Herd Mentality" in Language Research

**Non-English Languages Studied in Groups:**
Languages with moderate representation (Chinese, Arabic, Spanish) appear **primarily in multilingual studies** rather than focused, language-specific safety analyses. This "herd mentality" severely limits:
- **Language-specific safety analysis**
- **Cultural nuance understanding**
- **Meaningful insights** for individual linguistic communities

**Depth vs. Breadth Trade-off:**
- **Breadth prioritized:** Large multilingual evaluations preferred
- **Depth sacrificed:** Focused monolingual analyses rare
- **Research Bias:** Reviewer preference for multilingual over monolingual non-English papers
- **Community Impact:** Underrepresented languages lack specialized safety research

### 3.3 Categorical Analysis Across Safety Domains

**Universal English-Centricity:**
English-only publications substantially outnumber multilingual work across **every safety category**:

1. **LLM Alignment:** Most pronounced disparity (critical for RLHF and preference learning)
2. **Jailbreaking Attacks:** Severe underrepresentation of multilingual research
3. **Toxicity and Bias:** Limited cultural variation research despite high relevance
4. **Privacy and Policy:** Near absence of multilingual work (cultural/legal variations overlooked)
5. **Factuality and Hallucination:** Modest multilingual representation
6. **AI Privacy:** Minimal cross-linguistic research

**Critical Implications:**
- **Safety techniques developed primarily for English** may not transfer effectively
- **Cultural and legal variations** in safety requirements remain unexplored
- **Policy frameworks** conceptualized through English-language lens

### 3.4 Publication Venue Disparities

**Structural Barriers:**
- **Conference Dominance:** English-only research primarily published in top-tier conferences
- **Workshop Accessibility:** Monolingual non-English safety papers **46% more likely** to appear in workshops
- **Barrier Analysis:** Non-English safety research faces higher barriers to prestigious conference acceptance
- **Community Role:** Workshops serve as more accessible venues for diverse language research

**Specialized Workshop Impact:**
- **GeBNLP (Gender Bias in NLP):** Platform for diverse language bias research
- **Safety4ConvAI:** Venue for multilingual conversational AI safety
- **Community Building:** Workshops facilitate dissemination of underrepresented research

### 3.5 Documentation Practice Disparities

**Critical Finding - Language Documentation Gaps:**
- **English-only papers:** 50.6% fail to explicitly mention "English" as study language
- **Non-English monolingual:** 100% compliance (explicitly document languages)
- **Multilingual papers:** 100% compliance (explicitly document languages)

**Systematic Reporting Bias:**
- **English assumption of universality:** Implicit assumption that English findings generalize
- **Transparency gap:** English-centered research lacks methodological transparency
- **Documentation standards:** Non-English research demonstrates superior reporting practices

**Importance of Language Documentation ("Bender's Rule"):**
1. **Safety non-generalization:** Safety alignment doesn't necessarily transfer across languages
2. **Progress measurement:** Clear language limitations enable accurate progress tracking
3. **Equity advancement:** Explicit acknowledgment encourages broader language coverage

## 4. Real-World Safety Vulnerabilities

### 4.1 Commercial LLM Performance Gaps

**Empirical Evidence from Wang et al. [2024]:**

| Model | English | Chinese | French | Russian | German | Arabic | Hindi | Spanish | Japanese | Bengali | Average | Worst Case |
|-------|---------|---------|--------|---------|--------|--------|-------|---------|----------|---------|---------|------------|
| **ChatGPT** | 99.0 | 91.9 | 86.3 | 87.5 | 85.3 | 90.8 | 81.7 | 91.5 | 79.0 | 62.6 | 85.56 | **62.6** |
| **PaLM-2** | 89.7 | 78.4 | 84.6 | 85.9 | 83.6 | 82.6 | 83.0 | 85.7 | 70.1 | 78.1 | 82.17 | **70.1** |
| **Llama-2** | 85.4 | 73.5 | 83.2 | 82.3 | 82.0 | - | 63.5 | 79.3 | 71.0 | - | 77.53 | **63.5** |
| **Vicuna** | 94.0 | 89.4 | 90.6 | 83.3 | 88.3 | 43.4 | 36.8 | 88.8 | 60.2 | 18.4 | 69.32 | **18.4!** |

**Critical Insights:**
1. **Average vs. Worst-Case Disparity:** ChatGPT leads on average (85.56) but PaLM-2 has better worst-case performance (70.1 vs. 62.6)
2. **False Security:** Vicuna's high average (69.32) masks catastrophic Bengali performance (18.4) - **unsafe deployment risk**
3. **Language-Specific Vulnerabilities:** Each model shows different language-specific failure patterns

### 4.2 Attack Vector Identification

**Multilingual Jailbreaking Techniques:**
1. **Code-switching attacks:** Alternating between languages within single utterances to bypass guardrails
2. **Script variation exploitation:** Arabic content safe in standard script but jailbroken in Arabizi (English characters)
3. **Cultural context manipulation:** Content acceptable in one culture but harmful in another
4. **Translation quality exploitation:** Lower-quality translations creating safety blind spots

**Real-World Examples:**
- **Arabizi Jailbreaking:** Standard Arabic safely handled, but Arabic written in English characters bypasses safety measures
- **Bengali Vulnerability:** Severe safety degradation in Bengali across multiple models
- **Cultural Nuance Attacks:** Exploiting cultural differences in harm perception

## 5. Future Research Directions

### 5.1 Advanced Safety Evaluation Methodologies

#### Moving Beyond Average Performance Metrics

**Critical Limitation of Current Approaches:**
Traditional evaluation focuses on **average performance across languages**, which is susceptible to outliers and unsuitable for comparing models with different language support. **Average metrics can create false sense of safety.**

**Recommended Evaluation Framework:**
1. **Worst-Case Performance Metrics:** Report minimum harmlessness scores across all languages
2. **Adaptive Thresholding:** Language-specific safety baselines according to cultural contexts
3. **Cultural Context Weighting:** Performance weighted by cultural sensitivity requirements
4. **Robustness Assessment:** Consistency measures across linguistic variations

#### Comprehensive Language Coverage

**Current Limitation:**
Most multilingual red-teaming focuses only on languages used in post-pretraining finetuning, potentially missing **crosslingual transfer vulnerabilities** from pretraining contamination.

**Enhanced Coverage Strategy:**
1. **Pretraining Language Analysis:** Evaluate all languages with potential crosslingual transfer capability
2. **Contamination-Aware Testing:** Account for language contamination effects in safety evaluation
3. **Disclaimer Protocols:** Clear safety limitation statements for unevaluated languages
4. **Community Awareness:** Inform language communities of potential risks

#### Natural Linguistic Pattern Integration

**Beyond Monolingual Evaluation:**
Current safety evaluation treats languages in isolation, failing to capture **real-world multilingual communication patterns**.

**Advanced Evaluation Patterns:**
1. **Code-switching Evaluation:** Systematic testing of language alternation within conversations
2. **Script Variation Testing:** Multiple writing systems for same language (Arabic/Arabizi)
3. **Cultural Register Variation:** Formal vs. informal registers, cultural contexts
4. **Multi-turn Multilingual Interactions:** Complex conversational patterns across languages

### 5.2 Culturally-Contextualized Training Data Generation

#### Constitutional AI for Multilingual Alignment

**Framework Adaptation:**
Extending Constitutional AI principles to **multicultural contexts** requires interdisciplinary collaboration among linguists, cultural anthropologists, and AI researchers.

**Core Components:**
1. **Culturally-Informed Constitutional Principles:**
   - Diverse value systems across societies
   - Ethical frameworks reflecting cultural variations
   - Community-validated harm definitions
   - Context-sensitive safety guidelines

2. **Multilingual Constitutional Generation:**
   - Sufficiently capable multilingual LLMs for principle understanding
   - High-quality content generation in target languages
   - Cultural nuance preservation in generation process
   - Community-specific safety preference modeling

3. **Validation Protocols:**
   - Native speaker evaluation of constitutional principles
   - Cultural expert validation of synthetic data
   - Community feedback integration systems
   - Iterative refinement based on cultural input

#### Machine Translation-Based Approaches

**Enhanced Translation Pipeline:**
Machine translation for safety data creation faces challenges in **culture-specific harm preservation** and **bias introduction**.

**Advanced MT Strategy:**
1. **Culture-Aware Translation:** Preserve cultural harm nuances during translation
2. **Constitutional Refinement:** Iterative improvement detecting translation artifacts
3. **Cross-Cultural Adaptation:** Leverage decades of MT cross-cultural research
4. **Automated Quality Assessment:** Methods for identifying culture-specific safety issues

**Benefits:**
- **Established Research Foundation:** Decades of MT cross-cultural adaptation studies
- **Scalable Implementation:** Automated pipeline for multiple languages
- **Quality Control:** Systematic identification of cultural safety preservation

### 5.3 Understanding Crosslingual Safety Generalization

#### Mechanistic Interpretability for Safety Transfer

**Research Questions:**
- Why does **detoxification transfer effectively** across languages but **refusal training does not**?
- What mechanisms enable or prevent safety alignment knowledge transfer?
- How does **language adaptation** affect safety alignment preservation?

**Mechanistic Analysis Framework:**
1. **Circuit-Level Investigation:** Understand neural pathways for safety behavior across languages
2. **Component Analysis:** Identify specific model components responsible for crosslingual safety
3. **Transfer Mechanism Discovery:** Characterize conditions enabling/preventing safety transfer
4. **Adaptation Impact Assessment:** Safety preservation during language-specific fine-tuning

**Practical Applications:**
- **Novel Training Techniques:** Zero-shot crosslingual safety alignment methods
- **Consistency Optimization:** Maintain safety across language coverage expansion
- **Architecture Improvements:** Design choices supporting robust crosslingual safety

#### Training Data Influence Analysis

**Underexplored Research Direction:**
Using **influence functions** to trace causal relationships between training examples and safety-relevant model behaviors across languages.

**Key Research Questions:**
1. **Resource Disparity Impact:** How do high-resource vs. low-resource language examples affect safety outputs?
2. **Crosslingual Generalization:** Which safety examples contribute most to harmful/aligned outputs across languages?
3. **Language Adaptation Safety:** Identifying problematic documents in continued pretraining corpora

**Methodological Framework:**
1. **Influence Function Application:** Trace training-example-to-output relationships for multilingual safety
2. **Causal Analysis:** Quantify specific training example contributions to safety behavior
3. **Data Curation:** Targeted identification and removal of problematic training data
4. **Cross-linguistic Pattern Discovery:** Universal vs. language-specific safety influences

## 6. Recommendations for Research Community

### 6.1 Conference and Venue Improvements

**Immediate Actions:**
1. **Public Language Metadata:** Make OpenReview language coverage information publicly available
2. **Transparent Tracking:** Enable systematic monitoring of linguistic representation
3. **Meta-Analysis Support:** Facilitate future research on multilingual coverage

**Structural Incentives:**
1. **Multilingual Safety Theme Tracks:** Dedicated conference sections for multilingual safety research
2. **Shared Task Creation:** Community-wide multilingual safety benchmark challenges
3. **Workshop Expansion:** Increased support for specialized multilingual safety workshops
4. **Recognition Programs:** Awards for outstanding multilingual safety contributions

### 6.2 Research Practice Standards

**Documentation Requirements:**
1. **Mandatory Language Declaration:** Explicit statement of all languages studied
2. **Limitation Acknowledgment:** Clear safety limitation statements for non-evaluated languages
3. **Cultural Context Documentation:** Acknowledgment of cultural variations in safety assessment
4. **Community Impact Assessment:** Discussion of implications for understudied language communities

**Evaluation Best Practices:**
1. **Worst-Case Reporting:** Include minimum performance metrics alongside averages
2. **Cultural Sensitivity Integration:** Account for cultural variations in harm assessment
3. **Robustness Measurement:** Consistency evaluation across linguistic variations
4. **Real-World Pattern Testing:** Beyond monolingual evaluation to natural usage patterns

### 6.3 Industry Engagement

**Corporate Responsibility:**
1. **Multilingual Safety Investment:** Proportional safety research for deployed language capabilities
2. **Transparency Requirements:** Public reporting of multilingual safety alignment efforts
3. **Community Collaboration:** Partnership with linguistic communities for safety assessment
4. **Resource Sharing:** Open access to multilingual safety evaluation tools and datasets

## 7. Technical Innovations and Methodological Advances

### 7.1 Survey Methodology Contributions

**Systematic Analysis Framework:**
- **First comprehensive survey** of multilingual LLM safety research landscape
- **Quantitative documentation** of English-centric bias with statistical validation
- **Temporal trend analysis** showing widening language gap over time
- **Cross-category examination** revealing universal patterns across safety domains

**Replicable Methodology:**
- **Transparent annotation protocols** with high inter-annotator agreement (0.80-0.96)
- **Public dataset release** enabling community validation and extension
- **Scalable framework** applicable to future multilingual AI research surveys
- **Bias detection methods** for systematic inequality identification

### 7.2 Safety Evaluation Innovations

**Beyond Average Metrics:**
- **Worst-case performance analysis** revealing hidden vulnerabilities in high-performing models
- **Cultural context weighting** for more realistic safety assessment
- **Robustness measurements** accounting for linguistic variation
- **False security detection** in multilingual deployment scenarios

**Real-World Pattern Integration:**
- **Code-switching evaluation** reflecting natural multilingual communication
- **Script variation testing** for comprehensive language coverage
- **Cultural register analysis** across formal/informal communication styles
- **Multi-turn interaction assessment** for complex conversational safety

### 7.3 Training Data Methodological Advances

**Constitutional AI Enhancement:**
- **Multicultural principle development** with community validation
- **Cross-cultural harm definition** reflecting diverse value systems
- **Scalable constitutional generation** for multilingual alignment
- **Iterative refinement protocols** based on cultural expert feedback

**Translation Quality Innovation:**
- **Culture-aware translation** preserving safety-relevant cultural nuances
- **Automated quality assessment** for cultural safety preservation
- **Cross-cultural adaptation** leveraging established MT research
- **Constitutional refinement** detecting and correcting translation artifacts

## 8. Global Impact and Equity Implications

### 8.1 Digital Equity Considerations

**Unequal Safety Protection:**
The documented language gap creates **systematic inequalities** in AI safety protection, with severe implications for global digital equity:

1. **Resource-Based Discrimination:** High-resource languages receive disproportionate safety research and protection
2. **Cultural Marginalization:** Non-Western cultural contexts underrepresented in safety frameworks
3. **Community Vulnerability:** Marginalized linguistic communities face higher AI-related harm risks
4. **Access Inequality:** Safe AI benefits concentrated in dominant linguistic groups

**Magnification of Existing Inequalities:**
- **Language Technology Privilege:** Systematic advantages for certain sociolinguistic groups
- **Data Collection Bias:** Safety training data reflecting dominant cultural perspectives
- **Annotation Protocol Bias:** Western-centric harm definitions and safety standards
- **Evaluation Methodology Bias:** English-centric evaluation frameworks

### 8.2 Responsible Deployment Implications

**Current Deployment-Safety Mismatch:**
- **Capability-Safety Gap:** Wide multilingual deployment vs. limited multilingual safety alignment
- **Community Risk:** Vulnerable populations exposed to inadequately tested AI systems
- **Corporate Responsibility:** Insufficient safety investment relative to deployment scope
- **Regulatory Gaps:** Policy frameworks primarily addressing English-language contexts

**Recommendations for Responsible Scaling:**
1. **Proportional Safety Investment:** Safety research resources matching deployment scope
2. **Community Engagement:** Meaningful involvement of affected linguistic communities
3. **Transparent Limitation Disclosure:** Clear communication of safety coverage limitations
4. **Phased Deployment:** Gradual rollout with community feedback integration

## 9. Limitations and Future Work

### 9.1 Current Study Limitations

**Venue Coverage:**
- **Focus on *ACL venues** may miss relevant work at ML conferences (ICLR, NeurIPS, ICML)
- **Peer-review bias** potentially missing rejected multilingual safety work
- **Temporal snapshot** representing specific time period in rapidly evolving field
- **Keyword filtering** may miss relevant work using different terminology

**Annotation Accuracy:**
- **Inter-annotator disagreement** primarily in safety topic categorization
- **Language coverage oversight** possible when not prominently stated
- **Depth variation** in paper analysis due to annotation time constraints
- **Recall limitations** for subtle multilingual safety mentions

### 9.2 Future Research Needs

**Expanded Survey Scope:**
1. **Venue Diversification:** Include ML conferences and industry publications
2. **Temporal Extension:** Continuous monitoring of field evolution
3. **Methodology Refinement:** Enhanced annotation protocols and validation procedures
4. **Community Input:** Stakeholder feedback on findings and recommendations

**Methodology Development:**
1. **Automated Detection:** AI-assisted identification of multilingual safety research
2. **Impact Assessment:** Measuring real-world influence of safety research
3. **Community Surveys:** Direct feedback from affected linguistic communities
4. **Longitudinal Studies:** Long-term tracking of research gap evolution

## 10. Conclusion

This systematic survey of nearly 300 LLM safety publications reveals a **critical and widening language gap** in AI safety research. The findings demonstrate that even high-resource non-English languages receive minimal attention compared to English, with this disparity becoming more pronounced over time.

### Key Contributions

**Empirical Documentation:**
- **First comprehensive quantification** of linguistic bias in LLM safety research
- **Temporal trend analysis** showing widening gap (5 papers in 2020 → 83 papers in 2024)
- **Cross-category evidence** of universal English-centricity across safety domains
- **Documentation practice analysis** revealing systematic reporting disparities

**Methodological Innovations:**
- **Systematic survey framework** with high inter-annotator agreement
- **Worst-case performance analysis** revealing hidden vulnerabilities
- **Cultural context integration** in safety evaluation protocols
- **Real-world pattern incorporation** in multilingual safety assessment

**Community Impact:**
- **Public dataset release** enabling further research and validation
- **Concrete recommendations** for conferences, researchers, and industry
- **Future research directions** with practical implementation pathways
- **Awareness raising** about critical gaps in global AI safety

### Critical Implications for Global AI Safety

**Immediate Risks:**
- **Vulnerable Populations:** Marginalized linguistic communities exposed to inadequately tested AI systems
- **False Security:** Average performance metrics masking catastrophic language-specific failures
- **Cultural Blind Spots:** Safety frameworks missing culture-specific harm patterns
- **Deployment-Safety Mismatch:** Wide multilingual capabilities vs. narrow safety coverage

**Long-Term Consequences:**
- **Digital Divide Amplification:** Unequal AI safety protection exacerbating existing inequalities
- **Cultural Homogenization:** Western-centric safety standards affecting global AI deployment
- **Community Trust Erosion:** Repeated safety failures in underserved languages
- **Regulatory Inadequacy:** Policy frameworks insufficient for multilingual AI governance

### Path Forward

The field can develop more robust, inclusive AI safety practices by:

1. **Implementing recommended evaluation practices** (worst-case metrics, cultural context weighting)
2. **Investing in culturally-contextualized training data** generation
3. **Advancing crosslingual safety generalization** research
4. **Establishing community engagement** protocols for affected linguistic groups
5. **Creating incentive structures** for multilingual safety research
6. **Demanding proportional safety investment** from AI developers

**Urgency of Action:**
As LLMs become increasingly powerful and globally deployed, addressing the multilingual safety gap becomes not just a research priority but a **moral imperative**. The current trajectory risks creating a world where AI safety is a privilege of linguistic dominance rather than a universal right.

By releasing this survey and proposed directions, we aim to catalyze community action toward more equitable, globally-capable AI safety practices that serve diverse linguistic communities with equal effectiveness and cultural sensitivity.

---

## Research Significance for Cohere Scholars Application

This research represents **exactly the type of forward-thinking, globally-conscious AI safety work** that aligns perfectly with Cohere's mission and values:

### 1. AI Safety Leadership
- **Systematic Gap Identification:** First comprehensive documentation of critical safety blind spots affecting global populations
- **Empirical Evidence:** Quantitative analysis revealing up to 83-paper gap between English and multilingual safety research
- **Real-World Impact:** Documentation of commercial LLM vulnerabilities affecting millions of non-English speakers
- **Preventive Framework:** Proactive identification of safety issues before widespread deployment

### 2. Global Equity Focus
- **Marginalized Community Advocacy:** Explicit focus on protecting underserved linguistic communities
- **Digital Rights Perspective:** Framing AI safety as universal right rather than linguistic privilege
- **Cultural Sensitivity:** Recognition of culture-specific harm patterns and safety requirements
- **Community Engagement:** Recommendations for meaningful involvement of affected populations

### 3. Technical Excellence with Social Impact
- **Methodological Rigor:** High inter-annotator agreement (0.80-0.96), systematic evaluation framework
- **Cohere Institution Connection:** Co-authored by Cohere Labs researchers demonstrating direct institutional alignment
- **Community Resource Creation:** Public dataset release enabling further research and validation
- **Practical Solutions:** Concrete recommendations for industry, academia, and policy makers

### 4. Research Leadership and Vision
- **Field-Shaping Impact:** First systematic survey establishing baseline for future multilingual safety research
- **Future Direction Setting:** Three concrete research directions with implementation pathways
- **Cross-Disciplinary Integration:** Bridging linguistics, cultural studies, machine learning, and policy
- **Collaborative Scholarship:** Multi-institutional authorship demonstrating community building capacity

### 5. Cohere Mission Alignment
- **Global AI for Good:** Direct alignment with Cohere's mission of responsible AI development for global populations
- **Responsible Scaling:** Framework for ethical AI deployment across linguistic communities
- **Community-Centered Research:** Emphasis on community engagement and cultural sensitivity
- **Transparent Research Practices:** Open data release and methodological transparency

This work demonstrates the **exact combination of technical depth, global perspective, and ethical consideration** that Cohere values in its scholars - researchers who can advance the state of AI while ensuring its benefits reach all of humanity equitably and safely.