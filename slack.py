import requests
import json

# Slack에서 발급받은 Webhook URL
WEBHOOK_URL = "https://hooks.slack.com/services/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"

# 보낼 메시지 내용
payload = {
    "text": "안녕하세요! 🎉 Python에서 Slack으로 보낸 메시지입니다."
}

# 요청 전송
response = requests.post(WEBHOOK_URL, data=json.dumps(payload))

# 결과 확인
if response.status_code == 200:
    print("✅ 메시지 전송 성공!")
else:
    print("❌ 메시지 전송 실패:", response.text)
