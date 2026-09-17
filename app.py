import os
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Token JWT chuẩn từ request mới nhất của bạn
RAW_JWT = (
    "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9."
    "eyJ1c2VyIjoiMDE2ODI5NjIxODIiLCJpbWVpIjoiNTEwMDEtMWIxYjAyMWQ1NDgyZjA4MWVkODY1ZmJkM2UwMDAwYWYyNzU4ZmIxMmUxOGRiZGUzZGMwOTM1MWI5NDI1ZWY1MyIsImhJbWVpIjoiOEZiSVBHVkI4dEsyajNkRWd2dWZURDZXTU5LWkhVMmxtWWdMRlZUNDZLOXhNM055bzRxdXRYV1FYNTlPbU1NSkh1c0pzck9ub1pqazl6RysveXAzaktidnlseER2ZHhTZC9mSlV1cUJESms9IiwiTUFQX1NBQ09NX0NBUkQiOjAsIk5BTUUiOiJUcuG6p24gTmjhuq10IEhvw6BuZyIsImRFVklDRV9PUyI6ImlvcyIsImFQUF9WRVIiOjUxNTAwLCJhZ2VudF9pZCI6MTEwMzM1MTY0LCJzZXNzaW9uS2V5IjoicGZuRkRkUnA5SldUQTZuU2ZoN252SjQ2b3g4VWs0Qmg3V1BrSWZFS3p0TjluMVRPQmpUOVNRPT0iLCJ1c2VyX3R5cCI6MSwia2V5IjoibW9tbyIsInJhcGlkX2lkIjoiUHdwQW5BM05aeWM1OGZ6d2Q4ZHAzQmpCdGtlZVRSTlljL3hEMTBNZktma2N0clJwMlBoZ1lXVVZvRTc5alZlRE9wZ0NBTzlVaWpFPT0iLCJ1aWQiOiIwMTY4Zjk2MjE4MiIsImV4cCI6MTc4OTkwNzk1N30."
    "pf0dxo-9L72AKhZ-FSB7hZ9M0WKaestpSCkGwFIqfyXHAd1jWBMgVSpSsEyv3P6JDfFneDYRLRG6NGlKCl-ktxmum2lIvcjJtGhfIt_Wly5nT9fAEcTCyWA5TQFbe03VjLEez24L8pIMydgb0-yh_eO4jG8t1eimJkO1ZRUGKWrjsKlk5rhp_GvQyq_OORNE_I0h8lILEv1jpeiYadMEgB6-3FjBW9kIlPAjdtB0CcIp1gyUasM2BoE6v0eAN_Sp8_7TE9VR8wffBBalPS1WidgLNfXLgrT5ZgdMJJzro238pMBTgI5_o5Jil7MfHh9E92t0SzOoEvN62R8YX1XQqw"
)

