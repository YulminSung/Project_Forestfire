# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import geopandas as gpd
import pandas_gbq
import json
from shapely.geometry import Point, Polygon, MultiPolygon, shape
from shapely import wkt
import googlemaps
from google.cloud import bigquery
from google.oauth2 import service_account
from PIL import Image

import warnings
warnings.filterwarnings("ignore")

KEY_PATH = ".config/"

key_path = KEY_PATH + "fireforest-2023-9fb91d08cec6.json"
servicekey_path = KEY_PATH + "serviceKey.json"


def get_service_key(servicekey_path, key_name):
    """
    주어진 서비스 키 파일에서 지정된 키 이름에 해당하는 서비스 키를 반환합니다.

    Args:
        servicekey_path (str): 서비스 키 파일의 경로.
        key_name (str): 반환할 서비스 키의 이름.

    Returns:
        str or None: 지정된 키 이름에 해당하는 서비스 키. 키를 찾을 수 없는 경우 None을 반환합니다.
    """

    with open(servicekey_path) as f:
        data = json.load(f)
        service_key = data.get(key_name)
    return service_key

def get_dataframe_from_bigquery(dataset_id, table_id, key_path):
    """
    주어진 BigQuery 테이블에서 데이터를 조회하여 DataFrame으로 반환합니다.

    Args:
        dataset_id (str): 대상 데이터셋의 ID.
        table_id (str): 대상 테이블의 ID.
        key_path (str): 서비스 계정 키 파일의 경로.

    Returns:
        pandas.DataFrame: 조회된 데이터를 담은 DataFrame 객체.
    """

    # Credentials 객체 생성
    credentials = service_account.Credentials.from_service_account_file(key_path)

    # BigQuery 클라이언트 생성
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)

    # 테이블 레퍼런스 생성
    table_ref = client.dataset(dataset_id).table(table_id)

    # 테이블 데이터를 DataFrame으로 변환
    df = client.list_rows(table_ref).to_dataframe()

    return df


def get_geodataframe_from_bigquery(dataset_id, table_id, key_path):
    """
    주어진 BigQuery 테이블에서 데이터를 조회하여 Geopandas GeoDataFrame으로 반환합니다.

    Args:
        dataset_id (str): 대상 데이터셋의 ID.
        table_id (str): 대상 테이블의 ID.
        key_path (str): 서비스 계정 키 파일의 경로.

    Returns:
        geopandas.GeoDataFrame: 조회된 데이터를 담은 Geopandas GeoDataFrame 객체.
    """

    # Credentials 객체 생성
    credentials = service_account.Credentials.from_service_account_file(key_path)

    # 빅쿼리 클라이언트 객체 생성
    client = bigquery.Client(credentials=credentials)

    # 쿼리 작성
    query = f"SELECT * FROM `{dataset_id}.{table_id}`"

    # 쿼리 실행
    df = client.query(query).to_dataframe()

    # 'geometry' 열의 문자열을 다각형 객체로 변환
    df['geometry'] = df['geometry'].apply(wkt.loads)

    # GeoDataFrame으로 변환
    gdf = gpd.GeoDataFrame(df, geometry='geometry')
    gdf.crs = "EPSG:4326"

    return gdf


