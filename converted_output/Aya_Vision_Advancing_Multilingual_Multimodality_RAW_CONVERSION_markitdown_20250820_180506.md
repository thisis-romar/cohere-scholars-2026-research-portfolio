# Raw PDF Conversion: Aya_Vision_Advancing_Multilingual_Multimodality

**Source**: 01-PAPERS\Multimodal\Aya_Vision_Advancing_Multilingual_Multimodality.pdf
**Method**: markitdown
**Converted**: 20250820_180506
**Length**: 176137 characters

---

5
2
0
2

y
a
M
3
1

]
L
C
.
s
c
[

1
v
1
5
7
8
0
.
5
0
5
2
:
v
i
X
r
a

Aya Vision: Advancing the Frontier of

Multilingual Multimodality

Saurabh Dash

⋆ 1, Yiyang Nan

⋆1, John Dang1, Arash Ahmadian1,2,

Shivalika Singh1, Madeline Smith1, Bharat Venkitesh2,
Vlad Shmyhlo2, Viraat Aryabumi2, Walter Beller-Morales2,
Jeremy Pekmez2, Jason Ozuzu2, Pierre Richemond2,
Acyr Locatelli2, Nick Frosst2, Phil Blunsom2, Aidan Gomez2,
Ivan Zhang2, Marzieh Fadaee1, Manoj Govindassamy2, Sudip Roy2,
Matthias Gallé♦1, Beyza Ermis♦1, Ahmet Üstün♦1,
and Sara Hooker♦1

Corresponding authors: {saurabh, olivernan, matthias, beyza, ahmet, sarahooker}@cohere.com

1Cohere Labs, 2Cohere

Abstract

Building multimodal language models is fundamentally challenging: it requires aligning vision and
language modalities, curating high-quality instruction data, and avoiding the degradation of exist-
ing text-only capabilities once vision is introduced. These difficulties are further magnified in the
multilingual setting, where the need for multimodal data in different languages exacerbates exist-
ing data scarcity, machine translation often distorts meaning, and catastrophic forgetting is more
pronounced. To address the aforementioned challenges, we introduce novel techniques spanning
both data and modeling. First, we develop a synthetic annotation framework that curates high-
quality, diverse multilingual multimodal instruction data, enabling Aya Vision models to produce
natural, human-preferred responses to multimodal inputs across many languages. Complementing
this, we propose a cross-modal model merging technique that mitigates catastrophic forgetting,
effectively preserving text-only capabilities while simultaneously enhancing multimodal generative
performance. Aya-Vision-8B achieves best-in-class performance compared to strong multimodal
models such as Qwen-2.5-VL-7B, Pixtral-12B, and even much larger Llama-3.2-90B-Vision. We
further scale this approach with Aya-Vision-32B, which outperforms models more than twice its
size, such as Molmo-72B and LLaMA-3.2-90B-Vision. Our work advances multilingual progress on
the multi-modal frontier, and provides insights into techniques that effectively bend the need for
compute while delivering extremely high performance.
Aya-Vision-8B: https://huggingface.co/CohereLabs/aya-vision-8B
Aya-Vision-32B: https://huggingface.co/CohereLabs/aya-vision-32B
AyaVisionBench: https://huggingface.co/datasets/CohereLabs/AyaVisionBench

⋆First authors. ♦Principal senior advisors.

Released as a preprint on May 14, 2025

1

Figure 1: Aya Vision models achieve state-of-the-art multilingual performance across
both multimodal and text-only tasks. We report multimodal and text-only win rates against
Pangea-7B [Yue et al., 2024b], averaged over 23 languages. Aya-Vision-8B achieves best-in-class
multimodal performance without compromising text capabilities, while Aya-Vision-32B outperforms
all baselines, including much larger models such as Llama-3.2-90B-Vision [Grattafiori et al., 2024],
establishing an optimal balance between efficiency and cross-modal strength.

1

Introduction

We do not describe the world we see, we see the world we can describe. — René
Descartes

Although multimodal large language models (MLLMs) [Liu et al., 2023c; 2024; Deitke et al., 2024;
Team, 2024b; Laurençon et al., 2024a; Chen et al., 2024; Bai et al., 2025; Team et al., 2025] have
demonstrated remarkable success in jointly reasoning over various modalities, their performance
remains predominantly confined to English. This linguistic limitation represents a substantial bot-
tleneck in advancing multilingual AI, restricting global accessibility and impact.

Expanding multimodal models across languages exacerbates existing challenges at the frontier of
AI. Foremost among these is the scarcity of high-quality multimodal data. While there has been
expansion of languages served in language models [Üstün et al., 2024; Aryabumi et al., 2024b;
Dang et al., 2024; Cohere et al., 2025], the intersection of both images and languages remains
severely underserved. High-quality multimodal instruction-tuning datasets are scarce and primarily
composed of short, simplistic, task-oriented image-text pairs [Goyal et al., 2017; Wang et al., 2021;
Schwenk et al., 2022]. These datasets, while useful for benchmarking, inadequately prepare models
for the rich, conversational scenarios encountered in real-world applications. Existing approaches
primarily rely on machine translation to address this disparity [Li et al., 2023b; Maaz et al., 2024;
Yue et al., 2024b]. However, translations often introduce linguistic artifacts (“translationese”), biases
[Vanmassenhove et al., 2021; Savoldi et al., 2021; Hartung et al., 2023; Muennighoff et al., 2022],

2

and fail to capture culture-specific nuances [Singh et al., 2024b; Salazar et al., 2025], contextual
subtleties, and image-text alignments [Wang et al., 2022; Pudjiati et al., 2022]. Creating high-
quality, culturally and linguistically accurate multimodal instruction data across diverse languages
thus remains an essential yet unsolved challenge.

The second significant challenge is the known tension between adding vision capabilities and main-
taining robust text-only performance.
Integrating vision modalities commonly results in catas-
trophic forgetting, where models lose previously acquired language skills [Bai et al., 2023; Deitke
et al., 2024; Grattafiori et al., 2024; Pozzobon et al., 2023]. This decay is further amplified when
expanding coverage across multiple languages.

Equally pressing is the need for robust evaluations to measure progress. Any scientific pursuit re-
quires a reliable metric of success. Existing multimodal benchmarks typically emphasize academic-
style, multiple-choice tasks, evaluating models via rigid pattern-matching with predefined answer
sets [Changpinyo et al., 2022; Romero et al., 2024; Yue et al., 2024b]. While useful for standard-
ized comparisons, these fall short in capturing the nuanced, open-ended interactions that charac-
terize real-world usage. Moreover, the few benchmarks that support more complex, open-ended
interactions [Lu et al., 2024; Agrawal et al., 2024] are currently only available in English– leaving
multilingual multimodal evaluation largely unexplored.

In this work, we tackle these challenges collectively. To address data scarcity, we replace naive
translation pipelines with a hybrid method that pairs a specialized translation model with a larger
LLM to correct and remove systematic translationese artifacts. We term this approach context-aware
rephrasing, which enables the creation of higher-quality, human-preferred multimodal instruction
data. We also systematically explore the benefits of merging to mitigate catastrophic forgetting.
We propose a a novel cross-modal merging strategy (§ 3) that fuses capabilities across models,
allowing for preservation and “on-the-fly” extension of capabilities across modalities. We see this as
a powerful new paradigm to create adaptive models efficiently for new tasks. Our merging paradigm
improves text-only tasks 50.2% and multimodal tasks 20.5% relative to the unmerged checkpoint,
due to the inherent compositionality between the tasks and modalities.

The result of our work is Aya Vision, a family of state-of-the-art multilingual multimodal models
available in 8B and 32B sizes. In contrast to the many existing MLLMs, Aya Vision models are
trained with a strong emphasis on multilingual and multimodal generation, yielding fluent chat
performance. Aya-Vision-8B achieves best-in-class performance, surpassing Qwen-2.5-VL-7B [Bai
et al., 2025], Llama-3.2-11B-Vision [Grattafiori et al., 2024], Pixtral 12B [Agrawal et al., 2024],
and Gemini-Flash-1.5-8B [Team, 2024b], with up to 79% win rate across multimodal tasks in
23 languages. Aya-Vision-32B outcompetes models over twice its size, including Llama-3.2-90B-
Vision [Grattafiori et al., 2024], Molmo-72B [Deitke et al., 2024], and Qwen-2.5-VL-72B [Bai et al.,
2025], with win rates up to 72.4%.

Our primary contributions are as follows:

1. A family of state-of-the-art multilingual multimodal LLMs: We introduce Aya-Vision-
8B and 32B models, covering 23 languages spoken by half the worlds population. In contrast
to the many existing multimodal LLMs, Aya Vision models are trained with a strong emphasis
on multilingual, multimodal generation, yielding fluent chat performance preferred by humans.

3

Figure 2: Aya Vision establishes a new Pareto frontier in the performance-efficiency
trade-off. We show multimodal win rates against Pangea-7B, with respect to the number of
parameters for each model.

2. A novel multilingual multimodal synthetic annotation framework: We develop a
novel multilingual multimodal framework that combines synthetic data distillation, automated
translation, and context-aware rephrasing to produce high-quality and diverse instruction data
across languages, addressing data scarcity challenges. Recaptioning increases the average
number of tokens from 27.2 to 140.8 and the measure of lexical diversity from 11.0 to 61.2.
Our translation pipeline improves the translation quality by 11.24% over the NLLB-3.3B
[Costa-Jussà et al., 2022] translations.

3. Optimizing performance across modalities with cross-modal model merging: We
introduce a novel cross-modal model merging strategy that not only recovers text-only capabil-
ities lost to catastrophic forgetting – boosting text win-rates by up to 50.2% but simultaneously
enhances multilingual multimodal performance – improving vision win-rates by up to 20.5%,
demonstrating an efficient, training-free path to stronger models across modalities.

4. A comprehensive benchmark suite for real-world multilingual multimodal evalu-
ation: We introduce AyaVisionBench 1, a benchmark spanning 23 languages and 9 vision-
language tasks, specifically designed to evaluate generative, open-ended instruction follow-
ing. To support multilingual evaluation further, we introduce m-WildVision 2, a high-quality
translation of WildVision [Lu et al., 2024]. Together, they offer a meaningful and challenging
testbed for multimodal models.

1https://huggingface.co/datasets/CohereLabs/AyaVisionBench
2https://huggingface.co/datasets/CohereLabs/m-WildVision

4

2 A Comprehensive Multilingual Multimodal Data Framework

To solve for the scarcity of multilingual multimodal instruction data, prior efforts often depend on
direct LLM-based translations of English-centric datasets. Approaches such as Pangea [Yue et al.,
2024b] and Palo [Maaz et al., 2024] extend coverage across languages either through large-scale
translation or multilingual caption alignment. However, these methods still struggle with limited
linguistic diversity, the introduction of “translationese” from overreliance on translation, strict task
formulations, and a lack of conversational naturalness.

To address these gaps, we introduce a robust multimodal synthetic re-annotation pipeline for con-
structing high-quality multilingual multimodal datasets. As illustrated in Figure 3, our pipeline
comprises three core stages: 1) distillation-based recaptioning (§ 2.2), 2) dataset filtering (§ 2.3),
and 3) translation combined with multilingual rephrasing (§ 2.4). This pipeline significantly enhances
the dataset’s quality, diversity, and linguistic coverage, resulting in a rich multilingual instruction
dataset spanning 23 languages.

2.1 Data Collection

We began dataset construction by curating a diverse English-language multimodal instruction-
tuning corpus. We constructed our dataset on well-established open-source resources, including
Cauldron 3 [Laurençon et al., 2024b], a large-scale collection of 50 vision-language datasets (∼30M
samples), and PixMo4 [Deitke et al., 2024], a comprehensive dataset spanning seven multimodal
tasks (∼ 6M samples). We also drew from other sources such as SlideVQA [Tanaka et al., 2023],
PDFVQA [Ding et al., 2023], and ScreenQA [Hsiao et al., 2022]. Our dataset follows Cauldron’s
framework and covers a broad range of multimodal tasks: visual question answering (VQA), cap-
tioning, OCR and document understanding, chart and figure analysis, table comprehension, logical
reasoning, academic or textbook questions, image comparison, and code generation from screen-
shots. As Cauldron performs upstream filtering to remove duplicates across its aggregated sources,

Table 1: Task-wise distribution in our curated dataset, showing the proportion and the number of
samples in the ∼2.29M collection.

Task

VQA Capt.

OCR/
Doc

Chart/
Fig

Table
Compr.

Logic.
Reasoning

2 Image
Diff.

Textbook

Total Samples
Proportion

560K 220K
24.5% 9.6%

490K
21.4%

289K
12.6%

222K
9.2%

252K
11.0%

239K
10.4%

20K
0.9%

SS to
Code

9.5K
0.4%

the subset we use does not contain repeated samples. Likewise, the PixMo data we incorporate –
primarily within the chart and figure category – consists of synthetically generated content that is
distinct from Cauldron and other sources, ensuring no overlap across datasets.

To ensure robust generalization across task types, we regulated the number of samples per cat-
egory to construct a balanced and representative dataset. The final collection contains ∼2.29M
samples, with the task-wise sample counts and distribution detailed in Table 1. This English data
mixture serves as the basis for our further synthetic re-annotation and translation pipeline, forming
multilingual instruction tuning set used to train Aya Vision.

3https://huggingface.co/datasets/HuggingFaceM4/the_cauldron
4https://huggingface.co/collections/allenai/pixmo-674746ea613028006285687b

5

Figure 3: Our synthetic annotation pipeline enables diverse, high quality responses for
multimodal instructions. The pipeline consists of three core stages: (1) distillation-based re-
captioning, (2) machine translation, and (3) rephrasing. We highlight common machine translation
errors, such as unknown tokens (e.g. consistency, lit candle) or mistranslations, as in the case of
‘French press’ rendered as ‘French media’ due to lexical ambiguity in the word ‘press’. Rephrasing
helps to resolve such issues, improving both the fluency and semantic accuracy of translations.

2.2 Distillation-based Recaptioning

Our goal with recaptioning is to alter the data space such that it better reflects the data distribution
we aim to represent in the real-world. To achieve this, we generate synthetic alternatives to the
original completions across the ∼2.3M data points in our English dataset selection.

The original dataset is primarily composed of open-source, academic image captioning corpora,
which exhibit limited linguistic diversity and constrained stylistic variation. Much of the data
originates from a narrow set of sources such as MS-COCO [Lin et al., 2014], Visual Genome [Krishna
et al., 2017], and Open Images [Kuznetsova et al., 2020], leading to repetitive content and reduced
variation in captions for similar images. Furthermore, these English datasets are typically short and
simplistic (average caption length across datasets is just 14.2), and often lack detailed descriptions
or a conversational tone expected from state-of-the-art generative models.

Given these limitations, our goal with synthetic re-annotation is to generate recaptions that are
more detailed, natural, and diverse in both tone and content. However, a key constraint in this
process is that the recaptioned outputs also must remain anchored to the ground-truth answer.

The effectiveness of the recaptioning depends heavily on the quality of the prompt templates, which
play a critical role in shaping the richness and relevance of the generated annotations [Guo et al.,
2024; Fang et al., 2024]. To enhance the quality of our synthetic data, we design task-specific prompt
templates for the teacher model, which guide the recaptioning process. These prompt strategies are
adapted to rewrite captions based on the ground-truth and to meet the requirements of different
vision-language tasks. For example, templates for reasoning tasks are more structured to elicit step-
by-step explanations; captioning prompts emphasize more detailed and informative descriptions;
and VQA prompts are designed to have accurate and image-grounded answers. Table 2 presents
examples for two different tasks, illustrating how recaptioning instructions vary by context. For
additional task types and full prompt formats, see Appendix D.

6

Original DataPrompt:Prompt:Prompt:Prompt:Completion:Completion:Completion:Completion:Distillation Based RecaptioningMachine TranslationRephrasingQuestion: How many parts are shown in the heart? Choices:
A. 7. B. 4. C. 8. D.  3.Question: How many parts are shown in the heart?  Choices: A. 7. B. 4. C. 8. D.  3.Answer: AThe image displays the human heart with various parts labeled. To determine the number of parts shown, we can count each labeled section: 1. Aorta 2. Superior vena cava 3. Right atria 4. Tricuspid valve 5. Mitral valve 6. Left ventricle 7. Right ventricle. There are a total of 7 parts labeled in the image. Therefore, the correct answer is A.Source: AI2D [Kembhavi et al., 2016]问题:心脏有多少个部分? 选择:
一,七. B. 4. 没有 C. 八个 D. 3. 没有.图像显示了人类的心脏与标记的各个部分. 为了确定显示的部分数量, 我们可以计算每个标记的部分: 在 一个 大动脉 2. 没有 上腔静脉 3. 没有. 右心房 4. 没有 三<unk>门 五个 中心<unk> 六个 左心室 七个 右心室 在 图片中标有7个部分. 因此,正确的答案是A.问题: 心脏由多少部分组成? 选项:
A. 7 B. 4 C. 8 D. 3图像展示了人类心脏的各个部分，并附有标记。为了确定显示了多少部分，我们可以逐一计算每个标记的部分：1. 大动脉，2. 上腔静脉，3. 右心房，4. 三尖瓣，5. 心脏中心，6. 左心室，7. 右心室。图片中共标注了7个部分。因此，正确答案是A。Original DataPrompt:Prompt:Translated Prompt:Rephrased Prompt:Translated Recaption:Rephrased Recaption:Caption:Recaption:Distillation Based RecaptioningMachine TranslationRephrasingWhat kind of beverage is in the french press?What kind of beverage is in the french press?CoffeeThe French press in the image contains a dark liquid, which is likely coffee based on its color and consistency. The presence of a spoon next to the press also suggests that it might be used for stirring a beverage like coffee. Additionally, the overall warm and cozy setting, with a lit candle and autumnal decorations, is often associated with enjoying a hot cup of coffee. Therefore, it is reasonable to conclude that the beverage in the French press is coffee.Source: OK-VQA [Schwenk et al., 2022]法国媒体上有什么样的饮料?照片中的法式印刷机含有深色液体,根据颜色和<unk>度可能是咖啡. 压<unk>机旁边有一个<unk>匙, 也表明它可能用于<unk>咖啡等饮料. 另外,整体温暖舒适的环境, 灯<unk>和秋季装饰, 常常与享受一杯热咖啡有关. 因此,可以合理地得出结论,法国媒体所提到的饮料是咖啡.法国压滤壶中通常冲泡什么饮料？照片中的法式压滤壶装有深色液体，从其颜色和稠度来看，很可能是咖啡。压滤壶旁边有一把勺子，也暗示它可能用于搅拌咖啡等饮料。此外，整体温馨舒适的环境，点燃的蜡烛和秋季装饰，通常与享用一杯热咖啡的氛围相符。因此，可以合理地推断，法式压滤壶中的饮料是咖啡。Table 2: Examples of task-specific recaptioning outputs for different prompt strategies.

Task Type

Prompt Instruction (Simplified)

Sample Recaptioned Output

Captioning

Rewrite the original caption to be more de-
tailed, descriptive, and human-like. Avoid
introducing unseen elements.

A man wearing a red helmet rides a
mountain bike along a forest trail, sur-
rounded by tall green trees.

Reasoning /
Math

Solve the visual/mathematical problem
with a clear, step-by-step explanation.
Ensure logical correctness and clarity.
The response should be logical, clear, and
easy to follow. Include intermediate rea-
soning steps.

To find the total, we multiply 4 by 3
because there are 4 rows with 3 items
each. 4 × 3 = 12. So, the final answer
is 12.

Taken together, recaptioning serves to bridge the gap between limited, narrowly scoped training
data and the rich, diverse language found in real-world contexts. To quantify its linguistic impact,
we analyze several textual properties –average word count, number of tokens, and lexical diversity
– using the Measure of Textual Lexical Diversity (MTLD) [Shen, 2022]. Following recaptioning, the
average word count increases from 14.2 to 100.1, token count rises from 27.2 to 140.8, and
MTLD improves from 11.0 to 61.2. Higher MTLD scores indicate greater vocabulary variation;
a score of 61.2 suggests strong lexical richness comparable to fluent language use [McCarthy &
Jarvis, 2010; Ploeger et al., 2024]. These more expressive and natural annotations support better
generalization and improved robustness in downstream multimodal tasks. Examples of recaptioned
outputs are provided in Appendix E.

2.3 Verifying and Filtering Recaptioned Instruction Data

Recaptioning offers a scalable approach to improving the quality of model responses. However,
synthetic generations can still introduce errors or hallucinated content that is not grounded in the
image [Rohrbach et al., 2018; Liu et al., 2023b; Li et al., 2023c; Gunjal et al., 2023]. Training on
such data may amplify a model’s tendency to hallucinate or generate inaccuracies that compromise
overall quality. To mitigate these risks and ensure both fluency and correctness, we implement a
two-stage filtering pipeline that enhances the overall reliability of the recaptioned dataset. While
some methods apply single-pass alignment filtering, e.g CLIP score [Gadre et al., 2023], or train
models to avoid hallucinations using reward learning [Ben-Kish et al., 2023; Wang et al., 2024a], our
two-stage pipeline adds an extra safeguard against the inclusion of fluent yet hallucinated outputs.

Stage 1: Keyword-based filtering. We begin with simple keyword detection to identify recap-
tioned samples that exhibit common failure modes, such as refusals to respond or repeated phrases
from the input prompt. To catch these issues, we compile a list of keywords and phrases that au-
tomatically flag such responses. Flagged samples are either sent back to the model for regeneration
or discarded if the issue persists.

While keyword-matching can detect basic errors, it still struggles to identify more subtle inaccura-
cies. This limitation is particularly critical for tasks that require deterministic or subjective answer,
such as question answering or mathematical reasoning. In these cases, the teacher model may ignore
the provided ground truth or hallucinate details, resulting in flawed or incorrect answers.

7

Stage 2: LLM-based semantic filtering. To address more nuanced errors, we apply a second-
stage filtering using command-r-plus-08-20245 for semantic verification (see Appendix F for the
prompt). In this stage, the original and rephrased captions are presented to the model, which acts
as a semantic judge to assess whether the answer to the original caption remains valid given the
rephrased version. This ensures that recaption do not alter the underlying meaning or contradict
with the ground truth answer. All corrupted samples identified at this stage are discarded. This
step reveals an overall error rate of 3.2% (62,370 samples) in the recaptioned data. Task complexity
significantly influences error frequency – for example, reasoning tasks exhibit a higher error rate
(4.6%) than simpler VQA tasks (2.5%). This trend aligns with findings from prior work [Yue et al.,
2024a; Wang et al., 2024c; Song et al., 2025]. By integrating keyword-based filtering with nuanced
semantic evaluation capabilities of an LLM, our pipeline generates a recaptioned dataset that is
cleaner, more reliable, and better optimized for visual instruction tuning. Examples of filtered
samples are provided in Appendix F.

2.4 Hybrid Translation Pipeline for Multilingual Instruction Data

Our approach diverges from prior efforts that either rely exclusively on proprietary LLMs for transla-
tion [Yue et al., 2024b; Maaz et al., 2024] or highlight disparities in translation quality between high-
and low-resource languages without directly addressing how to mitigate them [Hendy et al., 2023].
For example, Hendy et al. [2023] find that GPT models perform competitively on high-resource lan-
guages but struggle significantly with low-resource ones. Although machine translation has inherit
limitations, it remains essential for broad language coverage, especially in-language human-curated
datasets in many languages are scarce and typically reserved for evaluation [Singh et al., 2024b;
Romanou et al., 2024; Aakanksha et al., 2024b; Singh et al., 2024a; Salazar et al., 2025]. Prior work
has also shown that translating instruction data can significantly improve cross-lingual generaliza-
tion in language models [Ranaldi & Pucci, 2023; Dang et al., 2024; Ermis et al., 2024; Üstün et al.,
2024].

However, while machine translation models offer broad coverage, they often introduce artifacts that
compromise fluency and fidelity. These include unnatural phrasing, incorrect lexical choices, or
incomplete renderings as documented in prior studies [Bizzoni et al., 2020; Vanmassenhove et al.,
2021; Üstün et al., 2024; Singh et al., 2024b]. Large language models may struggle with translation,
especially in low-resource language contexts [Zhu et al., 2023]. To balance language coverage with
translation quality, we adopt a hybrid approach:

• We begin with machine translation, using the NLLB-3.3B model6 [Costa-Jussà et al., 2022].
Specifically, we translate our re-annotated English dataset (see §2.2) into the following 22
languages: Arabic, Chinese, Czech, Dutch, French, German, Greek, Hebrew, Hindi, Indone-
sian, Italian, Japanese, Korean, Persian, Polish, Portuguese, Romanian, Russian, Spanish,
Turkish, Ukrainian, and Vietnamese.

• We then apply a post-editing step using a capable multilingual language model, command-r-pl-
us-08-20245, to refine the translations. This step uses the initial machine-translated output
as an in-context example to guide the model toward generating more fluent and accurate
outputs [Zhu et al., 2023; Raunak et al., 2023].
In doing so, we correct common machine
translation artifacts while preserving the original semantic content.

5https://huggingface.co/CohereLabs/c4ai-command-r-plus-08-2024
6https://huggingface.co/facebook/nllb-200-3.3B

8

The prompt used for this rephrasing step and some examples illustrating improvements from rephras-
ing are in Appendix G.

This two-stage process ensures higher translation quality across languages by combining broad
coverage from machine translation with fluency improvements from LLM-based post-editing. To
further improve training efficiency and generalization, we do not translate the full English dataset
into all 22 languages; instead, we randomly sample subsets of the English pool of examples for
each languages. This approach improves efficiency and helps avoid overfitting by reducing repeated
exposure to identical content across languages. Prior work has shown that partial translation can
achieve strong multilingual generalization while significantly reducing data size [Geigle et al., 2023;
Shaham et al., 2024], and is commonly used in large-scale multilingual datasets to enhance linguistic
diversity without unnecessary duplication [Muennighoff et al., 2022; Nguyen et al., 2024; Üstün et al.,
2024; Dang et al., 2024; Aryabumi et al., 2024a].

To evaluate translation quality, we report COMET7 8 [Rei et al., 2020; 2023], a reference-free
machine translation evaluation metric. The translations from NLLB-3.3B achieve an average score
of 0.7455 across the 22 languages. After post-editing, the average score increases to 0.8293,
indicating the effectiveness of our hybrid strategy. COMET scores typically range from 0 to
1, with higher values indicating better adequacy and fluency. Thus, a gain of over 0.08 reflects
a substantial quality improvement. Detailed per-language COMET improvements are reported in
Table 7 in Appendix K.

3 Balancing Performance across Languages, Modalities and Tasks

