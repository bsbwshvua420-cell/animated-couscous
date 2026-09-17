import os
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Gom chuỗi Authorization dài để tránh lỗi ngắt dòng
auth_token = (
    "Bearer "
    "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9."
    "eyJ1c2VyIjoiMDE2ODI5NjIxODIiLCJpbWVpIjoiNTEwMDEtMWIxYjAyMWQ1NDgyZjA4MWVkODY1ZmJkM2UwMDAwYWYyNzU4ZmIxMmUxOGRiZGUzZGMwOTM1MWI5NDI1ZWY1MyIsImhJbWVpIjoiOEZiSVBHVkI4dEsyajNkRWd2dWZURDZXTU5LWkhVMmxtWWdMRlZUNDZLOXhNM055bzRxdXRYV1FYNTlPbU1NSkh1c0pzck9ub1pqazl6RysveXAzaktidnlseER2ZHhTZC9mSlV1cUJESms9IiwiTUFQX1NBQ09NX0NBUkQiOjAsIk5BTUUiOiJUcuG6p24gTmjhuq10IEhvw6BuZyIsIkRFVklDRV9PUyI6ImlvcyIsImFQUF9WRVIiOjUxNTAwLCJhZ2VudF9pZCI6MTEwMzM1MTY0LCJzZXNzaW9uS2V5IjoicGZuRkRkUnA5SldUQTZuU2ZoN252SjQ2b3g4VWs0Qmg3V1BrSWZFS3p0SjluMVRPQmpUOVNRPT0iLCJ1c2VyX3R5cCI6MSw notammentiOiJtb21vIiwicmFwaWRfaWQiOiJQd3BBbkAzTlp4YzU4Rnp3ZDhkcDNCakJ0a2VlVlJZQlcveEQxTWZLZmtjdHJCcFpQaGdZV1VWb0U3OWpWZURPcGdDQU85VVpqRT0iLCJ1aWQiOiIwMTY4Zjk2MjE4MiIsImV4cCI6MTc4OTkwNzk1N30."
    "pf0dxo-9L72AKhZ-FSB7hZ9M0WKaestpSCkGwFIqfyXHAd1jWBMgVSpSsEyv3P6JDfFneDYRLRG6NGlKCl-ktxmum2lIvcjJtGhfIt_Wly5nT9fAEcTCyWA5TQFbe03VjLEez24L8pIMydgb0-yh_eO4jG8t1eimJkO1ZRUGKWrjsKlk5rhp_GvQyq_OORNE_I0h8lILEv1jpeiYadMEgB6-3FjBW9kIlPAjdtB0CcIp1gyUasM2BoE6v0eAN_Sp8_7TE9VR8wffBBalPS1WidgLNfXLgrT5ZgdMJJzro238pMBTgI5_o5Jil7MfHh9E92t0SzOoEvN62R8YX1XQqw"
)

# Thay thế bằng đoạn mã sạch hơn không bị lỗi kí tự
auth_token_clean = (
    "Bearer"
    " eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VyIjoiMDE2ODI5NjIxODIiLCJpbWVpIjoiNTEwMDEtMWIxYjAyMWQ1NDgyZjA4MWVkODY1ZmJkM2UwMDAwYWYyNzU4ZmIxMmUxOGRiZGUzZGMwOTM1MWI5NDI1ZWY1MyIsImhJbWVpIjoiOEZiSVBHVkI4dEsyajNkRWd2dWZURDZXTU5LWkhVMmxtWWdMRlZUNDZLOXhNM055bzRxdXRYV1FYNTlPbU1NSkh1c0pzck9ub1pqazl6RysveXAzaktidnlseER2ZHhTZC9mSlV1cUJESms9IiwiTUFQX1NBQ09NX0NBUkQiOjAsIk5BTUUiOiJUcuG6p24gTmjhuq10IEhvw6BuZyIsIkRFVklDRV9PUyI6ImlvcyIsImFQUF9WRVIiOjUxNTAwLCJhZ2VudF9pZCI6MTEwMzM1MTY0LCJzZXNzaW9uS2V5IjoicGZuRkRkUnA5SldUQTZuU2ZoN252SjQ2b3g4VWs0Qmg3V1BrSWZFS3p0SjluMVRPQmpUOVNRPT0iLCJ1c2VyX3R5cCI6MSwia2V5IjoibW9tbyIsInJhcGlkX2lkIjoiUHdwQW5BM05aeWM1OGZ6d2Q4ZHAzQmpCdGtlZVRSTlljL3hEMTBNZktma2N0clJwMlBoZ1lXVVZvRTc5alZlRE9wZ0NBTzlVaWpFPT0iLCJ1aWQiOiIwMTY4Zjk2MjE4MiIsImV4cCI6MTc4OTkwNzk1N30.pf0dxo-9L72AKhZ-FSB7hZ9M0WKaestpSCkGwFIqfyXHAd1jWBMgVSpSsEyv3P6JDfFneDYRLRG6NGlKCl-ktxmum2lIvcjJtGhfIt_Wly5nT9fAEcTCyWA5TQFbe03VjLEez24L8pIMydgb0-yh_eO4jG8t1eimJkO1ZRUGKWrjsKlk5rhp_GvQyq_OORNE_I0h8lILEv1jpeiYadMEgB6-3FjBW9kIlPAjdtB0CcIp1gyUasM2BoE6v0eAN_Sp8_7TE9VR8wffBBalPS1WidgLNfXLgrT5ZgdMJJzro238pMBTgI5_o5Jil7MfHh9E92t0SzOoEvN62R8YX1XQqw"
)


