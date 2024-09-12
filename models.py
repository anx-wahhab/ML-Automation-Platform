import os
import pickle
import db_conn
import pandas as pd
import streamlit as st
from pyspark.ml import PipelineModel
from pyspark.ml.regression import LinearRegression, RandomForestRegressor, GBTRegressor
from pyspark.ml.classification import NaiveBayes, LogisticRegression, RandomForestClassifier
from pyspark.ml.classification import LogisticRegressionModel, RandomForestClassificationModel, NaiveBayesModel


class Model:
    def __init__(self, dataset_name, task):
        self.classifiers = []
        self.regressors = []
        self.model_dic = {}
        self.dataset_name = dataset_name
        self.task = task
        self.trained_models = []
        self.initialize()
        self.selected_models = None
        self.path = 'Models/' + db_conn.current_user_session() + '/' + self.task + '/' + self.dataset_name

    def initialize(self):
        self.classifiers = ['Logistic Regression', 'Naive Bayes', 'Random Forest Classifier']

        self.regressors = ['Linear Regression', 'Random Forest Regressor',
                           'Gradiant Boosted Tree Regressor']

        classifier_models = [LogisticRegression, NaiveBayes, RandomForestClassifier]
        regressor_models = [LinearRegression, RandomForestRegressor, GBTRegressor]

        self.model_dic = {key: value for key, value in zip(self.classifiers, classifier_models)}
        self.model_dic.update({key: value for key, value in zip(self.regressors, regressor_models)})

    def go(self, df, target_variable, models):
        self.selected_models = models
        train, test = df.randomSplit([0.8, 0.2], seed=42)
        self.train(train, target_variable, models=models)
        self.save_models()
        predictions = self.predict(test, self.task, fun='evaluate')
        return predictions

    def train(self, train, output_feature, models):
        self.trained_models = []
        for model in models:
            model = self.model_dic.get(model)
            model = model(featuresCol='scaled_features', labelCol=output_feature + '_indexed')
            model = model.fit(train)
            self.trained_models.append(model)

    def predict(self, unclassified_instances, task, fun):
        trained_models = self.load_models()
        all_predictions = pd.DataFrame()
        """
        axis=0 -> Within Each Column, iteration over rows 
        axis=1 -> Within each row, iteration over columns  
        """
        for model in trained_models:
            predictions = getattr(model, 'transform')(unclassified_instances).select('prediction').toPandas()
            # predictions = model.transform(unclassified_instances).select('prediction').toPandas()
            all_predictions = pd.concat([all_predictions, predictions], axis=1)

        if task == 'Classification':
            return all_predictions.apply(lambda row: row.mode(), axis=1)

        return all_predictions.apply(lambda row: row.mean(), axis=1)

    def save_models(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        for model in self.trained_models:
            model.write().overwrite().save(self.path + '/' + str(model).split(":")[0])

    def load_models(self):
        models = []
        saved_model_types = os.listdir(self.path)
        for model in saved_model_types:
            models.append(getattr(__import__('pyspark.ml.' + self.task.lower(), fromlist=[model]), model).load(self.path + '/' + model))

        return models

    @staticmethod
    def check_trained_datasets(dataset, task):
        return dataset in os.listdir('Models/' + db_conn.current_user_session() + '/' + task + '/')
