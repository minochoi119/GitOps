import requests
from bs4 import BeautifulSoup
import os

TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# 타겟 설정
KEYWORD = "용아맥"
URL = "https://gall.dcinside.com/mgallery/board/lists?id=commercial_movie"

# 디시인사이드는 봇 차단이 있어서 일반 브라우저인 척 위장해야 함
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def send_message(text):
    api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(api_url, data={'chat_id': CHAT_ID, 'text': text})

def main():
    # 1. 이전 마지막 글 번호 읽어오기
    last_id = 0
    if os.path.exists('last_id.txt'):
        with open('last_id.txt', 'r') as f:
            content = f.read().strip()
            if content.isdigit():
                last_id = int(content)

    try:
        response = requests.get(URL, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # 2. 게시판 글 목록 가져오기 (디시인사이드 'tr.us-post' 태그)
        posts = soup.select('tr.us-post')
        
        new_max_id = last_id

        # 3. 최신 글부터 아래로 탐색
        for post in posts:
            num_element = post.select_one('td.gall_num')
            # 공지사항이나 설문조사 등 글 번호가 숫자가 아닌 것은 패스
            if not num_element or not num_element.text.isdigit():
                continue 
            
            post_id = int(num_element.text)
            
            # 이미 텔레그램으로 보냈거나 확인한 예전 글이면 탐색 중단
            if last_id > 0 and post_id <= last_id:
                break

            # 이번 크롤링에서 가장 최신 글 번호 기억하기
            if post_id > new_max_id:
                new_max_id = post_id

            title_element = post.select_one('td.gall_tit a:not(.reply_num)')
            if not title_element:
                continue
                
            title = title_element.text.strip()
            link = "https://gall.dcinside.com" + title_element.get('href')

            # 4. 키워드 검사 및 알림 전송
            if KEYWORD in title:
                message = f"🍿 상업영화 갤러리 알림!\n제목: {title}\n링크: {link}"
                send_message(message)

        # 5. 확인한 최신 글 번호를 텍스트 파일로 저장
        if new_max_id > last_id:
            with open('last_id.txt', 'w') as f:
                f.write(str(new_max_id))
            print(f"업데이트 완료: {new_max_id}번 글까지 확인됨.")
        else:
            print("새로 올라온 글이 없습니다.")

    except Exception as e:
        print(f"에러 발생: {e}")

if __name__ == "__main__":
    main()
