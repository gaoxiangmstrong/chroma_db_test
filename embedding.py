from dotenv import load_dotenv
from openai import OpenAI
import os


load_dotenv()
openai = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# 故事转向量
def get_embedding(texts):
    response = openai.embeddings.create(
        input=texts,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding