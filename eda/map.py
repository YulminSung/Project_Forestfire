# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import geopandas as gpd
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

import folium
from streamlit_folium import st_folium
from data.load_data import load_data

def run_feature():
    forestfire_occurs, gangwon_UMD, gangwon_code, pre_forestfire_occurs = load_data()

    gangwon_code["code"] = gangwon_code["code"].astype(str).str[:-2]
    gangwon_code['code'] = gangwon_code['code'].drop_duplicates()
    gangwon_code = gangwon_code[~gangwon_code["code"].isna()].rename(columns={"code": "EMD_CD"})

    # 강원_UMD와 강원_code를 병합한 데이터프레임 생성
    gangwon_sample = pd.merge(gangwon_UMD, gangwon_code, on="EMD_CD")

    # 지도 시각화 feature 전처리
    w_regions = {
        'Region': ['강원북부내륙', '강원중부내륙', '강원남부내륙', '강원북부산지', '강원중부산지', '강원남부산지', '강원북부해안', '강원중부해안', '강원남부해안'],
        'Geometry': [
            gangwon_sample[
                (gangwon_sample["address"].str.contains("철원군")) | (gangwon_sample["address"].str.contains("화천군"))][
                'geometry'].unary_union,
            gangwon_sample[(gangwon_sample["address"].str.contains("춘천시")) | (
                    gangwon_sample["address"].str.contains("홍천군") & ~gangwon_sample["address"].str.contains("내면"))][
                'geometry'].unary_union,
            gangwon_sample[
                (gangwon_sample["address"].str.contains("원주시")) | (gangwon_sample["address"].str.contains("횡성군"))][
                'geometry'].unary_union,
            gangwon_sample[
                (gangwon_sample["address"].str.contains("양구군")) | (gangwon_sample["address"].str.contains("인제군"))][
                'geometry'].unary_union,
            gangwon_sample[
                (gangwon_sample["address"].str.contains("홍천군") & gangwon_sample["address"].str.contains("내면")) | (
                        gangwon_sample["address"].str.contains("평창군") & gangwon_sample["address"].str.contains(
                    "대관령면")) | (
                        gangwon_sample["address"].str.contains("평창군") & gangwon_sample["address"].str.contains(
                    "진부면"))]['geometry'].unary_union,
            gangwon_sample[
                (gangwon_sample["address"].str.contains("영월군")) | (gangwon_sample["address"].str.contains("정선군")) | (
                        gangwon_sample["address"].str.contains("평창군") & ~gangwon_sample["address"].str.contains(
                    "대관령면") & ~gangwon_sample["address"].str.contains("진부면"))]['geometry'].unary_union,
            gangwon_sample[
                (gangwon_sample["address"].str.contains("고성군")) | (gangwon_sample["address"].str.contains("속초시")) | (
                    gangwon_sample["address"].str.contains("양양군"))]['geometry'].unary_union,
            gangwon_sample[gangwon_sample["address"].str.contains("강릉시")]['geometry'].unary_union,
            gangwon_sample[
                (gangwon_sample["address"].str.contains("동해시")) | (gangwon_sample["address"].str.contains("삼척시")) | (
                    gangwon_sample["address"].str.contains("태백시"))]['geometry'].unary_union
        ]
    }

    # 피해 건수 지도시각화
    gdf = gpd.GeoDataFrame(w_regions, geometry='Geometry')

    return pre_forestfire_occurs, gdf

