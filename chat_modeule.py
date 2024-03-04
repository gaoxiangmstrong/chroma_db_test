from openai import OpenAI
import os
import sys
from dotenv import load_dotenv
load_dotenv()
from persona import akira
from my_db.seeds import username, connect_to_databse
client = OpenAI()
import json


con, cur = connect_to_databse()

class Chat:
    def __init__(self, story):
        self.conversation_history = [
            {"role": "system", "content": f"{akira}"},  
            {"role": "user", "content": f"Let's begin with the {story}. You need to keep asking until I understand the story. if user is not clear to the answer you need to correct him and provide the next question"}
        ]
        
    def get_last_message_content(self):
        return self.conversation_history[-1]["content"]
    
    def is_last_message_from_AI(self):
        # 直接返回条件表达式的结果
        return self.conversation_history[-1]["role"] == "assistant"
    
    def add_assistant_message(self):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=self.conversation_history,
                temperature=0.8
            )
        except Exception as e:
            print(f"Error adding assistant message: {e}")
            return
        
        # 拿到请求的结果
        role = response.choices[0].message.role
        content = response.choices[0].message.content
        self.conversation_history.append({"role": role, "content": content})
        
    def get_message(self):
        # 简化函数
        return self.get_last_message_content()
    
    def add_user_message(self, user_message):
        self.conversation_history.append({"role": "user", "content": user_message})
    
    def get_conversation_history(self):
        return self.conversation_history


folder_path = "./stories"
file_names = [file_name for file_name in os.listdir(folder_path)]

def main():
    if username == "gaoxiang":
        print("成功login")
    selected_story = input("Select the story you want you read: ").strip()
    # 选择一个故事
    if selected_story in file_names:
        with open(f"stories/{selected_story}", "r") as f:
            the_story = f.read()
            chat = Chat(the_story)
            try:
              while True:
                  # if last message_is system message
                  if chat.is_last_message_from_AI():
                      user_message = input("your answer: ")
                      chat.add_user_message(user_message)
                  else:
                      chat.add_assistant_message()
                      print(chat.get_last_message_content())              
            except EOFError:
                ###
                # 保存对话历史
                ###
                conversation_history = chat.get_conversation_history()
                user_id = 1

                # select story_id
                id_query = f'SELECT "id" FROM "stories" WHERE "title" = "{selected_story}"'
                story_id = int(cur.execute(id_query).fetchone()[0]) # number
                conversation_history_str = json.dumps(conversation_history)

                insert_query = "INSERT INTO conversation_histories (user_id, story_id, conversation) VALUES (?, ?, ?)"
                cur.execute(insert_query, (user_id, story_id, conversation_history_str))
                con.commit()
                print("history saved")

                
                sys.exit()


              
            

if __name__ == "__main__":
    main()
        



