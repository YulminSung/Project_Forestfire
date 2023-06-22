# -*- coding: utf-8 -*-
import streamlit as st
from eda.map import run_map
from data.map_data import map_loadData
from eda.weather import weather_chart
import PIL

def run_region():
    st.subheader("강원도 지역 분할")
    st.markdown("- 강원도 지역을 **:red[기상관측지점]** 및 **:red[구역(내륙/산지/해안)]** 등의 기준에 따라 9분할 분류")
    st.image("img/eda_img/region.png")

def run_eda():
    st.sidebar.markdown("## Exploration for Data")
    eda = st.sidebar.radio('submenu', ['Gangwon Regional Classification', 'Weather data by region', 'Damage Map', 'Chart4'], label_visibility='collapsed')
    if eda == 'Weather data by region':
        st.markdown("## Weather data by region")
        weather_chart()
    elif eda == 'Damage Map':
        st.markdown("## Damage Map")
        run_map()
    elif eda == 'Gangwon Regional Classification':
        run_region()
    elif eda == 'Chart4':
        st.markdown("## Chart4")
        pass

if __name__ == '__main__':
    run_eda()