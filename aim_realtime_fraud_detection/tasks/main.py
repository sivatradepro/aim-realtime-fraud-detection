import argparse
import datetime
import pathlib
from datetime import datetime

from pyspark.sql import SparkSession

from config_manager import ConfigManager
from aim_realtime_fraud_detection.tasks.task_runner import TaskRunner


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(allow_abbrev=False)

    parser.add_argument("--task", type=str, required=True, choices=["algorithm"])
    parser.add_argument("--config-file-path", type=pathlib.Path, required=True)

    return parser.parse_args()


def _init_spark(task: str) -> SparkSession:
    execution_date = datetime.now()
    return (
        
        SparkSession.builder.appName(f"Movies task {task} - {execution_date.strftime('%Y%m%d')}")
        .config("spark.sql.sources.partitionOverwriteMode", "dynamic")
        .enableHiveSupport()
        .getOrCreate()
    )


def main() -> None:
    args = _parse_args()
    spark = _init_spark(args.task)
    config_manager = ConfigManager(args.config_file_path)
    TaskRunner(spark, config_manager, args.task).run()


if __name__ == "__main__":
    main()
