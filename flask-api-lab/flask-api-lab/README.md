# 狗狗圖片探索站

Python 3.12、Flask、requests 的公開 API 課程範例。免金鑰，沒有資料庫。
官方 API 文件：https://dog.ceo/dog-api/documentation/random

## Windows PowerShell

在包含 app.py 的資料夾執行：

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m flask --app app run --port 5000
```

開啟 http://127.0.0.1:5000 。停止服務按 Ctrl+C。

## Mac 或 Linux

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m flask --app app run --port 5000
```

## 驗證

- GET /：首頁。
- GET /api/health：`{"ok": true}`。
- GET /api/dog：取得圖片網址；外部服務失敗時顯示可理解的錯誤。
- Windows：`.\.venv\Scripts\python.exe -m unittest discover -s tests -v`
- Mac：`.venv/bin/python -m unittest discover -s tests -v`

測試以模擬回應驗證錯誤分支，不需呼叫真實 API；另應手動做一次真實連線檢查。

## GitHub 與 Vercel

1. 將此資料夾內的程式放到自己的 GitHub repo，根目錄直接含 app.py。
2. 手動上傳時先解壓縮，不要只上傳 ZIP；保留 templates/index.html 的路徑。
3. 不上傳 .venv、.env、.git、快取或任何真實憑證。
4. Vercel 匯入 repo，Root Directory 指向含 app.py 的位置。
5. Framework Preset 使用 Flask；Build Command、Output Directory 保留預設。
6. 本範例不需要自訂 vercel.json 或環境變數；.python-version 指定 3.12。
7. Ready 後測試正式網址的首頁、/api/health、/api/dog。

依目前官方方式，根目錄 app.py 匯出 app 即可辨識。CSS 與 JS 內嵌在範本；
若拆成獨立檔案，Vercel Flask 採 public/ 並以根路徑引用，另處理本機對應。
官方部署文件：https://vercel.com/docs/frameworks/backend/flask

## 安全與平台邊界

程式只呼叫固定上游，設定 timeout，檢查 JSON 與 HTTPS 圖片來源。
不將上游例外細節回傳給訪客。本課示範不含生產服務的登入與分散式流量限制。
收藏與上傳若需永久保存，應另接資料庫或物件儲存。
.env.example 只示範名稱，程式沒有自動載入 .env，也不需其中的金鑰。
請尊重 API 與圖片供應商的使用條件；免費服務不保證可用性。
