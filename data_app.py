# -*- coding:utf-8 -*-

import streamlit as st
import pandas as pd
import geopandas as gpd
import pandas_gbq
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
from matplotlib import font_manager as fm
import seaborn as sns
import plotly.express as px
import folium
from folium.plugins import MarkerCluster, HeatMap
from streamlit_folium import st_folium
from shapely.geometry import Point, Polygon, MultiPolygon, shape
from shapely import wkt
from PIL import Image

import utils
import home_app
import eda_app
import stat_app
import model_app
import service_app

import os
import warnings
warnings.filterwarnings("ignore")

def font_set():
    # matplotlib 한글 폰트 설정
    font_dirs = [os.getcwd() + '/nanum']
    font_files = fm.findSystemFonts(fontpaths=font_dirs)
    for font_file in font_files:
        fm.fontManager.addfont(font_file)
    fm._load_fontmanager(try_read_cache=False)

def create_choropleth_map(dataframe, geometry_column, value_column, legend_name):
    """
    GeoDataFrame을 기반으로 Choropleth 맵을 생성합니다.

    Args:
        dataframe (geopandas.GeoDataFrame): Choropleth 맵을 생성할 GeoDataFrame.
        geometry_column (str): 지오메트리 정보를 포함하는 열의 이름.
        value_column (str): 색상으로 표현할 값을 포함하는 열의 이름.
        legend_name (str): 범례의 이름.

    Returns:
        folium.Map: 생성된 Choropleth 맵 객체.
    """

    # 표현할 좌표계 설정
    dataframe.crs = "EPSG:4326"

    # 지도 생성
    map = folium.Map(location=[37.5, 128], zoom_start=7)

    # 테두리 선 스타일 함수
    def style_function(feature):
        return {
            'fillColor': 'YlOrRd',
            'fillOpacity': 0.7,
            'color': 'black',  # 테두리 선 색상
            'weight': 1,  # 테두리 선 두께
            'dashArray': '5, 5'  # 테두리 선 스타일
        }

    # Choropleth 맵 생성
    folium.Choropleth(
        geo_data=dataframe,
        data=dataframe,
        columns=[geometry_column, value_column],
        key_on='feature.properties.' + geometry_column,
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.4,
        line_color='black',  # 폴리곤 테두리 선 색상
        line_weight=3,  # 폴리곤 테두리 선 두께
        line_dash='5, 5',  # 폴리곤 테두리 선 스타일
        legend_name=legend_name,
        highlight=True,
        highlight_function=lambda x: {'weight': 3}  # 하이라이트 스타일
    ).add_to(map)

    st_folium(map)

def visualize_forestfire_by_region(dataframe, region_column, value_column, cmap_name, title):
    """
    지역별 특정 값에 따른 시각화를 수행합니다.

    Args:
        dataframe (pandas.DataFrame): 지역별 값 데이터가 포함된 DataFrame.
        region_column (str): 지역 정보가 포함된 열의 이름.
        value_column (str): 시각화할 값이 포함된 열의 이름.
        cmap_name (str): 색상 맵 이름.
        title (str): 시각화 제목.

    Returns:
        None
    """
    dataframe.crs = "EPSG:4326"

    # 색상 설정
    cmap = LinearSegmentedColormap.from_list(cmap_name, ['green', 'orange', 'darkred'])

    # 지도 그리기
    fig, ax = plt.subplots(figsize=(10, 12))
    dataframe.plot(column=value_column, cmap=cmap, linewidth=0.8, ax=ax, edgecolor='0.8')

    # 범례 설정
    sm = plt.cm.ScalarMappable(cmap=cmap)
    sm.set_array([])
    cbar = plt.colorbar(sm, **{'orientation': 'vertical', 'shrink': 0.6})  # cbar_kwargs를 사용하여 높이 조절

    # 축 제거
    ax.axis('off')

    # 제목 설정
    plt.title(title)

    # 시각화 출력
    st.pyplot(plt)

