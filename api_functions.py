import requests
import json


def readDatabase(databaseId, headers):
    readUrl = f"https://api.notion.com/v1/databases/{databaseId}/query"

    res = requests.request("POST", readUrl, headers=headers)

    return res.json()


def updatePage(pageId, headers, updateData):
    updateUrl = f"https://api.notion.com/v1/pages/{pageId}"

    data = json.dumps(updateData)

    response = requests.request("PATCH", updateUrl, headers=headers, data=data)

    return response.status_code
