import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import openai
from typing import Union
from pydantic import BaseModel
from langchain.chat_models import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from dotenv import load_dotenv, find_dotenv
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from fastapi import FastAPI

SQLALCHEMY_DATABASE_URL = "postgresql://default:65EvzyobfYsR@http://ep-spring-pond-821996-pooler.eu-central-1.postgres.vercel-storage.com//verceldb"

app=FastAPI()
import warnings
warnings.filterwarnings('ignore')
_=load_dotenv(find_dotenv())
openai.api_key=os.environ['OPENAI_API_KEY']
name='hachem saihi'
age='22'
gender='male'
conditions='arthritis'
allergies='dog allergy'
bloodtype='A+'
chat=ChatOpenAI(temperature=0)
memory=ConversationBufferMemory()
template="""You are a very smart medical doctor named VegaBot. \
You are great at answering questions about medicine in a concise\
and easy to understand manner, not longer than 12 words.\
you never say that you are not a doctor, and always say something helpful.\
When you don't know the answer to a question you admit\
that you don't know. \
current conversation : \
{history}
Human : {input} \
AI assistant :"""
memory.save_context({'input':f"my name is {name}. my age is {age}. my gender is {gender}. my conditions are{conditions}. my allergies are {allergies}. my bloodtype is {bloodtype}."},{'output':'okay.'})
prompt=PromptTemplate(input_variables=['history','input'],template=template)
conversation=ConversationChain(prompt=prompt,llm=chat,memory=memory,verbose=False)

@app.post('/response')
def getResponse(ch : str):
    return {'response' : conversation.predict(input=ch)}

