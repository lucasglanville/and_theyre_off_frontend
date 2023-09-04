#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd
import numpy as np
import base64

st.set_page_config(page_title="And They're Off", page_icon="🐎", initial_sidebar_state="expanded")

##########################################
##  Load and Prep Data                  ##
##########################################

@st.cache_data
def load_data():
    data = pd.read_csv('/Users/james/code/lucasglanville/and_theyre_off_frontend/interface/data_cleaned_and_preprocessed_v3.csv',
                       usecols = ['f_ko', 'pred_isp'])
    return data
data = load_data()
data["required_odds"] = round(1/(data.pred_isp/1.1),2)
data['pred_isp'] = round(data.pred_isp,2)
cols = ['f_ko', 'pred_isp','required_odds']

##########################################
##  Style and Formatting                ##
##########################################

# CSS for tables

hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>   """

center_heading_text = """
    <style>
        .col_heading   {text-align: center !important}
    </style>          """

center_row_text = """
    <style>
        td  {text-align: center !important}
    </style>      """

# Inject CSS with Markdown

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)
set_background('/Users/james/code/lucasglanville/and_theyre_off_frontend/interface/images/ascot.jpg')

st.markdown(hide_table_row_index, unsafe_allow_html=True)
st.markdown(center_heading_text, unsafe_allow_html=True)
st.markdown(center_row_text, unsafe_allow_html=True)



# More Table Styling
# def color_threshold(val):
#     if str(val) == '0':
#         color = 'azure'
#     elif str(val)[0] == '-':
#         color = 'lightpink'
#     else:
#         color = 'lightgreen'
#     return 'background-color: %s' % color

heading_properties = [('font-size', '16px'),('text-align', 'center'),
                      ('color', 'black'),  ('font-weight', 'bold'),
                      ('background', 'mediumturquoise'),('border', '1.2px solid')]

cell_properties = [('font-size', '16px'),('text-align', 'center')]

dfstyle = [{"selector": "th", "props": heading_properties},
               {"selector": "td", "props": cell_properties}]

# Expander Styling

st.markdown(
    """
<style>
.streamlit-expanderHeader {
 #   font-weight: bold;
    background: aliceblue;
    font-size: 18px;
}
</style>
""",
    unsafe_allow_html=True,
)

##########################################
##  Title, Tabs, and Sidebar            ##
##########################################

st.title("Time to place your bets!")
st.markdown('''##### <span style="color:gray">A Data-led approach to having a flutter...</span>
            ''', unsafe_allow_html=True)

tab_races, tab_horse, tab_explore, tab_faq = st.tabs(["Today' Races", "Horse Lookup",
                                                                 "Explore", "FAQ"])

col1, col2, col3 = st.sidebar.columns([1,8,1])
with col1:
    st.write("")
with col2:
    st.image('/Users/james/code/lucasglanville/and_theyre_off_frontend/interface/images/john-mcririck.jpeg',  use_column_width=True)
with col3:
    st.write("")

st.sidebar.markdown(" ## A Data-led approach to having a flutter...")
st.sidebar.markdown("""Our model was trained on horse-racing data from the past
                    two years, which included information about previous wins,
                    starting odds, jockey and trainer. Using a Deep Learning Neural Network, we were able to use
                    the model to generate our own odds for horses within any
                    given race. If the difference between our winner and the
                    bookies' favourite was above a certain threshold
                    then we place the bet.""")
st.sidebar.info("""DISCLAIMER:
                   This app does not in any way constitute financial advice or
                   guarantee an outcome.
                   [When the fun stops, stop](https://www.begambleaware.org/?gclid=Cj0KCQjwl8anBhCFARIsAKbbpyR-hWh4_1ohK2g55Fv4CQo8uEnyDZiSXOxJN1-uW6SqzKqEe0UOBPsaAt_OEALw_wcB&gclsrc=aw.ds).""", icon="⚠️")


#########################################
## RACES TAB                           ##
#########################################

with tab_races:
    date = st.selectbox("Select Race Date & Time:", data.f_ko.unique(), index = 0)
    st.markdown('''#### Race Details:''', unsafe_allow_html=True)

    styler_race_odds = (data[data.f_ko == date][cols]
                   .style.set_properties(**{'background': 'azure', 'border': '1.2px solid'})
                   .hide(axis='index')
                   .set_table_styles(dfstyle))
                #    .applymap(color_threshold))
    st.table(styler_race_odds)


    st.success('''**A Brief Note on Methods:**

The machine learning model deployed in this app is a Random Forest
Classifier that uses the following information to predict a player's market value: Games Played, Games Started,
Minutes Per Game, Points Per Game, Usage Percentage, Offensive Box Plus/Minus (OBPM), Value Over Replacement Player (VORP),
and Win Shares (WS), all scraped from [Basketball Reference](http://www.basketball-reference.com).''',)

    ###############################################################################
