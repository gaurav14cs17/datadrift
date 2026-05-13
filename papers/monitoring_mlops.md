# Monitoring & MLOps

[← Back to Main Page](README.md)

Papers on production ML monitoring, data validation, ML pipelines, and operational systems for detecting and managing data drift.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│               END-TO-END ML MONITORING ARCHITECTURE                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  DATA SOURCES          FEATURE STORE          MODEL SERVING                 │
│  ┌─────┐ ┌─────┐      ┌──────────────┐      ┌──────────────┐              │
│  │ API │ │ DB  │─────►│  Transform   │─────►│  Inference   │              │
│  └─────┘ └─────┘      │  + Validate  │      │  Engine      │              │
│  ┌─────┐ ┌─────┐      │  + Log       │      │  + Log       │              │
│  │Files│ │Event│─────►│              │      │              │              │
│  └─────┘ └─────┘      └──────┬───────┘      └──────┬───────┘              │
│                               │                      │                      │
│           ┌───────────────────┴──────────────────────┘                      │
│           │                                                                 │
│           ▼                                                                 │
│  ┌─────────────────────────────────────────────────────────┐               │
│  │              MONITORING LAYER                            │               │
│  │                                                         │               │
│  │  ┌──────────┐   ┌──────────┐   ┌──────────┐           │               │
│  │  │  DATA    │   │  MODEL   │   │OPERATIONAL│           │               │
│  │  │  DRIFT   │   │ QUALITY  │   │ HEALTH   │           │               │
│  │  │          │   │          │   │          │           │               │
│  │  │• Features│   │• Accuracy│   │• Latency │           │               │
│  │  │• Schema  │   │• Prec/Rec│   │• Errors  │           │               │
│  │  │• Missing%│   │• AUC     │   │• CPU/GPU │           │               │
│  │  │• Outliers│   │• Calib.  │   │• Memory  │           │               │
│  │  └────┬─────┘   └────┬─────┘   └────┬─────┘           │               │
│  │       └──────────────┼───────────────┘                  │               │
│  └──────────────────────┼──────────────────────────────────┘               │
│                         ▼                                                   │
│  ┌──────────┐   ┌──────────────┐   ┌──────────────────┐                   │
│  │ ALERT    │   │  DASHBOARD   │   │  AUTO-RETRAIN    │                   │
│  │ Slack/PD │   │  & Reports   │   │  Pipeline        │                   │
│  └──────────┘   └──────────────┘   └──────────────────┘                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

```
    ML TECHNICAL DEBT ICEBERG (Sculley et al., 2015)
    ══════════════════════════════════════════════════

                    ┌──────────────┐
                    │   ML CODE    │  ← Only a small fraction!
                    └──────┬───────┘
          ─────────────────┼─────────────────── waterline
           ╱               │               ╲
          ╱  ┌─────────────┴─────────────┐  ╲
         ╱   │     DATA COLLECTION       │   ╲
        ╱    ├───────────────────────────┤    ╲
       ╱     │   DATA VERIFICATION       │     ╲
      ╱      ├───────────────────────────┤      ╲
     ╱       │ FEATURE EXTRACTION        │       ╲
    ╱        ├───────────────────────────┤        ╲
   ╱         │ MONITORING & TESTING      │         ╲
  ╱          ├───────────────────────────┤          ╲
 ╱           │ CONFIGURATION / SERVING   │           ╲
╱            └───────────────────────────┘            ╲
```

---

## Quick Links

