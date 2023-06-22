# -*- coding: utf-8 -*-
import streamlit as st

def run_fireWarring():
    # Define the URL of the webpage
    url = "http://forestfire.nifos.go.kr/main.action"
    st.markdown(f"[Forest Fire Information System]({url})")
    st.image("http://forestfire.nifos.go.kr/images/map/img_forest_today.gif")

if __name__ == "__main__":
    run_fireWarring()