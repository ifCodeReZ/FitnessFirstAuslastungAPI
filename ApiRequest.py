import sqlite3
import requests
from datetime import datetime


#CREATE DATABASE
con = sqlite3.connect('database.db')
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS fitnessFirstAuslastung (Zeit text, Gendarmenmarkt double, PrenzlauerBerg double, Steglitz double, Wilmersdorf double, Zehlendorf double)''')

#API-Request @param clubNumber, @return utilization
def auslastung(clubNumber):
    url = f"https://www.fitnessfirst.de/club/api/checkins/{clubNumber}"
    data = requests.get(url).json()
    checkins = data['data']['check_ins']
    allowedPeople = data['data']['allowed_people']
    auslastung = round((checkins / allowedPeople) * 100, 1)
    return auslastung

if __name__ == "__main__":
    auslastungGedarmenmarkt = auslastung(clubNumber="berlin12")
    auslastungPrenzlauerBerg = auslastung(clubNumber="berlin2")
    auslastungSteglitz = auslastung(clubNumber="berlin3")
    auslastungWilmersdorf = auslastung(clubNumber="berlin10")
    auslastungZehlendorf = auslastung(clubNumber="berlin11")
    #GET TIME AND DATE
    datumZeit = datetime.today()
    # COPY DATA TO DATABASE
    cur.execute(f'''INSERT INTO fitnessFirstAuslastung VALUES ('{datumZeit}','{auslastungGedarmenmarkt}','{auslastungPrenzlauerBerg}','{auslastungSteglitz}','{auslastungWilmersdorf}','{auslastungZehlendorf}')''')
    con.commit()


# Debug
# print(auslastung)
# print(datumZeit)
# print(checkins)
# print(allowedPeople)