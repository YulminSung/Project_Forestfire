# -*- coding: utf-8 -*-
import pandas as pd
import streamlit as st
from google.cloud import bigquery
from utils import credentials

# 빅쿼리 클라이언트 객체 생성
client = bigquery.Client(credentials=credentials, project=credentials.project_id)
def run_appendix():
    tab1, tab2 = st.tabs(["✅ Codebook", "✅ 부록"])
    with tab1:
        """
           Display the dataframe, data types, and describe statistics in a Streamlit-style format.
    
           :param dataframe: The input dataframe.
           :return: None
        """
        st.subheader("Select to Data Set")
        # 데이터셋 목록 가져오기
        datasets = list(client.list_datasets())
        # 데이터셋 목록을 담을 빈 리스트
        dataset_list = []
        # 각 데이터셋에 대해 데이터셋 ID를 가져와 리스트에 추가
        for dataset in datasets:
            dataset_list.append(dataset.dataset_id)

        dataset_list = st.selectbox("DateSet", ('Analysis_Data', 'PreProcessing_Data', 'Raw_Data'),
                                    label_visibility='collapsed')  # 원하는 데이터셋 ID로 변경
        # 특정 데이터셋의 테이블 목록 조회
        st.subheader("Select to Data Table")
        dataset_id = dataset_list
        tables = list(client.list_tables(dataset_id))
        datatable_list = []
        for table in tables:
            datatable_list.append(table.table_id)
        df_tables = pd.DataFrame({"Table List": datatable_list})
        tablenames = st.selectbox("DataTable", df_tables, label_visibility='collapsed')
        if dataset_id == 'Analysis_Data':
            datasetimg = 'A'
        elif dataset_id == 'PreProcessing_Data':
            datasetimg = 'P'
        else:
            datasetimg = 'R'
        st.image(f"img/codebook/{datasetimg}_{tablenames}.png")

    with tab2:
        option = st.selectbox(
            "#### 첨부 목록",
            ('첨부1 : 코드 목록', '첨부2 : 지점 번호', '첨부3 : 뭐 이런것들?'))
        if option == '첨부2 : 지점 번호':
            st.image("img/WSN.png")
        else:
            pass

if __name__ == '__main__':
    run_appendix()