import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

conn = sqlite3.connect("bandwidth.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usage(
id INTEGER PRIMARY KEY AUTOINCREMENT,
date TEXT,
data_used REAL
)
""")
conn.commit()

st.title("📡 Bandwidth Usage Analyzer")

menu = st.sidebar.selectbox("Menu", ["Add Usage", "View Report"])

if menu == "Add Usage":
    data = st.number_input("Data Used (GB)", min_value=0.0)

    if st.button("Add"):
        cursor.execute("INSERT INTO usage(date,data_used) VALUES(?,?)",
                       (datetime.now().strftime("%Y-%m-%d"), data))
        conn.commit()
        st.success("Usage Added!")

elif menu == "View Report":
    df = pd.read_sql_query("SELECT * FROM usage", conn)
    st.dataframe(df)

    if not df.empty:
        st.metric("Total Data Used (GB)", round(df["data_used"].sum(),2))
        st.line_chart(df["data_used"])
