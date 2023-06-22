# -*- coding: utf-8 -*-
import pandas as pd
import streamlit as st

def run_callNumber():
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["강원도", "산림청", "시/군", "소방서", "국립공원", "한국전력공사"])
    with tab1 :
        st.subheader("강원도")
        gangwon = pd.read_csv("data/gangwon.csv", encoding='cp949')
        # Add link to phone number column
        gangwon['대표전화번호'] = gangwon['대표전화번호'].apply(lambda x: f'<a href="tel:{x}">{x}</a>')
        # Convert DataFrame to HTML table with center-aligned content and column names
        gangwon_table = gangwon.to_html(index=False, classes=["center-aligned"], justify="center", escape=False)
        # Apply CSS styling to center-align the table
        gangwon_table = f"<style>.center-aligned {{ text-align: center; }}</style>{gangwon_table}"
        # Display the HTML table in Streamlit
        st.markdown(gangwon_table, unsafe_allow_html=True)
    with tab2:
        st.subheader("산림청")
        mountain = pd.read_csv("data/mountain.csv", encoding='cp949')
        # Add link to phone number column
        mountain['대표전화번호'] = mountain['대표전화번호'].apply(lambda x: f'<a href="tel:{x}">{x}</a>')
        # Convert DataFrame to HTML table with center-aligned content and column names
        mountain_table = mountain.to_html(index=False, classes=["center-aligned"], justify="center", escape=False)
        # Apply CSS styling to center-align the table
        mountain_table = f"<style>.center-aligned {{ text-align: center; }}</style>{mountain_table}"
        # Display the HTML table in Streamlit
        st.markdown(mountain_table, unsafe_allow_html=True)
    with tab3:
        st.subheader("시/군")
        mountain = pd.read_csv("data/mountain.csv", encoding='cp949')
        # Add link to phone number column
        mountain['대표전화번호'] = mountain['대표전화번호'].apply(lambda x: f'<a href="tel:{x}">{x}</a>')
        # Convert DataFrame to HTML table with center-aligned content and column names
        mountain_table = mountain.to_html(index=False, classes=["center-aligned"], justify="center", escape=False)
        # Apply CSS styling to center-align the table
        mountain_table = f"<style>.center-aligned {{ text-align: center; }}</style>{mountain_table}"
        # Display the HTML table in Streamlit
        st.markdown(mountain_table, unsafe_allow_html=True)
    with tab4:
        st.subheader("소방서")
        firestation = pd.read_csv("data/firestation.csv", encoding='cp949')
        # Add link to phone number column
        firestation['대표전화번호'] = firestation['대표전화번호'].apply(lambda x: f'<a href="tel:{x}">{x}</a>')
        # Convert DataFrame to HTML table with center-aligned content and column names
        firestation_table = firestation.to_html(index=False, classes=["center-aligned"], justify="center", escape=False)
        # Apply CSS styling to center-align the table
        firestation_table = f"<style>.center-aligned {{ text-align: center; }}</style>{firestation_table}"
        # Display the HTML table in Streamlit
        st.markdown(firestation_table, unsafe_allow_html=True)
    with tab5:
        st.subheader("국립 공원")
        park = pd.read_csv("data/mountain.csv", encoding='cp949')
        # Add link to phone number column
        park['대표전화번호'] = park['대표전화번호'].apply(lambda x: f'<a href="tel:{x}">{x}</a>')
        # Convert DataFrame to HTML table with center-aligned content and column names
        park_table = park.to_html(index=False, classes=["center-aligned"], justify="center", escape=False)
        # Apply CSS styling to center-align the table
        park_table = f"<style>.center-aligned {{ text-align: center; }}</style>{park_table}"
        # Display the HTML table in Streamlit
        st.markdown(park_table, unsafe_allow_html=True)
    with tab6:
        st.subheader("한국 전력 공사")
        elect = pd.read_csv("data/elect.csv", encoding='cp949')
        # Add link to phone number column
        elect['대표전화번호'] = elect['대표전화번호'].apply(lambda x: f'<a href="tel:{x}">{x}</a>')
        # Convert DataFrame to HTML table with center-aligned content and column names
        elect_table = elect.to_html(index=False, classes=["center-aligned"], justify="center", escape=False)
        # Apply CSS styling to center-align the table
        elect_table = f"<style>.center-aligned {{ text-align: center; }}</style>{elect_table}"
        # Display the HTML table in Streamlit
        st.markdown(elect_table, unsafe_allow_html=True)

if __name__ == "__main__":
    run_callNumber()