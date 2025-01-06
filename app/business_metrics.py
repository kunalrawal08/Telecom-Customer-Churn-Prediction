import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards

def display_business_metrics(df):
    """Display key business metrics in the sidebar."""
    st.sidebar.markdown("---")
    st.sidebar.header("📈 Business Metrics (Overall)")

    if df is not None:
        clv = df['totrev'].mean() / df['months'].mean()
        arpu = df['rev_Mean'].mean()
        num_complaints = df['custcare_Mean'].mean() if 'custcare_Mean' in df.columns else 0

        st.sidebar.metric(label="📊 Average CLV", value=f"${clv:.2f}")
        st.sidebar.metric(label="💳 Average ARPU", value=f"${arpu:.2f}")
        st.sidebar.metric(label="📞 Average Complaints", value=f"{num_complaints:.2f}")
        style_metric_cards()  # Apply styling to metric cards