For multimodal LLMs, carefully sampling the fine-tuning mixture with high-quality and task-
oriented visual instructions is crucial for optimal performance [Liu et al., 2023c; Laurençon et al.,
2024b; Tong et al., 2024; Dai et al., 2024]. In multilingual multimodal LLMs, this challenge in-
tensifies as the balancing should be optimized for both multilingual and multimodal dimensions.
Previous works [Üstün et al., 2024; Aryabumi et al., 2024b; Dang et al., 2024] have shown that
a skewed distribution of languages in the training mixture hampers the model’s ability to learn
reliably, leading to measurable drops in accuracy on a subset of languages. Furthermore, a state-
of-the-art multimodal LLM should also retain its text-only capabilities, as these models are often
deployed in real-world scenarios that encompass both multimodal and text-only use cases.

Retaining the text-only performance of the backbone LLM, while acquiring strong multimodal
capabilities through multimodal training is challenging for several reasons. Firstly, choosing the
data mixture to strike a balance between multimodal and text datasets is a challenging problem, as
finding the right balance is non-trivial and requires a multitude of ablations. For instance, Molmo
[Deitke et al., 2024] and Pangea [Yue et al., 2024b] include approximately 10% text-only data in their
multimodal SFT mixture to retain text performance. While this might enable minimal degradation
on text-only academic benchmarks, we observe in practice that both models suffer a significant drop
in open-ended generation performance measured by the preference evaluation as shown in Figure 5.

Secondly, reintroducing previously seen text-only data can potentially lead to overfitting with mini-
mal improvement in text performance and a higher degradation in multimodal performance [Marafi-

7https://github.com/Unbabel/COMET
8https://huggingface.co/Unbabel/wmt23-cometkiwi-da-xxl

9

Task

General VQA
Captioning
OCR
Figures/Charts
Table Compr.
Reason./Logic/Math
Multi Image
Textbook/Academic
Screenshot → Code

.
g
i
r
O

269.0k
-
231.8k
290.0k
77.5k
-
39.6k
19.1k
9.5k

.
i
t
l
u
M

311.2k
74.6k
60.7k
31.3k
260.7k
136.4k
78.0k
-
5.2k

.
h
t
n
y
S

168.2k
109.0k
188.8k
159.6k
56.5k
60.9k
97.3k
12.8k
-

l
a
t
o
T

748.4k
183.6k
481.3k
480.9k
394.7k
197.2k
214.8k
31.9k
14.7k

)

%

(
r
e
P

27.2
6.7
17.5
17.5
14.4
7.2
7.8
1.2
0.5

Total

936.3k

958.1k

853.0k

2.75M 100%

Figure 4: Overview of our multilingual multimodal SFT mixture from various task
categories. Left: Number of samples across data sources and tasks categories used in training.
Right: Visual breakdown of dataset source distributions.

oti et al., 2025]. We further investigate this pattern through ablations, presented in detail in Sec-
tion 7.2. Moreover, post-training of state-of-the-art LLMs typically involves several steps of SFT
and preference optimization [Dang et al., 2024; Lambert et al., 2024; Cohere et al., 2025], which
could cause instability due to the shift in the data distribution in the multimodal fine-tuning step.
This highlights the importance of striking a balance during multimodal fine-tuning to maintain
model robustness and generalization.

In this work, we explore a variety of mitigation to this solution including (1) systematic weighting of
different sources of data to preserve both language balancing and diversity, (2) Cross-modal model
merging to seamlessly integrate multimodal and text-only capabilities.

3.1 Sampling Visual Instructions from Multiple Sources and Languages

To balance coverage and preserve diversity, we mix and weight three buckets of data:

1. Synthetically Re-annotated data in English: This data was generated after the first
phase of our data framework (§ 2.2), 2.29M samples in total. Inside this bucket, we upsample
datasets with a small number of samples, such as science or textbook questions, to avoid
underrepresenting any task categories. Additionally, we also upsample datasets deemed to be
of higher quality upon manual inspection leading to a total of 3.5M samples from this bucket
being seen by the model.

2. Multilingual datasets: This data was generated by using a subset of re-annotated English
dataset through our data framework (§ 2.4). We uniformly sample data across 22 languages
(except English) and maintain a similar task distribution to the first bucket. While the total
data volume in this bucket amounts to a total of 5M samples, we sample 3.4M uniformly
distributed across 22 languages (except English) to preserve the balance between tasks.

3. High-quality original datasets: In addition to the fully synthetic data, we also use a
selection of original datasets, based on their quality. This bucket is required since some
downstream VQA evaluations expect syntactically accurate answers that match their training

10

MultilingualOriginalSyntheticGeneral VQATablesMulti ImageCaptioningOCRFigures / ChartsGeneral VQAOCRTablesOCRGeneral VQAFigures / ChartsCaptioningMulti ImageTablesScreenshot → CodeFigures / ChartsReasoning / Logic / MathTextbook / AcademicReasoning / Logic / MathTextbook / AcademicScreenshot → CodeMulti Imagedistribution and penalize semantically correct generations (for example 0.5 instead of 1/2).
However, we downsample the original corpus to avoid a drop in overall quality, as this data
penalizes natural generations and completion length – thereby degrading the model’s free-form
conversational abilities. While the total number of samples in this bucket is 6M, we sample
3.7M for training.

In each data bucket, we ensure a diverse set of tasks is represented. To enhance multilingual perfor-
mance, we experiment with varying proportions of multilingual data – these results are presented in
§ 7.4. Based on these findings, we use approximately 66% of synthetically re-annotated datasets out
of which 35% corresponds to the multilingual datasets; while the remaining 34% are the high-quality
original datasets. Figure 4 illustrates the composition of the training data across buckets and tasks,
totaling 2.75M sequence-packed final training samples.

3.2 Unifying Multimodal Performance with State-of-the-Art Text Capabilities

In Aya Vision, instead of balancing multimodal
and text-only abilities in the data space via a
sweep over data mixtures, we introduce a novel
cross-modal model merging inspired by the re-
cent body of work in model merging [Worts-
man et al., 2022; Matena & Raffel, 2022; Yadav
et al., 2023; Aakanksha et al., 2024a; Goddard
et al., 2024]. Concretely, we posit that since
the multimodal model is initialized from the fi-
nal preference-tuned LLM checkpoint, sharing
a part of the optimization trajectory [Izmailov
et al., 2018; Frankle et al., 2020; Ilharco et al.,
2022] makes the multimodal LLM and the back-
bone LLM amenable to merging. Cross-modal
model merging introduces an efficient, training-
free recovery solution for retaining text-only
performance by balancing multimodal and text-
only capabilities in the weight space aposteriori. We conduct systematic study of merging techniques
applied to the weights of the original text-only LLM and the LLM backbone of the multimodal model
(see § 7.1).

Figure 5: Degradation in text-only win-rates
after multimodal training. Each model is com-
pared to their initial LLM on mArenaHard [Dang
et al., 2024]. We see that only including a per-
centage of text-only data in the final multimodal
training mix is insufficient to retain open-ended
generative performance.

We perform a linear interpolation between the text-only LLM and the backbone LLM of the multi-
modal model as the merging method, as shown in Equation 1. Since the text-only language model
lacks the vision encoder and alignment layer, we simply inherit them from the vision-language
model.

Wmerged = α.Wmm-LLM + (1 − α).Wtext-LLM

(1)

11

Aya Vision-8BPangea-7BQwen2.5VL-7BMolmo-7B5040302010010Win Rate (%)-5.92%-16.43%-22.14%-44.08%Text Win Rates against Initial LLM4 Aya Vision’s Architecture and Training Details

4.1 Architecture

Aya Vision models follow the common architecture design for vision-language models [Liu et al.,
2023c; 2024; Laurençon et al., 2024b; McKinzie et al., 2024; Chen et al., 2024; Deitke et al., 2024] that
is based on late-fusion [Team, 2024a] of (1) a vision encoder to compute image patch embeddings
which is pre-trained on billions of image-text pairs [Radford et al., 2021; Zhai et al., 2023; Chen
et al., 2024; Tschannen et al., 2025], (2) a connector that maps the embeddings from the output
space of the vision encoder to the input embedding space of the language model, (3) a large language
model.

Vision Encoder: We use siglip2-so400m [Tschannen et al., 2025] as the initialization for the
vision encoder, which has been pretrained with an auto-regressive decoder-based loss in addition
to the original sigmoidal loss [Zhai et al., 2023]. This primes the vision encoder to generate high-
quality dense feature representations for generative tasks, making it the perfect candidate for a
multilingual vision language model. Specifically, we use siglip2-so400m-patch14-3849 in Aya-
Vision-8B for a reduced activation footprint, making it widely accessible on cheaper hardware. For
Aya-Vision-32B, we opt for the higher resolution siglip2-so400m-patch16-51210 to achieve better
performance[Laurençon et al., 2024b].

Image Processing: The performance of multimodal LLMs improves with higher input resolution
[McKinzie et al., 2024; Laurençon et al., 2024b], however, most vision encoders are pretrained on a
fixed resolution. To enable Aya Vision models to process images with arbitrary resolutions, similar
to Chen et al. [2024], we map the input images to the nearest supported resolution that minimizes
distortion in the aspect ratio. After resizing, we split the image into up to 12 non-overlapping tiles
based on the image encoder’s resolution to be processed independently by the vision encoder. In
addition to tiles, we include a thumbnail (resized) for a low-resolution overview of the image.

Vision-Language Connector: Following the image encoder, the vision-language connector maps
features from the vision encoder to the language model’s input embedding space. We use a 2-layer
MLP with SwiGLU activation function [Shazeer, 2020]. To reduce the number of image tokens
passed to the language model, we perform Pixel Shuffle [Chen et al., 2024], which downsamples the
image tokens in the spatial dimensions by stacking 2 × 2 patch embeddings along the embedding
dimension before passing through the connector layer. This decreases the number of image tokens by
4×, resulting in a maximum of 2,197 and 3,328 image tokens for our 8B and 32B models respectively.
When passing image tokens to LLM, we use special delimitation tokens to denote the start and the
end of image token sequences. Additionally, we inject 1D-tile tags [Dai et al., 2024] to denote
image tiles as a form of explicit positional encoding for the tiles. We use regular text tokens
(TILE_1,...,TILE_N and TILE_GLOBAL for thumbnail) for potential inference-time scaling.

Language Model: Although some previous works initialize the language model from a pre-trained
base checkpoint [Beyer et al., 2024], we initialize the language model from a multilingually post-
trained LLM to inherit strong capabilities in various tasks including chat, instruction-following,
and multilingual. For Aya-Vision-8B, we use an LLM based on Command-R7B11 which is further

9https://huggingface.co/google/siglip2-so400m-patch14-384
10https://huggingface.co/google/siglip2-so400m-patch16-512
11https://huggingface.co/CohereLabs/c4ai-command-r7b-12-2024

12

post-trained with the Aya Expanse recipe [Dang et al., 2024], and for Aya-Vision-32B, we use the
Aya-Expanse-32B [Dang et al., 2024].

4.2 Multimodal Training

Following previous work that use late-fusion as in our models [Liu et al., 2023c; 2024; Laurençon
et al., 2024b; McKinzie et al., 2024; Chen et al., 2024; Deitke et al., 2024], we train Aya Vision
models in two steps: (1) Vision-Language Alignment and (2) Supervised Fine-tuning.

Vision-Language Alignment: In this step, we only train the vision-language connector by keep-
ing both the vision encoder and the language model frozen. Freezing the language model and vision
encoder allows for using a high learning rate to quickly map the image features to the input em-
bedding space. We use a peak learning rate of 10−4 and 10−3 for Aya-Vision-8B and 32B models
respectively. Additionally, we find that the 32B model requires longer training in this step due to
the much larger connector size. While Aya-Vision-8B includes a 190M vision-language connector,
the parameter size of the connector in 32B model is 428M. Therefore, we train the 8B model for
9.7k steps (1 epoch) and the 32B model for 19k steps (2 epochs). Similar to previous works [Liu
et al., 2023c; Yue et al., 2024b] we use LLaVa-Pretrain12 as the primary source of data in this step.
However, since this data is English-only, we add a small fraction of the multilingual data generated
by our data framework amounting to 14% of the total data seen during this step. All training details
can be found in Table 6 in the appendix.

Visual Instruction Fine-tuning: In the instruction fine-tuning step (i.e., supervised fine-tuning
with visual instructions), we train both the vision-language connector and the language model but
keep the vision encoder frozen. We experiment with both full model fine-tuning and LoRA [Hu
et al., 2022]. For both Aya-Vision-8B and Aya-Vision-32B, we use a batch size of 128 and train for
31k iterations with µP enabled on about 10M samples. The peak learning rates are set to 10−4 and
5 × 10−4 respectively established via hyperparameter tuning. We utilize sequence packing to pack
multiple samples into a single sequence of length 8192 for improved training efficiency. A breakdown
of the SFT training data can be found in Figure 4 with detailed discussion presented in § 3.

5 Evaluation

5.1 Multilingual Multimodal Preference Evaluation

5.1.1 Open-ended Multimodal Evaluation

While recent efforts have explored multilingual evaluation for multimodal LLMs [Changpinyo et al.,
2022; Romero et al., 2024; Tang et al., 2024; Yue et al., 2024b], existing benchmarks still fall short
of enabling robust, real-world evaluation. Most current suites focus on static, single-turn tasks with
predefined answers, failing to capture the nuanced, open-ended, and dynamic nature of real-world
user interactions. To address this, we introduce:

AyaVisionBench 13, a benchmark explicitly designed to evaluate not only multimodal understand-
ing and reasoning but also generation quality along human-centric dimensions, such as relevance,

12https://huggingface.co/datasets/liuhaotian/LLaVA-CC3M-Pretrain-595K
13https://huggingface.co/datasets/CohereLabs/AyaVisionBench

13

Dataset

Task

Metric

# Languages

Multimodal Academic Bench.

xMMMU [Yue et al., 2024b]

Multimodal Understanding

Accuracy

MaXM [Changpinyo et al., 2022]

CVQA [Romero et al., 2024]

MTVQA [Singh et al., 2019]

Kaleidoscope [Salazar et al., 2025]

VQA

VQA

VQA

VQA

Multimodal Open-Ended Bench.

AyaVisionBench

m-WildVision [Lu et al., 2024]

xChat [Yue et al., 2024b]

Text-only Bench.

Multimodal Chat

Multimodal Chat

Multimodal Chat

Accuracy

Accuracy

VQA Score

Accuracy

Win-Rates

Win-Rates

LLM-Score

m-ArenaHard [Dang et al., 2024]

Open-Ended Generations

Win-Rates

MGSM [Shi et al., 2022]

Math. Reasoning

Global MMLU-Lite [Singh et al., 2024a]

Language Understanding

FLORES [Guzmán et al., 2019]

Language Understanding

IFEval [Zhou et al., 2023]

Instruction Following

Accuracy

Accuracy

SpBLEU

Accuracy

7

7

31

9

18

23

23

7

23

6

15

23

1

Table 3: Multilingual multimodal evaluation suite used in Aya Vision. Our evaluation suite
consists of multilingual multimodal benchmarks, multimodal open-ended benchmarks for preference
evaluation, and finally, text-only benchmarks include open-ended, generative, and discriminative
evaluation sets.

fluency, and engagement. AyaVisionBench targets the question: How well can a multimodal model
respond to complex, open-ended instructions across languages and modalities?

AyaVisionBench spans 23 languages and comprises 135 image-question pairs per language, cover-
ing 9 diverse task categories: captioning, chart and figure understanding, identifying differences
between two images, general visual question answering, OCR, document understanding, text tran-
scription, mathematical or logical reasoning, textbook questions and converting screenshots to code.
This multilingual, multi-task design supports comprehensive evaluation of cross-lingual multimodal
understanding. Most samples include ground-truth responses for reference. Further construction
details are available in Appendix A.1. The benchmark is publicly released for community use and
broader evaluation.

Multilingual WildVision (m-WildVision) and xChatBench To complement AyaVisionBench,
we release m-WildVision14, a multilingual extension of WildVision-Bench [Lu et al., 2024], fea-
turing translated prompts in 22 languages. WildVision is curated from real-world user interactions
and provides practical, context-rich evaluation scenarios. We also incorporate xChatBench [Yue
et al., 2024b], which supports fine-grained, score-based assessments across 7 languages and various
interaction types.

14https://huggingface.co/datasets/CohereLabs/m-WildVision

14

To evaluate model performance across all three benchmarks, we follow the VLM-as-a-judge proto-
col used in prior multilingual studies [Üstün et al., 2024; Dang et al., 2024], conducting pairwise
comparisons between Aya Vision and baseline models. For scoring and preference ranking, we use
claude-3-7-sonnet-20250219 [Anthropic, 2025] as the multimodal judge. This choice is based on
a comparative study using the translated Multimodal RewardBench [Yasunaga et al., 2025] across 8
languages,15 where Claude-3-7-Sonnet outperformed GPT-4o [OpenAI, 2024] and Gemini-2.0-Flash
[Team et al., 2024] by 6.4% and 25.8% respectively in preference ranking accuracy. Full details on
the evaluation prompt are provided in Appendix J.

5.1.2 Academic Multilingual Multimodal Benchmarks

In addition to the preference-based open-ended multimodal evaluation, we evaluate Aya Vision on
visual question answering and reasoning style benchmarks that require the generations to adhere
to a prescribed format, such as multiple-choice style or short-form answers, for easy automated
evaluation. Specifically, we use xMMMU [Yue et al., 2024b], MaXM [Changpinyo et al., 2022],
CVQA [Romero et al., 2024], MTVQA [Tang et al., 2024] and Kaleidoscope [Salazar et al., 2025].
These benchmarks, covering a range of languages, measure multimodal understanding, knowledge,
and reasoning capabilities of multimodal LLMs. The number of languages in each dataset is shown
in Table 3, and details of these benchmarks are given in Appendix A.

5.2 Multilingual Text-Only Evaluations

As a final component of our multilingual evaluation suite, we evaluate Aya Vision models and
baselines on various text-only benchmarks. This is important to reflect real-world deployment sce-
narios where models are used with both multimodal and text-only inputs. However, as shown in § 3,
many vision-language models experience some degree of degradation in their text-only performance.
Therefore, to evaluate models’ performance in various tasks, we include a set of representative text-
only evaluations.

Open-ended evaluation Similar to AyaVisionBench, we use m-ArenaHard [Li et al., 2024;
Dang et al., 2024] to evaluate and compare models’ performance in open-ended text generations in
23 languages.16

Task-specific benchmarks Additionally, we included MGSM [Shi et al., 2022], Global MMLU-
Lite [Singh et al., 2024a], and FLORES [Guzmán et al., 2019] covering mathematical reasoning,
multilingual language understanding, and machine translation, respectively. Each of these bench-
marks includes a different set of languages, as listed in Table 3. For FLORES, we evaluate models’
translation performance from English to the target language (En→X) as translating from English is
a harder task and a good indication for multilingual performance. Finally, we also include IFE-
val [Zhou et al., 2023], although it is English-only, as it measures instruction-following capabilities
of models, which potentially impacts the performance in other multimodal and text-only bench-
marks. Metrics for these benchmarks are given in Table 3, and additional details can be found in
Appendix A.

15English (original), Arabic, Farsi, French, Hindi, Portuguese, Turkish, Vietnamese, Simplified Chinese.
16We use gpt-4o-2024-11-20 [OpenAI, 2024] as the LLM-judge following Dang et al. [2024].

15

Figure 6: Aya-Vision-8B achieves best-in-class performance on preference evaluation.
Pair-wise win-rates on AyaVisionBench and m-WildVision [Lu et al., 2024] averaged across 23
languages. We compare Aya-Vision-8B with Gemini-Flash-8B, Llama-3.2-11B-Vision, Qwen-2.5–
VL-7B, Pixtral-12B and Pangea-7B on AyaVisionBench (left) and m-WildVision (right). Language-
specific breakdown for the results can be found in Table 9 & Table 10 in the Appendix.

Models / Evaluations MaxM xMMMU CVQA MTVQA Kaleidoscope xChat

avg

Pangea-7B

Molmo-7B-D

Llama-3.2-11B-Vision

Pixtral-12B

Qwen-2.5-VL-7B

Aya-Vision-8B

Molmo-72B

51.27

44.16

39.30

44.43

52.65

58.21

55.62

Llama-3.2-90B-Vision

64.17

Qwen-2.5-VL-72B

Aya-Vision-32B

56.42

62.28

44.00

37.87

42.73

42.27

46.77

39.94

51.53

52.40

61.74

45.11

60.53

58.53

58.92

63.54

73.22

61.86

72.77

81.88

82.10

74.06

18.32

16.89

16.40

19.81

29.57

19.33

18.66

27.44

31.92

23.46

29.46

36.42

36.50

36.08

39.64

38.62

50.34

48.41

55.02

41.73

32.21

23.36

28.59

64.50

58.14

58.64

45.43

51.12

39.30

36.21

37.07

45.11

50.00

46.16

49.06

54.24

71.13

59.72

70.07

52.81

Table 4: Evaluation on multilingual multimodal benchmarks for Aya-Vision-8B and Aya-
Vision-32B together with the baselines. For each benchmark, we include languages that are
in the list of Aya Vision’s 23 languages. The full results on all available languages are given in
Appendix K.

5.3 Baselines

We compare Aya Vision models against a range of state-of-the-art multimodal LLMs, both open- and
closed-weight, to evaluate multilingual, multimodal, and text-only capabilities. We select models
based on architecture, model size, base model family, and language coverage. The selected models
cover a range of sizes (7B to 90B), base models (Llama-3.2, Qwen-2.5, Molmo), and language

16

Gemini-Flash1.5-8BLlama-3.211B-VisionQwen-2.5-VL7BMolmo7B-DPixtral12BPangea7B020406080Win Rate (%)     56.0%     72.1%     52.7%     78.5%     49.2%     70.3%     35.1%     19.1%     37.7%     11.9%     41.3%     18.7%     8.9%     8.8%     9.6%     9.6%     9.1%     11.0%Win Rate (AyaVisionBench)Gemini-Flash1.5-8BLlama-3.211B-VisionQwen-2.5-VL7BMolmo7B-DPixtral12BPangea7B020406080     64.5%     79.1%     57.5%     80.3%     59.4%     73.1%     31.4%     17.2%     38.4%     15.3%     35.7%     22.1%     4.0%     3.8%     4.1%     4.5%     5.0%     4.8%Win Rate (m-WildVision)WinLossTieFigure 7: Aya-Vision-32B outperforms models more than double its size. Pairwise win-
rates on AyaVisionBench and m-WildVision [Lu et al., 2024] averaged across 23 languages. We
compare Aya-Vision-32B with Llama-3.2-90B-Vision, Molmo-72B and Qwen-2.5-VL-72B on AyaV-
isionBench (left) and m-WildVision (right). Language-specific breakdown for the results can be
found in Table 12 & Table 13 in the Appendix.

coverage (including both English and multilingual models). Our evaluation includes open-weight
models (Pixtral [Agrawal et al., 2024], Molmo [Deitke et al., 2024], Qwen-2.5-VL [Bai et al., 2025]
and Pangea [Yue et al., 2024b]) as well as the closed-weight (Gemini-Flash-1.5 [Team, 2024b]). For
model families, Qwen, Molmo, and Llama, we report results across multiple sizes ranging from 7B
to 90B parameters.

Among the baseline models, Pangea, Qwen, Pixtral, Llama, and Gemini explicitly report multilin-
gual support. We also include Molmo, which does not explicitly claim to support multiple languages,
however in practice, they are heavily used by multilingual users relative to some multilingual models
like Pangea-7B [Yue et al., 2024b]. Hence, we think it is important to include. Furthermore, we
also find that these models achieve considerable performance in many multilingual tasks, as shown
in our evaluation.

17

Llama-3.290B-VisionMolmo72BQwen-2.5-VL72B020406080Win Rate (%)   65.9%   61.2%   48.5%   26.9%   32.9%   44.8%   7.2%   5.9%   6.7%Win Rate (AyaVisionBench)Llama-3.290B-VisionMolmo72BQwen-2.5-VL72B020406080   73.0%   68.8%   53.3%   23.6%   27.0%   42.9%   3.4%   4.2%   3.8%Win Rate (m-WildVision)WinLossTieFigure 8: Aya Vision models are amongst the best models in text-only preference evalu-
ation compared to models with much larger size. Pairwise win-rates for Aya-Vision-8B (left)
and 32B (right) on m-ArenaHard [Li et al., 2024; Dang et al., 2024] averaged across 23 languages.
Language-specific breakdown for the results can be found in Table 8 & Table 11 in the Appendix.

Models / Evaluations G-MMLU (Lite) MGSM FLORES IFEval

avg

Pangea-7B

Molmo-7B-D

Llama-3.2-11B-Vision

Pixtral-12B

Qwen-2.5-VL-7B

Aya-Vision-8B

Molmo-72B

Llama-3.2-90B-Vision

Qwen-2.5-VL-72B

Aya-Vision-32B

49.35

39.63

60.75

66.09

64.82

62.52

71.02

77.46

81.49

63.58

50.51

49.94

72.84

77.62

60.90

76.42

86.00

66.67

89.61

79.46

28.04

15.74

31.84

29.29

27.98

35.90

32.52

38.25

35.71

37.79

23.99

56.10

83.43

65.59

72.46

82.78

78.10

88.14

37.97

40.35

62.22

59.65

56.54

64.41

66.91

67.63

89.74

74.14

78.50

64.83

Table 5: Evaluation on multilingual text-only academic benchmarks for Aya-Vision-8B
and Aya-Vision-32B together with the baselines. For each benchmark, we include languages
that are in the list of Aya Vision’s 23 languages. The full results on all languages are available in
Appendix K.

18

Gemini-Flash-1.5-8BLlama3.2-11BQwen2.5-VL-7BMolmo-7B-DPixtral-12BPangea-7B020406080100Win Rate (%)   30.5   63.4   61.6   95.9   44.0   80.0   69.3   36.3   38.0   3.8   55.7   19.5   0.1   0.3   0.5   0.2   0.3   0.5Aya Vision-8BLlama3.2-90BMolmo-72BQwen2.5VL-72B020406080100   43.2   77.3   50.9   56.5   22.4   48.8   0.3   0.3   0.3Aya Vision-32BWinLossTie6 Results and Discussion

6.1 Multilingual Multimodal Open-Ended Performance

Aya-Vision-8B achieves best-in-class performance in preference evaluation. Figure 6
shows pairwise win-rates on AyaVisionBench and m-WildVision, averaged over 23 languages for Aya-
Vision-8B against the other state-of-the-art multimodal LLMs. Overall, Aya-Vision-8B achieves the
best-in-class performance, outperforming all the models by win-rate, ranging from 49.6% to 80.3%.
We find that Aya-Vision-8B achieves slightly higher win-rates on m-WildVision compared to AyaV-
isionBench – 6% on average, potentially due to the challenging characteristic of AyaVisionBench –
higher tie rates also indicate failure cases for both models in the comparison. Aya-Vision-8B outper-
forms both Qwen-2.5-VL-7B and Pixtral-12B by 54.8% win-rate averaged across the two datasets,
even though Pixtral-12B is a larger model. Additionally, Aya-Vision-8B also outperforms strong
proprietary models like Gemini-Flash1.5-8B with a win-rate of 60.3% on average. Notably, Aya-
Vision-8B outperforms Pangea-7B by a significant margin (71.7% win-rate) even though Pangea
includes a large proportion of multilingual data in its training.

