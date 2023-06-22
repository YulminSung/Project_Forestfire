# -*- coding: utf-8 -*-
import streamlit as st
from streamlit_option_menu import option_menu

import utils
import home_app
import stats_app
# import data_app
# import eda_app
# import stat_app
# import model_app
# import service_app

import time
import warnings
warnings.filterwarnings("ignore")


def main():
    """
        Main function to run the Streamlit app.
    """

    st.set_page_config(page_title="강원도 산불 예측 및 피해 최소화 프로젝트",
                       page_icon=':fire:',
                       layout="wide",
                       initial_sidebar_state="auto",
                       menu_items=None)

    # Streamlit 앱 실행
    with st.sidebar:
        selected = option_menu("Main Menu", ["HOME", "DATA", "EDA", "STAT", "MODEL", "SERVICE"],
                               icons=["house", "card-checklist", "bar-chart", "clipboard-data", "gear"],
                               menu_icon="cast",
                               default_index=0,
                               orientation="vertical",
                               key = 'main_option',
                               styles = {
                                   "container": {"padding": "5!important", "background-color": "#fafafa"},
                                   "icon": {"color": "orange", "font-size": "25px"},
                                   "nav-link": {"font-size": "16px", "text-align":"left", "margin":"0px", "--hover-color": "#eee"},
                                   "nav-link-selected": {"background-color": "#02ab21"},
                               })

    if selected == "HOME":
        home_app.home_app()
    elif selected == "DATA":
        pass
    elif selected == "EDA":
        pass
    elif selected == "STAT":
        stats_app.run_stats()
    elif selected == "MODEL":
        pass
    elif selected == "SERVICE":
        pass

if __name__ == "__main__":
    main()