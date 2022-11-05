import requests

url = "http://127.0.0.1:5000/perform_query"

payload = {
   'file_name': 'apache_logs.txt',
   'cmd1': 'regex',
   'value1': 'images/\\w+\\.png',
   'cmd2': 'sort',
   'value2': 'asc'
}

"""
payload={
  'file_name': 'apache_logs.txt',
  'cmd1': 'filter',
  'value1': 'GET',
  'cmd2': 'map',
  'value2': '0',
  'cmd3': 'unique',
  'value3': '',
  'cmd4': 'sort',
  'value4': 'desc',
  'cmd5': 'limit',
  'value5': '10'
}
"""

# response = requests.request("POST", url, data=payload)
response = requests.request("POST", url, params=payload)
print(response.text)
