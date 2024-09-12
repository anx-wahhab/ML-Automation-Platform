# AutoML Platform with Streamlit, PySpark, and HDFS

This repository contains an automated machine learning platform built with **Streamlit**, **PySpark**, and **Hadoop's HDFS**. The platform allows users to sign up, train models, make predictions, and generate dummy datasets. It integrates PySpark for distributed data processing and uses HDFS for storing and retrieving machine learning models.

## Features

### 1. User Authentication:
- Users can **sign up** and **log in** to the platform for personalized access.

### 2. Model Training:
- Users can upload datasets, specify the target variable, and select one or more machine learning models to train.
- The platform automatically **cleans** and **processes** the dataset, trains the selected model(s), and **saves** the models using **HDFS** for distributed storage.

### 3. Model Prediction:
- Users can select previously trained models and input a dataset for predictions.
- The platform handles data preprocessing and generates predictions with accuracy and other performance metrics, using models retrieved from HDFS.

### 4. Dummy Data Generation:
- Users can generate dummy datasets based on custom instructions, which can be used for testing and experimentation purposes.

## Prerequisites:
- **Hadoop HDFS**: For model storage and retrieval.
- **PySpark**: For distributed data processing.
- **Streamlit**: For the frontend interface.

## Code Files
- **`db_conn.py`**: Handles database connections for user authentication and model management.
- **`dummy_data_generator.py`**: Generates dummy datasets based on user inputs.
- **`GUI.py`**: The main Streamlit interface for user interaction, handling login, dataset upload, and model selection.
- **`login_page.py`**: Manages user authentication (sign up and login).
- **`models.py`**: Contains machine learning models for training and prediction.
- **`preprocessing.py`**: Handles data cleaning, preprocessing, and preparation for both training and prediction.

## Libraries & Frameworks Used:
- **Streamlit**: For the frontend interface.
- **Pandas**: For data manipulation and preprocessing.
- **Scikit-learn**: For machine learning models.
- **PySpark**: For distributed data processing.
- **Hadoop HDFS**: For saving and retrieving models.

## Future Enhancements:
- Add support for more machine learning algorithms.
- Implement more advanced data preprocessing techniques.
- Expand user analytics and model performance tracking.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
