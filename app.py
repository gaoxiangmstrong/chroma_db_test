import chromadb
from dotenv import load_dotenv
from embedding import get_embedding
import chromadb.utils.embedding_functions as embedding_functions
import os
import pandas as pd

load_dotenv()

client = chromadb.PersistentClient(path="db/")

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.environ.get("OPENAI_API_KEY"),
    model_name="text-embedding-ada-002"
)


# 删除collection
# client.delete_collection(name="my_stories")

# 创建或拿到collection
collection = client.get_or_create_collection(name="my_stories", embedding_function=openai_ef)  # 设置collection名字


# 保存到chromadb
def read_and_save_one_story(address):
  with open(f"stories/{address}.txt") as f:
    story = f.read()

    # 添加一个故事到collection
    collection.add(
      documents = story,
      ids = f"{address}"
    )
  print("saved")



# read_and_save_one_story("story5")
# read_and_save_one_story("story6")

# query
query_text = """
Their journey took them through treacherous seas, perilous encounters, and fierce battles against powerful enemies. But Luffy and his crew faced every challenge with unwavering resolve, fueled by their unbreakable bonds of friendship. They laughed, cried, trusted, and fought together, forming an unyielding unity that made them virtually unstoppable.

In their pursuit of the One Piece, Luffy and his crew discovered the true meaning of courage, sacrifice, and loyalty. They encountered allies who became family, enemies who became allies, and obstacles that tested their determination. And through it all, they never lost sight of their ultimate goal.
"""
# 拿到文章的embeddings然后返回一个pandas表格
def query_and_process_results(query_text, n_results=6):
    """
    对集合执行查询，并处理查询结果。
    
    参数:
    - query_text: str, 查询文本。
    - n_results: int, 返回结果的数量。
    
    返回:
    - df: DataFrame, 查询结果的DataFrame。
    """
    vector = get_embedding(query_text)
    data = collection.query(query_embeddings=vector, n_results=n_results) # 选择查找的数量
    # Adjusting the data to ensure all lists are of the same length
    ids = data['ids'][0]
    distances = data['distances'][0]
    documents = data['documents'][0]

    # Truncating the lists to the length of the shortest list
    min_length = min(len(ids), len(distances), len(documents))
    ids = ids[:min_length]
    distances = distances[:min_length]
    documents = documents[:min_length]

    # Truncating document excerpts to 100 characters
    document_excerpts = [doc[:30] for doc in documents]

    # Creating a DataFrame
    df = pd.DataFrame({
        'Story ID': ids,
        'Distance Score': distances,
        'Document Excerpt': document_excerpts
    })

    # Display the DataFrame
    return df


print(query_and_process_results(query_text=query_text, n_results=6))
