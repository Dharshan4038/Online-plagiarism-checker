from googleapiclient.discovery import build
def search(keywords):
    api_key = 'AIzaSyC9ophsAVPp8e8BDY7CM5IM0_X5uf-3gt4'
    service = build('customsearch', 'v1', developerKey=api_key)
    result = service.cse().list(q=keywords, cx='9324b599048c04bd5', num=10).execute()
    #if no result found
    if 'items' not in result:
        return []
    it = result['items']
    return it