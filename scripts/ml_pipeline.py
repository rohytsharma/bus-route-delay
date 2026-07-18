"""
ml_pipeline.py — Feature engineering, model training, and evaluation.

Standalone module version of the MLlib pipeline used in
bus_delay_risk_scoring.ipynb. Building a Pipeline this way documents the
exact stages (StringIndexer -> StringIndexer -> VectorAssembler) required by
the brief.
"""

from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.regression import LinearRegression, RandomForestRegressor, GBTRegressor
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder

FEATURE_COLUMNS = ["hour", "route_idx", "day_idx", "scheduled_duration_minutes", "historical_avg_delay"]


def add_historical_average_delay(df):
    """Add a leakage-safe historical average delay feature: for each route,
    the mean delay of all PRECEDING rows only (never future rows)."""
    window = (Window.partitionBy("route_description").orderBy("calendar_date")
              .rowsBetween(Window.unboundedPreceding, -1))
    df = df.withColumn("historical_avg_delay", F.avg("delay_minutes").over(window))
    global_mean = df.agg(F.mean("delay_minutes")).first()[0]
    return df.fillna({"historical_avg_delay": global_mean})


def build_feature_pipeline():
    """Build the MLlib feature engineering Pipeline (documented stages)."""
    route_indexer = StringIndexer(inputCol="route_description", outputCol="route_idx", handleInvalid="keep")
    day_indexer = StringIndexer(inputCol="operating_day", outputCol="day_idx", handleInvalid="keep")
    assembler = VectorAssembler(inputCols=FEATURE_COLUMNS, outputCol="features")
    return Pipeline(stages=[route_indexer, day_indexer, assembler])


def time_based_split(df, split_date):
    """Split a trip-level DataFrame into train/test sets by calendar date
    (not randomly), preventing future-date leakage."""
    train_df = df.filter(F.col("calendar_date") < split_date)
    test_df = df.filter(F.col("calendar_date") >= split_date)
    return train_df, test_df


def get_regression_models():
    """Return the three regression models compared in this project."""
    return {
        "LinearRegression": LinearRegression(featuresCol="features", labelCol="delay_minutes"),
        "RandomForest": RandomForestRegressor(featuresCol="features", labelCol="delay_minutes",
                                              numTrees=50, maxDepth=8, maxBins=320, seed=42),
        "GBTRegressor": GBTRegressor(featuresCol="features", labelCol="delay_minutes",
                                     maxIter=50, maxDepth=6, maxBins=320, seed=42),
    }


def evaluate_regression(fitted_model, test_df):
    """Evaluate a fitted regression model, returning RMSE, MAE, R²."""
    preds = fitted_model.transform(test_df)
    metrics = {}
    for name in ("rmse", "mae", "r2"):
        evaluator = RegressionEvaluator(labelCol="delay_minutes", predictionCol="prediction", metricName=name)
        metrics[name] = evaluator.evaluate(preds)
    return metrics


def cross_validate_random_forest(train_df, test_df):
    """3-fold CrossValidator hyperparameter search over the Random Forest."""
    rf = RandomForestRegressor(featuresCol="features", labelCol="delay_minutes", maxBins=320, seed=42)
    grid = ParamGridBuilder().addGrid(rf.numTrees, [20, 50]).addGrid(rf.maxDepth, [5, 8]).build()
    evaluator = RegressionEvaluator(labelCol="delay_minutes", predictionCol="prediction", metricName="rmse")
    cv = CrossValidator(estimator=rf, estimatorParamMaps=grid, evaluator=evaluator, numFolds=3, seed=42)
    cv_model = cv.fit(train_df)
    cv_rmse = evaluator.evaluate(cv_model.transform(test_df))
    return cv_model, cv_rmse
