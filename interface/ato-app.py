#!/usr/bin/env python
# coding: utf-8

import streamlit as st
from st_files_connection import FilesConnection
import pandas as pd
import numpy as np
import base64
import gcsfs
import requests
import json
from fractions import Fraction



st.set_page_config(page_title="And They're Off", page_icon="🐎", initial_sidebar_state="expanded")

##########################################
##  Load and Prep Data                  ##
##########################################

@st.cache_data



def load_data():
    conn = st.experimental_connection('gcs', type= FilesConnection )
    data = conn.read("and-theyre-off/hr_data_0409_221rem.csv", input_format="csv", ttl=600)
    # data = pd.read_csv('/Users/james/code/lucasglanville/and_theyre_off_frontend/interface/data_cleaned_and_preprocessed_v3.csv',
    #                    usecols = ['f_ko', 'pred_isp'])
    return data
data = load_data()
def extract_date(x):
    return x[:10]
def extract_time(x):
    return x[11:]
data['date'] = data['f_ko'].apply(extract_date)
data['time'] = data['f_ko'].apply(extract_time)

# def float_to_integer(x):
#     ratio = x.as_integer_ratio()
#     return f'{ratio[0]}'/{ratio[1]}'
# data.pred_isp = data[['pred_isp'][0]].apply(float_to_integer)

data["required_odds"] = round(1/(data.pred_isp/1.1),2)
data['pred_isp'] = round(data.pred_isp,2)
cols = ['time', 'f_horse', 'pred_isp']
pred_cols = ['time', 'f_horse', 'pred_isp']

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
st.markdown('''##### <span style="color:white">Select a course and a time, then hit that predict button below!</span>
            ''', unsafe_allow_html=True)

tab_races, tab_historic, tab_explore, tab_faq = st.tabs(["Today's Races", "Historic Stats",
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
    ### USER SELECTS TRACK & TIME ###
    date_df = (data[data.date == '02/09/2023'])
    '02/09/2023'
    track = st.selectbox("Select A Racecourse:", date_df.f_track.unique(), index = 0)
    racecourse_df = (date_df[date_df.f_track == track])

    racecourse_df['Kick Off'] = racecourse_df.time
    racecourse_df['Horse'] = racecourse_df.f_horse
    racecourse_df['Jockey'] = racecourse_df.f_jockey
    racecourse_df['Trainer'] = racecourse_df.f_trainer
    racecourse_df['Racing Post Odds'] = racecourse_df['pred_isp']

    # racecourse_df['Racing Post Odds'] = racecourse_df['pred_isp'].apply(float_to_integer)

    time = st.selectbox("Select A Race Time:", racecourse_df.time.unique(), index = 0)
    # time_df = (racecourse_df[racecourse_df.time == time])


    ### RETURN RACE DETAILS AS DATAFRAME
    st.markdown('''#### <span style="color:white">Race Details:</span>
            ''', unsafe_allow_html=True)
    styler_race_odds = (racecourse_df[racecourse_df.time == time][['Horse', 'Jockey', 'Trainer','Racing Post Odds']]
                   .style.set_properties(**{'background': 'azure', 'border': '1.2px solid'})
                   .hide(axis='index')
                   .set_table_styles(dfstyle))
                #    .applymap(color_threshold))
    # styler_race_odds.format({"Racing Post Odds": "{:.2f}".format})
    st.table(styler_race_odds)

    ### CONVERT DATAFRAME TO JSON TO SEND TO API
    data_to_send = racecourse_df[racecourse_df.time == time].drop(columns = ['date', 'time', 'required_odds'])
    json_df = data_to_send.to_json(orient="records")

    url = "http://127.0.0.1:8000/return-df"
    data = json.dumps({"df": json_df})
    headers = {"Content-Type": "application/json"}


    if st.button("PREDICT"):
        st.markdown('''## <span style="color:white">Race Predictions:</span>
            ''', unsafe_allow_html=True)
        response = requests.post(url, data=data, headers=headers)
        st.write(f'The return from the API is: {response}')
        response = response.json()
        return_df = pd.read_json(response["df"])
        # st.write(return_df.shape)
        print("Converted To JSON")
#
        return_df['date'] = return_df['f_ko'].apply(extract_date)
        return_df['time'] = return_df['f_ko'].apply(extract_time)
        # return_df["required_odds"] = round(1/(return_df.pred_isp/1.1),2)
        # return_df['pred_isp'] = round(return_df.pred_isp,2)

        styler_predictions = (return_df[return_df.time == time][['f_horse', 'bet','model_preds']]
                   .style.set_properties(**{'background': 'azure', 'border': '1.2px solid'})
                   .hide(axis='index')
                   .set_table_styles(dfstyle))
                #    .applymap(color_threshold))
        styler_predictions.format({"pred_isp": "{:.2f}".format})
        st.table(styler_predictions)

        # st.write(return_df)

    #################################################################################£
