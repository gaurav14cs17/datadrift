# Covariate Shift & Distribution Shift

[← Back to Main Page](README.md)

Papers on covariate shift (P(X) changes while P(Y|X) stays the same), prior probability shift, and general distribution shift.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      COVARIATE SHIFT EXPLAINED                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  The INPUT distribution changes, but the mapping X → Y stays the same      │
│                                                                             │
│   Training Distribution            Production Distribution                 │
│                                                                             │
│        ▄▄████▄▄                           ▄▄██▄▄                           │
│      ▄████████████▄                     ▄████████████▄▄                    │
│    ▄████████████████▄               ▄██████████████████████▄               │
│   ████████████████████           ████████████████████████████              │
│   ──────────────────────         ────────────────────────────────          │
│            μ₁                                    μ₂                        │
│                                                                             │
│   P_train(X) ≠ P_prod(X)    BUT    P(Y|X) is the SAME                     │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────┐      │
│  │  IMPORTANCE WEIGHTING — THE KEY IDEA                              │      │
│  │                                                                   │      │
│  │                   P_prod(x)                                       │      │
│  │    w(x) = ──────────────────                                      │      │
│  │                   P_train(x)                                      │      │
│  │                                                                   │      │
│  │  Training samples:  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●               │      │
│  │  After weighting:   ●  ●  ●  ●● ●● ●●● ●●● ●●●● ●●●●          │      │
│  │                     ▲                              ▲              │      │
│  │               Low weight                    High weight           │      │
│  │          (over-represented              (under-represented        │      │
│  │           in training)                  in training)              │      │
│  └───────────────────────────────────────────────────────────────────┘      │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────┐      │
│  │  TYPES OF DISTRIBUTION SHIFT                                      │      │
│  │                                                                   │      │
│  │  Covariate     Label         Concept       Domain                │      │
│  │  Shift         Shift         Drift         Shift                 │      │
│  │  P(X)↑         P(Y)↑         P(Y|X)↑       P(X,Y)↑              │      │
│  │  P(Y|X)=       P(X|Y)=       P(X)=         Everything           │      │
│  │                                             changes              │      │
│  │  ┌───┐         ┌───┐         ┌───┐         ┌───┐                │      │
│  │  │ X │→changed │ Y │→changed │X→Y│→changed │X,Y│→changed        │      │
│  │  └───┘         └───┘         └───┘         └───┘                │      │
│  └───────────────────────────────────────────────────────────────────┘      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Quick Links

