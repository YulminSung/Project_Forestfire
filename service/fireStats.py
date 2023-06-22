# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd

def run_fireStats():
    bigfire = pd.read_csv("data/bigfire.csv", encoding='cp949')
    # Convert DataFrame to HTML table with center-aligned content and column names
    bigfire_table = bigfire.to_html(index=False, classes=["center-aligned"], justify="center", escape=False, na_rep="")
    # Apply CSS styling to center-align the table
    bigfire_table = f"<style>.center-aligned {{ text-align: center; }}</style>{bigfire_table}"
    # Display the HTML table in Streamlit
    st.markdown(bigfire_table, unsafe_allow_html=True)

if __name__ == "__main__":
    run_fireStats()