Aya-Vision-8B also outperforms Pangea-7B across all 23 languages – ranging from 56% in English
to 83.6% in Greek. Given that the “curse of multilinguality" leads to drop in per-language perfor-
mance as the number of languages covered increases, Aya-Vision-8B is still extremely competitive
with Molmo-7B (specifically optimized for English) with a win-rate of 48.3% in English while out-
performing it over the other 22 languages with an average win-rate of 80%.

Finally, in addition to AyaVisionBench and m-WildVision, Aya-Vision-8B outperforms all models
in the same parameter class on xChatBench as shown in Table 4. Notably, Aya-Vision-8B not only
achieves a significant margin against models like Pangea-7B, Molmo-7B-D, and Llama-3.2-11B, but
also outperforms much larger models such as Molmo-72B and Llama-3.2-90B by 28.5% and 14.7%
relative increase, validating its strong conversational ability.

Aya Vision outperforms far larger models. While scaling model size has demonstrated tan-
gible gains in model performance [Kaplan et al., 2020]; complementing this with careful data and
model optimization techniques yields significant efficiency gains. Such optimizations improve the
underlying scaling dynamics, reducing the parameter count needed for equivalent performance
[Hooker, 2024]. Figure 7 shows pairwise win-rates averaged over 23 languages for Aya-Vision-32B on
AyaVisionBench and m-WildVision. Across both AyaVisionBench and m-WildVision, Aya-Vision-
32B consistently outperforms models over 2× larger, such as Molmo-72B, Qwen-2.5-VL-72B, and
Llama-3.2-90B-Vision by win-rates ranging from 48.5% to 73%. Notably, Aya-Vision-32B outper-
forms Llama-3.2-90B-Vision on AyaVisionBench and m-WildVision by 65.9% and 73% win-rates,
respectively. The closest competitor to Aya-Vision-32B is Qwen-2.5-VL-72B, where Aya-Vision-32B
outperforms Qwen-2.5-VL-72B by 50.8% win-rate on average across both datasets. This showcases
our critical focus on efficiency by achieving more using less compute. This also enables greater
support for the research community, who often have more limited access to compute resources.

6.2 Multilingual Multimodal Academic Benchmarks

Aya Vision models achieve competitive performance in multiple-choice or short-form
academic benchmarks. Aya Vision models are optimized for open-ended real-world usage rather

19

than academic benchmarks featuring multiple-choice or short-form answers. These benchmarks,
typically designed as visual question answering tasks, tend to prioritize constrained, static evaluation
formats and often fail to capture the full generative capabilities of modern MLLMs. As noted in
prior work [Muennighoff et al., 2022; Agrawal et al., 2024; Deitke et al., 2024; Üstün et al., 2024],
performance on such benchmarks correlates weakly with real-world open-ended tasks. Nonetheless,
Aya Vision models demonstrate strong performance across these evaluations. Results are reported
in Table 4.

Notably, on MaxM, a short-form VQA benchmark, Aya-Vision-8B outperforms all models in its
parameter class, including larger ones like Pixtral-12B and LLaMA-3.2-11B-Vision. Similarly, on
Kaleidoscope, it performs competitively with Qwen-2.5-VL-7B and surpasses all other baselines.

Finally, our 32B model Aya Vision model exhibits competitive performance on academic benchmarks
against models more than 2× its size. Aya-Vision-32B outperforms Molmo-72B on all benchmarks
except xMMMU, and closely matches Llama-3.2-90B-Vision, despite being nearly 3× smaller.

6.3 Text-Only Performance

Aya Vision models punch above their size in text-only preference evaluation. A key
concern with multimodal models is that introducing vision can degrade existing text performance.
Hence, we evaluate the final overall performance in text performance. Figure 8 shows win-rates for
Aya Vision models against the baselines on m-ArenaHard dataset, averaged over 23 languages. At
8B parameter scale, Aya-Vision-8B outperforms all the models except Gemini-Flash1.5-8B, which
is a proprietary model. Compared to models that are larger than ours, while Aya-Vision-8B beats
Llama-3.2-11B-Vision with a 63.4% win-rate, it is outperformed by Pixtral-12B with 44.0% win-rate.
For the larger model comparison, Aya-Vision-32B outperforms Molmo-72B and Qwen-2.5-VL-72B
by win-rates of 77.3% and 50.9% respectively. Our 32B model is competitive with Llama-3.2-90B-
Vision with a 43.2% win-rate. Considered together with superior multimodal win-rates (Figure 6 &
Figure 7), these results show the relative preservation in text performance while adding best-in-class
multimodal abilities.

Aya Vision recovers open-ended text-only performance in a significantly higher degree
than the baselines. As an additional perspective on text-only performance, Figure 5 compares the
text-only win-rates on mArenaHard for Aya-Vision-8B, Pangea-7B, Qwen-2.5-7B, and Molmo-7B
compared to the LLMs they were initialized from. Here, Aya-Vision-8B with cross-modal merg-
ing makes significant strides towards much closer performance to the initial LLM – limiting the
degradation to within 5.9%. This degradation, however, is significantly higher in the other models
evaluated, 16.4% for Pangea, 22.1% for Qwen-2.5, and 44.1% for Molmo compared to their initial
LLMs. These results highlight the benefits of our cross-modal merging framework.

It is easier to recover text-only performance in academic benchmarks compared to
open-ended evaluation. As we show in § 3, maintaining the base LLM’s text-only performance
in academic benchmarks is much easier than preference evaluation due to the nature of these bench-
marks. Hence, the performance of similar-sized models is closer in these benchmarks. At 8B
parameter scale, Aya-Vision-8B achieves the best average performance across text-only benchmarks
of 64.41%, where it outperforms all models in FLORES (En→X, 23 languages) and reaches the
second-best performance in both MGSM and IFEval, after Pixtral-12B and Llama-3.2-11B-Vision

20

Figure 9: Impact of cross-modal merging across various merge ratios. Multimodal and text
win-rates are calculated against Pangea-7B on AyaVisionBench and m-ArenaHard respectively over
7 languages. Multimodal academic benchmark is an average of CVQA and xMMMU; Text-Only
academic benchmarks are averaged over IFEval, MGSM and MMMLU (subset).

respectively. Notably, both models are much larger than our 8B model. For Aya-Vision-32B, our
model achieves second-best performance for FLORES, but falls behind other models on other tasks.
We relate this to the original performance of base LLMs in these benchmarks, where recovery is
relatively straightforward. It is important to note that the models compared to Aya-Vision-32B are
over 2× its size (72B and 90B models). Overall, we observe that both multimodal and text-only
academic benchmark results have poor alignment with their open-ended generation counterparts;
as demonstrated in prior works [Muennighoff et al., 2022; Üstün et al., 2024] due to their rigid
metrics emphasizing precise format compliance at the expense of semantic correctness and quality
of generations.

7 Key Ablations and Discussion

To isolate the impact of our design choices, we perform a set of controlled ablations focusing on –
(1) cross-modal model merging, (2) comparison with the addition of text-only data, (3) multilingual
data percentage during SFT, (4) the vision encoder, and (5) comparison of full model fine-tuning
with low-rank adaptation, all at the 8B parameter scale. In each of these ablations, we only vary a
single variable of interest, while keeping the rest of the experimental setup fixed. To evaluate each
ablation, we use multimodal win-rates on AyaVisionBench and text win-rates on mArena-Hard using
a subset of languages17 against Pangea-7B. In addition, we also report scores on various academic
benchmarks based on the ablation.

7.1 Model Merging Improves Multilingual Performance Across Tasks and

Modalities

To understand the impact of our cross-modal model merging as the merging ratio changes, we ablate
the interpolation weight α in Equation (1) for the multimodal LLM, and evaluate the resulting
merged multimodal LLMs. An α of 0 corresponds to purely the text-only model whereas an α
In addition to the win-rates for
of 1 corresponds to just the post-multimodal training model.
both multimodal and text-only, we report the average of CVQA and xMMMU for academic vision

17English, French, Hindi, Arabic, Turkish, Japanese, Chinese

21

0.30.40.50.60.70.80.91.0Multimodal Merge Fraction505560657075Win Rate (%)Win RatesMultimodalText0.30.40.50.60.70.80.91.0Multimodal Merge Fraction0.500.550.600.650.70Average AccuracyAcademic Benchmark ScoresMultimodalText-onlybenchmarks and IFEval, MMMLU (subset), and MGSM for text-only academic benchmarks.

While our original motivation for model merging was retention of performance on text-only multi-
lingual benchmarks, Figure 9 (left) shows that our novel cross-modal merging recipe additionally
boosts multilingual vision win-rates as the interpolation weight for text-only model increases. Be-
low 0.6 multimodal interpolation weight, the text-only win-rates keep climbing; however, the vision
win-rates saturate. For academic benchmarks, we again observe a similar trend – as the ratio of
the text-only model increases, text-only benchmarks rapidly increase until 0.5, following which the
gains are minimal. Interestingly, even academic multimodal benchmarks see a minor gain due to
model merging. Based on these results, we chose 0.4 as the merging ratio for both our 8B and 32B
models.

7.2 Model merging is more effective than adding seen text data for cross-modal

transfer

An alternate approach to recover performance on text-only tasks is to include a certain percentage
of text-only data in the training mixture. To understand the role of text-only data on multimodal
and text-only win-rates and specifically compare it with our cross-modal merging approach, we
train 3 variants with varying proportions of text data – 0%, 10%, and 30%. For the variants with
text-data added, we evaluate the final checkpoints without merging, and compare with the model
where our merging recipe is applied on the variant with 0% text-data. Figure 10 shows the results
of these experiments.

While increasing the amount of text-
only data improves the quality of gen-
erations for textual prompts as indi-
cated by win-rates going from 50.2%
to 74.8%; these gains do not trans-
late to multimodal prompts. In fact,
as seen in Figure 10 these win-rates
are substantially lower than those ob-
tained by training on purely multi-
modal data followed by merging with
a weight of 0.4. Additionally, increas-
ing the amount of text data added
from 10% to 30% leads to a slight
decrease in the multimodal win-rates
due to increasing share of model ca-
pacity being used for text-only mod-
eling. This highlights the simplic-
ity and efficacy of our model merging
framework at cross-modal transfer of
capabilities.

Figure 10: Modal merging is an efficient way to enable
cross-modal transfer. Multimodal and text-only win-
rates on AyaVisionBench and m-ArenaHard against Pangea-
7B. We increase the amount of text-only mixture in SFT and
compare to cross-modal merging (dashed line).

22

0%10%30%Text-Only Data (%)4050607080Win Rate (%)Multimodal Win Rates51.6%55.7%54.4%MultimodalCross-Modal Merging0%10%30%Text-Only Data (%)Text Win Rates50.2%74.3%75.8%TextCross-Modal MergingFigure 11: A balanced data mixture is essential for multilingual multimodal perfor-
mance. Multimodal and text win-rates are calculated against Pangea-7B on AyaVisionBench
and m-ArenaHard respectively over 7 languages. Multimodal academic benchmark is an average
of CVQA and xMMMU; Text-Only academic benchmarks are averaged over IFEval, MGSM and
MMMLU (subset).

7.3 Data Improvements has the Highest Impact on the Quality of Generations

Our data generation framework has a strong em-
phasis on the quality but can we quantify the
importance of the data improvement process?
To answer this question, we train 2 variants –
(1) with only existing open-source data, (2) with
the data mixture proposed in § 3 – holding the
amount of data and iterations during training
fixed; and measure the multimodal win-rates.
Please note that no merging is performed here
to allow for a cleaner comparison. Figure 12
shows the impact of synthetic annotations on
the win-rates. Compared to variant (1) trained
purely on original task-specific data, our data
improvements lead to the largest jump in win-
rates – 17% amongst our various interventions.
This underscores the importance of fluent, detailed and diverse completions in the training data
mixture towards building a strong conversational multimodal model. Additionally, when paired
with cross-modal merging the total improvement increases to nearly 30%.

Figure 12: Impact of various interventions.
Step-by-step improvements in Aya Vision 8B’s
pairwise win-rates against Pangea-7B.

7.4 A Balanced Data Mixture is Essential for Multilingual Multimodal

Performance

An important question in building a multilingual multimodal model is – What is the right ratio of
multilingual data in the training mixture?

To answer this question, we train 3 variants with varying proportions of multilingual multimodal
data – 17.5%, 35%, and 67%, which is uniformly distributed across 22 languages (except English).
We compare these variants using preference evaluation (win-rates), and a subset of multimodal and

23

17.535.067.0Multilingual Data (%)69.069.570.070.571.0Win Rate (%)Win RatesMultimodalText17.535.067.0Multilingual Data (%)525456586062Average AccuracyAcademic Benchmark ScoresMultimodalTextAya Vision8B Base+SFT withData Improvements+Merging+ModelScale0102030405060708090Multilingual Vision Win Rate40.9%58.1%70.0%79.1%+17.2%+11.9%+9.1%text-only academic benchmarks. Note that we merge each trained checkpoint with the text-only
model with the same interpolation factor (α) to make it consistent with our final recipe. Figure 11
shows the results.

Balanced multilingual data leverages cross-lingual transfer from English for best perfor-
mance across modalities and languages. We observe that increasing the ratio of multilingual
multimodal data from 35% to 67% leads to degradation in the quality of generations – reducing the
win-rates from 71.4% to 68.7%, and also hurts multimodal academic benchmarks, emphasizing the
importance of the balance between English and multilingual data. Given the scarcity of high-quality
multilingual multimodal data, upsampling this bucket requires repeating the data multiple times,
limiting its benefit in multilingual multimodal performance. Additionally, a sufficient percentage of
the more diverse English data is crucial for cross-lingual transfer. Therefore, we use 35% of mul-
tilingual data in our final recipe, leaving 65% for a diverse set of English datasets, which includes
selected original datasets (34%), and a high-quality synthetically re-annotated dataset (31%) as
presented in Section 3.

7.5 Low Rank Finetuning is Comparable to Full Finetuning

Low-rank training (LoRA) is an extremely per-
formant method to reduce the hardware foot-
print during training for improved efficiency.
LoRA drastically reduces the number of train-
able parameters and optimizer states to be
stored in the accelerator memory [Zadouri et al.,
2023]. Furthermore, freezing the LLM and con-
straining the rank of updates has the potential
to prevent catastrophic forgetting on text-only
prompts. To understand the impact of the rank
of training updates during the SFT stage, we
train 2 variants on the same data – (1) trained
with LoRA (rank = 256, α = 512) [Hu et al.,
2022] while (2) is trained with full finetuning (all
network weights are updated). Once both the
models are trained, we merge the multimodal
updates to the text-only language model with
a weight (α) of 0.5. Finally, we evaluate both
variants on multimodal and text win-rates; and
academic benchmarks like CVQA and xMMMU. Figure 13 shows the results on all the above tasks.

Figure 13: Impact of training with LoRA vs.
Full-Finetuning. We compare vision win-rates
(left) and text-only win-rates (center) against
Pangea-7B averaged across 7 languages. We also
report the average of CVQA and xMMMU (right).

On academic tasks like CVQA and xMMMU, we observe that both variants perform equally well,
51.2 vs 51.0 average accuracy for LoRA and full model fine-tuning, respectively. On multimodal
win-rate evaluations, both models are extremely close – with 68.4% and 67.2% win-rates for the
LoRA and fully-finetuned variants respectively. Any improvement exhibited by the LoRA variant
on win-rates is well within the noise-margin. On text-only win-rates, the LoRA variant is 3.4%
better than full-finetuning which can be attributed to the frozen LLM backbone during training
and the amenability of LoRA model to merging due to the shared optimization trajectory.

24

MultimodalText-OnlyAcademicBenchmarks0102030405060708090Win Rate / Accuracy (%)68.4%76.2%51.2%67.2%72.8%51.0%LoRA + 0.5 MergeFull Finetuning + 0.5 Merge8 Related Work

Visual Instruction Tuning Visual instruction tuning [Liu et al., 2023c; Chen et al., 2023; Liu
et al., 2024; Chen et al., 2024; Agrawal et al., 2024; Wang et al., 2024b; Deitke et al., 2024; Bai et al.,
2025] combines a pre-trained vision encoder [Radford et al., 2021; Zhai et al., 2023; Chen et al., 2024;
Tschannen et al., 2025] with an off-the-shelf large language model via a dedicated vision–language
connector. This process extends the LLM’s text capabilities into the visual domain while retaining
its desirable attributes– such as in-context learning, reasoning, and instruction following. As a
result, visual instruction tuning has emerged as a highly effective method to achieve state-of-the-art
performance on a wide range of tasks – even outperforming certain proprietary models.

Multilingual Multimodal Models Initial works on multilingual multimodal models [Ni et al.,
2021; Jain et al., 2021; Zeng et al., 2023] focused on learning robust, universal representations for
retrieval tasks across modalities. However, these models require further downstream training to
be used as generative models. On the other hand, [Geigle et al., 2023; Chen et al., 2023; Yue
et al., 2024b] perform large-scale multilingual multi-task fine-tuning to enable multilingual under-
standing and generation. However, they focus only on vision-language academic benchmarks which
are reference based – focusing on exact matches rather than free-form holistic evaluations of the
generations.

Multilingual Multimodal Evaluations Multilingual multimodal evaluation benchmarks have
traditionally focused on visual question answering (VQA) tasks, where the model-generated re-
sponse must exactly match a human-provided reference answer [Changpinyo et al., 2022; Romero
et al., 2024; Tang et al., 2024]. This approach often penalizes responses that are semantically correct
but differ syntactically from the reference [Agrawal et al., 2024]. To address these limitations, recent
work [Yue et al., 2024b; Maaz et al., 2024] has proposed multilingual multimodal chat benchmarks.
Instead of relying solely on exact matches, these benchmarks evaluate free-form responses by em-
ploying a Vision-Language model as an adjudicator–either by scoring responses against a detailed
rubric or by selecting the superior generation from a pair of outputs.

Multimodal Merging Recent work by Zhu et al. [2025] introduces REMEDY, a method for
merging VLM weights – including the connector layer – after low-rank fine-tuning on various VLM
tasks. However, REMEDY does not address the merging of weights that have been trained for
different modalities. In a closely related concurrent work, Li et al. [2025] merge a text-only reward
model with a vision-language model with the goal to specifically transfer the reward modeling
capabilities from the text-based reward model to build a multimodal reward model.

9 Conclusion

In this work, we introduced Aya Vision, a family of multilingual vision-language models (8B and
32B) designed to improve multimodal understanding across 23 languages. Addressing key challenges
in this space, we propose a scalable synthetic annotation framework to overcome multilingual data
scarcity, and a training-free model merging approach to preserve text-only performance during
multimodal training. Our models outperform existing open-weight baselines and are supported by
AyaVisionBench, a benchmark tailored for evaluating generative multilingual multimodal systems.
By releasing our models and evaluation suite, we aim to lower barriers for research in this area and
support continued progress toward more inclusive and linguistically diverse multimodal AI.

25

10 Acknowledgements

Thank you to all our colleagues across Cohere who jumped in to help test Aya Vision in their
language: Ivan Zhang, Irem Ergün, Eddie Kim, Hemant Jain, Wei-Yin Ko, Adrian Morisot, Rod
Hajjar, Gokce Keskin, Trushant Kalyanpur, Julia Kreutzer, Olivia Lasche, Dennis Aumiller, Fe-
lipe Cruz Salinas, Alice Schoenauer Sebag, Dwarak Talupuru, Diana Abagyan, Ammar Khairi,
Huey Sun, Varun Kumethi, Viraat Aryabumi, Sungjin Hong, Trent Fowlers, Lidiya Murakhovska,
Aidan Peppin, Jay Alammar, Samuel Cahyawijaya, Brittawnya Prince, Daniel D’souza and Vivek
Muppalla.

And to the members of our Open Science Community who shared their expertise and insights:
Ahmad Anis, Amir Nuriyev, Bronson Bakunga„ Daniel Laurin, Danylo Boiko, David Cairuz, Dina
Kliuchareva, Dominik Krzemiński, Erika Watanabe, Fernanda Guerriero Antunes, Gimei Alex, Jie
Gao, Joana da Matta, Joseph Pollack, Karthik Kanjula, Kenny Rebelo, Kentaro Kojima, Kian
Kyers, Lana Ludmila, Leticia Mie Otani, Louisa Chang, Marek Suppa, Mayuko Koizumi, Mei E.,
Mei Hirata, Micol Altomare, Nicole Mak, Ning Sun, Rami Rao, Reuben Fernandes, Reza Rob,
Selina Tong, Shayekh Bin Islam, Shirley Au, Silvia Fernandez, Sree Harsha Nelaturu, Tai Guratti,
Teresa Shiho Waddell, Thiago Correia, Xuelong An Wang, and Yanny Li.

The authors would also like to thank Fraser Greenlee for his contributions during the early stages
of this project.

References

Aakanksha, Arash Ahmadian, Seraphina Goldfarb-Tarrant, Beyza Ermis, Marzieh Fadaee, and
Sara Hooker. Mix data or merge models? optimizing for diverse multi-task learning, 2024a. URL
https://arxiv.org/abs/2410.10801.

Arash Aakanksha, Ahmadian, Beyza Ermis, Seraphina Goldfarb-Tarrant, Julia Kreutzer, Marzieh
Fadaee, Sara Hooker, et al. The multilingual alignment prism: Aligning global and local prefer-
ences to reduce harm. arXiv preprint arXiv:2406.18682, 2024b.

Manoj Acharya, Kushal Kafle, and Christopher Kanan. Tallyqa: Answering complex counting

questions. In AAAI, 2019.

Pravesh Agrawal, Szymon Antoniak, Emma Bou Hanna, Baptiste Bout, Devendra Chaplot, Jessica
Chudnovsky, Diogo Costa, Baudouin De Monicault, Saurabh Garg, Theophile Gervet, et al.
Pixtral 12b. arXiv preprint arXiv:2410.07073, 2024.

Anthropic. Claude 3.7 sonnet system card. https://assets.anthropic.com/m/785e231869ea8b3
b/original/claude-3-7-sonnet-system-card.pdf, February 2025. Accessed: 2025-04-17.

Viraat Aryabumi, John Dang, Dwarak Talupuru, Saurabh Dash, David Cairuz, Hangyu Lin, Bharat
Venkitesh, Madeline Smith, Jon Ander Campos, Yi Chern Tan, Kelly Marchisio, Max Bartolo, Se-
bastian Ruder, Acyr Locatelli, Julia Kreutzer, Nick Frosst, Aidan Gomez, Phil Blunsom, Marzieh
Fadaee, Ahmet Üstün, and Sara Hooker. Aya 23: Open weight releases to further multilingual
progress, 2024a. URL https://arxiv.org/abs/2405.15032.

Viraat Aryabumi, John Dang, Dwarak Talupuru, Saurabh Dash, David Cairuz, Hangyu Lin, Bharat

26

Venkitesh, Madeline Smith, Jon Ander Campos, Yi Chern Tan, et al. Aya 23: Open weight releases
to further multilingual progress. arXiv preprint arXiv:2405.15032, 2024b.

Jinze Bai, Shuai Bai, Shusheng Yang, Shijie Wang, Sinan Tan, Peng Wang, Junyang Lin, Chang
Zhou, and Jingren Zhou. Qwen-vl: A versatile vision-language model for understanding, local-
ization, text reading, and beyond. arXiv preprint arXiv:2308.12966, 2023.

Shuai Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, Sibo Song, Kai Dang, Peng Wang,
Shijie Wang, Jun Tang, Humen Zhong, Yuanzhi Zhu, Mingkun Yang, Zhaohai Li, Jianqiang Wan,
Pengfei Wang, Wei Ding, Zheren Fu, Yiheng Xu, Jiabo Ye, Xi Zhang, Tianbao Xie, Zesen Cheng,
Hang Zhang, Zhibo Yang, Haiyang Xu, and Junyang Lin. Qwen2.5-vl technical report, 2025.
URL https://arxiv.org/abs/2502.13923.

Assaf Ben-Kish, Moran Yanuka, Morris Alper, Raja Giryes, and Hadar Averbuch-Elor.
arXiv preprint

Mocha: Multi-objective reinforcement mitigating caption hallucinations.
arXiv:2312.03631, 2, 2023.

Lucas Beyer, Andreas Steiner, André Susano Pinto, Alexander Kolesnikov, Xiao Wang, Daniel
Salz, Maxim Neumann, Ibrahim Alabdulmohsin, Michael Tschannen, Emanuele Bugliarello, et al.
Paligemma: A versatile 3b vlm for transfer. arXiv preprint arXiv:2407.07726, 2024.

Ali Furkan Biten, Rubèn Tito, Andrés Mafla, Lluis Gomez, Marçal Rusiñol, C.V. Jawahar, Ernest
Valveny, and Dimosthenis Karatzas. Scene text visual question answering. In 2019 IEEE/CVF
International Conference on Computer Vision (ICCV), pp. 4290–4300, 2019. doi: 10.1109/ICCV
.2019.00439.

Yuri Bizzoni, Tom S Juzek, Cristina España-Bonet, Koel Dutta Chowdhury, Josef van Genabith,
and Elke Teich. How human is machine translationese? comparing human and machine transla-
tions of text and speech. In Proceedings of the 17th International conference on spoken language
translation, pp. 280–290, 2020.

Soravit Changpinyo, Linting Xue, Michal Yarom, Ashish V Thapliyal, Idan Szpektor, Julien Amelot,
Xi Chen, and Radu Soricut. Maxm: Towards multilingual visual question answering. arXiv
preprint arXiv:2209.05401, 2022.

Xi Chen, Josip Djolonga, Piotr Padlewski, Basil Mustafa, Soravit Changpinyo, Jialin Wu, Car-
los Riquelme Ruiz, Sebastian Goodman, Xiao Wang, Yi Tay, et al. Pali-x: On scaling up a
multilingual vision and language model. arXiv preprint arXiv:2305.18565, 2023.

Zhe Chen, Weiyun Wang, Hao Tian, Shenglong Ye, Zhangwei Gao, Erfei Cui, Wenwen Tong,
Kongzhi Hu, Jiapeng Luo, Zheng Ma, et al. How far are we to gpt-4v? closing the gap to
commercial multimodal models with open-source suites. Science China Information Sciences, 67
(12):220101, 2024.

Zhiyu Chen, Wenhu Chen, Charese Smiley, Sameena Shah, Iana Borova, Dylan Langdon, Reema
Moussa, Matt Beane, Ting-Hao Huang, Bryan Routledge, et al. Finqa: A dataset of numerical
reasoning over financial data. arXiv preprint arXiv:2109.00122, 2021.