def load_data(type):
    if type == "RAW_DATA":
        # BigQuery 에 RAW_DATA Load
        weather_stations = get_dataframe_from_bigquery("RAW_DATA", "weather_stations", key_path).sort_values(["stnId"])
        weather_days = get_dataframe_from_bigquery("RAW_DATA", "weather_days", key_path).sort_values(["stnId", "tm"])
        forestfire_occurs = get_dataframe_from_bigquery("RAW_DATA", "forestfire_occurs", key_path).sort_values(["objt_id", "occu_date"])
        forestfire_occurs_add = get_dataframe_from_bigquery("RAW_DATA", "forestfire_occurs_add", key_path).sort_values(["objt_id", "occu_date"])
        gangwon_code = get_dataframe_from_bigquery("RAW_DATA", "gangwon_code", key_path).sort_values(["code"])
        gangwon_SGG = get_geodataframe_from_bigquery("RAW_DATA", "gangwon_SGG", key_path).sort_values(["ADM_SECT_C", "SGG_NM"])
        gangwon_UMD = get_geodataframe_from_bigquery("RAW_DATA", "gangwon_UMD", key_path).sort_values(["EMD_CD"])

        return weather_stations, weather_days, forestfire_occurs, forestfire_occurs_add, gangwon_code, gangwon_SGG, gangwon_UMD

    elif type == "PREPROCESSING_DATA":
        # BigQuery 에 PREPROCESSING_DATA Load
        weather_stations = get_dataframe_from_bigquery("PREPROCESSING_DATA", "weather_stations", key_path).sort_values(["stnId"])
        weather_days = get_dataframe_from_bigquery("PREPROCESSING_DATA", "weather_days", key_path).sort_values(["stnId", "tm"])
        forestfire_occurs = get_dataframe_from_bigquery("PREPROCESSING_DATA", "forestfire_occurs", key_path).sort_values(["objt_id", "occu_date"])
        gangwon_regions = get_geodataframe_from_bigquery("PREPROCESSING_DATA", "gangwon_regions", key_path)

        return weather_stations, weather_days, forestfire_occurs, gangwon_regions

    elif type == "ANALSIS_DATA":
        ANALSIS_DATA = get_dataframe_from_bigquery("ANALSIS_DATA", "ANALSIS_DATA", key_path).sort_values(["tm"]).reset_index(drop=True)
        data_1 = get_dataframe_from_bigquery("ANALSIS_DATA", "GangwonNorthInland", key_path).sort_values(["tm"]).reset_index(drop=True)
        data_2 = get_dataframe_from_bigquery("ANALSIS_DATA", "GangwonNorthMount", key_path).sort_values(["tm"]).reset_index(drop=True)
        data_3 = get_dataframe_from_bigquery("ANALSIS_DATA", "GangwonNorthCoast", key_path).sort_values(["tm"]).reset_index(drop=True)
        data_4 = get_dataframe_from_bigquery("ANALSIS_DATA", "GangwonCentralInland", key_path).sort_values(["tm"]).reset_index(drop=True)
        data_5 = get_dataframe_from_bigquery("ANALSIS_DATA", "GangwonCentralMount", key_path).sort_values(["tm"]).reset_index(drop=True)
        data_6 = get_dataframe_from_bigquery("ANALSIS_DATA", "GangwonCentralCoast", key_path).sort_values(["tm"]).reset_index(drop=True)
        data_7 = get_dataframe_from_bigquery("ANALSIS_DATA", "GangwonSouthInland", key_path).sort_values(["tm"]).reset_index(drop=True)
        data_8 = get_dataframe_from_bigquery("ANALSIS_DATA", "GangwonSouthMount", key_path).sort_values(["tm"]).reset_index(drop=True)
        data_9 = get_dataframe_from_bigquery("ANALSIS_DATA", "GangwonSouthInland", key_path).sort_values(["tm"]).reset_index(drop=True)

        ANALSIS_DATA = ANALSIS_DATA[ANALSIS_DATA['tm'] < '2023-01-01']
        data_1 = data_1[data_1['tm'] < '2023-01-01']
        data_2 = data_2[data_2['tm'] < '2023-01-01']
        data_3 = data_3[data_3['tm'] < '2023-01-01']
        data_4 = data_4[data_4['tm'] < '2023-01-01']
        data_5 = data_5[data_5['tm'] < '2023-01-01']
        data_6 = data_6[data_6['tm'] < '2023-01-01']
        data_7 = data_7[data_7['tm'] < '2023-01-01']
        data_8 = data_8[data_8['tm'] < '2023-01-01']
        data_9 = data_9[data_9['tm'] < '2023-01-01']

        return ANALSIS_DATA, data_1, data_2, data_3, data_4, data_5, data_6, data_7, data_8, data_9