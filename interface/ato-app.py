#!/usr/bin/env python
# coding: utf-8

import os
import streamlit as st
from st_files_connection import FilesConnection
import pandas as pd
import numpy as np
import base64
import gcsfs
import requests
import json
from fractions import Fraction

st.set_page_config(page_title="And They're Off",
                   page_icon="🐎",
                   initial_sidebar_state="collapsed")

##########################################
##  Load and Prep Data                  ##
##########################################

@st.cache_data
def load_data():
    conn = st.experimental_connection('gcs', type= FilesConnection )
    data = conn.read("and-theyre-off/hr_thurs_rem.csv", input_format="csv", ttl=600)
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
data['RACING POST ODDS'] = round(data.pred_isp,2)

def float_to_integer(x):
        x = x - 1
        if x % 1 == 0:
            ratio = x.as_integer_ratio()
            num = ratio[0]
            den = ratio[1]
            return f'{num}/{den}'
        else:
            return Fraction(str(x)).limit_denominator()
data['RACING POST ODDS'] = data['RACING POST ODDS'].apply(float_to_integer)

cols = ['time', 'f_horse', 'pred_isp']
pred_cols = ['time', 'f_horse', 'pred_isp']
image_path = os.path.join(os.getcwd(), 'interface', 'images')

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



st.markdown(hide_table_row_index, unsafe_allow_html=True)
st.markdown(center_heading_text, unsafe_allow_html=True)
st.markdown(center_row_text, unsafe_allow_html=True)
set_background(os.path.join(image_path,'background-2.jpg'))

cell_properties = [('font-size', '16px'),('text-align', 'center')]

heading_properties1 = [('font-size', '16px'),('text-align', 'center'),
                       ('color', 'black'),  ('font-weight', 'bold'),
                       ('background', '#e47dff'),('border', '1.2px solid')]

dfstyle1 = [{"selector": "th", "props": heading_properties1},
            {"selector": "td", "props": cell_properties}]

heading_properties2 = [('font-size', '16px'),('text-align', 'center'),
                       ('color', 'black'),  ('font-weight', 'bold'),
                       ('background', '#88FFB3'),('border', '1.2px solid')]