def run_count():
    st.subheader("강원도 산불 피해 건수")
    pre_forestfire_occurs, gdf = run_feature()
    empty, col, empty = st.columns([1, 5, 1])
    with col:
        # w_regions별 value_counts 계산
        region_counts = pre_forestfire_occurs['w_regions'].value_counts().reset_index()
        region_counts.columns = ['w_regions', 'Counts']

        # 데이터프레임 생성
        region_counts_df = pd.DataFrame(region_counts)

        # 데이터프레임 생성
        FireCounts = pd.DataFrame({'Region': region_counts_df['w_regions'],
                                   'Fire_Counts': region_counts_df['Counts']})

        merged_Count = gdf.merge(FireCounts, on='Region', how='left')

        merged_Count.crs = "EPSG:4326"

        # 지도 생성
        map = folium.Map(location=[37.5, 128], zoom_start=8)

        # GeoDataFrame 생성
        Count_gdf = gpd.GeoDataFrame(merged_Count, geometry='Geometry')

        # Choropleth 맵 생성
        folium.Choropleth(
            geo_data=Count_gdf,
            data=Count_gdf,
            columns=['Region', 'Fire_Counts'],
            key_on='feature.properties.Region',
            fill_color='YlOrRd',
            fill_opacity=0.7,
            line_opacity=0.4,
            line_color='black',  # 폴리곤 테두리 선 색상
            line_weight=3,  # 폴리곤 테두리 선 두께
            line_dash='5, 5',  # 폴리곤 테두리 선 스타일
            legend_name='Fire Counts',
            highlight=True,
            highlight_function=lambda x: {'weight': 3}  # 하이라이트 스타일
        ).add_to(map)

        # 지도 출력
        st_folium(map)


def run_money():
    st.subheader("강원도 산불 피해 금액")
    empty, col, empty = st.columns([1,5,1])
    with col:
        pre_forestfire_occurs, gdf = run_feature()

        visual_feature = pre_forestfire_occurs[["ar", "amount", "latitude", "longitude", "w_regions"]].groupby(
            ["w_regions"]).agg({
            "ar": lambda x: x.astype(float).sum(),
            "amount": lambda x: x.astype(float).sum(),
            "latitude": "mean",
            "longitude": "mean"
        }).reset_index()

        # 데이터프레임 생성
        Damage_Amount = pd.DataFrame({'Region': visual_feature['w_regions'],
                                      'Amount': visual_feature['amount']})

        merged_Amount = gdf.merge(Damage_Amount, on='Region', how='left')

        # 표현할 좌표계 설정
        merged_Amount.crs = "EPSG:4326"

        # 지도 생성
        map = folium.Map(location=[37.5, 128], zoom_start=7)

        # GeoDataFrame 생성
        Amount_gdf = gpd.GeoDataFrame(merged_Amount, geometry='Geometry')

        # Choropleth 맵 생성
        folium.Choropleth(
            geo_data=Amount_gdf,
            data=Amount_gdf,
            columns=['Region', 'Amount'],
            key_on='feature.properties.Region',
            fill_color='YlOrRd',
            fill_opacity=0.7,
            line_opacity=0.4,
            line_color='black',  # 폴리곤 테두리 선 색상
            line_weight=3,  # 폴리곤 테두리 선 두께
            line_dash='5, 5',  # 폴리곤 테두리 선 스타일
            legend_name='Amount',
            highlight=True,
            highlight_function=lambda x: {'weight': 3}  # 하이라이트 스타일
        ).add_to(map)

        # 지도 출력
        st_folium(map)

def run_arrange():
    st.subheader("강원도 산불 피해 범위")
    empty, col, empty = st.columns([1,5,1])
    with col:
        pre_forestfire_occurs, gdf = run_feature()

        visual_feature = pre_forestfire_occurs[["ar", "amount", "latitude", "longitude", "w_regions"]].groupby(
            ["w_regions"]).agg({
            "ar": lambda x: x.astype(float).sum(),
            "amount": lambda x: x.astype(float).sum(),
            "latitude": "mean",
            "longitude": "mean"
        }).reset_index()

        # 데이터프레임 생성
        Damage_Area = pd.DataFrame({'Region': visual_feature['w_regions'],
                                    'DamageArea': visual_feature['ar']})

        merged_Area = gdf.merge(Damage_Area, on='Region', how='left')

        # 표현할 좌표계 설정
        merged_Area.crs = "EPSG:4326"

        # 지도 생성
        map = folium.Map(location=[37.5, 128], zoom_start=7)

        # GeoDataFrame 생성
        Area_gdf = gpd.GeoDataFrame(merged_Area, geometry='Geometry')

        # Choropleth 맵 생성
        folium.Choropleth(
            geo_data=Area_gdf,
            data=Area_gdf,
            columns=['Region', 'DamageArea'],
            key_on='feature.properties.Region',
            fill_color='YlOrRd',
            fill_opacity=0.7,
            line_opacity=0.4,
            line_color='black',  # 폴리곤 테두리 선 색상
            line_weight=3,  # 폴리곤 테두리 선 두께
            line_dash='5, 5',  # 폴리곤 테두리 선 스타일
            legend_name='DamageArea',
            highlight=True,
            highlight_function=lambda x: {'weight': 3}  # 하이라이트 스타일
        ).add_to(map)

        # 지도 출력
        st_folium(map)

