import streamlit as st
import pandas as pd
from database.config import SDETDatabase
from database.postgres_helper import PostgresHelper

config = SDETDatabase()
db_helper = PostgresHelper(config=config)

def fetch_latest_results(limit: int = 10) -> pd.DataFrame:
    query = """
        SELECT *
        FROM automation_test_result
        ORDER BY create_time DESC
        LIMIT %s;
    """
    # 一次拿 rows + columns
    with db_helper.connection.cursor() as cur:
        cur.execute(query, (limit,))
        rows = cur.fetchall()
        cols = [d[0] for d in cur.description]

    return pd.DataFrame(rows, columns=cols)

@st.cache_data(ttl=30)
def load_results(limit: int):
    return fetch_latest_results(limit)

def main():
    st.set_page_config(page_title="Automation Test Results", layout="wide")
    st.title("Automation Test Results (Latest)")

    limit = st.sidebar.slider("Number of rows", 5, 50, 10, step=5)

    if st.button("Refresh Data", use_container_width=True):
        load_results.clear()

    try:
        df = load_results(limit)
        if df.empty:
            st.info("No records found.")
        else:
            st.dataframe(df, use_container_width=True, height=600)
    except Exception as e:
        st.error(f"Query failed: {e}")

if __name__ == "__main__":
    main()
