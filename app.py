from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
import requests
import uuid

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# / の場合のSheetDBのAPIエンドポイント
CAT_LIST_API = "https://sheetdb.io/api/v1/svuox1q3tty72"
CAT_HEALTH_API = "https://sheetdb.io/api/v1/3q64amcttgfit"

@app.get("/")
async def index(request: Request):
    # 猫一覧の取得
    response = requests.get(CAT_LIST_API)
    cats = response.json()
    return templates.TemplateResponse("index.html", {"request": request, "cats": cats})

@app.post("/add_cat")
async def add_cat(name: str = Form(...), gender: str = Form(...), age: str = Form(...), breed: str = Form(...)):
    try:
        # 新しい猫のIDを生成
        new_id = str(uuid.uuid4().hex)[:7]

        # データの組み立て
        data = {
            "id": new_id,
            "名前": name,
            "性別": gender,
            "年齢": age,
            "猫種": breed
        }

        # SheetDBにPOSTリクエストを送信してデータを追加
        response = requests.post(CAT_LIST_API, json=data)

        # 成功した場合はリダイレクト
        if response.status_code == 201:
            return JSONResponse(content={"message": "猫が登録されました。"}, status_code=201)
        else:
            raise HTTPException(status_code=500, detail="猫の登録に失敗しました。")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"エラーが発生しました: {str(e)}")

@app.delete("/delete_cat/{id}")
async def delete_cat(id: str):
    # SheetDBから猫の情報を削除
    delete_url = f"{CAT_LIST_API}/id/{id}"
    response = requests.delete(delete_url)

    if response.status_code == 200:
        return JSONResponse(content={"message": "猫の情報が削除されました。"}, status_code=200)
    else:
        raise HTTPException(status_code=500, detail="猫の情報の削除に失敗しました。")

@app.get("/cat_health/{id}")
async def cat_health(request: Request, id: str):
    return templates.TemplateResponse("cat_health.html", {"request": request, "cat_id": id, })

@app.post("/add_health_entry")
async def add_health_entry(id: str = Form(...), date: str = Form(...), weight: float = Form(...), 
                           food_intake: float = Form(...), excretion: float = Form(...), 
                           exercise: float = Form(...), remarks: str = Form(None)):
    try:
        # データの組み立て
        data = {
            "id": id,
            "日付": date,
            "体重": weight,
            "餌の摂取量": food_intake,
            "排泄量": excretion,
            "運動量": exercise,
            "備考": remarks
        }

        # SheetDBにPOSTリクエストを送信してデータを追加
        response = requests.post(CAT_HEALTH_API, json=data)
        
        # 成功した場合はリダイレクト
        if response.status_code == 201:
            return JSONResponse(content={"message": "情報が追加されました。"}, status_code=201)
        else:
            raise HTTPException(status_code=500, detail="情報の追加に失敗しました。")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"エラーが発生しました: {str(e)}")
