import requests
from bs4 import BeautifulSoup
import json
import re


def fetch_data():
    url = 'https://www.worldometers.info/coronavirus/'
    req = requests.get(url)
    if(req.status_code != 200):
        print("something wen wrong", req.status_code)
        return
    soup = BeautifulSoup(req.text, "html.parser")
    rows = soup.find("tbody").find_all("tr")
    data = {}
    regex = r"[+,/s]*"
    for row in rows:
        td = row.find_all("td")
        region = td[0].text
        data[region] = {}
        data[region]["total_cases"] = re.sub(regex, "", td[1].text)
        data[region]["new_cases"] = re.sub(regex, "", td[2].text)
        data[region]["total_deaths"] = re.sub(regex, "", td[3].text)
        data[region]["new_deaths"] = re.sub(regex, "", td[4].text)
        data[region]["total_recovered"] = re.sub(regex, "", td[5].text)
        data[region]["active_cases"] = re.sub(regex, "", td[6].text)
        data[region]["serious"] = re.sub(regex, "", td[7].text)
    print("fetched data")
    return data


def store_data(data):
    json_data = json.dumps(data)
    with open("data.json", "w") as f:
        f.write(json_data)
    print("saved as data.json")


store_data(fetch_data())