def plot_boxplot(data_frames, column_name, labels, colors, title, ylabel):
    """
    여러 데이터프레임의 특정 컬럼에 대한 boxplot을 그리는 함수입니다.

    Args:
        data_frames (list): 데이터프레임들의 리스트
        column_name (str): boxplot에 사용할 컬럼의 이름
        labels (list): 각 boxplot에 대한 레이블 리스트
        colors (list): 각 boxplot의 색상 리스트
        title (str): 그래프의 제목
        ylabel (str): y축 레이블

    Returns:
        None
    """

    plt.style.use('ggplot')
    plt.rcParams['figure.figsize'] = (10, 5)
    plt.rcParams['font.size'] = 12
    plt.rcParams['font.family'] = 'Malgun Gothic'
    plt.rcParams['axes.unicode_minus'] = False

    fig, ax = plt.subplots()

    box_width = 1.5
    median_color = 'red'

    for i, df in enumerate(data_frames):
        data = [df[column_name]]
        box = ax.boxplot(data, patch_artist=True, positions=[i*4+2], widths=box_width,
                         boxprops={'linewidth': 1.7, 'edgecolor': 'black'},
                         whiskerprops={'linewidth': 1.7})

        for patch, color in zip(box["boxes"], colors):
            patch.set_facecolor(color)

        for median in box["medians"]:
            median.set(color=median_color)

    ax.set_xticks([i*4+2 for i in range(len(data_frames))])

    if pd.Series(title).str.contains("기온").any():
        yticks = np.arange(-30, 50, 10)
    elif pd.Series(title).str.contains("습도").any():
        yticks = np.arange(10, 110, 10)
    elif pd.Series(title).str.contains("풍속").any():
        yticks = np.arange(0, 35, 5)
    else:
        yticks = None

    if yticks is not None:
        ax.set_yticks(yticks)

    legend_patches = [mpatches.Patch(color=color, label=label) for color, label in zip(colors, labels)]
    ax.legend(handles=legend_patches, loc='lower center', bbox_to_anchor=(0.5, -0.2),
              fontsize=8.5, ncol=len(data_frames))

    ax.set_xticklabels(["지역 " + str(i+1) for i in range(len(data_frames))])
    ax.set_title(title, fontweight='bold')
    ax.set_ylabel(ylabel)
    plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9)

    st.pyplot(plt)

def data_app():
    weather_stations, weather_days, forestfire_occurs, gangwon_regions = utils.load_data("PREPROCESSING_DATA")

    # visual_feature = forestfire_occurs[["w_regions", "ar", "amount", "latitude", "longitude"]].groupby(
    #     ["w_regions"]).agg({
    #     "ar": lambda x: x.astype(float).sum(),
    #     "amount": lambda x: x.astype(float).sum(),
    #     "latitude": "mean",
    #     "longitude": "mean"
    # }).reset_index()
    #
    # Damage_Amount = pd.DataFrame({'w_regions': visual_feature['w_regions'],
    #                               'Amount': visual_feature['amount']})
    #
    # merged_Amount = gangwon_regions.merge(Damage_Amount, on='w_regions', how='left')
    #
    # visualize_forestfire_by_region(merged_Amount, "w_regions", "Amount", "Amount_cmap", "Amount by Region")

    # w_regions별 value_counts 계산
    region_counts = forestfire_occurs['w_regions'].value_counts().reset_index()
    region_counts.columns = ['w_regions', 'Counts']

    # 데이터프레임 생성
    region_counts_df = pd.DataFrame({'w_regions': region_counts['w_regions'],
                                     'Fire_Counts': region_counts['Counts']})

    merged_Count = gangwon_regions.merge(region_counts_df, on='w_regions', how='left')

    create_choropleth_map(merged_Count, "w_regions", "Fire_Counts", "w_regions")