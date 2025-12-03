import json
import requests
import os
from datetime import datetime, timedelta, timezone

# 1. OCR로 추출한 12월 신효주님 스케줄 데이터
SCHEDULE_DATA = {
  "1": "OFF", "2": "OFF", "3": "마감", "4": "마감", "5": "오픈",
  "6": "오픈", "7": "오픈", "8": "오픈", "9": "오픈", "10": "마감",
  "11": "마감", "12": "마감", "13": "오픈", "14": "오픈", "15": "OFF",
  "16": "개인일정", "17": "OFF", "18": "개인일정", "19": "마감", "20": "마감",
  "21": "마감", "22": "오픈", "23": "오픈", "24": "마감", "25": "마감",
  "26": "오픈", "27": "OFF", "28": "OFF", "29": "OFF", "30": "OFF", "31": "OFF"
}

def send_discord_alert():
    # 깃허브 서버(UTC) 시간을 한국 시간(KST)으로 변환
    kst = timezone(timedelta(hours=9))
    now = datetime.now(kst)
    
    month = str(now.month)
    day = str(now.day)

    # 12월 데이터만 있으므로 체크
    if month != "12":
        print("12월 데이터만 존재합니다.")
        return

    # 오늘 스케줄 조회
    today_schedule = SCHEDULE_DATA.get(day, "정보 없음")
    
    # 디스코드 메시지 내용 구성 (색상 및 포맷)
    content = f" **[12월 {day}일 스케줄 알림]**\n오늘 이쁜이님의 근무: **{today_schedule}** 입니다."

    # 디스코드 웹훅 전송
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("에러: 웹훅 URL이 설정되지 않았습니다.")
        return

    data = {"content": content}
    response = requests.post(webhook_url, json=data)
    
    if response.status_code == 204:
        print("전송 성공!")
    else:
        print(f"전송 실패: {response.status_code}")

if __name__ == "__main__":
    send_discord_alert()
