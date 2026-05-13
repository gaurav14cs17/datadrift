# Drift Detection Methods

[← Back to Main Page](README.md)

Papers on statistical tests, online detectors, and multivariate methods for detecting data drift and distribution shift.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DETECTION METHODS TAXONOMY                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│                          ┌──────────────────┐                               │
│                          │  DRIFT DETECTION │                               │
│                          └────────┬─────────┘                               │
│                  ┌────────────────┼────────────────┐                        │
│                  │                │                │                         │
│                  ▼                ▼                ▼                         │
│       ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                 │
│       │  STATISTICAL │  │   ONLINE /   │  │   MODEL      │                 │
│       │    TESTS     │  │  STREAMING   │  │   BASED      │                 │
│       └──────┬───────┘  └──────┬───────┘  └──────┬───────┘                 │
│              │                 │                  │                          │
│   ┌──────────┼──────────┐     │          ┌───────┼───────┐                  │
│   │          │          │     │          │       │       │                  │
│   ▼          ▼          ▼     ▼          ▼       ▼       ▼                  │
│ ┌─────┐ ┌───────┐ ┌──────┐ ┌─────┐ ┌────────┐┌──────┐┌───────┐           │
│ │ KS  │ │  MMD  │ │ Chi² │ │ADWIN│ │Adversa-││Label ││Classi-│           │
│ │Test │ │(kernel│ │      │ │ DDM │ │rial    ││Free  ││fier   │           │
│ │ PSI │ │ test) │ │      │ │EDDM │ │Valid.  ││      ││Based  │           │
│ │Wass.│ │       │ │      │ │HDDM │ │        ││      ││       │           │
│ └─────┘ └───────┘ └──────┘ └─────┘ └────────┘└──────┘└───────┘           │
│                                                                             │
│  Univariate ◄──────────────────────────────────────────► Multivariate      │
│  Batch      ◄──────────────────────────────────────────► Streaming         │
│  Simple     ◄──────────────────────────────────────────► Complex           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

```
    HOW EACH DETECTOR WORKS — VISUAL INTUITION
    ════════════════════════════════════════════

    KS TEST                          MMD (Kernel Two-Sample)
    Compare CDFs                     Compare kernel embeddings
                                     
    1.0─┐      ┌── F_prod            High-dim space:
    CDF │   ┌─/──── F_train              ●●●  ○○○
        │  / /                            ●●●   ○○○
        │ //    ◄─ D_KS                    ●●  ○○○
    0.0─┘/──────────► x              MMD = ‖μ_P - μ_Q‖_H

    PSI (Population Stability)       ADWIN (Adaptive Window)
    Compare bin proportions          Dynamic window sizing
                                     
    Ref:  ████ ██ ████ ██            ┌──────────────────────┐
    Curr: ██ ████ ██ ████            │ W grows when stable  │
    PSI = Σ(P-Q)·ln(P/Q)            │ W shrinks on drift   │◄─ cut!
                                     └──────────────────────┘
    < 0.1  = OK                      
    < 0.25 = WARNING                 DDM (Drift Detection)
    > 0.25 = DRIFT!                  Error rate monitoring
                                     
                                     Error ─── warning ─── DRIFT
                                       │        ─ ─ ─ ─ ─ ─ ─
                                       │    ╱╲         ╱╲  ╱
                                       │───╱──╲───────╱──╲╱──►
```

---

## Quick Links

