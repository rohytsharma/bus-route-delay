# Bus Delay & Route Risk Scoring — Setup Guide

## 1. Install dependencies
```bash
pip install -r requirements.txt
```

## 2. Folder layout (place data next to the notebook)
```
project/
├── bus_delay_risk_scoring.ipynb
├── app.py
├── requirements.txt
└── data/
    ├── timetable/timetable/   <- your 151 .xml files
    └── location/location/     <- location CSVs (all_siri_vm_analysed.csv etc.)
```
If your XML files are in a different folder, edit `TIMETABLE_DIR` in the "Locate and parse" step.

## 3. Run the notebook
```bash
jupyter notebook
```
Run all cells top to bottom. As you go, screenshot each "📸 Figure N" output — there are 77 numbered figures.
The notebook exports:
- `figures/` — every chart as PNG
- `app_data/` — CSVs the dashboard reads
- `models/` — saved feature pipeline + best regressor (for the live predictor)
- `bus_delay_project.db` + `bus_delay_project_dump.sql` — SQLite results + dump

Keep the **Spark UI (http://localhost:4040)** open — a few figures are screenshots of its Jobs/Storage tabs.

## 4. Run the dashboard (after the notebook finishes)
```bash
streamlit run app.py
```
Pages: Overview, Exploratory Analysis, Model Performance, Compliance Classifier
(confusion matrix + ROC), Live Delay Predictor (runs the saved Spark model), Route Risk Explorer.
Screenshot the dashboard pages for the report's UI figures.

## 5. Spark configuration (documented for the brief)
- Master: `local[4]` (4 partitions minimum)
- `spark.sql.shuffle.partitions = 8`
- `spark.driver.memory = 4g`
- Caching, repartitioning, broadcast join, Spark SQL, lazy-eval/DAG all demonstrated.

## 6. If a cell errors
Paste the exact traceback back and it'll be a quick fix — you're the first to run the Spark cells,
since PySpark can't be executed in the build sandbox.

## 7. Submission checklist
- [ ] Report exported to PDF, named `NAME_studentID.pdf`
- [ ] Fill cover page + update Table of Contents / Table of Figures fields in Word
- [ ] Insert screenshots into every "PLACE SCREENSHOT HERE" box
- [ ] Fill the [INSERT] model metric values in the Results table
- [ ] GitHub repo link added to the Appendix
- [ ] Repo contains: notebook, app.py, requirements.txt, this README, SQL dump, figures/
