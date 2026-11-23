# 苗栗美食探索站

Python 3.12、Flask 課程範例：透過後端 JSON API 提供苗栗在地美食推薦與隨機抽籤。

## Windows PowerShell

在包含 `app.py` 的資料夾執行：

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m flask --app app run --port 5000
```

開啟 `http://127.0.0.1:5000` 。停止服務按 `Ctrl+C`。

## Mac 或 Linux

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m flask --app app run --port 5000
```

## 驗證

- `GET /`：首頁。
- `GET /api/health`：`{"ok": true, "count": 6}`。
- `GET /api/food`：取得一筆苗栗美食資料；可搭配 `?area=大湖` 或 `?area=銅鑼` 篩選。
- Windows：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`
- Mac：`.venv/bin/python -m unittest discover -s tests -v`

## GitHub 與 Vercel

1. 將此資料夾內的檔案放到自己的 GitHub repo，根目錄直接含 `app.py`。
2. 手動上傳時先解壓縮，不要只上傳 ZIP；保留 `templates/index.html` 的路徑。
3. 不上傳 `.venv`、`.env`、`.git`、快取或任何真實憑證。
4. Vercel 匯入 repo，Root Directory 指向含 `app.py` 的位置。
5. Framework Preset 使用 `Flask`；Build Command、Output Directory 保留預設。
6. Ready 後測試正式網址的首頁、`/api/health`、`/api/food`。

官方部署文件：https://vercel.com/docs/frameworks/backend/flask
