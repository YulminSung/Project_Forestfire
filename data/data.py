# -*- coding:utf-8 -*-
# 전체 데이터 로드
import streamlit as st
from google.cloud import bigquery
from utils import credentials

@st.cache_data(ttl=600)
def load_data():
    # 빅쿼리 클라이언트 객체 생성
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)

    # 프로젝트 ID 설정
    project_id = 'forestfire-389107'

    # 모든 데이터셋 조회
    datasets = client.list_datasets(project=project_id)

    # 결과를 저장할 딕셔너리 초기화
    results  = []
    # 데이터셋 반복문 실행
    for dataset in datasets:
        dataset_id = dataset.dataset_id

        # 테이블 목록 조회
        tables = client.list_tables(dataset.reference)

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
            results.append({
                'dataset_id': dataset_id,
                'table_id': table_id,
                'dataframe': result
            })

    return results

def run_dataload():
    results = load_data()
    if len(results) > 0:
        for table in results:
            dataset_id = table['dataset_id']
            table_id = table['table_id']
            dataframe = table['dataframe']

            st.write(f"Dataset: {dataset_id}, Table: {table_id}")
            st.dataframe(dataframe.head())
            st.markdown("\n")
    else:
        st.write("No tables found in the project.")

# Streamlit 애플리케이션 실행
if __name__ == '__main__':
    run_dataload()