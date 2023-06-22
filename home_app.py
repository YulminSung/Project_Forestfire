# -*- coding:utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
import pandas_gbq

import requests
from bs4 import BeautifulSoup
import json
import lxml

from datetime import datetime, timedelta
import time

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
import branca.colormap as cm

from shapely.geometry import Point, Polygon, MultiPolygon, shape
from shapely import wkt

import statsmodels.api as sm

from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import KFold, StratifiedKFold, TimeSeriesSplit, train_test_split, GridSearchCV, RandomizedSearchCV, cross_val_score, cross_val_predict
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score, confusion_matrix, classification_report,  roc_curve, auc, RocCurveDisplay
from imblearn.over_sampling import SMOTE

from xgboost import XGBClassifier, plot_importance
from lightgbm import LGBMClassifier, plot_importance

import googlemaps
from google.cloud import bigquery
from google.oauth2 import service_account

import utils

import os
import warnings
warnings.filterwarnings("ignore")

KEY_PATH = ".streamlit/"

key_path = KEY_PATH + "fireforest-team-ys-2023.json"
servicekey_path = KEY_PATH + "serviceKey.json"

def home_app():
    """
        Renders the introduction section of the app, including tabs for overview, objectives, and analysis phases.
    """

    st.markdown(
        "<h2 style='text-align: center; color: black;'>강원도 산불 예측 및 피해 최소화 프로젝트</span>",
        unsafe_allow_html=True)
    st.write('<hr>', unsafe_allow_html=True)

    # Content
    st.markdown("<h4 style='font-size: 24px; color: black;'>🔍 Goal of the Competition</h4>", unsafe_allow_html=True)
    st.write(
        """
The goal of this competition is to predict MDS-UPDR scores, which measure progression in patients with Parkinson's disease. 
The Movement Disorder Society-Sponsored Revision of the Unified Parkinson's Disease Rating Scale (MDS-UPDRS) is a comprehensive assessment of both motor and non-motor symptoms associated with Parkinson's. 
You will develop a model trained on data of protein and peptide levels over time in subjects with Parkinson’s disease versus normal age-matched control subjects.

Your work could help provide important breakthrough information about which molecules change as Parkinson’s disease progresses.
        """
    )

    st.write('<hr>', unsafe_allow_html=True)

    # Content
    st.markdown("<h4 style='font-size: 24px; color: black;'>🔍 Goal of the Competition</h4>", unsafe_allow_html=True)
    st.write(
        """
The goal of this competition is to predict MDS-UPDR scores, which measure progression in patients with Parkinson's disease. 
The Movement Disorder Society-Sponsored Revision of the Unified Parkinson's Disease Rating Scale (MDS-UPDRS) is a comprehensive assessment of both motor and non-motor symptoms associated with Parkinson's. 
You will develop a model trained on data of protein and peptide levels over time in subjects with Parkinson’s disease versus normal age-matched control subjects.

Your work could help provide important breakthrough information about which molecules change as Parkinson’s disease progresses.
        """
    )

    st.write('<hr>', unsafe_allow_html=True)

    # Link
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info('**Data Analyst: [@Sung](https://muhanyuljung.tistory.com/)**', icon="💡")
    with c2:
        st.info('**GitHub: [@YulminSung](https://github.com/YulminSung/Parkinson_1)**', icon="💻")
    with c3:
        st.info(
            '**Data: [Kaggle](https://www.kaggle.com/competitions/amp-parkinsons-disease-progression-prediction)**',
            icon="🧠")