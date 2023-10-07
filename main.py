import sqlite3
import requests
from bs4 import BeautifulSoup

response = requests.get("https://sinoptik.ua/погода-днепр-303007131")

class GetInfo:
    def __init__(self, dateInfo=0, temperatureInfo=0):
        self.dateInfo = dateInfo
        self.temperature = temperatureInfo

    def getInfo(self, dayId):
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, features="html.parser")
            soupList = soup.findAll("div", {"id": f"bd{dayId}"})
            # print(soupList)

            resultDay = soupList[0].find("p", {"class": "date"})
            resultMonth = soupList[0].find("p", {"class": "month"})
            resultTemperature = soupList[0].find("div", {"class": "temperature"})

            self.dateInfo = f"{resultDay.text} {resultMonth.text}"
            self.temperatureInfo = resultTemperature.text

con = sqlite3.connect("hw_10_db.sl3")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS weather (date TEXT, temperature TEXT)")
cur.execute("DELETE FROM weather")
for i in range(7):
    info = GetInfo()
    info.getInfo(i+1)
    cur.execute("INSERT INTO weather (date, temperature) values (?, ?)",(info.dateInfo, info.temperatureInfo))

cur.execute("SELECT date, temperature FROM weather")
print(cur.fetchall())
con.commit()
con.close()
