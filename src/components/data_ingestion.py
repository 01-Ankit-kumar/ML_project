import os 
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

# Configuration class for data ingestion paths
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
            train_data.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_data.to_csv(self.ingestion_config.test_data_path, index=False, header=True)
            
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
    obj.initiate_data_ingestion()