def run_point():
    pass
    # pre_forestfire_occurs, gdf = run_feature()
    # # 지도 생성
    # map = folium.Map(location=[37.55, 128], zoom_start=8)
    #
    # # 마커 그룹화
    # # marker_cluster = MarkerCluster().add_to(map)
    #
    # # 데이터프레임의 각 행을 반복하며 마커 추가
    # for index, row in pre_forestfire_occurs.iterrows():
    #     popup = folium.Popup(row['adres'], max_width=300)
    #     folium.CircleMarker(
    #         location=[row['latitude'], row['longitude']],
    #         radius=4,
    #         popup=popup,
    #         icon=folium.Icon(color='red', icon='info-sign'),
    #         color='red'
    #     ).add_to(map)
    #
    # region_colors = {
    #     '강원북부내륙': 'blue',
    #     '강원중부내륙': 'brown',
    #     '강원남부내륙': 'green',
    #     '강원북부산지': 'orange',
    #     '강원중부산지': 'purple',
    #     '강원남부산지': 'black',
    #     '강원북부해안': 'gray',
    #     '강원중부해안': 'red',
    #     '강원남부해안': 'magenta'
    # }
    #
    # # Add the regions to the map with different colors
    # folium.GeoJson('강원북부내륙',
    #                style_function=lambda feature: {'fillColor': region_colors['강원북부내륙'], 'color': 'blue'}).add_to(map)
    # folium.GeoJson('강원중부내륙',
    #                style_function=lambda feature: {'fillColor': region_colors['강원중부내륙'], 'color': 'brown'}).add_to(map)
    # folium.GeoJson('강원남부내륙',
    #                style_function=lambda feature: {'fillColor': region_colors['강원남부내륙'], 'color': 'green'}).add_to(map)
    # folium.GeoJson('강원북부해안',
    #                style_function=lambda feature: {'fillColor': region_colors['강원북부해안'], 'color': 'gray'}).add_to(map)
    # folium.GeoJson('강원중부해안',
    #                style_function=lambda feature: {'fillColor': region_colors['강원중부해안'], 'color': 'red'}).add_to(map)
    # folium.GeoJson('강원남부해안',
    #                style_function=lambda feature: {'fillColor': region_colors['강원남부해안'], 'color': 'magenta'}).add_to(
    #     map)
    # folium.GeoJson('강원남부산지',
    #                style_function=lambda feature: {'fillColor': region_colors['강원남부산지'], 'color': 'black'}).add_to(map)
    # folium.GeoJson('강원북부산지',
    #                style_function=lambda feature: {'fillColor': region_colors['강원북부산지'], 'color': 'orange'}).add_to(map)
    # folium.GeoJson('강원중부산지',
    #                style_function=lambda feature: {'fillColor': region_colors['강원중부산지'], 'color': 'purple'}).add_to(map)
    #
    # # 지도 표시
    # st_folium(map)

def run_map():
    tab1, tab2, tab3, tab4 = st.tabs(["산불 피해 건수", "산불 피해 범위", "산불 피해 금액", "산불 발생 위치"])
    with tab1:
        run_count()
    with tab2:
        run_arrange()
    with tab3:
        run_money()
    with tab4:
        run_point()


if __name__ == "__main__":
    run_map()