Team Cohere, Aakanksha, Arash Ahmadian, Marwan Ahmed, Jay Alammar, Yazeed Alnumay,
Sophia Althammer, Arkady Arkhangorodsky, Viraat Aryabumi, Dennis Aumiller, Raphaël Ava-
los, Zahara Aviv, Sammie Bae, Saurabh Baji, Alexandre Barbet, Max Bartolo, Björn Bebensee,
Neeral Beladia, Walter Beller-Morales, Alexandre Bérard, Andrew Berneshawi, Anna Bialas,

27

Phil Blunsom, Matt Bobkin, Adi Bongale, Sam Braun, Maxime Brunet, Samuel Cahyawijaya,
David Cairuz, Jon Ander Campos, Cassie Cao, Kris Cao, Roman Castagné, Julián Cendrero,
Leila Chan Currie, Yash Chandak, Diane Chang, Giannis Chatziveroglou, Hongyu Chen, Claire
Cheng, Alexis Chevalier, Justin T. Chiu, Eugene Cho, Eugene Choi, Eujeong Choi, Tim Chung,
Volkan Cirik, Ana Cismaru, Pierre Clavier, Henry Conklin, Lucas Crawhall-Stein, Devon Crouse,
Andres Felipe Cruz-Salinas, Ben Cyrus, Daniel D’souza, Hugo Dalla-Torre, John Dang, William
Darling, Omar Darwiche Domingues, Saurabh Dash, Antoine Debugne, Théo Dehaze, Shaan
Desai, Joan Devassy, Rishit Dholakia, Kyle Duffy, Ali Edalati, Ace Eldeib, Abdullah Elkady,
Sarah Elsharkawy, Irem Ergün, Beyza Ermis, Marzieh Fadaee, Boyu Fan, Lucas Fayoux, Yan-
nis Flet-Berliac, Nick Frosst, Matthias Gallé, Wojciech Galuba, Utsav Garg, Matthieu Geist,
Mohammad Gheshlaghi Azar, Seraphina Goldfarb-Tarrant, Tomas Goldsack, Aidan Gomez, Vic-
tor Machado Gonzaga, Nithya Govindarajan, Manoj Govindassamy, Nathan Grinsztajn, Nikolas
Gritsch, Patrick Gu, Shangmin Guo, Kilian Haefeli, Rod Hajjar, Tim Hawes, Jingyi He, Sebas-
tian Hofstätter, Sungjin Hong, Sara Hooker, Tom Hosking, Stephanie Howe, Eric Hu, Renjie
Huang, Hemant Jain, Ritika Jain, Nick Jakobi, Madeline Jenkins, JJ Jordan, Dhruti Joshi, Ja-
son Jung, Trushant Kalyanpur, Siddhartha Rao Kamalakara, Julia Kedrzycki, Gokce Keskin,
Edward Kim, Joon Kim, Wei-Yin Ko, Tom Kocmi, Michael Kozakov, Wojciech Kryściński, Ar-
nav Kumar Jain, Komal Kumar Teru, Sander Land, Michael Lasby, Olivia Lasche, Justin Lee,
Patrick Lewis, Jeffrey Li, Jonathan Li, Hangyu Lin, Acyr Locatelli, Kevin Luong, Raymond Ma,
Lukas Mach, Marina Machado, Joanne Magbitang, Brenda Malacara Lopez, Aryan Mann, Kelly
Marchisio, Olivia Markham, Alexandre Matton, Alex McKinney, Dominic McLoughlin, Jozef
Mokry, Adrien Morisot, Autumn Moulder, Harry Moynehan, Maximilian Mozes, Vivek Muppalla,
Lidiya Murakhovska, Hemangani Nagarajan, Alekhya Nandula, Hisham Nasir, Shauna Nehra,
Josh Netto-Rosen, Daniel Ohashi, James Owers-Bardsley, Jason Ozuzu, Dennis Padilla, Gloria
Park, Sam Passaglia, Jeremy Pekmez, Laura Penstone, Aleksandra Piktus, Case Ploeg, Andrew
Poulton, Youran Qi, Shubha Raghvendra, Miguel Ramos, Ekagra Ranjan, Pierre Richemond, Cé-
cile Robert-Michon, Aurélien Rodriguez, Sudip Roy, Laura Ruis, Louise Rust, Anubhav Sachan,
Alejandro Salamanca, Kailash Karthik Saravanakumar, Isha Satyakam, Alice Schoenauer Sebag,
Priyanka Sen, Sholeh Sepehri, Preethi Seshadri, Ye Shen, Tom Sherborne, Sylvie Chang Shi,
Sanal Shivaprasad, Vladyslav Shmyhlo, Anirudh Shrinivason, Inna Shteinbuk, Amir Shukayev,
Mathieu Simard, Ella Snyder, Ava Spataru, Victoria Spooner, Trisha Starostina, Florian Strub,
Yixuan Su, Jimin Sun, Dwarak Talupuru, Eugene Tarassov, Elena Tommasone, Jennifer Tracey,
Billy Trend, Evren Tumer, Ahmet Üstün, Bharat Venkitesh, David Venuto, Pat Verga, Maxime
Voisin, Alex Wang, Donglu Wang, Shijian Wang, Edmond Wen, Naomi White, Jesse Willman,
Marysia Winkels, Chen Xia, Jessica Xie, Minjie Xu, Bowen Yang, Tan Yi-Chern, Ivan Zhang,
Zhenyu Zhao, and Zhoujie Zhao. Command a: An enterprise-ready large language model, 2025.
URL https://arxiv.org/abs/2504.00698.

Marta R Costa-Jussà, James Cross, Onur Çelebi, Maha Elbayad, Kenneth Heafield, Kevin Heffer-
nan, Elahe Kalbassi, Janice Lam, Daniel Licht, Jean Maillard, et al. No language left behind:
Scaling human-centered machine translation. arXiv preprint arXiv:2207.04672, 2022.

Wenliang Dai, Nayeon Lee, Boxin Wang, Zhuolin Yang, Zihan Liu, Jon Barker, Tuomas Rintamaki,
Mohammad Shoeybi, Bryan Catanzaro, and Wei Ping. Nvlm: Open frontier-class multimodal
llms. arXiv preprint arXiv:2409.11402, 2024.

John Dang, Shivalika Singh, Daniel D’souza, Arash Ahmadian, Alejandro Salamanca, Made-
line Smith, Aidan Peppin, Sungjin Hong, Manoj Govindassamy, Terrence Zhao, et al. Aya

28

expanse: Combining research breakthroughs for a new multilingual frontier. arXiv preprint
arXiv:2412.04261, 2024.

Matt Deitke, Christopher Clark, Sangho Lee, Rohun Tripathi, Yue Yang, Jae Sung Park, Moham-
madreza Salehi, Niklas Muennighoff, Kyle Lo, Luca Soldaini, et al. Molmo and pixmo: Open
weights and open data for state-of-the-art multimodal models. arXiv preprint arXiv:2409.17146,
2024.

Yihao Ding, Siwen Luo, Hyunsuk Chung, and Soyeon Caren Han. Vqa: A new dataset for real-
world vqa on pdf documents. In Joint European Conference on Machine Learning and Knowledge
Discovery in Databases, pp. 585–601. Springer, 2023.

Beyza Ermis, Luiza Pozzobon, Sara Hooker, and Patrick Lewis. From one to many: Expand-
ing the scope of toxicity mitigation in language models. In Lun-Wei Ku, Andre Martins, and
Vivek Srikumar (eds.), Findings of the Association for Computational Linguistics: ACL 2024,
pp. 15041–15058, Bangkok, Thailand, August 2024. Association for Computational Linguistics.
doi: 10.18653/v1/2024.findings-acl.893. URL https://aclanthology.org/2024.findings-acl
.893/.

Yunhao Fang, Ligeng Zhu, Yao Lu, Yan Wang, Pavlo Molchanov, Jan Kautz, Jang Hyun Cho,
Marco Pavone, Song Han, and Hongxu Yin. Vila2: Vila augmented vila, 2024. URL https:
//arxiv.org/abs/2407.17453.

Jonathan Frankle, Gintare Karolina Dziugaite, Daniel Roy, and Michael Carbin. Linear mode
connectivity and the lottery ticket hypothesis. In International Conference on Machine Learning,
pp. 3259–3269. PMLR, 2020.

Samir Yitzhak Gadre, Gabriel Ilharco, Alex Fang, Jonathan Hayase, Georgios Smyrnis, Thao
Nguyen, Ryan Marten, Mitchell Wortsman, Dhruba Ghosh, Jieyu Zhang, et al. Datacomp: In
search of the next generation of multimodal datasets. Advances in Neural Information Processing
Systems, 36:27092–27112, 2023.

Gregor Geigle, Abhay Jain, Radu Timofte, and Goran Glavaš. mblip: Efficient bootstrapping of

multilingual vision-llms. arXiv preprint arXiv:2307.06930, 2023.

Charles Goddard, Shamane Siriwardhana, Malikeh Ehghaghi, Luke Meyers, Vladimir Karpukhin,
Brian Benedict, Mark McQuade, and Jacob Solawetz. Arcee’s mergekit: A toolkit for merging
large language models. In Proceedings of the 2024 Conference on Empirical Methods in Natural
Language Processing: Industry Track, pp. 477–485, 2024.

Yash Goyal, Tejas Khot, Douglas Summers-Stay, Dhruv Batra, and Devi Parikh. Making the v in
vqa matter: Elevating the role of image understanding in visual question answering. In Proceedings
of the IEEE conference on computer vision and pattern recognition, pp. 6904–6913, 2017.

Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad
Al-Dahle, Aiesha Letman, Akhil Mathur, Alan Schelten, Alex Vaughan, et al. The llama 3 herd
of models. arXiv preprint arXiv:2407.21783, 2024.

Anisha Gunjal, Jihan Yin, and Erhan Bas. Detecting and preventing hallucinations in large vision

language models. arXiv preprint arXiv:2308.06394, 2023.

29

Jarvis Guo, Tuney Zheng, Yuelin Bai, Bo Li, Yubo Wang, King Zhu, Yizhi Li, Graham Neubig,
Wenhu Chen, and Xiang Yue. Mammoth-vl: Eliciting multimodal reasoning with instruction
tuning at scale. arXiv preprint arXiv:2412.05237, 2024.

Francisco Guzmán, Peng-Jen Chen, Myle Ott, Juan Pino, Guillaume Lample, Philipp Koehn,
Vishrav Chaudhary, and Marc’Aurelio Ranzato. The flores evaluation datasets for low-resource
machine translation: Nepali-english and sinhala-english. arXiv preprint arXiv:1902.01382, 2019.

Kai Hartung, Aaricia Herygers, Shubham Vijay Kurlekar, Khabbab Zakaria, Taylan Volkan, Sören
Gröttrup, and Munir Georges. Measuring sentiment bias in machine translation. In International
Conference on Text, Speech, and Dialogue, pp. 82–93. Springer, 2023.

Amr Hendy, Mohamed Abdelrehim, Amr Sharaf, Vikas Raunak, Mohamed Gabr, Hitokazu Mat-
sushita, Young Jin Kim, Mohamed Afify, and Hany Hassan Awadalla. How good are gpt models
at machine translation? a comprehensive evaluation. arXiv preprint arXiv:2302.09210, 2023.

Sara Hooker. On the limitations of compute thresholds as a governance strategy, 2024. URL

https://arxiv.org/abs/2407.05694.

Yu-Chung Hsiao, Fedir Zubach, Gilles Baechler, Victor Carbune, Jason Lin, Maria Wang, Srinivas
Sunkara, Yun Zhu, and Jindong Chen. Screenqa: Large-scale question-answer pairs over mobile
app screenshots. arXiv preprint arXiv:2209.08199, 2022.

Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang,
Weizhu Chen, et al. Lora: Low-rank adaptation of large language models. ICLR, 1(2):3, 2022.

Gabriel Ilharco, Marco Tulio Ribeiro, Mitchell Wortsman, Suchin Gururangan, Ludwig Schmidt,
Hannaneh Hajishirzi, and Ali Farhadi. Editing models with task arithmetic. arXiv preprint
arXiv:2212.04089, 2022.

Pavel Izmailov, Dmitrii Podoprikhin, Timur Garipov, Dmitry Vetrov, and Andrew Gordon Wil-
arXiv preprint

son. Averaging weights leads to wider optima and better generalization.
arXiv:1803.05407, 2018.

Aashi Jain, Mandy Guo, Krishna Srinivasan, Ting Chen, Sneha Kudugunta, Chao Jia, Yinfei Yang,
and Jason Baldridge. Mural: multimodal, multitask retrieval across languages. arXiv preprint
arXiv:2109.05125, 2021.

Kushal Kafle, Brian Price, Scott Cohen, and Christopher Kanan. Dvqa: Understanding data
visualizations via question answering. In Proceedings of the IEEE conference on computer vision
and pattern recognition, pp. 5648–5656, 2018.

Samira Ebrahimi Kahou, Vincent Michalski, Adam Atkinson, Ákos Kádár, Adam Trischler, and
Yoshua Bengio. Figureqa: An annotated figure dataset for visual reasoning. arXiv preprint
arXiv:1710.07300, 2017.

Jared Kaplan, Sam McCandlish, Tom Henighan, Tom B Brown, Benjamin Chess, Rewon Child,
Scott Gray, Alec Radford, Jeffrey Wu, and Dario Amodei. Scaling laws for neural language
models. arXiv preprint arXiv:2001.08361, 2020.

Aniruddha Kembhavi, Mike Salvato, Eric Kolve, Minjoon Seo, Hannaneh Hajishirzi, and Ali
Farhadi. A diagram is worth a dozen images.
In Computer Vision–ECCV 2016: 14th Euro-
pean Conference, Amsterdam, The Netherlands, October 11–14, 2016, Proceedings, Part IV 14,
pp. 235–251. Springer, 2016.

30

Aniruddha Kembhavi, Minjoon Seo, Dustin Schwenk, Jonghyun Choi, Ali Farhadi, and Hannaneh
Hajishirzi. Are you smarter than a sixth grader? textbook question answering for multimodal
machine comprehension. In 2017 IEEE Conference on Computer Vision and Pattern Recognition
(CVPR), pp. 5376–5384, 2017. doi: 10.1109/CVPR.2017.571.

Ranjay Krishna, Yuke Zhu, Oliver Groth, Justin Johnson, Kenji Hata, Joshua Kravitz, Stephanie
Chen, Yannis Kalantidis, Li-Jia Li, David A Shamma, et al. Visual genome: Connecting language
and vision using crowdsourced dense image annotations. International journal of computer vision,
123:32–73, 2017.

Alina Kuznetsova, Hassan Rom, Neil Alldrin, Jasper Uijlings, Ivan Krasin, Jordi Pont-Tuset, Sha-
hab Kamali, Stefan Popov, Matteo Malloci, Alexander Kolesnikov, et al. The open images dataset
v4: Unified image classification, object detection, and visual relationship detection at scale. In-
ternational journal of computer vision, 128(7):1956–1981, 2020.

Nathan Lambert, Jacob Morrison, Valentina Pyatkin, Shengyi Huang, Hamish Ivison, Faeze Brah-
man, Lester James V Miranda, Alisa Liu, Nouha Dziri, Shane Lyu, et al. T\" ulu 3: Pushing
frontiers in open language model post-training. arXiv preprint arXiv:2411.15124, 2024.

Hugo Laurençon, Andrés Marafioti, Victor Sanh, and Léo Tronchon. Building and better under-
In Workshop on Responsibly

standing vision-language models:
Building the Next Generation of Multimodal Foundational Models, 2024a.

insights and future directions.

Hugo Laurençon, Léo Tronchon, Matthieu Cord, and Victor Sanh. What matters when building
vision-language models? Advances in Neural Information Processing Systems, 37:87874–87907,
2024b.

Bo Li, Yuanhan Zhang, Liangyu Chen, Jinghao Wang, Fanyi Pu, Jingkang Yang, Chunyuan Li, and
Ziwei Liu. Mimic-it: Multi-modal in-context instruction tuning. arXiv preprint arXiv:2306.05425,
2023a.

Chen-An Li, Tzu-Han Lin, Yun-Nung Chen, and Hung-yi Lee. Transferring textual preferences to
vision-language understanding through model merging. arXiv preprint arXiv:2502.13487, 2025.

Lei Li, Yuwei Yin, Shicheng Li, Liang Chen, Peiyi Wang, Shuhuai Ren, Mukai Li, Yazheng Yang,
Jingjing Xu, Xu Sun, et al. M3it: A large-scale dataset towards multi-modal multilingual in-
struction tuning. arXiv preprint arXiv:2306.04387, 2023b.

Tianle Li, Wei-Lin Chiang, Evan Frick, Lisa Dunlap, Tianhao Wu, Banghua Zhu, Joseph E Gon-
zalez, and Ion Stoica. From crowdsourced data to high-quality benchmarks: Arena-hard and
benchbuilder pipeline. arXiv preprint arXiv:2406.11939, 2024.

Yifan Li, Yifan Du, Kun Zhou, Jinpeng Wang, Wayne Xin Zhao, and Ji-Rong Wen. Evaluating
object hallucination in large vision-language models. arXiv preprint arXiv:2305.10355, 2023c.

Tsung-Yi Lin, Michael Maire, Serge Belongie, James Hays, Pietro Perona, Deva Ramanan, Piotr
Dollár, and C Lawrence Zitnick. Microsoft coco: Common objects in context. In Computer vision–
ECCV 2014: 13th European conference, zurich, Switzerland, September 6-12, 2014, proceedings,
part v 13, pp. 740–755. Springer, 2014.

Fangyu Liu, Guy Emerson, and Nigel Collier. Visual spatial reasoning. Transactions of the Asso-

ciation for Computational Linguistics, 11:635–651, 2023a.

31

Fuxiao Liu, Kevin Lin, Linjie Li, Jianfeng Wang, Yaser Yacoob, and Lijuan Wang. Mitigat-
ing hallucination in large multi-modal models via robust instruction tuning. arXiv preprint
arXiv:2306.14565, 2023b.

Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. Visual instruction tuning. Advances

in neural information processing systems, 36:34892–34916, 2023c.

Haotian Liu, Chunyuan Li, Yuheng Li, and Yong Jae Lee.

Improved baselines with visual in-
struction tuning. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern
Recognition, pp. 26296–26306, 2024.

Pan Lu, Ran Gong, Shibiao Jiang, Liang Qiu, Siyuan Huang, Xiaodan Liang, and Song-Chun Zhu.
Inter-gps: Interpretable geometry problem solving with formal language and symbolic reasoning.
arXiv preprint arXiv:2105.04165, 2021.

Pan Lu, Liang Qiu, Kai-Wei Chang, Ying Nian Wu, Song-Chun Zhu, Tanmay Rajpurohit, Peter
Clark, and Ashwin Kalyan. Dynamic prompt learning via policy gradient for semi-structured
mathematical reasoning. In International Conference on Learning Representations (ICLR), 2023.

Yujie Lu, Dongfu Jiang, Wenhu Chen, William Yang Wang, Yejin Choi, and Bill Yuchen Lin.
Wildvision: Evaluating vision-language models in the wild with human preferences. arXiv preprint
arXiv:2406.11069, 2024.

Muhammad Maaz, Hanoona Rasheed, Abdelrahman Shaker, Salman Khan, Hisham Cholakal,
Rao M Anwer, Tim Baldwin, Michael Felsberg, and Fahad S Khan. Palo: A polyglot large
multimodal model for 5b people. arXiv preprint arXiv:2402.14818, 2024.

Andrés Marafioti, Orr Zohar, Miquel Farré, Merve Noyan, Elie Bakouch, Pedro Cuenca, Cyril Zakka,
Loubna Ben Allal, Anton Lozhkov, Nouamane Tazi, et al. Smolvlm: Redefining small and efficient
multimodal models. arXiv preprint arXiv:2504.05299, 2025.

Kenneth Marino, Mohammad Rastegari, Ali Farhadi, and Roozbeh Mottaghi. Ok-vqa: A visual
In Proceedings of the IEEE/cvf

question answering benchmark requiring external knowledge.
conference on computer vision and pattern recognition, pp. 3195–3204, 2019.

Ahmed Masry, Do Xuan Long, Jia Qing Tan, Shafiq Joty, and Enamul Hoque. Chartqa: A bench-
mark for question answering about charts with visual and logical reasoning. arXiv preprint
arXiv:2203.10244, 2022.

Michael S Matena and Colin A Raffel. Merging models with fisher-weighted averaging. Advances

in Neural Information Processing Systems, 35:17703–17716, 2022.

Minesh Mathew, Dimosthenis Karatzas, and C. V. Jawahar. Docvqa: A dataset for vqa on document
In 2021 IEEE Winter Conference on Applications of Computer Vision (WACV), pp.

images.
2199–2208, 2021. doi: 10.1109/WACV48630.2021.00225.

Philip M. McCarthy and Scott Jarvis. Mtld, vocd-d, and hd-d: A validation study of sophisticated
approaches to lexical diversity assessment. Behavior Research Methods, 42(2):381–392, 2010. doi:
10.3758/BRM.42.2.381.

Brandon McKinzie, Zhe Gan, Jean-Philippe Fauconnier, Sam Dodge, Bowen Zhang, Philipp Dufter,
Dhruti Shah, Xianzhi Du, Futang Peng, Anton Belyi, et al. Mm1: methods, analysis and insights

32

from multimodal llm pre-training. In European Conference on Computer Vision, pp. 304–323.
Springer, 2024.

Niklas Muennighoff, Teven Le Scao, Yacine Jernite Wang, Philipp Schmid, Rachel Bawden, Angela
Fan, Vishrav Chaudhary, Matthias Gallé, et al. Crosslingual generalization through multitask
finetuning.
In Proceedings of the 2022 Conference on Empirical Methods in Natural Language
Processing (EMNLP), 2022.

Toan Q Nguyen, Vishrav Chaudhary, Xian Wang, Raj Dabre, Maha Elbayad, Angela Fan, et al.
Diverse multilingual pretraining for vision-language models. arXiv preprint arXiv:2402.13673,
2024.

Minheng Ni, Haoyang Huang, Lin Su, Edward Cui, Taroon Bharti, Lijuan Wang, Dongdong Zhang,
and Nan Duan. M3p: Learning universal representations via multitask multilingual multimodal
pre-training.
In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern
Recognition (CVPR), pp. 3977–3986, June 2021.

OpenAI. Gpt-4o system card. https://arxiv.org/abs/2410.21276, October 2024. Accessed:

2025-04-17.

Esther Ploeger, Huiyuan Lai, Rik van Noord, and Antonio Toral. Towards tailored recovery of

lexical diversity in literary machine translation. arXiv preprint arXiv:2408.17308, 2024.

Jordi Pont-Tuset, Jasper Uijlings, Soravit Changpinyo, Radu Soricut, and Vittorio Ferrari. Con-

necting vision and language with localized narratives, 2020.

Luiza Pozzobon, Beyza Ermis, Patrick Lewis, and Sara Hooker. Goodtriever: Adaptive toxicity
mitigation with retrieval-augmented models, 2023. URL https://arxiv.org/abs/2310.07589.

Danti Pudjiati, Ninuk Lustyantie, Ifan Iskandar, and Tira Nur Fitria. Post-editing of machine
translation: Creating a better translation of cultural specific terms. Language Circle: Journal of
Language and Literature, 17(1):61–73, 2022.

Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal,
Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, et al. Learning transferable visual
models from natural language supervision. In International conference on machine learning, pp.
8748–8763. PmLR, 2021.

Leonardo Ranaldi and Giulia Pucci. Does the english matter? elicit cross-lingual abilities of large
language models. In Proceedings of the 3rd Workshop on Multi-lingual Representation Learning
(MRL), pp. 173–183, 2023.

Vikas Raunak, Amr Sharaf, Yiren Wang, Hany Hassan Awadallah, and Arul Menezes. Leveraging

gpt-4 for automatic translation post-editing. arXiv preprint arXiv:2305.14878, 2023.

Ricardo Rei, Craig Stewart, Ana C Farinha, and Alon Lavie. Comet: A neural framework for mt

evaluation. arXiv preprint arXiv:2009.09025, 2020.

Ricardo Rei, Nuno M Guerreiro, José Pombal, Daan van Stigt, Marcos Treviso, Luisa Coheur,
José GC de Souza, and André FT Martins. Scaling up cometkiwi: Unbabel-ist 2023 submission
for the quality estimation shared task. arXiv preprint arXiv:2309.11925, 2023.

33

Anna Rohrbach, Lisa Anne Hendricks, Kaylee Burns, Trevor Darrell, and Kate Saenko. Object

hallucination in image captioning. arXiv preprint arXiv:1809.02156, 2018.

Angelika Romanou, Negar Foroutan, Anna Sotnikova, Zeming Chen, Sree Harsha Nelaturu, Shiv-
alika Singh, Rishabh Maheshwary, Micol Altomare, Mohamed A Haggag, Alfonso Amayuelas,
et al. Include: Evaluating multilingual language understanding with regional knowledge. arXiv
preprint arXiv:2411.19799, 2024.

David Romero, Chenyang Lyu, Haryo Akbarianto Wibowo, Teresa Lynn, Injy Hamed, Aditya Nanda
Kishore, Aishik Mandal, Alina Dragonetti, Artem Abzaliev, Atnafu Lambebo Tonja, et al.
Cvqa: Culturally-diverse multilingual visual question answering benchmark.
arXiv preprint
arXiv:2406.05967, 2024.

Israfel Salazar, Manuel Fernández Burda, Shayekh Bin Islam, Arshia Soltani Moakhar, Shivalika
Singh, Fabian Farestam, Angelika Romanou, Danylo Boiko, Dipika Khullar, Mike Zhang, et al.
Kaleidoscope: In-language exams for massively multilingual vision evaluation. arXiv preprint
arXiv:2504.07072, 2025.

Beatrice Savoldi, Marco Gaido, Luisa Bentivogli, Matteo Negri, and Marco Turchi. Gender bias in
machine translation. Transactions of the Association for Computational Linguistics, 9:845–874,
2021.

Dustin Schwenk, Apoorv Khandelwal, Christopher Clark, Kenneth Marino, and Roozbeh Mottaghi.
A-okvqa: A benchmark for visual question answering using world knowledge. In European con-
ference on computer vision, pp. 146–162. Springer, 2022.

Uri Shaham, Avia Efrat, Tom Kwiatkowski, Raghav Gupta, Chau Tran, Caiming Xiong, and Nishant
In Findings of the

Subramani. Just a pinch of multilinguality improves instruction tuning.
Association for Computational Linguistics (ACL), 2024.

Noam Shazeer. Glu variants improve transformer. arXiv preprint arXiv:2002.05202, 2020.

Lucas Shen. Lexicalrichness: A small module to compute textual lexical richness, 2022. URL

https://github.com/LSYS/lexicalrichness.

