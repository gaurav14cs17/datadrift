# Tools & Frameworks

[← Back to Main Page](README.md)

Open-source libraries, cloud platforms, and production tools for data drift detection, monitoring, and mitigation.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     DRIFT DETECTION ECOSYSTEM MAP                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  OPEN SOURCE LIBRARIES                         CLOUD PLATFORMS              │
│  ═════════════════════                         ═══════════════              │
│                                                                             │
│  ┌─────────────────┐  ┌─────────────────┐     ┌─────────────────┐          │
│  │  Evidently AI   │  │   Alibi Detect  │     │  AWS SageMaker  │          │
│  │                 │  │                 │     │  Model Monitor  │          │
│  │ Dashboards +    │  │ Deep learning + │     └─────────────────┘          │
│  │ Reports + Tests │  │ Statistical     │     ┌─────────────────┐          │
│  │ ★★★★★           │  │ ★★★★☆           │     │  Azure ML       │          │
│  └─────────────────┘  └─────────────────┘     │  Data Drift     │          │
│  ┌─────────────────┐  ┌─────────────────┐     └─────────────────┘          │
│  │    NannyML      │  │     River       │     ┌─────────────────┐          │
│  │                 │  │                 │     │  Google Vertex   │          │
│  │ No-label perf.  │  │ Online/Streaming│     │  AI Monitoring  │          │
│  │ estimation      │  │ All detectors  │     └─────────────────┘          │
│  │ ★★★★☆           │  │ ★★★★★           │                                  │
│  └─────────────────┘  └─────────────────┘     COMMERCIAL PLATFORMS          │
│  ┌─────────────────┐  ┌─────────────────┐     ═══════════════════          │
│  │   Deepchecks    │  │    WhyLabs     │     ┌─────────────────┐          │
│  │                 │  │   (whylogs)     │     │  Arize AI       │          │
│  │ Testing suite + │  │                 │     │  Fiddler AI     │          │
│  │ CI/CD ready     │  │ Lightweight     │     │  Aporia         │          │
│  │ ★★★★☆           │  │ profiling       │     │  Arthur AI      │          │
│  └─────────────────┘  │ ★★★★☆           │     │  Superwise      │          │
│                       └─────────────────┘     └─────────────────┘          │
│                                                                             │
│  DATA VALIDATION              ONLINE LEARNING       EXPERIMENT TRACKING     │
│  ═══════════════              ═══════════════       ════════════════════    │
│  ┌──────────────┐             ┌──────────────┐     ┌──────────────┐        │
│  │Great Expect. │             │    River     │     │   MLflow     │        │
│  │TFDV          │             │    MOA       │     │   W&B        │        │
│  │Deequ         │             │    Vowpal W. │     │   Neptune    │        │
│  │Pandera       │             │    CapyMOA   │     │   DVC        │        │
│  └──────────────┘             └──────────────┘     └──────────────┘        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

```
    CHOOSING THE RIGHT TOOL — DECISION FLOWCHART
    ══════════════════════════════════════════════

    What's your use case?
           │
     ┌─────┼──────────────────────────────────────────┐
     │     │                                          │
     ▼     ▼                                          ▼
   Batch  Streaming                              Production
   data?  data?                                  monitoring?
     │     │                                          │
     ▼     ▼                                          ▼
  ┌──────┐ ┌──────┐                              ┌──────────┐
  │Evid- │ │River │                              │WhyLabs / │
  │ently │ │      │◄── Need all-in-one? ───────►│Evidently  │
  │Alibi │ │MOA   │                              │Cloud     │
  │NannyML│ │      │                              └──────────┘
  └──────┘ └──────┘
     │         │
     ▼         ▼
   Need      Need just         Need cloud     Need data
   reports?  detection?        managed?       validation?
     │         │                   │              │
     ▼         ▼                   ▼              ▼
  Evidently  Alibi Detect    SageMaker /     Great Expect.
             Frouros         Azure ML /      TFDV / Deequ
             TorchDrift      Vertex AI
```

---

## Quick Links

