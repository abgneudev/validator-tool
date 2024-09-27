import streamlit as st
import random
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import ast
import openai 
from validator import df

import matplotlib.pyplot as plt

try:
    conn = psycopg2.connect(
        host="104.196.119.128",
        port="5432",
        user="postgres-user",
        password="zqA#q>pv`h3UG.XH",
        database="postgres"
    )
    
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    
    engine = conn
except Exception as e:
    engine = None
    st.error(f"Database connection error: {str(e)}")

# Queries
if engine:
    try:
        query = 'SELECT * FROM gaia.tasks'
        df_tasks = pd.read_sql(query, conn)
    except Exception as e:
        st.sidebar.error(f"Error executing query: {str(e)}")
        df_tasks = pd.DataFrame()
else:
    df_tasks = pd.DataFrame()


if engine:
    try:
        query = 'SELECT * FROM gaia.executions'
        df_executions = pd.read_sql(query, conn)
    except Exception as e:
        st.sidebar.error(f"Error executing query: {str(e)}")
        df_executions = pd.DataFrame()
else:
    df_executions = pd.DataFrame()

if engine:
    try:
        query = 'SELECT * FROM gaia.stepruns'
        df_stepruns = pd.read_sql(query, conn)
    except Exception as e:
        st.sidebar.error(f"Error executing query: {str(e)}")
        df_stepruns = pd.DataFrame()
else:
    df_stepruns = pd.DataFrame()

total_prompts = df['task_id'].nunique()
prompts_tested = df_tasks['req_id'].nunique()

# Sidebar Navigation
st.sidebar.markdown(f"""
#### *Total Prompts*
<p style='font-size: 56px; font-weight: bold; line-height: 2rem;'>{total_prompts}</p>
""", unsafe_allow_html=True)


st.sidebar.markdown(f"""
#### *Total Prompts Tested*
<p style='font-size: 56px; font-weight: bold; line-height: 2rem;'>{prompts_tested}</p>
""", unsafe_allow_html=True)

