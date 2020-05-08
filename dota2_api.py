import requests

def get_api_json(url):
    try:
        r = requests.get(url, timeout=3)
        response_dict = r.json()
        return response_dict
    except:
        return get_api_json(url)

if __name__ == '__main__':
    pass