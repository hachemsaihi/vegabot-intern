import os
import openai
from langchain.chat_models import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from dotenv import load_dotenv, find_dotenv
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from flask import Flask, jsonify, request

app = Flask(__name__)
import warnings
warnings.filterwarnings('ignore')
_=load_dotenv(find_dotenv())
openai.api_key=os.environ['OPENAI_API_KEY']
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
#memory.save_context({'input':f"my name is {name}. my age is {age}. my gender is {gender}. my conditions are{conditions}. my allergies are {allergies}."},{'output':'okay.'})
prompt=PromptTemplate(input_variables=['history','input'],template=template)
conversation=ConversationChain(prompt=prompt,llm=chat,memory=memory,verbose=False)
@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form['user_input']
    bot_response = conversation.predict(input=user_input)
    response_data = {'response': bot_response}
    return jsonify(response_data)