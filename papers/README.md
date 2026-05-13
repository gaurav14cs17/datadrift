# Awesome-Data-Drift [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

<p align="center">
  <img src="https://img.shields.io/badge/Papers-200+-blue" alt="Papers"/>
  <img src="https://img.shields.io/badge/Topic-Data%20Drift-orange" alt="Data Drift"/>
  <img src="https://img.shields.io/badge/Maintained-Yes-green" alt="Maintained"/>
  <img src="https://img.shields.io/github/last-commit/ggoswami/DataDrift" alt="Last Commit"/>
  <img src="https://img.shields.io/badge/PRs-Welcome-brightgreen" alt="PRs Welcome"/>
</p>

A curated list of **research papers, tools, and resources** on **Data Drift, Concept Drift, and Distribution Shift** in Machine Learning systems — inspired by [Awesome-Efficient-LLM](https://github.com/horseee/Awesome-Efficient-LLM).

---

## What is Data Drift?

Data drift occurs when the statistical properties of the data that a production ML model receives change over time, causing model performance to degrade. It is one of the most critical challenges in deploying and maintaining ML systems.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        THE DATA DRIFT PROBLEM                               │
│                                                                             │
│   TRAINING PHASE                              PRODUCTION PHASE              │
│   ┌───────────────┐    ┌─────────────┐    ┌───────────────┐                │
│   │               │    │             │    │               │                │
│   │  P_train(X,Y) │───►│    MODEL    │◄───│  P_prod(X,Y)  │                │
│   │               │    │             │    │               │                │
│   │   ▄▄████▄▄   │    │  Trained    │    │     ▄▄██▄▄   │                │
│   │  ██████████  │    │  on past    │    │   ████████▄▄ │                │
│   │  ██████████  │    │  data       │    │  ████████████ │                │
│   └───────────────┘    └──────┬──────┘    └───────────────┘                │
│                               │                                             │
│                               ▼                                             │
│                    P_train ≠ P_prod                                          │
│                    ───────────────                                           │
│                    Model degrades                                            │
│                    silently!                                                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Taxonomy of Data Drift

```
                              ┌─────────────────────┐
                              │    DATASET SHIFT     │
                              │   P(X,Y) changes     │
                              └──────────┬──────────┘
                    ┌────────────────────┼────────────────────┐
                    │                    │                    │
                    ▼                    ▼                    ▼
         ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
         │  COVARIATE SHIFT │ │   LABEL SHIFT    │ │  CONCEPT DRIFT   │
         │  P(X) changes    │ │  P(Y) changes    │ │  P(Y|X) changes  │
         │  P(Y|X) same     │ │  P(X|Y) same     │ │  Most dangerous  │
         └────────┬─────────┘ └────────┬─────────┘ └────────┬─────────┘
                  │                    │                    │
                  ▼                    ▼                    ▼
           Age, income          Fraud rate            Customer
           distributions        increases             behavior
           shift                                      evolves

    ┌─────────────────────────────────────────────────────────────────────┐
    │                    CONCEPT DRIFT PATTERNS                           │
    │                                                                     │
    │  SUDDEN          GRADUAL         INCREMENTAL      RECURRING        │
    │  ▓▓▓▓            ▓▓▓▓░░          ▓▓▓▓▒            ▓▓▓▓             │
    │  ▓▓▓▓            ▓▓▓▓░░░░        ▓▓▓▓▒▒           ░░░░             │
    │  ────░░░░        ▓▓░░░░░░░░      ▓▓▓▒▒▒▒          ▓▓▓▓             │
    │      ░░░░        ──░░░░░░░░      ──▒▒▒▒▒▒         ░░░░             │
    │      ░░░░          ░░░░░░░░        ▒▒▒▒▒▒         ▓▓▓▓             │
    │  t ────────►    t ────────►    t ────────►     t ────────►         │
    └─────────────────────────────────────────────────────────────────────┘
```

---

## Research Landscape Mind Map

```
                                 ┌──────────────┐
                        ┌────────│  DATA DRIFT  │────────┐
                        │        └──────┬───────┘        │
                        │               │                │
               ┌────────▼───────┐       │       ┌───────▼────────┐
               │   DETECTION    │       │       │   MITIGATION   │
               │                │       │       │                │
               │ • KS Test      │       │       │ • Retraining   │
               │ • MMD          │       │       │ • Online Learn │
               │ • PSI          │       │       │ • Ensembles    │
               │ • ADWIN / DDM  │       │       │ • Domain Adapt │
               │ • Chi-Square   │       │       │ • Test-Time    │
               └────────────────┘       │       └────────────────┘
                                        │
               ┌────────────────┐       │       ┌────────────────┐
               │   MONITORING   │       │       │  DEEP LEARNING │
               │                │◄──────┴──────►│                │
               │ • MLOps        │               │ • NLP Drift    │
               │ • Pipelines    │               │ • Vision Shift │
               │ • Dashboards   │               │ • LLM Drift    │
               │ • Alerting     │               │ • RL Shift     │
               └────────────────┘               └────────────────┘
                        │                                │
                        │       ┌────────────────┐       │
                        └──────►│ TOOLS & BENCH  │◄──────┘
                                │                │
                                │ • Evidently    │
                                │ • Alibi Detect │
                                │ • NannyML      │
                                │ • WILDS        │
                                └────────────────┘
```

---

## Full List

| Category | Description | Paper Count |
|---|---|---|
| [Survey & Benchmark](surveys.md) | Comprehensive surveys, tutorials, and benchmarks | 25+ |
| [Drift Detection Methods](detection_methods.md) | Statistical tests, online detectors, multivariate methods | 45+ |
| [Concept Drift](concept_drift.md) | P(Y\|X) changes — evolving relationships | 40+ |
| [Covariate Shift](covariate_shift.md) | P(X) changes — input distribution shift | 25+ |
| [Monitoring & MLOps](monitoring_mlops.md) | Production monitoring, pipelines, and ML operations | 20+ |
| [Mitigation & Adaptation](mitigation_adaptation.md) | Retraining, online learning, domain adaptation | 30+ |
| [Drift in Deep Learning](drift_in_deep_learning.md) | DNN-specific drift: NLP, CV, LLMs, Foundation Models | 25+ |
| [Tools & Frameworks](tools_frameworks.md) | Open-source libraries and cloud platforms | 20+ |
| [Benchmarks & Datasets](benchmarks_datasets.md) | Standard datasets and evaluation benchmarks | 15+ |

### Please check out all the papers by selecting the sub-area you're interested in. On this main page, only key recommended papers are shown.

---

## Historical Timeline of Key Milestones

```
1954        1996       2004       2007       2009          2012        2014         2017         2019         2021         2023+
 │           │          │          │          │             │           │            │            │            │            │
 ▼           ▼          ▼          ▼          ▼             ▼           ▼            ▼            ▼            ▼            ▼
Page-      FLORA      DDM       ADWIN    Dataset Shift   MMD Test    Gama's      TF Data      NeurIPS      WILDS       Explaining
Hinkley    Framework  (Gama)    (Bifet)   Book (MIT)     (Gretton)  Survey      Validation    Failing     Benchmark    Distribution
Test                                                                  (3000+      (Google)     Loudly                   Shifts
                                                                     citations)
 │           │          │          │          │             │           │            │            │            │            │
 ├───────────┴──────────┴──────────┴──────────┴─────────────┴───────────┴────────────┴────────────┴────────────┴────────────┤
 │                                                                                                                         │
 │  FOUNDATIONS ──────► STREAMING ERA ──────► THEORY ──────► PRODUCTION ERA ──────► DEEP LEARNING ERA                      │
 │                                                                                                                         │
 └─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Updates

- **May 2026**: Initial release with 200+ papers across 9 categories
- Papers are organized chronologically (newest first) within each category
- Each entry includes: title, authors, venue, links to paper/code/project

---

## Contributing

If you'd like to include your paper, or need to update any details such as conference information or code URLs, please feel free to submit a pull request. We warmly appreciate your contributions to this list. Alternatively, you can email with the links to your paper and code.

**Format for adding a paper:**

```markdown
| **Paper Title** | Authors | Venue Year | [Paper](url) [Code](url) | Brief description |
```

---

## Recommended Papers (Highly Cited / Foundational)

### Surveys

| Title & Authors | Venue | Links |
|---|---|---|
| ⭐ **A Survey on Concept Drift Adaptation** — Gama, J., Žliobaitė, I., Bifet, A., Pechenizkiy, M., Bouchachia, A. | ACM Computing Surveys 2014 | [Paper](https://doi.org/10.1145/2523813) |
| ⭐ **Learning under Concept Drift: A Review** — Lu, J., Liu, A., Dong, F., Gu, F., Gama, J., Zhang, G. | IEEE TKDE 2019 | [Paper](https://doi.org/10.1109/TKDE.2018.2876857) |
| ⭐ **Dataset Shift in Machine Learning** — Quiñonero-Candela, J., Sugiyama, M., Schwaighofer, A., Lawrence, N. | MIT Press 2009 | [Paper](https://mitpress.mit.edu/books/dataset-shift-machine-learning) |
| ⭐ **Failing Loudly: An Empirical Study of Methods for Detecting Dataset Shift** — Rabanser, S., Günnemann, S., Lipton, Z.C. | NeurIPS 2019 | [Paper](https://arxiv.org/abs/1810.11953) [Code](https://github.com/steverab/failing-loudly) |
| ⭐ **A Unifying View on Dataset Shift** — Moreno-Torres, J.G., Raeder, T., Alaiz-Rodríguez, R., Chawla, N.V., Herrera, F. | Pattern Recognition 2012 | [Paper](https://doi.org/10.1016/j.patcog.2011.06.019) |

### Detection Methods

| Title & Authors | Venue | Links |
|---|---|---|
| ⭐ **Learning from Time-Changing Data with Adaptive Windowing (ADWIN)** — Bifet, A., Gavaldà, R. | SDM 2007 | [Paper](https://doi.org/10.1137/1.9781611972771.42) |
| ⭐ **Learning with Drift Detection (DDM)** — Gama, J., Medas, P., Castillo, G., Rodrigues, P. | SBIA 2004 | [Paper](https://doi.org/10.1007/978-3-540-28645-5_29) |
| ⭐ **A Kernel Two-Sample Test** — Gretton, A., Borgwardt, K., Rasch, M., Schölkopf, B., Smola, A. | JMLR 2012 | [Paper](https://jmlr.org/papers/v13/gretton12a.html) [Code](https://github.com/skhobahi/mmd-test) |
| ⭐ **Detecting and Correcting for Label Shift with Black Box Predictors** — Lipton, Z.C., Wang, Y., Smola, A. | ICML 2018 | [Paper](https://arxiv.org/abs/1802.03916) [Code](https://github.com/kundajelab/labelshift) |

### Covariate Shift & Domain Adaptation

| Title & Authors | Venue | Links |
|---|---|---|
| ⭐ **Covariate Shift Adaptation by Importance Weighted Cross Validation** — Sugiyama, M., Krauledat, M., Müller, K. | JMLR 2007 | [Paper](https://jmlr.org/papers/v8/sugiyama07a.html) |
| ⭐ **Domain Adaptation under Target and Conditional Shift** — Zhang, K., Schölkopf, B., Muandet, K., Wang, Z. | ICML 2013 | [Paper](https://proceedings.mlr.press/v28/zhang13d.html) |

### MLOps & Production Systems

| Title & Authors | Venue | Links |
|---|---|---|
| ⭐ **Hidden Technical Debt in Machine Learning Systems** — Sculley, D., Holt, G., Golovin, D., et al. | NeurIPS 2015 | [Paper](https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems) |
| ⭐ **Monitoring Machine Learning Models in Production** — Breck, E., Cai, S., Nielsen, E., Salib, M., Sculley, D. | NeurIPS Workshop 2017 | [Paper](https://research.google/pubs/pub46555/) |

---

## Quick Navigation

```
papers/
├── README.md                    ← You are here (index + recommended papers)
├── surveys.md                   ← Survey papers, tutorials, books
├── detection_methods.md         ← Statistical tests, online detectors
├── concept_drift.md             ← Concept drift (P(Y|X) changes)
├── covariate_shift.md           ← Covariate shift (P(X) changes)
├── monitoring_mlops.md          ← Production monitoring & MLOps
├── mitigation_adaptation.md     ← Retraining, adaptation, online learning
├── drift_in_deep_learning.md    ← DNN, NLP, CV, LLM specific drift
├── tools_frameworks.md          ← Open-source tools & cloud platforms
└── benchmarks_datasets.md       ← Standard benchmarks & datasets
```

---

## Star History

If you find this resource useful, please star the repository!

---

## Citation

```bibtex
@misc{awesome-data-drift-2026,
  title={Awesome-Data-Drift: A Curated List of Data Drift Research},
  author={Gaurav Goswami},
  year={2026},
  howpublished={\url{https://github.com/ggoswami/DataDrift}}
}
```

---

## License

This project is licensed under the MIT License.