Freda Shi, Mirac Suzgun, Markus Freitag, Xuezhi Wang, Suraj Srivats, Soroush Vosoughi,
Hyung Won Chung, Yi Tay, Sebastian Ruder, Denny Zhou, et al. Language models are mul-
tilingual chain-of-thought reasoners. arXiv preprint arXiv:2210.03057, 2022.

Amanpreet Singh, Vivek Natarajan, Meet Shah, Yu Jiang, Xinlei Chen, Dhruv Batra, Devi Parikh,
and Marcus Rohrbach. Towards vqa models that can read. In Proceedings of the IEEE/CVF
conference on computer vision and pattern recognition, pp. 8317–8326, 2019.

Shivalika Singh, Angelika Romanou, Clémentine Fourrier, David I Adelani, Jian Gang Ngui, Daniel
Vila-Suero, Peerat Limkonchotiwat, Kelly Marchisio, Wei Qi Leong, Yosephine Susanto, et al.
Global mmlu: Understanding and addressing cultural and linguistic biases in multilingual evalu-
ation. arXiv preprint arXiv:2412.03304, 2024a.

Shivalika Singh, Freddie Vargus, Daniel Dsouza, Börje F. Karlsson, Abinaya Mahendiran, Wei-Yin
Ko, Herumb Shandilya, Jay Patel, Deividas Mataciunas, Laura OMahony, Mike Zhang, Ramith
Hettiarachchi, Joseph Wilson, Marina Machado, Luisa Souza Moura, Dominik Krzemiński,
Hakimeh Fadaei, Irem Ergün, Ifeoma Okoh, Aisha Alaagib, Oshan Mudannayake, Zaid Alyafeai,

34

Vu Minh Chien, Sebastian Ruder, Surya Guthikonda, Emad A. Alghamdi, Sebastian Gehrmann,
Niklas Muennighoff, Max Bartolo, Julia Kreutzer, Ahmet Üstün, Marzieh Fadaee, and Sara
Hooker. Aya dataset: An open-access collection for multilingual instruction tuning, 2024b.

Yueqi Song, Tianyue Ou, Yibo Kong, Zecheng Li, Graham Neubig, and Xiang Yue. Visualpuz-
arXiv preprint

zles: Decoupling multimodal reasoning evaluation from domain knowledge.
arXiv:2504.10342, 2025.

Ryota Tanaka, Kyosuke Nishida, Kosuke Nishida, Taku Hasegawa, Itsumi Saito, and Kuniko Saito.
Slidevqa: A dataset for document visual question answering on multiple images. arXiv preprint
arXiv:2301.04883, 2023.

Jingqun Tang, Qi Liu, Yongjie Ye, Jinghui Lu, Shu Wei, Chunhui Lin, Wanqing Li, Mohamad Fitri
Faiz Bin Mahmood, Hao Feng, Zhen Zhao, et al. Mtvqa: Benchmarking multilingual text-centric
visual question answering. arXiv preprint arXiv:2405.11985, 2024.

Chameleon Team. Chameleon: Mixed-modal early-fusion foundation models.

arXiv preprint

arXiv:2405.09818, 2024a.

Gemini Team. Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context,

2024b. URL https://arxiv.org/abs/2403.05530.

Gemini Team, Petko Georgiev, Ving Ian Lei, Ryan Burnell, Libin Bai, Anmol Gulati, Garrett
Tanzer, Damien Vincent, Zhufeng Pan, Shibo Wang, et al. Gemini 1.5: Unlocking multimodal
understanding across millions of tokens of context. arXiv preprint arXiv:2403.05530, 2024.

Kimi Team, Angang Du, Bofei Gao, Bowei Xing, Changjiu Jiang, Cheng Chen, Cheng Li, Chenjun
Xiao, Chenzhuang Du, Chonghua Liao, Chuning Tang, Congcong Wang, Dehao Zhang, Enming
Yuan, Enzhe Lu, Fengxiang Tang, Flood Sung, Guangda Wei, Guokun Lai, Haiqing Guo, Han
Zhu, Hao Ding, Hao Hu, Hao Yang, Hao Zhang, Haotian Yao, Haotian Zhao, Haoyu Lu, Haoze Li,
Haozhen Yu, Hongcheng Gao, Huabin Zheng, Huan Yuan, Jia Chen, Jianhang Guo, Jianlin Su,
Jianzhou Wang, Jie Zhao, Jin Zhang, Jingyuan Liu, Junjie Yan, Junyan Wu, Lidong Shi, Ling Ye,
Longhui Yu, Mengnan Dong, Neo Zhang, Ningchen Ma, Qiwei Pan, Qucheng Gong, Shaowei Liu,
Shengling Ma, Shupeng Wei, Sihan Cao, Siying Huang, Tao Jiang, Weihao Gao, Weimin Xiong,
Weiran He, Weixiao Huang, Wenhao Wu, Wenyang He, Xianghui Wei, Xianqing Jia, Xingzhe Wu,
Xinran Xu, Xinxing Zu, Xinyu Zhou, Xuehai Pan, Y. Charles, Yang Li, Yangyang Hu, Yangyang
Liu, Yanru Chen, Yejie Wang, Yibo Liu, Yidao Qin, Yifeng Liu, Ying Yang, Yiping Bao, Yulun
Du, Yuxin Wu, Yuzhi Wang, Zaida Zhou, Zhaoji Wang, Zhaowei Li, Zhen Zhu, Zheng Zhang,
Zhexu Wang, Zhilin Yang, Zhiqi Huang, Zihao Huang, Ziyao Xu, and Zonghan Yang. Kimi k1.5:
Scaling reinforcement learning with llms, 2025. URL https://arxiv.org/abs/2501.12599.

Peter Tong, Ellis Brown, Penghao Wu, Sanghyun Woo, Adithya Jairam Vedagiri IYER, Sai Charitha
Akula, Shusheng Yang, Jihan Yang, Manoj Middepogu, Ziteng Wang, et al. Cambrian-1: A fully
open, vision-centric exploration of multimodal llms. Advances in Neural Information Processing
Systems, 37:87310–87356, 2024.

Michael Tschannen, Alexey Gritsenko, Xiao Wang, Muhammad Ferjad Naeem, Ibrahim Alabdul-
mohsin, Nikhil Parthasarathy, Talfan Evans, Lucas Beyer, Ye Xia, Basil Mustafa, et al. Siglip 2:
Multilingual vision-language encoders with improved semantic understanding, localization, and
dense features. arXiv preprint arXiv:2502.14786, 2025.

35

Ahmet Üstün, Viraat Aryabumi, Zheng-Xin Yong, Wei-Yin Ko, Daniel D’souza, Gbemileke Onilude,
Neel Bhandari, Shivalika Singh, Hui-Lee Ooi, Amr Kayid, et al. Aya model: An instruction
finetuned open-access multilingual language model. arXiv preprint arXiv:2402.07827, 2024.

Eva Vanmassenhove, Dimitar Shterionov, and Matthew Gwilliam. Machine translationese: Effects of
algorithmic bias on linguistic complexity in machine translation. arXiv preprint arXiv:2102.00287,
2021.

Bryan Wang, Gang Li, Xin Zhou, Zhourong Chen, Tovi Grossman, and Yang Li. Screen2words: Au-
tomatic mobile ui summarization with multimodal learning. In The 34th Annual ACM Symposium
on User Interface Software and Technology, pp. 498–510, 2021.

Fei Wang, Wenxuan Zhou, James Y Huang, Nan Xu, Sheng Zhang, Hoifung Poon, and Muhao
Chen. mdpo: Conditional preference optimization for multimodal large language models. arXiv
preprint arXiv:2406.11839, 2024a.

Jun Wang, Benjamin Rubinstein, and Trevor Cohn. Measuring and mitigating name biases in
In Proceedings of the 60th Annual Meeting of the Association for

neural machine translation.
Computational Linguistics (Volume 1: Long Papers), pp. 2576–2590, 2022.

Peng Wang, Shuai Bai, Sinan Tan, Shijie Wang, Zhihao Fan, Jinze Bai, Keqin Chen, Xuejing Liu,
Jialin Wang, Wenbin Ge, et al. Qwen2-vl: Enhancing vision-language model’s perception of the
world at any resolution. arXiv preprint arXiv:2409.12191, 2024b.

Zirui Wang, Mengzhou Xia, Luxi He, Howard Chen, Yitao Liu, Richard Zhu, Kaiqu Liang, Xindi
Wu, Haotian Liu, Sadhika Malladi, et al. Charxiv: Charting gaps in realistic chart understanding
in multimodal llms. Advances in Neural Information Processing Systems, 37:113569–113697,
2024c.

Christoph Wendler. wendlerc/renderedtext, 2023. URL https://huggingface.co/datasets/wend

lerc/RenderedText.

Mitchell Wortsman, Gabriel Ilharco, Samir Ya Gadre, Rebecca Roelofs, Raphael Gontijo-Lopes,
Ari S Morcos, Hongseok Namkoong, Ali Farhadi, Yair Carmon, Simon Kornblith, et al. Model
soups: averaging weights of multiple fine-tuned models improves accuracy without increasing
inference time. In International conference on machine learning, pp. 23965–23998. PMLR, 2022.

xAI. Realworldqa dataset, 2024. URL https://huggingface.co/datasets/xai-org/Realworld

QA. Accessed on May 4, 2025.

Prateek Yadav, Derek Tam, Leshem Choshen, Colin A Raffel, and Mohit Bansal. Ties-merging:
Resolving interference when merging models. Advances in Neural Information Processing Systems,
36:7093–7115, 2023.

Michihiro Yasunaga, Luke Zettlemoyer, and Marjan Ghazvininejad. Multimodal rewardbench:
Holistic evaluation of reward models for vision language models, 2025. URL https://arxi
v.org/abs/2502.14191.

Xiang Yue, Yuansheng Ni, Kai Zhang, Tianyu Zheng, Ruoqi Liu, Ge Zhang, Samuel Stevens, Dongfu
Jiang, Weiming Ren, Yuxuan Sun, et al. Mmmu: A massive multi-discipline multimodal under-
standing and reasoning benchmark for expert agi. In Proceedings of the IEEE/CVF Conference
on Computer Vision and Pattern Recognition, pp. 9556–9567, 2024a.

36

Xiang Yue, Yueqi Song, Akari Asai, Simran Khanuja, Anjali Kantharuban, Seungone Kim, Jean
de Dieu Nyandwi, Lintang Sutawika, Sathyanarayanan Ramamoorthy, and Graham Neubig.
Pangea: A fully open multilingual multimodal llm for 39 languages. In The Thirteenth Inter-
national Conference on Learning Representations, 2024b.

Ted Zadouri, Ahmet Üstün, Arash Ahmadian, Beyza Ermiş, Acyr Locatelli, and Sara Hooker.
Pushing mixture of experts to the limit: Extremely parameter efficient moe for instruction tuning.
arXiv preprint arXiv:2309.05444, 2023.

Yan Zeng, Wangchunshu Zhou, Ao Luo, Ziming Cheng, and Xinsong Zhang. Cross-view language
modeling: Towards unified cross-lingual cross-modal pre-training, 2023. URL https://arxiv.
org/abs/2206.00621.

Xiaohua Zhai, Basil Mustafa, Alexander Kolesnikov, and Lucas Beyer. Sigmoid loss for language
image pre-training. In Proceedings of the IEEE/CVF international conference on computer vision,
pp. 11975–11986, 2023.

Yilun Zhao, Yunxiang Li, Chenying Li, and Rui Zhang. MultiHiertt: Numerical reasoning over
multi hierarchical tabular and textual data. In Proceedings of the 60th Annual Meeting of the
Association for Computational Linguistics (Volume 1: Long Papers), pp. 6588–6600, Dublin,
Ireland, May 2022. Association for Computational Linguistics. URL https://aclanthology.o
rg/2022.acl-long.454.

Jeffrey Zhou, Tianjian Lu, Swaroop Mishra, Siddhartha Brahma, Sujoy Basu, Yi Luan, Denny
Zhou, and Le Hou. Instruction-following evaluation for large language models. arXiv preprint
arXiv:2311.07911, 2023.

Didi Zhu, Yibing Song, Tao Shen, Ziyu Zhao, Jinluan Yang, Min Zhang, and Chao Wu. Rem-
edy: Recipe merging dynamics in large vision-language models. In The Thirteenth International
Conference on Learning Representations, 2025.

Fengbin Zhu, Wenqiang Lei, Youcheng Huang, Chao Wang, Shuo Zhang, Jiancheng Lv, Fuli Feng,
and Tat-Seng Chua. TAT-QA: A question answering benchmark on a hybrid of tabular and textual
content in finance. In Proceedings of the 59th Annual Meeting of the Association for Computational
Linguistics and the 11th International Joint Conference on Natural Language Processing (Volume
1: Long Papers), pp. 3277–3287, Online, August 2021. Association for Computational Linguistics.
doi: 10.18653/v1/2021.acl-long.254. URL https://aclanthology.org/2021.acl-long.254.

Wenhao Zhu, Hongyi Liu, Qingxiu Dong, Jingjing Xu, Shujian Huang, Lingpeng Kong, Jiajun Chen,
and Lei Li. Multilingual machine translation with large language models: Empirical results and
analysis. arXiv preprint arXiv:2304.04675, 2023.

37

A Evaluation Details

A.1 AyaVisionBench

To create this dataset, we first sourced images from the test splits of various datasets included
in Cauldron [Laurençon et al., 2024b], a large-scale collection of 50 high-quality vision datasets.
By exclusively selecting images from the test splits, we ensured that none had been seen during
model training. Following the original task categories defined in Cauldron, we randomly sampled
15 images from each of 9 distinct tasks, resulting in a total of 135 unseen images. For each image,
we generated a corresponding question that required explicit visual understanding to answer. These
questions were initially generated synthetically and then manually reviewed for clarity, relevance,
and dependence on the visual content.

To support multilingual evaluation, each question was translated into 22 additional languages us-
ing Google Translate18, covering all 23 languages supported by Aya Vision. All translations were
subsequently verified by human annotators to ensure fidelity and naturalness. During human an-
notation, annotators were also asked to validate the prompts and provide reference answers for
questions with deterministic answers. These reference answers are included in the benchmark.
The resulting dataset, AyaVisionBench, offers a diverse and challenging benchmark for evaluat-
ing vision-language models in multilingual and open-ended contexts. Representative examples are
shown in Figure 14.

Figure 14: Three sample entries from AyaVisionBench, illustrating a range of languages
and image task types. From left to right: English (TQA [Kembhavi et al., 2017]), Chinese (VSR
[Liu et al., 2023a]), and Turkish (TabMWP [Lu et al., 2023]). All images are sourced from the test
sets of the respective datasets.

18https://cloud.google.com/translate?hl=en

38

	A botanist discovers a new plant species with leaves that have a pointed base. Using the provided image, which leaf shape most closely matches this description? Additionally, if the leaves are asymmetrical, with one side of the leaf blade lower than the other, which term from the image corresponds to this characteristic?Reference: cuneate, oblique根据透过车窗看到的场景，这个地方可能正在庆祝或观察什么独特的文化传统或活动？Her ay yüzdelik düşüş oranının benzer şekilde devam ettiği varsayıldığında, Ağustos ayında yaklaşık kaç derginin satılması beklenir?Reference: 1209 * (0.46)^2 = 256A.2 Multimodal Acedemic Benchmarks

• xMMMU [Yue et al., 2024b], a machine-translated version of 300 questions from the MMMU
validation set into 6 languages to measure the multimodal understanding and reasoning.

• MaXM [Changpinyo et al., 2022] evaluates vision-language models on multilingual VQA tasks

in 7 languages.

• CVQA [Romero et al., 2024] is a large-scale, multilingual VQA dataset to test models’ un-

derstanding of cultural nuances in 31 languages.

• MTVQA [Tang et al., 2024] evaluates multilingual multimodal models on text-centric scene

understanding in 9 languages.

• Kaleidoscope [Salazar et al., 2025] consists of 20,911 multimodal multiple-choice questions
in 18 languages, designed to evaluate the reasoning and knowledge of vision-language models
across diverse subjects and cultures.

A.3 Text-Only Benchmarks

• m-ArenaHard [Li et al., 2024] following [Dang et al., 2024], we use multilingual ArenaHard
to measure the win-rates against other models across 23 languages to understand the impact
of multimodal training on the model’s text-only capabilities. We use gpt-4o-2024-11-20
[OpenAI, 2024] as the judge.

• MGSM [Shi et al., 2022] evaluates the reasoning abilities of large language models with 250

grade-school math problems in 10 languages

• Global MMLU-Lite [Singh et al., 2024a] is a multilingual MMLU test set spanning 42

languages

• FLORES [Guzmán et al., 2019] is an evaluation benchmark for machine translation in low-

resource languages.

• IFEval [Zhou et al., 2023] is a benchmark designed to assess the ability of large language

models to follow verifiable instructions.

B Training Hyerparameters

Table 6: Training Hyper-parameters for Aya Vision-8B and Aya Vision-32B models

Aya Vision

8B

32B

Vision Encoder
Params
Dim
MLP Dim
Act.
Heads

400M
1152
4304
GELU
16

400M
1152
4304
GELU
16

39

KV Heads
Layers
Image Size
Patch Size

16
27
364×364
14

16
27
512×512
16

Vision-Language Connector
Params
Downsample Factor
MLP Dim
Act.

190M
2
14336
SwiGLU

428M
2
24676
SwiGLU

32.3B
256k
8192
24676
SwiGLU
64
8
40
4M

8B
256k
4096
14336
SwiGLU
32
8
32
50k

200
1e-4
10%

200
1e-3
10%

AdamW AdamW
0.9, 0.95
0.9, 0.95
128
128
19k
9.7k

200
1e-4
10%
0.9, 0.95
128
31k

200
5e-4
10%
0.9, 0.95
128
31k

LLM
Params
Embed
Dim
MLP Dim
Act.
Heads
KV Heads
Layers
Theta

Alignment
Warmup
Peak LR
Cosine Decay
Optimizer
Betas
Batch Size
Steps

SFT
Warmup LLM
Peak LR
Cosine Decay
Betas
Batch Size
Steps

C Additional Ablations

C.1 Stronger Vision Encoder Improves VQA Performance

With the recent releases of better vision encoders, we ask how do these gains translate to downstream
multimodal performance? We design an experiment by training a variant of Aya Vision-8B with
the original SigLIP encoder instead of SigLIP-2 with the same resolution and patch size. Interest-
ingly, we observe no visible impact on the multimodal win-rates; however, switching to SigLIP-2

40

provides substantial improvements in multimodal academic benchmarks like CVQA[Romero et al.,
2024], TextVQA [Singh et al., 2019], DocVQA [Mathew et al., 2021], ChartQA [Masry et al., 2022],
OKVQA [Marino et al., 2019] and RealWorldQA [xAI, 2024] – with an average improvement of 4%
as shown in Figure 15.

Figure 15: Improvement by switching to SigLIP-2. We report the average of VQA evaluations
listed in § C.1.

41

SigLIP-1SigLIP-2404550556065Average Normalized Score (%)57.1%60.9%D Recaptioning Templates

General Visual Question Answering

System Prompt:
You are an advanced multimodal AI chatbot with strong visual question answering capabili-
ties.
User Prompt:
Here is a question-answer pair for the given image:
Question:
{instruction}
Reference Answer:
{answer}
Task Description:
Analyze all provided image and fully understand the question, paying attention to every
detail and context within the image.
The reference answer is the correct answer to the question.
Your task is to generate a more comprehensive, natural and human-preferred response to the
question.
Enhance the response by adding additional visual context, mentioning relevant information,
or providing detailed explanations.
If the question is multiple-choice, the response should mention the letter/number of the
selected choice.
Also, ensure that the final result in the response is consistent with the reference answer.
But, do not explicitly mention there is a reference answer in the response.
The response should stand independently as a complete and well-organized new answer to
the question.

Enclose the new answer within <answer> </answer> tags.

42

Captioning

System Prompt:
You are an advanced multimodal AI chatbot with strong image captioning capabilities.
User Prompt:
Here is an image captioning instruction along with the original caption for the provided
image.
Instruction:
{instruction}
Original Caption:
{answer}
Task Description:
Examine the image carefully, paying attention to every detail and context within the image.
Your task is to rewrite the original caption to be more detailed, descriptive, comprehensive,
and human-preferred.
Ensure that the new caption accurately reflects the content and context of the image while
following the given instruction.
Since this is an image captioning task, do not include any information that is not directly
visible in the image.
Do not explicitly mention there is an original caption in the response.
Ensure the response stands independently as a complete and well-organized new caption.

Enclose the new caption within <answer> </answer> tags.

43

OCR, document understanding, text transcription

System Prompt:
You are an advanced multimodal AI chatbot with strong text-rich image understanding
capabilities.
User Prompt:
Here is a question-answer pair based on the provided document, screenshot or scanned
image.
Question:
{instruction}
Reference Answer:
{answer}
Task Description:
Read the provided text-rich document, screenshot, or scanned image carefully to ensure a
comprehensive understanding of its contents.
The reference answer is the correct answer to the question.
Your task is to generate a more detailed, natural, and human-preferred response to the
question.
Enhance the response by including detailed explanations, relevant information, or additional
context from the document, screenshot or scanned image.
Also, ensure that the final result in the response is consistent with the reference answer.
But, do not explicitly mention there is a reference answer in the response.
The response should stand independently as a complete and well-organized new answer to
the question.

Enclose the new answer within <answer> </answer> tags.

44

Chart/figure understanding

System Prompt:
You are an advanced multimodal AI chatbot with strong chart and figure understanding
capabilities.
User Prompt:
Here is a question-answer pair based on the provided chart or figure.
Question:
{instruction}
Reference Answer:
{answer}
Task Description:
Carefully analyze the provided chart or figure to ensure a comprehensive understanding of
its contents.
The reference answer is the correct answer to the question.
Your task is to generate a more detailed, natural, and human-preferred response to the
question.
Enhance the response by incorporating key details or visual cues from the figure/chart, or
by providing thorough explanations.
Also, ensure that the final result in the response is consistent with the reference answer.
But, do not explicitly mention there is a reference answer in the response.
The response should stand independently as a complete and well-organized new answer to
the question.

Enclose the new answer within <answer> </answer> tags.

45

Table understanding

System Prompt:
You are an advanced multimodal AI chatbot with strong table understanding capabilities.
User Prompt:
Here is a question-answer pair for the given image:
Question:
{instruction}
Reference Answer:
{answer}
Task Description:
Analyze all provided image and fully understand the question, paying attention to every
detail and context within the image.
The reference answer is the correct answer to the question.
Your task is to generate a more comprehensive, natural and human-preferred response to the
question.
Enhance the response by adding additional visual context, mentioning relevant information,
or providing detailed explanations.
If the question is multiple-choice, the response should mention the letter/number of the
selected choice.
Also, ensure that the final result in the response is consistent with the reference answer.
But, do not explicitly mention there is a reference answer in the response.
The response should stand independently as a complete and well-organized new answer to
the question.

Enclose the new answer within <answer> </answer> tags.

46

Reasoning, logic, maths

System Prompt:
You are an advanced multimodal AI chatbot with strong visual reasoning and mathematical
capabilities.
User Prompt:
Here is a visual reasoning or mathematical question-answer pair based on the provided
image.
Question:
{instruction}
Reference Answer:
{answer}
Task Description:
Analyze the provided image and think carefully. The question requires visual or mathemati-
cal reasoning skills.
The reference answer is the correct answer to the question.
Your task is to provide a more comprehensive response to the question.
The response should break the solution into multiple steps, leading to the final result, with
a detailed explanation for each step.
Ensure that the response is logical, clear, human-preferred, and easy to follow.
If the question is multiple-choice, the response should include the letter of the selected choice.
Also, ensure that the final result in the response is consistent with the reference answer.
But, do not explicitly mention there is a reference answer in the response.
The response should stand independently as a complete and well-organized new answer to
the question.

Enclose the new answer within <answer> </answer> tags.

47

Textbook/academic questions

System Prompt:
You are an advanced multimodal AI chatbot with strong visual capabilities and extensive
knowledge.
User Prompt:
Here is a question-answer pair based on the provided textbook or academic image.
Question:
{instruction}
Reference Answer:
{answer}
Task Description:
Examine the textbook or academic image, read the question and background context (if
provided), and think carefully.
The reference answer is the correct answer to the question.
Your task is to generate a more comprehensive, natural, and human-preferred response to
the question.
Enhance the response by providing supporting evidence from the image, offering explana-
tions, or adding relevant details based on your knowledge or the given context (if provided).
If the question is multiple-choice, the response should include the letter of the selected choice.
Also, ensure that the final result in the response is consistent with the reference answer.
But, do not explicitly mention there is a reference answer in the response.
The response should stand independently as a complete and well-organized new answer to
the question.

Enclose the new answer within <answer> </answer> tags.

48

Differences between 2 images

System Prompt:
You are an advanced multimodal AI chatbot with strong visual description capabilities.
User Prompt:
Here is a instruction-answer pair based on provided images.
Instruction:
{instruction}
Reference Answer:
{answer}
Task Description:
Examine the two provided images carefully, paying close attention to their differences.
Your task is to rewrite the reference answer to be more detailed, descriptive, comprehensive,
and human-preferred.
Ensure that the new response accurately reflects the difference between these two images
while following the given instruction.
Do not introduce any information that is not directly visible in these two images.
Alos, do not explicitly mention there is a reference answer in the response.
Ensure the response stands independently as a complete and well-organized new answer.

Enclose the new answer within <answer> </answer> tags.

49

E Recaptioned Examples

General Visual Question Answering

Prompt
What is the object behind the truck?
Choose the right answer and clarify with the
format:
’Answer: answer Rationale: rationale.’
Options: Block wall, motorhome, trailer, ufo.

A-OKVQA [Schwenk et al., 2022]

Caption
Answer: trailer. Rationale: There is a large red object following the car.
Recaption
Answer: trailer. Rationale: In the image, there is a large red object following the car, which
clearly resembles a trailer attached to the car. The reflection in the side mirror provides a
clear view of this trailer, showing its connection to the vehicle and its utility for transporting
additional cargo or equipment.

Captioning

Prompt
Can you explain what this image depicts?

Localized Narratives [Pont-Tuset et al., 2020]

Caption
In the center of the image there is a buildings. There are windows. There is a railing.
Recaption
The image showcases a picturesque scene of historical architecture, featuring buildings with
arched windows and ornate balconies. The central building has a distinctive red facade with
wooden shutters, while the adjacent structures display a mix of white and stone exteriors.
Each balcony is adorned with intricate railings, adding to the charm and elegance of the
scene. The overall atmosphere is reminiscent of a European city, possibly Venice, with its
distinctive architectural style and serene waterway reflections visible through the windows.

50

OCR, document understanding, text transcription

Prompt
What is written at the top?

TextVQA [Singh et al., 2019]

Caption
Hi-tech.
Recaption
At the top of the image, the text "Hi-tech" is written, indicating the brand or type of the
device or software associated with the keyboard pictured. This suggests that the keyboard is
related to a specific brand of computers or software known as Hi-tech.

