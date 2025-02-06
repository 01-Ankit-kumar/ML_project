import os
import sys
import numpy as np
from dataclasses import dataclass
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    # Path to save the preprocessor object
    preprocessor_obj_file_path = os.path.join('artifacts', "preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        # Initialize configuration
        self.data_tranformation_config = DataTransformationConfig()
        
    def get_data_transformer_obj(self):
        '''
        This function is responsible for creating a preprocessing pipeline that includes:
        - Imputation (handling missing values)
        - Scaling (standardization of numerical features)
        - Encoding (converting categorical variables to numerical form)
        '''
        try:
            # Defining numerical and categorical feature columns
            numerical_features = ['writing_score', 'reading_score']
            categorical_features = [
                'gender',
                'race_ethnicity',
                'parental_level_of_education',
                'lunch',
                'test_preparation_course'
            ]
            
            # Creating a pipeline for numerical features
            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy='median')),  # Handle missing values with median
                    ("scaler", StandardScaler())  # Standardize numerical features
                ]
            )
            logging.info(f"Numerical features: {numerical_features}")
            
            # Creating a pipeline for categorical features
            cat_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='most_frequent')),  # Handle missing categorical values
                    ('one_hot_encoding', OneHotEncoder()),  # Convert categorical variables to numerical form
                    ('scaler', StandardScaler(with_mean=False))  # Scale categorical features (only necessary if needed for modeling)
                ]
            )
            logging.info(f"Categorical columns: {categorical_features}")
            
            # Combine both pipelines using ColumnTransformer
            preprocessor = ColumnTransformer(
                transformers=[
                    ('num_pipeline', num_pipeline, numerical_features),
                    ('cat_pipeline', cat_pipeline, categorical_features)
                ]
            )
            return preprocessor
        
        except Exception as e:
            raise CustomException(e, sys)
    
    def initiate_data_transformation(self, train_path, test_path):
        try:
            # Read training and testing datasets
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            
            logging.info("Read train and test data completed")
            logging.info("Obtaining the preprocessing object")
            
            # Get the preprocessing object
            preprocessing_obj = self.get_data_transformer_obj()
            target_column_name = "math_score"
            numerical_columns = ['writing_score', 'reading_score']
            
            # Separating input features and target variable for train and test sets
            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]
            
            logging.info("Applying preprocessing object on training and testing data")
            
            # Applying transformations
            input_feature_train_array = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_array = preprocessing_obj.transform(input_feature_test_df)
            
            # Concatenating transformed features with target variable
            train_arr = np.c_[
                input_feature_train_array, np.array(target_feature_train_df)
            ]
            
            test_arr = np.c_[
                input_feature_test_array, np.array(target_feature_test_df)
            ]
            
            logging.info("Saving preprocessing object")
            
            # Save the preprocessor object for later use
            save_object(
                file_path=self.data_tranformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )
            
            return (
                train_arr,
                test_arr,
                self.data_tranformation_config.preprocessor_obj_file_path
            )
        
        except Exception as e:
            raise CustomException(e, sys)