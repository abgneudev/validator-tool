# validator-tool

A tool with Streamlit for Model evaluation team to select a validation test case from GAIA dataset and evaluate OpenAI model against the test case.

WE ATTEST THAT WE HAVEN’T USED ANY OTHER STUDENTS’ WORK IN OUR ASSIGNMENT AND ABIDE BY THE POLICIES LISTED IN THE STUDENT HANDBOOK

Team:
Abhinav Gupta (002290559)
Dhir Thacker (002819144)
Nishita Matlani (002866323)


Here’s the complete `README.md` in markdown format based on your requirements, with `data.py` and `dashboard.py` as the only files:

---

# Assignment 2: Model Evaluation Tool using GAIA Dataset

## Project Overview
This repository contains the implementation of **Assignment 2**. It is designed to build a **Model Evaluation Tool** using Streamlit to evaluate test cases from the GAIA dataset against the OpenAI model. The tool allows users to select specific test cases, submit them to the model, and compare the results. It supports step modifications for incorrect responses and includes comprehensive feedback recording and visualization.

### Live Application Links
- **Deployed Application**: [Streamlit App Link](#)
- **Google Colab Codelabs**: [Colab Notebook Link](#)
- **GitHub Repository**: [GitHub Repo Link](#)

*(Replace `#` with the actual links post-deployment.)*

## Problem Statement
The project aims to develop a tool to streamline model evaluation using test cases from the GAIA dataset. The solution should enable real-time model response evaluation, visualization of the results, and the ability to iteratively improve the model's performance through user-guided modifications.

## Project Goals
Key tasks include:

- **Test Case Selection**: Allow users to select a specific test case from a validation file.
- **OpenAI Integration**: Send the selected test case and context data to the OpenAI model.
- **Response Comparison**: Compare the OpenAI response to the correct answer in the metadata.
- **User Feedback**: Allow users to modify incorrect responses by providing step-by-step guidance.
- **Performance Visualization**: Generate real-time visualizations to depict model performance.
- **Session Tracking**: Log all user interactions for each session for later analysis.

## Technologies Used
- **Streamlit**: Frontend application interface.
- **OpenAI API**: Model for generating answers.
- **Google Cloud Storage (GCS)**: Store and retrieve additional data files.
- **PostgreSQL - Cloud SQL**: Manage and store file bytecode.

## Data Sources
The main test case data is retrieved from the GAIA benchmark dataset, while supplementary data files such as PNG, MP3, and Excel files are stored in Google Cloud Storage.

## Pre-requisites
- **Python 3.6 or later**: [Download Python](https://www.python.org/downloads)
- **Google Cloud Credentials**: For accessing GCS and BigQuery.
- **OpenAI API Key**: For interacting with the OpenAI model.

## Project Structure
```markdown
├─ .streamlit/
│  └─ Config files for Streamlit
├─ .gitignore
├─ README.md                  # Documentation file (you are here)
├─ LICENSE                    # Licensing details
├─ requirements.txt           # List of required dependencies
├─ Architecture_Diagram.png   # Architecture Diagram for reference
├─ data.py                    # Script for retrieving and processing data
├─ dashboard.py               # Main script for running the Streamlit dashboard
```

### **File Descriptions**
- **`.streamlit/`**: Contains configuration files for the Streamlit application.
- **`.gitignore`**: Specifies files and directories to be excluded from version control.
- **`README.md`**: This documentation file, explaining the repository structure and usage.
- **`LICENSE`**: Licensing details for the project.
- **`requirements.txt`**: List of dependencies required for the project.
- **`Architecture_Diagram.png`**: A visual representation of the project’s architecture.
- **`data.py`**: Handles data retrieval from BigQuery, GCS, and integrates additional content.
- **`dashboard.py`**: Main script for creating the Streamlit dashboard, including user interfaces for selecting test cases and visualizing the results.

## Instructions for Running Locally
1. **Clone the repository**:  
   ```bash
   git clone https://github.com/your-repo-name.git
   cd your-repo-name
   ```

2. **Create a virtual environment**:  
   ```bash
   python -m venv myenv
   source myenv/bin/activate
   ```

3. **Install the requirements**:  
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit application**:  
   ```bash
   streamlit run dashboard.py
   ```

## Deployment
The Streamlit application is deployed on [Streamlit Cloud](https://streamlit.io/). You can access the live application using the following link: [**Live Streamlit App**](#).

*(Replace `#` with the actual link post-deployment.)*

## Documentation
- **[Streamlit Documentation](https://docs.streamlit.io/)**: For more information on how to extend and modify the Streamlit application.
- **GAIA Dataset on HuggingFace**: [GAIA Benchmark](https://huggingface.co/datasets/gaia-benchmark/GAIA).
- **OpenAI API Documentation**: [OpenAI API](https://openai.com/api/).

## Contribution
We attest that we haven’t used any other students’ work in our assignment and abide by the policies listed in the student handbook.
