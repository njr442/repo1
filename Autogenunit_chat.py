import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
#from langchain_google_genai import GoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
#from langchain.llms import OpenAI
import google.generativeai as gai
import os
import base64
#import vertexai
#from vertexai.generative_models import GenerativeModel, Part, FinishReason
#import vertexai.preview.generative_models as generative_models
from dotenv import load_dotenv

# from langchain_google_vertexai import VertexAI, HarmCategory, HarmBlockThreshold
load_dotenv()



gai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_res(question,prompt):
    model=gai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0], question], generation_config=generation_config)
    return response.text


generation_config = {
    "max_output_tokens": 10000,
    "temperature": 1,
    "top_p": 0.95
}

    
# ss = {
    
#     HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
#     HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
#     HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
#     HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
# }


prompt =[ """
    You have an expertise as test lead. Your goal is to provide unit test class or unit test cases or unit test senarios based on the question.
         
    Unit test class : Write a code to test the unit by recognizing the coding language. Unit Test class is consisting of an evaluation function and result functions. It's not intended to be a full-blown test suite but rather a simple mechanism to evaluate your code to determine if it is producing the correct data type and result.
    The main goal of unit testing is to ensure that each unit of the software performs as intended and meets requirements. Unit tests help make sure that software is working as expected before it is released. 
                    
    Unit test cases : Test cases are sets of actions that are executed to verify particular features or functionality of software applications. It consists of test data, test steps, preconditions, and postconditions that are developed for specific test scenarios to verify any requirement.

    Unit test scenarios : A test scenario is a collective set of test cases that helps the testing team determine the positive and negative features of the project.

    When the user question is to provide "unit test senario", give the following content information:
    1. Programming language in the following format:
    "Programming Language: "
    2. The unit test senarios in the following format:
    "   Given:
        when:
        then:"
        Example for unit test scenario is
        "successful login with valid credentials,
        Given the user is on the login page,
        when the user enters valid credentials,
        then the user is redirected to the homepage"

    When the user question is to provide "unit test cases", give the following content information:
    1.  "Programming Language: "
    2. Unit test cases:

    When the user question is to provide "unit test class", give the following content information:
    1. "Programming Language:"
    2. Unit test Class: (include all possible test logic for different methodsand with setup method)

    Answer the following questions considering the history of the conversation:

    quetion=generate {test_case_option} for the code from {TestClass}
        


    
        """]


# session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(page_title="Auto Test Gen (ATG)", page_icon="🤖",layout = "wide")
# st.title("Streaming Bot")

# Create a container for the logo and heading
col1, col2 = st.columns([1, 4])  # Adjust the ratio as needed

with col1:
    # Add logo using Streamlit's st.image function
    st.image("./Screenshot4.png", width=340, use_column_width='400')  # Ensure the path is correct

with col2:
    # Add heading with green text and centered alignmen
    st.markdown(
        "<h1 style='color: green; text-align: center;'>Auto Test Gen</h1>",
        unsafe_allow_html=True
    )
    st.divider()

# Add a new heading below
# st.markdown(
#     "<h2 style='text-align: left;color: darkblue;'>Generate Unit Test Cases</h2>",
#     unsafe_allow_html=True
# )

# Toggle between Test Cases and Test Integration
# toggle_option = st.radio("Select Option:", ("Test Cases", "Test Integration"))
# Dropdown for selecting option
with col2:
    toggle_option = st.selectbox("Select Option:", ("Unit Test", "Integration test"))

    if toggle_option == "Unit Test":
        # Display radio buttons for test cases
        test_case_option = st.radio("Select Test Type:", ("Unit Test Class" , "Unit Test Cases" ,"Unit Test Scenarios"))
    
    # # Handle the selected test case type
    # st.write(f"You selected: {test_case_option}")

    elif toggle_option == "Test Integration":
        test_case_option = "Test Integration"
        # Display the test integration option
        st.write(f"You selected: {test_case_option}")

    # File uploader for .py, .java, and .txt files
    uploaded_file = st.file_uploader("Upload your file", type=['py', 'java', 'txt'])
    TestClass = ""
    if uploaded_file is not None:
        # Show the file name and contents if it's a text-based file
        st.write("File uploaded:", uploaded_file.name)
        if uploaded_file.type in ["text/plain", "text/x-python", "text/x-java"]:
            TestClass = uploaded_file.read().decode("utf-8")
            # st.text_area("Function:", content, height=300)



    # Initialize session state for button click
    if 'is_generated' not in st.session_state:
        st.session_state.is_generated = False


    # Generate button with blue background
    if st.button("Generate", key="generate_button"):
        st.markdown("<div style='color: white;'>Generating...</div>", unsafe_allow_html=True)
        st.session_state.is_generated = True  # Set the variable to True

    # CSS for button styling (optional)
    st.markdown(
        """
        <style>
        .stButton>button {
            background-color: darkblue;  /* Blue color */
            color: white;                /* Text color */
            border: none;                /* Remove border */
            padding: 10px 20px;         /* Padding */
            border-radius: 5px;         /* Rounded corners */
            cursor: pointer;             /* Pointer cursor */
        }
        </style>
        """,
        unsafe_allow_html=True
)    


# conversation
# for message in st.session_state.chat_history:
#     if isinstance(message, AIMessage):
#         with st.chat_message("AI"):
#             st.write(message.content)
#     elif isinstance(message, HumanMessage):
#         with st.chat_message("Human"):
#             st.write(message.content)

# user input
#question = st.chat_input("Type your message here...")

# if question is not None and question != "":
#     #custom_message = f"User asked: {question}\nCode provided: {TestClass}"
#     st.session_state.chat_history.append(HumanMessage(content=question))
# elif question is None and question == "":
#     st.session_state.chat_history.append(HumanMessage(content=TestClass))


if TestClass is not None and TestClass != "":
    custom_message = f"Generate: {test_case_option}\nfor Code provided: {TestClass}\n .use the instructions provided in prompt"
    st.session_state.chat_history.append(HumanMessage(content=custom_message))

    with st.chat_message("Human"):
        st.markdown(custom_message)

    with st.chat_message("AI"):
        response = st.write(get_res(custom_message, prompt))

        #print(response)
        #st.write(response)

    #st.session_state.chat_history.append(AIMessage(content=response))


#chat history
#Token optimization

#file out put

