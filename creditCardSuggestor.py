import streamlit as st
import requests
from bs4 import BeautifulSoup
import json
from streamlit.components.v1 import html
from openai import OpenAI 

def getResponse(content, user_message, api_key):
    messages=[{"role":"system","content":"you are a expert text to diagram bot , you are excellent and capable of writing mermaid js script to generate diagram from text, and always respond back in json format"},
              {"role":"system","content":"below given is the details of various credit cards offer by a bank which is also mentioned in the same use it as your knowledge base"+content},
              {"role":"system","content":"Below are the mentioned requirent of the user " + user_message},
              {"role":"system","content":"Now you have to suggest the best credit card for the user based on his requirement ALWAYS respond back in json format with code as key and mermaid code as value, another key value pair should be explaination with reason why you are suggesting this card to the user"},
              {"role":"system","content":"And always remember make mermaid js showing the feature offered by the card you have suggested"},]
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        response_format={ "type": "json_object" },
        temperature=0.7
            
        )
    response=json.loads(completion.choices[0].message.content)
    code=response.get("code")
    explaination=response.get("explanation")
    return code,explaination

def fetch_webpage_content(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return ' '.join(soup.stripped_strings)
    except Exception as e:
        return f"Error fetching page: {e}"


def display_mermaid_diagram(code):
    # Example Mermaid diagram
    
    code = code.replace("\\n", "\n")
    code = code.replace("\\", "")
    code = code.replace(";", "")
    code= code.replace("mermaid", "")
    code= code.replace("```", "")
      
    
    diagram = code
    diagram = code
    # HTML and JS to render the Mermaid diagram
    mermaid_html = f"""
        <div class="mermaid">
            {diagram}
        </div>
        <script src="https://cdn.jsdelivr.net/npm/mermaid@8.13.5/dist/mermaid.min.js"></script>
        <script>
        function loadMermaid() {{
            if (typeof mermaid === 'undefined') {{
                setTimeout(loadMermaid, 100);
            }} else {{
                mermaid.initialize({{ startOnLoad: true }});
            }}
        }}
        loadMermaid();
        </script>
    """
    html(mermaid_html,width=1000,height=1000)




st.title("Credit card suggestor")


user_url = st.text_input("Enter the URL of the website:")



user_message = st.text_area("Enter details like your income, requirements, etc.")
api_key = st.text_input("Enter your API key:")

if st.button("Submit"):
    
    content = fetch_webpage_content(user_url)
    code,explaination=getResponse(content, user_message, api_key)

    st.write(explaination)
    display_mermaid_diagram(code)




