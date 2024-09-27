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

input_tokens_run =  df_executions['input_token'].sum()
input_tokens_rerun =  df_stepruns['input_token'].sum()

output_tokens_run =  df_executions['output_token'].sum()
output_tokens_rerun =  df_stepruns['output_token'].sum()

total_input_tokens = input_tokens_run+input_tokens_rerun
total_input_tokens_cost = (total_input_tokens*0.000005)
total_output_tokens = output_tokens_run+output_tokens_rerun
total_output_tokens_cost = (total_output_tokens*0.000015)
total_cost = total_input_tokens_cost+total_output_tokens_cost

# Sidebar Navigation
st.sidebar.markdown(f"""
#### *Total Prompts*
<p style='font-size: 56px; font-weight: bold; line-height: 2rem;'>{total_prompts}</p>
""", unsafe_allow_html=True)

st.sidebar.markdown(f"""
#### *Total Prompts Tested*
<p style='font-size: 56px; font-weight: bold; line-height: 2rem;'>{prompts_tested}</p>
""", unsafe_allow_html=True)

st.sidebar.markdown(f"""
#### *Total Input Tokens Used*
<p style='font-size: 56px; font-weight: bold; line-height: 2rem;'>{total_input_tokens}</p>
""", unsafe_allow_html=True)

st.sidebar.markdown(f"""
#### *Total Output Tokens Used*
<p style='font-size: 56px; font-weight: bold; line-height: 2rem;'>{total_output_tokens}</p>
""", unsafe_allow_html=True)

st.sidebar.markdown(f"""
#### *Total Cost*
<p style='font-size: 56px; font-weight: bold; line-height: 1rem;'>${round(total_cost, 4)}</p>
""", unsafe_allow_html=True)