# -*- coding: utf-8 -*-
import streamlit as st
from google.cloud import bigquery
from utils import credentials

@st.cache_data(ttl=600)
def map_loadData():
    # 빅쿼리 클라이언트 객체 생성
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)

    # 쿼리 작성
    query = """
     SELECT *
     FROM `forestfire-389107.PreProcessing_Data.forestfire_occurs`
     """
    # 쿼리 실행 및 결과를 데이터프레임으로 변환
    forestfire_occurs = client.query(query).to_dataframe()
    forestfire_occurs = forestfire_occurs.dropna()
    forestfire_occurs = forestfire_occurs[~forestfire_occurs['adres'].str.contains("신북면 발산리")]

    # 쿼리 작성
    query1 = """
     SELECT *
     FROM `forestfire-389107.Raw_Data.weather_stations`
     """
    # 쿼리 실행 및 결과를 데이터프레임으로 변환
    weather_stations = client.query(query1).to_dataframe()
    weather_stations = weather_stations[
        weather_stations["stnAddress"].str.contains("강원도") & weather_stations["endDate"].isna()]
    weather_stations = weather_stations.reset_index(drop=True)

    # 쿼리 작성
    query2 = """
      SELECT *
      FROM `forestfire-389107.Raw_Data.gangwon_code`
      """
    # 쿼리 실행 및 결과를 데이터프레임으로 변환
    gangwon_code = client.query(query2).to_dataframe()
    gangwon_code["code"] = gangwon_code["code"].astype(str).str[:-2]
    gangwon_code['code'] = gangwon_code['code'].drop_duplicates()
    gangwon_code = gangwon_code[~gangwon_code["code"].isna()].rename(columns={"code": "EMD_CD"})

    # 쿼리 작성
    query3 = """
      SELECT *
      FROM `forestfire-389107.Raw_Data.gangwon_UMD`
      """
    # 쿼리 실행 및 결과를 데이터프레임으로 변환
    gangwon_UMD = client.query(query3).to_dataframe()

    return forestfire_occurs, weather_stations, gangwon_code, gangwon_UMD

if __name__ == "__main__":
    map_loadData()