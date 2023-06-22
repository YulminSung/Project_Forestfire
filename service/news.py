import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import datetime
from tqdm import tqdm
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import streamlit as st

def run_crawling():
    search = '강원도 산불'
    page = 5
    #start수를 1, 11, 21, 31 ...만들어 주는 함수
    page_num = 0

    if page == 1:
        page_num =1
    elif page == 0:
        page_num =1
    else:
        page_num = page+9*(page-1)

    news_title = []
    news_url = []
    news_content = []

    for i in range(1, page_num + 1, 10):
      #url 생성
      url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=" + search + "&start=" + str(page_num)

      # ConnectionError방지
      headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/100.0.48496.75" }

      #html불러오기
      original_html = requests.get(url, headers=headers)
      html = BeautifulSoup(original_html.text, "html.parser")

      # 검색결과
      articles = html.select("div.group_news > ul.list_news > li div.news_area > a")

      for i in articles:
          news_title.append(i.attrs['title'])
          news_url.append(i.attrs['href'])

    news_df = pd.DataFrame({'Title': news_title, 'URL': news_url})

    return news_df


def run_news():
    st.subheader("News")
    news_df = run_crawling()
    # Add link to phone number column
    news_df['URL'] = news_df['URL'].apply(lambda x: f'<a href="{x}">{x}</a>')
    # Convert DataFrame to HTML table with center-aligned content and column names
    news_df = news_df.to_html(index=False, classes=["center-aligned"], justify="center", escape=False)
    # Apply CSS styling to center-align the table
    news_df = f"<style>.center-aligned {{ text-align: center; }}</style>{news_df}"
    # Display the HTML table in Streamlit
    st.markdown(news_df, unsafe_allow_html=True)

if __name__ == "__main__":
    run_news()