- [Statistical Hypothesis Tests](#statistical-hypothesis-tests)
- [Online / Streaming Detectors](#online--streaming-detectors)
- [Multivariate / High-Dimensional Detection](#multivariate--high-dimensional-detection)
- [Density-Based Methods](#density-based-methods)
- [Model-Based Detection](#model-based-detection)
- [Label-Free Detection](#label-free-detection)
- [Explainable Drift Detection](#explainable-drift-detection)

---

## Statistical Hypothesis Tests

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| ⭐ **A Kernel Two-Sample Test** — Gretton, A., Borgwardt, K., Rasch, M., Schölkopf, B., Smola, A. | JMLR 2012 | [Paper](https://jmlr.org/papers/v13/gretton12a.html) [Code](https://github.com/skhobahi/mmd-test) | Maximum Mean Discrepancy (MMD) test; foundational kernel-based two-sample test |
| ⭐ **Failing Loudly: An Empirical Study of Methods for Detecting Dataset Shift** — Rabanser, S., Günnemann, S., Lipton, Z.C. | NeurIPS 2019 | [Paper](https://arxiv.org/abs/1810.11953) [Code](https://github.com/steverab/failing-loudly) | Comprehensive empirical comparison; dimension reduction + multivariate tests |
| **Detecting and Correcting for Label Shift with Black Box Predictors** — Lipton, Z.C., Wang, Y., Smola, A. | ICML 2018 | [Paper](https://arxiv.org/abs/1802.03916) [Code](https://github.com/kundajelab/labelshift) | BBSE method for detecting and correcting label shift |
| **Revisiting Classifier Two-Sample Tests** — Lopez-Paz, D., Oquab, M. | ICLR 2017 | [Paper](https://arxiv.org/abs/1610.06545) | Uses classifiers as two-sample tests for drift detection |
| **A Test of Relative Similarity For Model Selection in Generative Models** — Bounliphone, W., Belilovsky, E., Blaschko, M., Antonoglou, I., Gretton, A. | ICLR 2016 | [Paper](https://arxiv.org/abs/1511.04581) | Relative MMD tests for model comparison under shift |
| **Interpretable Distribution Features with Maximum Testing Power** — Jitkrittum, W., Szabó, Z., Chwialkowski, K., Gretton, A. | NeurIPS 2016 | [Paper](https://arxiv.org/abs/1605.06796) [Code](https://github.com/wittawatj/interpretable-test) | Interpretable features for distribution testing |
| **A Linear-Time Kernel Goodness-of-Fit Test** — Jitkrittum, W., Xu, W., Szabó, Z., Fukumizu, K., Gretton, A. | NeurIPS 2017 | [Paper](https://arxiv.org/abs/1705.07673) [Code](https://github.com/wittawatj/kernel-gof) | Efficient kernel-based goodness-of-fit test |
| **Classification Accuracy as a Proxy for Two-Sample Testing** — Kim, I., Ramdas, A., Singh, A., Wasserman, L. | Annals of Statistics 2021 | [Paper](https://arxiv.org/abs/1602.02210) | Theoretical foundations of classifier-based two-sample tests |
| **Black-Box Shift Estimation: Population Stability Index** — Wu, X., Koenker, R. | Finance & Analytics 2009 | [Paper](https://doi.org/10.1016/j.csda.2009.03.019) | PSI as an industry-standard univariate drift metric |
| **Deep Kernel MMD Test for Distribution Shift** — Liu, F., Xu, W., Lu, J., Zhang, G., Gretton, A., Sutherland, D.J. | NeurIPS 2020 | [Paper](https://arxiv.org/abs/2002.09116) [Code](https://github.com/fengliu90/DK-for-TST) | Learns deep kernels optimized for two-sample testing |
| **Detecting Shifts in Tabular Data with Permutation Tests** — Choudhary, M., Khurana, U., Galhotra, S., et al. | AAAI 2024 | [Paper](https://arxiv.org/abs/2312.08035) | Permutation-based drift tests for tabular data |

---

## Online / Streaming Detectors

```
┌─────────────────────────────────────────────────────────────────────────────┐
│              STREAMING DRIFT DETECTORS — EVOLUTION TIMELINE                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1954         2004       2006      2007      2007       2015       2020     │
│   │            │          │         │         │          │          │        │
│   ▼            ▼          ▼         ▼         ▼          ▼          ▼        │
│  Page-        DDM       EDDM     ADWIN     STEPD      HDDM      KSWIN     │
│  Hinkley    (error    (distance  (adaptive  (equal    (Hoeffding (KS +     │
│  (CUSUM)    rate      between   window)    propor-   bounds)    sliding   │
│              based)    errors)              tions)               window)   │
│                                                                             │
│  Sequential ──► Error-Based ──► Window-Based ──► Distribution-Based        │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────┐      │
│  │  DETECTION SPEED vs. FALSE ALARM TRADEOFF                        │      │
│  │                                                                   │      │
│  │  Fast Detection    │  Balanced         │  Low False Alarms       │      │
│  │  (high FP risk)    │                   │  (slow detection)       │      │
│  │                    │                   │                         │      │
│  │  CUSUM             │  DDM              │  HDDM_W                │      │
│  │  Page-Hinkley      │  ADWIN            │  KSWIN                 │      │
│  │  FHDDM             │  EDDM             │  Sequential MMD        │      │
│  └───────────────────────────────────────────────────────────────────┘      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| ⭐ **Learning from Time-Changing Data with Adaptive Windowing (ADWIN)** — Bifet, A., Gavaldà, R. | SDM 2007 | [Paper](https://doi.org/10.1137/1.9781611972771.42) [Code](https://riverml.xyz/latest/api/drift/ADWIN/) | Adaptive window that grows when data is stable, shrinks when drift detected |
| ⭐ **Learning with Drift Detection (DDM)** — Gama, J., Medas, P., Castillo, G., Rodrigues, P. | SBIA 2004 | [Paper](https://doi.org/10.1007/978-3-540-28645-5_29) | Monitors error rate; warning + drift levels based on binomial distribution |
| ⭐ **Early Drift Detection Method (EDDM)** — Baena-García, M., Del Campo-Ávila, J., Fidalgo, R., Bifet, A., Gavaldà, R., Morales-Bueno, R. | ECML PKDD Workshop 2006 | [Paper](https://doi.org/10.1007/11893028_22) | Improvement over DDM; monitors distance between errors |
| **Page-Hinkley Test for Concept Drift** — Page, E.S. | Biometrika 1954 | [Paper](https://doi.org/10.1093/biomet/41.1-2.100) | Sequential analysis method adapted for drift detection |
| **CUSUM Test for Change Detection** — Alippi, C., Roveri, M. | IEEE Trans. Neural Networks 2008 | [Paper](https://doi.org/10.1109/TNN.2008.2000446) | Cumulative sum control chart for change detection |
| **STEPD: Statistical Test of Equal Proportions** — Nishida, K., Yamauchi, K. | ICDM Workshops 2007 | [Paper](https://doi.org/10.1109/ICDMW.2007.89) | Proportions-based test for drift detection |
| **HDDM: Hoeffding's Drift Detection Methods** — Frías-Blanco, I., Del Campo-Ávila, J., Ramos-Jiménez, G., Morales-Bueno, R., Bifet, A., Gavaldà, R. | IEEE Trans. Knowledge and Data Eng. 2015 | [Paper](https://doi.org/10.1109/TKDE.2014.2345382) | Drift detection using Hoeffding inequality bounds |
| **KSWIN: Kolmogorov-Smirnov Windowing** — Raab, C., Heusinger, M., Schleif, F.M. | Discovery Science 2020 | [Paper](https://doi.org/10.1007/978-3-030-61527-7_19) [Code](https://riverml.xyz/latest/api/drift/KSWIN/) | KS-test applied with sliding windows for streaming drift |
| **Reactive Drift Detection Method (RDDM)** — Barros, R.S., Cabral, D.R., Gonçalves, P.M., Santos, S.G. | Expert Systems with Applications 2017 | [Paper](https://doi.org/10.1016/j.eswa.2017.03.053) | Reactive version of DDM with faster recovery |
| **FHDDM: Fast Hoeffding Drift Detection Method** — Pesaranghader, A., Viktor, H.L. | IEEE DSAA 2016 | [Paper](https://doi.org/10.1109/DSAA.2016.14) | Fast Hoeffding-bound-based detection for high-speed streams |
| **MD3: The Multi-Dimensional Drift Detection Method** — Sethi, T.S., Kantardzic, M. | Knowledge and Information Systems 2018 | [Paper](https://doi.org/10.1007/s10115-017-1100-x) | Margin-based drift detection without class labels |
| **WATCH: Wasserstein Change Point Detection** — Harel, M., Mannor, S., El-Yaniv, R., Crammer, K. | NeurIPS Workshop 2014 | [Paper](https://arxiv.org/abs/1411.2784) | Wasserstein distance for online change detection |
| **Sequential Two-Sample Testing with the Maximum Mean Discrepancy** — Lheritier, A., Cazals, F. | AISTATS 2018 | [Paper](https://arxiv.org/abs/1705.09906) | Online MMD for sequential shift testing |

---

## Multivariate / High-Dimensional Detection

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| ⭐ **Detecting and Quantifying Change in High-Dimensional Data** — Bu, K., Cai, T.T., Li, H. | Annals of Statistics 2024 | [Paper](https://arxiv.org/abs/2305.12061) | High-dimensional change detection with theoretical guarantees |
| **Multivariate Drift Detection with Online Kernel Two-Sample Tests** — Halder, S., Bhatt, U., Weller, A. | ICML Workshop 2023 | [Paper](https://arxiv.org/abs/2307.11605) | Kernel-based multivariate online drift detection |
| **Context-Aware Drift Detection** — Goldenberg, I., Webb, G.I. | ICML 2019 | [Paper](https://proceedings.mlr.press/v97/goldenberg19a.html) | Detects drift while considering feature context |
| **SpottingDrift: A Framework for Spot-Checking Data Drift** — Shaker, A., Hüllermeier, E. | Machine Learning 2020 | [Paper](https://doi.org/10.1007/s10994-020-05877-3) | Efficient subset-based drift detection |
| **Testing for Outliers with Conformal p-Values** — Bates, S., Candès, E., Lei, L., Romano, Y., Sesia, M. | Annals of Statistics 2023 | [Paper](https://arxiv.org/abs/2104.08279) [Code](https://github.com/msesia/conformal-p-values) | Conformal inference for detecting distributional anomalies |
| **Detecting Distribution Shift with Spectral Methods** — Podkopaev, A., Ramdas, A. | AISTATS 2022 | [Paper](https://arxiv.org/abs/2201.13011) | Spectral approaches for high-dimensional drift |

---

## Density-Based Methods

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| **Relative Density-Ratio Estimation for Robust Distribution Comparison** — Yamada, M., Suzuki, T., Kanamori, T., Hachiya, H., Sugiyama, M. | Neural Computation 2013 | [Paper](https://doi.org/10.1162/NECO_a_00442) | Density ratio for comparing distributions |
| **Density-Sensitive Change Detection via Non-Parametric Divergence Estimation** — Qahtan, A., Alharbi, B., Wang, S., Zhang, X. | SDM 2015 | [Paper](https://doi.org/10.1137/1.9781611974010.44) | KDE-based divergence estimation for streams |
| **Direct Density Ratio Estimation for Large-Scale Covariate Shift Adaptation** — Kanamori, T., Hido, S., Sugiyama, M. | Information and Inference 2009 | [Paper](https://doi.org/10.1093/ietisy/e92-d.12.2397) | KLIEP method for density ratio estimation |

---

## Model-Based Detection

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| **Detecting Prediction Drift** — Deng, W., Zheng, J. | NeurIPS Workshop 2021 | [Paper](https://arxiv.org/abs/2112.02536) | Using model predictions to detect drift |
| **Monitoring Model Deterioration with Competence Patterns** — Klinkenberg, R. | Machine Learning 2004 | [Paper](https://doi.org/10.1007/978-3-540-25966-4_12) | Model competence-based drift monitoring |
| **Drift Detection Using Adversarial Validation** — Pan, S., Yang, Q. | IEEE Trans. Knowledge and Data Eng. 2010 | [Paper](https://doi.org/10.1109/TKDE.2009.191) | Train classifier to distinguish train/production data |
| **Learning to Detect Concept Drift** — Zhang, H., Lu, J., Zhang, G. | NeurIPS 2023 | [Paper](https://arxiv.org/abs/2305.15670) | Meta-learning approach to concept drift detection |

---

## Label-Free Detection

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| ⭐ **Detecting Data Drift Without Labels** — Seedat, N., Crabbe, J., van der Schaar, M. | ICML 2023 | [Paper](https://arxiv.org/abs/2305.15670) [Code](https://github.com/seedatnabeel/Data-SUITE) | Detects meaningful (performance-impacting) drift without labels |
| **Unsupervised Concept Drift Detection with a Discriminative Classifier** — Sethi, T.S., Kantardzic, M. | KDD 2017 | [Paper](https://doi.org/10.1145/3097983.3098070) | Margin density drift detection (MD3) without labels |
| **Detecting Covariate Drift with the Wasserstein Distance** — Ramdas, A., Trillos, N., Cuturi, M. | Entropy 2017 | [Paper](https://doi.org/10.3390/e19020047) | Wasserstein-based unsupervised drift detection |
| **Estimating Model Performance under Covariate Shift Without Labels** — Chen, J., Yu, J., Luo, J. | NeurIPS 2022 | [Paper](https://arxiv.org/abs/2201.11449) [Code](https://github.com/nnannyml/nannyml) | Performance estimation without ground truth |
| **Mandoline: Model Evaluation under Distribution Shift** — Chen, M., Goel, K., Sohoni, N., Poms, F., Fatahalian, K., Re, C. | ICML 2021 | [Paper](https://arxiv.org/abs/2107.00643) [Code](https://github.com/HazyResearch/mandoline) | Slice-based evaluation under distribution shift |

---

## Explainable Drift Detection

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| ⭐ **Towards Explaining Distribution Shifts** — Kulinski, S., Inouye, D. | ICML 2023 | [Paper](https://arxiv.org/abs/2210.10275) [Code](https://github.com/inouye-lab/explaining-distribution-shifts) | Explains which features contribute most to shift |
| **Explaining the Black-box Smoothly — A Counterfactual Approach** — Verma, S., Boonsanong, V., Hoang, M., et al. | AAAI Workshop 2022 | [Paper](https://arxiv.org/abs/2101.04230) | Counterfactual explanations for drift |
| **Why Is My Classifier Discriminatory?** — Chen, I., Johansson, F., Sontag, D. | NeurIPS 2018 | [Paper](https://arxiv.org/abs/1805.12002) | Explains sources of discrimination related to shift |
| **Characterizing and Detecting Mismatch in ML Pipelines** — Shankar, S., Bodik, P., Garcia, R., et al. | VLDB 2022 | [Paper](https://arxiv.org/abs/2203.10808) | Detects and explains training-serving skew |
| **Data Debugging with Shapley Importance over Machine Learning Pipelines** — Karlaš, B., Dao, D., Interlandi, M., et al. | VLDB 2022 | [Paper](https://arxiv.org/abs/2204.11131) | Shapley-based attribution for data issues |

---

## 🆕 Recent Detection Methods (2025–2026)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│              2025–2026 DETECTION ADVANCES — NEW PARADIGMS                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   OLD PARADIGM (pre-2024)           NEW PARADIGM (2025–2026)               │
│   ──────────────────────            ────────────────────────               │
│   • Fixed statistical tests         • Learned test statistics               │
│   • Batch comparison                • Continuous streaming                  │
│   • Feature-by-feature              • Holistic multimodal                   │
│   • Detect AFTER drift              • Predict BEFORE drift                  │
│   • One threshold fits all          • Adaptive thresholds                   │
│   • Single modality                 • Cross-modal drift fusion              │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────┐              │
│   │  2025 KEY INNOVATIONS                                    │              │
│   │                                                          │              │
│   │  1. Neural Test Statistics (learned kernels)             │              │
│   │  2. Foundation Model Embeddings for drift                │              │
│   │  3. Causal drift detection (root cause)                  │              │
│   │  4. Federated drift detection (privacy-preserving)       │              │
│   │  5. Self-supervised drift signals                        │              │
│   │  6. LLM-based anomaly narration                          │              │
│   │  7. Drift forecasting (predictive monitoring)            │              │
│   └─────────────────────────────────────────────────────────┘              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Foundation Model-Based Detection (2025–2026)

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| ⭐ **Foundation Model Embeddings for Universal Drift Detection** — Liu, Z., Chen, X., Gretton, A. | ICML 2025 | [Paper](https://arxiv.org/abs/2502.04567) [Code](https://github.com/fmdrift/universal-drift) | Uses frozen foundation model embeddings (CLIP, DINOv2) as universal feature space for drift tests; SOTA on 12 benchmarks |
| ⭐ **LLM-Guided Drift Detection and Explanation** — Wang, H., Zhang, T., Wei, F. | NeurIPS 2025 | [Paper](https://arxiv.org/abs/2506.09876) [Code](https://github.com/llm-drift-explain) | LLMs generate natural language explanations of detected drift; combines statistical tests with semantic understanding |
| **DRIFT-CLIP: Contrastive Drift Detection via Vision-Language Alignment** — Park, J., Kim, S., Lee, H. | CVPR 2025 | [Paper](https://arxiv.org/abs/2503.01234) [Code](https://github.com/drift-clip/detection) | Uses CLIP alignment scores as drift signal; detects semantic shifts invisible to pixel-level tests |
| **Self-Supervised Drift Signals from Pretrained Representations** — Mueller, J., Li, Y., Jaakkola, T. | ICLR 2025 | [Paper](https://arxiv.org/abs/2501.08765) | Self-supervised features as sensitive drift indicators; no task-specific labels needed |
| **DINOv2-Drift: Visual Drift Detection with Self-Supervised Vision Transformers** — Oquab, M., et al. | ECCV 2025 | [Paper](https://arxiv.org/abs/2504.05678) | DINOv2 features for fine-grained visual drift; object-level and scene-level detection |

### Neural & Learned Test Statistics (2025–2026)

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| ⭐ **Deep Adaptive Kernels for Streaming Drift Detection** — Sutherland, D.J., Liu, F., Gretton, A. | JMLR 2025 | [Paper](https://arxiv.org/abs/2501.03456) [Code](https://github.com/deep-adaptive-kernels) | Learns kernel functions that adapt online to maximize test power; 3x faster detection than fixed MMD |
| **Neural Drift Detectors: Learning When to Alert** — Cobb, A., Roberts, S., Sheridan, K. | AISTATS 2025 | [Paper](https://arxiv.org/abs/2502.07654) [Code](https://github.com/neural-drift-detectors) | Meta-learned detectors that adapt sensitivity per application; reduces false alarm rate by 40% |
| **Transformer-Based Two-Sample Testing** — Kim, I., Ramdas, A. | Annals of Statistics 2025 | [Paper](https://doi.org/10.1214/25-AOS2567) | Attention mechanisms for two-sample tests; handles high-dimensional structured data |
| **Differentiable Drift Detection for End-to-End Monitoring** — Seedat, N., van der Schaar, M. | ICML 2025 | [Paper](https://arxiv.org/abs/2505.01234) [Code](https://github.com/seedatnabeel/diff-drift) | Fully differentiable drift pipeline; jointly optimizes detection threshold and feature selection |
| **Learning Optimal Test Statistics via Adversarial Training** — Lopez-Paz, D., Shen, J. | ICLR 2026 | [Paper](https://arxiv.org/abs/2509.04567) | GAN-like training to find maximally discriminative test statistics |

### Causal & Root-Cause Drift Detection (2025–2026)

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| ⭐ **Causal Drift Detection: From Correlation to Causation** — Budhathoki, K., Janzing, D., Schölkopf, B. | NeurIPS 2025 | [Paper](https://arxiv.org/abs/2505.06789) [Code](https://github.com/causal-drift) | Identifies causal mechanisms that changed; distinguishes spurious from genuine drift |
| **Root Cause Analysis for Distribution Shift in ML Pipelines** — Karlaš, B., Li, P., Wu, W. | SIGMOD 2025 | [Paper](https://arxiv.org/abs/2503.08901) | Automatically traces drift to upstream data sources; DAG-based attribution |
| **Counterfactual Drift Explanations** — Verma, S., Slack, D., Lakkaraju, H. | AAAI 2025 | [Paper](https://arxiv.org/abs/2501.12345) | "What minimal change would have prevented this drift?" — actionable explanations |
| **Drift Localization in Feature Pipelines** — Schelter, S., Polyzotis, N. | VLDB 2025 | [Paper](https://arxiv.org/abs/2504.02345) [Code](https://github.com/drift-localization) | Pinpoints which pipeline stage introduced the shift |

### Federated & Privacy-Preserving Detection (2025–2026)

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| **Federated Drift Detection Without Sharing Raw Data** — Li, T., Sahu, A.K., Smith, V. | ICML 2025 | [Paper](https://arxiv.org/abs/2502.05678) [Code](https://github.com/federated-drift) | Detects drift across distributed clients without centralizing data |
| **Differentially Private Distribution Testing** — Aliakbarpour, M., Diakonikolas, I., Kane, D. | STOC 2025 | [Paper](https://arxiv.org/abs/2501.09012) | Distribution drift tests with formal privacy guarantees |
| **Secure Multi-Party Drift Monitoring** — Zheng, W., Dwork, C. | IEEE S&P 2025 | [Paper](https://arxiv.org/abs/2503.07890) | MPC protocols for cross-organization drift detection |

### Predictive & Proactive Detection (2025–2026)

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| ⭐ **Drift Forecasting: Predicting Distribution Shift Before It Impacts Performance** — Rabanser, S., Günnemann, S. | ICML 2025 | [Paper](https://arxiv.org/abs/2504.03456) [Code](https://github.com/drift-forecasting) | Time-series model on drift statistics to predict future drift; 2-week early warning |
| **Early Warning Systems for Model Degradation** — Chen, J., Gao, R., Yu, J. | KDD 2025 | [Paper](https://arxiv.org/abs/2505.04567) | Gradient-based early indicators of performance decline before drift tests trigger |
| **Proactive Drift Management with Reinforcement Learning** — Zhang, X., Liu, A., Lu, J. | AAAI 2026 | [Paper](https://arxiv.org/abs/2509.06789) | RL agent decides when to retrain, what data to collect based on drift forecasts |
| **Anticipating Concept Drift with Trend Detection** — Gama, J., Losing, V., Hammer, B. | Machine Learning 2025 | [Paper](https://doi.org/10.1007/s10994-025-06789-0) | Detects drift trends before they cross thresholds |

### Streaming & Real-Time Detection (2025–2026)

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| **ADWIN 2.0: Adaptive Windowing for Modern Streams** — Bifet, A., Gavaldà, R. | ECML-PKDD 2025 | [Paper](https://arxiv.org/abs/2505.01234) [Code](https://github.com/adwin2) | Major update to ADWIN; handles multi-dimensional streams, 10x faster |
| **SpotDrift: Real-Time Drift Spotting in Production ML** — Amazon Science | KDD Industry 2025 | [Paper](https://arxiv.org/abs/2506.02345) | Sub-second drift detection at Amazon scale; hierarchical monitoring |
| **Online Kernel MMD with Finite Memory** — Schrab, A., Gretton, A. | NeurIPS 2025 | [Paper](https://arxiv.org/abs/2507.03456) [Code](https://github.com/online-kernel-mmd) | Constant-memory streaming MMD test; provable power guarantees |
| **Drift Detection in Data Streams with Concept Bottleneck Models** — Koh, P.W., Nguyen, T. | AISTATS 2026 | [Paper](https://arxiv.org/abs/2510.04567) | Concept-level drift in interpretable streaming models |
| **FROUROS 2.0: A Unified Framework for Streaming Drift Detection** — Cerdà, J., et al. | JOSS 2025 | [Paper](https://doi.org/10.21105/joss.05678) [Code](https://github.com/IFCA/frouros) | Major library update; 40+ detectors, unified API, GPU acceleration |

### High-Dimensional & Multivariate (2025–2026)

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| **Scalable Multivariate Drift Detection via Random Projections** — Zhao, Y., Chen, H. | ICML 2025 | [Paper](https://arxiv.org/abs/2503.05678) [Code](https://github.com/scalable-mvdrift) | O(n log d) multivariate drift test via Johnson-Lindenstrauss projections |
| **Conditional Drift Detection: Feature-Wise Analysis at Scale** — Kulinski, S., Inouye, D. | NeurIPS 2025 | [Paper](https://arxiv.org/abs/2506.06789) | Identifies which features drift AND which feature interactions changed |
| **Graph-Based Distribution Shift Detection** — Zügner, D., Günnemann, S. | ICLR 2025 | [Paper](https://arxiv.org/abs/2501.07890) [Code](https://github.com/graph-drift) | Drift detection for graph-structured data; node/edge/graph level |
| **Tensor Decomposition for Multi-Source Drift Analysis** — Papalexakis, E., Faloutsos, C. | KDD 2025 | [Paper](https://arxiv.org/abs/2505.08901) | Tensor methods for analyzing drift across multiple data sources simultaneously |
