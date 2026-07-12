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
ecom_data['order_date']=pd.to_datetime(ecom_data['order_date'], errors='coerce', format='mixed')
ecom_data.dropna(subset=['order_date'], inplace=True)
logging.info(f'Converting dtype of order_date column to datetime and dropping null values')

#Converting columns like price,total and quantity to float and integer respectively 
#and dropping columns with non numerical value
ecom_data['quantity']=pd.to_numeric(ecom_data['quantity'], errors='coerce').astype('Int64')
ecom_data['price']=pd.to_numeric(ecom_data['price'], errors='coerce').astype('Float64')
ecom_data['total']=pd.to_numeric(ecom_data['total'], errors='coerce').astype('Float64')
logging.info(f'Convertion of price, total and quantity columns to int and float is successfull')

#Dropping rows with missing category
missing_category= ecom_data['category'].isnull().sum()
ecom_data.dropna(subset=['category'], inplace=True)
if ecom_data['category'].isnull().sum()==0:
    logging.info('QUALITY GATE PASSES: No missing value remains in category column')
else:
    logging.critical(f'QUALITY GATE FAILED: Found {missing_category} null values')
    #Physically stopping the script
    raise ValueError('Pipleline halted due to unhealed missing values')

#Dealing with null values in price quantity and total columns
numeric_column=['price','quantity','total']
for col in numeric_column:
    if col=='quantity':
        ecom_data[col]=ecom_data.groupby('category')[col].transform(lambda x: x.fillna(np.round(x.mean())))
        #Incase whole quantity column is empty
        global_qty=int(np.round(ecom_data[col].mean()))
        ecom_data[col]=ecom_data[col].fillna(global_qty)
    else:  
        ecom_data[col]=ecom_data.groupby('category')[col].transform(lambda x: x.fillna(x.mean()))
        #Incase whole quantity column is empty
        global_val=ecom_data[col].mean()
        ecom_data[col]=ecom_data[col].fillna(global_val)

remaining_nulls= ecom_data[numeric_column].isnull().sum().sum()
if remaining_nulls==0:
    logging.info(f'FINAL QUALITY GATE PASSED: All null values have been removed , column is healed')
else:
    logging.critical(f'FINAL QUALITY GATE FAILED: {remaining_nulls} null values still remains in numeric columns')
    raise ValueError('Pipeline halted: Numeric columns have not healed perfectly')

#Checking for duplicates and removing if any
duplicate_count=ecom_data.duplicated().sum()
if duplicate_count>0:
    logging.warning(f'DUPLICATE ROWS DETECTED...removing them')
    ecom_data.drop_duplicates(inplace=True)
    logging.info(f'Removed {duplicate_count} duplicated rows')
else:
    logging.info(f' NO DUPLICATE VALUES EXISTS')

#Forcing total equal to quantity*price to fix any incorrect total
ecom_data['total']=ecom_data['quantity']*ecom_data['price']
