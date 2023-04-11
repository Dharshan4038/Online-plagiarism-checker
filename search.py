from googleapiclient.discovery import build
def search(keywords):
    api_key = 'AIzaSyBkgLrf-RqqopoUxhqFmkOOrRoy0Bng5SM'
    service = build('customsearch', 'v1', developerKey=api_key)
    result = service.cse().list(q=keywords, cx='9324b599048c04bd5', num=10).execute()
    it = result['items']
    return it
# print(search('python'))