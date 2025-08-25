# NeoBabel: A Multilingual Open Tower for Visual Generation

**Authors:** Mohammad Mahdi Derakhshani², Dheeraj Varghese², Marzieh Fadaee♦¹, and Cees G. M. Snoek♦²

¹Cohere Labs, ²University of Amsterdam

Corresponding authors: m.m.derakhshani@uva.nl, marzieh@cohere.com

## Abstract

Text-to-image generation advancements have been predominantly English-centric, creating barriers for non-English speakers and perpetuating digital inequities. While existing systems rely on translation pipelines, these introduce semantic drift, computational overhead, and cultural misalignment. We introduce NeoBabel, a novel multilingual image generation framework that sets a new Pareto frontier in performance, efficiency and inclusivity, supporting six languages: English, Chinese, Dutch, French, Hindi, and Persian. The model is trained using a combination of large-scale multilingual pretraining and high-resolution instruction tuning. To evaluate its capabilities, we expand two English-only benchmarks to multilingual equivalents: m-GenEval and m-DPG. NeoBabel achieves state-of-the-art multilingual performance while retaining strong English capability, scoring 0.75 on m-GenEval and 0.68 on m-DPG. Notably, it performs on par with leading models on English tasks while outperforming them by +0.11 and +0.09 on multilingual benchmarks, even though these models are built on multilingual base LLMs. This demonstrates the effectiveness of our targeted alignment training for preserving and extending cross-lingual generalization. We further introduce two new metrics to rigorously assess multilingual alignment and robustness to code-mixed prompts. Notably, NeoBabel matches or exceeds English-only models while being 2–4× smaller. We release an open toolkit, including all code, model checkpoints, a curated dataset of 124M multilingual text-image pairs, and standardized multilingual evaluation protocols, to advance inclusive AI research. Our work demonstrates that multilingual capability is not a trade-off but a catalyst for improved robustness, efficiency, and cultural fidelity in generative AI.

**Website:** https://Neo-Babel.github.io  
**Code:** https://github.com/mmderakhshani/NeoBabel  
**Models:** https://hf.co/mderakhshani/NeoBabel  
**Pretraining Data:** https://hf.co/datasets/mderakhshani/NeoBabel-Pretrain  
**Instruction Data:** https://hf.co/datasets/mderakhshani/NeoBabel-Instruct  
**Evaluation Data:** https://hf.co/datasets/mderakhshani/NeoBabel-Eval  

*Released as a preprint on July 9, 2025*

## 1 Introduction

Recent advances in diffusion models and large-scale vision-language pretraining have revolutionized text-to-image generation, enabling the creation of high-quality images from natural language descriptions [Rombach et al., 2022; Peebles & Xie, 2023; Bao et al., 2023; Chen et al., 2024a; Xie et al., 2023; Wu et al., 2023a; Lipman et al., 2022; Xie et al., 2025a; Qin et al., 2025; Zhang et al., 2023; Seawead et al., 2025]. Despite these remarkable capabilities, the field suffers from a critical limitation: an overwhelming reliance on English as the primary—and often exclusive—input language [Ramesh et al., 2022; Xie et al., 2025b; Team, 2024]. This monolingual bias creates substantial barriers for the billions of users who communicate in other languages, fundamentally restricting global access to state-of-the-art generative AI technologies [Bassignana et al., 2025; Peppin et al., 2025].

The consequences of this linguistic limitation extend far beyond mere inconvenience. As text-to-image systems become integral to education, creative industries, art, and journalism, the lack of native multilingual support perpetuates existing digital divides and cultural inequities [Liu et al., 2023; Rege et al., 2025]. Non-English speakers are forced to navigate through translation layers that not only introduce friction but also risk losing the nuanced meanings and cultural contexts that make their creative expressions unique [Kannen et al., 2024; Friedrich et al., 2024]. Building truly multilingual models, like we do in this paper, is therefore not merely a technical challenge but an ethical imperative, one that ensures equitable access to generative AI while preserving linguistic diversity and cultural authenticity in the digital age.

