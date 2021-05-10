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
def calc_zip(lat: float, lon: float, zip_data: pd.DataFrame) -> list:
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
    :param file_path: File path for arrest_numba_zipcode.csv dataset
    :return:  Dataframe containing clenaed arrest data

    >>> test_data = arrest_clean('data/arrest_numba_zipcode.csv')
    >>> test_data.columns.to_list()
    ['Report ID', 'Arrest Date', 'Age', 'Sex Code', 'Charge Group Code', 'Charge Group Description', 'Lat', 'Lon', 'ZipCode', 'Year']
    >>> test_data['Charge Group Code'].isnull().values.any()
    False
    >>> test_data['Charge Group Code'].dtype
    dtype('int64')
    >>> test_data['Charge Group Description'].isnull().values.any()
    False
    >>> test_data.shape
    (1191071, 10)

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
    :param file_path: File path for crime_numba_zipcode.csv dataset
    :return:  Dataframe containing crime data

    >>> test_data = crime_clean('data/crime_numba_zipcode.csv')
    >>> test_data.columns.to_list()
    ['DR Number', 'Date Reported', 'Date Occurred', 'Crime Code', 'Crime Code Description', 'Victim Age', 'Victim Sex', 'Lat', 'Lon', 'ZipCode', 'Year', 'Crime Date']
    >>> test_data.shape
    (1993259, 12)
    >>> test_data['ZipCode'].dtype
    dtype('O')
    """
    crime_data = pd.read_csv(file_path, dtype={'ZipCode': 'str'})
    crime_data['Year'] = crime_data['Date Occurred'].apply(lambda x: x[:4])
    crime_data['Crime Date'] = crime_data['Date Occurred'].apply(lambda x: x[:10])
    return crime_data[['DR Number', 'Date Reported', 'Date Occurred', 'Crime Code', 'Crime Code Description',
                       'Victim Age', 'Victim Sex', 'Lat', 'Lon', 'ZipCode', 'Year', 'Crime Date']]


def income_clean(file_path: str) -> pd.DataFrame:
    """
    This function performs the data cleaning for the income dataset
    :param file_path: File path for LAIncome.csv dataset
    :return:  Cleaned income Dataframe

    >>> test_data = income_clean('data/LAIncome.csv')
    >>> test_data.columns.to_list()
    ['Zip', 'Amount']
    >>> test_data.shape
    (280, 2)
    >>> test_data['Amount'].dtype
    dtype('int64')
    >>> test_data['Amount'].isnull().values.any()
    False
    """
    income_data = pd.read_csv(file_path, sep='\t', dtype={'Zip': 'str'})
    income_data.drop(income_data[income_data['Amount'].apply(lambda x: not x.startswith('$'))].index, axis=0,
                     inplace=True)
    income_data['Amount'] = income_data['Amount'].replace('[\$,]', '', regex=True).astype(int)
    return income_data[['Zip', 'Amount']]


def full_moon_finder(file_path: str) -> list:
    """
    This function gives a list of the full_moon dates in the correct datetime format for further calculations
    :param file_path: File path for full_moon.csv dataset
    :return:  list of dates of full moon

    >>> test_data = full_moon_finder('data/full_moon.csv')
    >>> len(test_data)
    631
    >>> type(test_data[0])
    <class 'str'>
    """
    moon_data = pd.read_csv(file_path)
    moon_data['Form_Date'] = pd.to_datetime(moon_data[' Date'])
    moon_dates = moon_data['Form_Date'].astype('str').to_list()
    return moon_dates


def dst_clean(file_path: str, days_to_check: list) -> pd.DataFrame:
    """
    This function will give a datafram containing date and whther the date was during daylight time
    :param file_path: File path for dst.csv dataset
    :param days_to_check: list of days for which DST/Standard time needs to be calculated
    :return:  Dataframe containing whether the date was during dst or not

    >>> test_data = dst_clean('data/dst.csv', ['2010-05-04','2014-11-30', '2013-09-09'])
    >>> test_data.columns.to_list()
    ['Date', 'WasDST']
    >>> test_data.shape
    (3, 2)
    >>> test_data['WasDST'].to_list()
    [True, False, True]

    """
    dst_data = pd.read_csv(file_path, dtype={'Year': 'str'}, index_col='Year')
    dst_data['Start Complete'] = pd.to_datetime(dst_data['Start'] + ' ' + dst_data.index.astype(str))
    dst_data['End Complete'] = pd.to_datetime(dst_data['End'] + ' ' + dst_data.index.astype(str))

    def was_time_ahead(check_date: str) -> bool:
        """
        Function to see if the date was during daylight time.
        :param check_date: Data to check if DST
        :return: True if DST. False if Standard time
        """
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
    :param file_path: File path for LARace.csv dataset
    :return:  Cleaned dataframe with removed outliers

    >>> test_data = race_clean('data/LARace.csv')
    >>> test_data.shape
    (109, 10)
    >>> test_data.columns.to_list()
    ['Zip Code', 'Total Population', 'White Alone Not Hispanic or Latino', 'Black or African American Alone', 'American Indian & Alaska Native Alone', 'Asian Alone', 'Native Hawaiian & Other Pacific Islander Alone', 'Some Other Race Alone', 'Population of Two or More Races', 'Hispanic or Latino']
    >>> test_data['Zip Code'].dtype
    dtype('O')
    >>> test_data[test_data['Total Population'] < 1000].shape
    (0, 10)

    """
    race_data = pd.read_csv(file_path, dtype={'Zip Code': 'str'})
    race_data = race_data[race_data['Total Population'] > 1000]
    return race_data


