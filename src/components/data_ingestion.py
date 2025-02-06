import os 
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.components.data_transformation import DataTransformationConfig,DataTransformation

# Configuration class for data ingestion paths
'''
import os

class DataIngestionConfig:
    def __init__(self, train_data_path=None, test_data_path=None, raw_data_path=None):
        self.train_data_path = train_data_path or os.path.join('artifacts', 'train.csv')
        self.test_data_path = test_data_path or os.path.join('artifacts', 'test.csv')
        self.raw_data_path = raw_data_path or os.path.join('artifacts', 'data.csv')

    def __repr__(self):
        return (f"DataIngestionConfig(train_data_path='{self.train_data_path}', "
                f"test_data_path='{self.test_data_path}', "
                f"raw_data_path='{self.raw_data_path}')")

# Example usage
config = DataIngestionConfig()
print(config)

if we had not used data class
'''

@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', 'train.csv')
    test_data_path: str = os.path.join('artifacts', 'test.csv')
    raw_data_path: str = os.path.join('artifacts', 'data.csv')

# Class for handling data ingestion process
class DataIngestion:
    def __init__(self):
        # Initialize configuration for data ingestion
        self.ingestion_config = DataIngestionConfig()
         
    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion component")
        try:
            # Read the dataset into a dataframe
            df = pd.read_csv('dataset\\stud.csv')
            logging.info("read the dataset as dataframe")

            # Create directories if they do not exist
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)
            
            # Save the raw data to a CSV file
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            logging.info("train test split initiated")
            
            # Split the data into train and test sets
            train_data, test_data = train_test_split(df, test_size=0.2, random_state=42)

            # Save the train and test data to CSV files
            train_data.to_csv(self.ingestion_config.train_data_path, index=False, header=True) ## index,header??
            test_data.to_csv(self.ingestion_config.test_data_path, index=False, header=True)
            
            ## index=False → Prevents Pandas from writing row indices to the CSV.
            ## header=True → Ensures column names are included in the CSV.
            
            
            logging.info("ingestion of data is completed")
            
            # Return the paths to the train and test data
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
            )
        
        except Exception as e:
            # Raise a custom exception in case of error
            raise CustomException(e, sys)

# Main function to initiate the data ingestion process
if __name__ == "__main__":
    obj = DataIngestion()
    train_data,test_data = obj.initiate_data_ingestion()

    data_transformation = DataTransformation()
    data_transformation.initiate_data_transformation(train_data,test_data)