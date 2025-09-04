import streamlit as st
import plotly.express as px
from business import Business

st.set_page_config(page_title="Failure Insights", layout="wide")

business = Business()
st.header("📉 Failure Insights")

# 1. Failed count by service
df = business.fetch_failure_summary_grouped_by_service()

if df.empty:
    st.warning("No failure data found.")
else:
    fig = px.bar(
        df, x='service_team', y='fail_count', color='service_team',
        title='🧨 Failed Tests by Service Team', text='fail_count'
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# 2. Recent fail list
st.subheader("📋 Recent Failures")
recent_df = business.fetch_recent_failures()

if recent_df.empty:
    st.info("No recent failure records.")
else:
    for idx, row in recent_df.iterrows():
        with st.expander(f"❌ {row['test_name']} — {row['service_team']} — {row['timestamp']}"):
            st.error(row['error_message'] or "No traceback available")
