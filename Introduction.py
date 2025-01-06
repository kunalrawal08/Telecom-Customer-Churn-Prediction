import streamlit as st
import plotly.express as px

# Set up the app layout
st.set_page_config(
    layout="wide",
    page_title="Customer Churn Prediction App",
    page_icon="📊"
)

# Main content
st.title("Welcome to the Customer Churn Prediction App 🚀")
st.markdown("""
    This app is designed to help businesses analyze and predict customer churn by leveraging machine learning and data visualization techniques. 
    Customer churn, also known as customer attrition, occurs when customers stop doing business with a company. Understanding and predicting churn 
    is critical for retaining customers and improving business profitability.
""")

# Project Description
st.markdown("---")
st.markdown("### About the Project")
st.markdown("""
    The **Customer Churn Prediction App** is built to provide actionable insights into customer behavior and churn patterns. 
    It uses a machine learning model trained on historical customer data to predict the likelihood of churn for individual customers. 
    Additionally, the app offers a comprehensive dashboard to visualize key metrics, trends, and factors influencing churn.

    #### **Key Features**:
    - **Churn Prediction**: Predict the likelihood of customer churn using a pre-trained machine learning model.
    - **Interactive Dashboard**: Explore churn trends, customer demographics, and usage patterns through interactive visualizations.
    - **Data-Driven Insights**: Identify key factors contributing to churn and take proactive measures to retain customers.
    - **User-Friendly Interface**: Easily navigate between prediction and analysis tools with a clean and intuitive interface.

    #### How It Works:
    1. **Prediction Page**: Enter customer details to get real-time churn predictions.
    2. **Dashboard Page**: Analyze churn trends and patterns using interactive charts and graphs.
""")

# Add credentials
st.markdown("---")
st.markdown("### Connect with Me")
st.markdown("""
    - 🔗 [LinkedIn](https://www.linkedin.com/in/your-linkedin-profile)
    - 🐙 [GitHub](https://github.com/your-github-profile)
    - 📧 [Gmail](mailto:your-email@gmail.com)
    - 📞 [Contact](tel:+91 9326138375)
""")

# Footer
st.markdown("---")
st.markdown("© 2025 Customer Churn Prediction App. All rights reserved. Kunal Rawal")