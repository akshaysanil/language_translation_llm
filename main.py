import os
import dotenv
from fastapi import FastAPI
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langserve import add_routes

dotenv.load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

model = ChatGroq(model = "Gemma2-9b-It", groq_api_key = groq_api_key)

parser = StrOutputParser()

prompt = ChatPromptTemplate.from_messages(
    [
        ('system', "Translate the following into {language}:"),
        ('user', '{user_input}')
    ]
)

# combine all together and create chain
chain = prompt | model | parser

# chain.invoke({"language": "French", "user_input": "Hello"})

## app defenition
app = FastAPI(title='Langchain Server',
              version='1.0',
              description='A simple API server using Langchain runnable interfaces')

# adding chain routes 
add_routes(
    app,
    chain,
    path="/chain"
)

if __name__== '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)