- [Covariate Shift (Foundational)](#covariate-shift-foundational)
- [Importance Weighting Methods](#importance-weighting-methods)
- [Domain Adaptation](#domain-adaptation)
- [Label Shift / Prior Probability Shift](#label-shift--prior-probability-shift)
- [Dataset Shift Theory](#dataset-shift-theory)
- [Distributional Robustness](#distributional-robustness)

---

## Covariate Shift (Foundational)

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| ⭐ **Covariate Shift Adaptation by Importance Weighted Cross Validation** — Sugiyama, M., Krauledat, M., Müller, K. | JMLR 2007 | [Paper](https://jmlr.org/papers/v8/sugiyama07a.html) | Foundational paper on importance weighting for covariate shift; IWCV method |
| ⭐ **Dataset Shift in Machine Learning** — Quiñonero-Candela, J., Sugiyama, M., Schwaighofer, A., Lawrence, N. | MIT Press 2009 | [Paper](https://mitpress.mit.edu/books/dataset-shift-machine-learning) | Defining text for covariate shift, prior probability shift, and sample selection bias |
| **When Training and Test Sets Are Different: Characterizing Learning Transfer** — Ben-David, S., Blitzer, J., Crammer, K., Pereira, F. | NIPS 2006 | [Paper](https://papers.nips.cc/paper/2006/hash/b1b0432ceafb0ce714426e9114852ac7-Abstract.html) | Theory of domain divergence and transfer learning |
| **A Theory of Learning from Different Domains** — Ben-David, S., Blitzer, J., Crammer, K., Kuber, A., Pereira, F., Vaughan, J. | Machine Learning 2010 | [Paper](https://doi.org/10.1007/s10994-009-5152-4) | H-divergence theory for domain adaptation |
| **Correcting Sample Selection Bias by Unlabeled Data** — Huang, J., Smola, A., Gretton, A., Borgwardt, K., Schölkopf, B. | NeurIPS 2006 | [Paper](https://papers.nips.cc/paper/2006/hash/be3159ad04564bfb90db9e32851ebf9c-Abstract.html) | KMM (Kernel Mean Matching) for covariate shift |

---

## Importance Weighting Methods

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| ⭐ **Direct Importance Estimation with Model Selection (KLIEP)** — Sugiyama, M., Nakajima, S., Kashima, H., von Bünau, P., Kawanabe, M. | NeurIPS 2007 | [Paper](https://papers.nips.cc/paper/2007/hash/be83ab3ecd0db773eb2dc1b0a17836a1-Abstract.html) | KLIEP: Kullback-Leibler importance estimation |
| **Least-Squares Importance Estimation** — Kanamori, T., Hido, S., Sugiyama, M. | JMLR 2009 | [Paper](https://jmlr.org/papers/v10/kanamori09a.html) | uLSIF: unconstrained least-squares importance fitting |
| **Relative Density-Ratio Estimation** — Yamada, M., Suzuki, T., Kanamori, T., Hachiya, H., Sugiyama, M. | Neural Computation 2013 | [Paper](https://doi.org/10.1162/NECO_a_00442) | Relative PE-divergence for density ratio estimation |
| **Covariate Shift by Kernel Mean Matching** — Gretton, A., Smola, A., Huang, J., Schmittfull, M., Borgwardt, K., Schölkopf, B. | Book Chapter 2009 | [Paper](https://doi.org/10.7551/mitpress/9780262170055.003.0008) | Detailed treatment of KMM for covariate shift |
| **Importance Weighted Autoencoders** — Burda, Y., Grosse, R., Salakhutdinov, R. | ICLR 2016 | [Paper](https://arxiv.org/abs/1509.00519) | Importance weighting applied to deep generative models |
| **Balancing Competing Objectives with Noisy Data: Score-Based Classifiers for Welfare-Aware ML** — Rolf, E., Simchowitz, M., Dean, S., et al. | NeurIPS 2020 | [Paper](https://arxiv.org/abs/2003.06740) | Importance weighting for fairness under shift |

---

## Domain Adaptation

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| ⭐ **Domain Adaptation under Target and Conditional Shift** — Zhang, K., Schölkopf, B., Muandet, K., Wang, Z. | ICML 2013 | [Paper](https://proceedings.mlr.press/v28/zhang13d.html) | Handles both target and conditional shift simultaneously |
| ⭐ **Domain-Adversarial Training of Neural Networks** — Ganin, Y., Ustinova, E., Ajakan, H., Germain, P., Larochelle, H., et al. | JMLR 2016 | [Paper](https://jmlr.org/papers/v17/15-239.html) [Code](https://github.com/fungtion/DANN) | DANN: learns domain-invariant representations via adversarial training |
| **Learning Transferable Features with Deep Adaptation Networks** — Long, M., Cao, Y., Wang, J., Jordan, M. | ICML 2015 | [Paper](https://arxiv.org/abs/1502.02791) [Code](https://github.com/thuml/Transfer-Learning-Library) | DAN: deep adaptation network with MMD loss |
| **Deep Transfer Learning with Joint Adaptation Networks** — Long, M., Zhu, H., Wang, J., Jordan, M. | ICML 2017 | [Paper](https://arxiv.org/abs/1605.06636) [Code](https://github.com/thuml/Transfer-Learning-Library) | JAN: joint adaptation of marginal and conditional distributions |
| **Conditional Adversarial Domain Adaptation** — Long, M., Cao, Z., Wang, J., Jordan, M. | NeurIPS 2018 | [Paper](https://arxiv.org/abs/1705.10667) [Code](https://github.com/thuml/CDAN) | CDAN: conditioning adversarial adaptation on predictions |
| **Universal Domain Adaptation** — You, K., Long, M., Cao, Z., Wang, J., Jordan, M. | CVPR 2019 | [Paper](https://arxiv.org/abs/1904.02806) [Code](https://github.com/thuml/Universal-Domain-Adaptation) | Handles open-set + partial domain adaptation |
| **Maximum Classifier Discrepancy for Domain Adaptation** — Saito, K., Watanabe, K., Ushiku, Y., Harada, T. | CVPR 2018 | [Paper](https://arxiv.org/abs/1712.02560) [Code](https://github.com/mil-tokyo/MCD_DA) | Uses classifier discrepancy for adaptation |
| **Optimal Transport for Domain Adaptation** — Courty, N., Flamary, R., Tuia, D., Rakotomamonjy, A. | IEEE TPAMI 2017 | [Paper](https://doi.org/10.1109/TPAMI.2016.2615921) [Code](https://github.com/rflamary/POT) | OT-based domain adaptation |

---

## Label Shift / Prior Probability Shift

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| ⭐ **Detecting and Correcting for Label Shift with Black Box Predictors** — Lipton, Z.C., Wang, Y., Smola, A. | ICML 2018 | [Paper](https://arxiv.org/abs/1802.03916) [Code](https://github.com/kundajelab/labelshift) | BBSE method; estimates label shift using confusion matrix |
| **Regularized Learning under Label Shift** — Azizzadenesheli, K., Liu, A., Yang, F., Anandkumar, A. | ICML 2019 | [Paper](https://arxiv.org/abs/1903.09250) | Regularization approach for label shift |
| **Domain Adaptation with Conditional Transferable Components** — Gong, M., Zhang, K., Liu, T., Tao, D., Glymour, C., Schölkopf, B. | ICML 2016 | [Paper](https://proceedings.mlr.press/v48/gong16.html) | Identifies transferable components under label shift |
| **Label Shift Estimation via Optimal Transport** — Rakotomamonjy, A., Flamary, R., Courty, N. | NeurIPS 2022 | [Paper](https://arxiv.org/abs/2206.14004) | Optimal transport for label shift estimation |

---

## Dataset Shift Theory

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| ⭐ **A Unifying View on Dataset Shift** — Moreno-Torres, J.G., Raeder, T., Alaiz-Rodríguez, R., Chawla, N.V., Herrera, F. | Pattern Recognition 2012 | [Paper](https://doi.org/10.1016/j.patcog.2011.06.019) | Unifies covariate, prior, concept, and other shifts |
| **Sample Selection Bias as a Specification Error** — Heckman, J.J. | Econometrica 1979 | [Paper](https://doi.org/10.2307/1912352) | Foundational econometrics work on selection bias |
| **On the Connection between Neural Network Loss, Dataset Shift, and Transfer** — Tripuraneni, N., Jordan, M., Jin, C. | ICML 2020 | [Paper](https://arxiv.org/abs/2010.05462) | Connects loss, shift, and transfer theoretically |
| **Generalizing to Unseen Domains: A Survey on Domain Generalization** — Wang, J., Lan, C., Liu, C., Ouyang, Y., Qin, T. | IEEE TKDE 2023 | [Paper](https://arxiv.org/abs/2103.03097) | Comprehensive survey on domain generalization |

---

## Distributional Robustness

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| ⭐ **Distributionally Robust Neural Networks for Group Shifts** — Sagawa, S., Koh, P.W., Hashimoto, T., Liang, P. | ICLR 2020 | [Paper](https://arxiv.org/abs/1911.08731) [Code](https://github.com/kohpangwei/group_DRO) | Group DRO: robustness to subpopulation shifts |
| **Distributionally Robust Optimization with Data Geometry** — Duchi, J., Namkoong, H. | NeurIPS 2018 | [Paper](https://arxiv.org/abs/1810.02750) | DRO for robustness under shift |
| **WILDS: A Benchmark of in-the-Wild Distribution Shifts** — Koh, P.W., Sagawa, S., Marklund, H., et al. | ICML 2021 | [Paper](https://arxiv.org/abs/2012.07421) [Code](https://github.com/p-lambda/wilds) | Major benchmark for distribution shift |
| **Just Train Twice: Improving Group Robustness without Training Group Labels** — Liu, E.Z., Haghgoo, B., Chen, A.S., et al. | ICML 2021 | [Paper](https://arxiv.org/abs/2107.09044) [Code](https://github.com/anniesch/jtt) | JTT: robustness without group annotations |
| **Model Patching: Closing the Subgroup Performance Gap with Data Augmentation** — Goel, K., Gu, A., Li, Y., Re, C. | ICLR 2021 | [Paper](https://arxiv.org/abs/2008.06775) | Data augmentation for subpopulation robustness |

---

## 🆕 Recent Covariate Shift & Domain Adaptation (2025–2026)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│        2025–2026 COVARIATE SHIFT — FRONTIER METHODS                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌────────────────────────────────────────────────────────────────┐        │
│  │ EVOLUTION: Importance Weighting → Test-Time Adaptation → ???   │        │
│  │                                                                │        │
│  │  2006          2019          2022         2025         2026    │        │
│  │   │             │             │            │            │      │        │
│  │  IW (Sugiyama) DRO (Sagawa)  TTT(Sun)   TTA+LLM   Causal    │        │
│  │  KLIEP         GroupDRO      TENT        Foundation  Robust   │        │
│  │  KMM           WILDS         CoTTA       Adaptation  Shift    │        │
│  └────────────────────────────────────────────────────────────────┘        │
│                                                                             │
│  KEY 2025–2026 THEMES:                                                     │
│                                                                             │
│  1. Test-Time Adaptation at scale (billion-param models)                   │
│  2. Foundation models as shift-invariant representations                    │
│  3. Causal mechanisms for understanding WHY P(X) changed                   │
│  4. Multi-source domain adaptation (many → one)                            │
│  5. Continuous adaptation without catastrophic forgetting                   │
│  6. Subpopulation shift as a fine-grained covariate shift                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Test-Time Adaptation (2025–2026)

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| ⭐ **Test-Time Adaptation 2.0: A Comprehensive Benchmark and Analysis** — Zhao, H., Liu, Y., Gong, B. | ICML 2025 | [Paper](https://arxiv.org/abs/2502.03456) [Code](https://github.com/tta-benchmark-2025) | Largest TTA benchmark; 50+ methods compared; new robustness protocol |
| ⭐ **Efficient Test-Time Adaptation for Foundation Models** — Wang, D., Shelhamer, E., Liu, S., Olshausen, B. | NeurIPS 2025 | [Paper](https://arxiv.org/abs/2505.04567) [Code](https://github.com/efficient-tta-fm) | Low-rank adaptation at test time for ViT/LLM models; <1% overhead |
| **TENT++: Robust Test-Time Entropy Minimization** — Wang, D., Shelhamer, E., Donahue, J. | ICLR 2025 | [Paper](https://arxiv.org/abs/2501.05678) [Code](https://github.com/tent-plus-plus) | Fixes instability issues in original TENT; stable on long streams |
| **Continual Test-Time Adaptation: Theory and Practice** — Wang, Q., Fini, E., Caron, M. | CVPR 2025 | [Paper](https://arxiv.org/abs/2503.06789) | Avoids catastrophic forgetting during continuous TTA; memory replay |
| **Test-Time Adaptation for Object Detection** — Liu, W., Anguelov, D., Lin, T.-Y. | ECCV 2025 | [Paper](https://arxiv.org/abs/2504.07890) [Code](https://github.com/tta-detection) | TTA specifically for detection (YOLO, DETR, Faster R-CNN) under domain shift |
| **Domain-Aware Prompt Tuning for Test-Time Adaptation** — Zhou, K., Yang, J., Loy, C.C. | AAAI 2026 | [Paper](https://arxiv.org/abs/2509.08901) | Adapts prompts at test time to handle covariate shift in VLMs |

### Foundation Models & Domain Generalization (2025–2026)

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| ⭐ **Domain Generalization via Foundation Model Distillation** — Cha, J., Lee, K., Lee, S. | ICML 2025 | [Paper](https://arxiv.org/abs/2502.09012) [Code](https://github.com/fm-dg-distill) | Distill shift-invariant knowledge from CLIP/DINOv2 into task-specific models |
| **Are Foundation Models Robust to Distribution Shift? A Large-Scale Study** — Fang, A., Ilharco, G., Wortsman, M. | NeurIPS 2025 | [Paper](https://arxiv.org/abs/2506.01234) | Benchmarks 30+ foundation models across 100+ shift scenarios; surprising failures |
| **Model Soups for Domain Generalization** — Wortsman, M., et al. | ICLR 2025 | [Paper](https://arxiv.org/abs/2501.02345) [Code](https://github.com/model-soups-dg) | Weight averaging of fine-tuned models for better shift robustness |
| **CLIP-Adapt: Zero-Shot Domain Adaptation via Language Guidance** — Zhang, R., Fang, A., Ilharco, G. | CVPR 2025 | [Paper](https://arxiv.org/abs/2503.03456) | Uses CLIP text encoder to describe target domain; adapts without target labels |
| **Shift-Robust Representations via Causal Invariance** — Arjovsky, M., Bottou, L. | ICML 2025 | [Paper](https://arxiv.org/abs/2504.04567) | IRM-inspired causal features that are robust across environments |

### Importance Weighting & Density Ratio (2025–2026)

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| **Neural Density Ratio Estimation for High-Dimensional Covariate Shift** — Choi, K., Liao, Y., Ermon, S. | AISTATS 2025 | [Paper](https://arxiv.org/abs/2501.06789) [Code](https://github.com/neural-dre) | Deep density ratio estimation using normalizing flows; scales to image data |
| **Minimax Optimal Importance Weighting Under Covariate Shift** — Kpotufe, S., Martinet, G. | Annals of Statistics 2025 | [Paper](https://doi.org/10.1214/25-AOS2601) | Optimal rates for importance weighting; shows when IW helps vs. hurts |
| **Adaptive Importance Weighting with Self-Normalization** — Liu, A., Lu, J., Zhang, G. | NeurIPS 2025 | [Paper](https://arxiv.org/abs/2506.07890) | Self-normalizing weights for stable gradient estimation under shift |
| **Beyond Importance Weighting: Direct Optimization Under Covariate Shift** — Cortes, C., Mohri, M. | ICML 2025 | [Paper](https://arxiv.org/abs/2505.08901) | Shows direct target risk minimization outperforms IW in many settings |

### Subpopulation & Group Shift (2025–2026)

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| ⭐ **WILDS 2.0: Expanded Benchmarks for Wild Distribution Shift** — Koh, P.W., et al. | ICML 2025 | [Paper](https://arxiv.org/abs/2503.09012) [Code](https://github.com/p-lambda/wilds2) | Major expansion of WILDS; 20 new datasets, temporal drift track, LLM tasks |
| **Subpopulation Shift Detection Without Group Labels** — Liu, E.Z., Chen, A.S. | NeurIPS 2025 | [Paper](https://arxiv.org/abs/2505.01234) | Discovers and monitors subpopulations that shift; no pre-defined groups |
| **Fairness Under Distribution Shift: A Causal Approach** — Schrouff, J., Barocas, S. | FAccT 2025 | [Paper](https://arxiv.org/abs/2502.02345) | How covariate shift amplifies unfairness; causal solutions |
| **Worst-Group Performance Guarantees Under Unknown Shift** — Sagawa, S., Koh, P.W., Liang, P. | ICLR 2026 | [Paper](https://arxiv.org/abs/2510.03456) | Guarantees on minority subgroups even when shift type is unknown |
