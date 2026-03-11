import cloudscraper # requests 대신 사용
from bs4 import BeautifulSoup
import os

TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

KEYWORD = "용아맥"
URL = "https://gall.dcinside.com/mgallery/board/lists?id=commercial_movie"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'https://gall.dcinside.com/'
}

def send_message(text):
    api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    cloudscraper.create_scraper().post(api_url, data={'chat_id': CHAT_ID, 'text': text})

def main():
    last_id = 0
    if os.path.exists('last_id.txt'):
        with open('last_id.txt', 'r') as f:
            content = f.read().strip()
            if content.isdigit():
                last_id = int(content)

    try:
        # 일반 requests 대신 cloudscraper 사용
        scraper = cloudscraper.create_scraper()
        response = scraper.get(URL, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # [디버깅] 차단당했는지 확인하기 위해 페이지 제목 출력
        page_title = soup.title.text if soup.title else "제목 없음"
        print(f"현재 로드된 페이지 제목: {page_title}")

        posts = soup.select('tr.us-post')
        
        # 글 목록을 아예 못 가져왔다면 차단당한 것
        if not posts:
            print("경고: 게시글 목록을 찾을 수 없습니다. (IP 차단 의심)")
            return

        new_max_id = last_id

        for post in posts:
            num_element = post.select_one('td.gall_num')
            if not num_element or not num_element.text.isdigit():
                continue 
            
            post_id = int(num_element.text)
            
            if last_id > 0 and post_id <= last_id:
                break

            if post_id > new_max_id:
                new_max_id = post_id

            title_element = post.select_one('td.gall_tit a:not(.reply_num)')
            if not title_element:
                continue
                
            title = title_element.text.strip()
            link = "https://gall.dcinside.com" + title_element.get('href')

            if KEYWORD in title:
                message = f"🍿 상업영화 갤러리 알림!\n제목: {title}\n링크: {link}"
                send_message(message)

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
