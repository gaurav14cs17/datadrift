# Benchmarks & Datasets

[← Back to Main Page](README.md)

Standard benchmarks, datasets, and evaluation frameworks for testing data drift detection and adaptation methods.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    BENCHMARK LANDSCAPE OVERVIEW                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  SYNTHETIC GENERATORS                    REAL-WORLD BENCHMARKS              │
│  ════════════════════                    ════════════════════               │
│                                                                             │
│  ┌───────────────────┐                   ┌───────────────────┐             │
│  │   MOA / River     │                   │     WILDS         │             │
│  │                   │                   │  (10 datasets)    │             │
│  │  SEA ─── sudden   │                   │  ┌─────┐ ┌─────┐ │             │
│  │  Hyperplane ─ grad│                   │  │Camel│ │FMoW │ │             │
│  │  RBF ─── gradual  │                   │  │yon17│ │     │ │             │
│  │  STAGGER ── recur │                   │  └─────┘ └─────┘ │             │
│  │  Agrawal ── mixed │                   │  ┌─────┐ ┌─────┐ │             │
│  │                   │                   │  │iWild│ │Civil │ │             │
│  │  Configurable:    │                   │  │Cam  │ │Comm. │ │             │
│  │  • Drift speed    │                   │  └─────┘ └─────┘ │             │
│  │  • # features     │                   └───────────────────┘             │
│  │  • Noise level    │                                                     │
│  └───────────────────┘                   ┌───────────────────┐             │
│                                          │  ImageNet-C/P/R/A │             │
│  STREAMING DATASETS                      │  75 corruptions   │             │
│  ══════════════════                      │  5 severity levels│             │
│  ┌───────────────────┐                   └───────────────────┘             │
│  │                   │                                                     │
│  │  Electricity 45K  │                   ┌───────────────────┐             │
│  │  Airlines   539K  │                   │   TableShift      │             │
│  │  Covertype  581K  │                   │  (15 tabular      │             │
│  │  KDD Cup   4.9M   │                   │   datasets)       │             │
│  │  Gas Sensor  14K  │                   └───────────────────┘             │
│  │  Spam        9K   │                                                     │
│  │                   │                   ┌───────────────────┐             │
│  └───────────────────┘                   │    Wild-Time      │             │
│                                          │  (5 temporal      │             │
│                                          │   shift datasets) │             │
│                                          └───────────────────┘             │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────┐      │
│  │  DATASET SIZE COMPARISON (log scale)                              │      │
│  │                                                                   │      │
│  │  KDD Cup    ████████████████████████████████████████████  4.9M    │      │
│  │  Covertype  █████████████████████████████████            581K    │      │
│  │  Airlines   █████████████████████████████                539K    │      │
│  │  Poker Hand ████████████████████████████████████         1.0M    │      │
│  │  Electricity████████████                                  45K    │      │
│  │  Weather    ████████                                      18K    │      │
│  │  Gas Sensor ███████                                       14K    │      │
│  │  Spam       ████                                           9K    │      │
│  │  Usenet     ███                                            6K    │      │
│  └───────────────────────────────────────────────────────────────────┘      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

```
    SYNTHETIC DRIFT PATTERNS — VISUAL EXAMPLES
    ═══════════════════════════════════════════

    SEA Generator (Sudden Drift):
    ┌────────────────────────────────────────────┐
    │  Concept A          │  Concept B           │
    │  f1 + f2 ≤ θ₁      │  f1 + f2 ≤ θ₂       │
    │  ●●●●●●●●●●        │  ○○○○○○○○○○         │
    │  ●●●●●●●●●●        │  ○○○○○○○○○○         │
    │  ●●●●●●●●●●   DRIFT│  ○○○○○○○○○○         │
    │─────────────────────┼──────────────────────│
    │       t=0      t=5000      t=10000         │
    └────────────────────────────────────────────┘

    Hyperplane Generator (Gradual Drift):
    ┌────────────────────────────────────────────┐
    │         ╱              ╱              ╱     │
    │        ╱ slowly       ╱ rotating    ╱      │
    │  ●●●● ╱  ○○○   ●●● ╱  ○○○○   ●● ╱ ○○○○○ │
    │  ●●● ╱ ○○○○    ●● ╱  ○○○○○    ● ╱ ○○○○○○ │
    │  ●● ╱ ○○○○○    ● ╱  ○○○○○○     ╱ ○○○○○○○ │
    │─────────────────────────────────────────────│
    │    t=0          t=5000          t=10000     │
    └────────────────────────────────────────────┘

    STAGGER Generator (Recurring):
    ┌────────────────────────────────────────────┐
    │  Concept A    Concept B    Concept A again  │
    │  (color=red)  (size=big)   (color=red)      │
    │  ████████    ░░░░░░░░    ████████          │
    │  ████████    ░░░░░░░░    ████████          │
    │─────────────────────────────────────────────│
    │    t=0      t=5000     t=10000    t=15000  │
    └────────────────────────────────────────────┘
```

