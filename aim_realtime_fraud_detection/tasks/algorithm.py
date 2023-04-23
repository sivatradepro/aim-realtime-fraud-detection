from pyspark.sql import DataFrame
from aim_realtime_fraud_detection.tasks.abstract.task import AbstractTask

class Algorithm(AbstractTask):
    
    @property
    def _input_table(self) -> str:
        return self.config_manager.get("data.raw.location")

    @property
    def _output_table(self) -> str:
        return self.config_manager.get("data.model.output")

    def _input(self) -> DataFrame:
        partition_expr = f"{self._partition_column_run_day} = {self.execution_date.strftime('%Y%m%d')}"
        self.logger.info(f"Reading from table {self._input_table}. Date partition '{partition_expr}'.")
        return self.spark.read.table(self._input_table).where(partition_expr)

    def _transform(self, df: DataFrame) -> DataFrame:
        print("algorithm transform")
        


# object Algorithms {
#   val logger = Logger.getLogger(getClass.getName)
#   def randomForestClassifier(df: org.apache.spark.sql.DataFrame)(implicit sparkSession:SparkSession) = {
#     import sparkSession.implicits._
#     val Array(training, test) = df.randomSplit(Array(0.7, 0.3))
#     val randomForestEstimator = new RandomForestClassifier().setLabelCol("label").setFeaturesCol("features").setMaxBins(700)
#     val model = randomForestEstimator.fit(training)
#     val transactionwithPrediction = model.transform(test)
#     logger.info(s"total data count is" + transactionwithPrediction.count())
#     logger.info("count of same label " + transactionwithPrediction.filter($"prediction" === $"label").count())
#     model
#   }
# }

# from pyspark.sql import SparkSession
# spark = SparkSession.builder.appName('ml-iris').getOrCreate()
# df = spark.read.csv('IRIS.csv', header = True, inferSchema = True)
# df.printSchema()



