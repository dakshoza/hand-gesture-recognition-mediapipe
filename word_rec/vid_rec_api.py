from fastapi import FastAPI, Body
from pydantic import BaseModel
from schemas.api_class import (word, translate)
from fastapi import FastAPI, Request, Form, status, Body, Response, BackgroundTasks
from fastapi.responses import JSONResponse
from word_rec_fun import return_vid_recs

app = FastAPI()

@app.post("/get_vid_recs_from_score")
async def articles(body: word):
    output = await return_vid_recs(body.user_query)
    return {"output":output}