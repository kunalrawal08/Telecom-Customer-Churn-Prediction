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
    """Load the pre-trained model from a pickle file."""
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
    """Load the customer churn data from a CSV file."""
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

# Function to display business metrics in the sidebar
def display_business_metrics(df):
    """Display key business metrics in the sidebar."""
    try:
        st.sidebar.markdown("---")
        st.sidebar.header("📈 Business Metrics (Overall)")

        if df is not None:
            # Example CLV calculation
            clv = df['totrev'].mean() / df['months'].mean()
            
            # Example ARPU calculation
            arpu = df['rev_Mean'].mean()
            
            # Example Number of Complaints (using custcare_Mean as a proxy)
            num_complaints = df['custcare_Mean'].mean() if 'custcare_Mean' in df.columns else 0

            # Display metrics vertically
            st.sidebar.metric(label="📊 Average CLV", value=f"${clv:.2f}")
            st.sidebar.metric(label="💳 Average ARPU", value=f"${arpu:.2f}")
            st.sidebar.metric(label="📞 Average Complaints", value=f"{num_complaints:.2f}")
            style_metric_cards()  # Apply styling to metric cards
    except Exception as e:
        st.error(f"An error occurred while displaying business metrics: {e}")
        logger.error(f"Error displaying business metrics: {e}")

# Function for Customer Churn Prediction section
def customer_churn_prediction(model):
    """Display the customer churn prediction interface."""
    try:
        st.title("📊 Telecom Customer Churn Prediction and Analytical Dashboard")
        st.markdown(
            """
            Welcome to the **Telecom Customer Churn Prediction & Insights Dashboard**. 
            This application leverages advanced machine learning models to predict customer churn and provides key insights for decision-making.
            """
        )

        # Input fields for features
        st.subheader("Enter Customer Information")
        col1, col2 = st.columns(2)

        with col1:
            age = st.slider("Age", 18, 100, 30)
            gender = st.selectbox("Gender", ["Male", "Female"])
            tenure = st.slider("Tenure (months)", 0, 120, 12)
            monthly_charges = st.number_input("Monthly Charges ($)", min_value=0.0, value=50.0, max_value=200.0, help="Maximum limit is $200")
            total_charges = st.number_input("Total Charges ($)", min_value=0.0, value=600.0, max_value=10000.0, help="Maximum limit is $10,000")

        with col2:
            contract_type = st.selectbox("Contract Type", ["Month-to-Month", "One Year", "Two Year"])
            credited = st.selectbox("Payment Method", ["Credit Card", "Bank Transfer", "Electronic Check"])
            usage_frequency = st.slider("Usage Frequency (per month)", 0, 100, 10)
            num_calls = st.slider("Number of Calls to Support", 0, 20, 2)
            complaints = st.slider("Number of Complaints", 0, 10, 0)

        # Convert categorical features to numerical
        gender = 1 if gender == "Male" else 0
        contract_mapping = {"Month-to-Month": 0, "One Year": 1, "Two Year": 2}
        contract_type = contract_mapping[contract_type]
        payment_mapping = {"Credit Card": 0, "Bank Transfer": 1, "Electronic Check": 2}
        credited = payment_mapping[credited]

        # Create a DataFrame for prediction
        input_data = pd.DataFrame({
            "Age": [age],
            "Gender": [gender],
            "Tenure": [tenure],
            "MonthlyCharges": [monthly_charges],
            "TotalCharges": [total_charges],
            "ContractType": [contract_type],
            "PaymentMethod": [credited],
            "UsageFrequency": [usage_frequency],
            "NumberOfCalls": [num_calls],
            "Complaints": [complaints]
        })

        # Real-time churn probability update
        churn_probability = calculate_churn_probability(input_data, model)

        # Prediction
        if st.button("Predict Churn"):
            st.subheader("Prediction Result")
            st.write(f"**Churn Probability: {churn_probability:.2%}**")
            st.progress(float(churn_probability))  # Progress bar for churn probability

            # Classification result
            if churn_probability >= 0.5:
                st.error("⚠️ High Churn Risk")
            else:
                st.success("✅ Low Churn Risk")

            # Gauge visualization for churn risk
            fig = create_gauge(churn_probability, "Churn Probability (%)")
            if fig:
                st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"An error occurred in the customer churn prediction section: {e}")
        logger.error(f"Error in customer churn prediction section: {e}")

