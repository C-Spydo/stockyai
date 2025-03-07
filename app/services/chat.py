import jsonpickle
from langchain.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
from app.dtos.chat_setting import ChatSetting
from app.dtos.prompt import Prompt
from app.repository.chat import get_chat_by_id
from app.repository.user import get_user_by_email
from ..enums import ActiveStocks
from langchain.chains.conversation.base import ConversationChain
from app.helpers import add_record_to_database
from app.models import Chat
from langchain_core.messages import SystemMessage
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from ..constants import PINCONE_INDEX
from flask import abort


def start_chat(request: ChatSetting):
    user = validate_user(request['email'])

    chat_memory = create_chat_memory()

    context = retrieve_relevant_documents(request['prompt'])
    
    langchain_conversation = create_conversation_chain(get_llm(), chat_memory, get_prompt_template(context))

    ai_response = langchain_conversation.invoke({"input": request['prompt']})

    chat = Chat(user_id=user.id, stock="", memory=jsonpickle.encode(chat_memory))
    add_record_to_database(chat)

    return {"chat_id": chat.id, "chat_history": chat_memory.load_memory_variables({})["chat_history"] ,"ai_response": ai_response}

def prompt_bot(request: Prompt):
    chat = get_chat_by_id(request['chat_id'])

    chat_memory = chat.deserialize_chat_memory()

    context = retrieve_relevant_documents(request['prompt'])

    langchain_conversation = create_conversation_chain(get_llm(), chat_memory, get_prompt_template(context))

    ai_response = langchain_conversation.predict(input=request['prompt'])

    chat.update_chat_memory(chat_memory)

    return {"chat_id": chat.id, "chat_history": chat_memory.load_memory_variables({})["chat_history"] ,"ai_response": ai_response}

def get_llm():
    llm = ChatGroq(
        model="llama3-8b-8192",
        temperature=0.4,
        max_tokens=250,
        timeout=3,
        max_retries=2
    )

    return llm


def create_conversation_chain(llm, chat_memory, prompt_template):
    return ConversationChain(
        llm=llm,
        memory=chat_memory,
        prompt=prompt_template,
        verbose=True  
    )


def retrieve_relevant_documents(prompt):  
    vectorstore = PineconeVectorStore(index_name=PINCONE_INDEX, embedding=HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2"))
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    relevant_documents = retriever.invoke(prompt)

    return "\n\n".join([doc.page_content for doc in relevant_documents])

def create_chat_memory():
    return ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=False,
            ai_prefix="AI",
            human_prefix="User"
        )

def get_system_message():
     return f"""
        You are a chatbot assistant on stocks.
        You are asked to generate short and accurate answers using the provided context.
        Do not formulate answers,only use the retrieved documents, but do not sound like you are using a retrieved document.
        If question is outside context made available to you, simply state so\n
        """
    

def get_prompt_template(context):
    system_message = get_system_message()

    return PromptTemplate(
        input_variables=["input", "chat_history"],
        template=(
                f"{system_message}"
                "The following is a conversation between User and AI:\n\n"
                "{chat_history}\n\n"
                f"Retrieved Document: {context} \n\n"
                "User question: {input}")
    )
    
def validate_user(email: str):
    user = get_user_by_email(email)

    if user is None:
        raise abort(404, "User not found")
    
    return user


def validate_stock(stock: str):
    if stock not in ActiveStocks.__members__:
        raise abort(400, f"Invalid stock: {stock}. Available stocks: {', '.join(ActiveStocks.__members__.keys())}")

    return stock
