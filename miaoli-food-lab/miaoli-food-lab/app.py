"""課程範例：同來源 Flask API 苗栗美食探索站。"""
import random
from urllib.parse import urlparse

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

MIAOLI_FOODS = [
    {
        "id": "ban-tiao",
        "name": "苗栗水晶餃／客家粄條",
        "area": "苗栗市／南庄",
        "category": "客家鹹食",
        "summary": "Q彈滑順的客家粄條搭配油蔥酥與韭菜，或晶瑩剔透的水晶餃湯，是苗栗最經典的日常小吃。",
        "must_try": "乾拌油蔥粄條、骨仔肉湯、水晶餃",
        "image_url": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?auto=format&fit=crop&w=900&q=80",
        "source": "苗栗美食精選資料庫（課程範例）",
    },
    {
        "id": "mei-gan-kou-rou",
        "name": "客家梅干扣肉與福菜湯",
        "area": "公館／頭份",
        "category": "客家菜餚",
        "summary": "肥瘦相間的控肉吸滿梅干菜香氣，鹹香下飯；再配上一碗酸甘爽口的福菜肉片湯最對味。",
        "must_try": "梅干扣肉、福菜湯、薑絲大腸",
        "image_url": "https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=900&q=80",
        "source": "苗栗美食精選資料庫（課程範例）",
    },
    {
        "id": "xian-cao",
        "name": "九降風仙草凍／仙草雞",
        "area": "銅鑼／苗栗市",
        "category": "甜品湯品",
        "summary": "苗栗仙草香氣濃郁，夏天做成冰涼滑嫩的仙草凍與芋圓，冬天則適合燉煮溫補的仙草雞湯。",
        "must_try": "招牌仙草凍、芋圓仙草奶凍、仙草雞湯",
        "image_url": "https://images.unsplash.com/photo-1563805042-7684c019e1cb?auto=format&fit=crop&w=900&q=80",
        "source": "苗栗美食精選資料庫（課程範例）",
    },
    {
        "id": "strawberry-dessert",
        "name": "大湖草莓甜點與果醬",
        "area": "大湖",
        "category": "季節甜點",
        "summary": "以大湖新鮮草莓製作的草莓大福、草莓冰與手工果醬，酸甜果香深受旅人喜愛。",
        "must_try": "現做草莓大福、草莓雪花冰、草莓香腸",
        "image_url": "https://images.unsplash.com/photo-1464305795204-6f5bbfc7fb81?auto=format&fit=crop&w=900&q=80",
        "source": "苗栗美食精選資料庫（課程範例）",
    },
    {
        "id": "mochi-lei-cha",
        "name": "客家麻糬與擂茶點心",
        "area": "南庄／三義",
        "category": "傳統點心",
        "summary": "手工捶打的軟Q麻糬裹上花生粉與芝麻粉，搭配穀物與茶葉研磨的擂茶，充滿山城茶香。",
        "must_try": "花生芝麻麻糬、客家擂茶、艾草粿",
        "image_url": "https://images.unsplash.com/photo-1582716401301-b2407dc7563f?auto=format&fit=crop&w=900&q=80",
        "source": "苗栗美食精選資料庫（課程範例）",
    },
    {
        "id": "hang-ju-tea-meal",
        "name": "銅鑼杭菊茶點與山產小炒",
        "area": "銅鑼",
        "category": "茶飲料理",
        "summary": "結合銅鑼杭菊花茶與在地山產料理，清爽花香能平衡重口味客家菜，適合搭配下午茶點心。",
        "must_try": "杭菊養生茶、茶油麵線、炸溪蝦",
        "image_url": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?auto=format&fit=crop&w=900&q=80",
        "source": "苗栗美食精選資料庫（課程範例）",
    },
]


def failure(message, status):
    return jsonify(ok=False, error=message), status


def is_safe_image_url(image_url):
    if not isinstance(image_url, str) or not image_url.strip():
        return False
    try:
        parsed = urlparse(image_url)
    except ValueError:
        return False
    return (
        parsed.scheme == "https"
        and bool(parsed.hostname)
        and parsed.username is None
        and parsed.password is None
        and parsed.port in (None, 443)
        and bool(parsed.path)
    )


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
    return jsonify(ok=True, count=len(MIAOLI_FOODS))


@app.get("/api/food")
def food():
    area = (request.args.get("area") or "").strip()
    candidates = MIAOLI_FOODS
    if area and area != "全部":
        candidates = [item for item in MIAOLI_FOODS if area in item["area"]]
        if not candidates:
            return failure("找不到符合該地區的苗栗美食，請換個地區試試。", 404)

    picked = random.choice(candidates)
    if not is_safe_image_url(picked.get("image_url", "")):
        return failure("美食圖片網址格式不正確。", 502)

    return jsonify(
        ok=True,
        food=picked,
        source=picked["source"],
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