Chart/figure understanding

Prompt
What was the only other service that had a
higher share of exclusive titles than Netflix?

ChartQA [Masry et al., 2022]

Caption
Apple TV+.
Recaption
The only other service that had a higher share of exclusive titles than Netflix is Apple TV+.
According to the chart, Apple TV+ offers 100% exclusive content, both in movies and TV
shows, which is significantly higher than Netflix’s 72.34% exclusive TV shows and 48.64%
exclusive movies. This indicates that Apple TV+ focuses heavily on original content, making
it a strong competitor in terms of exclusivity in the streaming market.

51

Table understanding

TAT QA [Zhu et al., 2021]

Prompt
A county agency recorded the money donated
to several charitable
causes over time. How much more money was
raised for parks in
April than in March?

Caption
Find the Parks row. Find the numbers in this row for April and March. April: $ 15.00 March:
$7.00 Now subtract: $15.00 - $7.00 = $8.00 $8 more was raised for parks in April than in
March.
Recaption
To determine how much more money was raised for parks in April than in March, we need to
look at the amounts donated to parks in each month. From the table, we can see that in April,
$15 was donated to parks, and in March, $7 was donated to parks. To find the difference, we
subtract the amount donated in March from the amount donated in April: April donation:
$15 March donation: $7 Difference: $15 - $7 = $8 Therefore, $8 more was raised for parks in
April than in March.

52

Reasoning, logic, maths

Inter GPS [Lu et al., 2021]

Prompt
Question: Find x.
Choices: A. 8 B. 11.3 C. 13.9 D. 16

√

3:2.

Caption
Answer: C
Recaption
To find the length of x in the given right-angled triangle, we can use trigonometric ratios.
Since the triangle has a 60-degree angle, we can apply the properties of a 30-60-90 triangle,
where the sides are in the ratio 1:
1. Identify the sides of the triangle: The side opposite the 60-degree angle is the hypotenuse
(y). The side adjacent to the 60-degree angle is x. The side opposite the right angle is 8
units.
2. Use the appropriate trigonometric ratio: - In a 30-60-90 triangle, the side adjacent to the
60-degree angle (x) is
3 times the length of the side opposite the 30-degree angle (which is
half the hypotenuse).
3. Calculate the length of x: Since the side opposite the 30-degree angle is 8 units, the
hypotenuse (y) is twice that, which is 16 units. The length of x is
3 times the length of the
side opposite the 30-degree angle. Therefore, (x = 8 times
4. Simplify the expression: (x = 8 times
nearest tenth, the length of x is approximately 13.9 units.
Therefore, the correct answer is C. 13.9.

3 approx 8 times 1.732 = 13.856).Rounding to the

3).

√

√

√

√

53

Textbook/academic questions

Prompt
Question: What
Choices:
A. sun B. sky C. star D. moon

the

is

earth orbiting?

AI2D [Kembhavi et al., 2016]

Caption
Answer: A
Recaption
Answer: A. The Earth is orbiting the Sun. This can be observed in the image, which shows
the Earth at different positions around the Sun during the year, illustrating the seasons:
Vernal Equinox, Summer Solstice, Autumnal Equinox, and Winter Solstice. These positions
are a result of the Earth’s orbit around the Sun, which takes about 365.25 days to complete
one full orbit. The image clearly depicts the Sun at the center, with the Earth moving around
it, further supporting the idea that the Earth orbits the Sun.

54

Differences between 2 images

MIMIC-IT [Li et al., 2023a]

Prompt
The first image is the image on the left, the second image is the image on the right. Given
the left and right images, does the statement "There are at least two people riding on one of
the dog sleds." hold true?

Caption
No.
Recaption
No, the statement does not hold true. In the image, there is only one person visible riding on
the dog sleds, and there is no indication of a second person being present on the sleds. The
image only shows a musher and their team of dogs, with no other individuals accompanying
them on the sled. Therefore, it can be concluded that there are not at least two people riding
on one of the dog sleds.

55

F Filtering Template and Filtered Samples

Filtering Template

Question:
{question}
Ground Truth Answer:
{answer}
Generated Response:
{response}
Instruction:
Given the question, compare the generated response with the ground truth answer.
Your task is to evaluate the correctness of the generated response.
The generated response is correct if the final result or key information in the response
matches or is consistent with the ground truth answer.
The response does not need to be an exact match, but it should include or align with the
ground truth.

Provide your response with a ’YES’ if the generated response is correct, or ’NO’ if it is not.
Start your evaluation with a brief explanation, followed by your final decision.

Your output must strictly follow this format:
Explanation: <brief explanation> Final Decision: <YES or NO>

Sample 1

Prompt
What number comes after Shepshed?

ST VQA [Biten et al., 2019]

Caption (Ground Truth)
4.
Recaption
In the visible part of the sign, the numbers listed are 1, 3, and 9 miles, corresponding to
distances to Whitwick, Mount Saint Bernard Abbey, and The Oaks respectively. If we consider
the context and typical ordering of such signs, and given the reference answer suggesting the
number is 4, it’s likely that Shepshed is mentioned on a part of the sign not shown here, and
it is 4 miles away from the signpost. Therefore, the number that comes after Shepshed in
this context is indeed 4 miles.

56

Sample 2

Prompt
How many people can you see?

TallyQA [Acharya et al., 2019]

Caption (Ground Truth)
5.
Recaption
In the image, I can see six people. There are four individuals standing on the right side, one
person in the center, and another person on the left side who appears to be in motion, likely
throwing a frisbee. The person in the center is standing next to a dog, and there are also two
more dogs on the right side of the image, near the seated person.

57

G Translation Rephrasing Template and Translation

Enhancements

Translation Rephrasing Template

Original Text:
{raw_text}

Translation:
{translation}

improve the quality of the translation by

Instruction:
Given the original text and its translation,
rephrasing it.
Ensure the rephrased translation closely aligns with the original text in meaning, structure,
tone, and style.
Make the rephrased translation sound natural and fluent in the target language (language)
while preserving all essential details, correcting any grammatical errors, and retaining all
stylistic elements (e.g., enumeration, parentheses, punctuation, capitalization, spacing, line
breaks, etc.) from the original.

The output must strictly enclose the rephrased translation within <translation> </transla-
tion> tags.

58

59

HindiVQAv2[Goyaletal.,2017]PromptHasthekitchenbeenrecentlyrenovated?NLLBTranslatedPromptक्यारसोईघरकाहालहीमेंनवीनीकरण(cid:607)कयागयाहै?RephrasedPromptक्याहालहीमेंरसोईकानवीनीकरण(cid:607)कयागयाहै?RecaptionNo,thekitchenhasnotbeenrecentlyrenovated.Thepresenceofanoldermodelrefrigerator,theworncountertopwithvisiblestains,andtheoutdatedwallpapersuggestthatthekitchenisquiteagedandhasnotundergonerecentupdatesorrenovations.NLLBTranslatedRecaptionनहीं,रसोईकाहालहीमेंनवीनीकरणनहीं(cid:607)कयागयाहै।पुरानेमॉडलकेरे(cid:607)फ्रजरेटरक(cid:655)उप(cid:604)(cid:568)(cid:607)त,(cid:606)दखनेवालेदागोंकेसाथपहनाहुआकाउंटरटॉप,औरपुरानेवॉलपेपरसेपताचलताहै(cid:607)करसोईकाफ(cid:655)पुरानीहैऔरहालहीमेंअपडेटयानवीनीकरणनहीं(cid:607)कयागयाहैRephrasedRecaptionनहीं,रसोईकाहालहीमेंनवीनीकरणनहीं(cid:607)कयागयाहै।उपकरणपुरानेहैं,औरसमग्रसजावटऔरसतहोंपहननेऔरउम्रकेसंकेत(cid:606)दखातेहैं,यहदशार्ताहै(cid:607)कयहएकसमयमें(cid:607)कसीभीमहत्वपूणर्अद्यतनयासुधारनहीं(cid:607)कयागयाहै।6060

TurkishGQA[Hudson&Manning,2019]PromptWhatkindoffurnitureisbehindthechair?NLLBTranslatedPromptSandalyeninarkasındanetürbirmobilyavar?RephrasedPromptSandalyeninarkasındahangimobilyalarbulunuyor?RecaptionBehindthechair,thereisawoodenbookshelf.Thisbookshelfappearstobefilledwithvariousbooksandpossiblyotheritems,indicatingitmightbeacentralpieceforstorageandorganizationinthisroom.Theshelfispositionedagainstthewall,addingtothecozyandfunctionallayoutofthespace.NLLBTranslatedRecaptionSandalyeninarkasında,ahşapbirkitaplıkvar.Bukitaplıkçeşitlikitaplarlavemuhteme-lendiğereşyalarladolugörünüyor,buodadadepolamavedüzenlemeiçinmerkezibirparçaolabileceğinigösteriyor.Rafduvaradayanarakyerleştirilmiştir,mekanınrahatveişlevseldüzeninekatkıdabulunur.RephrasedRecaptionSandalyeninarkasında,ahşapbirkitaplıkbulunuyor.Kitaplık,farklıkitaplarvemuh-temelendiğereşyalarladolugörünüyor,budaodadakidepolamavedüzenlemeiçinönemlibirparçaolabileceğinigösteriyor.Kitaplık,duvarayaslanmışşekildekonumlan-dırılmışveodanınrahatvekullanışlıdüzeninekatkıdabulunuyor.ChineseCOCOQA[Renetal.,2015]PromptWhatstandsinanopenfieldlookingup-wards?NLLBTranslatedPrompt在野外,有一只长<unk>鹿高高的站着,抬头看.长<unk>鹿的长<unk>子和独特的毛皮图案RephrasedPrompt什么东西在空旷的田野中仰望天空?RecaptionIntheopenfield,thereisagiraffestandingtallandlookingupwards.Thegiraffe’slongneckanddistinctivecoatpatternofdarkpatchesseparatedbylighterlinesareclearlyvisible.NLLBTranslatedRecaption在野外,有一只长<unk>鹿高高的站着,抬头看.长<unk>鹿的长<unk>子和独特的毛皮图案RephrasedRecaption在空旷的田野中,有一只长颈鹿昂首挺立,望向天空.长颈鹿的长脖子和独特的毛皮图案清晰可见,由深色斑块和浅色线条间隔组成61H Translation Quality Score

Language NLLB after Rephrasing
fra_Latn
por_Latn
tur_Latn
nld_Latn
pes_Arab
rus_Cyrl
ron_Latn
zho_Hant
ita_Latn
deu_Latn
jpn_Jpan
ukr_Cyrl
vie_Latn
arb_Arab
zho_Hans
heb_Hebr
pol_Latn
spa_Latn
ell_Grek
ind_Latn
ces_Latn
kor_Hang
hin_Deva

0.8285
0.8374
0.8321
0.8394
0.8247
0.8293
0.8787
0.7997
0.8447
0.8275
0.8596
0.8428
0.8372
0.8213
0.8216
0.8160
0.8151
0.8228
0.8363
0.8412
0.8523
0.8537
0.7124

0.7786
0.7610
0.7688
0.7922
0.7528
0.7685
0.8145
0.4436
0.7979
0.7876
0.7271
0.7492
0.7580
0.7411
0.6612
0.7107
0.7304
0.7595
0.7783
0.7841
0.7825
0.7982
0.7001

Table 7: reference-free machine translation score by language

61

I

Image Translation and Re-rendering effort

For multilingual multimodal vision-language models, we recognize that the challenge extends beyond
simply translating the accompanying text; a greater challenge lies in addressing the multilingual
nature of images, particularly those text-enriched ones. Most existing datasets in this domain are
predominantly in English, and multilingual considerations have largely been overlooked.
In this
work, we not only translate the textual components of our collected image-text pairs, but also
devote some effort to identifying source datasets – synthetic ones – that are suitable for transla-
In other words, we translate the original image source files into multiple
tion and re-rendering.
target languages and subsequently re-render the images with the translated text. Our translation
workflow is consistent with the approach described in Section 2.4. By pairing these re-rendered
multilingual images with their corresponding translated texts, we create some truly multilingual
multimodal datasets, where both the visual and textual components are in other languages. This
greatly supports cross-lingual multimodal understanding. Specifically, the datasets we processed
include Multihiertt [Zhao et al., 2022], FinQA [Chen et al., 2021], DVQA [Kafle et al., 2018], Fig-
ureQA [Kahou et al., 2017], and RenderedText [Wendler, 2023]. Here we are showing some examples
of our re-rendered images:

(a) eng_Latn

(b) jpn_Jpan

Figure 16: DVQA [Kafle et al., 2018]

62

(a) eng_Latn

(b) arb_Arab

Figure 17: FigureQA[Kahou et al., 2017]

(a) eng_Latn

(b) fra_Latn

Figure 18: FinQA[Chen et al., 2021]

(a) eng_Latn

(b) zho_Hans

Figure 19: Multihiertt [Zhao et al., 2022]

63

J

Judge Prompt

VLM-as-a-Judge Prompt

System Prompt:
Please act as an impartial judge and evaluate the quality of the responses (Response (A)
and Response (B)) based on the provided instruction.

User Prompt:
Which of the following responses better addresses the given instruction in {language}?
Evaluation Guidelines:
The response should be primarily in {language}.
The evaluation should prioritize accuracy and correctness.
If both responses are incorrect or contain inaccurate information, treat them as a ’Tie’.
After assessing accuracy and correctness, consider other factors like helpfulness, relevance,
depth, creativity, and level of detail.
Do not let the length or order of the responses influence your judgment.
Ensure your evaluation is objective and free from position bias.
Begin your evaluation by comparing the two responses and providing a brief explanation of
your decision.
After your comparison, select one of the following choices as your final decision:
1) Response (A) is significantly better: [[A≫B]]
2) Response (A) is slightly better: [[A>B]]
3) Tie, Response (A) and Response (B) are relatively the same: [[A=B]]
4) Response (B) is slightly better: [[B>A]]
5) Response (B) is significantly better: [[B≫A]]
Instruction: {prompt}
Response (A): {completion_a}
Response (B): {completion_b}
Your response must strictly follow this format:
Explanation: <concise comparison and explanation in English>
Final Decision: <[[B>A]], [[B≫A]], [[A≫B]], [[A>B]], [[A=B]] >

64

LLM-as-a-Judge Prompt

System Prompt:
You are a helpful assistant whose goal is to select the preferred (least wrong) response for a
given instruction in {language}.

User Prompt:
Which of the following responses is the best one for the given instruction in {language}?
A good response should follow these rules:

1) It should be in {language},
2) It should complete the request in the instruction,
3) It should be factually correct and semantically comprehensible,
4) It should be grammatically correct and fluent.
Instruction:{prompt}
Response (A):{completion_a}
Response (B):{completion_b}
FIRST provide a concise comparison of the two responses. If one Response is better, explain
which you prefer and why. If both responses are identical or equally good or bad, explain
why.
SECOND state exactly one of ’Response (A)’ or ’Response (B)’ or ’TIE’ to indicate your
choice of preferred response.
Your response must strictly follow this format:
Comparison: <concise comparison and explanation in English> Preferred: <’Response (A)’
or ’Response (B)’ or ’TIE’>

65

K Breakdown by Language

Aya-Vision-8B

B
8
-
5
.
1
-
h
s
a
l
F
-
i
n
i
m
e
G

s
s
o
L

74.0
77.9
64.4
71.2
70.6
72.6
67.5
64.4
74.8
74.0
67.1
71.4
68.7
70.2
68.8
71.3
68.5
67.0
70.0
62.4
65.3
64.9
68.0
69.3

e
g
a
u
g
n
a
L

eng_Latn
fra_Latn
arb_Arab
tur_Latn
jpn_Jpan
zho_Hans
hin_Deva
vie_Latn
kor_Hang
deu_Latn
ind_Latn
ita_Latn
pol_Latn
por_Latn
rus_Cyrl
spa_Latn
ukr_Cyrl
ces_Latn
nld_Latn
ell_Grek
heb_Hebr
pes_Arab
ron_Latn
avg

n
i
W

25.8
21.9
35.6
28.6
29.0
27.2
32.2
35.6
25.2
25.9
32.7
28.6
30.9
29.8
31.0
28.7
31.5
32.8
29.8
37.4
34.7
35.1
32.0
30.5

e
i
T

0.2
0.2
0.0
0.2
0.4
0.2
0.2
0.0
0.0
0.2
0.2
0.0
0.4
0.0
0.2
0.0
0.0
0.2
0.2
0.2
0.0
0.0
0.0
0.1

n
i
W

44.4
46.6
77.2
67.2
66.6
55.6
70.6
62.2
68.8
56.3
64.9
59.8
63.1
54.4
57.4
55.3
67.9
66.6
58.1
73.6
86.6
71.3
63.2
63.4

-

n
o
i
s
i
V
B
1
1
-
2
.
3
-
a
m
a
l
L

s
s
o
L

54.2
53.2
22.6
32.4
33.2
43.8
29.0
37.6
31.0
43.5
35.1
39.8
36.5
45.2
42.6
44.3
31.5
33.0
41.2
25.8
13.4
28.7
36.6
36.3

B
7
-
L
V
-
5
.
2
-
n
e
w
Q

s
s
o
L

60.4
57.2
25.4
30.0
37.8
54.0
12.2
36.0
33.0
45.5
42.6
47.2
39.9
45.4
47.3
44.6
37.0
36.8
48.3
14.0
13.8
28.1
36.4
37.9

e
i
T

1.4
0.2
0.2
0.4
0.2
0.6
0.5
0.2
0.2
0.2
0.0
0.4
0.4
0.4
0.0
0.4
0.6
0.4
0.6
0.6
0.0
0.0
0.2
0.4

n
i
W

38.8
42.2
74.6
69.4
61.8
45.8
87.4
63.4
65.6
53.5
57.2
52.0
59.7
54.0
52.5
54.6
62.8
62.8
51.7
85.8
86.2
71.5
63.2
61.6

-

D
B
7
-
o
m
l
o
M

s
s
o
L

13.0
11.7
1.2
1.0
2.6
7.8
1.2
3.2
2.8
2.6
2.8
6.2
3.2
5.6
5.6
5.8
1.0
2.0
4.0
0.4
1.0
0.8
2.6
3.8

B
2
1
-
l
a
r
t
x
i
P

s
s
o
L

69.0
70.3
42.5
52.0
63.8
65.8
48.8
55.3
61.2
63.3
58.6
65.2
51.9
62.2
59.2
67.7
43.2
44.0
62.2
41.8
34.7
45.6
52.8
55.7

B
7
-
a
e
g
n
a
P

s
s
o
L

27.2
32.1
20.2
17.2
19.0
25.4
18.9
22.7
21.8
22.0
22.1
21.4
16.2
23.0
24.8
21.5
14.3
13.0
16.3
4.6
17.2
6.2
21.0
19.5

e
i
T

1.2
1.0
0.2
0.6
0.4
0.2
0.5
0.0
0.6
0.6
0.4
0.2
0.6
1.2
1.0
0.4
0.0
0.4
0.4
0.4
0.6
0.2
0.6
0.5

e
i
T

0.4
0.2
0.0
0.6
1.0
0.6
0.5
0.0
0.8
0.4
0.0
0.2
0.6
0.2
0.4
0.4
0.4
0.4
0.0
0.4
0.2
0.0
0.2
0.3

n
i
W

71.6
66.9
79.6
82.2
80.6
74.4
80.6
77.3
77.6
77.3
77.5
78.4
83.2
75.8
74.2
78.1
85.7
86.6
83.3
95.0
82.2
93.6
78.4
80.0

e
i
T

1.0
1.0
0.0
0.0
0.0
0.6
0.0
0.2
0.0
0.4
0.0
0.0
0.2
0.4
0.2
0.2
0.0
0.0
0.0
0.2
0.0
0.4
0.4
0.2

n
i
W

30.6
29.5
57.5
47.4
35.2
33.6
50.7
44.7
38.0
36.3
41.4
34.6
47.5
37.6
40.4
31.9
56.4
55.6
37.8
57.8
65.1
54.4
47.0
44.0

e
i
T

0.8
0.6
0.0
0.6
0.4
0.2
0.5
0.6
1.4
1.0
0.2
0.8
0.4
0.6
0.2
0.8
0.2
0.4
0.0
0.2
0.0
0.4
0.4
0.5

n
i
W

86.0
87.3
98.8
99.0
97.4
91.6
98.8
96.6
97.2
97.0
97.2
93.8
96.6
94.0
94.2
94.0
99.0
98.0
96.0
99.4
99.0
98.8
97.0
95.9

Table 8: Win/Loss/Tie rates by Language for Aya-Vision-8B on m-ArenaHard

66

Aya-Vision-8B

B
8
-
5
.
1
-
h
s
a
l
F
-
i
n
i
m
e
G

s
s
o
L

56.7
31.3
19.4
38.4
44.0
35.1
35.1
36.6
32.8
42.1
37.3
31.3
29.9
36.6
33.6
43.3
32.1
41.0
35.8
30.6
28.4
23.9
32.1
35.1

e
g
a
u
g
n
a
L

eng_Latn
fra_Latn
arb_Arab
tur_Latn
jpn_Jpan
zho_Hans
hin_Deva
vie_Latn
kor_Hang
deu_Latn
spa_Latn
ind_Latn
ita_Latn
pol_Latn
por_Latn
rus_Cyrl
ukr_Cyrl
ces_Latn
nld_Latn
ell_Grek
heb_Hebr
pes_Arab
ron_Latn
avg

n
i
W

27.6
61.2
70.9
53.4
47.0
52.2
58.2
56.0
56.0
48.1
53.7
58.2
61.2
58.2
55.2
50.0
57.5
51.5
53.0
64.9
67.2
67.9
59.0
56.0

e
i
T

15.7
7.5
9.7
8.3
9.0
12.7
6.7
7.5
11.2
9.8
9.0
10.4
9.0
5.2
11.2
6.7
10.4
7.5
11.2
4.5
4.5
8.2
9.0
8.9

n
i
W

50.8
69.4
79.8
75.9
67.2
66.4
79.8
65.7
73.9
66.2
70.2
74.6
71.6
74.6
70.9
63.4
73.9
78.4
67.9
83.6
87.3
75.4
73.1
72.1

-

n
o
i
s
i
V
B
1
1
-
2
.
3
-
a
m
a
l
L

s
s
o
L

30.6
19.4
9.0
18.1
21.6
19.4
14.2
23.9
18.7
24.1
19.4
18.7
18.7
20.1
22.4
25.4
17.9
17.2
20.9
11.9
8.2
17.2
21.6
19.1

B
7
-
L
V
-
5
.
2
-
n
e
w
Q

s
s
o
L

48.5
40.3
30.6
38.4
49.2
55.2
21.6
35.1
32.1
47.4
50.0
35.1
39.5
44.8
38.1
50.0
35.8
41.0
32.1
25.4
18.7
26.9
31.3
37.7

e
i
T

18.7
11.2
11.2
6.0
11.2
14.2
6.0
10.4
7.5
9.8
10.4
6.7
9.7
5.2
6.7
11.2
8.2
4.5
11.2
4.5
4.5
7.5
5.2
8.8

n
i
W

31.3
49.2
61.9
56.4
45.5
35.8
69.4
58.2
54.5
42.9
37.3
59.7
47.0
47.8
49.2
41.8
55.2
51.5
55.2
67.2
73.9
61.9
58.2
52.7

-

D
B
7
-
o
m
l
o
M

s
s
o
L

33.0
23.7
7.6
4.3
13.6
10.2
6.8
13.6
8.5
12.0
20.3
16.1
15.2
4.2
21.2
16.9
8.5
6.8
12.7
2.5
1.7
5.9
8.5
11.9

B
2
1
-
l
a
r
t
x
i
P

s
s
o
L

56.7
51.5
36.6
42.1
47.0
44.8
50.0
46.3
47.0
58.6
50.0
35.1
39.5
44.8
38.1
50.0
35.8
41.0
32.1
25.4
18.7
26.9
31.3
41.3

B
7
-
a
e
g
n
a
P

s
s
o
L

26.9
17.9
20.9
16.5
18.7
23.1
21.6
20.9
14.2
21.1
23.9
25.4
23.1
16.4
15.7
18.7
16.4
12.7
18.7
8.2
17.9
9.7
20.9
18.7

e
i
T

17.2
11.2
12.7
13.5
15.7
17.2
9.7
6.7
9.7
9.8
11.2
9.0
10.4
11.2
11.2
13.4
9.0
11.2
11.9
8.2
6.7
7.5
10.4
11.0

e
i
T

9.7
10.4
5.2
5.3
10.4
14.9
4.5
5.2
10.4
7.5
12.7
5.2
13.4
7.5
12.7
8.2
9.0
7.5
12.7
7.5
7.5
11.2
10.4
9.1

n
i
W

56.0
70.9
66.4
69.9
65.7
59.7
68.7
72.4
76.1
69.2
64.9
65.7
66.4
72.4
73.1
67.9
74.6
76.1
69.4
83.6
75.4
82.8
68.7
70.3

e
i
T

18.6
8.5
8.5
10.3
13.6
10.2
7.6
6.8
11.9
10.3
14.4
5.1
11.9
8.5
12.7
12.7
7.6
5.1
7.6
2.5
7.6
9.3
8.5
9.6

n
i
W

33.6
38.1
58.2
52.6
42.5
40.3
45.5
48.5
42.5
33.8
37.3
59.7
47.0
47.8
49.2
41.8
55.2
51.5
55.2
67.2
73.9
61.9
58.2
49.6

e
i
T

20.1
10.4
7.5
5.3
5.2
9.0
9.0
6.7
13.4
9.8
12.7
5.2
13.4
7.5
12.7
8.2
9.0
7.5
12.7
7.5
7.5
11.2
10.4
9.6

n
i
W

48.3
67.8
83.9
85.5
72.9
79.7
85.6
79.7
79.7
77.8
65.2
78.8
72.9
87.3
66.1
70.3
83.9
88.1
79.7
94.9
90.7
84.8
83.0
78.5

Table 9: Win/Loss/Tie rates by Language for Aya-Vision-8B on AyaVisionBench

67

Aya-Vision-8B

B
8
-
5
.
1
-
h
s
a
l
F
-
i
n
i
m
e
G

s
s
o
L

53.4
36.6
19.4
32.4
33.2
29.8
26.8
26.1
29.6
39.6
37.3
31.3
33.2
32.5
31.0
32.8
34.3
30.0
33.6
22.0
26.0
19.8
31.9
31.4

e
g
a
u
g
n
a
L

eng_Latn
fra_Latn
arb_Arab
tur_Latn
jpn_Jpan
zho_Hans
hin_Deva
vie_Latn
kor_Hang
deu_Latn
spa_Latn
ind_Latn
ita_Latn
pol_Latn
por_Latn
rus_Cyrl
ukr_Cyrl
ces_Latn
nld_Latn
ell_Grek
heb_Hebr
pes_Arab
ron_Latn
avg

n
i
W

