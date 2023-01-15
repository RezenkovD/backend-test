import os

from fastapi import APIRouter, File, UploadFile
from pydrive2.drive import GoogleDrive
from pydrive2.auth import GoogleAuth

from crud import upload_to_google_drive
from crud import get_file_for_key

router = APIRouter()

folder_id = os.getenv("folder_id")


@router.post("/upload-file/")
async def upload_file(data: UploadFile = File(...)):
    try:
        g_auth = GoogleAuth()
        drive = GoogleDrive(g_auth)
        g_auth.LocalWebserverAuth()
        upload_to_google_drive(
            drive=drive, g_auth=g_auth, data=data, folder_id=folder_id
        )
        return {"Success": True}

    except Exception as ex:
        print("Error: ", str(ex))
        return {"Success": False}


@router.get("/get-file/")
async def get_file(key: str):
    try:
        g_auth = GoogleAuth()
        drive = GoogleDrive(g_auth)
        get_file_for_key(drive=drive, key=key, folder_id=folder_id)
        return {"Success": True}

    except Exception as ex:
        print("Error: ", str(ex))
        return {"Success": False}
