import streamlit as st
import pandas as pd
import plotly.express as px

def model_evaluation_metrics():
    """Display model evaluation metrics."""
    st.header("📊 Model Evaluation Metrics")
    st.markdown(
        """
        Evaluate the performance of the machine learning model using key metrics and visualizations.
        """
    )

    rmse = 0.49174695355193226
    mae = 0.48607733765642713
    r2 = 0.03183860198932953

    col1, col2, col3 = st.columns(3)
    col1.metric(label="RMSE", value=f"{rmse:.2f}")
    col2.metric(label="MAE", value=f"{mae:.2f}")
    col3.metric(label="R²", value=f"{r2:.2f}")

    metrics_data = pd.DataFrame({
        "Metric": ["RMSE", "MAE", "R²"],
        "Value": [rmse, mae, r2]
    })

    st.subheader("Model Performance Metrics")
    fig = px.bar(
        metrics_data,
        x="Metric",
        y="Value",
        text="Value",
        title="Model Performance Metrics",
        labels={"Value": "Metric Value"},
        color="Metric",
        color_discrete_sequence=px.colors.sequential.Viridis 
    )
    fig.update_traces(
        texttemplate='%{text:.4f}', 
        textposition='outside', 
        marker_line_color='black',
        marker_line_width=1.5
    )
    fig.update_layout(
        title=dict(
            text="📊 Model Performance Metrics",
            x=0.2,
            font=dict(size=24, color="darkblue")
        ),
        xaxis=dict(
            tickfont=dict(size=14, color="black"),
            title=dict(font=dict(size=16, color="darkblue"))
        ),
        yaxis=dict(
            tickfont=dict(size=14, color="black"),
            title=dict(font=dict(size=16, color="darkblue")),
            gridcolor='lightgrey'
        ),
        plot_bgcolor='white',
        margin=dict(l=50, r=50, t=100, b=50)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        """
        **Insights:**
        - **RMSE (Root Mean Squared Error):** Measures the average deviation of predictions from actual values. Lower values indicate better performance.
        - **MAE (Mean Absolute Error):** Represents the average absolute difference between predicted and actual values. It provides a clear understanding of prediction errors.
        - **R² (R-squared):** Indicates the proportion of variance in the target variable explained by the model. A higher R² value suggests a better fit.
        """
    )