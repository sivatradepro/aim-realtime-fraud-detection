import datetime
from abc import ABC, abstractmethod
from logging import Logger
from typing import List

from pyspark.sql import Catalog, DataFrame, SparkSession
from soda.scan import Scan

from config_manager import ConfigManager


class AbstractTask(ABC):
    """
    Base class to read a dataset, transform it, and save it to a table.
    """

    def __init__(
        self, spark: SparkSession, logger: Logger, execution_date: datetime.date, config_manager: ConfigManager
    ):
        self.spark = spark
        self.execution_date = execution_date
        self.config_manager = config_manager
        self.logger = logger

    def run(self) -> None:
        df = self._input()
        df_transformed = self._transform(df)
        self._output(df_transformed)        

    @abstractmethod
    def _input(self) -> DataFrame:
        raise NotImplementedError

    @abstractmethod
    def _transform(self, df: DataFrame) -> DataFrame:
        raise NotImplementedError

    def _output(self, df: DataFrame) -> None:
        self.logger.info(f"Saving to table {self._output_table}.")

        if self._table_exists(self._output_table):
            self.logger.info("Table exists, inserting.")
            df.write.mode("overwrite").insertInto(self._output_table)
        else:
            self.logger.info("Table does not exist, creating and saving.")
            partition_cols = [self._partition_column_run_day] + self._partition_columns_extra
            df.write.mode("overwrite").partitionBy(partition_cols).format("delta").saveAsTable(self._output_table)