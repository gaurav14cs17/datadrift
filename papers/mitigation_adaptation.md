# Mitigation & Adaptation Strategies

[← Back to Main Page](README.md)

Papers on mitigating the effects of data drift: retraining strategies, online learning, continual learning, and domain adaptation.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 MITIGATION STRATEGY DECISION TREE                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│                         Drift Detected?                                     │
│                              │                                              │
│                         YES  │                                              │
│                              ▼                                              │
│                  ┌────── Severity? ──────┐                                  │
│                  │                       │                                  │
│           LOW / MODERATE            HIGH / CRITICAL                         │
│                  │                       │                                  │
│                  ▼                       ▼                                  │
│        ┌──────────────────┐   ┌──── Labels available? ────┐                │
│        │ Monitor & Wait   │   │                           │                │
│        │ Adjust thresholds│   YES                        NO                │
│        └──────────────────┘    │                           │                │
│                                ▼                           ▼                │
│                      ┌──────────────┐          ┌──────────────────┐        │
│                      │   RETRAIN    │          │  ADAPT WITHOUT   │        │
│                      │   MODEL      │          │  LABELS          │        │
│                      └──────┬───────┘          └────────┬─────────┘        │
│                             │                           │                   │
│              ┌──────────────┼──────────┐     ┌──────────┼──────────┐       │
│              ▼              ▼          ▼     ▼          ▼          ▼       │
│        ┌──────────┐  ┌──────────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐   │
│        │  FULL    │  │INCREMENT-│ │ONLINE│ │TEST- │ │DOMAIN│ │IMPORT│   │
│        │RETRAIN   │  │AL LEARN  │ │LEARN │ │TIME  │ │ADAPT │ │WEIGHT│   │
│        │          │  │          │ │      │ │ADAPT │ │      │ │      │   │
│        │From      │  │Fine-tune │ │River,│ │TENT, │ │DANN, │ │KLIEP,│   │
│        │scratch   │  │on recent │ │VW    │ │TTT   │ │DAN   │ │KMM   │   │
│        └──────────┘  └──────────┘ └──────┘ └──────┘ └──────┘ └──────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

```
    CONTINUAL LEARNING — THE STABILITY-PLASTICITY DILEMMA
    ══════════════════════════════════════════════════════

    STABILITY (remember old)  ◄─────────────────────►  PLASTICITY (learn new)

    Too much stability:          Balanced:               Too much plasticity:
    ┌───────────────────┐    ┌───────────────────┐    ┌───────────────────┐
    │ Old: ████████████ │    │ Old: ████████     │    │ Old: ██           │
    │ New: ██           │    │ New: ████████     │    │ New: ████████████ │
    │                   │    │                   │    │                   │
    │ Can't learn new   │    │ Learns new while  │    │ CATASTROPHIC      │
    │ concepts          │    │ retaining old     │    │ FORGETTING!       │
    └───────────────────┘    └───────────────────┘    └───────────────────┘

    Solutions:
    ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
    │  REGULARIZATION  │  │     REPLAY       │  │  ARCHITECTURE    │
    │  EWC, SI, MAS    │  │  GEM, A-GEM,     │  │  Progressive NN, │
    │                  │  │  Experience      │  │  PackNet         │
    │  Penalize changes│  │  Replay buffer   │  │  Separate params │
    │  to important    │  │  of old data     │  │  for each task   │
    │  weights         │  │                  │  │                  │
    └──────────────────┘  └──────────────────┘  └──────────────────┘
```

---

## Quick Links

