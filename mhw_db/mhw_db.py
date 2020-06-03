import requests
import json

class Client:

  def _url(self, path):

    return 'https://mhw-db.com' + path



  def get(self, path, params):

    url = self._url(path)
    return requests.get(url, params=params)




# TODO: Look into making methods that make http calls async
class Monster:

  def __init__(self, name):

    self.name = name



  def _path(self):

    return '/monsters'



  def weaknesses(self):

    q = {
      'name': {
        '$like': self.name + '%'
      }
    }
    p = {
      'name': True,
      'weaknesses': True
    }
    params = {
      'q': json.dumps(q),
      'p': json.dumps(p)
    }

    c = Client()
    response = c.get(self._path(), params)
    if response.status_code == 200:
      _json = response.json()
      if len(_json) > 0:
        return _json

    return []

