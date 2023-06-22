# -*- coding: utf-8 -*-
import streamlit as st
from data.showdata import run_show_data
from data.appendix import run_appendix

def run_data():
    st.sidebar.markdown("## SubMenu")
    Data_List = st.sidebar.radio(" ", ['ERD', 'Show Data', 'Appendix'], label_visibility='collapsed')
    if Data_List == 'ERD':
        st.header("ERD")
        st.image("img/ERD.png")
    elif Data_List == 'Show Data':
        run_show_data()
    elif Data_List == 'Appendix':
        run_appendix()


# Streamlit 애플리케이션 실행
if __name__ == '__main__':
    run_data()