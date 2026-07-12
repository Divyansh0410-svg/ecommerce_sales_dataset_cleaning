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
ecom_data.info()

#Stip the unwanted space of the column headers and turning them in lowercase
ecom_data.columns=ecom_data.columns.str.strip().str.lower()

#Dropping the column which are not required
drop_columns=['id','customer_name','order_id']
ecom_data.drop(drop_columns, axis=1, inplace=True)
logging.info(f'Tracking dropped columns, Remaining columns are; {list(ecom_data.columns)}')