dfstyle2 = [{"selector": "th", "props": heading_properties2},
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
col1, col2 = st.columns([3,8])
with col1:
    st.image(os.path.join(image_path, 'Logo.png'), use_column_width = True)

with col2:
    st.title("AND THEY'RE OFF!")
    st.markdown('''#### <span style="color:black">A data-led approach to finding value in horse racing...</span>
                ''', unsafe_allow_html=True)

tab_overview, tab_races, tab_analysis, tab_aboutus = st.tabs(["Overview",
                                   "Races",
                                   "Analysis",
                                   "About Us"
                                  ])


#########################################
##            OVERVIEW TAB             ##
#########################################

with tab_overview:

    st.markdown(" #### Hello!")
    st.markdown('''<div style="text-align: justify;">
    Welcome to AND THEY'RE OFF, a data-science project that combines futuristic
    deep-learning techniques with the age-old sport of horse racing.
    </div>''', unsafe_allow_html=True)
    ""
    st.markdown('''<div style="text-align: justify;">
    Our team set out to create an innovative model capable
    of forecasting the profitability of each horse in any given Handicap race.
    We've replaced gut-feelings, intuition, and useless tips from Dave down the
    pub with a reliable long-term strategy in the marketplace.
    Forget Dave, we've brought you the power of Neural Networks!
    </div>''', unsafe_allow_html=True)
    ""
    st.image('https://user-images.githubusercontent.com/74038190/241765440-80728820-e06b-4f96-9c9e-9df46f0cc0a5.gif',  use_column_width=True)
    st.markdown(" #### Using Neural Networks to analyse historic horse-racing data")
    st.markdown('''<div style="text-align: justify;">
    Our model was trained on horse-racing data from the past
    two years, which included information about previous wins,
    starting odds, jockey and trainer. Using a Deep Learning Neural Network, we were able to use
    the model to generate our own odds for horses within any
    given race. If the difference between our winner and the
    bookies' favourite was above a certain threshold
    then we place the bet.</div>''', unsafe_allow_html=True)
    ""
    st.info("""DISCLAIMER:
                    This app does not in any way constitute financial advice or
                    guarantee an outcome.
                    [When the fun stops, stop](https://www.begambleaware.org/?gclid=Cj0KCQjwl8anBhCFARIsAKbbpyR-hWh4_1ohK2g55Fv4CQo8uEnyDZiSXOxJN1-uW6SqzKqEe0UOBPsaAt_OEALw_wcB&gclsrc=aw.ds).""",
            icon="⚠️")

#########################################
## RACES TAB                           ##
#########################################

with tab_races:
    ### USER SELECTS TRACK & TIME ###
    # st.markdown('''##### <span style="color:black">Showing results for 02/09/2023</span>
    #         ''', unsafe_allow_html=True)

    date = st.selectbox("Select A Date:", data.date.unique(), index = 844)
    date_df = (data[data.date == date])
    track = st.selectbox("Select A Racecourse:", date_df.f_track.unique(), index = 0)
    racecourse_df = (date_df[date_df.f_track == track])
    time = st.selectbox("Select A Race Time:", racecourse_df.time.unique(), index = 0)

    data_send_df = racecourse_df[racecourse_df.time == time]

    racecourse_df['HORSE'] = racecourse_df.f_horse
    racecourse_df['JOCKEY'] = racecourse_df.f_jockey
    racecourse_df['TRAINER'] = racecourse_df.f_trainer

    ### RETURN RACE DETAILS AS DATAFRAME
    st.markdown('''## <span style="color:black">Race Details</span>
            ''', unsafe_allow_html=True)
    "Below are the details of each horse in the race you have selected..."
    # st.markdown('''#### <span style="color:black">Below are the details of each horse in the race you have selected...</span>
    #         ''', unsafe_allow_html=True)
    styler_race_odds = (racecourse_df[racecourse_df.time == time][['HORSE', 'JOCKEY', 'TRAINER','RACING POST ODDS']]
                   .style.set_properties(**{'background': "#F4E5FD", 'border': '1.2px solid'})
                   .hide(axis='index')
                   .set_table_styles(dfstyle1))
                #    .applymap(color_threshold))
    # styler_race_odds.format({"Racing Post Odds": "{:.2f}".format})
    st.table(styler_race_odds)

    ### CONVERT DATAFRAME TO JSON TO SEND TO API
    data_to_send = data_send_df[data_send_df.time == time].drop(columns = ['date', 'time', 'RACING POST ODDS'])
    json_df = data_to_send.to_json(orient="records")

    url = "https://ato-image-byhyua3o7a-nw.a.run.app/return-df"
    data = json.dumps({"df": json_df})
    headers = {"Content-Type": "application/json"}

    if st.button("Show me the predictions!",use_container_width = True, type = 'primary'):
        st.markdown('''## <span style="color:black">Race Predictions</span>
            ''', unsafe_allow_html=True)
        "Here are the predictions from our model on whether each horse is worth a bet or not..."
        # st.markdown('''#### <span style="color:black">Here are the predictions from our model on whether each horse is worth a bet or not...</span>
        #     ''', unsafe_allow_html=True)
        response = requests.post(url, data=data, headers=headers)
        # st.write(f'The return from the API is: {response}')
        response = response.json()
        return_df = pd.read_json(response["df"])
        # st.write(return_df.shape)
        # print("Converted To JSON")
#
        return_df['date'] = return_df['f_ko'].apply(extract_date)
        return_df['time'] = return_df['f_ko'].apply(extract_time)
        return_df['HORSE'] = return_df.f_horse
        def res_to_percent(x):
            # x = str(x*100)
            return str(x)[:4]
        return_df['MODEL CONFIDENCE'] = return_df['model_preds'].apply(res_to_percent)
        #  = return_df.model_preds
        return_df['BACK?'] = return_df.bet

        def bet_to_back(x):
            if x == 'BET':
                return '✅ BACK ✅'
            return '❌ BELOW THRESHOLD ❌'
        return_df['BACK?'] = return_df['BACK?'].apply(bet_to_back)

        styler_predictions = (return_df[return_df.time == time][['HORSE','MODEL CONFIDENCE', 'BACK?']]
                   .style.set_properties(**{'background': "#E1FDEB", 'border': '1.2px solid'})
                   .hide(axis='index')
                   .set_table_styles(dfstyle2))
                #    .applymap(pred_color_threshold))
        st.table(styler_predictions)
        # styler_predictions.format({"pred_isp": "{:.2f}".format})
        st.info("""
        PLEASE READ CAREFULLY:
        1. The model ONLY applies to Betfair Exchange odds. Other bookmakers will have lower odds and the potential edge will not hold.
        2. The model is trained on odds FIVE minutes before the race starts and ONLY applies to horses that have odds of < 50.0 at this EXACT
        point in time.
        3. Any horses FIVE minutes before race start with odds >50.0 would automatically not reach our model threshold, but are still included
        in the horse list.
        
        - If we were to put this model into production we would automate placement using a [Betfair bot](https://www.bfbotmanager.com/en) that would only ’back’ 
        selections 5 mins before race time on horses with odds <50.0.
        - If anyone was to use this model manually, they would need to check the odds manually 5 mins before the race and ‘back’
        only if odds <50.0.

        DISCLAIMER: none of the above constitutes financial advice and the model is still in advanced 'testing' phases.

        """, icon="⚠️") 

        # st.write(return_df)

###############################################################################

#########################################
## THE SCIENCE TAB                     ##
#########################################

graph_path = os.path.join(os.getcwd(), 'interface', 'images', 'graphs')
    

with tab_analysis:

    # st.markdown('''##### <span style="color:black">Simulated Results & Analysis</span>
    #         ''', unsafe_allow_html=True)
    st.markdown('''<div style="text-align: justify;">
    The raw dataset consisted of over 10 racetypes, however our analysis concentrated
    on 'Flat Handicap' races, as this was by far the modal racetype.
    We then split our data chronologically to ensure no look-ahead bias. Hence, our
    test set for these simulated results spans the last 12 months - from October
    2022 to September 2023. It contains 4,150 races.
    </div>''', unsafe_allow_html=True)
    ""
    ""
    ############# 1. Comparing Our Model To Baseline Strategies ################

    st.markdown('''##### <span style="color:black">1. Comparing Our Model To Baseline Strategies</span>
            ''', unsafe_allow_html=True)
    st.markdown('''<div style="text-align: justify;">
    Here are our simulated profits of betting £1 on each horse that our model
    indicates. To compare, we also show the results of betting £1 every race on
    the horse with the best odds, betting £1 on every horse, and one of the best
    strategies there is, not betting at all:
    </div>''', unsafe_allow_html=True)
    ""
    st.image(os.path.join(graph_path, 'graph-model_vs_baseline.png'), use_column_width = True)
    ""
    st.markdown('''<div style="text-align: justify;">
    Unsurprisingly, betting on every horse is a sure-fire way to lose all your
    money. Betting on the horse with the best odds appears to be a damage-limiting
    strategy, making a small loss. Our neural network model is profitable
    over this test set, and over a reasonably large sample size too - it places
    999 total bets over the 4150 races.
    </div>''', unsafe_allow_html=True)
    ""
    ""
    ""
    ""
    ########################### 2. Monthly Metrics ############################
    

    st.markdown('''##### <span style="color:black">2. Monthly Metrics</span>
            ''', unsafe_allow_html=True)

    st.markdown('''<div style="text-align: justify;">
    Here are monthly metrics from our simulated results. There are more races -
    and thus more bets placed - in the summer months. The model makes a profit
    in 8 out of the 12 months, but it's difficult to discern any seasonal patterns
    in our returns without more than a single year of test data.
    </div>''', unsafe_allow_html=True)
    ""
    st.image(os.path.join(graph_path, 'graph-bets_by_month.png'), use_column_width = True)
    ""
    ""
    ""
    ""
    ############ 3. Exploring different model confidence thresholds ############
    st.markdown('''##### <span style="color:black">3. Exploring Different Model Confidence Thresholds</span>
            ''', unsafe_allow_html=True)

    st.markdown('''<div style="text-align: justify;">
    A crucial decision we had to make was choosing the model confidence 'threshold' for
    placing a bet. Should we place a bet every time our model outputs a confidence
    value above 50%? Or allow ourselves a buffer by raising the threshold for placing a bet?
    </div>''', unsafe_allow_html=True)
    ""
    ""
    st.markdown('''<div style="text-align: justify;">
    The first graph below shows the simulated returns of betting £1 on horses using
    different confidence thresholds for bet-placing:
    </div>''', unsafe_allow_html=True)
    ""
    st.image(os.path.join(graph_path, 'graph-confidence_thresholds1.png'), use_column_width = True)
    ""
    st.markdown('''<div style="text-align: justify;">
    On our test data, using a 90% confidence threshold generated almost the same
    total profit as using a 50% confidence threshold in less than half as many
    bets, and actually generated higher total profit than using a 70% threshold.
    </div>''', unsafe_allow_html=True)
    ""
    st.image(os.path.join(graph_path, 'graph-confidence_thresholds2.png'), use_column_width = True)
    ""
    st.markdown('''<div style="text-align: justify;">
    As the third graph shows below, bets placed within the 50%-90% confidence band
    only made marginal positive returns. For this reason, a 90% confidence threshold for
    bet-placing was chosen for our final model.
    </div>''', unsafe_allow_html=True)
    ""
    st.image(os.path.join(graph_path, 'graph-confidence_thresholds3.png'), use_column_width = True)
    ""
    ""
    ""
    ""
    #################### 4. Exploring different odds bands ####################

    st.markdown('''##### <span style="color:black">4. Exploring Different Odds Bands</span>
            ''', unsafe_allow_html=True)
    ""
    st.image(os.path.join(graph_path, 'graph-returns_by_odds.png'), use_column_width = True)
    ""
    st.markdown('''<div style="text-align: justify;">
    Analysis by odds bands shows that odds up to 50/1 are still profitable on average
    in the backtests. We might consider removing odds under 10/1 if that odds band didn't show
    imporovement.
    </div>''', unsafe_allow_html=True)
    ""
    ""
    #################### 5. ROI ####################

    st.markdown('''##### <span style="color:black">5. Return On Investment</span>
            ''', unsafe_allow_html=True)
    ""
    st.image(os.path.join(graph_path, 'graph-returns_by_odds.png'), use_column_width = True)
    ""
    st.markdown('''<div style="text-align: justify;">
    ROI text
    </div>''', unsafe_allow_html=True)
    ""
    ""

#########################################
## TEST TAB                            ##
#########################################

# with tab_test:

#     col4, col5 = st.columns([8,8], gap = 'large')
#     with col4:
#         st.image("../interface/images/graphs/graph-returns_by_odds.png",
#                  use_column_width= True)
#         st.image("../interface/images/graphs/graph-returns_by_odds.png",
#                  use_column_width= True)
#     with col5:
#         st.markdown('''<div style="text-align: justify;">Our model was trained on horse-racing data from the past
#                             two years, which included information about previous wins,
#                             starting odds, jockey and trainer. Using a Deep Learning Neural Network, we were able to use
#                             the model to generate our own odds for horses within any
#                             given race. If the difference between our winner and the
#                             bookies' favourite was above a certain threshold
#                             then we place the bet.</div>''', unsafe_allow_html=True)
#         ""
#         ""
#         ""
#         st.markdown('''<div style="text-align: justify;">Our model was trained on horse-racing data from the past
#                             two years, which included information about previous wins,
#                             starting odds, jockey and trainer. Using a Deep Learning Neural Network, we were able to use
#                             the model to generate our own odds for horses within any
#                             given race. If the difference between our winner and the
#                             bookies' favourite was above a certain threshold
#                             then we place the bet.</div>''', unsafe_allow_html=True)
#         ""
#         ""
#         ""


with tab_aboutus:
    column1, column2 = st.columns([2,9])
    with column1:
        st.image(os.path.join(image_path, 'JStone2069.jpg'), width=100)
     
        ""
        st.image(os.path.join(image_path, "jimjamjoyce.jpg"), width=100)
        ""
        st.image(os.path.join(image_path, "cjh78.jpg"), width=100)
        ""

        st.image(os.path.join(image_path, "lucasglanville.jpg"),width=100)
        ""

        st.image(os.path.join(image_path, "OliverGreene.jpg"), width=100)
        
        # st.image("../interface/images/JStone2069.jpg", width=100)
        # ""
        # st.image("../interface/images/jimjamjoyce.jpg", width=100)
        # ""
        # st.image("../interface/images/cjh78.jpg", width=100)
        # ""

        # st.image("interface/images/lucasglanville.jpg",width=100)
        # ""

        # st.image("../interface/images/OliverGreene.jpg", width=100)

    with column2:
        st.subheader("Josh Stone \nhttps://github.com/JStone2609")
        ""
        ""
        st.subheader("James Joyce \nhttps://github.com/jimjamjoyce")
        ""
        ""
        st.subheader("Connor Hassan \nhttps://github.com/cjh78")
        ""
        ""
        st.subheader("Lucas Glanville \nhttps://github.com/lucasglanville")
        ""
        ""
        st.subheader("Oliver Greene \nhttps://github.com/OliverGreene")