def plot_daylight_crime_rate(crime_desc_list, crime_rates_dst):
    """
    This function plots a histogram for Hypothesis 3
    :param crime_rates_dst: Dataframe having the crime rate for standard time and daylight time
    :param crime_desc_list: List of crime descriptions for which a plot needs to be formed
    :return:  None. Plotly Plots

    """
    for crime_desc in crime_desc_list:
        plot_data = crime_rates_dst[crime_rates_dst['Crime Code Description'] == crime_desc].melt().iloc[1:]
        fig = plot_data.plot.bar(x='variable',
                            y='value',
                           title=crime_desc,
                           labels={'variable':'Time','value':'Daily Crime Rate'})
        fig.show()


def race_vs_arrest(arrest_data: pd.DataFrame, race_data: pd.DataFrame, arrest_charge: str, race: str) -> pd.DataFrame:
    """
    This function will create a dataframe for arrest vs percentage of a population of one race for every zip code
    :param arrest_data: Data about arrests
    :param race_data:  Data about racial composition in each zip code
    :param arrest_charge: The arrest for which race vs arrest has to be calculated
    :param race: The race for which race vs arrest has to be calculated
    :return: Dataframe containing race vs arrest

    >>> test_arrest_data = arrest_clean('data/arrest_numba_zipcode.csv')
    >>> test_race_data = race_clean('data/LARace.csv')
    >>> test_data = race_vs_arrest(test_arrest_data, test_race_data, 'Homicide', 'Black or African American Alone')
    >>> test_data.shape
    (68, 3)
    >>> test_data.columns.to_list()
    ['Zip Code', 'Homicide Arrests per 100k', 'Black or African American Alone Percent']

    """
    single_arrest_data = pd.DataFrame(arrest_data[arrest_data['Charge Group Description'] == arrest_charge].groupby(['ZipCode', 'Year']).size(), columns=[f'{arrest_charge} Arrests']).reset_index()
    single_arrest_data = pd.DataFrame(
        single_arrest_data.groupby('ZipCode')[f'{arrest_charge} Arrests'].sum() / single_arrest_data.groupby('ZipCode')['Year'].count(),
        columns=[f'{arrest_charge} Arrests per Year'])
    race_single_arrest_data = race_data.merge(single_arrest_data, how='left', left_on='Zip Code', right_on='ZipCode').dropna(
        subset=[f'{arrest_charge} Arrests per Year'])
    race_single_arrest_data [f'{race} Percent'] = (race_single_arrest_data [race] / race_single_arrest_data ['Total Population']) * 100
    race_single_arrest_data[f'{arrest_charge} Arrests per 100k'] = (race_single_arrest_data [f'{arrest_charge} Arrests per Year'] / race_single_arrest_data ['Total Population']) * 100000
    return race_single_arrest_data[['Zip Code', f'{arrest_charge} Arrests per 100k', f'{race} Percent']]


def income_vs_crime(crime_data: pd.DataFrame, income_data: pd.DataFrame, race_data: pd.DataFrame) -> pd.DataFrame:
    """
    Function to create dataframe for income vs crime rate (per 1k) per year for every zip code
    :param crime_data: Data about crimes
    :param income_data: Data about median household income for every zip code
    :param race_data: Data about racial composition of each zip code
    :return: Dataframe containing income vs crime rate (per 1k) per year

    >>> test_crime_data = crime_clean('data/crime_numba_zipcode.csv')
    >>> test_income_data = income_clean('data/LAIncome.csv')
    >>> test_race_data = race_clean('data/LARace.csv')
    >>> test_data = income_vs_crime(test_crime_data, test_income_data, test_race_data)
    >>> test_data.shape
    (72, 3)
    >>> test_data.columns.to_list()
    ['Crime Rate per 1k', 'Zip', 'Amount']

    """
    crime_zip = pd.DataFrame(crime_data.groupby(['ZipCode', 'Year']).size(), columns=['Crime']).reset_index()
    crime_zip_all = pd.DataFrame(
        crime_zip.groupby('ZipCode')['Crime'].sum() / crime_zip.groupby('ZipCode')['Year'].count(),
        columns=['Total Crime per Year']).reset_index()
    crime_zip_all = crime_zip_all.merge(race_data, left_on='ZipCode', right_on='Zip Code')[['ZipCode', 'Total Crime per Year', 'Total Population']]
    crime_zip_all['Crime Rate per 1k'] = (crime_zip_all['Total Crime per Year'] / crime_zip_all['Total Population']) * 1000
    crime_income = crime_zip_all.merge(income_data, left_on='ZipCode', right_on='Zip').drop(['ZipCode', 'Total Crime per Year', 'Total Population'], axis=1)
    return crime_income

