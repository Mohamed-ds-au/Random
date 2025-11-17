import streamlit as st
import pandas as pd
import pickle
st.title("Model")

st.header("Predict from file", divider= "grey")


uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)

    with open("best_model.pkl", 'rb') as file:

        model = pickle.load(file)

    pred = model.predict(data)
    pred = pd.Series(pred).map({0: 'Stayed', 1: 'Left'})

    data["attrition"] = pred


    @st.cache_data
    def convert_for_download(df):
        return df.to_csv().encode("utf-8")

    csv = convert_for_download(data)

    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="data.csv",
        mime="text/csv",
        icon=":material/download:",
    )
