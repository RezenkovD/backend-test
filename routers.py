import json
import os

from fastapi import APIRouter, File, UploadFile
from pydrive2.drive import GoogleDrive
from pydrive2.auth import GoogleAuth

from utils import upload_to_google_drive, get_file_for_key

router = APIRouter()

FOLDER_ID = os.getenv("FOLDER_ID")


@router.post("/upload-file/")
def upload_file(data: UploadFile = File(...)) -> json:
    try:
        g_auth = GoogleAuth()
        drive = GoogleDrive(g_auth)
        g_auth.LocalWebserverAuth()
        upload_to_google_drive(
            drive=drive, g_auth=g_auth, data=data, folder_id=FOLDER_ID
        )
        return {"Status": True}

    except Exception:
        return {"Success": False}


@router.get("/get-file/")
def get_file(key: str) -> json:
    try:
        g_auth = GoogleAuth()
        drive = GoogleDrive(g_auth)
        output = get_file_for_key(drive=drive, key=key, folder_id=FOLDER_ID)
        return {"Success": True, "file_name": output}

    except Exception as ex:
        print("Error: ", str(ex))
        return {"Success": False}
