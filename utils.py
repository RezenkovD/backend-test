import json
import requests

from fastapi import UploadFile
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive


def search_file_in_drive_or_none(
    drive: GoogleDrive, key: str, folder_id: str
) -> GoogleDrive:
    file_list = drive.ListFile(
        {"q": f"'{folder_id}' in parents and trashed=false"}
    ).GetList()
    for file in file_list:
        if key == file["title"]:
            return file


def upload_to_google_drive(
    drive: GoogleDrive, g_auth: GoogleAuth, data: UploadFile, folder_id: str
) -> int:
    key = data.filename
    value = data.file
    metadata = {
        "name": f"{key}",
        "parents": [folder_id],
    }
    files = {
        "data": ("metadata", json.dumps(metadata), "application/json"),
        "file": value,
    }
    file = search_file_in_drive_or_none(drive=drive, key=key, folder_id=folder_id)
    if file is not None:
        file_id = f"{file['id']}"
        response = requests.put(
            f"https://www.googleapis.com/upload/drive/v2/files/{file_id}?uploadType=multipart",
            headers={"Authorization": "Bearer " + g_auth.credentials.access_token},
            files=files,
        )
        return response.status_code
    else:
        response = requests.post(
            "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
            headers={"Authorization": "Bearer " + g_auth.credentials.access_token},
            files=files,
        )
        return response.status_code


def get_file_for_key(drive: GoogleDrive, key: str, folder_id: str) -> str:
    file = search_file_in_drive_or_none(drive=drive, key=key, folder_id=folder_id)
    if file is not None:
        file.GetContentFile(file["title"])
        return file["title"]
