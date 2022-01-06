import sqlite3
import requests
from datetime import datetime


# Create Database
con = sqlite3.connect('database.db')
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS fitnessFirstAuslastung (
Zeit text, Gendarmenmarkt double, PrenzlauerBerg double, Steglitz double, Wilmersdorf double, Zehlendorf double)''')


# API-Request @param clubNumber, @return utilization
def auslastung(clubnumber):
    url = f"https://www.fitnessfirst.de/club/api/checkins/{clubnumber}"
    data = requests.get(url).json()
    checkins = data['data']['check_ins']
    allowedPeople = data['data']['allowed_people']
    utilization = round((checkins / allowedPeople) * 100, 1)
    return utilization


if __name__ == "__main__":
    # Get Utilization
    auslastungGedarmenmarkt = auslastung(clubnumber="berlin12")
    auslastungPrenzlauerBerg = auslastung(clubnumber="berlin2")
    auslastungSteglitz = auslastung(clubnumber="berlin3")
    auslastungWilmersdorf = auslastung(clubnumber="berlin10")
    auslastungZehlendorf = auslastung(clubnumber="berlin11")
    # Get time and date
    datumZeit = datetime.today()
    # Copy data to database
    cur.execute(f'''INSERT INTO fitnessFirstAuslastung VALUES ('{datumZeit}',
    '{auslastungGedarmenmarkt}',
    '{auslastungPrenzlauerBerg}',
    '{auslastungSteglitz}',
    '{auslastungWilmersdorf}',
    '{auslastungZehlendorf}')''')
    con.commit()
