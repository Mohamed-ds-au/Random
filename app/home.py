import streamlit as st
import pandas as pd

st.title("Employee Attrition Classification")


st.header("Objective", divider= "gray")
st.write("Our objective in this project is to make analysis about employee attrition and make predctions based on the data")

st.header("Data", divider= "gray")
df = pd.read_csv("../data/Faker_Data/synthetic_hr_dataset.csv")

st.dataframe(df)


