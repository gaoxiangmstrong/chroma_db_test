from bs4 import BeautifulSoup
import requests
# # 网站的 URL
# url = "https://ieltstutors.org/academic-word-list/"

# # 向网站发送请求
# response = requests.get(url)

# # 检查请求是否成功
# def get_words():_list
#   if response.status_code == 200:
#       print("请求成功")
#       # 解析网页的 HTML 内容
#       soup = BeautifulSoup(response.text, 'html.parser')

#       # 查找所有具有指定类的 'a' 标签
#       a_tags = soup.find_all('a', class_='wpg-list-item-title')

#       # 从每个 'a' 标签中提取文本
#       words = [tag.text.strip() for tag in a_tags]

#       # 打开acdemic_word_list.txt文件保存上面的words list line by line
#       with open('IELTS/acdemic_word_list.txt', 'w') as f:
#           for word in words:
#               f.write(word + '\n')
#   else:
#       words = []



import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
nltk.download('punkt') # 
nltk.download('averaged_perceptron_tagger') # 词性标注

# 读取文件内容
def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# 提取短语
def extract_phrases(text):
    # 分词
    tokens = word_tokenize(text)
    # 词性标注
    tagged_tokens = pos_tag(tokens)

    # 定义规则提取短语（例如名词短语）
    phrases = []
    current_phrase = []

    for word, tag in tagged_tokens:
        if tag.startswith('NN') or tag.startswith('JJ') or tag.startswith('NNP'):
            current_phrase.append(word)
        else:
            if current_phrase:
                phrases.append(' '.join(current_phrase))
                current_phrase = []

    if current_phrase:
        phrases.append(' '.join(current_phrase))

    return phrases

# 把词汇写入
def write_words(words,title):
  with open(f"TOFEL/{title}.txt", "w") as f:
    for word in words:
      f.write(word + "\n")

# 主函数
def main():
    file_path = 'reading.txt'  # 替换为您的文件路径
    text = read_file(file_path)
    phrases = extract_phrases(text)
    title = phrases[0]
    write_words(phrases,title)

if __name__ == "__main__":
    main()
