import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import pandas as pd
import json
import plotly.express as plt
import config
import Dataset_Lists
import Database_List

def print_database_codes():
    '''
    Usage: Prints possible Database Codes to output
    '''
    print("\nDatabase Codes:\n")

    for database in Database_List.databases:
        print(database + '\n')

def print_dataset_codes(database_code):
    '''
    Usage: Prints possible Data Set Codes to output

    Parameters:
    database_code (str): Database code for a specific NASDAQ Database
    '''

    print("\nData Set Codes:\n")
    print("Pair : Code")

    if database_code == 'BOE':
        for key, value in Dataset_Lists.BOE_to_GBP.items():
            print(key + ' = ' + value + '\n')
    elif database_code == 'FRED':
        for key, value in Dataset_Lists.FRED_to_USD.items():
            print(key + ' = ' + value + '\n')
    elif database_code == 'ECB':
        for key, value in Dataset_Lists.ECB_to_EUR.items():
            print(key + ' = ' + value + '\n')

def get_price_data(database_code, dataset_code, api_key):
    '''
    Usage: Fetches data from NASDAQ Data Frame

    Parameters:
    database_code (str): Database code for a specific NASDAQ Database
    dataset_code (str): Data set code for specific NASDAQ Data set
    api_key (str): API Key for request authentication

    Returns: Corresponding data in a Pandas Data Frame
    '''
    url = f'https://data.nasdaq.com/api/v3/datasets/{database_code}/{dataset_code}/data.json?api_key={api_key}'

    try:
        response = requests.get(url)
    except (ConnectionError, Timeout, TooManyRedirects, Exception) as e:
        print(e + ': Unable to fetch data.')

    return pd.DataFrame(json.loads(response.text)['dataset_data']['data'], columns = ['Date', 'Price'])

def dataset_key(database_code, dataset_code):
    '''
    Usage: Finds key in Dataset List

    Parameters:
    dataset_code (str): Dictionary value
    value (str): Dictionary value

    Returns (str): Key
    '''
    if database_code == 'BOE':
        position = list(Dataset_Lists.BOE_to_GBP.values()).index(dataset_code)
        return list(Dataset_Lists.BOE_to_GBP)[position]
    elif database_code == 'FRED':
        position = list(Dataset_Lists.FRED_to_USD.values()).index(dataset_code)
        return list(Dataset_Lists.FRED_to_USD)[position]
    elif database_code == 'ECB':
        position = list(Dataset_Lists.ECB_to_EUR.values()).index(dataset_code)
        return list(Dataset_Lists.ECB_to_EUR)[position]



#MAIN

cont = 'Y'

while cont == 'Y':

    # Create variables for codes
    database_code = ''
    dataset_code = ''

    #Check whether the collected database code is valid or if the baselist needs to be printed off
    while (not database_code in Database_List.databases) or  database_code == 'baselist':
        print("Please input a NASDAQ Database Code (Ex. FRED). Type 'baselist' to print Database List.")
        database_code = input()

        if database_code == 'baselist':
            print_database_codes()

    #Check whether the collected setlist code is valid or if the setlist needs to be printed off
    while (not dataset_code in Dataset_Lists.BOE_to_GBP.values()) and (not dataset_code in Dataset_Lists.FRED_to_USD.values()) and (not dataset_code in Dataset_Lists.ECB_to_EUR.values()) or dataset_code == 'setlist':
        print("\nPlease input a NASDAQ Data Set Code (Ex. DEXUSAL). Type 'setlist' to print Data Set List.")
        dataset_code = input()

        if dataset_code == 'setlist':
            print_dataset_codes(database_code)

    #Collect api key
    api_key = config.api_key

    #Store the price data to a dataframe and restructure the data frame
    df = get_price_data(database_code, dataset_code, api_key)

    df['Date'] = pd.to_datetime(df['Date'])

    title = dataset_key(database_code, dataset_code)

    #Plot the price data
    fig = plt.line(df, x = 'Date', y = 'Price', title = title)

    fig.show()

    print(df)

    #Continue prompt
    print('Would you like to render another price chart? (Y/N)')
    cont = input()


