import json
import requests
import os
from datetime import datetime, timedelta, timezone

# 1. 징우여찡구님의 1월 스케줄 데이터 (제공된 표의 두 번째 열 반영)
SCHEDULE_DATA = {
    "1": "OFF", "2": "OFF", "3": "OFF", "4": "OFF", "5": "OFF",
    "6": "OFF", "7": "마감", "8": "마감", "9": "오픈", "10": "오픈",
    "11": "오픈", "12": "OFF", "13": "마감", "14": "마감", "15": "오픈",
    "16": "오픈", "17": "OFF", "18": "마감", "19": "오픈", "20": "마감",
    "21": "마감", "22": "마감", "23": "오픈", "24": "OFF", "25": "마감",
    "26": "오픈", "27": "오픈", "28": "마감", "29": "오픈", "30": "오픈",
    "31": "OFF"
}

def get_status_emoji(status):
    """근무 상태에 따라 어울리는 하트 반환 (오픈, OFF, 마감만 사용)"""
    if status == "오픈":
        return "💛" # 아침 느낌 노란 하트
    elif status == "마감":
        return "💜" # 저녁 느낌 보라 하트
    elif status == "OFF":
        return "🤍" # 휴식 느낌 하얀 하트
    else:
        return "❤️" # 기본 빨간 하트

def send_discord_alert():
    # 깃허브 서버(UTC) 시간을 한국 시간(KST)으로 변환
    kst = timezone(timedelta(hours=9))
    now = datetime.now(kst)
    
    # 임베드 필드(Fields)에 들어갈 내용 생성
    fields_list = []
    
    # 오늘(0), 내일(1), 모레(2)
    for i in range(3):
        target_date = now + timedelta(days=i)
        month = str(target_date.month)
        day = str(target_date.day)
        
        # 요일 (0:월 ~ 6:일)
        weekday_str = ["월", "화", "수", "목", "금", "토", "일"][target_date.weekday()]

        # 데이터 조회 (징우여찡구님의 1월 스케줄을 조회)
        if month == "1": # 1월 데이터 조회
            schedule = SCHEDULE_DATA.get(day, "정보 없음")
        else:
            # 1월이 아닌 달은 '-'로 표시
            schedule = "-"
        
        # 하트 아이콘 매칭
        heart = get_status_emoji(schedule)

        # 필드 추가
        date_title = f"{month}/{day} ({weekday_str})"
        value_text = f"{heart} **{schedule}**"
        
        fields_list.append({
            "name": date_title,
            "value": value_text,
            "inline": True 
        })

    # 임베드 데이터 구성
    embed = {
        "title": "🩷 1월 징우여찡구 스케줄 알림",
        "description": "오늘 내일 모래",
        "color": 0xFFB6C1, # 파스텔 핑크 색상 코드
        "fields": fields_list,
        "footer": {
            "text": "오늘도 화이팅하세요! ❤️"
        }
    }

    # 디스코드 웹훅 전송
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("에러: 웹훅 URL이 설정되지 않았습니다.")
        return

    # content 대신 embeds 키를 사용해야 함
    data = {
        "embeds": [embed]
    }
    
    response = requests.post(webhook_url, json=data)
    
    if response.status_code == 204:
        print("전송 성공!")
    else:
        print(f"전송 실패: {response.status_code}, {response.text}")

if __name__ == "__main__":
    send_discord_alert()
