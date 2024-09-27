import streamlit as st
import random
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import ast
import openai 
from validator import df


if not df.empty:
     st.header("Database Results")
     st.dataframe(df)