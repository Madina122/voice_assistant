import os
from langchain_groq import ChatGroq

os.environ["GROQ_API_KEY"] = "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"

# Обращаемся к LLM
class LLM:
    def __init__(self):
        self.llm = ChatGroq(model="llama3-70b-8192")
        
    def llm_work(self, user_message):
        system_message = "Ты полезный ассистент. Отвечай на вопросы кратко и понятно"
        
        message = [
            {'role': 'system', 'content': system_message},
            {'role':'user', 'content':user_message}
        ]
        response = self.llm.invoke(message)

        return response.content