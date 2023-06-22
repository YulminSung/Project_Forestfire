# -*- coding:utf-8 -*-
import pandas as pd
import streamlit as st
from utils import credentials

from statsmodels.tsa.stattools import adfuller
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import scipy.stats as stats
from pingouin import ttest
# @st.cache_data(ttl=600)
# def run_twoMeans():
#     st.markdown("- **The independent samples $t$-test** comes in two different forms, Student’s and Welch’s. The original Student **$t$-test** – which is the one I’ll describe in this section – is the simpler of the two, but relies on much more restrictive assumptions than the Welch **$t$-test**. Assuming for the moment that you want to run a two-sided test, the goal is to determine whether two “independent samples” of data are drawn from populations with the same mean (the null hypothesis) or different means (the alternative hypothesis). When we say “independent” samples, what we really mean here is that there’s no special relationship between observations in the two samples. This probably doesn’t make a lot of sense right now, but it will be clearer when we come to talk about the paired samples **$t$-test** later on. For now, let’s just point out that if we have an experimental design where participants are randomly allocated to one of two groups, and we want to compare the two groups’ mean performance on some outcome measure, then an independent samples **$t$-test** (rather than a paired samples **$t$-test**) is what we’re after. \n"
#                 r"- Okay, so let’s let $\mu_1$ denote the true population mean for group 1 , and $\mu_2$ will be the true population mean for group 2, and as usual we’ll let $\bar{X}_1$ and $\bar{X}_2$ denote the observed sample means for both of these groups. Our null hypothesis states that the two population means are identical ($\mu_1 = \mu_2$) and the alternative to this is that they are not ($\mu_1 \neq \mu_2$). Written in Written in mathematical-ese, this is…")
#     st.latex(r"""
#         \begin{split}
#         \begin{array}{ll}
#         H_0: & \mu_1 = \mu_2  \\
#         H_1: & \mu_1 \neq \mu_2
#         \end{array}
#         \end{split}
#     """)
#
#     mu1 = 0
#     sigma = 1
#     mu2 = 2
#
#     x1 = np.linspace(mu1 - 4 * sigma, mu1 + 4 * sigma, 100)
#     y1 = 100 * stats.norm.pdf(x1, mu1, sigma)
#     x2 = np.linspace(mu2 - 4 * sigma, mu2 + 4 * sigma, 100)
#     y2 = 100 * stats.norm.pdf(x2, mu2, sigma)
#
#     fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
#
#     sns.lineplot(x=x1, y=y1, color='black', ax=ax1)
#
#     sns.lineplot(x=x1, y=y1, color='black', ax=ax2)
#     sns.lineplot(x=x2, y=y2, color='black', ax=ax2)
#
#     ax1.text(0, 43, 'null hypothesis', size=20, ha="center")
#     ax2.text(0, 43, 'alternative hypothesis', size=20, ha="center")
#
#     ax1.set_frame_on(False)
#     ax2.set_frame_on(False)
#     ax1.get_yaxis().set_visible(False)
#     ax2.get_yaxis().set_visible(False)
#     ax1.get_xaxis().set_visible(False)
#     ax2.get_xaxis().set_visible(False)
#     ax1.axhline(y=0, color='black')
#     ax2.axhline(y=0, color='black')
#
#     st.pyplot(fig)
#
#     st.markdown('## Data Visualization')
#     st.markdown("#### 데이터 차트 넣기")
#
#     st.markdown("### Data Cleaning and Comparison")
#     st.markdown("![](https://www.investopedia.com/thmb/R4twtcFq0xh1C2YLF-_QfeH30Is=/750x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/ttest2-147f89de0b384314812570db74f16b17.png)")
#     col1 = st.selectbox('Select Column 1', )
#     col2 = st.selectbox('Select Column 2', )
#     if col1 != col2:
#         st.markdown("Sample Size is Equal?")
#         st.markdown("Independent Test")
#     else:
#         st.warning("Two Columns are must be different")

def run_regression():
    select_region = st.selectbox('지역 선택', ['강원북부내륙', '강원중부내륙', '강원남부내륙', '강원북부산지', '강원중부산지', '강원남부산지', '강원북부해안', '강원중부해안', '강원남부해안'])
    mapping = {
        '강원북부내륙': 1, '강원북부산지': 2, '강원북부해안': 3,
        '강원중부내륙': 4, '강원중부산지': 5, '강원중부해안': 6,
        '강원남부내륙': 7, '강원남부산지': 8, '강원남부해안': 9
    }
    if select_region in mapping:
        st.image("img/eda_img/region_stats" + str(mapping[select_region]) + ".png")


def run_stats():
    st.sidebar.markdown("## SubMenu")
    submenu = st.sidebar.radio("Submenu", ['Two Means', 'Logistic Regression'], label_visibility='collapsed')
    if submenu == 'Two Means':
        st.markdown("## Two Means")
        pass
    elif submenu == 'Logistic Regression':
        run_regression()