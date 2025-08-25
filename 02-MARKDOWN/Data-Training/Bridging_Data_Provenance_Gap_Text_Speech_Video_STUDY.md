# Bridging the Data Provenance Gap Across Text, Speech, and Video

**Research Study Analysis for Cohere Scholars Program 2026**  
**Paper Authors**: Shayne Longpre, The Data Provenance Initiative (65+ researchers)  
**Institution**: The Data Provenance Initiative, MIT, Mozilla Data Futures Lab  
**Category**: Data-Training  

---

## Abstract Summary

This groundbreaking study presents the largest and most comprehensive multimodal audit of AI training data to date, examining nearly 4,000 datasets across text, speech, and video modalities from 1990-2024. The research covers 608 languages, 798 sources, 659 organizations across 67 countries, analyzing 2.1T tokens and 1.9M hours of content. This ecosystem-level analysis reveals critical trends in data sourcing, licensing restrictions, and representation that directly impact responsible AI development and deployment strategies.

## Key Research Questions

1. **Data Sourcing Evolution**: How have data sources shifted across modalities over time, and what are the implications for model quality and risk?

2. **Licensing Inconsistencies**: What gaps exist between dataset licenses and their source restrictions, and how do these affect commercial AI development?

3. **Representation Dynamics**: Has geographical and linguistic representation in AI training data improved over the past decade despite increased awareness?

4. **Multimodal Ecosystem**: How do sourcing patterns, restrictions, and representation vary across text, speech, and video modalities?

## Methodology Framework

### Comprehensive Audit Scope
- **Text**: 3,717 datasets from 108 collections (post-training focus)
- **Speech**: 95 datasets covering ASR tasks across multilingual contexts
- **Video**: 104 datasets spanning classification, captioning, and generation tasks
- **Time Period**: 1990-2024 longitudinal analysis
- **Geographic Coverage**: 67 countries, 659 organizations
- **Linguistic Coverage**: 608 languages across 37 language families

### Annotation Taxonomy
- **License Categories**: Commercial, Non-commercial/Academic, Unspecified
- **Source Terms**: Unrestricted, Unspecified, Source Closed, Model Closed
- **Representation Metrics**: Gini coefficients for inequality measurement
- **Organization Types**: Academic, Research Groups, Industry Labs, Corporations, Startups

## Major Findings

### 1. Dominance of Web-Crawled and Synthetic Data Sources

**Key Discovery**: Overwhelming shift toward web-crawled, social media, and synthetically generated content across all modalities.

**Evidence**:
- **YouTube Dominance**: 71% of video data and 69% of speech data sourced from YouTube
- **Synthetic Growth**: Synthetic text data grew from <0.1% to 10% of web encyclopedia proportion (2020-2024)
- **Web Supremacy**: Web sources provide majority of tokens across text datasets
- **Traditional Source Decline**: Movies, audiobooks, manually collected content eclipsed by web sources

**Critical Implications**: Scale and convenience drive source selection, but introduces privacy, copyright, bias, and factuality risks inherent in user-generated content.

### 2. Massive License-Source Restriction Misalignment

**Key Discovery**: Fundamental inconsistency between dataset licenses and their source restrictions creates legal uncertainty.

**Evidence**:
- **Text**: 99.8% of content carries non-commercial source restrictions, but only 21% of content has restrictive dataset licenses
- **Inconsistency Rates**: 79% of text tokens, 55% of speech hours, 65% of video hours have license-source misalignment
- **Documentation Gaps**: 19%, 14%, and 36% of text, speech, and video datasets lack clear licensing documentation
- **Commercial Viability**: <0.1% of text, 5.4% of speech, 0.6% of video content available for unrestricted commercial use

**Strategic Implications**: Developers face significant legal uncertainty and may unknowingly violate source terms despite permissive dataset licenses.

### 3. Persistent Western-Centric Representation Despite Growth

**Key Discovery**: While absolute diversity increases, relative representation remains concentrated in Western organizations and languages.

**Evidence**:
- **Geographic Concentration**: Gini coefficients remain stable (Text: 0.92, Speech: 0.86, Video: 0.74) indicating high inequality
- **Continental Dominance**: North America + Europe comprise 93% of text tokens, 61% of speech hours, 60% of video hours
- **Global South Exclusion**: Africa and South America organizations account for <0.2% of all content across modalities
- **Language Inequality**: Only text language families show improvement in Gini coefficients since 2013

**Representation Reality**: Despite 600+ languages and 60+ countries represented in 2024, proportional representation shows no significant improvement over the past decade.

### 4. Modality-Specific Ecosystem Characteristics

