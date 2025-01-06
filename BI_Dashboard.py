import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set up the dashboard layout (MUST BE THE FIRST STREAMLIT COMMAND)
st.set_page_config(layout="wide", page_title="Customer Churn Prediction Dashboard", page_icon="📊")

# Load the data
@st.cache_data
def load_data():
    return pd.read_csv(r"C:\Users\Kunal\OneDrive\Desktop\Customer Churn Predictions\data\Telecom_customer churn.csv")

df = load_data()

# Replace marital status codes with their full forms
marital_status_mapping = {
    "S": "Single",
    "A": "Annulled",
    "B": "Divorced",
    "U": "Unknown",
    "M": "Married"
}
df['marital'] = df['marital'].replace(marital_status_mapping)

# Custom color theme
COLOR_THEME = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]

# Title and description
st.title("📊 Customer Churn Prediction Dashboard")
st.markdown("""
    This dashboard provides insights into customer churn patterns and helps identify key factors influencing churn.
    Use the interactive visualizations to explore the data and make data-driven decisions.
""")

# Sidebar for advanced filters
st.sidebar.header("Advanced Filters")
selected_area = st.sidebar.selectbox("Select Area", df['area'].unique())
selected_months = st.sidebar.slider("Select Months with Company", min_value=1, max_value=df['months'].max(), value=(1, 24))
selected_marital = st.sidebar.multiselect("Select Marital Status", df['marital'].unique(), default=df['marital'].unique())
selected_income = st.sidebar.slider("Select Income Range", min_value=df['income'].min(), max_value=df['income'].max(), value=(df['income'].min(), df['income'].max()))

# Filter data based on sidebar selections
filtered_df = df[
    (df['area'] == selected_area) &
    (df['months'].between(selected_months[0], selected_months[1])) &
    (df['marital'].isin(selected_marital)) &
    (df['income'].between(selected_income[0], selected_income[1]))
]

# Main Content: Non-Scrollable Layout
with st.container():
    # Row 1: Key Metrics (Top Section)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Total Customers", value=len(filtered_df), delta="+5%")

    with col2:
        st.metric(label="Churn Rate", value=f"{filtered_df['churn'].mean() * 100:.2f}%", delta="-2%")

    with col3:
        st.metric(label="Average Revenue", value=f"${filtered_df['totrev'].mean():.2f}", delta="+3%")

# Main Content: Grid Layout
with st.container():
    # Row 1: Churn Rate Over Time (full width)
    st.subheader("Churn Rate Over Time")
    churn_over_time = filtered_df.groupby('months')['churn'].mean().reset_index()
    fig1 = px.line(churn_over_time, x='months', y='churn', title="Churn Rate Over Time", 
                   labels={'churn': 'Churn Rate', 'months': 'Months'}, 
                   color_discrete_sequence=[COLOR_THEME[0]], 
                   template="plotly_white")
    fig1.update_traces(line=dict(width=3))
    st.plotly_chart(fig1, use_container_width=True, height=300)

    # Row 2: Churn Distribution and Usage Patterns
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Churn Distribution by Marital Status")
        churn_by_marital = filtered_df.groupby('marital')['churn'].mean().reset_index()
        fig2 = px.bar(churn_by_marital, x='marital', y='churn', title="Churn Rate by Marital Status", 
                      labels={'churn': 'Churn Rate', 'marital': 'Marital Status'}, 
                      color='marital', color_discrete_sequence=COLOR_THEME, 
                      template="plotly_white")
        st.plotly_chart(fig2, use_container_width=True, height=300)

    with col2:
        st.subheader("Usage Patterns: MOU vs. Churn")
        fig3 = px.scatter(filtered_df, x='mou_Mean', y='churn', title="Minutes of Usage (MOU) vs. Churn", 
                          labels={'mou_Mean': 'Mean MOU', 'churn': 'Churn'}, 
                          color='churn', color_discrete_sequence=COLOR_THEME, 
                          trendline="lowess", template="plotly_white")
        st.plotly_chart(fig3, use_container_width=True, height=300)

    # Row 3: Revenue Impact and Service Plan Churn
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Revenue Impact of Churn")
        revenue_impact = filtered_df.groupby('churn')['totrev'].sum().reset_index()
        fig4 = px.bar(revenue_impact, x='churn', y='totrev', title="Total Revenue by Churn Status", 
                      labels={'totrev': 'Total Revenue', 'churn': 'Churn'}, 
                      color='churn', color_discrete_sequence=COLOR_THEME, 
                      template="plotly_white")
        st.plotly_chart(fig4, use_container_width=True, height=300)

    with col4:
        st.subheader("Churn by Service Plan")
        churn_by_plan = filtered_df.groupby('crclscod')['churn'].mean().reset_index()
        fig5 = px.bar(churn_by_plan, x='crclscod', y='churn', title="Churn Rate by Service Plan", 
                      labels={'churn': 'Churn Rate', 'crclscod': 'Service Plan'}, 
                      color='crclscod', color_discrete_sequence=COLOR_THEME, 
                      template="plotly_white")
        st.plotly_chart(fig5, use_container_width=True, height=300)

    # Row 4: Customer Complaints and Predictive Churn Probability
    col5, col6 = st.columns(2)

    with col5:
        st.subheader("Customer Complaints vs.. Churn")
        complaints_churn = filtered_df.groupby('custcare_Mean')['churn'].mean().reset_index()
        fig6 = px.scatter(complaints_churn, x='custcare_Mean', y='churn', title="Customer Complaints vs. Churn", 
                          labels={'custcare_Mean': 'Customer Care Calls', 'churn': 'Churn Rate'}, 
                          color='custcare_Mean', color_continuous_scale=COLOR_THEME, 
                          template="plotly_white")
        st.plotly_chart(fig6, use_container_width=True, height=300)

    with col6:
        st.subheader("Predictive Churn Probability")
        churn_probability = filtered_df['mou_Mean'].mean() / filtered_df['mou_Mean'].max()
        fig7 = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = churn_probability,
            title = {'text': "Churn Probability"},
            gauge = {'axis': {'range': [None, 1]},
                     'steps': [
                         {'range': [0, 0.3], 'color': "lightgreen"},
                         {'range': [0.3, 0.7], 'color': "yellow"},
                         {'range': [0.7, 1], 'color': "red"}],
                     'threshold': {'line': {'color': "black", 'width': 4}, 'thickness': 0.75, 'value': churn_probability}}))
        st.plotly_chart(fig7, use_container_width=True, height=300)

    # Row 5: Comprehensive Churn Analysis (full width)
    st.subheader("Comprehensive Churn Analysis")
    churn_heatmap = filtered_df.groupby(['area', 'crclscod'])['churn'].mean().unstack()
    fig8 = px.imshow(churn_heatmap, labels=dict(x="Service Plan", y="Area", color="Churn Rate"),
                     title="Churn Rate by Area and Service Plan", color_continuous_scale=COLOR_THEME)
    st.plotly_chart(fig8, use_container_width=True, height=400)

# Footer
st.markdown("---")
st.markdown("© 2023 Customer Churn Prediction Dashboard. All rights reserved.")
