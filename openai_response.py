from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))



# 写一个可以生成故事并保存故事的函数
def save_one_story(address, title):
  """保存故事以及有标题来生成想要的故事故事"""
  completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages= [
      {"role": "system", "content": "You are a poetic assistant, skilled in generating complex story with creative flair."},
      {"role": "user", "content": f"write a story about {title} in 200 words"}
    ]
  )
  with open(f"stories/{address}.txt", "w") as f:
    f.write(completion.choices[0].message.content)

save_one_story(address="story6", title="traveling around the world")