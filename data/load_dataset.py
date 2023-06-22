# -*- coding:utf-8 -*-
# 전체 데이터 로드
import streamlit as st
from google.cloud import bigquery
from utils import credentials

@st.cache_data(ttl=600)
def load_analysis(table_id=None):
    # 빅쿼리 클라이언트 객체 생성
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)

    # 프로젝트 ID 설정
    project_id = 'forestfire-389107'
    dataset_id = 'Analysis_Data'

    # 테이블을 담을 빈 리스트
    load_analysis = []
    # 테이블 목록 조회
    tables = client.list_tables(f"{project_id}.{dataset_id}")
    # 테이블 반복문 실행
    for table in tables:
        table_id = table.table_id

        # 쿼리 작성
        query = f"""
        SELECT *
        FROM `{project_id}.{dataset_id}.{table_id}`
        """

        # 쿼리 실행 및 결과를 데이터프레임으로 변환
        result = client.query(query).to_dataframe()

        # 결과를 리스트에 추가
        load_analysis.append({
            'dataframe': result
        })
    return load_analysis


# Streamlit 애플리케이션 실행
if __name__ == '__main__':
    load_analysis()