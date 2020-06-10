import json

import httpx


class Client:

    def _url(self, path):
        return 'https://mhw-db.com' + path

    async def get(self, path, params):
        url = self._url(path)
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)

        if response.status_code == 200:
            return response.json()
        return None


class Monster:

    def __init__(self, name):
        self.name = name

    def _path(self):
        return '/monsters'

    async def weaknesses(self):
        q = {
            'name': {
                '$like': self.name + '%'
            }
        }
        p = {
            'name': True,
            'resistances': True,
            'weaknesses': True
        }
        params = {
            'q': json.dumps(q),
            'p': json.dumps(p)
        }

        c = Client()
        _json = await c.get(self._path(), params)
        if _json is not None and len(_json) > 0:
            return _json
        return []