**Key Discovery**: Each modality exhibits distinct sourcing patterns, organizational structures, and risk profiles.

**Evidence**:
- **Creator Distribution**: Academia dominates video (71%) and speech (47%) but represents only 16% of text datasets
- **Industry Engagement**: Text datasets show most diverse organizational participation including startups and corporations
- **Source Preferences**: Speech and video heavily dependent on YouTube; text more distributed across web sources
- **Size Distributions**: Text shows thickest right tail for large datasets; video datasets typically smallest

**Ecosystem Implications**: Different modalities require distinct approaches to sourcing, licensing, and risk management strategies.

## Technical Innovation

### 1. Unprecedented Scale and Scope
- First comprehensive multimodal audit spanning three decades
- Manual annotation by domain experts ensuring accuracy
- Full provenance tracing through dataset derivation chains
- Ecosystem-level analysis enabling trend identification

### 2. Legal Framework Development
- Comprehensive license taxonomy distinguishing dataset licenses from source terms
- Systematic documentation of restriction inconsistencies
- Commercial viability assessment across modalities
- Risk assessment framework for practitioners

### 3. Representation Measurement
- Gini coefficient application for inequality quantification
- Longitudinal trend analysis over 11-year period
- Geographic and linguistic diversity tracking
- Creator organization categorization and analysis

## Strategic Research Implications

### For Cohere's Responsible AI Mission

1. **Data Sourcing Strategy**: Understanding source concentration and risks enables informed decisions about training data composition and quality

2. **Legal Risk Management**: Systematic assessment of license-source inconsistencies supports compliance frameworks and risk mitigation

3. **Global Representation**: Recognition of persistent Western-centricity informs targeted efforts to improve geographic and linguistic diversity

4. **Quality vs. Scale Trade-offs**: Empirical evidence of web source dominance enables strategic decisions about curation versus scale

### For AI Ecosystem Development

1. **Transparency Infrastructure**: Demonstrates need for systematic data documentation and provenance tracking across the industry

2. **Licensing Harmonization**: Reveals urgent need for consistent licensing practices and clear commercial use permissions

3. **Representation Accountability**: Provides empirical baseline for measuring progress toward more inclusive AI training data

4. **Risk Assessment**: Enables evidence-based evaluation of privacy, copyright, and bias risks associated with different data sources

## Connection to Cohere's Research Leadership

**Institutional Significance**: 
- **Collaborative Research**: Represents largest collective research effort in data transparency with 65+ contributors
- **Mozilla Partnership**: Supported by Mozilla Data Futures Lab demonstrating commitment to responsible AI infrastructure
- **Open Science**: Public release of entire audit enables community-wide improvement in data practices

**Strategic Alignment**: Direct relevance to Cohere's responsible AI development and global deployment goals, providing empirical foundation for data strategy decisions.

## Research Excellence Indicators

1. **Scale Achievement**: Largest multimodal data audit ever conducted with unprecedented breadth and depth
2. **Methodological Rigor**: Manual expert annotation ensuring accuracy and systematic provenance tracing
3. **Longitudinal Analysis**: 34-year historical perspective enabling trend identification and progress measurement
4. **Practical Impact**: Immediate utility for practitioners through public release of audit tools and data
5. **Policy Relevance**: Empirical foundation for data governance discussions and regulatory considerations

## Critical Implications for AI Development

### Immediate Challenges
1. **Legal Uncertainty**: Widespread license-source misalignment creates compliance risks for commercial AI development
2. **Quality Concerns**: Heavy reliance on user-generated content introduces bias, factuality, and privacy challenges
3. **Access Inequality**: Platform restrictions on crawling may limit academic and open-source development
4. **Documentation Deficit**: Inconsistent metadata practices hamper informed decision-making

### Strategic Opportunities
1. **Curation Investment**: Recognition of web source risks supports investment in higher-quality curated datasets
2. **Representation Initiatives**: Empirical baseline enables targeted efforts to improve global and linguistic diversity
3. **Transparency Standards**: Industry-wide adoption of comprehensive data documentation practices
4. **Legal Clarity**: Development of clearer licensing frameworks for AI training data

## Future Research Directions

1. **Dynamic Monitoring**: Continuous tracking of ecosystem evolution and representation progress
2. **Risk Quantification**: Systematic measurement of privacy, copyright, and bias risks across data sources
3. **Quality Assessment**: Development of metrics for training data quality beyond scale considerations
4. **Global Participation**: Investigation of barriers and incentives for increased Global South participation

---

**Analysis Date**: January 2025  
**Strategic Context**: Data-Training Category Development  
**Portfolio Position**: Foundational data infrastructure expertise supporting responsible AI development and global deployment strategies