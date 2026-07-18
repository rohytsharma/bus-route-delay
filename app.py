"""
Bus Delay & Route Risk Dashboard — Streamlit app
Run AFTER the notebook has completed (it exports app_data/, models/, bus_delay_project.db).
Launch:  streamlit run app.py
"""
import os
import sqlite3
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Bus Delay & Route Risk", page_icon="🚌",
                   layout="wide", initial_sidebar_state="expanded")

# ---------- styling ----------
st.markdown("""
<style>
    .main {background-color: #f7f9fc;}
    section[data-testid="stSidebar"] {background: linear-gradient(180deg,#1f3b57 0%,#2e5a88 100%);}
    section[data-testid="stSidebar"] * {color: #eaf0f6 !important;}
    div[data-testid="stMetric"] {background: white; border-radius: 12px; padding: 14px;
        box-shadow: 0 2px 8px rgba(30,60,90,.08); border-left: 5px solid #2e5a88;}
    h1, h2, h3 {color: #1f3b57;}
    .risk-high {color:#c0392b; font-weight:700;}
</style>
""", unsafe_allow_html=True)

DATA = "app_data"
def load_csv(name):
    p = os.path.join(DATA, name)
    return pd.read_csv(p) if os.path.exists(p) else None

route_risk = load_csv("route_risk.csv")
comparison = load_csv("model_comparison.csv")
cls_metrics = load_csv("classification_metrics.csv")
roc_points = load_csv("roc_points.csv")
conf_mat = load_csv("confusion_matrix.csv")
feat_imp = load_csv("feature_importance.csv")
delay_by_hour = load_csv("delay_by_hour.csv")
delay_by_dow = load_csv("delay_by_dow.csv")
top_routes = load_csv("top_routes_freq.csv")
worst_routes = load_csv("worst_routes.csv")
sample_trips = load_csv("sample_trips.csv")

# ---------- sidebar ----------
with st.sidebar:
    st.title("🚌 Route Risk Platform")
    st.caption("Stagecoach Merseyside — BODS data | PySpark pipeline")
    page = st.radio("Navigate", ["📊 Overview", "🔍 Exploratory Analysis",
                                  "🤖 Model Performance", "🎯 Compliance Classifier",
                                  "⚡ Live Delay Predictor", "🗺️ Route Risk Explorer",
                                  "ℹ️ About"])
    st.divider()
    st.caption("Big Data Programming Project · ST5011CEM")

# ---------- pages ----------
if page == "📊 Overview":
    st.title("Transport Authority — Route Risk Overview")
    st.caption("Composite risk scoring across the network: predicted delay + headway regularity + service reliability")
    if route_risk is not None:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Routes scored", f"{len(route_risk):,}")
        c2.metric("Avg predicted delay", f"{route_risk['predicted_avg_delay'].mean():.2f} min")
        c3.metric("Avg reliability", f"{100*route_risk['service_reliability_rate'].mean():.1f}%")
        c4.metric("Routes above 85% target", f"{(route_risk['service_reliability_rate']>=0.85).sum()}")
        st.divider()
        left, right = st.columns([3, 2])
        with left:
            top = route_risk.nlargest(10, "route_risk_score")
            fig = px.bar(top[::-1], x="route_risk_score", y="route_description", orientation="h",
                         color="route_risk_score", color_continuous_scale="RdYlGn_r",
                         title="Top 10 Highest-Risk Routes (intervention priority)")
            fig.update_layout(height=460, showlegend=False, coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)
        with right:
            fig = px.scatter(route_risk, x="predicted_avg_delay", y="service_reliability_rate",
                             color="route_risk_score", color_continuous_scale="RdYlGn_r",
                             hover_name="route_description",
                             title="Reliability vs Predicted Delay")
            fig.add_hline(y=0.85, line_dash="dash", line_color="red",
                          annotation_text="85% target")
            fig.update_layout(height=460)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Run the notebook first — app_data/route_risk.csv not found.")

