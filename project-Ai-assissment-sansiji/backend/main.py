from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import json
import os
from typing import Optional
import time

app = FastAPI(title="三思集后端")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KB_PATH = os.path.join(BASE_DIR, "knowledge_base.json")
ADMIN_PWD_FILE = os.path.join(BASE_DIR, "admin_pwd.json")

OLLAMA_URL = "http://127.0.0.1:11434/v1/chat/completions"
MODEL_NAME = "qwen2.5:7b"

def load_json(filepath, default):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return default

def save_json(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 初始化内置知识库（先放几条测试数据，后面再替换成开源库转换结果）
def init_kb():
    if not os.path.exists(KB_PATH):
        init_data = [
            {
                "question": "应届生如何选第一份工作",
                "high": "优先行业赛道、直属领导、成长空间",
                "diff": "薪资vs长期发展取舍",
                "warn": "警惕高薪外包无成长岗位",
                "tag": "职场",
                "type": "职业决策",
                "expireTime": "2028-12-31",
                "confidence": 0.92
            },
            {
                "question": "考研还是直接就业",
                "high": "评估专业就业率、个人抗压、家庭支持",
                "diff": "沉没成本、备考周期",
                "warn": "不要盲目跟风考研",
                "tag": "学生",
                "type": "学业决策",
                "expireTime": "2028-12-31",
                "confidence": 0.90
            }
        ]
        save_json(KB_PATH, init_data)

def load_admin_pwd():
    pwd_data = load_json(ADMIN_PWD_FILE, {})
    if "pwd" not in pwd_data:
        init_pwd = "sansiji123"
        save_json(ADMIN_PWD_FILE, {"pwd": init_pwd})
        return init_pwd
    return pwd_data["pwd"]

init_kb()
admin_pwd = load_admin_pwd()

# 简易检索
def search_kb(q: str):
    kb = load_json(KB_PATH, [])
    q_low = q.lower()
    res = []
    for item in kb:
        q_item = item.get("question", "").lower()
        if q_item in q_low or q_low in q_item:
            if item.get("type") == "政策类":
                item["confidence"] = max(0.4, float(item["confidence"]) - 0.25)
            res.append(item)
    return res

class StreamReq(BaseModel):
    question: str
    compare: bool = False

class PwdReq(BaseModel):
    pwd: str
    newPwd: Optional[str] = None

# 流式问答接口（前端对接这个）
@app.post("/api/llm/stream")
async def stream_chat(req: StreamReq):
    kb_hit = search_kb(req.question)
    if kb_hit:
        def gen():
            for item in kb_hit:
                text = f"""【高优要点】{item['high']}
【难点取舍】{item['diff']}
【风险警告】{item['warn']}
标签：{item['tag']}｜类型：{item['type']}｜置信度：{item['confidence']}"""
                for c in text:
                    yield c
                    time.sleep(0.015)
        return gen()
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role":"user","content":req.question}],
        "stream": True
    }
    r = requests.post(OLLAMA_URL, json=payload, stream=True)
    if r.status_code != 200:
        raise HTTPException(status_code=500, detail="ollama调用失败，请检查ollama是否启动")
    return r.iter_content()

# 管理员密码校验
@app.post("/api/admin/checkpwd")
async def check_pwd(req: PwdReq):
    global admin_pwd
    if req.pwd == admin_pwd:
        return {"ok": True}
    return {"ok": False}

# 修改管理员密码
@app.post("/api/admin/setpwd")
async def set_pwd(req: PwdReq):
    global admin_pwd
    if not req.newPwd:
        raise HTTPException(status_code=400, detail="需要传入newPwd")
    admin_pwd = req.newPwd
    save_json(ADMIN_PWD_FILE, {"pwd": admin_pwd})
    return {"ok": True, "msg":"密码已更新"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
