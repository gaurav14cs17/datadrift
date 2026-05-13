# Concept Drift

[← Back to Main Page](README.md)

Papers on concept drift — when the relationship P(Y|X) between input features and the target variable changes over time.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        CONCEPT DRIFT EXPLAINED                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  The SAME input X now maps to a DIFFERENT output Y                          │
│                                                                             │
│  BEFORE DRIFT:                    AFTER DRIFT:                              │
│  ┌──────────────────┐             ┌──────────────────┐                      │
│  │ Income > 50K  ──►│ Low Risk    │ Income > 50K  ──►│ HIGH Risk           │
│  │ Age < 30     ──►│ Low Risk    │ Age < 30     ──►│ MEDIUM Risk          │
│  │ Location=NYC ──►│ Medium      │ Location=NYC ──►│ Low Risk             │
│  └──────────────────┘             └──────────────────┘                      │
│                                                                             │
│  P_before(Y|X) ≠ P_after(Y|X)    ← The decision boundary MOVED            │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────┐      │
│  │  VISUAL: Decision Boundary Shift                                  │      │
│  │                                                                   │      │
│  │  Before:          After:           Gradual:                       │      │
│  │  ● ● ●│○ ○ ○     ● ● ○│○ ○ ○     ● ● ●╲○ ○ ○                   │      │
│  │  ● ● ●│○ ○ ○     ● ○ ○│○ ○ ○     ● ● ○ ╲○ ○ ○                  │      │
│  │  ● ● ●│○ ○ ○     ● ● ○│○ ○ ○     ● ● ● ○╲○ ○                   │      │
│  │       boundary      moved           rotating                      │      │
│  └───────────────────────────────────────────────────────────────────┘      │
│                                                                             │
│  FOUR TYPES OF CONCEPT DRIFT:                                               │
│                                                                             │
│   SUDDEN            GRADUAL          INCREMENTAL       RECURRING            │
│   ████              ████▒▒▒          ████▒             ████                 │
│   ████              ████▒▒▒▒▒        ████▒▒            ▒▒▒▒                 │
│   ────░░░░          ████▒▒▒▒▒▒▒      ████▒▒▒           ████                 │
│       ░░░░          ────▒▒▒▒▒▒▒      ────▒▒▒▒          ▒▒▒▒                 │
│       ░░░░              ▒▒▒▒▒▒▒          ▒▒▒▒▒         ████                 │
│                                                                             │
│   One abrupt       Old concept     Multiple         Switching               │
│   change point     fades into      intermediate     between known           │
│                    new one         concepts         concepts                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Quick Links

