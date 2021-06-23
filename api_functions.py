import requests
import json
import os


def searchTeacher(username, headers):
    teachers_db = os.getenv('TEACHERS_DATABASE_ID')
    queryUrl = f"https://api.notion.com/v1/databases/{teachers_db}/query"

    with open('./jsons/search_teacher_query.json') as f:
        queryData = json.load(f)

    queryData['filter']['rich_text']['contains'] = username
    data = json.dumps(queryData)

    res = requests.request("POST", queryUrl, headers=headers, data=data)
    return res.json()['results'][0]['id']


def readDatabase(databaseId, headers):
    readUrl = f"https://api.notion.com/v1/databases/{databaseId}/query"

    res = requests.request("POST", readUrl, headers=headers)

    return res.json()


def createPage(databaseId, headers, username='undefined', text='undefined_message'):
    createUrl = 'https://api.notion.com/v1/pages'

    with open('./jsons/new_page.json') as f:
        newPageData = json.load(f)

    newPageData['parent']['database_id'] = databaseId
    newPageData['properties']['Padavan']['select']['name'] = username
    newPageData['properties']['Problem']['rich_text'][0]['text']['content'] = text
    newPageData['properties']['Teacher']['relation'][0]['id'] = searchTeacher(username, headers)
    print(searchTeacher(username, headers))

    data = json.dumps(newPageData)

    res = requests.request("POST", createUrl, headers=headers, data=data)

    return res.text


def updatePage(pageId, headers, updateData):
    updateUrl = f"https://api.notion.com/v1/pages/{pageId}"

    data = json.dumps(updateData)

    res = requests.request("PATCH", updateUrl, headers=headers, data=data)

    return res.status_code