Existing approaches to multilingual image generation typically employ a translation-first strategy, converting non-English prompts to English before processing. While this appears pragmatic, it introduces a cascade of problems that fundamentally compromise the user experience [Kreutzer et al., 2025; Li et al., 2025b; Bafna et al., 2025]. The computational overhead of chaining translation and generation models effectively doubles inference time, creating prohibitive delays for real-time applications, thereby further disadvantaging non-English speakers. Most critically, this approach suffers from semantic drift—the systematic loss of culturally specific meanings and linguistic subtleties [Cohn-Gordon & Goodman, 2019; Vanmassenhove et al., 2019; Beinborn & Choenni, 2020].

For instance consider the Dutch term "gezellig" which encompasses a complex blend of coziness, conviviality, and belonging and has no direct English equivalent. When forced through translation, such rich cultural concepts are inevitably flattened or distorted, resulting in generated images that fail to capture the intended meaning. The fundamental issue lies deeper than mere translation accuracy [Wein & Schneider, 2023; Singh et al., 2024; Salazar et al., 2025].

Current vision-language architectures treat multilingual support as an afterthought, forcing diverse linguistic communities to conform to English-centric models rather than developing systems that natively understand and respect linguistic diversity. This design philosophy not only limits accessibility but also wastes the potential benefits of multilingual training, which could enhance model robustness, cross-cultural understanding, and generalization capabilities across different linguistic and cultural contexts [Ji et al., 2024; Faisal & Anastasopoulos, 2024; Dash et al., 2025; Shimabucoro et al., 2025].

These challenges demand a paradigm shift toward native multilingual understanding in text-to-image generation. The primary obstacle remains the scarcity of high-quality, culturally annotated visual-linguistic datasets for non-English languages. Even with adequate data, significant technical barriers persist: establishing robust cross-lingual concept alignment, modeling typological variations across language families, and preserving culture-specific semantics during generation. Overcoming these limitations is critical for transitioning from mere translation-based approaches to systems with genuine multilingual competence.

This paper introduces NeoBabel, a novel multilingual image generation framework that represents the first scalable solution for direct text-to-image synthesis across six languages. Through meticulous curation of high-quality multilingual vision-language datasets and end-to-end training, NeoBabel establishes direct cross-lingual mappings between textual descriptions and visual outputs across all supported languages. This approach not only removes translation dependencies but also maintains crucial cultural and linguistic specificity in the generated images. Our model demonstrates that multilingual capability isn't a trade-off but rather a catalyst for improved model performance.

Our work addresses three key questions: 1) How can we train a single model to handle multiple languages effectively? 2) Does multilingual training degrade performance in high-resource languages like English? and 3) Can a unified model outperform language-specific or translation-based approaches? To answer these, we introduce a progressive training pipeline that combines large-scale multilingual pretraining with high-resolution instruction tuning. We evaluate NeoBabel on m-GenEval and m-DPG, our multilingual extensions of GenEval [Ghosh et al., 2023] and DPG-Bench [Hu et al., 2024], and introduce two new metrics, Cross-Lingual Consistency (CLC) and Code Switching Similarity (CSS), to quantify multilingual performance.

As shown in Figure 1, NeoBabel matches the performance of state-of-the-art English-only models while being 2–4× smaller. Here, we report English-only results for fair comparison, as prior work evaluates only in English. Furthermore, NeoBabel maintains strong generation quality in all six supported languages. For instance, on the m-GenEval benchmark, it achieves a new state-of-the-art score of 0.75—an improvement of 0.11 over the very recent BLIP3-o 8B model (0.64) [Chen et al., 2025a]. Similarly, on m-DPG, it scores 0.68, outperforming BLIP3-o 8B by 0.09. These results demonstrate that strong multilingual generation is achievable without resorting to large-scale models or sacrificing output quality.

### Key Contributions

1. **A novel multilingual training framework.** We introduce a novel multilingual training framework that establishes new state-of-the-art performance in cross-lingual image generation. Our approach achieves language-agnostic understanding by directly mapping prompts from any supported language to visual concepts without requiring translation, while maintaining performance parity that matches or exceeds English-only models across all languages. This unified architecture delivers significant operational efficiency gains by eliminating the need for separate translation infrastructure, enabling single-model deployment that reduces both computational overhead and system complexity. The unified architecture delivers significant efficiency improvements, processing multilingual prompts 2.8x faster than translation-then-generation pipelines while using 59% less memory which is critical for real-world deployment scenarios. To train the unified model, we introduce a data curation pipeline that prepares multilingual image-text pairs for both pretraining and instruction tuning.