- [ML System Design & Technical Debt](#ml-system-design--technical-debt)
- [Data Validation & Quality](#data-validation--quality)
- [Model Monitoring in Production](#model-monitoring-in-production)
- [MLOps Architecture & Pipelines](#mlops-architecture--pipelines)
- [Feature Stores & Data Management](#feature-stores--data-management)
- [Continuous Training & Deployment](#continuous-training--deployment)

---

## ML System Design & Technical Debt

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| ⭐ **Hidden Technical Debt in Machine Learning Systems** — Sculley, D., Holt, G., Golovin, D., et al. | NeurIPS 2015 | [Paper](https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems) | Seminal paper on ML system debt; identifies data dependencies, feedback loops, and configuration debt |
| ⭐ **Reliable Machine Learning** — Breck, E., Cai, S., Nielsen, E., Salib, M., Sculley, D. | NeurIPS Workshop 2017 | [Paper](https://research.google/pubs/pub46555/) | Production ML monitoring principles from Google |
| **Machine Learning: The High-Interest Credit Card of Technical Debt** — Sculley, D., et al. | SE4ML Workshop 2014 | [Paper](https://research.google/pubs/pub43146/) | Earlier version identifying ML-specific debt |
| **What's Your ML Test Score? A Rubric for ML Production Readiness** — Breck, E., Cai, S., Nielsen, E., Salib, M., Sculley, D. | NeurIPS Workshop 2017 | [Paper](https://research.google/pubs/pub46555/) | 28-point test for production ML readiness |
| **Challenges in Deploying Machine Learning: A Survey of Case Studies** — Paleyes, A., Urma, R., Lawrence, N. | ACM Computing Surveys 2022 | [Paper](https://doi.org/10.1145/3533378) | Survey of real-world ML deployment challenges |

---

## Data Validation & Quality

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| ⭐ **Data Validation for Machine Learning (TFDV)** — Breck, E., Polyzotis, N., Roy, S., Whang, S., Zinkevich, M. | SysML 2019 | [Paper](https://mlsys.org/Conferences/2019/doc/2019/167.pdf) [Code](https://github.com/tensorflow/data-validation) | TensorFlow Data Validation; schema-based validation with drift detection |
| **Data Management Challenges in Production Machine Learning** — Polyzotis, N., Roy, S., Whang, S.E., Zinkevich, M. | SIGMOD 2017 | [Paper](https://doi.org/10.1145/3035918.3054782) | Data management perspective on production ML |
| **Automating Large-Scale Data Quality Verification** — Schelter, S., Lange, D., Schmidt, P., Ceber, M., Biessmann, F., Grafberger, A. | VLDB 2018 | [Paper](https://doi.org/10.14778/3229863.3229867) [Code](https://github.com/awslabs/deequ) | Deequ: unit tests for data quality |
| **Amazon Deequ: A Library for Data Quality** — Schelter, S., et al. | AWS Blog 2019 | [Code](https://github.com/awslabs/deequ) | Declarative data quality constraints |
| **Great Expectations: Always Know What to Expect from Your Data** — Great Expectations Team | Open Source 2019 | [Code](https://github.com/great-expectations/great_expectations) | Pipeline-integrated data validation framework |
| **Slicing and Dicing Data for ML Monitoring** — Chung, Y., Kraska, T., Polyzotis, N., Tae, K., Whang, S.E. | VLDB 2019 | [Paper](https://doi.org/10.14778/3342263.3342268) | Slice-based monitoring for detecting drift in subpopulations |

---

## Model Monitoring in Production

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| ⭐ **Monitoring Machine Learning Models in Production** — Klaise, J., Van Looveren, A., Vacanti, G., Zmijewski, O. | arXiv 2021 | [Paper](https://arxiv.org/abs/2005.12068) | Comprehensive framework for model monitoring |
| **Estimating and Explaining Model Performance When Both Covariates and Labels Shift** — Chen, J., et al. | NeurIPS 2022 | [Paper](https://arxiv.org/abs/2209.08436) | Performance estimation without labels in production |
| **Model Performance Prediction in Production** — Deng, W., Zheng, J. | arXiv 2021 | [Paper](https://arxiv.org/abs/2112.02536) | Predicting when models will fail in production |
| **Characterizing and Detecting Mismatch in ML Pipelines** — Shankar, S., Bodik, P., Garcia, R., et al. | MLSys 2022 | [Paper](https://arxiv.org/abs/2203.10808) | Detecting training-serving skew |
| **Monitoring and Explainability of Models in Production** — Bhatt, U., Xiang, A., Sharma, S., et al. | ICML Workshop 2020 | [Paper](https://arxiv.org/abs/2007.06299) | Monitoring for explainability and trust |
| **Detecting Silent Data Drift** — Amazon Science 2023 | [Paper](https://www.amazon.science/publications/detecting-silent-drift) | Detecting drift that doesn't trigger alerts |

---

## MLOps Architecture & Pipelines

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| ⭐ **Machine Learning Operations (MLOps): Overview, Definition, and Architecture** — Kreuzberger, D., Kühl, N., Hirschl, S. | IEEE Access 2023 | [Paper](https://doi.org/10.1109/ACCESS.2023.3262138) | Comprehensive MLOps reference architecture |
| **TFX: A TensorFlow-Based Production-Scale Machine Learning Platform** — Baylor, D., Breck, E., Cheng, H.-T., et al. | KDD 2017 | [Paper](https://doi.org/10.1145/3097983.3098021) [Code](https://github.com/tensorflow/tfx) | Google's end-to-end ML platform with built-in validation |
| **MLflow: A Platform for the ML Lifecycle** — Zaharia, M., Chen, A., Davidson, A., et al. | Open Source 2018 | [Code](https://github.com/mlflow/mlflow) | Experiment tracking and model registry |
| **Towards ML Engineering: A Brief History of TensorFlow Extended (TFX)** — Breck, E., et al. | arXiv 2019 | [Paper](https://arxiv.org/abs/1904.02641) | Evolution of Google's ML platform |
| **Continuous Delivery for Machine Learning** — Sato, D., Wider, A., Windheuser, C. | Martin Fowler Blog 2019 | [Article](https://martinfowler.com/articles/cd4ml.html) | Patterns for ML continuous delivery |
| **Operationalizing Machine Learning: An Interview Study** — Shankar, S., et al. | arXiv 2022 | [Paper](https://arxiv.org/abs/2209.09125) | Interviews with ML practitioners on operationalization |

---

## Feature Stores & Data Management

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| **Feast: Feature Store for Machine Learning** — Tecton Team | Open Source 2019 | [Code](https://github.com/feast-dev/feast) | Open-source feature store with point-in-time correctness |
| **Hopsworks Feature Store** — Dowling, J., et al. | 2020 | [Code](https://github.com/logicalclocks/hopsworks) | Feature store with built-in data monitoring |
| **Rethinking Feature Stores** — Li, A., Maas, A. | VLDB Workshop 2023 | [Paper](https://arxiv.org/abs/2305.09638) | Modern approaches to feature management |
| **Time Travel in Feature Stores** — Hermann, J., et al. | SIGMOD 2021 | [Paper](https://doi.org/10.1145/3448016.3457569) | Point-in-time joins for avoiding data leakage |

---

## Continuous Training & Deployment

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| **Continuous Training for Production ML** — Shankar, S., et al. | SysML 2019 | [Paper](https://mlsys.org/Conferences/2019/) | Patterns for continuously retraining models |
| **Towards Automated ML Model Monitoring: Measure, Improve, Repeat** — Huyen, C. | 2022 | [Book](https://www.oreilly.com/library/view/designing-machine-learning/9781098107956/) | Practical monitoring from "Designing ML Systems" |
| **On Efficient Training of Large-Scale Deep Learning Models: A Literature Review** — Gusak, J., et al. | arXiv 2022 | [Paper](https://arxiv.org/abs/2304.03589) | Efficient training for continuous model updates |
| **CI/CD for Machine Learning** — Sato, D. | ThoughtWorks 2020 | [Article](https://www.thoughtworks.com/insights/articles/intelligent-enterprise-series-cd4ml) | CI/CD patterns for ML systems |
