

from pyspark.sql import SparkSession

SPARK_CONFIG = {
    "app_name": "BusDelayRiskScoring",
    "master": "local[4]",                     # 4 local cores -> satisfies >=4 partitions requirement
    "spark.sql.shuffle.partitions": "8",
    "spark.driver.memory": "4g",
}

INGESTION_PARTITIONS = 4
PROCESSING_PARTITIONS = 8

SQLITE_DB_PATH = "bus_delay_project.db"
SQL_DUMP_PATH = "bus_delay_project_dump.sql"

TIMETABLE_DIR = "data/timetable/timetable"
LOCATION_SAMPLE_PATH = "data/location/location/all_siri_vm_analysed.csv"

CALENDAR_START_DATE = "2025-08-01"
CALENDAR_END_DATE = "2026-07-31"

SPLIT_DATE = "2026-06-01"


def get_spark_session() -> SparkSession:
    """Build the SparkSession using the settings above. Import and call this
    from the notebook or any script instead of duplicating configuration."""
    builder = SparkSession.builder.appName(SPARK_CONFIG["app_name"]).master(SPARK_CONFIG["master"])
    for key, value in SPARK_CONFIG.items():
        if key not in ("app_name", "master"):
            builder = builder.config(key, value)
    return builder.getOrCreate()
