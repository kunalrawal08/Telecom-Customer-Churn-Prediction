import streamlit as st
import pandas as pd
import pickle
import plotly.express as px
import plotly.graph_objects as go
from streamlit_extras.metric_cards import style_metric_cards
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Custom color theme for eye-catching visuals
COLOR_THEME = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]

# Load the model
@st.cache_data
def load_model():
   
    try:
        with open('voting_regressor_model.pkl', 'rb') as f:
            model = pickle.load(f)
        logger.info("Model loaded successfully.")
        return model
    except FileNotFoundError:
        st.error("Model file 'voting_regressor_model.pkl' not found. Please ensure it exists in the correct directory.")
        logger.error("Model file not found.")
        return None
    except Exception as e:
        st.error(f"An error occurred while loading the model: {e}")
        logger.error(f"Error loading model: {e}")
        return None

# Load the CSV file
@st.cache_data
def load_csv():

    try:
        df = pd.read_csv(r"C:\Users\Kunal\OneDrive\Desktop\Telecom-Customer-Churn-Prediction\data\Telecom_customer churn.csv")
        logger.info("CSV file loaded successfully.")
        return df
    except FileNotFoundError:
        st.error("CSV file 'Telecom_customer_churn.csv' not found. Please ensure it exists in the correct directory.")
        logger.error("CSV file not found.")
        return None
    except Exception as e:
        st.error(f"An error occurred while loading the CSV file: {e}")
        logger.error(f"Error loading CSV file: {e}")
        return None