elif page == "🔍 Exploratory Analysis":
    st.title("Exploratory Data Analysis")
    c1, c2 = st.columns(2)
    if delay_by_hour is not None:
        with c1:
            fig = px.area(delay_by_hour, x="hour", y="avg_delay",
                          title="Average Delay by Hour of Day")
            fig.add_vrect(x0=7, x1=9, fillcolor="red", opacity=0.15, annotation_text="AM rush")
            fig.add_vrect(x0=16, x1=18, fillcolor="firebrick", opacity=0.15, annotation_text="PM rush")
            st.plotly_chart(fig, use_container_width=True)
    if delay_by_dow is not None:
        with c2:
            fig = px.bar(delay_by_dow, x="operating_day", y="avg_delay",
                         color="avg_delay", color_continuous_scale="Blues",
                         title="Average Delay by Day of Week")
            fig.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)
    c3, c4 = st.columns(2)
    if top_routes is not None:
        with c3:
            fig = px.bar(top_routes[::-1], x="trips", y="line_name", orientation="h",
                         title="Top 10 Most Frequent Lines", color_discrete_sequence=["#8e44ad"])
            st.plotly_chart(fig, use_container_width=True)
    if worst_routes is not None:
        with c4:
            fig = px.bar(worst_routes[::-1], x="avg_delay", y="route_description", orientation="h",
                         title="Top 10 Routes by Average Delay", color_discrete_sequence=["#c0392b"])
            st.plotly_chart(fig, use_container_width=True)
    if sample_trips is not None and "delay_minutes" in sample_trips.columns:
        fig = px.histogram(sample_trips, x="delay_minutes", nbins=60,
                           title="Delay Distribution (sample)", color_discrete_sequence=["#5bb8b4"])
        st.plotly_chart(fig, use_container_width=True)

elif page == "🤖 Model Performance":
    st.title("Regression Model Comparison")
    if comparison is not None:
        best = comparison.sort_values("rmse").iloc[0]
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Best model", best["model"])
        c2.metric("RMSE", f"{best['rmse']:.3f} min")
        c3.metric("MAE", f"{best['mae']:.3f} min")
        c4.metric("R²", f"{best['r2']:.3f}")
        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            fig = px.bar(comparison, x="model", y="rmse", title="RMSE (lower is better)",
                         color="model", color_discrete_sequence=px.colors.qualitative.Set2)
            st.plotly_chart(fig, use_container_width=True)
            fig = px.bar(comparison, x="model", y="r2", title="R² (higher is better)",
                         color="model", color_discrete_sequence=px.colors.qualitative.Set2)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            fig = px.bar(comparison, x="model", y="mae", title="MAE (lower is better)",
                         color="model", color_discrete_sequence=px.colors.qualitative.Set2)
            st.plotly_chart(fig, use_container_width=True)
            fig = px.bar(comparison, x="model", y="train_time_sec", title="Training Time (s)",
                         color="model", color_discrete_sequence=px.colors.qualitative.Set2)
            st.plotly_chart(fig, use_container_width=True)
    if feat_imp is not None:
        fig = px.bar(feat_imp, x="importance", y="feature", orientation="h",
                     title="Feature Importance (Random Forest)", color_discrete_sequence=["#e67e22"])
        st.plotly_chart(fig, use_container_width=True)

elif page == "🎯 Compliance Classifier":
    st.title("Service-Reliability Compliance Classifier")
    st.caption("Trips within ±2 minutes of timetable = compliant (brief's Service Reliability tolerance)")
    if cls_metrics is not None:
        m = cls_metrics.iloc[0]
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Accuracy", f"{m['accuracy']:.3f}")
        c2.metric("Precision", f"{m['precision']:.3f}")
        c3.metric("Recall", f"{m['recall']:.3f}")
        c4.metric("F1-score", f"{m['f1']:.3f}")
        c5.metric("ROC-AUC", f"{m['auc']:.3f}")
        st.divider()
    c1, c2 = st.columns(2)
    if conf_mat is not None:
        with c1:
            z = conf_mat.set_index(conf_mat.columns[0]).values
            fig = go.Figure(data=go.Heatmap(z=z, x=["Compliant","Non-compliant"],
                                            y=["Compliant","Non-compliant"],
                                            colorscale="Blues", text=z, texttemplate="%{text:,}"))
            fig.update_layout(title="Confusion Matrix", xaxis_title="Predicted", yaxis_title="Actual")
            st.plotly_chart(fig, use_container_width=True)
    if roc_points is not None:
        with c2:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=roc_points["fpr"], y=roc_points["tpr"],
                                     mode="lines", name="ROC", line=dict(width=3, color="#2e5a88")))
            fig.add_trace(go.Scatter(x=[0,1], y=[0,1], mode="lines", name="Random",
                                     line=dict(dash="dash", color="red")))
            fig.update_layout(title="ROC Curve", xaxis_title="False Positive Rate",
                              yaxis_title="True Positive Rate")
            st.plotly_chart(fig, use_container_width=True)

