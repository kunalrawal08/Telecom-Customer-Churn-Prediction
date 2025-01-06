import streamlit as st
import pandas as pd
import plotly.express as px

COLOR_THEME = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]

def key_insights_and_analysis(df):
    """Display key insights and analysis based on the data."""
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
        df['churn_status'] = df['churn'].map({0: 'Retained', 1: 'Churned'})
        payment_churn = df.groupby(['creditcd', 'churn_status']).size().reset_index(name='count')
        
        fig = px.sunburst(
            payment_churn,
            path=['creditcd', 'churn_status'],
            values='count',
            title="Churn by Payment Method (Sunburst Chart)",
            color='churn_status',
            color_discrete_sequence=COLOR_THEME,
            hover_data=['count']
        )
        fig.update_traces(textinfo="label+percent parent")
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
            df['churn_status'] = df['churn'].map({0: 'Retained', 1: 'Churned'})
            df['ARPU_bin'] = pd.cut(df['rev_Mean'], bins=20)
            df['ARPU_bin'] = df['ARPU_bin'].astype(str)
            arpu_churn = df.groupby(['ARPU_bin', 'churn_status']).size().unstack().fillna(0)

            if 'Churned' in arpu_churn.columns:
                fig = px.line(
                    arpu_churn,
                    x=arpu_churn.index,
                    y=arpu_churn.columns,
                    title="ARPU: Churned vs Retained (Line Chart)",
                    labels={'value': 'Number of Customers', 'index': 'ARPU Bin', 'variable': 'Churn Status'},
                    color_discrete_sequence=COLOR_THEME
                )
                fig.update_traces(mode='lines+markers')
                fig.update_layout(
                    xaxis_title="ARPU Bin",
                    yaxis_title="Number of Customers",
                    legend_title="Churn Status",
                    template="plotly_white",
                    hovermode="x"
                )
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