2. **Comprehensive multilingual benchmark and metrics.** We introduce the first standardized framework for evaluating multilingual image generation, addressing critical gaps in existing benchmarks. Our protocol includes: (1) extended versions of GenEval [Ghosh et al., 2023] and DPG-Bench [Hu et al., 2024], referred to as m-GenEval and m-DPG, across six languages, enabling direct comparison between native multilingual and translation-based approaches; and (2) two novel metrics—Cross-Lingual Consistency (CLC) and Code-Switching Similarity (CSS), to quantify semantic alignment and robustness to mixed-language prompts. CLC measures image equivalence across languages using EVA-CLIP [Sun et al., 2023b] and DINOv2 [Oquab et al., 2023] embeddings, while CSS evaluates real-world code-switching scenarios. NeoBabel achieves state-of-the-art multilingual performance while maintaining strong English capabilities. Notably, it matches the English results of leading multilingual models while outperforming them by +0.11 and +0.09 on multilingual benchmarks—despite those models being built on multilingual base LLMs. This positions NeoBabel as a strong foundation for future research in equitable, culturally adaptive generative AI.

3. **Open toolkit for inclusive research.** We release a comprehensive research toolkit comprising NeoBabel model checkpoints trained on six languages (English, Chinese, Dutch, French, Hindi, and Persian), a systematically curated dataset of 124M multilingual text-image pairs with quality-controlled translations, and a complete reproducibility package including training scripts, hyperparameter configurations, and standardized evaluation protocols. Our framework is designed to be easily extensible to additional languages, thanks to a scalable training pipeline, with validation metrics and benchmarking guidelines that support systematic comparison of multilingual generation across research groups.

## 2 NeoBabel Architecture

We first outline the core architectural components of NeoBabel, including its multilingual transformer backbone (Section 2.1), training objectives (Section 2.2), and the multilingual model merging strategy (Section 2.3) designed to enhance generation quality across diverse linguistic settings.

### 2.1 Model Architecture

Our architecture's core components, a multilingual tokenizer and transformer backbone, are specifically optimized for efficient, scalable cross-lingual image generation, supporting seamless processing across diverse languages and image types. Figure 2 provides an overview of the NeoBabel architecture.

#### 2.1.1 Tokenizers

**Text Tokenization.** For textual input, we adopt the tokenizer of the pretrained multilingual large language model Gemma-2 [Gemma Team et al., 2024] without any modifications. This approach maintains compatibility with multilingual inputs while utilizing proven tokenization methods from language modeling.

**Image Tokenization.** For image input, we leverage the MAGVIT-v2 quantizer [Yu et al., 2023] retrained by Show-o [Xie et al., 2025b] on 25 million images. This lookup-free quantizer learns a discrete codebook of size K=8,192 and encodes 256 × 256 resolution images into 16 × 16 grids of discrete tokens. The quantization approach supports efficient downstream training and generation while preserving fine-grained visual details.

#### 2.1.2 Transformer Backbone

As we build upon the pretrained multilingual large language model (LLM) Gemma-2 [Gemma Team et al., 2024], we maintain its overall transformer architecture, while introducing two key modifications: (1) integration of a unified multimodal embedding space, and (2) modality-aware attention patterns for flexible generation. Additionally, we apply qk-norm [Henry et al., 2020] to each attention layer to enhance training stability and convergence.

**Unified Multimodal Embedding and Prompt Design.** To enable seamless multimodal learning, we extend the LLM's embedding table with 8,192 new learnable embeddings for discrete image tokens, allowing the model to process image inputs natively without architectural changes. Both text and image tokens are embedded in a shared space, enabling the model to learn cross-modal compositionality and semantic alignment. We represent all tasks including text-to-image generation as unified autoregressive sequences. Given a tokenized image-text pair, text and image tokens are concatenated into a single sequence. Special tokens such as [T2I], [SOT], [EOT], [SOI], and [EOI] explicitly mark task type and modality boundaries, enabling the model to disambiguate different modalities and tasks through prompting alone. This design simplifies the training pipeline by removing the need for modality-specific components or task-specific heads, allowing for flexible, scalable, and unified multimodal generation.

