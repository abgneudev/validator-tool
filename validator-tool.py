#prompt section
### can choose
### can randomize
### can edit

#steps section
### can edit

#results section
### actual answer
### chatGPT answer

#reports section

# ------------------------------
import streamlit as st

st.header("Validator Tool")

st.write('')
st.write('')

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

dropdown_value = st.sidebar.selectbox("Choose a prompt to test", ["Option 1", "Option 2", "Option 3"])


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
