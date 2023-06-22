# -*- coding: utf-8 -*-
import streamlit as st
from google.cloud import bigquery
from utils import credentials

# 빅쿼리 클라이언트 객체 생성
client = bigquery.Client(credentials=credentials, project=credentials.project_id)
@st.cache_data(ttl=600)
def run_query(cols,dataset_id,table_id):
    st.subheader("Load Data")
    # 쿼리 작성
    sql = f"""
    SELECT {cols}
    FROM `forestfire-389107.{dataset_id}.{table_id}`
    """
    # 쿼리 실행 및 결과를 데이터프레임으로 변환
    df = client.query(sql).to_dataframe()
    # 데이터프레임 출력
    st.dataframe(df)

if __name__ == "__main__":
    run_query()