import os

from fastapi import FastAPI, responses, status, HTTPException, UploadFile
from pydantic import BaseModel

import templates

app = FastAPI()
server_folder = "server_side_folder"


class File(BaseModel):
    name: str
    data: bytes


@app.get("/")
def root():
    return responses.HTMLResponse(templates.HOME_PAGE)


@app.get("/apis")
def apis():
    return responses.RedirectResponse("/")


@app.get("/apis/files")
def get_file(filename: str):
    path = os.path.join(server_folder, filename)

    if not os.path.exists(path):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "File not found")
    elif os.path.isdir(path):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Requested file is a directory")

    return responses.FileResponse(path=path, filename=filename, media_type="application/octet-stream")


@app.get("/apis/files/all_names")
def get_all_filenames():
    return [file for file in os.listdir(server_folder) if not file.startswith(".")]


@app.post("/apis/files/upload")
def upload_file(file: UploadFile):
    path = os.path.join(server_folder, file.filename)
    if os.path.exists(path):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "File already exists")

    with open(path, 'wb') as f:
        f.write(file.file.read())


@app.put("/apis/files/edit")
def replace_file_data(file: UploadFile):
    new_data = file.file.read()
    path = os.path.join(server_folder, file.filename)
    if not os.path.exists(path):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "File not found")
    elif os.path.isdir(path):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Requested file is a directory")

    with open(path, 'wb') as f:
        f.write(new_data)


@app.delete("/apis/files/delete")
def delete_file(filename):
    path = os.path.join(server_folder, filename)
    if not os.path.exists(path):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "File not found")
    elif os.path.isdir(path):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Requested file is a directory")

    os.remove(path)
