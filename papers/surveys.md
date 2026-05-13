# Surveys, Tutorials & Books on Data Drift

[← Back to Main Page](README.md)

A comprehensive collection of survey papers, tutorials, and books covering data drift, concept drift, and dataset shift.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SURVEY LANDSCAPE AT A GLANCE                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌───────────────┐   ┌───────────────┐   ┌───────────────┐                 │
│  │  FOUNDATIONAL │   │   DETECTION   │   │ DOMAIN-SPECIFIC│                │
│  │               │   │   FOCUSED     │   │               │                 │
│  │ Gama (2014)   │   │ Rabanser      │   │ CV: Ye (2022) │                 │
│  │ Lu (2019)     │   │  (2019)       │   │ NLP: Biesialska│                │
│  │ Moreno-Torres │   │ Sethi (2017)  │   │ TS: Gao (2024)│                │
│  │  (2012)       │   │ Gemaque (2020)│   │ OOD: Shen     │                │
│  │ Bayram (2022) │   │               │   │  (2021)       │                 │
│  └───────┬───────┘   └───────┬───────┘   └───────┬───────┘                 │
│          │                   │                    │                          │
│          └───────────────────┼────────────────────┘                          │
│                              │                                               │
│  ┌───────────────┐   ┌──────▼────────┐   ┌───────────────┐                 │
│  │   STREAMING   │   │   INDUSTRY    │   │   TUTORIALS   │                 │
│  │               │   │   & APPLIED   │   │               │                 │
│  │ Gomes (2017)  │   │ Sculley(2015) │   │ Webb (KDD'20) │                │
│  │ Nguyen (2015) │   │ Paleyes(2022) │   │ Bifet (ECML)  │                │
│  │ Lu (2023)     │   │ Kreuzberger   │   │ Lipton (ICML) │                │
│  │               │   │  (2023)       │   │               │                 │
│  └───────────────┘   └───────────────┘   └───────────────┘                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

```
    SURVEY PAPERS — CITATION IMPACT (approximate)
    ═══════════════════════════════════════════════

    Gama et al. (2014)        ████████████████████████████████████████  3000+
    Sculley et al. (2015)     ██████████████████████████████████        2500+
    Lu et al. (2019)          ████████████████████████████              2000+
    Moreno-Torres (2012)      ██████████████████████                    1500+
    Gomes et al. (2017)       █████████████████                        1100+
    Rabanser et al. (2019)    ████████████                              800+
    Shen et al. (2021)        ███████████                               700+
    Bayram et al. (2022)      ██████                                    400+
```

---

## Foundational Books

| Title & Authors | Year | Links | Description |
|---|---|---|---|
| ⭐ **Dataset Shift in Machine Learning** — Quiñonero-Candela, J., Sugiyama, M., Schwaighofer, A., Lawrence, N. | 2009 | [Book](https://mitpress.mit.edu/books/dataset-shift-machine-learning) | The foundational text on dataset shift; defines covariate shift, prior probability shift, and sample selection bias |
| **Knowledge Management in the Age of Artificial Intelligence** (Ch. on Concept Drift) — Webb, G.I. | 2023 | [Book](https://doi.org/10.1007/978-3-031-35891-3) | Modern perspective on drift in knowledge systems |

---

## Survey Papers

### Comprehensive Surveys

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| ⭐ **A Survey on Concept Drift Adaptation** — Gama, J., Žliobaitė, I., Bifet, A., Pechenizkiy, M., Bouchachia, A. | ACM Computing Surveys 2014 | [Paper](https://doi.org/10.1145/2523813) | Definitive survey on concept drift; 3000+ citations; covers detection, understanding, and adaptation |
| ⭐ **Learning under Concept Drift: A Review** — Lu, J., Liu, A., Dong, F., Gu, F., Gama, J., Zhang, G. | IEEE TKDE 2019 | [Paper](https://doi.org/10.1109/TKDE.2018.2876857) | Comprehensive review covering drift detection, understanding, and adaptation with taxonomy |
| **A Comprehensive Survey on Concept Drift** — Bayram, F., Ahmed, B.S., Kassler, A. | ACM Computing Surveys 2022 | [Paper](https://doi.org/10.1145/3524491) | Modern survey covering 2014-2022 advances in concept drift research |
| ⭐ **A Unifying View on Dataset Shift in Classification** — Moreno-Torres, J.G., Raeder, T., Alaiz-Rodríguez, R., Chawla, N.V., Herrera, F. | Pattern Recognition 2012 | [Paper](https://doi.org/10.1016/j.patcog.2011.06.019) | Unifies covariate shift, prior probability shift, and concept shift frameworks |
| **Concept Drift Adaptation by Exploiting Drift Type** — Webb, G.I., Lee, L.K., Petitjean, F., Goethals, B. | ACM Computing Surveys 2023 | [Paper](https://doi.org/10.1145/3588782) | Survey on drift-type-aware adaptation strategies |
| **Data Distribution Shifts and Monitoring** — Garg, S., Balakrishnan, S., Lipton, Z.C., Neyshabur, B., Sedghi, H. | NeurIPS 2022 | [Paper](https://arxiv.org/abs/2207.09888) | Survey on distribution shift detection in modern ML |

### Detection-Focused Surveys

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| ⭐ **Failing Loudly: An Empirical Study of Methods for Detecting Dataset Shift** — Rabanser, S., Günnemann, S., Lipton, Z.C. | NeurIPS 2019 | [Paper](https://arxiv.org/abs/1810.11953) [Code](https://github.com/steverab/failing-loudly) | Empirical comparison of shift detection methods; introduces dimensionality reduction + testing pipeline |
| **A Survey on Data-Driven Software Monitoring** — Ackermann, S., Jungiewicz, M., Felderer, M., Pahl, C. | ACM Computing Surveys 2024 | [Paper](https://doi.org/10.1145/3643564) | Survey on monitoring data-driven systems |
| **Concept Drift Detection: Dealing with Missing Ground Truth** — Sethi, T.S., Kantardzic, M. | IEEE Trans. Neural Networks 2017 | [Paper](https://doi.org/10.1109/TNNLS.2017.2682773) | Survey on drift detection without labels |
| **A Survey of Methods for Detecting and Handling Concept Drift** — Gemaque, R.N., Costa, A.F.J., Giusti, R., Santos, E.M.D. | Journal of the Brazilian Computer Society 2020 | [Paper](https://doi.org/10.1186/s13173-020-00095-y) | Overview of detection and handling methods |

### Domain-Specific Surveys

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| **A Survey on Monitoring of Machine Learning Models in Production** — Klaise, J., Van Looveren, A., Vacanti, G., Zmijewski, O. | Journal of ML Research 2021 | [Paper](https://arxiv.org/abs/2005.12068) | Practical survey on monitoring ML in production environments |
| **Distribution Shift in Computer Vision: A Survey** — Ye, N., Li, K., Bai, H., Yu, R., Hong, L., et al. | CVPR Workshop 2022 | [Paper](https://arxiv.org/abs/2205.12710) | Survey on distribution shift specifically in computer vision |
| **Continual Learning in Natural Language Processing: A Survey** — Biesialska, M., Biesialska, K., Costa-jussà, M.R. | COLING 2020 | [Paper](https://aclanthology.org/2020.coling-main.574/) | Survey on handling drift in NLP models |
| **Out-of-Distribution Generalization: A Survey** — Shen, Z., Liu, J., He, Y., Zhang, X., Xu, R., et al. | arXiv 2021 | [Paper](https://arxiv.org/abs/2108.13624) | Comprehensive survey on OOD generalization connecting to drift |
| **A Survey on Distribution Shift in Time Series** — Gao, J., Wen, Q., Zhang, C., Liang, S., Sun, L., et al. | arXiv 2024 | [Paper](https://arxiv.org/abs/2401.16603) | Survey on distribution shift in temporal data |
| **Model Evaluation, Model Selection, and Algorithm Selection in ML** — Raschka, S. | arXiv 2020 | [Paper](https://arxiv.org/abs/1811.12808) | Covers evaluation under distribution shift |
| **Towards Explaining Distribution Shifts** — Kulinski, S., Inouye, D. | ICML 2023 | [Paper](https://arxiv.org/abs/2210.10275) [Code](https://github.com/inouye-lab/explaining-distribution-shifts) | Survey-level paper on explainable distribution shift |
| **Maintaining Fairness Across Distribution Shift** — Schrouff, J., et al. | FAccT 2022 | [Paper](https://doi.org/10.1145/3531146.3533157) | Drift from a fairness perspective |

### Streaming & Online Learning Surveys

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| ⭐ **A Survey on Ensemble Learning for Data Stream Classification** — Gomes, H.M., Barddal, J.P., Enembreck, F., Bifet, A. | ACM Computing Surveys 2017 | [Paper](https://doi.org/10.1145/3054925) | Ensembles for drift-aware stream classification |
| **Data Stream Mining: A Review** — Nguyen, H.L., Woon, Y.K., Ng, W.K. | Data Mining and Knowledge Discovery 2015 | [Paper](https://doi.org/10.1007/s10618-014-0382-x) | Covers stream mining with drift |
| **Challenges in Benchmark and Evaluation of Concept Drift** — Lu, N., Lu, J., Zhang, G., de Mantaras, R.L. | IEEE ICDM Workshop 2023 | [Paper](https://doi.org/10.1109/ICDMW.2018.00102) | Challenges in evaluating drift methods |

### Industry & Applied Surveys

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| ⭐ **Hidden Technical Debt in Machine Learning Systems** — Sculley, D., Holt, G., Golovin, D., et al. | NeurIPS 2015 | [Paper](https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems) | Seminal paper on ML system debt; data dependency and feedback loops |
| **Challenges in Deploying Machine Learning: A Survey of Case Studies** — Paleyes, A., Urma, R., Lawrence, N. | ACM Computing Surveys 2022 | [Paper](https://doi.org/10.1145/3533378) | Real-world challenges including drift in production |
| **Machine Learning Operations (MLOps): Overview, Definition, and Architecture** — Kreuzberger, D., Kühl, N., Hirschl, S. | IEEE Access 2023 | [Paper](https://doi.org/10.1109/ACCESS.2023.3262138) | Architectural patterns for handling drift in MLOps |
| **Data Management Challenges in Production Machine Learning** — Polyzotis, N., Roy, S., Whang, S.E., Zinkevich, M. | SIGMOD 2017 | [Paper](https://doi.org/10.1145/3035918.3054782) | Data management perspective on drift |

---

## Tutorials & Workshops

| Title | Venue | Links | Description |
|---|---|---|---|
| **Concept Drift and How to Identify It** — Webb, G.I. | KDD Tutorial 2020 | [Slides](https://kdd.org/kdd2020/tutorials/) | Hands-on tutorial on drift identification |
| **Learning in Non-Stationary Environments** — Bifet, A. | ECML-PKDD Tutorial 2019 | [Materials](https://www.ecmlpkdd2019.org/tutorials/) | Tutorial on streaming with drift |
| **Practical Distribution Shift** — Lipton, Z.C. | ICML Workshop 2022 | [Workshop](https://sites.google.com/view/icml-2022-pods/) | Workshop on practical distribution shift |