# Function for Realtime Churn Rate section
def realtime_churn_rate(model):
    """Display the real-time churn rate interface."""
    try:
        st.header("📉 Realtime Churn Rate")
        st.markdown(
            """
            Adjust customer information to see the real-time churn probability and gauge visualization.
            """
        )

        # Input fields for features
        st.subheader("Enter Customer Information")
        col1, col2 = st.columns(2)

        with col1:
            age = st.slider("Age", 18, 100, 30, key="realtime_age")
            gender = st.selectbox("Gender", ["Male", "Female"], key="realtime_gender")
            tenure = st.slider("Tenure (months)", 0, 120, 12, key="realtime_tenure")
            monthly_charges = st.number_input("Monthly Charges ($)", min_value=0.0, value=50.0, max_value=200.0, help="Maximum limit is $200", key="realtime_monthly_charges")
            total_charges = st.number_input("Total Charges ($)", min_value=0.0, value=600.0, max_value=10000.0, help="Maximum limit is $10,000", key="realtime_total_charges")

        with col2:
            contract_type = st.selectbox("Contract Type", ["Month-to-Month", "One Year", "Two Year"], key="realtime_contract_type")
            credited = st.selectbox("Payment Method", ["Credit Card", "Bank Transfer", "Electronic Check"], key="realtime_payment_method")
            usage_frequency = st.slider("Usage Frequency (per month)", 0, 100, 10, key="realtime_usage_frequency")
            num_calls = st.slider("Number of Calls to Support", 0, 20, 2, key="realtime_num_calls")
            complaints = st.slider("Number of Complaints", 0, 10, 0, key="realtime_complaints")

        # Convert categorical features to numerical
        gender = 1 if gender == "Male" else 0
        contract_mapping = {"Month-to-Month": 0, "One Year": 1, "Two Year": 2}
        contract_type = contract_mapping[contract_type]
        payment_mapping = {"Credit Card": 0, "Bank Transfer": 1, "Electronic Check": 2}
        credited = payment_mapping[credited]

        # Create a DataFrame for prediction
        input_data = pd.DataFrame({
            "Age": [age],
            "Gender": [gender],
            "Tenure": [tenure],
            "MonthlyCharges": [monthly_charges],
            "TotalCharges": [total_charges],
            "ContractType": [contract_type],
            "PaymentMethod": [credited],
            "UsageFrequency": [usage_frequency],
            "NumberOfCalls": [num_calls],
            "Complaints": [complaints]
        })

        # Real-time churn probability update
        churn_probability = calculate_churn_probability(input_data, model)

        # Display real-time churn probability
        st.subheader("Realtime Churn Probability")
        st.write(f"**Churn Probability: {churn_probability:.2%}**")
        st.progress(float(churn_probability))  # Progress bar for churn probability

        # Gauge visualization for real-time churn risk
        fig = create_gauge(churn_probability, "Realtime Churn Probability (%)")
        if fig:
            st.plotly_chart(fig, use_container_width=True)

        # Key insights based on churn probability
        st.subheader("Key Insights")
        if churn_probability >= 0.5:
            st.error("⚠️ **High Churn Risk Detected**")
            st.markdown(
                """
                **Actionable Recommendations:**
                - Offer personalized retention offers (e.g., discounts, free upgrades).
                - Proactively reach out to the customer to address concerns.
                - Analyze usage patterns to identify pain points.
                """
            )
        else:
            st.success("✅ **Low Churn Risk Detected**")
            st.markdown(
                """
                **Actionable Recommendations:**
                - Continue to engage the customer with loyalty programs.
                - Upsell additional services or features.
                - Monitor usage patterns for potential upsell opportunities.
                """
            )
    except Exception as e:
        st.error(f"An error occurred in the realtime churn rate section: {e}")
        logger.error(f"Error in realtime churn rate section: {e}")

