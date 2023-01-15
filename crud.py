import json
import requests

from fastapi import UploadFile


def upload_to_google_drive(g_auth, data: UploadFile, folder_id: str):
    key = data.filename
    value = data.file

    metadata = {"name": f"{key}", "parents": [folder_id]}
    files = {
        "data": ("metadata", json.dumps(metadata), "application/json"),
        "file": value,
    }

    requests.post(
        "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
        headers={"Authorization": "Bearer " + g_auth.credentials.access_token},
        files=files,
    )


def get_file_for_title(drive, key, folder_id):
    file_list = drive.ListFile(
        {"q": f"'{folder_id}' in parents and trashed=false"}
    ).GetList()
    for file in file_list:
        if key == file["title"]:
            file.GetContentFile(file["title"])
