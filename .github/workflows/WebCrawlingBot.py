import requests
from bs4 import BeautifulSoup
import os

# GitHub Secrets에서 텔레그램 정보 가져오기
TOKEN = os.environ.get('8577307201:AAFaLjfoRQCQ-zySoFtfxc0GJvWahvNOUXM')
CHAT_ID = os.environ.get('467275132')
KEYWORD = "용아맥"

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={'chat_id': CHAT_ID, 'text': text})

# 크롤링 로직 예시 (게시판 구조에 따라 수정 필요)
url = "https://gall.dcinside.com/mgallery/board/lists?id=commercial_movie"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# 예: 게시판 제목들을 가져온다고 가정
posts = soup.select('.post-title')

for post in posts:
    title = post.text
    link = post.get('href')
    
    # 제목에 키워드가 포함되어 있다면 알림 전송
    if KEYWORD in title:
        message = f"새 글 알림!\n제목: {title}\n링크: {link}"
        send_message(message)