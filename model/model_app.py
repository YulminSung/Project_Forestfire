# -*- coding:utf-8 -*-

import streamlit as st
import pandas as pd
import seaborn as sns
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import r2_score, mean_absolute_error
import plotly.graph_objects as go
import plotly.express as px

def run_model():
    st.sidebar.markdown("## Model")
    modeling = st.sidebar.radio('submenu',['ML', 'DL', 'ETC'], label_visibility='collapsed')
    if modeling == 'ML':
        st.header("ML")
    elif modeling == 'DL':
        st.header("DL")
    elif modeling == 'ETC':
        st.header("ETC")