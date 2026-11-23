"""課程範例：同來源 Flask API 串接 Dog CEO。"""
from urllib.parse import urlparse

import requests
from flask import Flask, jsonify, render_template

app = Flask(__name__)
API_URL = "https://dog.ceo/api/breeds/image/random"


def failure(message, status):
    return jsonify(ok=False, error=message), status


@app.after_request
def response_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Cache-Control"] = "no-store"
    return response


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/api/health")
def health():
    return jsonify(ok=True)


@app.get("/api/dog")
def dog():
    try:
        # 固定上游，不接受使用者指定網址，避免變成任意網址代理。
        with requests.get(
            API_URL, timeout=(3, 7), headers={"Accept": "application/json"}
        ) as response:
            if response.status_code == 429:
                return failure("圖片服務目前請求過多，請稍後再試。", 503)
            response.raise_for_status()
            data = response.json()
    except requests.Timeout:
        return failure("等候圖片服務逾時，請稍後再試。", 504)
    except requests.RequestException:
        return failure("暫時無法連線到圖片服務，請稍後再試。", 502)
    except ValueError:
        return failure("圖片服務回傳的資料不是有效 JSON。", 502)

    if not isinstance(data, dict) or data.get("status") != "success":
        return failure("圖片服務回傳非預期的狀態。", 502)
    image_url = data.get("message")
    if not isinstance(image_url, str):
        return failure("圖片服務缺少圖片網址。", 502)
    try:
        parsed = urlparse(image_url)
        valid = (
            parsed.scheme == "https"
            and parsed.hostname == "images.dog.ceo"
            and parsed.username is None
            and parsed.password is None
            and parsed.port in (None, 443)
            and bool(parsed.path)
        )
    except ValueError:
        valid = False
    if not valid:
        return failure("圖片服務回傳的圖片來源不符合預期。", 502)
    return jsonify(ok=True, image_url=image_url, source="Dog CEO")
