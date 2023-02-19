from fastapi import FastAPI, Response, Form, File
from typing import Optional
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import redis, asyncio


# https://github.com/chesnutcase/networks_lab2

app = FastAPI()

def get_redis_client():
    return redis.Redis(host="redis")

## Main checkoff
@app.get("/list_of_items")
def list_of_items(response: Response, sortBy: Optional[str] = None, limit: Optional[int] = None, offset: Optional[int] = None):
    redis_client = get_redis_client()
    outputs = []
    offset = 0
    limit = 0
    for key in redis_client.keys():
        temp_dict = {}
        temp_dict["fruit"] = key
        temp_dict["value"] = redis_client.get(key)
        outputs.append(temp_dict)
        limit += 1
    ## Return a list of all keys and values in the database
    if sortBy:
        if sortBy == "value":
            outputs = sorted(outputs, key=lambda output: output.get("value"), reverse=False)
            return outputs
        else:
            response.status_code = 400
            return None
    if limit:
        if limit < 0 or type(limit) == float:
            response.status_code = 400
        limit = int(limit)
    if offset:
        if offset < 0 or type(offset) == float:
            response.status_code = 400
        offset = int(offset)
    return outputs[offset:limit:]

@app.get("/get_item/{key}")
def get_item(response: Response, key: str):
    redis_client = get_redis_client()
    ## Return the value of the key
    item_value = redis_client.get(key)
    if not item_value:
        response.status_code = 404
        return None
    return {key: redis_client.get(key)}

@app.post("/add_item")
async def add_item(response: Response, key: str = Form(), value: int = Form()):
    redis_client = get_redis_client()
    if key and value:
        redis_client.set(key, value)
        return "Key Value added!s"
    response.status_code = 400
    return "Invalid Form Data!"

@app.delete("/delete_item/{key}")
def delete_item(response: Response, key: str):
    redis_client = get_redis_client()
    ## Delete a key and value from the database
    if not key:
        response.status_code = 400
        return "Please provide a key!"
    redis_client.delete(key)
    return "Deleted key and value from database!"

## Which routes are idempotent:
## All routes are idempotent except for the POST route which are:
## /get_item/{key}
## /delete_item/{key}
## /list_of_items

## Implementation of 2 challenges:
@app.post("/delete_multiple_items")
async def delete_multiple_items(response: Response, key: str = Form()):
    redis_client = get_redis_client()
    ## Delete multiple keys and values from the database
    if not key:
        response.status_code = 400
        return "Please provide a key!"
    key_arr = key.split(",")
    for key in key_arr:
        redis_client.delete(key)
    return "Deleted multiple keys and values from database!"

@app.post("/upload_file/{key}")
def upload_picture(response: Response, key: str, file: bytes = File()):
    redis_client = get_redis_client()
    ## Upload a picture to the database
    if not file:
        response.status_code = 400
        return "Please provide a file!"
    else:
        redis_client.set(key, file)
        response
        return "File uploaded!"

# @app.post("/files/")
# async def create_file(file: bytes | None = File(default=None)):
#     if not file:
#         return {"message": "No file sent"}
#     else:
#         return {"file_size": len(file)}

# @app.post("/file_upload")
# async def file_upload(response: Response, file: bytes = File(...)):
#     redis_client  = get_redis_client()
#     if not file:
#         response.status_code = 400
#         return "Please provide a file!"
#     else:
#         redis_client.set("file", file)
#         return "File uploaded!"