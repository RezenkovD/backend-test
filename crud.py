import json
import requests

from fastapi import UploadFile


def search_file_in_drive(drive, key, folder_id: str):
    file_list = drive.ListFile(
        {"q": f"'{folder_id}' in parents and trashed=false"}
    ).GetList()
    for file in file_list:
        if key == file["title"]:
            return file
    return None


def upload_to_google_drive(drive, g_auth, data: UploadFile, folder_id: str):
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
    file = search_file_in_drive(drive, key, folder_id)
    if file is not None:
        file_id = f"{file['id']}"
        requests.put(
            f"https://www.googleapis.com/upload/drive/v2/files/{file_id}?uploadType=multipart",
            headers={"Authorization": "Bearer " + g_auth.credentials.access_token},
            files=files,
        )
    else:
        requests.post(
            "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
            headers={"Authorization": "Bearer " + g_auth.credentials.access_token},
            files=files,
        )


def get_file_for_key(drive, key, folder_id: str):
    file = search_file_in_drive(drive, key, folder_id)
    if file is not None:
        file.GetContentFile(file["title"])
