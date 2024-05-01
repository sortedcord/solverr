from solverrapp.utils import Url
import urllib.parse
from .utils import Url
from enum import Enum
import requests


class ConnectorType(Enum):
    HTMLPARSE = 'HTML-PARSE'
    GETREQUEST = 'GET-REQUEST'
    COMPLEX = 'COMPLEX'


class Connector:
    tags = None

    def __init__(self, name: str, url: Url, tags: list[str], type: ConnectorType):
        self.name = name
        self.url = url
        self.tags = tags
        self.type = type

    def search(self, query: str) -> list:
        return []


class Sarthaks(Connector):
    search_url = f'https://www.sarthaks.com/search?q=%s'

    def __init__(self):
        self.name = 'sarthaks'
        self.type = ConnectorType.HTMLPARSE
        self.url = Url('https://www.sarthaks.com')
        self.tags = ['regular']

        super().__init__(name=self.name, type=self.type, tags=self.tags, url=self.url)

    def search(self, query: str) -> list:
        # Fix query
        query = urllib.parse.quote(query)
        search_url = self.search_url.replace("%s", query)

        html = requests.get(search_url, headers={
            'Referer': 'https://www.sarthaks.com/3632947/intersection-diagonals-rectangle-shifts-displacement-distance-particle-respectively',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Chromium";v="124", "Brave";v="124", "Not-A.Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
                            )
        print(html.content)

        return []