42.2
61.2
70.9
63.6
63.2
65.6
69.7
70.5
66.0
57.8
53.7
58.2
62.0
62.7
62.0
65.0
62.5
63.4
63.0
75.2
70.0
76.8
63.1
64.5

e
i
T

4.4
3.6
9.7
4.0
3.6
4.6
3.4
3.4
4.4
2.6
9.0
10.5
4.8
4.8
7.0
2.2
3.2
6.6
3.4
2.8
4.0
3.4
5.0
4.0

n
i
W

59.8
74.4
84.8
83.0
81.7
77.2
83.2
78.0
86.2
75.0
71.1
78.2
73.8
80.2
74.2
81.9
82.4
79.2
77.8
84.4
85.2
88.2
78.4
79.1

-

n
o
i
s
i
V
B
1
1
-
2
.
3
-
a
m
a
l
L

s
s
o
L

37.4
22.0
13.0
14.4
13.5
18.0
15.0
19.4
10.4
20.6
25.1
17.6
22.2
16.2
21.6
14.3
13.2
15.0
17.6
12.6
11.2
9.4
15.8
17.2

B
7
-
L
V
-
5
.
2
-
n
e
w
Q

s
s
o
L

58.4
49.4
30.6
38.4
48.3
49.6
18.5
37.7
32.1
47.4
50.0
35.8
45.8
40.1
45.4
41.3
37.1
36.4
43.0
23.2
18.8
24.7
35.1
38.4

e
i
T

2.8
3.6
2.2
2.6
4.8
4.8
1.8
2.6
3.4
4.4
3.8
4.2
4.0
3.6
4.2
3.8
4.4
5.8
4.6
3.0
3.6
2.4
5.8
3.8

n
i
W

37.4
49.2
61.9
56.4
47.1
46.6
78.3
59.3
54.5
42.9
37.3
59.0
49.4
56.5
48.4
56.1
58.3
60.0
52.8
73.8
77.8
72.3
60.3
57.5

-

D
B
7
-
o
m
l
o
M

s
s
o
L

35.0
26.2
22.6
4.3
20.9
28.4
6.8
13.6
8.5
12.0
20.3
7.2
10.8
5.4
21.2
8.7
4.6
6.8
6.0
3.2
4.6
3.6
6.4
15.3

B
2
1
-
l
a
r
t
x
i
P

s
s
o
L

49.0
45.2
29.2
42.1
41.3
44.6
50.0
46.3
47.0
58.7
50.0
35.2
41.4
34.1
41.8
40.2
25.9
30.8
37.8
20.8
25.0
19.0
30.9
35.7

B
7
-
a
e
g
n
a
P

s
s
o
L

35.0
17.9
22.6
16.5
20.9
28.4
21.6
17.2
14.2
21.1
23.9
27.2
23.2
18.6
25.6
23.9
16.2
14.6
18.8
7.4
22.6
10.0
27.7
22.1

e
i
T

6.0
11.2
5.4
13.5
5.8
5.2
9.7
4.6
9.7
9.8
11.2
7.0
5.4
3.6
7.6
5.2
3.6
5.0
4.4
2.6
4.2
3.6
4.0
4.8

e
i
T

4.8
5.0
3.0
5.3
5.0
4.0
4.5
5.2
10.4
7.5
12.7
8.2
5.2
2.8
7.6
3.4
4.2
5.4
5.2
4.2
4.6
4.2
5.4
5.0

n
i
W

59.0
70.9
72.0
69.9
73.2
66.4
68.7
78.2
76.1
69.2
64.9
65.8
71.4
77.8
66.8
70.8
80.2
80.4
76.8
90.0
73.2
86.4
68.3
73.1

e
i
T

6.0
4.0
5.4
10.3
5.8
5.2
7.6
6.8
11.9
10.3
14.4
3.4
4.4
4.6
12.7
5.4
2.8
5.4
3.0
1.6
3.4
3.0
4.4
4.5

n
i
W

46.2
49.8
67.8
52.6
53.7
51.4
45.5
48.5
42.5
33.8
37.3
56.6
53.4
63.1
50.6
56.3
69.9
63.8
57.0
75.0
70.4
76.8
63.7
59.4

e
i
T

4.2
3.4
7.5
5.3
4.6
3.8
3.2
3.0
13.4
9.8
12.7
5.2
4.8
3.4
6.2
2.6
4.6
3.6
4.2
3.0
3.4
3.0
4.6
4.1

n
i
W

59.0
69.8
72.0
85.5
73.2
79.7
85.6
79.7
79.7
77.8
65.3
89.4
84.8
90.0
66.1
85.9
92.6
88.0
91.0
95.2
92.0
93.4
89.2
80.3

Table 10: Win/Loss/Tie rates by Language for Aya-Vision-8B on m-WildVision

68

Language Llama-3.2-90B-Vision

Molmo-72B

Qwen-2.5-VL-72B

Win Loss

Tie

Win Loss Tie Win Loss Tie

Aya-Vision-32B

eng_Latn
fra_Latn
hin_Deva
arb_Arab
tur_Latn
jpn_Jpan
zho_Hans
vie_Latn
kor_Hang
deu_Latn
ind_Latn
ita_Latn
pol_Latn
por_Latn
rus_Cyrl
spa_Latn
ukr_Cyrl
ces_Latn
nld_Latn
ell_Grek
heb_Hebr
pes_Arab
ron_Latn
avg

26.2
39.6
47.4
54.2
45.2
47.2
42.8
41.8
51.6
40.4
39.8
41.0
42.2
35.2
40.0
38.8
44.6
45.6
42.0
46.2
51.2
51.0
40.4
43.2

73.6
60.4
52.0
45.2
54.4
52.4
57.0
58.0
48.4
59.6
59.8
59.0
57.6
64.6
60.0
60.8
55.2
54.2
57.2
53.6
48.6
48.8
59.2
56.5

0.2
0.0
0.6
0.6
0.4
0.4
0.2
0.2
0.0
0.0
0.4
0.0
0.2
0.2
0.0
0.4
0.2
0.2
0.8
0.2
0.2
0.2
0.4
0.3

66.0
72.2
86.0
81.4
78.6
84.2
75.2
77.0
78.6
78.6
76.4
75.2
75.4
70.6
66.8
69.2
80.0
75.6
76.8
84.2
85.8
84.4
78.8
77.3

32.8
27.6
14.0
18.6
20.8
15.8
24.6
22.6
21.2
21.0
23.2
24.2
24.0
29.0
33.0
30.6
20.0
24.4
23.2
15.4
14.0
15.0
21.0
22.4

1.2
0.2
0.0
0.0
0.6
0.0
0.2
0.4
0.2
0.4
0.4
0.6
0.6
0.4
0.2
0.2
0.0
0.0
0.0
0.4
0.2
0.6
0.2
0.3

35.8
46.8
69.2
59.6
51.4
54.8
43.6
55.0
56.4
47.4
49.2
38.2
43.4
44.6
47.6
45.4
48.0
53.0
46.8
62.4
63.4
57.6
51.6
50.9

63.6
52.8
30.8
40.4
48.2
44.6
55.6
44.8
43.6
51.8
50.4
61.2
56.4
55.4
52.0
54.0
51.8
47.0
52.6
37.2
36.6
42.4
48.2
48.8

0.6
0.4
0.0
0.0
0.4
0.6
0.8
0.2
0.0
0.8
0.4
0.6
0.2
0.0
0.4
0.6
0.2
0.0
0.6
0.4
0.0
0.0
0.2
0.3

Table 11: Win/Loss/Tie rates by Language for Aya-Vision-32B on m-ArenaHard

69

Language Llama-3.2-90B-Vision

Molmo-72B

Qwen-2.5-VL-72B

Aya-Vision-32B

eng_Latn
fra_Latn
hin_Deva
arb_Arab
tur_Latn
jpn_Jpan
zho_Hans
vie_Latn
kor_Hang
deu_Latn
ind_Latn
ita_Latn
pol_Latn
por_Latn
rus_Cyrl
spa_Latn
ukr_Cyrl
ces_Latn
nld_Latn
ell_Grek
heb_Hebr
pes_Arab
ron_Latn
avg

Win Loss

49.25
64.93
74.63
70.90
63.91
61.94
65.67
64.93
64.93
69.92
68.66
62.69
74.63
52.99
60.45
61.19
75.37
73.88
64.93
66.42
68.66
70.90
64.18
65.91

38.81
24.63
23.13
19.40
30.08
28.36
28.36
24.63
28.36
21.80
26.87
29.85
20.90
41.79
29.10
29.85
20.90
20.15
24.63
26.12
24.63
23.88
31.34
26.85

Tie

11.94
10.45
2.24
9.70
6.02
9.70
5.97
10.45
6.72
8.27
4.48
7.46
4.48
5.22
10.45
8.96
3.73
5.97
10.45
7.46
6.72
5.22
4.48
7.24

Win Loss Tie Win Loss Tie

35.82
53.73
72.39
73.13
64.66
61.94
66.42
50.75
58.96
60.15
56.72
55.97
65.67
51.49
50.75
52.99
61.94
67.91
52.24
78.36
68.66
78.36
68.66
61.20

54.48
39.55
25.37
20.90
30.08
35.82
26.87
42.54
33.58
33.83
37.31
35.07
28.36
42.54
40.30
37.31
32.84
27.61
42.54
17.91
26.87
18.66
26.87
32.92

9.70
6.72
2.24
5.97
5.26
2.24
6.72
6.72
7.46
6.02
5.97
8.96
5.97
5.97
8.96
9.70
5.22
4.48
5.22
3.73
4.48
2.99
4.48
5.88

62.69
49.25
35.82
44.03
52.63
48.51
44.03
52.99
44.78
48.87
47.76
52.99
48.51
54.48
50.75
50.75
50.75
50.75
50.00
38.81
42.54
46.27
47.01
48.48

24.63
42.54
61.19
47.76
44.36
45.52
46.27
41.04
44.78
48.12
44.78
39.55
45.52
36.57
41.04
43.28
43.28
46.27
45.52
51.49
51.49
50.00
45.52
44.81

12.69
8.21
2.99
8.21
3.01
5.97
9.70
5.97
10.45
3.01
7.46
7.46
5.97
8.96
8.21
5.97
5.97
2.99
4.48
9.70
5.97
3.73
7.46
6.72

Table 12: Win/Loss/Tie rates by Language for Aya-Vision-32B on AyaVisionBench

70

Language Qwen-2.5-VL-72B Llama-3.2-90B-Vision

Molmo-72B

Win Loss Tie Win Loss

Tie

Win Loss Tie

Aya-Vision-32B

eng_Latn
fra_Latn
hin_Deva
arb_Arab
tur_Latn
jpn_Jpan
zho_Hans
vie_Latn
kor_Hang
deu_Latn
ind_Latn
ita_Latn
pol_Latn
por_Latn
rus_Cyrl
spa_Latn
ukr_Cyrl
ces_Latn
nld_Latn
ell_Grek
heb_Hebr
pes_Arab
ron_Latn
avg

37.4
46.2
67.4
57.4
56.0
49.0
39.0
57.4
55.4
49.2
51.0
46.2
50.8
49.2
50.2
48.6
58.4
54.4
47.6
66.6
66.0
64.4
58.0
53.3

56.4
50.0
30.6
39.2
39.6
46.4
56.4
38.6
40.8
46.4
45.8
49.0
46.8
45.8
47.2
46.6
38.8
42.2
48.8
30.2
30.6
30.8
39.2
42.9

6.2
3.8
2.0
3.4
4.4
4.6
4.6
4.0
3.8
4.4
3.2
4.8
2.4
5.0
2.6
4.8
2.8
3.4
3.6
3.2
3.4
4.8
2.8
3.8

67.6
69.9
78.4
79.0
77.8
72.2
77.0
76.6
75.4
67.0
72.0
69.8
73.6
68.2
73.2
65.2
74.4
69.6
69.4
75.0
74.2
80.6
73.6
73.0

29.2
26.4
17.6
17.8
19.0
25.4
19.0
21.4
21.0
28.6
26.0
26.2
23.4
26.8
23.6
30.6
21.4
27.2
25.8
22.0
22.8
16.6
24.4
23.6

3.2
3.6
4.0
3.2
3.2
2.4
4.0
2.0
3.6
4.4
2.0
4.0
3.0
5.0
3.2
4.2
4.2
3.2
4.8
3.0
3.0
2.8
2.0
3.4

56.2
59.0
75.6
79.2
76.5
76.2
78.0
64.2
70.4
68.0
65.2
59.0
67.2
61.2
60.3
57.0
70.6
67.6
61.4
84.2
74.0
77.6
74.6
68.8

39.2
37.2
20.0
16.8
20.5
20.2
19.6
31.6
25.2
28.0
30.0
33.8
29.0
33.6
36.3
37.8
25.4
28.8
33.8
11.8
22.4
18.4
21.8
27.0

4.6
3.8
4.4
4.0
3.0
3.6
2.4
4.2
4.4
4.0
4.8
7.2
3.8
5.2
3.4
5.2
4.0
3.6
4.8
4.0
3.6
4.0
3.6
4.2

Table 13: Win/Loss/Tie rates by Language for Aya-Vision-32B on m-WildVision.

eng_Latn fra_Latn heb_Hebr hin_Deva

ron_Latn tha_Thai

zho_Hans

Pangea-7B
Molmo-7B-D
Llama-3.2-11B-Vision
Pixtral-12B
Qwen-2.5-VL-7B
Aya-Vision-8B

Molmo-72B
Llama-3.2-90B-Vision
Qwen-2.5-VL-72B
Aya-Vision-32B

55.30
68.09
56.03
57.20
57.98
57.59

59.92
75.00
55.25
55.64

43.60
54.17
45.08
43.56
52.65
54.92

54.92
67.05
49.62
60.61

59.30
34.29
31.07
40.00
54.29
58.57

58.21
59.64
62.86
66.43

53.50
31.92
45.00
55.38
54.62
66.92

62.69
70.38
66.15
71.54

45.80
30.28
38.38
41.20
44.72
54.93

50.70
59.51
46.13
57.75

67.20
53.73
42.16
55.97
67.16
33.21

65.30
68.66
74.25
43.07

50.20
46.21
20.22
29.24
51.62
56.32

47.29
53.43
58.48
61.73

avg

53.56
45.53
39.71
46.08
54.72
54.64

57.01
64.81
58.96
59.54

Table 14: MaxM

71

fra_Latn jpn_Jpan ind_Latn por_Latn hin_Deva

arb_Arab eng_Latn

Pangea-7B
Molmo-7B-D
Llama-3.2-11B-Vision
Pixtral-12B
Qwen-2.5-VL-7B
Aya-Vision-8B

Molmo-72B
Llama-3.2-90B-Vision
Qwen-2.5-VL-72B
Aya-Vision-32B

45.30
38.90
43.30
47.00
49.70
40.20

52.80
56.60
62.40
44.90

40.50
37.10
40.90
43.90
46.10
41.40

49.00
52.90
60.60
42.90

46.50
38.90
42.10
40.10
47.80
39.50

52.80
55.20
64.00
46.60

46.10
38.10
44.10
47.80
49.80
38.50

55.40
54.30
62.00
45.30

41.60
34.90
39.90
32.60
41.20
38.10

48.00
46.60
60.80
45.00

42.30
36.70
41.60
36.20
41.70
40.10

51.20
45.00
59.70
44.10

45.70
40.50
47.20
48.30
51.10
41.80

51.50
56.20
62.70
47.00

Table 15: xMMMU

arb_Arab deu_Latn fra_Latn ita_Latn jpn_Jpan kor_Hang

rus_Cyrl

vie_Latn tha_Thai

Pangea-7B
Molmo-7B-D
Llama-3.2-11B-Vision
Pixtral-12B
Qwen-2.5-VL-7B
Aya-Vision-8B

Molmo-72B
Llama-3.2-90B-Vision
Qwen-2.5-VL-72B
Aya-Vision-32B

8.53
5.83
7.97
7.68
19.26
13.69

6.54
19.91
23.19
116.33

29.96
26.24
24.24
32.54
35.31
28.72

30.34
36.35
35.78
34.83

32.39
35.67
27.99
37.92
42.66
35.89

35.44
40.29
43.91
40.52

23.87
29.86
22.85
32.69
36.76
28.39

30.54
35.29
39.14
32.20

9.30
7.61
10.75
8.33
21.98
10.51

9.42
17.27
21.98
15.03

13.44
9.86
13.08
13.08
32.80
13.08

10.04
30.11
35.66
14.57

7.67
5.03
7.01
7.14
10.45
6.35

8.73
10.98
12.83
10.28

21.38
15.05
17.31
19.12
37.33
17.99

18.21
29.30
42.87
23.91

15.15
15.15
16.88
14.29
22.51
7.79

17.32
25.97
27.27
11.45

Table 16: MTVQA

hin_Deva

ind_Latn kor_Hang

spa_Latn eng_Latn zho_Hans

jpn_Jpan

Pangea-7B
Molmo-7B-D
Llama-3.2-11B-Vision
Pixtral-12B
Qwen-2.5-VL-7B
Aya-Vision-8B

Molmo-72B
Llama-3.2-90B-Vision
Qwen-2.5-VL-72B
Aya-Vision-32B

29.00
4.00
13.00
50.50
20.50
56.50

19.5
38.50
44.50
68.50

36.50
24.50
35.50
66.50
58.50
60.50

53.5
54.50
77.00
72.00

28.50
8.50
13.78
60.00
53.00
56.00

27.0
42.35
71.94
62.50

34.00
42.50
43.00
72.50
66.50
60.00

64.5
60.50
80.50
77.00

26.50
65.50
55.50
74.00
78.00
60.50

65.5
63.00
82.00
72.50

36.00
2.00
23.00
64.00
71.50
55.50

42.5
53.00
71.00
66.50

35.00
16.50
16.33
64.00
59.00
61.50

45.5
46.00
71.00
71.50

Table 17: xChatBench

avg

44.00
37.87
42.73
42.27
46.77
39.94

51.53
52.40
61.74
45.11

avg

17.97
16.70
16.45
19.20
28.78
18.05

18.51
27.28
31.40
22.12

avg

32.21
23.36
28.59
64.50
58.14
58.64

45.43
51.12
71.13
70.07

tha_Thai

tel_Telu ben_Beng

eng_Latn spa_Latn jpn_Jpan zho_Hans

swh_Latn deu_Latn rus_Cyrl

fra_Latn

Pangea-7B
Molmo-7B-D
Llama-3.2-11B-Vision
Pixtral-12B
Qwen-2.5-VL-7B
Aya-Vision-8B

Molmo-72B
Llama-3.2-90B-Vision
Qwen-2.5-VL-72B
Aya-Vision-32B

49.60
24.50
64.26
63.86
58.44
12.45

79.52
84.34
87.95
39.36

5.60
2.41
6.88
36.55
4.42
0.00

11.65
7.63
13.25
0.00

0.00
6.02
18.88
57.83
37.75
6.83

55.82
26.51
64.26
14.46

82.00
73.90
84.74
89.16
85.14
84.34

96.39
96.39
95.18
87.95

74.8
39.36
71.89
82.73
43.37
77.91

89.56
26.91
93.17
82.33

22.00
41.77
55.24
64.66
61.85
67.87

69.08
81.53
86.35
75.50

68.00
58.06
73.90
73.90
72.29
74.70

86.35
77.91
91.16
80.32

54.0
0.00
56.63
23.69
4.09
4.90

57.03
82.73
65.06
23.69

68.4
52.61
76.31
79.92
74.30
75.90

88.76
89.96
89.52
81.53

68.0
47.79
77.11
78.71
63.27
80.72

90.76
87.95
91.57
76.31

63.2
36.14
70.68
74.30
26.10
73.49

81.12
6.02
80.32
72.29

avg

50.51
34.78
59.68
65.94
48.27
50.83

73.27
60.72
77.98
57.61

Table 18: MGSM

72

B
2
3
-
n
o
i
s
i
V
-
a
y
A

B
2
7
-
L
V
-
5
.
2
-
n
e
w
Q

-

n
o
i
s
i
V
B
0
9
-
2
.
3
-
a
m
a
l
L

B
2
7
-
o
m
l
o
M

B
8
-
n
o
i
s
i
V
-
a
y
A

B
7
-
L
V
-
5
.
2
-
n
e
w
Q

B
2
1
-
l
a
r
t
x
i
P

-

n
o
i
s
i
V
B
1
1
-
2
.
3
-
a
m
a
l
L

-

D
B
7
-
o
m
l
o
M

B
7
-
a
e
g
n
a
P

0
5
.
6
3

1
9
.
2
6

0
5
.
7
6

5
2
.
4
6

5
7
.
8
6

5
2
.
2
6

0
5
.
1
6

0
5
.
8
4

5
2
.
9
6

0
5
.
5
6

5
2
.
2
4

0
5
.
7
6

0
0
.
8
6

0
0
.
9
2

5
2
.
3
6

6
4
.
8
5

5
2
.
4
5

0
0
.
1
8

0
5
.
2
8

5
7
.
9
7

0
0
.
2
8

5
7
.
3
8

5
7
.
0
8

1
9
.
3
7

5
7
.
7
8

5
2
.
1
8

5
7
.
5
7

4
1
.
7
7

6
9
.
2
8

0
5
.
7
3

5
2
.
3
8

3
2
.
6
7

5
7
.
7
5

0
0
.
0
8

0
5
.
8
7

0
5
.
5
7

5
2
.
0
8

0
5
.
4
8

5
7
.
3
7

0
0
.
1
6

5
7
.
3
8

0
5
.
1
8

0
5
.
1
7

0
5
.
4
7

5
2
.
2
6

0
5
.
0
4

0
5
.
3
8

8
5
.
2
7

5
7
.
2
5

0
5
.
3
7

0
5
.
7
6

5
2
.
3
7

5
7
.
7
7

5
7
.
4
7

5
2
.
3
6

0
5
.
4
6

5
2
.
4
7

5
7
.
4
7

5
7
.
6
6

5
2
.
7
5

0
5
.
2
7

0
5
.
5
3

5
7
.
6
7

0
0
.
7
6

0
0
.
9
2

5
2
.
5
6

5
7
.
9
5

0
5
.
6
5

5
7
.
7
6

0
0
.
5
6

5
7
.
3
6

5
2
.
0
4

0
0
.
1
7

5
7
.
8
5

0
0
.
5
5

0
0
.
9
5

0
5
.
3
6

5
7
.
9
2

0
0
.
5
6

2
6
.
6
5

0
5
.
3
3

5
7
.
8
6

5
7
.
1
6

5
2
.
1
6

5
7
.
4
6

5
7
.
5
6

8
0
.
6
6

5
2
.
3
5

3
4
.
2
7

6
4
.
1
6

0
0
.
4
5

3
0
.
2
6

7
1
.
8
6

0
0
.
0
3

3
4
.
1
7

4
6
.
9
5

6
3
.
4
4

0
0
.
9
6

0
9
.
9
5

5
7
.
4
6

0
5
.
7
6

0
1
.
9
6

9
0
.
8
6

5
7
.
5
5

4
9
.
4
7

0
0
.
9
5

5
5
.
9
5

0
5
.
2
6

5
7
.
8
6

5
5
.
9
2

3
0
.
0
7

2
5
.
1
6

U
L
M
M

l
a
b
o
l
g

:
9
1

e
l
b
a
T

5
7
.
9
2

5
7
.
6
6

0
0
.
1
5

5
7
.
0
5

0
5
.
6
6

5
2
.
4
6

0
5
.
3
6

5
2
.
0
3

5
2
.
1
7

5
7
.
4
6

0
5
.
8
4

0
5
.
2
5

0
5
.
4
6

5
2
.
5
1

5
7
.
4
6

2
6
.
3
5

5
7
.
2
2

5
2
.
4
4

0
0
.
2
3

0
0
.
3
3

0
1
.
1
4

0
0
.
4
4

0
0
.
5
4

5
2
.
9
2

0
0
.
9
4

0
0
.
6
3

0
5
.
2
3

5
7
.
3
3

5
2
.
4
4

0
0
.
7
2

5
7
.
0
4

7
9
.
6
3

5
2
.
9
3

5
2
.
4
5

5
7
.
9
3

5
7
.
6
4

0
0
.
4
5

5
7
.
5
5

5
7
.
3
5

5
2
.
0
4

0
0
.
5
6

5
7
.
7
4

0
0
.
9
3

5
7
.
8
3

0
0
.
5
4

5
2
.
0
2

0
5
.
2
5

3
1
.
6
4

n
t
a
L
_
h
w
s

n
t
a
L
_
a
p
s

n
a
p
J
_
n
p
j

g
n
a
H
_
r
o
k

n
t
a
L
_
u
e
d

n
t
a
L
_
r
o
p

s
n
a
H
_
o
h
z

g
n
e
B
_
n
e
b

n
t
a
L
_
g
n
e

n
t
a
L
_
d
n
i

a
v
e
D
_
n
i
h

b
a
r
A
_
b
r
a

n
t
a
L
_
a
r
f

n
t
a
L
_
r
o
y

n
t
a
L
_
a
t
i

g
v
a

73

B
2
3
-
n
o
i
s
i
V
-
a
y
A

B
2
7
-
L
V
-
5
.
2
-
n
e
w
Q

-

n
o
i
s
i
V
B
0
9
-
2
.
3
-
a
m
a
l
L

B
2
7
-
o
m
l
o
M

B
8
-
n
o
i
s
i
V
-
a
y
A

B
7
-
L
V
-
5
.
2
-
n
e
w
Q

B
2
1
-
l
a
r
t
x
i
P

-

n
o
i
s
i
V
B
1
1
-
2
.
3
-
a
m
a
l
L

-

D
B
7
-
o
m
l
o
M

B
7
-
a
e
g
n
a
P

3
9
.
8
3

5
8
.
1
4

0
3
.
2
5

0
1
.
9
2

9
3
.
0
3

7
1
.
2
5

9
1
.
6
3

0
8
.
8
3

7
5
.
4
3

6
4
.
4
4

7
1
.
2
3

9
9
.
1
3

7
1
.
4
3

8
3
.
0
4

5
3
.
0
3

6
4
.
6
3

6
0
.
7
4

5
4
.
4
4

4
4
.
7
2

3
5
.
8
3

0
2
.
3
3

0
4
.
6
3

9
7
.
7
3

7
1
.
6
3

2
0
.
2
3

3
9
.
3
5

8
5
.
9
2

6
9
.
4
2

3
8
.
2
5

6
0
.
3
3

8
4
.
0
4

1
4
.
8
3

7
3
.
5
4

3
0
.
1
3

7
5
.
7
2

0
1
.
2
3

7
1
.
1
4

9
3
.
8
2

0
7
.
5
2

5
5
.
1
4

8
4
.
3
4

3
2
.
6
2

1
7
.
6
3

3
6
.
1
3

9
2
.
3
3

1
7
.
5
3

8
7
.
6
3

7
8
.
0
4

3
3
.
4
5

