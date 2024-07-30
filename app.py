import streamlit as st
import pandas as pd
import time
from datetime import datetime

t= time.time()
date=datetime.fromtimestamp(t).strftime('%Y-%m-%d ')
times=datetime.fromtimestamp(t).strftime('%H:%M:%S ')
df=pd.read_csv("Attendence/attendence_"+ date +".csv")

st.dataframe(df.style.highlight_max(axis=0))