**Modality-Aware Attention Patterns.** To accommodate the differing structural needs of text and image modalities, we employ a hybrid attention mechanism. Text tokens are modeled with causal attention to preserve autoregressive language modeling capabilities. Image tokens, in contrast, are modeled using full bidirectional attention, allowing rich interactions that are critical for high-fidelity image synthesis. When both modalities are present, attention masks are dynamically configured so that image tokens can fully attend to text tokens and preceding image tokens, enabling coherent, contextually grounded generation.

### 2.2 Training Objective

The model is trained on sequences composed of both textual and visual tokens, where text tokens act as a prefix and visual tokens form the postfix. We do not apply any learning objective to the text tokens; the loss is computed solely over the visual tokens.

Let t = {t₁, t₂, ..., tₙ} denote the text tokens and i = {i₁, i₂, ..., iₘ} denote the image tokens, forming a full input sequence [t; i]. During training, we randomly select a subset J ⊂ {1, ..., M} of image token indices to be masked. The corresponding masked sequence is denoted by i*, where iⱼ is replaced with a special [MASK] token for all j ∈ J. The model is trained to reconstruct the original visual tokens at the masked positions by conditioning on the full input sequence of text tokens and (partially masked) image tokens. The objective is defined as:

L = Σⱼ∈ⱼ log pθ(iⱼ | t, i*)

where pθ(·) is the model's predicted distribution over image codebook entries, parameterized by θ. The loss is only applied to the masked image tokens in J. We follow the masking strategy introduced by Xie et al. [2025b], randomly masking a fixed ratio of visual tokens within each training sample. To further improve generation controllability, we incorporate classifier-free guidance [Ho & Salimans, 2022] by replacing the conditioning text with a null string with some probability during training.

### 2.3 Multilingual Model Merging

To enhance generalization and stability of multilingual image generation models, we adopt model merging techniques that combine multiple checkpoints from the training trajectory. Let {Mᵢ}ᵢ₌₁ᴺ denote a sequence of N model checkpoints and {wᵢ}ᵢ₌₁ᴺ their corresponding non-negative weights. The merged model M̃ is defined as a convex combination:

M̃ = Σᵢ₌₁ᴺ αᵢMᵢ where αᵢ = wᵢ / Σⱼ₌₁ᴺ wⱼ

This formulation allows the merged model to interpolate within the solution space spanned by the selected checkpoints, potentially improving generalization on unseen prompts and enhancing robustness to overfitting. We consider three widely used weighting strategies for this purpose, each reflecting different assumptions about model evolution during training.

## 3 NeoBabel Multilingual Datasets

### 3.1 Data Curation Pipeline

Multilingual multimodal data remains scarce, especially compared to the abundance of English-centric resources. This imbalance poses a significant barrier to training and evaluating models that can understand grounded language across diverse linguistic contexts. To address this gap, we curate and augment several multilingual datasets by translating and recaptioning existing image-caption pairs into six target languages: English, Chinese, Dutch, French, Hindi, and Persian.

At the core of our approach is a multilingual captioning pipeline designed to ensure both semantic richness and linguistic diversity. We begin by generating a detailed English caption for each image using InternVL [Chen et al., 2024c], prompted with a simple instruction: "Describe this image in detail in English." This step guarantees comprehensive coverage of the visual content.

To preserve quality and consistency across languages, we implement a multi-step post-processing and filtering stage based on four strategies:

- **Length filtering**: Remove captions that are too short (e.g., fewer than 5 tokens) or excessively long (e.g., more than 500 tokens).
- **Language validation**: Detect and discard captions containing non-English phrases or corrupted outputs using language identification tools. We use the fastText language identification model trained on 176 languages [Joulin et al., 2016]. We discard any caption not classified as English with a confidence score above 90%.
- **Visual-text mismatch filtering**: Discard captions that do not align with visual content, measured via auxiliary vision-language models (e.g., using VQAScore). Specifically, we leverage MolMo-72B [Deitke et al., 2025] deployed with vLLM [Kwon et al., 2023], formulating the task as a binary structured prediction (yes/no) via vLLM's output interface.
- **Toxicity and NSFW filtering**: Discard samples using the LAION-5B NSFW classifier [Schuhmann et al., 2022] to ensure safe visual content before captioning, assuming high likelihood of appropriateness in the resulting captions.

Once high-quality English captions are obtained, we translate them into five target languages using the NLLB model [Costa-Jussà et al., 2022] for the pretraining datasets, and the Gemini Experimental model (gemini-2.0-flash-lite) for the instruction tuning datasets. This separation ensures high translation coverage at scale during pretraining, while leveraging higher-quality outputs for instruction-tuned data.

