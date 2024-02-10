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
  print("ok")


# read_and_save_one_story("story1", "one_piece")
# read_and_save_one_story("story2", "one_piece")
# read_and_save_one_story("story3", "one_piece")
# read_and_save_one_story("story4")

# query
vector = get_embedding("""
Their journey took them through treacherous seas, perilous encounters, and fierce battles against powerful enemies. But Luffy and his crew faced every challenge with unwavering resolve, fueled by their unbreakable bonds of friendship. They laughed, cried, trusted, and fought together, forming an unyielding unity that made them virtually unstoppable.

In their pursuit of the One Piece, Luffy and his crew discovered the true meaning of courage, sacrifice, and loyalty. They encountered allies who became family, enemies who became allies, and obstacles that tested their determination. And through it all, they never lost sight of their ultimate goal.
""")
data = collection.query(query_embeddings=vector, n_results=4) # 选择查找的数量
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
print(df)
