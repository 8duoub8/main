from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.spam import check_spam
# FastAPI 기반웹앱생성
# /docs (Swagger UI)에표기되는이름
app = FastAPI(title="SpamCheck Web")
# 정적HTML 서빙: static 안에파일들을URL로접근가능하게해라
# {URL}/static/…… 으로접근가능하게
app.mount("/static", StaticFiles(directory="static"), name="static")
# 메인페이지(/) 처리: “/”로접속시처리할작업
@app.get("/", response_class=HTMLResponse)
def home():
    with open("static/index.html", encoding="utf-8") as f:
       return f.read()
# classify 요청이올때할일# async: 비동기처리(서버가요청기다리는동안다른요청도처리가능
@app.post("/classify")
async def classify(request: Request):
    payload = await request.json()
    text = payload["text"]
    label, score = check_spam(text)
    return {
        "label": label, "score": score
    }
# 실행은운영환경의책임으로남기기위해만들지X
# http://127.0.0.1:8000 접속
# if __name__ == "__main__":
# uvicorn.run(app, host="127.0.0.1", port=8000)