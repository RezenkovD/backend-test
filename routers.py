import os

from fastapi import APIRouter, File, UploadFile
from pydrive2.drive import GoogleDrive
from pydrive2.auth import GoogleAuth

from crud import upload_to_google_drive
from crud import get_file_for_title

router = APIRouter()

folder_id = os.getenv("folder_id")


@router.post("/upload-file/")
async def upload_file(data: UploadFile = File(...)):
    try:
        g_auth = GoogleAuth()
        g_auth.LocalWebserverAuth()
        upload_to_google_drive(g_auth=g_auth, data=data, folder_id=folder_id)
        return {"Success": True}

    except Exception as ex:
        print("Error: ", str(ex))
        return {"Success": False}


@router.get("/get-file/")
async def get_file(key: str):
    try:
        gauth = GoogleAuth()
        drive = GoogleDrive(gauth)
        get_file_for_title(drive=drive, key=key, folder_id=folder_id)
        return {"Success": True}

    except Exception as ex:
        print("Error: ", str(ex))
        return {"Success": False}