@app.route("/", methods=["GET"])
def home():
  return jsonify(
      {"status": "success", "message": "MoMo API Proxy is running on Render!"}
  )


@app.route("/get-momo-history", methods=["GET", "POST"])
def get_momo_history():
  url = "https://api.momo.vn/transhis/api/transhis/golden-pocket/trans/browse"

  headers = {
      "Host": "api.momo.vn",
      "sessionKey": "30da4265-b745-46d0-93fe-de6f1f1b9528",
      "app_code": "5.15.0",
      "userId": "01682962182",
      "user_phone": "01682962182",
      "User-Agent": (
          "MoMoPlatform Store/5.15.0.51500 CFNetwork/1410.1 Darwin/22.6.0"
          " (iPhone 8 Plus iOS/16.7.16) AgentID/110335164"
      ),
      "lang": "vi",
      "device_performance": "low-end",
      "app_version": "51500",
      "wbmky": (
          "OtYyOKtLXGrcmW5MwY3fQAYkK2fDsGImGH5BmIt9YN8bqYxZ/9hmDXsy8FW50u32o1U0uoVb0bPRfgr2U5/yogk0ygZp27RhlNlZGVwFryncZL/LZF8+o20QyZmivwqejdfjJ3E230tRcedtENX8Uh7UpOHVe1/NYLIMjf6/CgSM5uDxcVkXgL5bc7qOcvwiDkSpT0VZLhqax39drO9C2lgF3Rjp5HSrWGx3LE6VjIgt/Lfg1xLUfZrFckt3CDOWYI3fGZ0C6RKOC7p/AAJ/adD7OvGR/yAodCVNzCnwpUTfMHsYfNhCx9vNaEimgh9p5e3pJHrw9DT7shCZ8voTcA=="
      ),
      "momo-session-key-tracking": "9E64FA7D-8494-469F-941B-7338CD0D02CC",
      "wbCode": "0&1789648767170",
      "baggage": (
          "sentry-environment=production,sentry-public_key=6e80c9f01f2440c9be5b37606028f996,sentry-release=vn.momo.platform.ios%405.15.0%2B51500,sentry-trace_id=b5dda73b8448412b974114dacee41672"
      ),
      "Connection": "keep-alive",
      "Authorization": auth_token_clean,
      "env": "production",
      "app_type": "production",
      "device_os": "IOS",
      "http-process-timestamp": "1789648767169",
      "timezone": "Asia/Ho_Chi_Minh",
      "Accept-Charset": "UTF-8",
      "Accept": "application/json",
      "agent_id": "110335164",
      "Content-Type": "application/json",
      "sentry-trace": "b5dda73b8448412b974114dacee41672-0e55c95a3c2846e5-0",
      "wbSign": (
          "ztiFBBUXjsstDMoQXyjkmnzhrUoHOICafHOf6qnp2Hxfh2YABnXajM6ZmxzuHL05gjFIgFtxVk5EuQpQzAxjspT1ej6us0xh9MbrUH9FGYk9"
      ),
      "platform-timestamp": "1789648767172",
  }

  try:
    payload = request.get_json(silent=True) or {}
    response = requests.post(url, headers=headers, json=payload, timeout=15)
    return jsonify(response.json()), response.status_code
  except Exception as e:
    return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