### 3.2 NeoBabel Pretraining Data

**m-ImageNet-1K**: The original English class labels are translated into five more languages to obtain a total of six target languages, forming multilingual textual prompts for class-conditional image generation.

**m-SA-1B and m-CC12M**: We incorporate 22 million image-caption pairs in English from SA-1B [Kirillov et al., 2023] and CC12M [Changpinyo et al., 2021]. These datasets provide rich natural image-caption pairs and enhance visual diversity. The texts are enhanced through our recaptioning pipeline.

**m-LAION-Aesthetic**: A subset of the LAION dataset including 12M image-text pairs is enhanced and translated, yielding approximately 72 million image-caption pairs for a total of six languages.

**m-JourneyDB**: This synthetic dataset consists of 4 million high-quality images generated by the Midjourney model [Sun et al., 2023a]. We apply the same recaptioning and translation pipeline to generate 24 million image-caption pairs for our six languages.

Combining all sources, the final pretraining dataset contains approximately **124 million image-text pairs across six languages**, covering diverse domains and visual aesthetics.

### 3.3 NeoBabel Instruction Tuning Data

**m-LAION-Aesthetic and m-JourneyDB**: Our setup continues to use the LAION-Aesthetic and JourneyDB datasets, as extended in the pretraining data.

**m-BLIP3o-Instruct**: An instruction-focused dataset introduced by Chen et al. [2025a], containing multimodal instruction samples, also translated into six languages for multilingual supervision.

All images are resized to 512 × 512. While the images are drawn from established, high-quality sources, most accompanying texts have been significantly enriched or rewritten, resulting in a more valuable and linguistically diverse dataset for instruction tuning and multilingual generation.

## 4 NeoBabel Training Stages: Learning Progression

NeoBabel is trained using a staged learning framework consisting of three progressive pretraining stages (Section 4.1) followed by two instruction tuning stages (Section 4.2).

### 4.1 Progressive Pretraining

Our pretraining includes three stages, progressively scaling from basic visual understanding to advanced multilingual image generation:

**Stage 1 – Pixel Dependency Learning**: The model initially learns foundational visual representations using m-ImageNet-1K. Class-conditional image generation is guided by translated class labels, enabling the model to form robust image token embeddings and capture pixel-level dependencies for high-fidelity output.

**Stage 2 – Scaling Alignment with Large-Scale Multilingual Data**: Using weights from the first stage, the model is fine-tuned on 22 million English-only image-caption pairs (from m-SA-1B and m-CC12M) and 72 million translated samples from m-LAION-Aesthetic. This stage strengthens the model's grounding in natural image-text alignment while developing multilingual capabilities through broad cross-lingual exposure.

**Stage 3 – Refined Multilingual Pretraining**: In the final stage, the model is trained on 96 million multilingual image-text pairs derived from m-LAION-Aesthetic and m-JourneyDB. The training balances high-quality real-world aesthetic data with diverse, synthetic images to improve generalization across languages, domains, and modalities.

### 4.2 Progressive Instruction Tuning

Following pretraining, the model advances to instruction tuning, where the focus shifts from unsupervised representation learning to explicit task-guided adaptation, refining its ability to interpret and execute complex, multilingual instructions through our curated datasets and progressive exposure to prompt-driven generation in two stages:

**Stage 1 – Initial Multilingual Instruction Alignment**: To build robust multilingual instruction-following capabilities at high resolution, the model is first trained with a diverse mixture of the three datasets described above. In this stage, training samples are drawn from m-LAION-Aesthetic, m-JourneyDB, and m-BLIP3o-Instruct using mixing weights α₁, α₂, and α₃, respectively, such that α₁ + α₂ + α₃ = 100.

**Stage 2 – Instruction Refinement**: In the second stage, we adjust the mixing weights to emphasize instruction-rich and synthetic supervision. Specifically, α₂ and α₃ are increased to draw more heavily from m-JourneyDB and m-BLIP3o-Instruct, while α₁ is decreased to reduce reliance on LAION-based content.

Each stage is trained for 500k steps (except the final stage of instruction tuning with 200k) using the AdamW optimizer and cosine learning rate decay. The learning rate is set to 1e−4 during pretraining and adjusted during instruction tuning. We gradually increase prompt sequence length and resolution from 128 to 512 and from 256 × 256 to 512 × 512 respectively.

