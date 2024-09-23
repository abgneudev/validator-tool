import streamlit as st
import random
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import ast
import psycopg2
import openai 

openai.api_key = 'Open_AI_API'

# Function to get OpenAI response with steps for "Re-run Prompt"
def get_openai_response_with_steps(question, steps):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert assistant capable of answering a wide variety of fact-based questions. Provide direct and accurate answers across different topics, always ensuring precision and clarity."
                },
                {
                    "role": "user",
                    "content": f"The user provided the following steps to solve the question:\n{steps}\n\nThe original question is: {question}"
                }
            ],
            temperature=0.2,  # Lower temperature for focused and deterministic answers
            max_tokens=1000,  # Adjust max tokens as needed
            top_p=1,
            frequency_penalty=0.5,  # Discourage repeating phrases
            presence_penalty=0.5  # Encourage introducing new relevant information
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error fetching response: {str(e)}"


# Function to get OpenAI response (normal Run Prompt without steps)
def get_openai_response(question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert assistant capable of answering a wide variety of fact-based questions. Provide direct and accurate answers across different topics, always ensuring precision and clarity."
                },
                {
                    "role": "user",
                    "content": "Who was the blue fish in Finding Nemo?"
                },
                {
                    "role": "assistant",
                    "content": "The blue fish in 'Finding Nemo' is named Dory."
                },
                {
                    "role": "user",
                    "content": question  # This is where the user's selected prompt will be inserted
                }
            ],
            temperature=0.5,
            max_tokens=2048,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error fetching response: {str(e)}"


# Database connection
try:
    conn = psycopg2.connect(
        host="xxx.xxxx.xxx",
        port="xxxx",
        user="xxxxxxx-xxxx",
        password="xxxxx#xx>xx`xx.xx",
        database="xxxxxx"
    )
    
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    
    engine = conn
except Exception as e:
    engine = None

st.header("Validator Tool")

st.write('')

# Fetch data if the connection is successful
if engine:
    try:
        query = 'SELECT * FROM gaia.data;'
        df = pd.read_sql(query, conn)
    except Exception as e:
        st.sidebar.error(f"Error executing query: {str(e)}")
        df = pd.DataFrame()
else:
    df = pd.DataFrame()

# Extract questions for the dropdown
if not df.empty:
    questions = df['question'].tolist()
else:
    questions = []

col1, col2 = st.sidebar.columns([2,1])

with col1:
    # Display dropdown with questions
    dropdown_value = st.sidebar.selectbox("Choose a prompt to test", questions)

# Placeholder for ChatGPT response
response_placeholder = st.empty()

# Randomize button in the sidebar
with col2:
    if st.sidebar.button("Randomize", key="randomize_button"):
        dropdown_value = random.choice(questions)

# Sidebar prompt section
st.sidebar.header("Prompt:")
prompt_text = dropdown_value if dropdown_value else "No question selected"
st.sidebar.write(prompt_text)

# "Run Prompt" button logic (without steps)
if st.sidebar.button("Run Prompt", key="run_prompt_button"):
    if dropdown_value:
        # Fetch the GPT-4 response for the selected question
        openai_response = get_openai_response(dropdown_value)
        
        # Store OpenAI response in session state to persist across reruns
        st.session_state['openai_response'] = openai_response  
    else:
        st.sidebar.write("Please select a question first.")

col1, col2 = st.columns(2)

# Fetch the actual answer for the selected question
if not df.empty:
    question_answer_dict = dict(zip(df['question'], df['final_answer']))
    final_answer = question_answer_dict.get(dropdown_value, "No final answer found.")
else:
    final_answer = "No data available."

# Display the actual and ChatGPT answers
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

# Initialize 'steps' properly before the "Re-run Prompt" button logic
if not df.empty:
    question_steps_dict = dict(zip(df['question'], df['annotator_metadata']))
    annotator_data_str = question_steps_dict.get(dropdown_value, "{}")
    try:
        annotator_data = ast.literal_eval(annotator_data_str)
    except ValueError:
        annotator_data = {}

    steps = annotator_data.get('Steps', "No steps found.")
else:
    steps = "No steps available."

# Display steps followed in the task
st.markdown("##### Steps followed:")
steps = st.text_area("Edit these steps and run again if validation fails", steps)

# Buttons for comparing answers and re-running the prompt
col1, col2 = st.columns([2,1])

with col1:
    # "Answers Match" button
    if st.button("Answers Match", key="answers_match_button"):
        st.write("You clicked Answers Match.")
    
    # "Re-run Prompt" button logic (with steps)
    if st.button("Re-run Prompt", key="re_run_prompt_button"):
        if dropdown_value and steps:
            # Fetch the GPT-4 response for the selected question and steps
            re_run_response = get_openai_response_with_steps(dropdown_value, steps)

            # Store OpenAI response in session state to persist across reruns
            st.session_state['openai_response'] = re_run_response

            # After "Re-run Prompt", update the displayed answer
            with col2:
                st.markdown("##### ChatGPT Answer")
                st.write(st.session_state['openai_response'])
        else:
            st.write("Please provide both the question and steps to re-run the prompt.")

# Display database results if available
if not df.empty:
     st.header("Database Results")
     st.dataframe(df)
