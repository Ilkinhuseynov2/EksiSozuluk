import json
info = open('info.json', 'r')
info = json.load(info)
entry_list = info[0]['entry']