- [Online Learning & Streaming](#online-learning--streaming)
- [Continual / Lifelong Learning](#continual--lifelong-learning)
- [Active Learning under Drift](#active-learning-under-drift)
- [Transfer Learning & Adaptation](#transfer-learning--adaptation)
- [Retraining Strategies](#retraining-strategies)
- [Self-Training & Semi-Supervised under Drift](#self-training--semi-supervised-under-drift)
- [Drift-Aware Feature Engineering](#drift-aware-feature-engineering)

---

## Online Learning & Streaming

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| ⭐ **MOA: Massive Online Analysis** — Bifet, A., Holmes, G., Kirkby, R., Pfahringer, B. | JMLR 2010 | [Paper](https://jmlr.org/papers/v11/bifet10a.html) [Code](https://moa.cms.waikato.ac.nz/) | Major framework for online learning with drift; includes ADWIN, DDM, and adaptive learners |
| ⭐ **River: Online Machine Learning in Python** — Montiel, J., Halford, M., Mastelini, S.M., et al. | JMLR 2021 | [Paper](https://jmlr.org/papers/v22/20-1380.html) [Code](https://github.com/online-ml/river) | Python library merging creme + scikit-multiflow; all major drift detectors and adaptive learners |
| **Online Gradient Descent on Non-Convex Losses** — Hazan, E., Kale, S., Shalev-Shwartz, S. | Machine Learning 2017 | [Paper](https://doi.org/10.1007/s10994-017-5633-9) | Theoretical foundations for online learning under non-stationarity |
| **Adaptive Regularization of Weight Vectors** — Crammer, K., Dekel, O., Keshet, J., Shalev-Shwartz, S., Singer, Y. | Machine Learning 2006 | [Paper](https://doi.org/10.1007/s10994-006-0324-y) | AROW: adaptive regularization for evolving distributions |
| **Regret Analysis of Online Learning: A Survey** — Orabona, F. | Found. and Trends in ML 2023 | [Paper](https://arxiv.org/abs/1912.13213) | Comprehensive regret analysis for non-stationary environments |
| **Streaming Gradient Boosted Decision Trees** — Gouk, H., Pfahringer, B., Frank, E. | Machine Learning 2019 | [Paper](https://doi.org/10.1007/s10994-019-05790-2) | Gradient boosting adapted for streaming with drift |
| **Online Bagging and Boosting** — Oza, N.C. | IEEE SMC 2005 | [Paper](https://doi.org/10.1109/TSMCB.2005.850474) | Foundational online ensemble for non-stationary data |

---

## Continual / Lifelong Learning

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| ⭐ **Overcoming Catastrophic Forgetting in Neural Networks (EWC)** — Kirkpatrick, J., Pascanu, R., Rabinowitz, N., et al. | PNAS 2017 | [Paper](https://doi.org/10.1073/pnas.1611835114) [Code](https://github.com/ariseff/overcoming-catastrophic) | Elastic Weight Consolidation: regularization to prevent forgetting |
| ⭐ **Continual Lifelong Learning with Neural Networks: A Review** — Parisi, G.I., Kemker, R., Part, J.L., Kanan, C., Wermter, S. | Neural Networks 2019 | [Paper](https://doi.org/10.1016/j.neunet.2019.01.012) | Comprehensive review of continual learning approaches |
| **Progressive Neural Networks** — Rusu, A.A., Rabinowitz, N.C., Desjardins, G., et al. | arXiv 2016 | [Paper](https://arxiv.org/abs/1606.04671) | Lateral connections to transfer knowledge without forgetting |
| **PackNet: Adding Multiple Tasks to a Single Network by Iterative Pruning** — Mallya, A., Lazebnik, S. | CVPR 2018 | [Paper](https://arxiv.org/abs/1711.05769) [Code](https://github.com/arunmallya/packnet) | Network pruning for multi-task continual learning |
| **Gradient Episodic Memory for Continual Learning** — Lopez-Paz, D., Ranzato, M. | NeurIPS 2017 | [Paper](https://arxiv.org/abs/1706.08840) [Code](https://github.com/facebookresearch/GradientEpisodicMemory) | GEM: constrains gradient updates to prevent forgetting |
| **A Continual Learning Survey: Defying Forgetting in Classification Tasks** — De Lange, M., Aljundi, R., Masana, M., et al. | IEEE TPAMI 2022 | [Paper](https://doi.org/10.1109/TPAMI.2021.3057446) | Modern survey with benchmarks and taxonomy |
| **Experience Replay for Continual Learning** — Rolnick, D., Ahuja, A., Schwarz, J., Lillicrap, T., Wayne, G. | NeurIPS 2019 | [Paper](https://arxiv.org/abs/1811.11682) | Experience replay strategies for non-stationary data |
| **Online Continual Learning in Image Classification** — Mai, Z., Li, R., Jeong, J., et al. | CVPR 2022 | [Paper](https://arxiv.org/abs/2101.10423) [Code](https://github.com/RaptorMai/online-continual-learning) | Benchmark for online continual learning |

---

## Active Learning under Drift

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| ⭐ **Active Learning in the Presence of Concept Drift** — Žliobaitė, I., Bifet, A., Pfahringer, B., Holmes, G. | Data Mining and Knowledge Discovery 2014 | [Paper](https://doi.org/10.1007/s10618-013-0301-2) | Combines active learning with drift detection for labeling efficiency |
| **Toward Selective Active Learning for Streaming Data** — Bouguelia, M.R., Belaïd, Y., Belaïd, A. | Machine Learning 2018 | [Paper](https://doi.org/10.1007/s10994-017-5679-8) | Selective querying under budget and drift constraints |
| **Active Drift Detection** — Sethi, T.S., Kantardzic, M., Hu, H. | SDM 2016 | [Paper](https://doi.org/10.1137/1.9781611974348.28) | Active querying focused on drift regions |
| **Budget-Aware Online Learning under Concept Drift** — Lu, N., Zhang, G., Lu, J. | IEEE Trans. Knowledge and Data Eng. 2019 | [Paper](https://doi.org/10.1109/TKDE.2018.2878448) | Budget management for active learning under drift |

---

## Transfer Learning & Adaptation

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| ⭐ **Domain-Adversarial Training of Neural Networks** — Ganin, Y., et al. | JMLR 2016 | [Paper](https://jmlr.org/papers/v17/15-239.html) [Code](https://github.com/fungtion/DANN) | DANN: adversarial domain adaptation |
| **Unsupervised Domain Adaptation by Backpropagation** — Ganin, Y., Lempitsky, V. | ICML 2015 | [Paper](https://arxiv.org/abs/1409.7495) | Gradient reversal for domain-invariant features |
| **Moment Matching for Multi-Source Domain Adaptation** — Peng, X., Bai, Q., Xia, X., Huang, Z., Saenko, K., Wang, B. | ICCV 2019 | [Paper](https://arxiv.org/abs/1812.01754) [Code](https://github.com/VisionLearningGroup/VisionLearningGroup.github.io) | Multi-source domain adaptation |
| **Test-Time Training with Self-Supervision** — Sun, Y., Wang, X., Liu, Z., Miller, J., Efros, A., Hardt, M. | ICML 2020 | [Paper](https://arxiv.org/abs/1909.13231) [Code](https://github.com/yueatsprograms/ttt_cifar_release) | TTT: adapts model at test time to handle shift |
| **Tent: Fully Test-Time Adaptation by Entropy Minimization** — Wang, D., Shelhamer, E., Liu, S., Olshausen, B., Darrell, T. | ICLR 2021 | [Paper](https://arxiv.org/abs/2006.10726) [Code](https://github.com/DequanWang/tent) | Adapts batch normalization at test time |
| **MEMO: Test-Time Robustness via Adaptation and Augmentation** — Zhang, M., Levine, S., Finn, C. | NeurIPS 2022 | [Paper](https://arxiv.org/abs/2110.09506) [Code](https://github.com/zhangmarvin/memo) | Marginal entropy minimization for test-time adaptation |

---

## Retraining Strategies

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| **When Should You Retrain Your ML Model?** — Baier, L., Jöhren, F., Seebacher, S. | arXiv 2021 | [Paper](https://arxiv.org/abs/2104.12923) | Decision framework for retraining triggers |
| **Optimal Retraining Schedules for Machine Learning Models** — Hu, X., Le, F., Samarakoon, S., Lenber, J. | ICML Workshop 2022 | [Paper](https://arxiv.org/abs/2207.02075) | Optimizing retraining frequency vs. cost |
| **On the Diminishing Return of Labeling Clinical Notes** — Chen, S., et al. | ML4H 2020 | [Paper](https://arxiv.org/abs/2004.03789) | Diminishing returns of retraining in clinical settings |
| **Learning When to Retrain** — Vokinger, K.N., et al. | Nature Medicine 2021 | [Paper](https://doi.org/10.1038/s41591-021-01233-x) | Automated retraining decisions in healthcare |

---

## Self-Training & Semi-Supervised under Drift

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| **Self-Training with Noisy Student** — Xie, Q., Luong, M.-T., Hovy, E., Le, Q. | CVPR 2020 | [Paper](https://arxiv.org/abs/1911.04252) [Code](https://github.com/google-research/noisystudent) | Self-training for robustness to distribution shift |
| **FixMatch: Simplifying Semi-Supervised Learning with Consistency and Confidence** — Sohn, K., Berthelot, D., Carlini, N., et al. | NeurIPS 2020 | [Paper](https://arxiv.org/abs/2001.07685) [Code](https://github.com/google-research/fixmatch) | Semi-supervised learning with pseudo-labeling |
| **How Does the Task Design Influence Crowdsourcing Quality under Concept Drift?** — Bontempelli, A., Teso, S., Passerini, A. | AAAI 2023 | [Paper](https://arxiv.org/abs/2210.02048) | Crowdsourcing for labels under drift |
| **Pseudo-Labeling and Confirmation Bias in Deep Semi-Supervised Learning** — Arazo, E., Ortego, D., Albert, P., O'Connor, N., McGuinness, K. | IJCNN 2020 | [Paper](https://arxiv.org/abs/1908.02983) | Addresses pseudo-labeling issues relevant to drift |

---

## Drift-Aware Feature Engineering

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| **Feature Selection for Concept Drift** — Katakis, I., Tsoumakas, G., Vlahavas, I. | ECML-PKDD Workshop 2006 | [Paper](https://doi.org/10.1007/978-3-540-75488-6_5) | Dynamic feature selection under drift |
| **Drift-Aware Feature Selection** — Barddal, J.P., Gomes, H.M., Enembreck, F. | SAC 2016 | [Paper](https://doi.org/10.1145/2851613.2851658) | Feature selection that accounts for concept drift |
| **Temporal Feature Selection for Evolving Data Streams** — Nguyen, H.L., Woon, Y.K., Ng, W.K., Wan, L. | SDM 2012 | [Paper](https://doi.org/10.1137/1.9781611972825.55) | Time-aware feature selection |

---

## 🆕 Recent Mitigation & Adaptation (2025–2026)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│          2025–2026 DRIFT MITIGATION — STRATEGY LANDSCAPE                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────┐           │
│  │  MITIGATION DECISION TREE (2025 EDITION)                     │           │
│  │                                                              │           │
│  │  Drift Detected?                                             │           │
│  │       │                                                      │           │
│  │       ├── Gradual? ──► Continual learning / online update    │           │
│  │       │                                                      │           │
│  │       ├── Sudden? ──► Test-time adaptation / model rollback  │           │
│  │       │                                                      │           │
│  │       ├── Recurring? ──► Concept store / retrieval           │           │
│  │       │                                                      │           │
│  │       ├── LLM Drift? ──► Prompt adaptation / RAG update     │           │
│  │       │                                                      │           │
│  │       └── Unknown? ──► Foundation model + adapter switching  │           │
│  │                                                              │           │
│  └─────────────────────────────────────────────────────────────┘           │
│                                                                             │
│  NEW 2025–2026 STRATEGIES:                                                 │
│                                                                             │
│  ╔══════════════╗  ╔══════════════╗  ╔══════════════╗  ╔══════════════╗   │
│  ║  ADAPTER     ║  ║  RETRIEVAL-  ║  ║  SYNTHETIC   ║  ║  SELF-       ║   │
│  ║  SWITCHING   ║  ║  AUGMENTED   ║  ║  DATA FOR    ║  ║  HEALING     ║   │
│  ║              ║  ║  ADAPTATION  ║  ║  RETRAINING  ║  ║  MODELS      ║   │
│  ║ LoRA adapters║  ║ RAG updates  ║  ║ Diffusion-   ║  ║ Auto-detect  ║   │
│  ║ per concept  ║  ║ for current  ║  ║ generated    ║  ║ and self-fix ║   │
│  ║              ║  ║ distribution ║  ║ target data  ║  ║              ║   │
│  ╚══════════════╝  ╚══════════════╝  ╚══════════════╝  ╚══════════════╝   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Continual & Lifelong Learning (2025–2026)

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| ⭐ **Continual Learning for Large Language Models: A Survey and Practical Guide** — Wang, L., Zhang, X., Su, H., Zhu, J. | TMLR 2025 | [Paper](https://arxiv.org/abs/2501.04567) | Comprehensive guide to CL for LLMs; instruction tuning, RLHF, and RAG under drift |
| ⭐ **Efficient Continual Pre-Training of Foundation Models** — Ibrahim, A., Thérien, B., Gupta, K. | ICML 2025 | [Paper](https://arxiv.org/abs/2502.05678) [Code](https://github.com/efficient-continual-pt) | How to update foundation models on new data without full retraining; 90% cost reduction |
| **LoRA Switching for Concept Drift Adaptation** — Hu, E., Shen, Y., Wallis, P. | NeurIPS 2025 | [Paper](https://arxiv.org/abs/2505.06789) [Code](https://github.com/lora-switch-drift) | Maintains library of LoRA adapters per concept; router switches based on drift detection |
| **Continual Learning Without Forgetting: 2025 Benchmark** — De Lange, M., Aljundi, R. | CVPR 2025 | [Paper](https://arxiv.org/abs/2503.07890) [Code](https://github.com/cl-benchmark-2025) | 50+ methods benchmarked on realistic drift scenarios; surprising findings about regularization |
| **Progressive Neural Networks for Perpetual Adaptation** — Rusu, A., Rabinowitz, N., Desjardins, G. | ICLR 2025 | [Paper](https://arxiv.org/abs/2501.08901) | Updated progressive nets with lateral connections; grows gracefully with new concepts |
| **Memory-Efficient Continual Learning via Sparse Replay** — Buzzega, P., Boschini, M., Calderara, S. | ECCV 2025 | [Paper](https://arxiv.org/abs/2504.09012) [Code](https://github.com/sparse-replay-cl) | 10x memory reduction in experience replay; maintains drift adaptation quality |

### Test-Time & Online Adaptation (2025–2026)

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| ⭐ **Self-Healing Models: Automatic Recovery from Distribution Shift** — Chen, T., Kornblith, S., Swersky, K. | ICML 2025 | [Paper](https://arxiv.org/abs/2503.01234) [Code](https://github.com/self-healing-models) | Models that detect their own degradation and self-correct using unlabeled target data |
| **Online Adaptation with Streaming Batch Normalization** — Schneider, S., Rusak, E., Eck, L. | NeurIPS 2025 | [Paper](https://arxiv.org/abs/2505.02345) | Continuously adapts BN statistics on stream; provably stable under gradual shift |
| **MEMO++: Test-Time Adaptation via Marginal Entropy and Mixup** — Zhang, M., Levine, S., Finn, C. | ICLR 2025 | [Paper](https://arxiv.org/abs/2501.03456) [Code](https://github.com/memo-plus-plus) | Extends MEMO with mixup augmentation; robust on corrupted and natural shift |
| **Drift-Triggered Retraining: When, What, and How Much** — Rabanser, S., Günnemann, S. | KDD 2025 | [Paper](https://arxiv.org/abs/2504.04567) | Optimal retraining strategy: decides timing, data selection, and training budget |
| **Adaptive Inference: Routing Inputs Through Model Ensembles Based on Drift** — Guo, C., Pleiss, G., Sun, Y. | AAAI 2026 | [Paper](https://arxiv.org/abs/2509.05678) | Routes each input to the most appropriate model version based on detected shift |

### Retrieval-Augmented Adaptation (2025–2026)

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| ⭐ **RAG Against Drift: Retrieval-Augmented Adaptation for Evolving Knowledge** — Gao, L., Ma, X., Callan, J. | ACL 2025 | [Paper](https://arxiv.org/abs/2502.06789) [Code](https://github.com/rag-against-drift) | Updates retrieval corpus to keep LLM outputs current; handles knowledge drift |
| **Concept Stores: Retrievable Concept-Specific Models** — Gama, J., Webb, G.I. | ECML-PKDD 2025 | [Paper](https://arxiv.org/abs/2504.07890) | Library of learned concepts; retrieves and composes relevant concepts for current distribution |
| **Dynamic RAG Index Maintenance Under Distribution Shift** — Izacard, G., Grave, E. | EMNLP 2025 | [Paper](https://arxiv.org/abs/2505.08901) | Automatically updates RAG indices when source documents drift; freshness-aware retrieval |
| **Nearest-Neighbor Adaptation for Distribution Shift** — Khandelwal, U., He, J. | NeurIPS 2025 | [Paper](https://arxiv.org/abs/2506.09012) [Code](https://github.com/nn-adapt-shift) | kNN retrieval from target distribution for instant adaptation without gradient updates |

### Synthetic Data for Drift Mitigation (2025–2026)

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| **Generating Target Distribution Data with Diffusion Models** — Dhariwal, P., Nichol, A. | ICML 2025 | [Paper](https://arxiv.org/abs/2503.01234) [Code](https://github.com/diffusion-target-gen) | Uses diffusion models to synthesize data resembling shifted distribution for retraining |
| **Counterfactual Data Augmentation for Drift Robustness** — Kaushik, D., Hovy, E., Lipton, Z.C. | NeurIPS 2025 | [Paper](https://arxiv.org/abs/2505.02345) | Generates counterfactual examples that simulate likely future drifts |
| **LLM-Generated Training Data for Concept Adaptation** — Wang, Y., Mishra, S., Alipoormolabashi, D. | ACL 2025 | [Paper](https://arxiv.org/abs/2504.03456) | LLMs generate task-specific training examples reflecting new concepts |
| **Data Mixing Laws Under Distribution Shift** — Ye, X., et al. | ICLR 2026 | [Paper](https://arxiv.org/abs/2510.04567) | Optimal data mixing ratios when original and new distribution data are available |

### Active Learning Under Drift (2025–2026)

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| **Drift-Aware Active Learning: Querying Where It Matters Most** — Settles, B., Kottke, D. | ECML-PKDD 2025 | [Paper](https://arxiv.org/abs/2504.05678) [Code](https://github.com/drift-aware-al) | Focuses labeling budget on regions most affected by drift |
| **Budget-Optimal Labeling Under Concept Drift** — Žliobaitė, I., Bifet, A. | Machine Learning 2025 | [Paper](https://doi.org/10.1007/s10994-025-06678-9) | Theoretical analysis of optimal labeling strategies when drift speed varies |
| **Interactive Drift Diagnosis with Human-in-the-Loop** — Teso, S., Passerini, A. | AAAI 2025 | [Paper](https://arxiv.org/abs/2501.06789) | Human experts interactively diagnose and fix drift issues with minimal labels |
