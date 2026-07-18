# 🚌 Predictive Delay & Route Risk Scoring Platform

**A Big Data Programming Project — ST5011CEM**

A distributed PySpark pipeline that ingests real UK Bus Open Data Service (BODS) timetables, predicts trip-level delays, classifies service-reliability compliance, and derives a composite **Route Risk Score** for a city transport authority — presented through an interactive Streamlit dashboard.

> **Network:** Stagecoach Merseyside & South Lancashire (SCMY) — Liverpool / St Helens region
> **Scale:** 151 real TransXChange files → 11,585 daily scheduled trips → several million annual trip-instances

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
- [Data Sources](#data-sources)
- [Machine Learning](#machine-learning)
- [Big Data Evidence](#big-data-evidence)
- [Security](#security)
- [Limitations](#limitations)
- [Author](#author)
- [License](#license)

---

## Overview

Urban bus networks generate large volumes of timetable and location data, yet transport authorities lack a consolidated, data-driven way to identify which routes are least reliable and where intervention budgets should be directed. This project builds an end-to-end big-data pipeline that:

1. **Ingests** real BODS timetable data via a custom TransXChange XML parser
2. **Scales** the dataset to millions of records through calendar expansion (PySpark)
3. **Augments** a documented, literature-informed synthetic delay signal (BODS provides no historical location archive)
4. **Predicts** delay using three compared regression models (Linear Regression, Random Forest, Gradient-Boosted Trees)
5. **Classifies** service-reliability compliance (±2 min tolerance) with a Logistic Regression classifier
6. **Scores** every route with a composite, weighted Route Risk Score
7. **Presents** everything through a live Streamlit dashboard with real-time model inference

## Key Features

- ✅ **Real data backbone** — 151 genuine BODS TransXChange files, zero parse errors
- ✅ **Genuine distributed processing** — PySpark DataFrames, Spark SQL, partitioning, caching, repartitioning, broadcast joins, lazy evaluation/DAG
- ✅ **3-model regression comparison** with CrossValidator hyperparameter tuning
- ✅ **Compliance classifier** with full metric suite (Accuracy, Precision, Recall, F1, ROC-AUC, confusion matrix)
- ✅ **Composite Route Risk Score** combining predicted delay, headway irregularity, and service reliability
- ✅ **Secure storage** — SQLite with parameterised queries only (no string concatenation)
- ✅ **Interactive dashboard** — Streamlit + Plotly, including a live delay predictor running the saved Spark model
- ✅ **77+ visual figures** — every analytical result is charted, not just tabulated

## Architecture
BODS Timetables (XML)  ──┐
├─► Python Parser ─► PySpark DataFrame ─► Calendar Expansion
BODS Location (sample) ──┘                                              │
▼
Synthetic Augmentation (PySpark UDF)
│
▼
Cleaning & Caching (PySpark) ─► Feature Engineering (MLlib)
│
▼
Train/Test Split ─► 3× Regression Models + Classifier
│
▼
Route Risk Scoring ─► SQLite ─► Streamlit Dashboard
## Tech Stack

| Layer | Technology |
|---|---|
| Distributed processing | Apache PySpark 3.5 (DataFrames, Spark SQL, MLlib) |
| Ingestion | Python `xml.etree.ElementTree` |
| Data storage | SQLite (parameterised queries), Parquet (checkpointing) |
| Machine learning | PySpark MLlib — Linear Regression, Random Forest, GBT, Logistic Regression, CrossValidator |
| Visualisation | Matplotlib, Plotly |
| Dashboard | Streamlit |
| Notebook environment | Jupyter |

## Project Structure
.
├── bus_delay_risk_scoring.ipynb   # Main pipeline — 85 steps, 77+ figures
├── app.py                          # Streamlit dashboard
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
├── data/
│   ├── timetable/timetable/          # 151 real TransXChange XML files
│   └── location/location/             # Real SIRI-VM location sample (CSV)
├── figures/                         # Auto-exported chart PNGs (generated on run)
├── app_data/                        # CSVs powering the dashboard (generated on run)
├── models/                          # Saved feature pipeline + best regressor (generated on run)
├── bus_delay_project.db             # SQLite results database (generated on run)
└── bus_delay_project_dump.sql       # SQL dump for submission (generated on run)

## Setup & Installation

```bash
# Clone the repository
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

# Install dependencies
pip install -r requirements.txt
```

**Requirements:** Python 3.10+, Java 8/11 (required by PySpark), ~4GB free RAM.

## Usage

### 1. Run the notebook
```bash
jupyter notebook bus_delay_risk_scoring.ipynb
```
Run all cells top to bottom. This ingests the data, trains all models, and exports everything the dashboard needs into `figures/`, `app_data/`, and `models/`.

Keep the **Spark UI** open at [http://localhost:4040](http://localhost:4040) while running — several figures are captured from its Jobs/Storage tabs.

### 2. Launch the dashboard
```bash
streamlit run app.py
```
Navigate between: **Overview**, **Exploratory Analysis**, **Model Performance**, **Compliance Classifier**, **Live Delay Predictor**, and **Route Risk Explorer**.

## Data Sources

- **Timetables:** [Bus Open Data Service](https://data.bus-data.dft.gov.uk/) — Stagecoach Merseyside & South Lancashire, TransXChange XML format
- **Location:** BODS SIRI-VM real-time vehicle activity sample (used as a schema/value-range template for synthetic augmentation, since BODS retains no historical location archive)

All data is published under the UK Open Government Licence and contains no personal information.

## Machine Learning

| Task | Models Compared | Metrics |
|---|---|---|
| Delay prediction (regression) | Linear Regression, Random Forest, Gradient-Boosted Trees | RMSE, MAE, R², training time, R²/sec (Model Efficiency) |
| Compliance classification | Logistic Regression | Accuracy, Precision, Recall, F1, ROC-AUC, confusion matrix |

Hyperparameters for the Random Forest family are tuned via a 3-fold `CrossValidator` grid search.

## Big Data Evidence

- Dataset scaled from 11,585 daily trips to **millions of annual trip-instances** via calendar expansion
- Spark configured with **≥4 partitions**, explicit `.cache()` / `.repartition()` calls throughout
- **Broadcast join** used for the route-metadata lookup
- **Spark SQL** used for complex aggregations (`spark.sql(...)`)
- **Lazy evaluation / DAG** demonstrated explicitly via `.explain()`
- Parquet used as the intermediate persistence/checkpoint format

## Security

- All SQL access — in both the notebook and the dashboard — uses **parameterised queries** (`?` placeholders), never string concatenation
- No hard-coded credentials
- Source data contains no personal information (GDPR-compliant)

## Limitations

- Delay values are **synthetically augmented** (documented, brief-sanctioned strategy) since BODS provides no historical location archive — results demonstrate pipeline correctness, not validated real-world accuracy
- Travel Time Variability and passenger-load-based Service Efficiency were not computed (data unavailable via the BODS free tier)
- Route Risk Score weights are a documented default, not calibrated against a real transport authority's stated priorities

See the accompanying report for full critical reflection.

## Author

**ROHIT SHARMA**
Module: Big Data Programming Project (ST5011CEM)


## License

This project is submitted as academic coursework. Source bus data is used under the [UK Open Government Licence](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).
