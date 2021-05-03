import pandas as pd
import plotly.express as px
from numba import jit
from datetime import datetime
import numpy as np
pd.options.plotting.backend = "plotly"


def convert_lat_lon(x:str) -> tuple:
    return float(eval(x)['latitude']), float(eval(x)['longitude'])


def was_time_ahead(check_date):
    check_date = datetime.strptime(check_date, '%Y-%m-%d')
    dst_selected_year = dst_data.loc[check_date.year].to_dict()
    return dst_selected_year['Start Complete'] <= check_date < dst_selected_year['End Complete']


@jit(forceobj=True)
def calc_zip(lat, lon, zip_data):
    zip_lat_list = zip_data['LAT'].to_list()
    zip_lon_list = zip_data['LNG'].to_list()
    zip_zip_list = zip_data['ZIP'].to_list()
    res_zip = None
    res_dis = 999

    i = 0
    for i in range(len(zip_zip_list)):
        zzip = zip_zip_list[i]
        zlat = zip_lat_list[i]
        zlon = zip_lon_list[i]
        tdis = (zlat - lat) ** 2 + (zlon - lon) ** 2
        if tdis < res_dis:
            res_dis = tdis
            res_zip = zzip

    return res_zip


def arrest_clean(file_path: str):
    arrest_data = pd.read_csv(file_path, dtype={'ZipCode': 'str'})
    arrest_data.dropna(subset=['Charge Group Description', 'Charge Group Code'], inplace=True)
    arrest_data['Charge Group Code'] = arrest_data['Charge Group Code'].astype('int')
    arrest_data['Year'] = arrest_data['Arrest Date'].apply(lambda x: x[:4])
    return arrest_data[['Report ID', 'Arrest Date', 'Age', 'Sex Code', 'Charge Group Code',
                        'Charge Group Description', 'Lat', 'Lon', 'ZipCode', 'Year']]


def crime_clean(file_path: str):
    crime_data = pd.read_csv(file_path, dtype={'ZipCode': 'str'})
    crime_data['Year'] = crime_data['Date Occurred'].apply(lambda x: x[:4])
    crime_data['Crime Date'] = crime_data['Date Occurred'].apply(lambda x: x[:10])
    return crime_data[['DR Number', 'Date Reported', 'Date Occurred', 'Crime Code', 'Crime Code Description',
                       'Victim Age', 'Victim Sex', 'Lat', 'Lon', 'ZipCode', 'Year', 'Crime Date']]


def income_clean(file_path: str):
    income_data = pd.read_csv(file_path, sep='\t', dtype={'Zip': 'str'})
    income_data.drop(income_data[income_data['Amount'].apply(lambda x: not x.startswith('$'))].index, axis=0,
                     inplace=True)
    income_data['Amount'] = income_data['Amount'].replace('[\$,]', '', regex=True).astype(int)
    return income_data[['Zip', 'Amount']]


def full_moon_finder(file_path: str):
    moon_data = pd.read_csv(file_path)
    moon_data['Form_Date'] = pd.to_datetime(moon_data[' Date'])
    moon_dates = moon_data['Form_Date'].astype('str').to_list()
    return moon_dates


def dst_clean(file_path: str, days_to_check):
    dst_data = pd.read_csv(file_path, dtype={'Year': 'str'}, index_col='Year')
    dst_data['Start Complete'] = pd.to_datetime(dst_data['Start'] + ' ' + dst_data.index.astype(str))
    dst_data['End Complete'] = pd.to_datetime(dst_data['End'] + ' ' + dst_data.index.astype(str))
    was_time_ahead = np.vectorize(was_time_ahead)
    was_dst_df = pd.DataFrame({'Date': days_to_check,
                             'WasDST': was_time_ahead(days_to_check)
                             })
    return was_dst_df


def race_clean(file_path: str):
    race_data = pd.read_csv(file_path, dtype={'Zip Code': 'str'})
    race_data = race_data[race_data['Total Population'] > 1000]
    return race_data


def plot_daylight_crime_rate(crime_desc_list):
    for crime_desc in crime_desc_list:
        plot_data = crime_rates_dst[crime_rates_dst['Crime Code Description'] == crime_desc].melt().iloc[1:]
        fig = plot_data.plot.bar(x='variable',
                            y='value',
                           title=crime_desc,
                           labels={'variable':'Time','value':'Daily Crime Rate'})
        fig.show()
