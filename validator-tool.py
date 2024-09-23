import streamlit as st
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

# Initialize GCP SQL cloud connection
import psycopg2

st.sidebar.write("Attempting to connect...")

# Initialize GCP SQL cloud connection using psycopg2
try:
    conn = psycopg2.connect(
        host="XXX.XXX.XXX.XXX",
        port="XXXX",
        user="XXXXXXXX-XXXX",
        password="XXXXXXXXXXXXXXXXX",
        database="XXXXXXXX"
    )
    
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    
    st.sidebar.success(f"Successfully connected to the database! Version: {record[0]}")
    
    # Replace the SQLAlchemy engine part, as you are using psycopg2
    engine = conn
except Exception as e:
    st.sidebar.error(f"Error connecting to the database: {str(e)}")
    engine = None

st.header("Validator Tool")

st.write('')
st.write('')

# Perform query if connection is successful
if engine:
    try:
        query = 'SELECT * FROM gaia.data;'
        df = pd.read_sql(query, conn)
        st.sidebar.success(f"Successfully fetched {len(df)} rows from the database.")
    except Exception as e:
        st.sidebar.error(f"Error executing query: {str(e)}")
        df = pd.DataFrame()
else:
    df = pd.DataFrame()

col1, col2 = st.columns(2)

with col1:
    st.markdown("##### Actual Answer")
    st.write("Placeholder for actual answer")

with col2:
    st.markdown("##### ChatGPT Answer")
    st.write("Placeholder for ChatGPT's answer")

st.divider()  # Adds a horizontal divider line, with some gap

col1, col2 = st.columns([2, 1])  # Adjust column width as needed

with col1:
    st.markdown("##### Comparison Result: ❌ Answers don't match")

with col2:
    st.button("Re-run Prompt")

st.markdown("##### Steps followed:")
steps = st.text_area("Edit these steps and run again if validation fails", "1. Step one\n2. Step two\n3. Step three")

# Extract questions for the dropdown
questions = df['question'].tolist()
        
# Create a dropdown in the sidebar with the questions
dropdown_value = st.sidebar.selectbox("Choose a prompt to test", questions)

col1, col2 = st.sidebar.columns(2)

with col1:
    if st.button("Run Prompt"):
        st.sidebar.write("Running the prompt...")

with col2:
    if st.button("Randomize"):
        st.sidebar.write("Randomizing...")

st.sidebar.header("Prompt:")
prompt_text = "This is a sample prompt. Modify this as needed."

st.sidebar.write(prompt_text)

# Display database results if available
if not df.empty:
    st.header("Database Results")
    st.dataframe(df)
