import json
from bot import MHW

with open('./config.json') as f:
  config = json.load(f)

mhw = MHW(config)
mhw.run()
