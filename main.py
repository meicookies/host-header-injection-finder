#!/usr/bin/python
# pip install yuyu
import requests
from yuyu_scanner import subdomain
import sys

req = requests.session()
try:
  domain = sys.argv[1]
  foundSubdo = False
  getSubdo = subdomain.check(domain).result
  listUrl = None
  if getSubdo:
    listUrl = getSubdo
    foundSubdo = True
  if foundSubdo:
    for site in getSubdo:
      try:
        response = req.get(f"http://{site}", headers={
          "X-Forwarded-Host": "evil.com"
        }, allow_redirects=False, timeout=3)
        try:
          loc = response.headers["Location"]
          vulnerable = False
          if "evil.com" in loc and response.status_code == 302:
            vulnerable = True
          if vulnerable:
              print(f"{site} Vulnerable")
              with open("saved.txt", "a") as file:
                file.write(f"{site}\n")
          if not vulnerable:
              print(f"{site} Not Vulnerable")
        except KeyError:
          print(f"{site} Not Found")
      except:
        print(f"{site} ERROR")
except IndexError:
  print("usage ./main.py domain")
except:
  print(f"{site} ERROR")