- [Foundational Work](#foundational-work)
- [Sudden Concept Drift](#sudden-concept-drift)
- [Gradual Concept Drift](#gradual-concept-drift)
- [Recurring Concept Drift](#recurring-concept-drift)
- [Ensemble Methods for Concept Drift](#ensemble-methods-for-concept-drift)
- [Decision Trees & Rules under Drift](#decision-trees--rules-under-drift)
- [Neural Network Approaches](#neural-network-approaches)
- [Theoretical Foundations](#theoretical-foundations)

---

## Foundational Work

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| ⭐ **Learning with Drift Detection (DDM)** — Gama, J., Medas, P., Castillo, G., Rodrigues, P. | SBIA 2004 | [Paper](https://doi.org/10.1007/978-3-540-28645-5_29) | Foundational DDM algorithm monitoring classification error rate |
| ⭐ **A Survey on Concept Drift Adaptation** — Gama, J., Žliobaitė, I., Bifet, A., Pechenizkiy, M., Bouchachia, A. | ACM Computing Surveys 2014 | [Paper](https://doi.org/10.1145/2523813) | Definitive survey establishing concept drift taxonomy |
| ⭐ **On the Problem of the Most Efficient Tests of Statistical Hypotheses** — Neyman, J., Pearson, E. | Philosophical Transactions 1933 | [Paper](https://doi.org/10.1098/rsta.1933.0009) | Foundation of hypothesis testing used in drift detection |
| **Tracking Recurring Concepts with Meta-Learners** — Gama, J., Kosina, P. | ECML-PKDD 2014 | [Paper](https://doi.org/10.1007/978-3-662-44845-8_27) | Meta-learning for recurring drift patterns |
| **FLORA: Framework for Learning in Dynamic Environments** — Widmer, G., Kubat, M. | Machine Learning 1996 | [Paper](https://doi.org/10.1007/BF00116900) | Early framework for learning under concept drift |

---

## Sudden Concept Drift

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| **Fast Change Detection Using Exponential Weighted Moving Average** — Ross, G.J., Adams, N.M., Tasoulis, D.K., Hand, D.J. | Pattern Recognition Letters 2012 | [Paper](https://doi.org/10.1016/j.patrec.2011.08.019) | EWMA-based detection for abrupt changes |
| **Adaptive Algorithms for Classification of Streaming Data** — Kolter, J.Z., Maloof, M.A. | Machine Learning 2007 | [Paper](https://doi.org/10.1007/s10994-007-5019-5) | DWM (Dynamic Weighted Majority) for sudden drift |
| **ECDD: Error-Cut Drift Detection** — Pesaranghader, A., Viktor, H.L., Paquet, E. | IJCNN 2018 | [Paper](https://doi.org/10.1109/IJCNN.2018.8489395) | Detects sudden drift via error-rate cutting |
| **Just-in-Time Adaptive Classifiers** — Alippi, C., Boracchi, G., Roveri, M. | IEEE Trans. Neural Networks 2012 | [Paper](https://doi.org/10.1109/TNNLS.2012.2199267) | Triggers retraining precisely at concept change points |

---

## Gradual Concept Drift

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| **Detecting Gradual Concept Drift with Fisher's Exact Test** — Delany, S.J., Cunningham, P., Tsymbal, A., Coyle, L. | Pattern Recognition Letters 2005 | [Paper](https://doi.org/10.1016/j.patrec.2005.04.017) | Statistical test for gradual drift detection |
| **Gradual Forgetting for Adaptation to Concept Drift** — Koychev, I. | ECAI Workshop 2000 | [Paper](https://citeseerx.ist.psu.edu/document?doi=10.1.1.34.4393) | Forgetting mechanisms for gradual shift |
| **Characterizing Concept Drift** — Webb, G.I., Hyde, R., Cao, H., Nguyen, H.L., Petitjean, F. | Data Mining and Knowledge Discovery 2016 | [Paper](https://doi.org/10.1007/s10618-015-0448-4) | Formal characterization of drift types including gradual |
| **Gradual Drift Detection for Stream Regression** — Sobolewski, P., Wozniak, M. | Information Sciences 2013 | [Paper](https://doi.org/10.1016/j.ins.2013.02.019) | Detecting gradual drift in regression tasks |

---

## Recurring Concept Drift

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| ⭐ **Recurring Concept Drifts: A Survey** — Gonçalves, P.M., de Carvalho Santos, S.G., Barros, R.S., Vieira, D.C. | ACM Computing Surveys 2014 | [Paper](https://doi.org/10.1145/2542182.2542205) | Survey on recurring patterns and how to exploit them |
| **Concept Profiling for Recurring Concept Drift** — Yang, Y., Wu, X., Zhu, X. | KDD 2006 | [Paper](https://doi.org/10.1145/1150402.1150497) | Builds profiles of concepts for reuse |
| **Learning Recurring Concepts from Data Streams with a Context Change Detector** — Gama, J., Kosina, P. | SDM 2009 | [Paper](https://doi.org/10.1137/1.9781611972795.15) | Identifies and stores recurring concepts |
| **Concept Drift Memory Management with Self-Organizing Maps** — Ramamurthy, S., Bhatnagar, R. | Knowledge and Information Systems 2007 | [Paper](https://doi.org/10.1007/s10115-007-0092-8) | SOM-based concept storage for recurring drift |

---

## Ensemble Methods for Concept Drift

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                  ENSEMBLE STRATEGIES FOR DRIFT                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. CHUNK-BASED ENSEMBLE (SEA, AUE2)                                        │
│     ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐                                    │
│     │ M1 │ │ M2 │ │ M3 │ │ M4 │ │ M5 │  ← Models trained on chunks       │
│     └──┬─┘ └──┬─┘ └──┬─┘ └──┬─┘ └──┬─┘                                    │
│        │w1    │w2    │w3    │w4    │w5    ← Weighted by accuracy            │
│        └──────┴──────┴──────┴──────┘                                        │
│                      │                                                      │
│                      ▼                                                      │
│               [ FINAL VOTE ]                                                │
│                                                                             │
│  2. ONLINE ENSEMBLE (Leveraging Bagging, ARF)                               │
│     ┌──────────────────────────────┐                                        │
│     │  Data Stream ─────────────►  │                                        │
│     │     │   │   │   │            │                                        │
│     │     ▼   ▼   ▼   ▼           │                                        │
│     │    M1  M2  M3  M4           │ ← Each model has ADWIN                 │
│     │     │   │   │   │            │   for drift detection                  │
│     │     ▼   ▼   ▼   ▼           │                                        │
│     │    [Majority Vote / Avg]     │ ← Replace worst on drift              │
│     └──────────────────────────────┘                                        │
│                                                                             │
│  3. DIVERSITY-DRIVEN (DDD)                                                  │
│     ┌─────────────────┐  ┌─────────────────┐                               │
│     │ HIGH DIVERSITY  │  │ LOW DIVERSITY   │                                │
│     │ ensemble        │  │ ensemble        │                                │
│     │ (good for drift)│  │ (good stable)   │                                │
│     └────────┬────────┘  └────────┬────────┘                               │
│              └────────┬───────────┘                                          │
│                       ▼                                                     │
│              [ Switch on drift ]                                             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| ⭐ **A Streaming Ensemble Algorithm (SEA) for Large-Scale Classification** — Street, W.N., Kim, Y. | KDD 2001 | [Paper](https://doi.org/10.1145/502512.502568) | Foundational streaming ensemble for drift |
| ⭐ **Online Accuracy Updated Ensemble for Data Streams with Concept Drift** — Brzezinski, D., Stefanowski, J. | ECML-PKDD 2014 | [Paper](https://doi.org/10.1007/978-3-662-44845-8_4) [Code](https://riverml.xyz/) | OAUE — accuracy-weighted ensemble for streams |
| **Accuracy Updated Ensemble (AUE2)** — Brzezinski, D., Stefanowski, J. | Information Sciences 2014 | [Paper](https://doi.org/10.1016/j.ins.2013.12.025) | Improved accuracy-based ensemble weighting |
| **Adaptive Random Forests for Evolving Data Stream Classification** — Gomes, H.M., Bifet, A., Read, J., et al. | Machine Learning 2017 | [Paper](https://doi.org/10.1007/s10994-017-5642-8) [Code](https://riverml.xyz/latest/api/forest/ARFClassifier/) | Random forests adapted for concept drift |
| **Streaming Random Patches for Evolving Data Streams** — Gomes, H.M., Read, J., Bifet, A. | ICDM 2019 | [Paper](https://doi.org/10.1109/ICDM.2019.00034) | Combines random subspace + bagging for drift |
| **Leveraging Bagging for Evolving Data Streams** — Bifet, A., Holmes, G., Pfahringer, B. | ECML-PKDD 2010 | [Paper](https://doi.org/10.1007/978-3-642-15880-3_15) | Bagging with ADWIN for drift-aware streaming |
| **DDD: Diversity for Dealing with Drifts** — Minku, L.L., Yao, X. | IEEE Trans. Knowledge and Data Eng. 2012 | [Paper](https://doi.org/10.1109/TKDE.2011.58) | Ensemble diversity management for drift |
| **Learn++.NSE: Non-Stationary Environment Learning** — Elwell, R., Polikar, R. | IEEE Trans. Neural Networks 2011 | [Paper](https://doi.org/10.1109/TNN.2011.2160459) | Incremental ensemble learning under drift |

---

## Decision Trees & Rules under Drift

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| ⭐ **Very Fast Decision Rules for Multi-Class Problems (VFDR)** — Gama, J., Kosina, P. | Machine Learning 2011 | [Paper](https://doi.org/10.1007/s10994-011-5255-5) | Streaming decision rules with drift handling |
| **Mining High-Speed Data Streams (VFDT / Hoeffding Tree)** — Domingos, P., Hulten, G. | KDD 2000 | [Paper](https://doi.org/10.1145/347090.347107) | Foundational stream classifier |
| **Hoeffding Adaptive Trees (HAT)** — Bifet, A., Gavaldà, R. | SIAM SDM 2009 | [Paper](https://doi.org/10.1137/1.9781611972795.34) [Code](https://riverml.xyz/latest/api/tree/HoeffdingAdaptiveTreeClassifier/) | Hoeffding trees with ADWIN for drift adaptation |
| **Extremely Fast Decision Tree (EFDT)** — Manapragada, C., Webb, G.I., Salehi, M. | KDD 2018 | [Paper](https://doi.org/10.1145/3219819.3220005) | Faster streaming trees with drift handling |

---

## Neural Network Approaches

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| **Learn++ with Neural Networks for Nonstationary Environments** — Polikar, R., Upda, L., Upda, S., Honavar, V. | IEEE Trans. SMC 2001 | [Paper](https://doi.org/10.1109/5326.983933) | Neural ensemble for non-stationary data |
| **Online Deep Learning: Learning Deep Neural Networks on the Fly** — Sahoo, D., Pham, Q., Lu, J., Hoi, S.C. | IJCAI 2018 | [Paper](https://arxiv.org/abs/1711.03705) [Code](https://github.com/phquang/OnlineDeepLearning) | Deep networks that adapt to concept drift online |
| **Concept Drift Detection in Neural Networks** — Disabato, S., Roveri, M. | IJCNN 2020 | [Paper](https://doi.org/10.1109/IJCNN48605.2020.9207110) | Drift detection embedded in neural architectures |
| **Continual Learning with Concept Drift** — Mallya, A., Lazebnik, S. | CVPR 2018 | [Paper](https://arxiv.org/abs/1801.06519) | PackNet approach for continual learning under shift |

---

## Theoretical Foundations

| Title & Authors | Venue | Links | Description |
|---|---|---|---|
| **On the Complexity of Concept Drift** — Helmbold, D.P., Long, P.M. | COLT 1994 | [Paper](https://doi.org/10.1145/180139.181125) | Theoretical analysis of learning under drift |
| **Tracking the Best Expert** — Herbster, M., Warmuth, M. | Machine Learning 1998 | [Paper](https://doi.org/10.1023/A:1007424614876) | Regret bounds for tracking changing distributions |
| **Statistical Learning under Changing Distributions** — Mohri, M., Muñoz Medina, A. | ICML 2012 | [Paper](https://proceedings.mlr.press/v22/mohri12.html) | Generalization bounds under distribution shift |
| **The Dynamics of Concept Drift** — Minku, L.L., White, A., Yao, X. | ECML-PKDD 2010 | [Paper](https://doi.org/10.1007/978-3-642-15883-4_24) | Formal analysis of drift dynamics and speed |