3
2
.
8
2

5
4
.
4
3

1
8
.
3
5

0
9
.
4
3

7
6
.
9
3

4
7
.
5
3

9
8
.
5
4

4
8
.
0
3

1
7
.
3
3

1
0
.
7
3

8
8
.
1
4

7
2
.
0
3

7
7
.
3
3

2
8
.
7
4

2
6
.
5
4

2
9
.
5
2

1
8
.
0
4

1
4
.
3
3

5
8
.
5
3

5
2
.
8
3

5
0
.
2
3

2
5
.
0
3

9
6
.
0
5

9
7
.
5
2

0
1
.
3
2

4
8
.
9
4

4
3
.
2
3

3
4
.
7
3

7
5
.
6
3

4
9
.
9
3

2
3
.
0
3

3
7
.
4
2

5
9
.
6
2

9
2
.
7
3

3
0
.
6
2

8
6
.
0
2

5
8
.
5
3

9
4
.
1
4

7
3
.
3
2

6
2
.
3
3

9
5
.
0
3

5
5
.
6
2

2
5
.
2
3

2
2
.
8
3

5
2
.
8
3

1
4
.
1
5

5
9
.
6
2

3
1
.
9
2

2
4
.
1
5

0
6
.
3
3

2
2
.
7
3

8
2
.
3
3

9
2
.
3
4

1
1
.
1
3

1
3
.
0
3

9
9
.
0
3

5
1
.
0
4

6
5
.
8
2

6
0
.
4
3

1
5
.
3
4

7
9
.
0
4

6
9
.
5
2

5
2
.
6
3

7
3
.
1
3

7
7
.
3
3

0
9
.
5
3

9
7
.
4
2

2
9
.
9
1

9
6
.
7
4

8
9
.
2
2

7
3
.
3
1

7
3
.
5
4

9
0
.
8
2

8
2
.
2
3

1
0
.
4
3

6
7
.
5
3

1
4
.
7
2

7
3
.
8
1

6
1
.
2
2

0
2
.
5
3

7
6
.
2
2

8
2
.
7
1

8
7
.
1
3

3
7
.
6
3

1
0
.
8
1

9
5
.
8
2

7
1
.
7
2

2
0
.
6
2

8
9
.
7
2

0
9
.
1
2

8
6
.
3
2

8
8
.
0
5

8
0
.
9
1

8
8
.
0
2

8
6
.
9
4

1
0
.
2
3

3
5
.
6
3

4
6
.
4
2

3
3
.
5
3

9
5
.
9
2

4
9
.
0
2

0
5
.
1
2

9
2
.
2
3

7
5
.
2
2

3
6
.
2
2

1
9
.
3
3

3
3
.
1
4

0
0
.
9
1

0
7
.
9
2

0
0
.
6
2

1
4
.
0
3

9
2
.
9
2

s
e
r
o
fl

:
0
2

e
l
b
a
T

2
6
.
6
2

2
3
.
8
2

4
2
.
9
4

0
2
.
2
2

5
0
.
7
2

9
7
.
8
4

0
4
.
1
3

8
5
.
3
3

2
8
.
8
2

6
6
.
9
3

3
3
.
8
2

3
4
.
7
2

6
3
.
7
2

8
9
.
6
3

9
5
.
5
2

3
2
.
6
2

7
1
.
0
4

9
5
.
9
3

6
5
.
0
2

7
9
.
3
3

4
9
.
8
2

6
5
.
9
2

4
8
.
1
3

6
2
.
1
1

7
0
.
1
1

2
5
.
1
3

0
5
.
1
1

0
2
.
6

9
4
.
5
3

6
3
.
9
1

1
3
.
2
2

2
2
.
1
2

5
0
.
0
2

5
1
.
1
2

6
4
.
8

3
2
.
8

8
1
.
0
2

4
2
.
1
1

4
1
.
5

3
8
.
5
1

4
5
.
1
2

9
6
.
8

4
3
.
2
1

7
6
.
5
1

0
9
.
7

4
7
.
5
1

0
5
.
7
2

6
3
.
7
2

1
0
.
7
4

1
7
.
2
2

6
2
.
0
2

8
6
.
6
4

2
6
.
8
2

8
0
.
1
3

3
5
.
1
3

6
4
.
0
4

7
8
.
7
2

0
6
.
4
1

2
8
.
5
2

5
5
.
5
3

9
8
.
9
1

7
2
.
2
1

9
3
.
7
3

5
4
.
4
3

6
7
.
8
1

5
8
.
3
2

2
0
.
4
2

4
2
.
9
1

4
0
.
8
2

b
a
r
A
_
b
r
a
>
-
n
t
a
L
_
g
n
e

r
b
e
H
_
b
e
h
>
-
n
t
a
L
_
g
n
e

n
t
a
L
_
r
o
p
>
-
n
t
a
L
_
g
n
e

n
a
p
J
_
n
p
j
>
-
n
t
a
L
_
g
n
e

a
v
e
D
_
n
i
h
>
-
n
t
a
L
_
g
n
e

n
t
a
L
_
a
r
f
>
-
n
t
a
L
_
g
n
e

n
t
a
L
_
a
t
i
>
-
n
t
a
L
_
g
n
e

l
r
y
C
_
s
u
r
>
-
n
t
a
L
_
g
n
e

s
n
a
H
_
o
h
z
>
-
n
t
a
L
_
g
n
e

n
t
a
L
_
d
n
i
>
-
n
t
a
L
_
g
n
e

n
t
a
L
_
a
p
s
>
-
n
t
a
L
_
g
n
e

b
a
r
A
_
s
e
p
>
-
n
t
a
L
_
g
n
e

n
t
a
L
_
r
u
t
>
-
n
t
a
L
_
g
n
e

n
t
a
L
_
e
i
v
>
-
n
t
a
L
_
g
n
e

n
t
a
L
_
l
o
p
>
-
n
t
a
L
_
g
n
e

k
e
r
G
_

l
l
e
>
-
n
t
a
L
_
g
n
e

n
t
a
L
_
n
o
r
>
-
n
t
a
L
_
g
n
e

n
t
a
L
_
u
e
d
>
-
n
t
a
L
_
g
n
e

g
n
a
H
_
r
o
k
>
-
n
t
a
L
_
g
n
e

n
t
a
L
_
s
e
c
>
-
n
t
a
L
_
g
n
e

n
t
a
L
_
d
l
n
>
-
n
t
a
L
_
g
n
e

l
r
y
C
_
r
k
u
>
-
n
t
a
L
_
g
n
e

g
v
a

74

B
2
3
-
n
o
i
s
i
V
-
a
y
A

B
2
7
-
L
V
-
5
.
2
-
n
e
w
Q

-

n
o
i
s
i
V
B
0
9
-
2
.
3
-
a
m
a
l
L

B
2
7
-
o
m
l
o
M

B
8
-
n
o
i
s
i
V
-
a
y
A

B
7
-
L
V
-
5
.
2
-
n
e
w
Q

B
2
1
-
l
a
r
t
x
i
P

-

n
o
i
s
i
V
B
1
1
-
2
.
3
-
a
m
a
l
L

-

D
B
7
-
o
m
l
o
M

B
7
-
a
e
g
n
a
P

3
1
.
6
5

8
1
.
6
6

0
0
.
8
3

5
7
.
1
6

3
5
.
2
5

4
2
.
5
7

0
7
.
7
6

8
6
.
1
6

1
1
.
8
7

5
8
.
5
7

0
0
.
0
8

3
9
.
3
6

4
3
.
6
6

2
7
.
9
7

7
6
.
1
7

8
8
.
7
6

0
9
.
1
6

1
0
.
8
7

2
2
.
6
6

5
4
.
6
3

1
3
.
4
6

9
4
.
6
5

8
1
.
9
2

8
3
.
2
7

7
4
.
8
6

9
7
.
7
5

3
4
.
1
7

7
0
.
7
8

3
4
.
0
4

6
5
.
5
5

7
1
.
4
7

4
4
.
9
6

1
1
.
9
5

6
3
.
9
3

6
5
.
9
3

0
0
.
0
8

7
1
.
6
6

6
1
.
7
7

1
0
.
6
3

0
8
.
2
6

8
9
.
7
5

1
3
.
5
5

5
5
.
6
3

9
7
.
1
5

0
5
.
6
5

3
5
.
5
8

4
9
.
8
6

8
8
.
8
5

2
1
.
5
7

5
8
.
5
7

9
5
.
7
7

9
0
.
4
6

2
0
.
5
6

2
4
.
6
7

0
1
.
5
7

0
5
.
6
6

8
7
.
7
5

6
7
.
6
7

6
5
.
8
6

5
0
.
5
3

7
2
.
1
6

9
9
.
1
6

8
4
.
6
3

0
5
.
2
6

8
0
.
1
6

0
5
.
8
5

2
0
.
6
6

3
3
.
3
8

0
3
.
8
3

2
2
.
5
5

3
8
.
5
7

4
7
.
5
6

2
6
.
8
5

8
7
.
7
3

0
5
.
5
4

0
0
.
9
7

9
3
.
1
6

8
0
.
3
7

0
1
.
9
3

9
6
.
1
6

9
9
.
6
7

5
8
.
9
7

0
0
.
2
5

9
4
.
6
7

0
5
.
2
7

0
6
.
3
8

1
6
.
4
7

5
4
.
6
8

5
0
.
0
9

7
8
.
8
7

7
1
.
5
8

4
6
.
3
8

6
7
.
2
8

8
3
.
5
8

8
4
.
5
8

7
0
.
1
8

2
5
.
9
6

6
5
.
5
8

3
9
.
8
7

3
7
.
6
4

7
9
.
4
8

9
3
.
7
6

2
8
.
2
6

2
3
.
0
8

2
9
.
1
7

0
5
.
3
8

8
1
.
8
7

8
8
.
0
9

9
8
.
4
5

9
0
.
6
7

9
0
.
7
8

3
4
.
8
8

4
0
.
4
6

4
6
.
8
4

6
5
.
7
6

0
5
.
5
8

5
6
.
4
8

4
0
.
5
8

7
7
.
5
5

4
2
.
6
7

6
0
.
7
5

7
7
.
7
6

0
5
.
1
4

7
1
.
8
5

0
0
.
2
5

6
5
.
5
7

1
7
.
4
6

1
4
.
8
5

1
1
.
8
7

7
4
.
5
7

4
1
.
4
7

5
5
.
9
6

3
5
.
4
6

2
0
.
3
8

6
8
.
3
7

3
8
.
3
6

7
2
.
1
6

6
4
.
7
7

0
9
.
9
6

6
0
.
2
4

8
8
.
8
6

8
6
.
7
5

0
3
.
5
4

4
8
.
9
6

2
6
.
8
5

0
0
.
7
5

9
8
.
9
6

6
5
.
9
7

3
4
.
0
4

8
8
.
4
5

0
2
.
0
7

4
4
.
9
6

4
1
.
7
5

6
0
.
5
3

8
7
.
5
4

0
0
.
4
8

1
8
.
8
6

7
0
.
6
7

6
7
.
7
4

0
2
.
3
6

4
2
.
7
4

5
9
.
4
5

7
6
.
4
3

0
4
.
2
5

0
5
.
6
4

6
1
.
5
6

9
5
.
7
5

9
3
.
4
4

9
6
.
2
6

2
0
.
4
6

9
3
.
4
7

7
2
.
7
4

6
0
.
4
4

2
8
.
6
6

1
5
.
8
5

9
6
.
6
5

1
9
.
3
4

8
7
.
6
6

0
2
.
3
5

1
7
.
2
3

2
8
.
9
4

4
7
.
4
4

4
4
.
9
2

1
0
.
7
5

9
4
.
1
5

0
5
.
7
4

2
8
.
7
5

3
5
.
4
7

6
7
.
2
3

5
1
.
8
4

9
7
.
2
6

3
9
.
0
5

8
2
.
8
4

1
4
.
4
3

9
8
.
8
2

3
3
.
6
6

5
7
.
0
5

2
5
.
3
6

3
5
.
8
2

2
3
.
1
5

8
3
.
6
7

3
5
.
2
7

0
0
.
8
4

3
1
.
8
6

0
5
.
3
7

1
7
.
9
8

7
5
.
9
7

0
7
.
5
7

8
5
.
4
8

5
7
.
0
8

6
8
.
5
8

0
0
.
0
8

8
8
.
4
7

6
2
.
7
8

1
9
.
0
8

3
8
.
8
7

6
1
.
0
7

6
8
.
4
8

0
6
.
0
8

6
4
.
3
4

2
7
.
9
7

9
1
.
9
6

7
3
.
8
5

8
6
.
9
7

8
3
.
4
7

0
5
.
3
7

3
7
.
8
7

4
1
.
2
9

3
8
.
3
4

4
3
.
7
6

0
1
.
5
8

6
5
.
0
8

6
4
.
9
6

0
2
.
4
4

5
0
.
2
6

0
0
.
4
8

0
2
.
0
8

2
6
.
1
8

1
8
.
4
5

1
7
.
3
7

7
6
.
7
5

7
0
.
0
6

0
5
.
1
4

9
3
.
1
5

0
0
.
9
4

5
4
.
9
6

6
1
.
3
6

7
8
.
1
5

5
8
.
0
3

3
4
.
9
6

5
4
.
3
7

9
0
.
9
3

3
5
.
4
6

0
4
.
8
6

6
4
.
8
6

6
8
.
2
6

1
4
.
8
5

9
5
.
3
7

1
2
.
4
6

1
5
.
5
3

5
2
.
8
4

1
9
.
2
2

1
9
.
2
3

0
9
.
1
6

5
3
.
3
4

0
5
.
2
3

2
7
.
0
7

9
3
.
2
8

7
4
.
4
3

8
1
.
1
5

8
8
.
7
6

4
9
.
6
5

6
2
.
9
4

0
8
.
5
3

4
4
.
8
2

0
0
.
7
3

9
1
.
1
3

7
3
.
1
7

4
7
.
9
3

9
5
.
2
5

A
Q
V
C

:
1
2

e
l
b
a
T

9
9
.
3
5

1
1
.
3
5

0
0
.
4
4

9
7
.
1
5

0
0
.
4
4

4
3
.
3
6

6
5
.
3
5

1
4
.
8
5

6
1
.
8
6

6
3
.
7
5

6
6
.
9
5

5
5
.
4
5

2
7
.
1
5

6
2
.
2
6

6
3
.
4
5

1
3
.
6
5

5
2
.
8
4

5
7
.
7
5

2
5
.
4
5

1
1
.
4
3

9
5
.
5
5

6
0
.
9
4

2
3
.
9
3

9
1
.
6
5

6
2
.
9
4

0
5
.
5
5

2
5
.
5
5

1
8
.
9
6

2
3
.
5
3

1
8
.
7
4

4
9
.
8
5

1
4
.
7
5

4
7
.
0
5

7
5
.
4
3

0
0
.
8
4

0
5
.
6
6

2
0
.
8
4

6
2
.
0
6

2
4
.
9
3

8
7
.
2
5

3
3
.
2
4

5
4
.
9
4

0
5
.
0
4

2
6
.
4
4

0
0
.
1
4

0
1
.
0
7

9
4
.
4
5

8
9
.
5
3

4
7
.
1
5

4
7
.
7
5

5
5
.
6
5

5
4
.
0
5

2
3
.
5
4

7
6
.
0
7

0
0
.
1
6

4
6
.
3
5

4
4
.
4
4

1
3
.
8
6

9
4
.
7
4

3
9
.
3
4

0
0
.
7
4

0
8
.
5
4

8
4
.
3
3

5
7
.
1
5

7
0
.
3
4

0
5
.
3
4

7
2
.
6
5

4
0
.
6
6

3
6
.
4
3

6
4
.
6
4

6
6
.
1
5

0
0
.
0
5

8
7
.
3
4

6
8
.
0
3

9
8
.
8
2

0
5
.
4
6

6
5
.
3
4

6
9
.
4
6

3
3
.
3
3

6
9
.
8
4

0
4
.
6
5

0
1
.
4
6

0
0
.
6
4

0
8
.
7
4

0
0
.
3
5

0
0
.
4
7

0
2
.
2
6

0
9
.
1
5

0
3
.
8
6

0
7
.
0
7

0
6
.
8
5

0
6
.
5
6

0
7
.
4
6

0
1
.
2
6

0
8
.
9
4

0
9
.
2
7

0
5
.
4
6

0
5
.
5
3

0
1
.
9
5

0
9
.
3
5

0
3
.
6
3

0
7
.
9
5

0
3
.
9
4

0
5
.
4
5

0
5
.
3
6

0
6
.
2
7

0
7
.
5
3

0
5
.
9
4

0
6
.
4
6

0
2
.
6
6

0
3
.
8
4

0
6
.
4
3

0
1
.
9
3

0
0
.
4
7

0
5
.
0
7

0
3
.
2
4

0
2
.
7
5

)
’
a
i
s
e
n
o
d
n
I
’

,
’
u
a
b
a
k
g
n
a
n
i
M

’
(

)
’
a
i
s
e
n
o
d
n
I
’

,
’
e
s
e
n
a
d
n
u
S
’
(

)
’
a
y
n
e
K

’

,
’
i
l
i
h
a
w
S
’
(

)
’
a
i
r
e
g
i
N

’

,
’
o
b
g
I
’
(

)
’
d
n
a
l
e
r
I
’

,
’
h
s
i
r
I
’
(

)
’
a
e
r
o
K
h
t
u
o
S
’

,
’
n
a
e
r
o
K
’
(

)
’
a
n
i
t
n
e
g
r
A

’

,
’
h
s
i
n
a
p
S
’
(

)
’
a
i
d
n
I
’

,
’
u
d
r
U
’
(

)
’
s
e
n
i
p
p
i
l
i
h
P

’

,
’
o
n
i
p
i
l
i

F
’
(

)
’
e
r
o
p
a
g
n
i
S
’

,
’
e
s
e
n
i
h
C
’
(

)
’
a
i
b
m
o
l
o
C

’

,
’
h
s
i
n
a
p
S
’
(

)
’
a
i
s
e
n
o
d
n
I
’

,
’
n
a
i
s
e
n
o
d
n
I
’
(

)
’
y
a
u
g
u
r
U

’

,
’
h
s
i
n
a
p
S
’
(

)
’
l
i
z
a
r
B

’

,
’
e
s
e
u
g
u
t
r
o
P
’
(

)
’
y
a
w
r
o
N

’

,
’
n
a
i
g
e
w
r
o
N
’
(

)
’
a
i
p
o
i
h
t
E

’

,
’
o
m
o
r
O
’
(

)
’
a
i
d
n
I
’

,
’
i
l
a
g
n
e
B
’
(

)
’
a
i
r
a
g
l
u
B

’

,
’
n
a
i
r
a
g
l
u
B
’
(

)
’
a
i
p
o
i
h
t
E

’

,
’
c
i
r
a
h
m
A
’
(

)
’
a
i
s
y
a
l
a
M

’

,
’
y
a
l
a
M

’
(

)
’
o
c
i
x
e
M

’

,
’
h
s
i
n
a
p
S
’
(

)
’
a
n
i
h
C

’

,
’
e
s
e
n
i
h
C
’
(

)
’
a
i
d
n
I
’

,
’
l
i

m
a
T
’
(

)
’
a
i
d
n
I
’

,
’
i
d
n
i
H
’
(

)
’
t
p
y
g
E

’

,
’
c
i
b
a
r
A
_
n
a
i
t
p
y
g
E
’
(

)
’
a
d
n
a
w
R

’

,
’
a
d
n
a
w
r
a
y
n
i
K
’
(

)
’
a
i
n
a
m
o
R

’

,
’
n
a
i
n
a
m
o
R
’
(

)
’
a
i
s
e
n
o
d
n
I
’

,
’
e
s
e
n
a
v
a
J
’
(

)
’
a
k
n
a
L
_
i
r
S
’

,
’
a
l
a
h
n
i
S
’
(

)
’
n
a
p
a
J
’

,
’
e
s
e
n
a
p
a
J
’
(

)
’
n
a
t
s
i
k
a
P

’

,
’
u
d
r
U
’
(

)
’
e
c
n
a
r
F

’

,
’
n
o
t
e
r
B
’
(

)
’
a
i
s
s
u
R

’

,
’
n
a
i
s
s
u
R
’
(

)
’
a
i
d
n
I
’

,
’
i
h
t
a
r
a
M

’
(

)
’
e
l
i
h
C

’

,
’
h
s
i
n
a
p
S
’
(

)
’
a
i
l
o
g
n
o
M

’

,
’
n
a
i
l
o
g
n
o
M

’
(

)
’
r
o
d
a
u
c
E

’

,
’
h
s
i
n
a
p
S
’
(

)
’
n
i
a
p
S
’

,
’
h
s
i
n
a
p
S
’
(

)
’
a
i
d
n
I
’

,
’
u
g
u
l
e
T
’
(

g
v
a

75

B
2
3
-
n
o
i
s
i
V
-
a
y
A

B
2
7
-
L
V
-
5
.
2
-
n
e
w
Q

-

n
o
i
s
i
V
B
0
9
-
2
.
3
-
a
m
a
l
L

B
2
7
-
o
m
l
o
M

B
8
-
n
o
i
s
i
V
-
a
y
A

B
7
-
L
V
-
5
.
2
-
n
e
w
Q

B
2
1
-
l
a
r
t
x
i
P

-

n
o
i
s
i
V
B
1
1
-
2
.
3
-
a
m
a
l
L

-

D
B
7
-
o
m
l
o
M

B
7
-
a
e
g
n
a
P

7
0
.
6
4

6
4
.
0
6

0
2
.
4
3

5
6
.
3
4

9
4
.
8
4

7
8
.
9
5

8
4
.
4
3

8
0
.
7
2

5
6
.
8
2

2
1
.
1
3

4
9
.
4
4

0
5
.
9
2

5
7
.
7
2

6
4
.
4
3

2
6
.
1
3

0
6
.
5
2

0
3
.
8
2

9
0
.
3
5

0
3
.
8
3

0
8
.
3
5

0
5
.
2
7

0
2
.
6
4

0
4
.
7
5

0
2
.
5
6

0
3
.
3
7

0
1
.
6
3

0
3
.
9
3

0
2
.
6
4

0
4
.
5
3

0
3
.
9
4

0
3
.
3
3

0
5
.
7
3

0
5
.
9
4

0
0
.
7
4

0
8
.
3
2

0
9
.
5
3

0
1
.
9
6

4
9
.
2
5

0
6
.
1
5

8
6
.
9
6

3
1
.
9
3

6
2
.
2
5

0
1
.
6
5

5
0
.
8
6

9
7
.
9
3

4
5
.
1
3

0
8
.
7
3

2
7
.
5
3

3
8
.
0
5

7
5
.
4
3

8
1
.
0
3

8
3
.
7
4

0
8
.
9
3

8
7
.
7
2

0
2
.
1
3

6
5
.
9
6

6
1
.
5
4

1
8
.
3
5

6
1
.
9
6

8
0
.
9
3

7
5
.
1
5

8
0
.
4
5

0
7
.
0
7

4
8
.
0
4

5
2
.
8
3

6
9
.
3
4

5
2
.
5
3

6
0
.
7
5

2
4
.
6
3

7
7
.
2
3

0
5
.
6
4

0
1
.
8
3

2
0
.
3
2

0
8
.
4
3

5
1
.
5
6

4
1
.
6
4

9
9
.
0
4

6
3
.
1
5

6
5
.
3
3

6
8
.
8
3

4
1
.
1
4

0
2
.
5
5

2
2
.
1
3

2
8
.
7
2

8
1
.
1
3

3
2
.
0
3

0
3
.
3
4

1
7
.
6
2

4
9
.
5
2

0
3
.
8
2

8
6
.
6
3

7
6
.
6
1

9
6
.
5
2

8
1
.
0
4

2
7
.
4
3

0
4
.
6
3

0
8
.
7
5

0
8
.
3
3

0
4
.
6
4

0
4
.
5
4

0
2
.
9
5

0
1
.
6
3

0
8
.
8
2

0
2
.
5
3

0
3
.
0
3

0
6
.
6
2

0
9
.
5
2

0
6
.
8
2

0
0
.
5
3

0
6
.
7
3

0
2
.
2
2

0
5
.
7
2

0
3
.
0
5

6
5
.
9
3

0
3
.
3
4

3
8
.
7
5

9
2
.
7
1

1
7
.
3
4

8
1
.
9
2

5
5
.
9
5

3
2
.
7
2

1
3
.
2
2

2
9
.
9
2

0
7
.
1
2

8
8
.
4
4

1
3
.
5
2

5
7
.
8
2

8
8
.
3
2

0
3
.
0
3

9
2
.
4
1

5
6
.
6
2

8
6
.
8
4

4
0
.
3
3

e
p
o
c
s
o
d
i
e
l
a
k

:
2
2

e
l
b
a
T

8
5
.
1
4

4
5
.
0
5

5
7
.
9
2

8
8
.
9
3

1
5
.
7
3

5
1
.
5
5

2
2
.
8
3

0
2
.
6
2

2
7
.
5
2

5
2
.
8
2

7
6
.
8
2

5
2
.
0
3

1
2
.
8
2

5
2
.
1
3

0
0
.
4
3

7
5
.
8
2

5
5
.
6
2

2
3
.
6
4

1
8
.
4
3

0
9
.
6
2

0
8
.
7
4

0
0
.
0
3

0
5
.
1
4

0
8
.
5
3

0
6
.
7
4

0
5
.
1
2

0
2
.
9
2

0
1
.
3
3

0
3
.
8
2

0
9
.
9
1

0
9
.
0
3

0
5
.
5
2

0
0
.
6
2

0
9
.
3
3

0
4
.
5
2

0
2
.
7
2

0
3
.
5
3

7
8
.
2
3

0
7
.
4
2

0
2
.
6
4

0
3
.
4
2

0
3
.
7
3

0
0
.
3
3

0
8
.
8
4

0
4
.
0
2

0
5
.
5
2

0
5
.
5
2

0
2
.
1
2

0
2
.
7
1

0
9
.
7
1

0
9
.
3
2

0
8
.
7
2

0
6
.
8
1

0
5
.
7
1

0
4
.
6
2

0
6
.
2
3

1
3
.
1
3

n
t
a
L
_
g
n
e

n
t
a
L
_
a
p
s

a
v
e
D
_
n
i
h

n
t
a
L
_
d
l
n

l
r
y
C
_
r
k
u

n
t
a
L
_
r
o
p

b
a
r
A
_
b
r
a

l
r
y
C
_
s
u
r

n
t
a
L
_
a
r
f

b
a
r
A
_
s
e
p

n
t
a
L
_
u
e
d

n
t
a
L
_
v
r
h

n
t
a
L
_
n
u
h

g
n
e
B
_
n
e
b

a
v
e
D
_
i
p
n

u
l
e
T
_
l
e
t

l
r
y
C
_
p
r
s

n
t
a
L
_
t
i
l

g
v
a

76

