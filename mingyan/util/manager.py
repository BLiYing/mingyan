import requests

proxypool_url = 'http://127.0.0.1:5555/random'

# 获取redis中ip
def get_random_proxy_from_redis():
    """
    get random proxy from proxypool
    :return: proxy
    """
    return requests.get(proxypool_url).text.strip()
