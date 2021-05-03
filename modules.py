import numpy as np
import pandas as pd
import json
import plotly.express as px
pd.options.plotting.backend = "plotly"
from numba import jit

def convert_lat_lon(x:str) -> tuple:
    return float(eval(x)['latitude']), float(eval(x)['longitude'])


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