# Drift in Deep Learning

[← Back to Main Page](README.md)

Papers on data drift specific to deep learning models: NLP, Computer Vision, LLMs, Foundation Models, and reinforcement learning.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│              DRIFT IN DEEP LEARNING — LANDSCAPE                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    FOUNDATION MODELS / LLMs                          │   │
│  │                                                                      │   │
│  │  Prompt Drift ─── Knowledge Staleness ─── Embedding Drift           │   │
│  │  (API behavior    (World changes,         (Representation           │   │
│  │   changes over    training cutoff)         space shifts)            │   │
│  │   time)                                                             │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│           │                    │                      │                      │
│  ┌────────▼──────┐   ┌────────▼──────┐   ┌──────────▼────┐                │
│  │     NLP       │   │    VISION     │   │  TIME SERIES  │                │
│  │               │   │               │   │               │                │
│  │ • Semantic    │   │ • Corruption  │   │ • Temporal    │                │
│  │   drift       │   │ • Domain gap  │   │   non-station │                │
│  │ • Temporal    │   │ • Subpop.     │   │ • Regime      │                │
│  │   language    │   │   shift       │   │   changes     │                │
│  │ • Bias drift  │   │ • Style shift │   │ • Seasonality │                │
│  └───────────────┘   └───────────────┘   └───────────────┘                │
│           │                    │                      │                      │
│  ┌────────▼──────┐   ┌────────▼──────┐   ┌──────────▼────┐                │
│  │    TABULAR    │   │      RL       │   │  MULTIMODAL   │                │
│  │               │   │               │   │               │                │
│  │ • Feature     │   │ • Environment │   │ • Cross-modal │                │
│  │   drift       │   │   dynamics    │   │   shift       │                │
│  │ • Schema      │   │ • Reward      │   │ • Alignment   │                │
│  │   changes     │   │   shift       │   │   degradation │                │
│  └───────────────┘   └───────────────┘   └───────────────┘                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

```
    LLM DRIFT — A NEW FRONTIER
    ═══════════════════════════

    Training Cutoff ────────► Deployment ────────► Months Later
         │                       │                      │
         ▼                       ▼                      ▼
    ┌──────────┐           ┌──────────┐           ┌──────────┐
    │ World    │           │ Model    │           │ Model    │
    │ State    │           │ knows    │           │ outputs  │
    │ captured │           │ "now"    │           │ stale    │
    │ in data  │           │          │           │ answers  │
    └──────────┘           └──────────┘           └──────────┘

    GPT-3.5/4 Behavior Change (Chen et al., 2023):
    ┌─────────────────────────────────────────────┐
    │  Task          Mar 2023   Jun 2023  Change  │
    │  ─────────────────────────────────────────── │
    │  Math           97.6%      2.4%     ▼95%    │
    │  Code gen       52.0%     10.0%     ▼42%    │
    │  Sensitivity    21.0%     61.0%     ▲40%    │
    │  Visual         27.4%     60.1%     ▲33%    │
    └─────────────────────────────────────────────┘
    Source: "How Is ChatGPT's Behavior Changing over Time?"
```

---

## Quick Links

