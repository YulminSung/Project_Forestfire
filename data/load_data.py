# -*- coding: utf-8 -*-
import streamlit as st

from utils import credentials
import geopandas as gpd
from shapely import wkt
from google.cloud import bigquery

def get_dataframe_from_bigquery(dataset_id, table_id):

    # BigQuery 클라이언트 생성
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)

    # 테이블 레퍼런스 생성
    table_ref = client.dataset(dataset_id).table(table_id)

    # 테이블 데이터를 DataFrame으로 변환
    df = client.list_rows(table_ref).to_dataframe()

    return df


def get_geodataframe_from_bigquery(dataset_id, table_id):

    # 빅쿼리 클라이언트 객체 생성
    client = bigquery.Client(credentials=credentials)

    # 쿼리 작성
    query = f"""
            SELECT *
            FROM `forestfire-389107.{dataset_id}.{table_id}`
            """

    # 쿼리 실행
    df = client.query(query).to_dataframe()

    # 'geometry' 열의 문자열을 다각형 객체로 변환
    df['geometry'] = df['geometry'].apply(wkt.loads)

    # GeoDataFrame으로 변환
    gdf = gpd.GeoDataFrame(df, geometry='geometry')
    gdf.crs = "EPSG:4326"

    return gdf

def load_data():
    # weather_stations = get_dataframe_from_bigquery("Raw_Data", "weather_stations").sort_values(["stnId"])
    # weather_days = get_dataframe_from_bigquery("Raw_Data", "weather_days").sort_values(["stnId", "tm"])
    forestfire_occurs = get_dataframe_from_bigquery("Raw_Data", "forestfire_occurs").sort_values(["objt_id", "occu_date"])
    # forestfire_occurs_add = get_dataframe_from_bigquery("Raw_Data", "forestfire_occurs_add").sort_values(["objt_id", "occu_date"])
    # gangwon_SGG = get_geodataframe_from_bigquery("Raw_Data", "gangwon_SGG").sort_values(["ADM_SECT_C", "SGG_NM"])
    gangwon_UMD = get_geodataframe_from_bigquery("Raw_Data", "gangwon_UMD").sort_values(["EMD_CD"])
    gangwon_code = get_dataframe_from_bigquery("Raw_Data", "gangwon_code").sort_values(["code"])

    pre_forestfire_occurs = get_dataframe_from_bigquery("PreProcessing_Data", "forestfire_occurs").sort_values(["objt_id", "occu_date"])
    pre_weather_days = get_dataframe_from_bigquery("PreProcessing_Data", "weather_days").sort_values(["stnId", "tm"])

    return forestfire_occurs, gangwon_UMD, gangwon_code, pre_forestfire_occurs, pre_weather_days

if __name__ == '__main__':
    load_data()