- [Drift Detection Libraries](#drift-detection-libraries)
- [ML Monitoring Platforms](#ml-monitoring-platforms)
- [Data Validation Tools](#data-validation-tools)
- [Online Learning Frameworks](#online-learning-frameworks)
- [Cloud Platform Tools](#cloud-platform-tools)
- [Experiment Tracking with Drift](#experiment-tracking-with-drift)

---

## Drift Detection Libraries

| Tool | Description | Links | Language |
|---|---|---|---|
| ⭐ **Evidently AI** | Open-source ML monitoring. Data drift reports, test suites, dashboards. Supports tabular, text, embeddings. 35+ drift metrics including PSI, KS, Wasserstein, Jensen-Shannon. | [GitHub](https://github.com/evidentlyai/evidently) [Docs](https://docs.evidentlyai.com/) [Paper](https://arxiv.org/abs/2104.00370) | Python |
| ⭐ **Alibi Detect** | Drift detection for tabular, text, images, time series. KS, MMD, Chi-squared, Learned Kernel, Classifier, Spot-the-diff detectors. TensorFlow & PyTorch backends. | [GitHub](https://github.com/SeldonIO/alibi-detect) [Docs](https://docs.seldon.io/projects/alibi-detect/) [Paper](https://arxiv.org/abs/2012.06078) | Python |
| ⭐ **NannyML** | Performance estimation without labels. CBPE and DLE methods. Univariate and multivariate drift detection. | [GitHub](https://github.com/NannyML/nannyml) [Docs](https://nannyml.readthedocs.io/) | Python |
| ⭐ **River** | Online machine learning library. All major drift detectors: ADWIN, DDM, EDDM, HDDM, KSWIN, Page-Hinkley. Integrated with adaptive learners. | [GitHub](https://github.com/online-ml/river) [Docs](https://riverml.xyz/) [Paper](https://jmlr.org/papers/v22/20-1380.html) | Python |
| **Deepchecks** | ML validation & testing suite. Data drift, model performance, data integrity checks. CI/CD integration ready. | [GitHub](https://github.com/deepchecks/deepchecks) [Docs](https://docs.deepchecks.com/) | Python |
| **Frouros** | Drift detection library with 20+ detectors. Both concept and data drift. Supports batch and streaming. | [GitHub](https://github.com/IFCA/frouros) [Paper](https://doi.org/10.1016/j.softx.2023.101478) | Python |
| **Menelaus** | Lightweight streaming drift detection. Implements DDM, EDDM, ADWIN, CUSUM, Page-Hinkley, STEPD, MD3. | [GitHub](https://github.com/mitre/menelaus) [Docs](https://menelaus.readthedocs.io/) | Python |
| **Eurybia** | Model drift monitoring with Shapley-based explanations. Generates drift reports with interpretability. | [GitHub](https://github.com/MAIF/eurybia) [Docs](https://eurybia.readthedocs.io/) | Python |
| **PopMon** | Population shift monitoring. Synthetic data comparison and distribution testing. | [GitHub](https://github.com/ing-bank/popmon) | Python |
| **Scikit-Multiflow** | Streaming ML framework (predecessor to River). Drift detectors and adaptive classifiers. | [GitHub](https://github.com/scikit-multiflow/scikit-multiflow) [Paper](https://jmlr.org/papers/v19/18-251.html) | Python |
| **TorchDrift** | Drift detection for PyTorch models. Kernel-based tests (MMD), dimensionality reduction, classification-based detection. | [GitHub](https://github.com/torchdrift/torchdrift) [Docs](https://torchdrift.org/) | Python |
| **DataProfiler** | Data profiling and drift. Automated schema detection and statistical profiling. | [GitHub](https://github.com/capitalone/DataProfiler) | Python |

---

## ML Monitoring Platforms

| Tool | Description | Links | Type |
|---|---|---|---|
| ⭐ **Evidently AI (Cloud)** | Full monitoring platform with dashboards, alerts, test suites. Open-core model. | [Website](https://www.evidentlyai.com/) [GitHub](https://github.com/evidentlyai/evidently) | Open Source + Cloud |
| ⭐ **WhyLabs (whylogs)** | Lightweight data logging and monitoring. Statistical profiles with low overhead. Real-time drift detection. | [GitHub](https://github.com/whylabs/whylogs) [Website](https://whylabs.ai/) | Open Source + Cloud |
| **Arize AI** | Production ML observability. Embedding drift, performance monitoring, root cause analysis. | [Website](https://arize.com/) | Commercial |
| **Fiddler AI** | ML model monitoring and explainability. Drift detection with feature importance explanations. | [Website](https://www.fiddler.ai/) | Commercial |
| **Aporia** | Real-time ML monitoring. Custom drift metrics, automated alerts, dashboard builder. | [Website](https://www.aporia.com/) | Commercial |
| **Superwise** | ML observability platform. Automated drift detection with smart alerting. | [Website](https://superwise.ai/) | Commercial |
| **Arthur AI** | ML monitoring with bias and drift detection. Performance degradation alerts. | [Website](https://www.arthur.ai/) | Commercial |
| **Censius** | AI observability. Data drift, concept drift, model performance monitoring. | [Website](https://censius.ai/) | Commercial |
| **Qualdo** | Data quality and ML monitoring. Automated drift detection and anomaly alerting. | [Website](https://www.qualdo.ai/) | Commercial |
| **Mona Labs** | Continuous ML monitoring. Context-aware drift detection with business metrics. | [Website](https://www.monalabs.io/) | Commercial |

---

## Data Validation Tools

| Tool | Description | Links | Type |
|---|---|---|---|
| ⭐ **Great Expectations** | Data validation framework. Expectation suites, data docs, checkpoint-based validation. | [GitHub](https://github.com/great-expectations/great_expectations) [Docs](https://docs.greatexpectations.io/) | Open Source |
| ⭐ **TensorFlow Data Validation (TFDV)** | Schema-based validation with drift/skew detection. Integrates with TFX pipelines. | [GitHub](https://github.com/tensorflow/data-validation) [Docs](https://www.tensorflow.org/tfx/data_validation/) | Open Source |
| **Deequ (Amazon)** | Data quality verification at scale. Unit tests for data. Runs on Spark. | [GitHub](https://github.com/awslabs/deequ) [Paper](https://doi.org/10.14778/3229863.3229867) | Open Source |
| **Pandera** | Statistical data validation for Pandas/Polars DataFrames. Schema-based checks with hypothesis tests. | [GitHub](https://github.com/unionai-oss/pandera) [Docs](https://pandera.readthedocs.io/) | Open Source |
| **Pydantic** | Data validation using Python type hints. Not drift-specific but foundational for schema validation. | [GitHub](https://github.com/pydantic/pydantic) | Open Source |
| **Soda** | Data quality testing platform. SQL-based checks with monitoring. | [GitHub](https://github.com/sodadata/soda-core) [Website](https://www.soda.io/) | Open Source + Cloud |

---

## Online Learning Frameworks

| Tool | Description | Links | Type |
|---|---|---|---|
| ⭐ **River** | Python online ML. Drift detectors + adaptive models in one library. | [GitHub](https://github.com/online-ml/river) [Docs](https://riverml.xyz/) | Open Source |
| **MOA (Massive Online Analysis)** | Java framework for data stream mining. WEKA integration. | [Website](https://moa.cms.waikato.ac.nz/) [GitHub](https://github.com/Waikato/moa) | Open Source |
| **Vowpal Wabbit** | Fast online learning system. Supports contextual bandits, reductions, and non-stationary environments. | [GitHub](https://github.com/VowpalWabbit/vowpal_wabbit) | Open Source |
| **Creme** | Predecessor to River. Incremental learning in Python. | [GitHub](https://github.com/MaxHalford/creme) | Open Source (archived) |
| **Apache SAMOA** | Distributed streaming ML framework. Scalable drift detection. | [GitHub](https://github.com/apache/incubator-samoa) | Open Source |
| **CapyMOA** | Python wrapper for MOA. Brings MOA's streaming algorithms to Python. | [GitHub](https://github.com/adaptive-machine-learning/CapyMOA) | Open Source |

---

## Cloud Platform Tools

| Tool | Description | Links | Provider |
|---|---|---|---|
| **Amazon SageMaker Model Monitor** | Automated drift detection for SageMaker endpoints. Data quality, model quality, bias drift, feature attribution drift. | [Docs](https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor.html) | AWS |
| **Azure ML Data Drift Monitor** | Built-in drift monitoring for Azure ML. Configurable alerts and automated dashboards. | [Docs](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-monitor-datasets) | Azure |
| **Google Vertex AI Model Monitoring** | Skew and drift detection for Vertex AI models. Training-serving skew and prediction drift. | [Docs](https://cloud.google.com/vertex-ai/docs/model-monitoring/overview) | GCP |
| **DataRobot MLOps** | Enterprise ML monitoring. Automated drift detection, accuracy tracking, retraining triggers. | [Website](https://www.datarobot.com/platform/mlops/) | Commercial |
| **Databricks Lakehouse Monitoring** | Table-level drift monitoring on Databricks. Profile-based statistical tests. | [Docs](https://docs.databricks.com/en/lakehouse-monitoring/index.html) | Databricks |
| **H2O MLOps** | ML operations with drift monitoring. Integrates with H2O model training. | [Website](https://h2o.ai/platform/ai-cloud/mlops/) | Commercial |

---

## Experiment Tracking with Drift

| Tool | Description | Links | Type |
|---|---|---|---|
| **MLflow** | Experiment tracking, model registry, model serving. Drift monitoring via custom metrics. | [GitHub](https://github.com/mlflow/mlflow) | Open Source |
| **Weights & Biases** | Experiment tracking with data versioning. Custom drift dashboards and alerts. | [Website](https://wandb.ai/) | Commercial |
| **Neptune.ai** | ML metadata store with monitoring capabilities. | [Website](https://neptune.ai/) | Commercial |
| **ClearML** | MLOps platform with experiment tracking and monitoring. | [GitHub](https://github.com/allegroai/clearml) | Open Source + Cloud |
| **DVC (Data Version Control)** | Data versioning for ML. Track data changes that may indicate drift. | [GitHub](https://github.com/iterative/dvc) | Open Source |

---

## Comparison Matrix

| Feature | Evidently | Alibi Detect | NannyML | River | WhyLabs |
|---|---|---|---|---|---|
| Univariate Drift | ✅ | ✅ | ✅ | ✅ | ✅ |
| Multivariate Drift | ✅ | ✅ | ✅ | ❌ | ✅ |
| Streaming Detection | ❌ | ❌ | ❌ | ✅ | ✅ |
| No-Label Detection | ✅ | ✅ | ✅ | Partial | ✅ |
| Visual Reports | ✅ | ✅ | ✅ | ❌ | ✅ (Cloud) |
| Image/Text Support | ✅ | ✅ | ❌ | ❌ | ✅ |
| CI/CD Integration | ✅ | ✅ | ✅ | ❌ | ✅ |
| Cloud Dashboard | ✅ | ❌ | ❌ | ❌ | ✅ |
| License | Apache 2.0 | BSL 1.1 | Apache 2.0 | BSD 3 | Apache 2.0 |
