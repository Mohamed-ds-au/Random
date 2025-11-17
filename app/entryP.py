import streamlit as st

#navigation

pages = [
    st.Page("home.py", icon = "🏠", title= "Home"),
    st.Page("visual.py", icon="📈", title= "Visualization"),
    st.Page("Model.py", icon="💻", title= "Model"),

]

pg = st.navigation(pages)
pg.run()

