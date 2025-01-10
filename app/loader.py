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

# Function to calculate churn probability
def calculate_churn_probability(input_data, model):
    """Calculate the churn probability using the provided model."""
    try:
        return model.predict(input_data)[0]
    except Exception as e:
        st.error(f"An error occurred while calculating churn probability: {e}")
        logger.error(f"Error calculating churn probability: {e}")
        return None

# Function to create a gauge visualization
def create_gauge(churn_probability, title):
    """Create a gauge chart to visualize churn probability."""
    try:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=churn_probability * 100,
            title={"text": title},
            gauge={
                "axis": {"range": [0, 100]},
                "steps": [
                    {"range": [0, 50], "color": "lightgreen"},
                    {"range": [50, 100], "color": "salmon"}
                ],
                "threshold": {"line": {"color": "red", "width": 4}, "thickness": 0.75, "value": 50}
            }
        ))
        return fig
    except Exception as e:
        st.error(f"An error occurred while creating the gauge chart: {e}")
        logger.error(f"Error creating gauge chart: {e}")
        return None