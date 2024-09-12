from pyspark.sql.types import StringType, IntegerType, NumericType
from pyspark.ml.feature import StringIndexer, StandardScaler
from pyspark.ml.feature import VectorAssembler
from pyspark.ml import Pipeline


def preprocess(data):
    data = handle_null_missing_values(data)
    data = encode(data)
    target_var = data.columns[-1]
    input_vars = data.select(data.columns)
    input_vars = handle_outliers(input_vars)
    scaled_data = scale_and_prepare(input_vars, target_var)
    return scaled_data


def handle_null_missing_values(data):
    for col in data.columns:
        if data.filter(data[col].isNull()).count() > 0:
            if isinstance(data.schema[col].dataType, StringType):
                data = data.fillna(method='bfill', subset=[col]).fillna(method='ffill', subset=[col])
            else:
                mean_val = data.select(col).agg({col: 'mean'}).collect()[0][0]
                data = data.fillna(mean_val, subset=[col])
    return data


def encode(data):
    for col in data.columns:
        if isinstance(data.schema[col].dataType, StringType):
            indexer = StringIndexer(inputCol=col, outputCol=col + "_indexed")
            data = indexer.fit(data).transform(data).drop(col)

    return data


def handle_outliers(data):

    for col in data.columns:
        if isinstance(data.schema[col].dataType, (IntegerType, NumericType)):
            quantiles = data.approxQuantile(col, [0.25, 0.75], 0.05)
            Q1 = quantiles[0]
            Q3 = quantiles[1]
            IQR = (Q3 - Q1) * 1.5
            lower = Q1 - IQR
            upper = Q3 + IQR

            filtered_data = data.filter((data[col] >= lower) & (data[col] <= upper))
            mean_without_outliers = filtered_data.agg({col: 'mean'}).collect()[0][0]
            data = data.fillna(mean_without_outliers, subset=[col])

    return data


def scale_and_prepare(data, tar_var):
    features = data.columns
    assembler = VectorAssembler(inputCols=features, outputCol="features")
    scaler = StandardScaler(inputCol="features", outputCol='scaled_features')
    return Pipeline(stages=[assembler, scaler]).fit(data).transform(data).select('scaled_features', str(tar_var))