---

## Quick Links

- [Major Benchmarks](#major-benchmarks)
- [Synthetic Drift Generators](#synthetic-drift-generators)
- [Real-World Drift Datasets](#real-world-drift-datasets)
- [Domain-Specific Datasets](#domain-specific-datasets)
- [Evaluation Metrics & Protocols](#evaluation-metrics--protocols)

---

## Major Benchmarks

| Name & Authors | Venue | Links | Description |
|---|---|---|---|
| ⭐ **WILDS: A Benchmark of in-the-Wild Distribution Shifts** — Koh, P.W., Sagawa, S., et al. | ICML 2021 | [Paper](https://arxiv.org/abs/2012.07421) [Code](https://github.com/p-lambda/wilds) [Website](https://wilds.stanford.edu/) | 10 datasets spanning vision, text, graphs with real-world distribution shifts; includes Camelyon17, FMoW, iWildCam, PovertyMap, etc. |
| ⭐ **BREEDS: Benchmarks for Subpopulation Shift** — Santurkar, S., Tsipras, D., Madry, A. | ICML 2021 | [Paper](https://arxiv.org/abs/2008.04859) [Code](https://github.com/MadryLab/BREEDS-Benchmarks) | Subpopulation shift using ImageNet class hierarchy; entity-13, entity-30, living-17, nonliving-26 |
| **TableShift: A Benchmark for Tabular Distribution Shifts** — Gardner, J., Popovic, Z., Schmidt, L. | NeurIPS 2023 | [Paper](https://arxiv.org/abs/2312.07577) [Code](https://github.com/mlfoundations/tableshift) | 15 tabular datasets with real-world domain shifts; healthcare, income, voting, food, etc. |
| **Wild-Time: A Benchmark of in-the-Wild Distribution Shifts over Time** — Yao, H., Choi, C., Cao, B., et al. | NeurIPS 2022 | [Paper](https://arxiv.org/abs/2211.14238) [Code](https://github.com/huaxiuyao/Wild-Time) | Temporal distribution shift across 5 datasets |
| **ImageNet-C / ImageNet-P** — Hendrycks, D., Dietterich, T. | ICLR 2019 | [Paper](https://arxiv.org/abs/1903.12261) [Code](https://github.com/hendrycks/robustness) | 75 corruption types at 5 severity levels for robustness evaluation |
| **DomainNet** — Peng, X., Bai, Q., et al. | ICCV 2019 | [Paper](https://arxiv.org/abs/1812.01754) [Code](http://ai.bu.edu/M3SDA/) | 6 domains, 345 categories, ~600K images for domain adaptation |
| **Office-Home** — Venkateswara, H., Eusebio, J., Chakraborty, S., Panchanathan, S. | CVPR 2017 | [Paper](https://arxiv.org/abs/1706.07522) [Data](https://www.hemanthdv.org/officeHomeDataset.html) | 4 domains (Art, Clipart, Product, Real), 65 categories |
| **Shifts Dataset** — Malinin, A., Band, N., Gal, Y., et al. | NeurIPS 2021 | [Paper](https://arxiv.org/abs/2107.07455) [Code](https://github.com/Shifts-Project/shifts) | Weather prediction, machine translation, autonomous driving with natural shifts |

---

## Synthetic Drift Generators

| Name & Authors | Venue | Links | Description |
|---|---|---|---|
| ⭐ **MOA Stream Generators** — Bifet, A., et al. | JMLR 2010 | [Code](https://moa.cms.waikato.ac.nz/) | SEA, STAGGER, Hyperplane, RandomRBF with configurable drift (sudden, gradual, incremental, recurring) |
| ⭐ **River Drift Datasets** — Montiel, J., et al. | JMLR 2021 | [Code](https://github.com/online-ml/river) [Docs](https://riverml.xyz/latest/api/datasets/) | Built-in synthetic streams: Agrawal, LED, RandomRBF, Waveform with drift injection |
| **Concept Drift Benchmark Generator** — Lu, N., et al. | IEEE ICDM 2018 | [Paper](https://doi.org/10.1109/ICDMW.2018.00102) | Configurable generator for all drift types |
| **Scikit-Multiflow Generators** | | [Code](https://github.com/scikit-multiflow/scikit-multiflow) | SEA, STAGGER, LED, Hyperplane generators |

### Common Synthetic Streams

| Stream | Type | Features | Drift Pattern |
|---|---|---|---|
| **SEA** (Street & Kim, 2001) | Binary classification | 3 features (1 irrelevant) | Abrupt concept drift via threshold change |
| **STAGGER** (Schlimmer & Granger, 1986) | Binary classification | 3 categorical features | Cycling through 3 target concepts |
| **Hyperplane** (Hulten et al., 2001) | Binary classification | Configurable dimensions | Gradual drift via rotating hyperplane |
| **RandomRBF** (Bifet, 2010) | Multi-class | Configurable | Gradual drift via moving centroids |
| **Agrawal** (Agrawal et al., 1992) | Binary classification | 9 features (6 relevant) | 10 classification functions |
| **LED** (Breiman, 1984) | Multi-class (10) | 7 binary + 17 noise | Drift via attribute noise changes |
| **Mixed / Interleaved** | Multi-type | Varies | Combines multiple drift types |

---

## Real-World Drift Datasets

### Streaming / Temporal Datasets

| Dataset | Domain | Size | Links | Drift Type |
|---|---|---|---|---|
| ⭐ **Electricity** | Energy pricing | 45,312 instances | [Data](https://www.openml.org/d/151) | Natural temporal drift; price changes |
| ⭐ **Covertype** | Forest cover | 581,012 instances | [Data](https://archive.ics.uci.edu/ml/datasets/covertype) | Spatial/temporal shift across regions |
| **Airlines** | Flight delays | 539,383 instances | [Data](https://www.openml.org/d/1169) | Temporal drift in delay patterns |
| **Weather** | Temperature prediction | 18,159 instances | [Data](https://www.openml.org/d/40669) | Seasonal concept drift |
| **Poker Hand** | Card game | 1,025,010 instances | [Data](https://archive.ics.uci.edu/ml/datasets/Poker+Hand) | Prior probability shift |
| **Spam / Email** | Spam detection | ~9,324 instances | [Data](https://www.openml.org/d/44) | Temporal concept drift as spam evolves |
| **Usenet** | News classification | 5,931 instances | [Data](https://sites.google.com/site/zliobaite/) | Natural drift in news topics |
| **NOAA Weather** | Weather classification | ~18,000 instances | [Data](https://moa.cms.waikato.ac.nz/datasets/) | Long-term environmental drift |
| **KDD Cup 1999** | Intrusion detection | 4,898,431 instances | [Data](https://archive.ics.uci.edu/ml/datasets/kdd+cup+1999+data) | Attack pattern evolution |
| **Gas Sensor** | Chemical sensing | 13,910 instances | [Data](https://archive.ics.uci.edu/ml/datasets/Gas+Sensor+Array+Drift+Dataset) | Sensor degradation drift over 36 months |

### Tabular / Cross-Sectional Datasets

| Dataset | Domain | Size | Links | Shift Type |
|---|---|---|---|---|
| **ACS Income** | Census/Income | ~1.5M/year | [Code](https://github.com/acs-community/acs-datasets) | Geographic and temporal shift |
| **MIMIC-III/IV** | Healthcare | ~60K patients | [Data](https://mimic.mit.edu/) | Temporal clinical practice shifts |
| **eICU** | Healthcare | ~200K stays | [Data](https://eicu-crd.mit.edu/) | Hospital-to-hospital shift |
| **Yelp Reviews** | NLP/Sentiment | 6.9M reviews | [Data](https://www.yelp.com/dataset) | Temporal language/rating drift |
| **Amazon Reviews** | NLP/Sentiment | 233M reviews | [Data](https://nijianmo.github.io/amazon/index.html) | Temporal and domain drift |
| **Stack Overflow** | NLP/Classification | Variable | [Data](https://archive.org/details/stackexchange) | Topic and language drift over years |

---

## Domain-Specific Datasets

### Healthcare

| Dataset | Description | Links | Drift Type |
|---|---|---|---|
| **Camelyon17** | Tumor detection in lymph node tissue | [WILDS](https://wilds.stanford.edu/) | Hospital/scanner shift |
| **CheXpert** | Chest X-ray interpretation | [Data](https://stanfordmlgroup.github.io/competitions/chexpert/) | Temporal + device shift |
| **PhysioNet Challenges** | Clinical time series | [Data](https://physionet.org/) | Patient population shift |

### Finance

| Dataset | Description | Links | Drift Type |
|---|---|---|---|
| **Credit Card Fraud** | Transaction fraud detection | [Kaggle](https://www.kaggle.com/mlg-ulb/creditcardfraud) | Fraud pattern evolution |
| **Lending Club** | Loan default prediction | [Data](https://www.kaggle.com/wordsforthewise/lending-club) | Economic cycle drift |
| **Stock Market** | Price/trend prediction | Various | Regime changes, market shifts |

### Remote Sensing / Geospatial

| Dataset | Description | Links | Drift Type |
|---|---|---|---|
| **FMoW** | Satellite imagery classification | [WILDS](https://wilds.stanford.edu/) | Temporal + geographic shift |
| **PovertyMap** | Poverty estimation from satellite | [WILDS](https://wilds.stanford.edu/) | Geographic distribution shift |
| **iWildCam** | Wildlife camera traps | [WILDS](https://wilds.stanford.edu/) | Location + temporal shift |

---

## Evaluation Metrics & Protocols

### Detection Metrics

| Metric | Description | Usage |
|---|---|---|
| **True Positive Rate (Recall)** | % of actual drifts correctly detected | Higher is better for safety-critical systems |
| **False Positive Rate** | % of false alarms | Lower is better for alert fatigue |
| **Detection Delay** | Time between drift occurrence and detection | Lower is better; measured in samples or time |
| **Mean Time Between False Alarms (MTBFA)** | Average time between false detections | Higher is better |
| **F1-Score (Drift)** | Harmonic mean of precision and recall for drift detection | Balanced evaluation |
| **AUC-ROC (Drift Classifier)** | Area under ROC for drift/no-drift classification | Overall discrimination ability |

### Adaptation Metrics

| Metric | Description | Usage |
|---|---|---|
| **Prequential Accuracy** | Test-then-train accuracy over stream | Standard streaming evaluation |
| **Kappa Statistic** | Accuracy relative to random classifier | Handles imbalanced streams |
| **Recovery Time** | Time to recover performance after drift | Measures adaptation speed |
| **Backward Transfer** | Impact on old concepts after learning new | Measures forgetting |
| **Forward Transfer** | Benefit of past learning on new concepts | Measures generalization |

### Standard Evaluation Protocol

```
┌─────────────────────────────────────────────────────────────────────────────┐
│               EVALUATION PROTOCOLS — VISUAL GUIDE                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. PREQUENTIAL (Interleaved Test-Then-Train)                               │
│                                                                             │
│  Stream: x₁  x₂  x₃  x₄  x₅  x₆  x₇  x₈  x₉ ...                       │
│          │   │   │   │   │   │   │   │   │                                 │
│          ▼   ▼   ▼   ▼   ▼   ▼   ▼   ▼   ▼                               │
│         [T] [T] [T] [T] [T] [T] [T] [T] [T]     T = Test then Train       │
│          ✓   ✓   ✗   ✓   ✗   ✓   ✓   ✓   ✗     ✓ = correct ✗ = wrong    │
│                                                                             │
│  Accuracy (sliding window of 100):                                          │
│  100%─┤●●●●●                                                               │
│       │      ●●●                                                            │
│   90%─┤         ●●                     ●●●●●●●●                            │
│       │           ●●●                ●●                                     │
│   80%─┤              ●●●           ●                                        │
│       │                 ●●●●●    ●                                          │
│   70%─┤                      ●●●● ← Drift here, then recovery              │
│       └──────────────────────────────────────────────►                      │
│                                                                             │
│  2. DRIFT-POINT EVALUATION                                                  │
│                                                                             │
│              Drift      Detection                                           │
│              occurs     point                                               │
│                │          │                                                  │
│                ▼          ▼                                                  │
│   ─────────────●──────────●──────────────────────►                         │
│                │◄────────►│                                                  │
│                 Detection                                                    │
│                  Delay                                                       │
│                                                                             │
│   Accuracy:    ▓▓▓▓▓▓▓▓▓▓░░░░░░░░▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓                        │
│                stable     ▲ drop  ▲ recovery  stable                        │
│                          drift    adaptation                                │
│                                   complete                                  │
│                                                                             │
│  3. KEY METRICS VISUAL                                                      │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────┐              │
│   │              CONFUSION MATRIX FOR DRIFT DETECTION       │              │
│   │                                                         │              │
│   │                      Predicted                          │              │
│   │                  Drift    No Drift                      │              │
│   │  Actual  Drift │  TP    │   FN    │ ← Want TP high     │              │
│   │       No Drift │  FP    │   TN    │ ← Want FP low      │              │
│   │                                                         │              │
│   │  Detection Delay = t_detected - t_actual_drift          │              │
│   │  MTBFA = avg time between false alarms                  │              │
│   └─────────────────────────────────────────────────────────┘              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```