- [NLP & Text Models](#nlp--text-models)
- [Computer Vision](#computer-vision)
- [LLMs & Foundation Models](#llms--foundation-models)
- [Tabular / Structured Data DNNs](#tabular--structured-data-dnns)
- [Reinforcement Learning](#reinforcement-learning)
- [Time Series Deep Learning](#time-series-deep-learning)
- [Multimodal Models](#multimodal-models)

---

## NLP & Text Models

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| ⭐ **Temporal Analysis of Sentiment Terms** — Hamilton, W.L., Leskovec, J., Jurafsky, D. | ACL 2016 | [Paper](https://arxiv.org/abs/1605.09096) [Code](https://github.com/williamleif/histwords) | Diachronic word embeddings reveal semantic drift over decades |
| **Time-Aware Language Models as Temporal Knowledge Bases** — Dhingra, B., Cole, J.R., Eisenschlos, J.M., et al. | TACL 2022 | [Paper](https://arxiv.org/abs/2106.15110) | Language models that account for temporal knowledge drift |
| **Temporal Adaptation of BERT for Temporal Reasoning** — Röttger, P., Pierrehumbert, J. | EMNLP 2021 | [Paper](https://arxiv.org/abs/2104.09521) | Adapting BERT to temporal language shifts |
| **Continual Learning in Natural Language Processing: A Survey** — Biesialska, M., Biesialska, K., Costa-jussà, M.R. | COLING 2020 | [Paper](https://aclanthology.org/2020.coling-main.574/) | Survey on handling drift in NLP models |
| **Dynamic Language Models for Continuously Evolving Content** — Lazaridou, A., Kuncoro, A., Gribovskaya, E., et al. | ACL 2021 | [Paper](https://arxiv.org/abs/2106.06297) | Language models that update with temporal shift |
| **On the Role of Distribution Shift in Benchmarking NLP** — Aroca-Ouellette, S., Ruder, S. | ACL Findings 2022 | [Paper](https://arxiv.org/abs/2204.00260) | Analyzes shift's impact on NLP benchmarks |
| **Time Waits for No One! Analysis and Challenges of Temporal Misalignment** — Luu, K., Khashabi, D., Goldwasser, D., et al. | NAACL 2022 | [Paper](https://arxiv.org/abs/2111.07408) | Temporal misalignment in NLP systems |
| **Detecting Emergent Intersectional Biases** — Guo, W., Caliskan, A. | AIES 2021 | [Paper](https://arxiv.org/abs/2006.03468) | Bias drift in language models over time |

---

## Computer Vision

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| ⭐ **Benchmarking Neural Network Robustness to Common Corruptions** — Hendrycks, D., Dietterich, T. | ICLR 2019 | [Paper](https://arxiv.org/abs/1903.12261) [Code](https://github.com/hendrycks/robustness) | ImageNet-C benchmark for distribution shift in vision |
| ⭐ **ImageNet-Sketch / ImageNet-R / ImageNet-A** — Hendrycks, D., et al. | Various 2019-2021 | [Paper](https://arxiv.org/abs/1907.07174) [Code](https://github.com/hendrycks/natural-adv-examples) | Natural distribution shift benchmarks for vision |
| **Measuring Robustness to Natural Distribution Shifts in Image Classification** — Taori, R., Dave, A., Shankar, V., et al. | NeurIPS 2020 | [Paper](https://arxiv.org/abs/2007.00644) [Code](https://github.com/modestyachts/ImageNetV2) | Systematic study of robustness to natural shifts |
| **Distribution Shift in Computer Vision: A Survey** — Ye, N., Li, K., Bai, H., et al. | arXiv 2022 | [Paper](https://arxiv.org/abs/2205.12710) | Survey on distribution shift in CV |
| **The Many Faces of Robustness** — Hendrycks, D., Basart, S., Mu, N., et al. | ICCV 2021 | [Paper](https://arxiv.org/abs/2006.16241) [Code](https://github.com/hendrycks/imagenet-r) | Multiple robustness benchmarks for vision |
| **Breeds: Benchmarks for Subpopulation Shift** — Santurkar, S., Tsipras, D., Madry, A. | ICML 2021 | [Paper](https://arxiv.org/abs/2008.04859) [Code](https://github.com/MadryLab/BREEDS-Benchmarks) | Subpopulation shift benchmark using ImageNet hierarchy |
| **Does Object Recognition Work for Everyone?** — DeVries, T., Misra, I., Wang, C., van der Maaten, L. | CVPR Workshop 2019 | [Paper](https://arxiv.org/abs/1906.02659) | Geographic distribution shift in object recognition |
| **AugMax: Adversarial Composition of Random Augmentations** — Wang, H., Xiao, C., Kossaifi, J., et al. | NeurIPS 2021 | [Paper](https://arxiv.org/abs/2110.13771) [Code](https://github.com/VITA-Group/AugMax) | Data augmentation for distribution shift robustness |

---

## LLMs & Foundation Models

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| ⭐ **Do Language Models Know When They Don't Know?** — Kadavath, S., Conerly, T., Askell, A., et al. | arXiv 2022 | [Paper](https://arxiv.org/abs/2207.05221) | LLM calibration and uncertainty under distribution shift |
| **Measuring Massive Multitask Language Understanding (MMLU)** — Hendrycks, D., et al. | ICLR 2021 | [Paper](https://arxiv.org/abs/2009.03300) [Code](https://github.com/hendrycks/test) | Benchmark revealing shift between training and evaluation |
| **Holistic Evaluation of Language Models (HELM)** — Liang, P., Bommasani, R., Lee, T., et al. | arXiv 2022 | [Paper](https://arxiv.org/abs/2211.09110) [Code](https://github.com/stanford-crfm/helm) | Comprehensive evaluation including robustness to shift |
| **The Pile: An 800GB Dataset of Diverse Text** — Gao, L., Biderman, S., Black, S., et al. | arXiv 2020 | [Paper](https://arxiv.org/abs/2101.00027) [Code](https://github.com/EleutherAI/the-pile) | Diverse training data to reduce training distribution bias |
| **Prompt Drift: Monitoring LLM Reliability in Production** — Chen, X., et al. | arXiv 2024 | [Paper](https://arxiv.org/abs/2401.10273) | Monitors how LLM behavior shifts over API updates |
| **How Is ChatGPT's Behavior Changing over Time?** — Chen, L., Zaharia, M., Zou, J. | arXiv 2023 | [Paper](https://arxiv.org/abs/2307.09009) | Empirical study of GPT-3.5/4 drift over months |
| **Temporal Degradation of Language Models** — Luu, K., et al. | ACL 2022 | [Paper](https://arxiv.org/abs/2203.07540) | How pre-trained LMs degrade on temporal data |
| **Detecting Pretraining Data from Large Language Models** — Shi, W., et al. | ICLR 2024 | [Paper](https://arxiv.org/abs/2310.16789) [Code](https://github.com/swj0419/detect-pretrain-code) | MIN-K% method; relevant for understanding data distribution |

---

## Tabular / Structured Data DNNs

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| **Drift Detection in Tabular Data with Deep Learning** — Seedat, N., Crabbe, J., van der Schaar, M. | ICML 2023 | [Paper](https://arxiv.org/abs/2305.15670) [Code](https://github.com/seedatnabeel/Data-SUITE) | Data-SUITE: detects drift without labels for tabular data |
| **TableShift: A Benchmark of Real-World Distribution Shifts for Tabular Data** — Gardner, J., Popovic, Z., Schmidt, L. | NeurIPS 2023 | [Paper](https://arxiv.org/abs/2312.07577) [Code](https://github.com/mlfoundations/tableshift) | Benchmark for tabular distribution shift |
| **WhyShift: A Benchmark for Feature-Based Explanations of Distribution Shift** — Bareinboim, E., et al. | NeurIPS 2023 | [Paper](https://arxiv.org/abs/2312.11596) | Explains which features cause tabular shift |
| **Revisiting Deep Learning Models for Tabular Data** — Gorishniy, Y., Rubachev, I., Khrulkov, V., Babenko, A. | NeurIPS 2021 | [Paper](https://arxiv.org/abs/2106.11959) [Code](https://github.com/yandex-research/rtdl) | Deep learning on tabular data with shift considerations |

---

## Reinforcement Learning

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| ⭐ **Towards Generalization and Simplicity in Continuous Control** — Rajeswaran, A., et al. | NeurIPS 2017 | [Paper](https://arxiv.org/abs/1703.02660) | Distribution shift in RL environments |
| **Off-Policy Evaluation Under Distribution Shift** — Nachum, O., Chow, Y., Dai, B., Li, L. | NeurIPS 2019 | [Paper](https://arxiv.org/abs/1906.03735) | Off-policy evaluation under covariate shift |
| **Environment Probing Interaction Policies** — Kim, Y., Ahn, S., Finn, C. | ICLR 2021 | [Paper](https://arxiv.org/abs/2102.02201) | Probing for environment changes in RL |
| **Addressing Distribution Shift in Online Reinforcement Learning** — Luo, Y., et al. | ICML 2022 | [Paper](https://arxiv.org/abs/2205.02804) | Distribution shift correction in online RL |

---

## Time Series Deep Learning

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| ⭐ **A Survey on Distribution Shift in Time Series** — Gao, J., Wen, Q., Zhang, C., et al. | arXiv 2024 | [Paper](https://arxiv.org/abs/2401.16603) | Comprehensive survey on temporal distribution shift |
| **AdaRNN: Adaptive Learning and Forecasting for Time Series** — Du, Y., Wang, J., Feng, W., et al. | CIKM 2021 | [Paper](https://arxiv.org/abs/2108.04443) [Code](https://github.com/thuml/Adaptive-Graph-Diffusion-Networks) | RNN that adapts to temporal distribution shift |
| **Non-Stationary Transformers: Exploring the Stationarity in Time Series Forecasting** — Liu, Y., Wu, H., Wang, J., Long, M. | NeurIPS 2022 | [Paper](https://arxiv.org/abs/2205.14415) [Code](https://github.com/thuml/Nonstationary_Transformers) | Transformers designed for non-stationary time series |
| **Reversible Instance Normalization for Accurate Time-Series Forecasting against Distribution Shift** — Kim, T., Kim, J., Tae, Y., et al. | ICLR 2022 | [Paper](https://arxiv.org/abs/2105.02855) [Code](https://github.com/ts-kim/RevIN) | RevIN: normalization for temporal distribution shift |
| **DRAIN: Drift-Adapted Incremental Network for Time Series** — Wang, J., et al. | IEEE Trans. Neural Networks 2023 | [Paper](https://doi.org/10.1109/TNNLS.2023.3241356) | Incremental network for temporal drift |

---

## Multimodal Models

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| **Multimodal Distribution Shift Detection** — Hu, S., et al. | NeurIPS 2023 | [Paper](https://arxiv.org/abs/2310.12592) | Detecting shift across multiple modalities simultaneously |
| **CLIP Under Distribution Shift** — Fang, A., et al. | ICML 2022 | [Paper](https://arxiv.org/abs/2205.09537) | How CLIP handles natural distribution shift |
| **Robust Fine-Tuning of Zero-Shot Models (WiSE-FT)** — Wortsman, M., et al. | CVPR 2022 | [Paper](https://arxiv.org/abs/2109.01903) [Code](https://github.com/mlfoundations/wise-ft) | Weight-space ensembling for robustness to shift |
| **Distribution Shift in Vision-Language Models** — Parashar, S., et al. | arXiv 2024 | [Paper](https://arxiv.org/abs/2402.09345) | Analyzing VLM behavior under distribution shift |
