# -*- coding: utf-8 -*-
import streamlit as st
from service.news import run_news
from service.youtubeNews import run_youtubeNews
from service.fireStats import run_fireStats
from service.fireWarring import run_fireWarring
from service.callNumber import run_callNumber
from service.declaration import run_declaration

def run_service():
    st.sidebar.markdown("## SubMenu")
    Service_List = st.sidebar.radio(" ", ['강원 비상 연락망', '네이버 뉴스', '강원 산불 영상', '신고 서비스',  '산불 위험 정보', '대형 산불 통계'], label_visibility='collapsed')
    if Service_List == '네이버 뉴스':
        st.header("강원 산불 뉴스")
        run_news()
    elif Service_List == '강원 산불 영상':
        st.header("강원 산불 뉴스 영상")
        run_youtubeNews()
    elif Service_List == '강원 비상 연락망':
        st.header("비상 연락망")
        run_callNumber()
    elif Service_List == '신고 서비스':
        st.header("신고 서비스")
        run_declaration()
    elif Service_List == '산불 위험 정보':
        st.header("산불 위험 정보")
        run_fireWarring()
    elif Service_List == '대형 산불 통계':
        st.header("대형 산불 통계")
        run_fireStats()


if __name__ == "__main__":
    run_service()