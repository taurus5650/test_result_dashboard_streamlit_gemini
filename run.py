import streamlit as st
from sqlalchemy import text

from database.config import SDETDatabase
from database.postgres_helper import PostgresHelper

# Set page config
st.set_page_config(page_title="Automation Dashboard", layout="wide")

# Dashboard title
st.title("🚦 Automation Test Result Dashboard")

# DB init
config = SDETDatabase()
db_helper = PostgresHelper(config)

with db_helper.get_session() as session:
    try:
        query = text("SELECT * FROM automation_test_result ORDER BY create_time DESC LIMIT 10")
        result = session.execute(query)
        rows = result.fetchall()
        columns = result.keys()

        if rows:
            st.success("✅ Query success")
            import pandas as pd

            df = pd.DataFrame(rows, columns=columns)
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("⚠️ No data found in automation_test_result table.")
    except Exception as e:
        st.error(f"❌ Query failed: {e}")
