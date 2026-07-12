#Importing all the libraries needed
import pandas as pd
import numpy as np
import logging

#Setting up logging data
logging.basicConfig(
    filename='ecommerce_sales.log',
    filemode='w',  # Force it to overwrite fresh every single run
    level=logging.INFO, 
    format='%(asctime)s - [%(levelname)s] - %(message)s'
)

#Reading and loading the raw dataset
ecom_data=pd.read_csv('messy_ecommerce_sales_data.csv')
logging.info(f"Succesfully loaded the the file, initial shape is: {ecom_data.shape}")

#Stip the unwanted space of the column headers and turning them in lowercase
ecom_data.columns=ecom_data.columns.str.strip().str.lower()

#Dropping the column which are not required
drop_columns=['id','customer_name','order_id']
ecom_data.drop(drop_columns, axis=1, inplace=True)
logging.info(f'Tracking dropped columns, Remaining columns are; {list(ecom_data.columns)}')

#Converting order_date format from str to datetime
ecom_data['order_date']=pd.to_datetime(ecom_data['order_date'], errors='coerce')
logging.info(f'Converting dtype of order_date column to datetime')

#Converting columns like price and quantity to float and integer respectively 
#and dropping columns with non numerical value
ecom_data['quantity']=pd.to_numeric(ecom_data['quantity'], errors='coerce').astype('Int64')
ecom_data['price']=pd.to_numeric(ecom_data['price'], errors='coerce').astype('Float64')
logging.info(f'Convertion of price and quantity columns to int and float is successfull')

#Dropping rows with missing category
missing_category= ecom_data['category'].isnull().sum()
ecom_data.dropna(subset=['category'], inplace=True)
if ecom_data['category'].isnull().sum()==0:
    logging.info('QUALITY GATE PASSES: No missing value remains')
else:
    logging.critical(f'QUALITY GATE FAILED: Found {missing_category} null values')
    #Physically stopping the script
    raise ValueError('Pipleline halted due to unhealed missing values')