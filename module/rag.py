import ollama
import google.generativeai as genai
from openai import OpenAI
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from module.text_tool import Text_tool


class RAG:
    def __init__(self, model_name, provider, chunk_size=2000, overlap=100):
        self.model_name = model_name
        self.provider = provider
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.Text_tool_instance = Text_tool(self.chunk_size, self.overlap)

    def get_embedding(self, text):
        if self.provider == 'ollama':
            return self.ollama_embedding(text)
    
    def ollama_embedding(self, text):

        text = self.Text_tool_instance.split_text_with_overlap(text)
        embeddings = []
        
        try:
            for chunk in text:
                response = ollama.embeddings(
                    model=self.model_name,  # 임베딩 모델
                    prompt=chunk  # 임베딩할 텍스트
                )
                embedding = response['embedding']
                embeddings.append(embedding)

            return embeddings
        except Exception as e:
            print(f"임베딩 생성 오류: {e}")
            return None