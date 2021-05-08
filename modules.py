import pandas as pd
from numba import jit
from datetime import datetime
import numpy as np
pd.options.plotting.backend = "plotly"


def convert_lat_lon(x: str) -> tuple:
    """
    This function converts the lat and lon column data to a tuple
    :param x: Location json converted into a string format
    :return:  Tuple of lat and lon

    >>> convert_lat_lon("{\'latitude\': \'34.024\', \'longitude\': \'-118.409\'}")
    (34.024, -118.409)
    >>> convert_lat_lon(pd.read_csv('data/arrest-data-from-2010-to-present.csv')['Location'].iloc[21])
    (34.1695, -118.3774)
    """
    return float(eval(x)['latitude']), float(eval(x)['longitude'])


@jit(forceobj=True)
def calc_zip(lat, lon, zip_data) -> list:
    """
    This function calculates the zipcode from the given latitude and longitude columns of a crime occurred in the dataset
    :param zip_data: Dataset containing lat lon zip mapping
    :param lon: Longitude
    :param lat: Latitude
    :return:  Zipcode

    >>> zip_test_data = pd.read_csv('data/ziplatlon.csv', dtype={'ZIP': 'str'})
    >>> calc_zip(34.0954, -118.2961, zip_test_data)
    '90029'
    >>> calc_zip(32.534, -118.463, zip_test_data)
    '90704'
    >>> calc_zip(35.049, -119.678, zip_test_data)
    '93254'

    """
    zip_lat_list = zip_data['LAT'].to_list()
    zip_lon_list = zip_data['LNG'].to_list()
    zip_zip_list = zip_data['ZIP'].to_list()
    res_zip = None
    res_dis = 999
    for i in range(len(zip_zip_list)):
        zzip = zip_zip_list[i]
        zlat = zip_lat_list[i]
        zlon = zip_lon_list[i]
        tdis = (zlat - lat) ** 2 + (zlon - lon) ** 2
        if tdis < res_dis:
            res_dis = tdis
            res_zip = zzip

    return res_zip


def arrest_clean(file_path: str) -> pd.DataFrame:
    """
    This function performs the data cleaning for the arrest dataset
    :param x: arrest-data-from-2010-to-present.csv dataset file
    :return:  Pandas Dataframe

    >>> arrest_clean(pd.read_csv('data/arrest-data-from-2010-to-present.csv'))

    """
    arrest_data = pd.read_csv(file_path, dtype={'ZipCode': 'str'})
    arrest_data.dropna(subset=['Charge Group Description', 'Charge Group Code'], inplace=True)
    arrest_data['Charge Group Code'] = arrest_data['Charge Group Code'].astype('int')
    arrest_data['Year'] = arrest_data['Arrest Date'].apply(lambda x: x[:4])
    return arrest_data[['Report ID', 'Arrest Date', 'Age', 'Sex Code', 'Charge Group Code',
                        'Charge Group Description', 'Lat', 'Lon', 'ZipCode', 'Year']]


def crime_clean(file_path: str) -> pd.DataFrame:
    """
    This function performs the data cleaning for the crime dataset
    :param x: crime-data-from-2010-to-present.csv dataset file
    :return:  Pandas Dataframe

    >>> crime_clean(pd.read_csv('data/crime-data-from-2010-to-present.csv'))

    """
    crime_data = pd.read_csv(file_path, dtype={'ZipCode': 'str'})
    crime_data['Year'] = crime_data['Date Occurred'].apply(lambda x: x[:4])
    crime_data['Crime Date'] = crime_data['Date Occurred'].apply(lambda x: x[:10])
    return crime_data[['DR Number', 'Date Reported', 'Date Occurred', 'Crime Code', 'Crime Code Description',
                       'Victim Age', 'Victim Sex', 'Lat', 'Lon', 'ZipCode', 'Year', 'Crime Date']]


def income_clean(file_path: str) -> pd.DataFrame:
    """
    This function performs the data cleaning for the income dataset
    :param x: LAIncome.csv dataset file
    :return:  Pandas Dataframe

    >>> arrest_clean(pd.read_csv('data/LAIncome.csv'))

    """
    income_data = pd.read_csv(file_path, sep='\t', dtype={'Zip': 'str'})
    income_data.drop(income_data[income_data['Amount'].apply(lambda x: not x.startswith('$'))].index, axis=0,
                     inplace=True)
    income_data['Amount'] = income_data['Amount'].replace('[\$,]', '', regex=True).astype(int)
    return income_data[['Zip', 'Amount']]


def full_moon_finder(file_path: str) -> pd.DataFrame:
    moon_data = pd.read_csv(file_path)
    moon_data['Form_Date'] = pd.to_datetime(moon_data[' Date'])
    moon_dates = moon_data['Form_Date'].astype('str').to_list()
    return moon_dates


def dst_clean(file_path: str, days_to_check) -> pd.DataFrame:
    """
    This function performs the data cleaning for the daylight savings dataset. It is a nested function which checks whether a crime data was a fullmoon night or not.
    :param x: LAIncome.csv dataset file, crime_data Dataframe
    :return:  Pandas Dataframe

    >>> dst_clean(pd.read_csv('data/dst.csv'))

    """
    dst_data = pd.read_csv(file_path, dtype={'Year': 'str'}, index_col='Year')
    dst_data['Start Complete'] = pd.to_datetime(dst_data['Start'] + ' ' + dst_data.index.astype(str))
    dst_data['End Complete'] = pd.to_datetime(dst_data['End'] + ' ' + dst_data.index.astype(str))

    def was_time_ahead(check_date) -> pd.DataFrame:
        check_date = datetime.strptime(check_date, '%Y-%m-%d')
        dst_selected_year = dst_data.loc[check_date.year].to_dict()
        return dst_selected_year['Start Complete'] <= check_date < dst_selected_year['End Complete']

    was_time_ahead_vec = np.vectorize(was_time_ahead)
    was_dst_df = pd.DataFrame({'Date': days_to_check,
                             'WasDST': was_time_ahead_vec(days_to_check)})
    return was_dst_df


def race_clean(file_path: str) -> pd.DataFrame:
    """
    This function performs the data cleaning for the races dataset
    :param x: LARace.csv dataset file
    :return:  Pandas Dataframe

    >>> race_clean(pd.read_csv('data/LARace.csv'))

    """
    race_data = pd.read_csv(file_path, dtype={'Zip Code': 'str'})
    race_data = race_data[race_data['Total Population'] > 1000]
    return race_data


def plot_daylight_crime_rate(crime_desc_list, crime_rates_dst):
    """
        This function plots a histogram for Hypothesis 3
        :param x: crime_desc_list, crime_rates_dst
        :return:  Dataframe Plot

        >>> race_clean(pd.read_csv('data/LARace.csv'))

        """
    for crime_desc in crime_desc_list:
        plot_data = crime_rates_dst[crime_rates_dst['Crime Code Description'] == crime_desc].melt().iloc[1:]
        fig = plot_data.plot.bar(x='variable',
                            y='value',
                           title=crime_desc,
                           labels={'variable':'Time','value':'Daily Crime Rate'})
        fig.show()
