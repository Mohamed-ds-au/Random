# import streamlit as st

# #navigation

# pages = [
#     st.Page("home.py", icon = "🏠", title= "Home"),
#     st.Page("visual.py", icon="📈", title= "Visualization"),
#     st.Page("dashboard.py", icon="📊", title= "Dashboard"),
#     st.Page("model.py", icon="💻", title= "Model"),
# ]

# pg = st.navigation(pages)
# pg.run()

import streamlit as st

# --- Streamlit Page Configuration (Title at first) ---
st.set_page_config(
    page_title="HR Attrition Predictor",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --- Navigation Setup ---
# Pages are defined here 
pages = [
    st.Page("home.py", icon="🏠", title="Home"),
    st.Page("visual.py", icon="📈", title="Visualization"),
    st.Page("dashboard.py", icon="📊", title="Dashboard (External)"),
    st.Page("model.py", icon="💻", title="Prediction Model"),
]

# Use the st.navigation object for the primary structure
pg = st.navigation(pages)

pg.run()