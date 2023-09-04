from st_on_hover_tabs import on_hover_tabs
import streamlit as st
import requests

import streamlit as st
from streamlit_folium import st_folium

st.set_page_config(layout="wide", page_icon= "🏇🏻",
                   initial_sidebar_state="expanded",
                   menu_items={
         'Get Help': 'https://www.google.com.com/',
         'Report a bug': "https://www.extremelycoolapp.com/bug",
         'About': "# This is a header. This is an *extremely* cool app!"
     }
)

st.title("_AND THEY'RE OFF..._")
st.title('_Streamlit_ is :red[cool] :sunglasses:')
'HOW ARE YOU'


def api_test():
    response = requests.get(
    "http://localhost:8000/api-test").json()
    return response
a = api_test()
a

def hello_name(x = st.text_input("your name here"), y = st.text_input("your surname here")):
    parameters = {"name": x,
                  "surname": y,}
    response = requests.get(
        "http://localhost:8000/hello-name",
        params = parameters).json()
    return response

# b = st.text_input("your name here")
# c = st.text_input("your surname here")
d = hello_name()
d

def my_sum(x, y, z):
    parameters = {"num1": x,
                  "num2" : y,
                  "num3" : z,}
    response = requests.get(
        "http://localhost:8000/my-sum",
        params = parameters).json()
    return response

x = st.text_input("num1")
y = st.text_input("num2")
z = st.text_input("num3")

def print_my_sum():
    if any([x,y,z]) == False:
        return "Please Choose 3 Numbers"
    d = my_sum(x,y,z)
    return d

e = print_my_sum()
e

# Just add it after st.sidebar:
# a = st.sidebar.radio('Choose:',[1,2])

# st.image('/Users/james/code/lucasglanville/and_theyre_off_frontend/interface/images/smiley.png')
