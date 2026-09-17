import os
from Flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Chuỗi JWT gốc đã được làm sạch không bị lỗi ký tự thừa
RAW_JWT = (
    "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9."
    "eyJ1c2VyIjoiMDE2ODI5NjIxODIiLCJpbWVpIjoiNTEwMDEtMWIxYjAyMWQ1NDgyZjA4MWVkODY1ZmJkM2UwMDAwYWYyNzU4ZmIxMmUxOGRiZGUzZGMwOTM1MWI5NDI1ZWY1MyIsImhJbWVpIjoiOEZiSVBHVkI4dEsyajNkRWd2dWZURDZXTU5LWkhVMmxtWWdMRlZUNDZLOXhNM055bzRxdXRYV1FYNTlPbU1NSkh1c0pzck9ub1pqazl6RysveXAzaktidnlseER2ZHhTZC9mSlV1cUJESms9IiwiTUFQX1NBQ09NX0NBUkQiOjAsIk5BTUUiOiJUcuG6p24gTmjhuq10IEhvw6BuZyIsIkRFVklDRV9PUyI6ImlvcyIsImFQUF9WRVIiOjUxNTAwLCJhZ2VudF9pZCI6MTEwMzM1MTY0LCJzZXNzaW9uS2V5IjoicGZuRkRkUnA5SldUQTZuU2ZoN252SjQ2b3g4VWs0Qmg3V1BrSWZFS3p0SjluMVRPQmpUOVNRPT0iLCJ1c2VyX3R5cCI6MSwia2V5IjoibW9tbyIsInJhcGlkX2lkIjoiUHdwQW5BM05aeWM1OGZ6d2Q4ZHAzQmpCdGtlZVRSTlljL3hEMTBNZktma2N0clJwMlBoZ1lXVVZvRTc5alZlRE9wZ0NBTzlVaWpFPT0iLCJ1aWQiOiIwMTY4Zjk2MjE4MiIsImV4cCI6MTc4OTkwNzk1N30."
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
        "aI3C/Mdsew1HVcEuju5Code4xbRiUqiyj6aVZxBnicE53GVIEvuZRTHu7ypmU5up7dxX6KoPy/K3vAdrDzs3aWRHi3KMgQpXynNRbrNs/Y5OmYY3kp5hGI6xSzUZ7NkrlERisA6sgzPBGhLUdKv6Wl7pe+t19Bqe6K7ZSA5QqciCdi5cZGAZpAyqbM8M1RoXj2rpbUPrf6oZNg8QWqlsxUy+s+hqEF21APzG3Mh+LadT7oxbPAzQp27ckR53tQdBrtiWX5KJs67yEAx42hURYtV61Wbpt+Hbk84SGcLLYGrv0PAkEAaOijy5YfFrrtdyxj3IXVioUxnmtkbWiCa2dw=="
    ),
    "wbmtd": (
        "K/69JuC5EeMSBMRhzoVj3s1bviUTaQEd/BzMnxkPFna+s9hHzBUaZtl4zHQxpSZnVHqh4veI/D9ODNodzBGpWSYvFQL3w01S1FpL5O2k7WoCFveMMKJIrL71Jjxka1f99o3gt/w/sWhW3AhAYfP4lrJgAV0Csdezw6uAU2wtADQqdSDLh6EGyA1ghidW9mQVrKZt4sXBNqzUWPwYPpz6GJXKOJ+RhtKfTF46J0kLVhxUw6SAOP6y96SG4PrVkCyqyyOTZTbZjTYtiwPhEFwxrO4YrTDy2Rwp6QGcIqnuPBBoa0EZZ1wgg4+VfWDdGbHwr5uviGBONXYqEp91SbX+j4xDVJIAMMEmFDfvbTn6iaMp7MvIds3gcdQ9r/sEs5/bqpEbtN/iYw24dDqz6xlIwXcIg6rXQD9t6x5ECiQKifNCsUiAsYwfTCl3AUCuwPPeT+5FNW5e/yCd+XfgMObVqbkvzyHaspxGWbcHH6aYmtD2dBeT2HS/cykZnPnt+67w4HX/9uwXdVRrrlnUG3WxrKWFdJpRwEl3LGoq1Mbbrm9NCpshto5Xf0pyWzUV2NIix4XaqOxDUJBJlaCwdwXNsbLvxhzh6bL1rmrostR2mPhEPoi7SUTYoyezAP9dwk204Zr2RIf/XBY7TFTLc7IcyHXc8/1jFxRl1D6fRpbRqKsHjtPZDm8fYX/ptf0axPirHBjT1CrJvYZQX2/C8a5kV/m0GWwcwpm562aNGenEKYMW9ukqdu/funW5oDYU6twgkPBav3G51iLpzEEQMuGJHEAo7+QFSN+JKswt3L5UvrPyzU/YD5dwfY73rWi5pZTZ15qiECViyY2j94r2mmu8J7h3GN6Uk3kgSgolpoeheoZJ7LmRD4RsEk5LErDTJsKJ1ykp6CWdeuNyio+838wi4Do1J7OZReU+jbj94mSRBuQrZtujEpaxskjzV3J8MgYzQXVCc3v9hLcKkEZ44BQxD2Z6p5iNgvnIytU8gVTxlILsHZd4qQ3T1yhMDmAdjvLW1E71J8f0QZ/6uoHjE/A/BuTZadOMa39oL0yL+gar7P7F0LQaCaIdAN+bPSaBR3DMVb/fgXdayu18x2QiV0+MdqKTe1annAYtnp3VeDK330cmwGwuBzQLp3pIZPXLRYTFAB/N9yHaGJfC/q4T2KHJsi0shSk6aBjm5EoFYHt+mleS6ARo6XXa2wZB1dP75yb2YInP4jdCkTkRyUT+SoZ6omcJnB/GNtrz24z2ohywAQ/MojgXQydhNs2U4fiH94maBne+Hl2cm8OOXgATcDaS5n/FZ7s3kD2EpBYTcwSnSlNyLYeLUC4Ag7g8xcm1C5jTyeu7ki2BE9YST3W8eW7daeeTJw2UspnSphiuerV7rz1xFdO0Eu1WdxCv2VHTnYUmn3jY3Ou7sl0OLdZ3IEbxU3SIMAJ92HYWIy0s8Dv66zprrb1Qh9fQ01oP/83lJnOmiS98K50umY5NS5oL+ZUVDU/P3OYIKuYd8ojOVCXara4PONdGTOweRSb/00LT+8fQq4AcUM4aQ5F2NnebCsSRbl0iOryRAGsfownqpNlFqbCLz4ctQVarxV2ymzTyi824klFZI1k7VOM2BWjuEXZ2TOg2r9C4qwsHP4b7ErutE719VvWgU37rK/IKGyta9KkLYylW1A4/CI0DkKw4BB/eXSztoDatDvf3/Pnw3PjTtUl+UO9BN7WvJhCbtoZjey+9ABPUTyJJ3jysFQ4TeNGnpIR1YIs6QTvMCJlJp5C242mkXpYvlIxg1Af1HDqNuJbZ9ARvhtMyBbHMssZc9jGDmWEeweby+vafytWW98LZHhsrtgMLKbsD+lSEeDly1wwEqthf0jzvTXHhOdyyUIRc9g=="
    ),
    "momo-session-key-tracking": "9E64FA7D-8494-469F-941B-7338CD0D02CC",
    "wbCode": "0&1789648766937",
    "baggage": (
        "sentry-environment=production,sentry-public_key=6e80c9f01f2440c9be5b37606028f996,sentry-release=vn.momo.platform.ios%405.15.0%2B51500,sentry-trace_id=b5dda73b8448412b974114dacee41672"
    ),
    "Connection": "keep-alive",
    "Authorization": "Bearer " + RAW_JWT,
    "env": "production",
    "app_type": "production",
    "device_os": "IOS",
    "http-process-timestamp": "1789648766936",
    "timezone": "Asia/Ho_Chi_Minh",
    "Accept-Charset": "UTF-8",
    "Accept": "application/json",
    "agent_id": "110335164",
    "Content-Type": "application/json",
    "sentry-trace": "b5dda73b8448412b974114dacee41672-0e55c95a3c2846e5-0",
    "wbSign": (
        "aO3lLUQ10/h6UIwcXOeTejDl09Aoe6FCRhFpGRkYd7bvx+abUD8Li45hdPlyPYUD3lrlWK0w+gQd/ocMpXOLq29qFEdZhT3tkf20FefMM/Jy"
    ),
    "platform-timestamp": "1789648766940",
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
    payload = request.get_json(silent=True) or {}
    res = requests.post(url, headers=NEW_HEADERS, json=payload, timeout=15)
    return jsonify(res.json()), res.status_code
  except Exception as e:
    return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