# Function for Key Insights and Analysis section
def key_insights_and_analysis(df):
    """Display key insights and analysis based on the data."""
    try:
        st.header("📊 Key Insights and Analysis")
        st.markdown(
            """
            Dive into customer churn data and uncover actionable insights using advanced analytics and visualizations.
            """
        )

        analysis_option = st.selectbox(
            "Choose an Analysis",
            [
                "Overall Churn Rate",
                "Churn Rate by Tenure",
                "Churn by Payment Method",
                "ARPU: Churned vs Retained"
            ]
        )

        if analysis_option == "Overall Churn Rate":
            churn_rate = df['churn'].mean() * 100
            st.metric(label="Overall Churn Rate", value=f"{churn_rate:.2f}%")
            
            fig = px.pie(df, names='churn', title="Overall Churn Rate", 
                         color_discrete_sequence=COLOR_THEME,
                         hole=0.4)
            st.plotly_chart(fig, use_container_width=True)

            st.markdown(
                """
                **Insights:**
                - The overall churn rate provides a high-level view of customer attrition.
                - A higher churn rate indicates a need for immediate retention strategies.
                - Compare this rate with industry benchmarks to assess performance.
                """
            )

        elif analysis_option == "Churn Rate by Tenure":
            fig = px.histogram(df, x='months', color='churn', 
                               barmode='group', title="Churn Rate by Tenure",
                               labels={'months': 'Tenure (Months)', 'churn': 'Churn'},
                               color_discrete_sequence=COLOR_THEME)
            st.plotly_chart(fig, use_container_width=True)

            st.markdown(
                """
                **Insights:**
                - Customers with shorter tenures are more likely to churn.
                - Long-term customers tend to have lower churn rates, indicating loyalty.
                - Focus retention efforts on customers in the 0-12 month tenure range.
                """
            )

        elif analysis_option == "Churn by Payment Method":
            # Advanced Visualization: Sunburst Chart
            df['churn_status'] = df['churn'].map({0: 'Retained', 1: 'Churned'})
            payment_churn = df.groupby(['creditcd', 'churn_status']).size().reset_index(name='count')
            
            fig = px.sunburst(
                payment_churn,
                path=['creditcd', 'churn_status'],  # Hierarchy: Payment Method -> Churn Status
                values='count',  # Size of each segment
                title="Churn by Payment Method (Sunburst Chart)",
                color='churn_status',  # Color by churn status
                color_discrete_sequence=COLOR_THEME,
                hover_data=['count']  # Show count on hover
            )
            fig.update_traces(textinfo="label+percent parent")  # Add labels and percentages
            st.plotly_chart(fig, use_container_width=True)

            st.markdown(
                """
                **Insights:**
                - Customers using electronic checks have a higher churn rate compared to other payment methods.
                - Credit card users are more likely to be retained, indicating a preference for convenience.
                - Consider incentivizing customers to switch to more stable payment methods.
                """
            )

        elif analysis_option == "ARPU: Churned vs Retained":
            if 'rev_Mean' in df.columns and 'churn' in df.columns:
                # Map churn to readable labels
                df['churn_status'] = df['churn'].map({0: 'Retained', 1: 'Churned'})

                # Group data by ARPU bins and churn status
                df['ARPU_bin'] = pd.cut(df['rev_Mean'], bins=20)  # Bin ARPU into 20 groups
                df['ARPU_bin'] = df['ARPU_bin'].astype(str)  # Convert intervals to strings
                arpu_churn = df.groupby(['ARPU_bin', 'churn_status']).size().unstack().fillna(0)

                if 'Churned' in arpu_churn.columns:
                    # Create line chart
                    fig = px.line(
                        arpu_churn,
                        x=arpu_churn.index,  # ARPU bins on x-axis
                        y=arpu_churn.columns,  # Churn status on y-axis
                        title="ARPU: Churned vs Retained (Line Chart)",
                        labels={'value': 'Number of Customers', 'index': 'ARPU Bin', 'variable': 'Churn Status'},
                        color_discrete_sequence=COLOR_THEME
                    )

                    # Optional: Add markers to the lines for better visibility
                    fig.update_traces(mode='lines+markers')

                    # Update layout
                    fig.update_layout(
                        xaxis_title="ARPU Bin",
                        yaxis_title="Number of Customers",
                        legend_title="Churn Status",
                        template="plotly_white",
                        hovermode="x"
                    )

                    # Add annotation to highlight the ARPU bin with the highest churn rate
                    max_churn_bin = arpu_churn['Churned'].idxmax()
                    max_churn_value = arpu_churn['Churned'].max()
                    fig.add_annotation(
                        x=max_churn_bin,
                        y=max_churn_value,
                        text=f"Max Churn: {max_churn_value}",
                        showarrow=True,
                        arrowhead=1,
                        ax=0,
                        ay=-40
                    )

                    # Display the chart in Streamlit
                    st.plotly_chart(fig, use_container_width=True)

                    st.markdown(
                        """
                        **Insights:**
                        - Customers with lower ARPU (Average Revenue Per User) are more likely to churn.
                        - High ARPU customers are retained at a higher rate, indicating their value to the business.
                        - Focus on increasing ARPU through upselling and cross-selling strategies.
                        """
                    )
                else:
                    st.warning("No churned customers found in the dataset for ARPU analysis.")
            else:
                st.error("Required columns ('rev_Mean' or 'churn') not found in the dataset.")
    except Exception as e:
        st.error(f"An error occurred in the key insights and analysis section: {e}")
        logger.error(f"Error in key insights and analysis section: {e}")

