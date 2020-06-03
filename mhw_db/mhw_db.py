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



  # TODO: add error handling
  def weaknesses(self):

    q = {
      'name': self.name,
    }
    p = {
      'weaknesses': True
    }
    params = {
      'q': json.dumps(q),
      'p': json.dumps(p)
    }

    c = Client()
    response = c.get(self._path(), params)
    _json = response.json()
    if len(_json) == 1:
      if 'weaknesses' in _json[0]:
        return _json[0]['weaknesses']
    return []

