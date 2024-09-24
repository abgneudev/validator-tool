import streamlit as st
import random
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import ast
import openai 

<<<<<<< Updated upstream

# Integrating OpenAI API
openai.api_key = 'Open_AI_API'

=======

# Integrating OpenAI API
openai.api_key = 'Open_AI_API"

# Function to get OpenAI response with optional steps for "Re-run Prompt"
>>>>>>> Stashed changes
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
    if not input_value:
        return False
    return True

# Connecting Database on GCP
try:
    conn = psycopg2.connect(
<<<<<<< Updated upstream
        host="104.196.119.128",
        port="5432",
        user="postgres-user",
        password="zqA#q>pv`h3UG.XH",
        database="postgres"
=======
        host="XXX.XXX..XXX",
        port="XXXX",
        user="XXXX-XXXX",
        password="XXXXX#XXXX",
        database="xxxxxx"
>>>>>>> Stashed changes
    )
    
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    
    engine = conn
except Exception as e:
    engine = None

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

<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
# Sidebar Navigation
if not df.empty:
    levels = ['All'] + sorted(df['level'].unique().tolist())
else:
    levels = ['All']
<<<<<<< Updated upstream

selected_level = st.sidebar.selectbox("Select difficulty level:", levels)

if selected_level != 'All' and not df.empty:
    filtered_df = df[df['level'] == selected_level]
    questions = filtered_df['question'].tolist()
else:
    questions = df['question'].tolist() if not df.empty else []
=======
>>>>>>> Stashed changes

selected_level = st.sidebar.selectbox("Select difficulty level:", levels)

if selected_level != 'All' and not df.empty:
    filtered_df = df[df['level'] == selected_level]
    questions = filtered_df['question'].tolist()
else:
    questions = df['question'].tolist() if not df.empty else []

col1, col2 = st.sidebar.columns([2, 1])

with col1:
<<<<<<< Updated upstream
    dropdown_value = st.sidebar.selectbox("Choose a prompt to test", questions)
=======
    # Display dropdown with questions and clear ChatGPT Answer on selection change
    dropdown_value = st.sidebar.selectbox("Choose a prompt to test", questions, on_change=lambda: st.session_state.update({'openai_response': ''}))
>>>>>>> Stashed changes

with col2:
    if st.sidebar.button("Randomize", key="randomize_button"):
        if selected_level != 'All' and not df.empty:
            filtered_questions = df[df['level'] == selected_level]['question'].tolist()
        else:
            filtered_questions = questions
        
        if filtered_questions:
            dropdown_value = random.choice(filtered_questions)
            if validate_input(dropdown_value):
                openai_response = get_openai_response(dropdown_value)
                st.session_state['openai_response'] = openai_response
            else:
                st.sidebar.error("No valid question selected.")
        else:
            st.sidebar.error("No questions available for the selected level.")

st.sidebar.header("Prompt:")
prompt_text = dropdown_value if dropdown_value else "No question selected"
st.sidebar.write(prompt_text)

if st.sidebar.button("Run Prompt", key="run_prompt_button"):
    if validate_input(dropdown_value):
        openai_response = get_openai_response(dropdown_value)
        
        st.session_state['openai_response'] = openai_response  
    else:
        st.sidebar.error("Please select a valid question.")

col1, col2 = st.columns(2)

if not df.empty:
    if selected_level != 'All':
        filtered_df = df[df['level'] == selected_level]
    else:
        filtered_df = df
    question_answer_dict = dict(zip(filtered_df['question'], filtered_df['final_answer']))
    final_answer = question_answer_dict.get(dropdown_value, "No final answer found.")
else:
    final_answer = "No data available."

# Main Section
st.header("Validator Tool")

st.write('')

response_placeholder = st.empty()

with col1:
    st.markdown("##### Actual Answer")
    st.write(final_answer)

with col2:
    st.markdown("##### ChatGPT Answer")
    if 'openai_response' in st.session_state:
        st.write(st.session_state['openai_response'])
    else:
        st.write("No response yet. Click 'Run Prompt' to get an answer.")

st.divider()

if not df.empty:
    if selected_level != 'All':
        filtered_df = df[df['level'] == selected_level]
    else:
        filtered_df = df
    question_steps_dict = dict(zip(filtered_df['question'], filtered_df['annotator_metadata']))
    annotator_data_str = question_steps_dict.get(dropdown_value, "{}")
    try:
        annotator_data = ast.literal_eval(annotator_data_str)
    except ValueError:
        annotator_data = {}

    steps = annotator_data.get('Steps', "No steps found.")
else:
    steps = "No steps available."

st.markdown("##### Steps followed:")
steps = st.text_area("Edit these steps and run again if validation fails", steps)

col1, col2 = st.columns([2,1])

with col1:
    if st.button("Re-run Prompt", key="re_run_prompt_button"):
        if validate_input(dropdown_value) and validate_input(steps):
            re_run_response = get_openai_response(dropdown_value, steps)

            st.session_state['openai_response'] = re_run_response

            st.rerun() 
        else:
            st.error("Please provide both a valid question and steps to re-run the prompt.")
<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes
