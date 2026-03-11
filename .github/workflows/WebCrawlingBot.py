import os
import requests

# GitHub Secrets에서 설정한 값 불러오기
TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    response = requests.post(url, data={'chat_id': CHAT_ID, 'text': text})
    
    if response.status_code == 200:
        print("텔레그램 메시지 전송 성공!")
    else:
        print(f"전송 실패: {response.text}")

if __name__ == "__main__":
    # 연동이 잘 되었는지 확인하기 위한 테스트 메시지
    send_message("🚀 깃허브 액션 봇 테스트 작동 성공! (토큰 및 챗아이디 연동 완료)")
