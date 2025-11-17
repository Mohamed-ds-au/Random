import streamlit as st
import pandas as pd
import pickle
from pathlib import Path

st.set_page_config(page_title="Model", layout="wide")
st.title("Model")

st.header("Predict from file")
uploaded_file = st.file_uploader("Choose a CSV file to predict (optional)", type=["csv"])
if uploaded_file is not None:
    try:
        data = pd.read_csv(uploaded_file)
        model_path = Path(__file__).parent / "best_model.pkl"
        if model_path.exists():
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            pred = model.predict(data)
            pred = pd.Series(pred).map({0: 'Stayed', 1: 'Left'})
            data['attrition'] = pred
            st.success('Prediction complete')
            st.dataframe(data.head())

            @st.cache_data
            def convert_for_download(df):
                return df.to_csv(index=False).encode('utf-8')

            st.download_button('Download predictions (CSV)', convert_for_download(data), file_name='predictions.csv')
        else:
            st.error('Model file `best_model.pkl` not found in app folder.')
    except Exception as e:
        st.error(f'Failed to read or predict on uploaded file: {e}')


st.markdown("---")
st.header("Manual input — edit the default row")

# Columns the user requested to be editable
editable_cols = [
    'age','gender','years_at_company','job_role','monthly_income','work_life_balance',
    'job_satisfaction','performance_rating','number_of_promotions','overtime','distance_from_home',
    'education_level','marital_status','number_of_dependents','job_level','company_size',
    'remote_work','leadership_opportunities','innovation_opportunities','company_reputation',
    'employee_recognition','attrition','age_groups','age_before_working'
]

# Load sample defaults from `synthetic_hr_dataset.csv` if available
sample_path = Path(__file__).parent / 'synthetic_hr_dataset.csv'
defaults = {}
sample_df = None
if sample_path.exists():
    try:
        sample_df = pd.read_csv(sample_path)
        first = sample_df.iloc[0]
        for c in editable_cols:
            if c in first:
                defaults[c] = first[c]
            else:
                defaults[c] = ''
    except Exception:
        defaults = {c: '' for c in editable_cols}
else:
    defaults = {c: '' for c in editable_cols}

st.write('A single row with default values is displayed below — edit any field and press Predict or Download.')

with st.form('manual_row_form'):
    inputs = {}
    # two-column layout for inputs
    cols = st.columns(2)
    for i, col_name in enumerate(editable_cols):
        target = cols[i % 2]
        default_val = defaults.get(col_name, '')
        # numeric widget for likely numeric columns
        if col_name in ('age','years_at_company','monthly_income','performance_rating','number_of_promotions','distance_from_home','number_of_dependents','age_before_working'):
            try:
                val = float(default_val) if default_val != '' else 0.0
            except Exception:
                val = 0.0
            inputs[col_name] = target.number_input(label=col_name, value=val)
        else:
            # if sample_df present, try to offer selectbox from unique values
            if sample_df is not None and col_name in sample_df.columns:
                try:
                    options = sample_df[col_name].dropna().unique().tolist()
                    # ensure string options
                    options = [str(x) for x in options]
                    default_index = 0
                    try:
                        default_index = options.index(str(default_val))
                    except Exception:
                        default_index = 0
                    inputs[col_name] = target.selectbox(label=col_name, options=options, index=default_index)
                except Exception:
                    inputs[col_name] = target.text_input(label=col_name, value=str(default_val))
            else:
                inputs[col_name] = target.text_input(label=col_name, value=str(default_val))

    submitted = st.form_submit_button('Predict')

if submitted:
    # build dataframe from inputs
    try:
        manual_df = pd.DataFrame([inputs])
        st.write('Edited row:')
        st.dataframe(manual_df)

        # attempt to run model if exists
        model_path = Path(__file__).parent / 'best_model.pkl'
        if model_path.exists():
            try:
                with open(model_path, 'rb') as f:
                    model = pickle.load(f)
                pred = model.predict(manual_df)
                pred_label = {0: 'Stayed', 1: 'Left'}.get(int(pred[0]), str(pred[0]))
                st.success(f'Prediction: {pred_label}')
                manual_df['attrition'] = pred_label
            except Exception as e:
                st.error(f'Prediction failed: {e}')
        else:
            st.info('No model file found — you can still download the edited row.')

        @st.cache_data
        def convert(df):
            return df.to_csv(index=False).encode('utf-8')

        st.download_button('Download edited row (CSV)', convert(manual_df), file_name='manual_row.csv')
    except Exception as e:
        st.error(f'Failed to prepare manual row: {e}')
