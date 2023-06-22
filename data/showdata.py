# -*- coding: utf-8 -*-
import pandas as pd
import streamlit as st
from google.cloud import bigquery
from streamlit_pandas_profiling import st_profile_report

from data.query import run_query
from utils import credentials

# 빅쿼리 클라이언트 객체 생성
client = bigquery.Client(credentials=credentials, project=credentials.project_id)

def run_show_data():
    tab1, tab2 = st.tabs(["✅Data List", "✅Show Data"])
    with tab1:
        # 빅쿼리 클라이언트 객체 생성
        client = bigquery.Client(credentials=credentials, project=credentials.project_id)
        # 데이터셋 목록 조회
        st.header("Data Set List")
        # 데이터셋 목록 가져오기
        datasets = list(client.list_datasets())
        # 데이터셋 목록을 담을 빈 리스트
        dataset_list = []
        # 각 데이터셋에 대해 데이터셋 ID를 가져와 리스트에 추가
        for dataset in datasets:
            dataset_list.append(dataset.dataset_id)
        df_datasets = pd.DataFrame({"Data Set List": dataset_list})
        st.dataframe(df_datasets)

        # 특정 데이터셋의 테이블 목록 조회
        st.subheader("DataTable List")
        dataset_list = st.selectbox("Select Date Set",
                                    ('Analysis_Data', 'PreProcessing_Data', 'Raw_Data'))  # 원하는 데이터셋 ID로 변경
        if dataset_list:
            dataset_id = dataset_list
            tables = list(client.list_tables(dataset_id))
            datatable_list = []
            for table in tables:
                datatable_list.append(table.table_id)
            df_tables = pd.DataFrame({"Table List": datatable_list})
            st.dataframe(df_tables)
    with tab2:
        """
           Display the dataframe, data types, and describe statistics in a Streamlit-style format.
    
           :param dataframe: The input dataframe.
           :return: None
        """
        st.markdown("**Data Set List**")
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
        st.markdown("**Data Table List**")
        dataset_id = dataset_list
        tables = list(client.list_tables(dataset_id))
        datatable_list = []
        for table in tables:
            datatable_list.append(table.table_id)
        df_tables = pd.DataFrame({"Table List": datatable_list})
        tablenames = st.selectbox("DataTable", df_tables, label_visibility='collapsed')

        tab1, tab2 = st.tabs(["🗃️Data Preview", "✅View Columns"])
        with tab1:
            if dataset_list =='Analysis_Data':
                st.markdown("#### 🗃️ Analysis Data Set : 분석을 위한 전처리 데이터")
                st.markdown("- 강원도 각 지역의 :red[**산불발생여부**] 및 **기상 데이터** 를 포함 \n"
                            "- 기상 데이터에는 **기온, 습도, 바람, 강수** 에 대한 내용 \n"
                            "- 또한 각 지역은 9개 구역으로 나누어져 있음 \n"
                            "- 9개 구역 \n"
                            "   + 강원 중부 해안 : 강릉시 \n"
                            "   + 강원 중부 내륙 : 춘천시, 홍천군(~내면) \n"
                            "   + 강원 중부 산지 : 홍천군(내면), 평창군(대관령면, 진부면) \n"
                            "   + 강원 북부 해안 : 고성군, 속초시, 양양군 \n"
                            "   + 강원 북부 내륙 : 철원군, 화천군 \n"
                            "   + 강원 북부 산지 : 양구군, 인제군 \n"
                            "   + 강원 남부 해안 : 동해시, 삼척시, 태백시 \n"
                            "   + 강원 남부 내륙 : 원주시, 횡성군 \n"
                            "   + 강원 남부 산지 : 열월군, 정선군, 평창군(~대관령면, ~진부면) \n"
                            "")
            elif dataset_list =='PreProcessing_Data':
                st.markdown("#### 🗃️ PreProcessing_Data Set : 기초 전처리 데이터")
                st.markdown("- **forestfire_occurs** : 산불 발생 이력 \n"
                            "- **weather_days** : 일간 기상 자료 \n"
                            "- **weather_stations** : 기상 관측 지점 자료 \n")
            elif dataset_list =='Raw_Data':
                st.markdown("#### 🗃️ Raw_Data Set : Open API를 통해 수집한 공공 데이터")
                st.markdown("- **데이터 출처** : 산림청, 기상청, 국토교통부, 행정안전부 \n")

            col1, col2 = st.columns([3, 2])
            with col1:
                st.subheader("📣 Data")
                if tablenames:
                    table_id = tablenames
                    query = f"""
                        SELECT *
                        FROM `forestfire-389107.{dataset_id}.{table_id}`
                        """
                    # 쿼리 실행 및 결과를 데이터프레임으로 변환
                    combined_df = client.query(query).to_dataframe()
                    # 데이터프레임 출력
                    st.dataframe(combined_df)
                    # IMPORTANT: Cache the conversion to prevent computation on every rerun
                    csv = combined_df.to_csv().encode('cp949')
                    st.download_button(
                        label="Download data as CSV",
                        data=csv,
                        file_name=f'{tablenames}.csv',
                        mime='text/csv')
                with st.expander("Report"):
                    pr = combined_df.profile_report()
                    st_profile_report(pr)

            with col2:
                st.subheader("📣 Describe")

                st.dataframe(combined_df.describe(), height=350, width=650)
                st.write("*Appendix 메뉴의 Codebook 참고")
        with tab2:
            if tablenames:
                dataset_id = dataset_list
                query = f"""
                    SELECT STRING_AGG(column_name)
                    FROM `forestfire-389107.{dataset_id}.INFORMATION_SCHEMA.COLUMNS`
                    group by table_name
                    """
                df = client.query(query).to_dataframe()
                all_cols = df.values[0][0].split(",")
                st.markdown("**Select Columns**")
                columns = st.multiselect("컬럼명 선택", all_cols, default=all_cols, label_visibility='collapsed')
                temp_Strings = ", ".join(columns)
                run_query(temp_Strings, dataset_id, tablenames)
            else :
                st.warning("error")

if __name__ == "__main__":
    run_show_data()