elif page == "⚡ Live Delay Predictor":
    st.title("Live Delay Prediction")
    st.caption("Runs the saved PySpark model on your inputs — genuine model inference, not a lookup.")
    if not os.path.exists("models/best_regressor"):
        st.error("models/best_regressor not found — run the notebook first.")
    elif route_risk is None:
        st.error("app_data/route_risk.csv not found — run the notebook first.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            route = st.selectbox("Route", sorted(route_risk["route_description"].unique()))
            day = st.selectbox("Day of week", ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
        with col2:
            hour = st.slider("Hour of departure", 5, 23, 8)
            duration = st.slider("Scheduled journey duration (min)", 5, 120, 35)
        if st.button("🔮 Predict delay", type="primary", use_container_width=True):
            with st.spinner("Loading Spark model and predicting..."):
                @st.cache_resource
                def get_spark_and_models():
                    from pyspark.sql import SparkSession
                    from pyspark.ml import PipelineModel
                    from pyspark.ml.regression import (LinearRegressionModel,
                        RandomForestRegressionModel, GBTRegressionModel)
                    spark = (SparkSession.builder.appName("DelayPredictorApp")
                             .master("local[2]").getOrCreate())
                    feat = PipelineModel.load("models/feature_pipeline")
                    model = None
                    for cls in (RandomForestRegressionModel, GBTRegressionModel, LinearRegressionModel):
                        try:
                            model = cls.load("models/best_regressor"); break
                        except Exception:
                            continue
                    return spark, feat, model
                spark, feat_model, reg_model = get_spark_and_models()
                hist = float(route_risk.loc[route_risk["route_description"]==route,
                                            "predicted_avg_delay"].iloc[0])
                row = spark.createDataFrame([{
                    "route_description": route, "operating_day": day, "hour": int(hour),
                    "scheduled_duration_minutes": float(duration),
                    "historical_avg_delay": hist, "delay_minutes": 0.0,
                }])
                pred = reg_model.transform(feat_model.transform(row)).select("prediction").first()[0]
            verdict = "🟢 COMPLIANT (within ±2 min)" if abs(pred) <= 2 else "🔴 NON-COMPLIANT (outside ±2 min)"
            c1, c2 = st.columns(2)
            c1.metric("Predicted delay", f"{pred:.2f} minutes")
            c2.metric("Service Reliability verdict", verdict)
            gauge = go.Figure(go.Indicator(mode="gauge+number", value=pred,
                title={"text": "Predicted delay (min)"},
                gauge={"axis": {"range": [-3, 12]},
                       "bar": {"color": "#2e5a88"},
                       "steps": [{"range": [-3, 2], "color": "#c8e6c9"},
                                 {"range": [2, 5], "color": "#fff3cd"},
                                 {"range": [5, 12], "color": "#f8d7da"}]}))
            st.plotly_chart(gauge, use_container_width=True)

elif page == "🗺️ Route Risk Explorer":
    st.title("Route Risk Explorer")
    st.caption("Query the SQLite results database — parameterised queries only (SQL-injection safe).")
    if os.path.exists("bus_delay_project.db"):
        thr = st.slider("Minimum risk score", 0.0, 1.0, 0.4, 0.05)
        conn = sqlite3.connect("bus_delay_project.db")
        df = pd.read_sql_query(
            "SELECT * FROM route_risk_scores WHERE route_risk_score >= ? ORDER BY route_risk_score DESC",
            conn, params=(thr,))   # parameterised — never string concatenation
        conn.close()
        st.metric("Routes above threshold", len(df))
        fig = px.bar(df.head(15)[::-1], x="route_risk_score", y="route_description", orientation="h",
                     color="route_risk_score", color_continuous_scale="RdYlGn_r",
                     title=f"Routes with risk ≥ {thr:.2f}")
        fig.update_layout(height=520, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df.round(3), use_container_width=True, height=300)
    else:
        st.error("bus_delay_project.db not found — run the notebook first.")

else:
    st.title("About this Platform")
    st.markdown("""
**Predictive Delay & Route Risk Scoring for a City Transport Authority**

| Layer | Technology |
|---|---|
| Ingestion | BODS TransXChange XML (151 real Stagecoach Merseyside files) |
| Processing | PySpark — calendar expansion, cleaning, caching, broadcast joins, Spark SQL |
| Augmentation | Documented synthetic delay signal (brief Strategy 3), grounded in a real SIRI-VM sample |
| ML | 3 regressors compared (Linear / Random Forest / GBT) + compliance classifier (LogReg) |
| Scoring | Composite Route Risk Score = 0.5·delay + 0.25·headway + 0.25·unreliability |
| Storage | SQLite with parameterised queries |
| Dashboard | Streamlit + Plotly |

**Note:** delay values are synthetically augmented (BODS keeps no historical location archive);
metrics demonstrate pipeline correctness, not validated real-world accuracy.
""")