NEW_HEADERS = {
    "Host": "api.momo.vn",
    "sessionKey": "30da4265-b745-46d0-93fe-de6f1f1b9528",
    "app_code": "5.15.0",
    "userId": "01682962182",
    "user_phone": "01682962182",
    "User-Agent": (
        "MoMoPlatform Store/5.15.0.51500 CFNetwork/1410.1 Darwin/22.6.0 (iPhone"
        " 8 Plus iOS/16.7.16) AgentID/110335164"
    ),
    "lang": "vi",
    "device_performance": "low-end",
    "app_version": "51500",
    "wbmky": (
        "YXUT23cOsZgJQ/gLwdwT9Y7S6/YJzcYFG71gv/"
        "UREKFKHLQ+4rgCaj5YdhH0cPN2ml9gdPV7zxtXt8gEGGo4bthsNiuTviesxc9k+vm0/"
        "Nckx9FwEX7FonrG3ZPRti8yqdOCMTWCOhMNxprlcy2R1e3qg5fn50Pt4BSoSRQLMidQFB0V0zpl7COT"
        "2Pe1I01vWpverWDVNOq9RRBXj0ODyqJXXxy3vBknAzD3zLeLTvi0mzfdD7XU2WGX3pAmPxkRGWH3Hm"
        "IYFaof0WH6nnJb/jPaPp5MlzcOlCO2olhUT9b2yrJfXlVfEN2CbZZOGZu"
    ),
    "wbmtd": (
        "S6LO46xfSxYUSLX4fsXJLLgfYINchWY4sGvftOLNWBdsfHNalP3w3ld9lPdM4++GqvWdQuSEm20v/"
        "S2KnN5tAWxct9uGZtyVQWd7m17CmeA/"
        "g9iGoBtBhEhZ5ESfDj811k28qo6lULaPFkcl8ZkarVFuYYO2iQBSrCzyoJgU/"
        "OXyye87afzf7YrbRZw+qartROZ0PVxtL0bjRKyA8DKd63Bq24lcj+Itkf4e35ib38TSCP8uPKI4EghgvKCw"
        "ZbTJ3OVCXB0RkmnxSMQWK/"
        "5cUhQDyix2Lei1QjOZPiBhCZ7e182GnBZuilz5qFoFSSNGugHPk2sKb1Mhxy3CbZuYzc1Omp5WWQl3OBINq"
        "otXpWPndUcVex9xF8+jGHR7QOoB9+AZlaptrff0e9rsSet/"
        "QbE4mxvWBy3BnN23Mz4grv6XGMQL8rh1uBHKMsRwStPZ3az2KCq4RIXFebVJip2lsTHZUrs1Ugloi5"
        "LVRh6uKLtAteFBOqRR5afhSl7uhWjJwaelkIDbuKVrnZsmmwytsdcC03aMVF4p8r8rtdg1fZViMJOp9GI+KC"
        "p8O7zN0/"
        "pARBJW5m0xtf5OPT3U46ue6fptjnq9qOjoTibLtwSn9yUmTU5Ydzj9pqrBkOshF+5LmYo3ZMRATp1OG8j"
        "seWucTtBE9D4Rohl1Slu1WFyfxXd4KoiWJMojueJ8Q29JgLxHjly1C9IPNAhl1XJKvUhEwmQSv44VKE6xP"
        "kAj02c0B/ayHA++1WCwaKGcqHgUrz+e3f1ax/"
        "k8rz3GzqlQPvtPLtj0eGB1Ubs/"
        "xofla7YOIPW0ROZe3xfyzVy9SIQx/"
        "YWw21yzFwXFTPeUuuXPb+jYbgP4ZsdLjHRFBkd"
        "B2ahOG/"
        "zP0B8PP3bnvR452gGCaSxJx4Zgo4NPDjiLiRXZRGSix877jD72ShorGfEfVnPur8Mw3q1xrv5WGIk+BSZQG"
        "WMBBI+nAVVJ/GRFEi36KtK51fM0/"
        "B1exgVsSmR7CYZMrPGaa8ex9zGAMPP4rq0qHluF3"
        "+alHyllWp+MDRTO3KtSfEMD5KpfSTAmDW97IBv0"
        "hOmx591W8Cnqt9+/YAnsWwjPwUk2uttV9/"
        "zdkZOJ0vv6XfbpAnZrCvwrAj2rBcw6HjMdoohRf6s"
        "D2pf1FC2rg2o/"
        "beAvl57bcsXVGdu7SGu4x9zOtz1tIAXw/"
        "XZ683+Tkk7XYWGQ3lc1YLWUNIXzfbW/"
        "XYLw2XOFRBdaeH/"
        "koJUE4Y9GlzgHzGkhjk2nQMdlty3UeLqUx3bt8mdaG"
        "MH+V//WX6VZX7tMyZOFDvYaUlYHNEI131If9KwAO/"
        "eRDCvoapgSpSu/"
        "11daLX5P29Lkilr9S8NHqYis3uelGKGYA8R96vJOV"
        "MSP15kilOHEdggR+A5VWLh2+SuxBBSOZ/"
        "pTYPG1jpwN1CKkKZPLN+0LcAm1r5JCk8ePXdGEqL"
        "Cm+CUsE5UPqp+Xrpeux7s4+Bqm61fM8SgNENUI"
        "7p5+yz8jQWtUmCkanMef6Wuk9g7mexmiPtoM2J0y"
        "yEprq5NwmKK8SAdMqmo4ivl4bZXRCvNE/"
        "LFVKN4caaTmjR4UTMN8xY1H2A4KtiskT6YuJSR1VB/"
        "F/"
        "cb6xtifAzFU6I8b1nVRWce4qMC8hk5iDJs9/6BX0ygI"
        "lpFi/ZNhIzTvTHWRUwPvymfshwQdUeu1NfRN/Cj3/"
        "IIMIZYI4IlfLvFtscAsSGGIWf9YNZ/"
        "H8N9D6x3ReUMA5vCCYMjsHYWixlqfOokl//"
        "GphEx0FHnRg7OFUywDd0sU3iQmh6OujviQmS5AbI"
        "AYOdNXwtTlvbN4SnMMI24CSCLFuYHjfinzM2nVIM"
        "SgpgZwQP1Ax5z7UNGBSyw=="
    ),
    "momo-session-key-tracking": "E19788AB-9BC1-4D14-B7B8-A607AD452A22",
    "wbCode": "0&1789650017432",
    "baggage": (
        "sentry-environment=production,sentry-public_key=6e80c9f01f2440c9be5b37606028f996,sentry-release=vn.momo.platform.ios%405.15.0%2B2B51500,sentry-trace_id=b5dda73b8448412b974114dacee41672"
    ),
    "Connection": "keep-alive",
    "Authorization": "Bearer " + RAW_JWT,
    "env": "production",
    "app_type": "production",
    "device_os": "IOS",
    "http-process-timestamp": "1789650017431",
    "timezone": "Asia/Ho_Chi_Minh",
    "Accept-Charset": "UTF-8",
    "Accept": "application/json",
    "agent_id": "110335164",
    "Content-Type": "application/json",
    "sentry-trace": "b5dda73b8448412b974114dacee41672-0e55c95a3c2846e5",
    "wbSign": (
        "MQNsZBBwFwzVEIQ/IY0hEnIUkqIfEGVK3GjoWRtL6QKMKpIRd6wuuYJlvI"
        "OK7EdLyRgiCV8OY15jnXx0jX7ZCTclOr2W9z40FwNg"
    ),
    "platform-timestamp": "1789650017434",
}


@app.route("/", methods=["GET"])
def home():
  return jsonify(
      {"status": "success", "message": "MoMo API Proxy is running on Render!"}
  )


@app.route("/get-momo-history", methods=["GET", "POST"])
def get_momo_history():
  url = "https://api.momo.vn/transhis/api/transhis/golden-pocket/trans/browse"

  try:
    safe_headers = {
        k: str(v).encode("utf-8", errors="ignore").decode("latin-1")
        for k, v in NEW_HEADERS.items()
    }
    payload = request.get_json(silent=True) or {}
    res = requests.post(url, headers=safe_headers, json=payload, timeout=15)
    return jsonify(res.json()), res.status_code
  except Exception as e:
    return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
