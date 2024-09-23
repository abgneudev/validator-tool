import streamlit as st
import random
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import ast

import psycopg2

try:
    conn = psycopg2.connect(
        host="XXX.XXX.XXX.XXX",
        port="XXXX",
        user="XXXXXXXX-XXXX",
        password="XXXXXXXXXXXXXXXX",
        database="XXXXXXXX"
    )
    
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    
    engine = conn
except Exception as e:
    engine = None

st.header("Validator Tool")

st.write('')
st.write('')

if engine:
    try:
        query = 'SELECT * FROM gaia.data;'
        df = pd.read_sql(query, conn)
    except Exception as e:
        st.sidebar.error(f"Error executing query: {str(e)}")
        df = pd.DataFrame()
else:
    df = pd.DataFrame()


questions = df['question'].tolist()

col1, col2 = st.sidebar.columns([2,1])

with col1:
    dropdown_value = st.sidebar.selectbox("Choose a prompt to test", questions)

with col2:
    if st.sidebar.button("Randomize"):
        dropdown_value = random.choice(questions)


st.sidebar.header("Prompt:")
prompt_text = dropdown_value
st.sidebar.write(prompt_text)

if st.sidebar.button("Run Prompt"):
    st.write("")

col1, col2 = st.columns(2)

question_answer_dict = dict(zip(df['question'], df['final_answer']))
final_answer = question_answer_dict.get(dropdown_value, "No final answer found.")

with col1:
    st.markdown("##### Actual Answer")
    st.write(final_answer)

with col2:
    st.markdown("##### ChatGPT Answer")
    st.write("Placeholder for ChatGPT's answer")

st.divider() 

col1, col2 = st.columns([2,1])
with col1:
    st.button("Answers Match")
    st.button("Re-run Prompt")

question_steps_dict = dict(zip(df['question'], df['annotator_metadata']))
annotator_data_str = question_steps_dict.get(dropdown_value, "{}") 
try:
    annotator_data = ast.literal_eval(annotator_data_str)
except ValueError:
    annotator_data = {}

steps = annotator_data.get('Steps', "No steps found.")

st.markdown("##### Steps followed:")
steps = st.text_area("Edit these steps and run again if validation fails",steps)

if not df.empty:
     st.header("Database Results")
     st.dataframe(df)
