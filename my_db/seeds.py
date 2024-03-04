import sqlite3
import os

def connect_to_databse():
  con = sqlite3.connect("/Users/gaoxiangmstronggmail.com/Desktop/chroma_test/ai.db")
  cur = con.cursor()
  return con, cur

con, cur = connect_to_databse()

# try:
#   cur.execute("INSERT INTO users('username', 'email') VALUES('admin', 'admin@gmail.com')")
#   con.commit()
# except sqlite3.IntegrityError:
#   print("admin saved")



res = cur.execute("SELECT * FROM users WHERE username = 'gaoxiang' ")

id, username, email = res.fetchall()[0]

# save stories to ai.db
def save_all_stories():
  """"
  保存所有在stories文件中的故事
  """
  folder_path = "/Users/gaoxiangmstronggmail.com/Desktop/chroma_test/stories"
  file_names = [file_name for file_name in os.listdir(folder_path)]
  data = []
  for file in file_names:
    with open(f"{folder_path}/{file}", "r") as f:
      content = f.read()
      data.append((file, content))
  return data



# cur.executemany("INSERT INTO stories('title', 'content') VALUES(?, ?)")
# con.commit()

# res = cur.execute("SELECT id FROM stories")
# print(res.fetchone()[0])