import streamlit as st
import pandas as pd 
import numpy as np
import plotly.express as px
import Introduction as intro
import inferential_statistics
import eda
import machine_learning
import prediction

st.set_page_config(layout="wide")
st.header("Autoscout Used Car Data Exploration")
st.subheader(":blue[_When the power of Exploratory Data Analysis, Inferential Statistics and Machine Lerning come together, the Data prevails in the most effcient way_]")
st.sidebar.header("Content")

import streamlit as st
import numpy as np
import pandas as pd



# Read the data
# die Liste in der Navigationsleiste definieren
content = {"1. Introduction":                                      intro,
    "2. EDA"   :                                                eda,
    "3. Inferential"  :                                       inferential_statistics,
    "4. Machine Learning ":                                 machine_learning,
    "5. Prediction ":                                    prediction}                                   

select = st.sidebar.radio("go to:", list(content.keys()))

content[select].app()