# Function for Model Evaluation Metrics section
def model_evaluation_metrics():
    """Display model evaluation metrics."""
    try:
        st.header("📊 Model Evaluation Metrics")
        st.markdown(
            """
            Evaluate the performance of the machine learning model using key metrics and visualizations.
            """
        )

        # Example evaluation metrics (replace with actual model metrics)
        rmse = 0.49174695355193226
        mae = 0.48607733765642713
        r2 = 0.03183860198932953

        # Display metrics in columns
        col1, col2, col3 = st.columns(3)
        col1.metric(label="RMSE", value=f"{rmse:.2f}")
        col2.metric(label="MAE", value=f"{mae:.2f}")
        col3.metric(label="R²", value=f"{r2:.2f}")

        # Final performance metrics
        metrics_data = pd.DataFrame({
            "Metric": ["RMSE", "MAE", "R²"],
            "Value": [0.49174695355193226, 0.48607733765642713, 0.03183860198932953]
        })

        # Visualization
        st.subheader("Model Performance Metrics")

        # Enhanced bar chart
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

        # Customizing the chart appearance
        fig.update_traces(
            texttemplate='%{text:.4f}', 
            textposition='outside', 
            marker_line_color='black',  # Black border for bars
            marker_line_width=1.5       # Border thickness
        )
        fig.update_layout(
            title=dict(
                text="📊 Model Performance Metrics",
                x=0.2,  # Center the title
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
            plot_bgcolor='white',  # White background 
            margin=dict(l=50, r=50, t=100, b=50)  # Adjust margins for clarity
        )

        # Display the chart
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(
            """
            **Insights:**
            - **RMSE (Root Mean Squared Error):** Measures the average deviation of predictions from actual values. Lower values indicate better performance.
            - **MAE (Mean Absolute Error):** Represents the average absolute difference between predicted and actual values. It provides a clear understanding of prediction errors.
            - **R² (R-squared):** Indicates the proportion of variance in the target variable explained by the model. A higher R² value suggests a better fit.
            """
        )
    except Exception as e:
        st.error(f"An error occurred in the model evaluation metrics section: {e}")
        logger.error(f"Error in model evaluation metrics section: {e}")

# Main function to run the app
def main():
    """Main function to run the Streamlit app."""
    try:
        # Load data and model
        model = load_model()
        df = load_csv()

        # Exit if data or model is not loaded
        if model is None or df is None:
            st.stop()

        # Sidebar: "Connect with Me" section at the top
        st.sidebar.header("📩 Connect with Me")
        st.sidebar.markdown(
            """ 
            - [LinkedIn](https://www.linkedin.com/in/kunaldrawal/)  
            - [GitHub](https://github.com/kunalrawal08/Telecom-Custom-Churn-Prediction)  
            - **Email:** kunaldrawal@gmail.com  
            """
        )
        st.sidebar.markdown("---")
        # Sidebar navigation
        st.sidebar.title("Navigation")
        app_mode = st.sidebar.selectbox(
            "Choose a Section",
            ["Customer Churn Prediction", "Realtime Churn Rate", "Key Insights and Analysis", "Model Evaluation Metrics"]
        )

        # Display business metrics in the sidebar
        display_business_metrics(df)

        # Run the selected section
        if app_mode == "Customer Churn Prediction":
            customer_churn_prediction(model)
        elif app_mode == "Realtime Churn Rate":
            realtime_churn_rate(model)
        elif app_mode == "Key Insights and Analysis":
            key_insights_and_analysis(df)
        elif app_mode == "Model Evaluation Metrics":
            model_evaluation_metrics()
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        logger.error(f"Unexpected error in main function: {e}")

# Run the app
if __name__ == "__main__":
    main()