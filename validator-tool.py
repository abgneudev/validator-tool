import streamlit as st
import random
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import ast
import openai 

# Integrating OpenAI API
openai.api_key = 'OPENAI_API_KEY'

def get_openai_response(question, steps=None):
    try:
        messages = [
            {
                "role": "system",
                "content": "You are an expert assistant capable of answering a wide variety of fact-based questions. Provide direct and accurate answers across different topics, always ensuring precision and clarity."
            },
            {
                "role": "user",
                "content": question
            }
        ]
        
        if steps:
            messages[1]["content"] = f"The user provided the following steps to solve the question:\n{steps}\n\nThe original question is: {question}"
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=0.2 if steps else 0.5,
            max_tokens=1000 if steps else 2048,
            top_p=1,
            frequency_penalty=0.5 if steps else 0,
            presence_penalty=0.5 if steps else 0
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error fetching response: {str(e)}"

def validate_input(input_value):
    return bool(input_value)

# Connecting Database on GCP
try:
    conn = psycopg2.connect(
        host="XXX.XXX.XXX",
        port="XXXX",
        user="XXXXXXXX-XXXX",
        password="XXX",
        database="XXXXXXXX"
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
        query = 'SELECT * FROM gaia.data;'
        df = pd.read_sql(query, conn)
    except Exception as e:
        st.sidebar.error(f"Error executing query: {str(e)}")
        df = pd.DataFrame()
else:
    df = pd.DataFrame()

st.header("Validator Tool")

st.write('')

# Sidebar Navigation
levels = ['All'] + sorted(df['level'].unique().tolist()) if not df.empty else ['All']
selected_level = st.sidebar.selectbox("Select difficulty level:", levels)

if selected_level != 'All' and not df.empty:
    filtered_df = df[df['level'] == selected_level]
    questions = filtered_df['question'].tolist()
else:
    questions = df['question'].tolist() if not df.empty else []

# Initialize session state for dropdown_value and openai_response
if 'dropdown_value' not in st.session_state:
    st.session_state.dropdown_value = questions[0] if questions else None
if 'openai_response' not in st.session_state:
    st.session_state.openai_response = "Run Prompt to get an answer from ChatGPT"

# Dropdown for question selection
dropdown_value = st.sidebar.selectbox(
    "Choose a prompt to test", 
    questions, 
    index=questions.index(st.session_state.dropdown_value) if st.session_state.dropdown_value in questions else 0,
    key="question_dropdown"
)

# Update session state and reset ChatGPT answer if a new question is selected
if dropdown_value != st.session_state.dropdown_value:
    st.session_state.dropdown_value = dropdown_value
    st.session_state.openai_response = "Run Prompt to get an answer from ChatGPT"

# Randomize button
if st.sidebar.button("Randomize", key="randomize_button"):
    if questions:
        st.session_state.dropdown_value = random.choice(questions)
        st.session_state.openai_response = "Run Prompt to get an answer from ChatGPT"
        st.rerun()
    else:
        st.sidebar.error("No questions available for the selected level.")

st.sidebar.header("Prompt:")
prompt_text = st.session_state.dropdown_value if st.session_state.dropdown_value else "No question selected"
st.sidebar.write(prompt_text)

if st.sidebar.button("Run Prompt", key="run_prompt_button"):
    if validate_input(st.session_state.dropdown_value):
        st.session_state.openai_response = "Fetching response from ChatGPT..."
        openai_response = get_openai_response(st.session_state.dropdown_value)
        st.session_state.openai_response = openai_response
    else:
        st.sidebar.error("Please select a valid question.")
        st.session_state.openai_response = "Run Prompt to get an answer from ChatGPT"

col1, col2 = st.columns(2)

question_answer_dict = dict(zip(df['question'], df['final_answer'])) if not df.empty else {}
final_answer = question_answer_dict.get(st.session_state.dropdown_value, "No final answer found.")

# Main Section
with col1:
    st.markdown("##### Actual Answer")
    st.write(final_answer)

with col2:
    st.markdown("##### ChatGPT Answer")
    st.write(st.session_state.openai_response)

st.divider()

question_steps_dict = dict(zip(df['question'], df['annotator_metadata'])) if not df.empty else {}
annotator_data_str = question_steps_dict.get(st.session_state.dropdown_value, "{}")
try:
    annotator_data = ast.literal_eval(annotator_data_str)
except ValueError:
    annotator_data = {}

steps = annotator_data.get('Steps', "No steps found.")

st.markdown("##### Steps followed:")
steps = st.text_area("Edit these steps and run again if validation fails", steps, height=250)

if st.button("Re-run Prompt", key="re_run_prompt_button"):
    if validate_input(st.session_state.dropdown_value) and validate_input(steps):
        st.session_state.openai_response = "Fetching response from ChatGPT..."
        # re_run_response = get_openai_response(st.session_state.dropdown_value, steps)
        re_run_response = get_openai_response(steps)
        st.session_state.openai_response = re_run_response
        st.rerun()
    else:
        st.error("Please provide both a valid question and steps to re-run the prompt.")
        st.session_state.openai_response = "Run Prompt to get an answer from ChatGPT"