## 5 Multilingual Evaluation of Image Generation

Existing image generation benchmarks are mostly English-centric, failing to capture cross-lingual performance. To resolve this limitation, we introduce a multilingual evaluation suite that extends established (English-only) benchmarks to cover six diverse languages and introduces new evaluation metrics for assessing cross-lingual visual consistency.

### 5.1 Multilingual Evaluation Suite

We assess the image generation capabilities of NeoBabel using two complementary benchmarks: GenEval [Ghosh et al., 2023] and DPG-Bench [Hu et al., 2024]. GenEval offers a structured evaluation of prompt-to-image alignment across six compositional dimensions: single object, two objects, counting, colors, position, and color attribute. In contrast, DPG-Bench targets general-purpose generation with open-ended, diverse prompts that test broader semantic understanding.

As part of our multilingual evaluation suite, we introduce **m-GenEval and m-DPG**, multilingual extensions of the original benchmarks. All prompts are translated into five additional languages: Chinese, Dutch, French, Hindi, and Persian, using the Gemini Experimental model, followed by human verification and manual corrections to ensure semantic fidelity and linguistic fluency.

### 5.2 Multilingual Evaluation Metrics

To complement the multilingual benchmarks introduced above, we introduce two metrics that assess how well generative models preserve visual and semantic consistency across languages.

**Cross-Linguistic Consistency (CLC)**: To evaluate whether multilingual models generate semantically consistent and faithful outputs across languages, we introduce the CLC score. Multilingual image generation models should produce visually similar outputs when given semantically equivalent prompts, regardless of the input language.

**Code-Switching Similarity (CSS)**: Real-world multilingual communication frequently involves code switching, i.e., interleaving of multiple languages within a single utterance. Therefore, a well-aligned multilingual model should demonstrate robustness not only to monolingual prompts but also to mixed-language inputs, capturing the inherent complexity and variability of natural language.

## 6 Results and Discussions

We evaluate NeoBabel on our multilingual extension of standard benchmarks, including m-GenEval and m-DPG, to assess performance across languages both quantitatively and qualitatively.

### 6.1 Multilingual Image Generation Performance

**m-GenEval Comparison**: Despite having only 2B parameters, NeoBabel outperforms or matches best-performing unified models such as Janus-Pro 7B (0.77) and BLIP3-o 8B (0.83), which are significantly larger in terms of parameters. It also surpasses SD3 2B (0.62), a leading model in the generative category, achieving the highest overall score of 0.83.

**m-DPG Comparison**: NeoBabel achieves comparable performance in English (0.75), even though it uses only 2B parameters, which is far fewer than BLIP3-o (4B and 8B) and Janus Pro (7B). More importantly, NeoBabel outperforms all baselines in the non-English settings.

### 6.2 Qualitative Evaluation

The results show that NeoBabel consistently generates semantically aligned and visually coherent images. Objects, layouts, and attributes are preserved across languages, demonstrating the model's strong multilingual alignment and consistency in representing concepts.

#### 6.2.1 Multilingual Image Inpainting and Extrapolation

NeoBabel enables new collaborative applications, such as a multilingual visual canvas where users can contribute prompts in their native languages to co-create coherent and expressive visual scenes. It supports text-guided image inpainting and extrapolation across multiple languages without requiring additional fine-tuning.

#### 6.2.2 Cross-lingual Image Generation

A more challenging evaluation of the model's multilingual ability involves prompts that combine multiple languages within the same input. This requires the model to integrate information from different languages into a coherent and semantically accurate image. The images generated by NeoBabel demonstrate its ability to follow complex multilingual instructions, producing visually coherent and semantically faithful outputs.

## 7 Ablations and Analyses

### 7.1 Effect of Progressive Pretraining

Each stage leads to steady improvements in multilingual performance on m-GenEval and m-DPG. In the first stage, using only m-ImageNet 1K, the average scores are modest: 0.04 on m-GenEval and 0.14 on m-DPG. In the second stage, the addition of large-scale but noisy datasets results in a significant increase, reaching 0.17 on m-GenEval and 0.58 on m-DPG. The third stage incorporates higher-quality datasets, leading to further gains: 0.02 on m-GenEval and 0.04 on m-DPG.

### 7.2 Effect of Progressive Instruction Tuning

