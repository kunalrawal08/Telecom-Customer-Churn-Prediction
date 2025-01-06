import streamlit as st

def realtime_churn_rate(model):
    """Display the real-time churn rate interface."""
    st.header("📊 Realtime Churn Rate")
    st.markdown(
        """
        Monitor the real-time churn rate of customers using the pre-trained model.
        """
    )

    # Input fields for real-time data
    tenure = st.number_input("Tenure (Months)", min_value=0, max_value=100, value=12)
    monthly_charges = st.number_input("Monthly Charges", min_value=0.0, max_value=200.0, value=50.0)
    total_charges = st.number_input("Total Charges", min_value=0.0, max_value=10000.0, value=600.0)
    contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
    payment_method = st.selectbox("Payment Method", ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"])

    # Convert categorical variables to numerical values
    contract_mapping = {"Month-to-month": 0, "One year": 1, "Two year": 2}
    payment_method_mapping = {"Electronic check": 0, "Mailed check": 1, "Bank transfer (automatic)": 2, "Credit card (automatic)": 3}

    contract_value = contract_mapping[contract]
    payment_method_value = payment_method_mapping[payment_method]

    # Prepare the input data for prediction
    input_data = [[tenure, monthly_charges, total_charges, contract_value, payment_method_value]]

    if st.button("Predict Churn Rate"):
        if model:
            prediction = model.predict(input_data)
            churn_probability = prediction[0]
            st.metric(label="Churn Probability", value=f"{churn_probability:.2f}")
        else:
            st.error("Model not loaded. Please check the model file.")