Both tuning stages progressively refine multilingual alignment, with consistent gains across all six languages. In the first stage, this stage yields a substantial multilingual gain of 0.52 on m-GenEval and 0.04 on m-DPG compared to the final stage of pretraining. In the second stage, this leads to a further multilingual gain of 0.02 in m-GenEval and a boost in m-DPG.

### 7.3 Effect of Model Merging on Generalization

We investigate the impact of model merging on multilingual image generation performance by combining N = 20 checkpoints sampled at 10,000-step intervals from the second instruction tuning stage. As reported, m-GenEval score on English prompt improves from 0.81 to 0.83 after model merging. Both WMA and SMA reach this upper bound, indicating that merging checkpoints along the optimization path enhances semantic alignment.

### 7.4 Cross-Lingual Consistency Analysis

Across both backbones, NeoBabel achieves the highest scores, 0.79 (EVA-CLIP) and 0.61 (DINOv2), outperforming larger models such as BLIP3-o 8B (0.77/0.45) and Janus Pro 7B (0.67/0.30). This indicates that training strategy and data alignment play a more significant role than parameter count alone in achieving cross-lingual consistency.

### 7.5 Code Switching Similarity Analysis

We evaluate model robustness to intra-prompt code switching using the proposed CSS score. NeoBabel consistently outperforms larger models, demonstrating stronger visual consistency under both English-First (EF) and English-Second (ES) variations. NeoBabel achieves this balance, with CSS scores of 0.82 (EF) and 0.81 (ES) for EVA-CLIP, and 0.67 (EF) and 0.64 (ES) for DINOv2.

## 8 Related Works

**Large Multimodal Models**: Recent advances in large multimodal models (LMMs) have extended large language models (LLMs) to support image understanding tasks, including image captioning and visual question answering. More recent encoder-free models bypass the explicit image encoder and instead align raw visual tokens directly within the LLM space.

**Visual Generative Models**: Two dominant paradigms have emerged for image and video generation: diffusion-based and autoregressive models. Diffusion models typically combine pretrained text encoders with denoising networks to iteratively refine visual outputs, while autoregressive models adopt LLM-based architectures trained via next-token prediction.

**Unified Multimodal Models**: Unified multimodal models aim to handle both image understanding and generation within a single architecture, typically categorized into native and adapter-based approaches.

## 9 Limitations

While NeoBabel demonstrates strong multilingual image generation capabilities, several limitations remain. First, the model currently supports only six languages; extending to broader linguistic coverage would require further tokenizer adaptation and additional training. Second, although NeoBabel adopts a unified architecture, it does not yet support vision-language tasks such as visual question answering, due to the absence of task-specific fine-tuning. Third, the model's performance is constrained by its parameter size and the diversity and quality of the training data.

## 10 Conclusion

NeoBabel demonstrates that high-quality, efficient multilingual image generation is not only possible but also advantageous. Through strategic data curation and a unified architecture, we set a new Pareto frontier in performance, efficiency, and inclusivity. While currently focused on text-to-image generation, our model is structurally capable of broader multimodal tasks. Our results across m-GenEval and m-DPG benchmarks, paired with the introduction of new evaluation metrics (CLC and CSS), establish a robust foundation for the next generation of multilingual generative models.

Our work opens several promising avenues for future research. First, extending NeoBabel to encompass a wider variety of languages, particularly those currently underrepresented in vision-language research, remains an important objective. Second, beyond linguistic diversity, integrating cultural grounding into multimodal models presents a compelling research direction. Finally, this work contributes to the broader goal of democratizing generative AI. By releasing all model weights, datasets, and evaluation protocols, we aim to encourage the research community to build upon this foundation, ultimately advancing toward generative models that better reflect and serve global linguistic and cultural diversity.

## Acknowledgment

We would like to thank the Cohere Labs team for their valuable feedback and for providing generous computing resources for conducting and analyzing our experiments. We further acknowledge the Dutch Research Council (NWO) in The Netherlands for awarding this project access to the LUMI supercomputer, owned by the EuroHPC Joint Undertaking, hosted by CSC (Finland) and the LUMI consortium through the Computing Time on National Computer Facilities call.

---

*This paper represents a significant contribution to multilingual AI research and directly demonstrates the type of innovative work being conducted at Cohere Labs in partnership with academic institutions.*
