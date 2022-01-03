import sqlite3
import requests
from datetime import datetime

#CONST
clubNumber = "berlin11"
checkins = 0
allowedPeople = 0

#SQL-DB erzeugen
con = sqlite3.connect('daten.db')
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS fitnessFirstAuslastung (Zeit text, Prozent double)''')



# API-Request
url = f"https://www.fitnessfirst.de/club/api/checkins/{clubNumber}"
data = requests.get(url).json()
datumZeit = datetime.today()
checkins = data['data']['check_ins']
allowedPeople = data['data']['allowed_people']
auslastung = round((checkins / allowedPeople) * 100, 1)

# Funktionstest
# print(auslastung)
# print(datumZeit)
# print(checkins)
# print(allowedPeople)

#DATEN IN SQL-DB ÜBERTRAGEN
cur.execute(f'''INSERT INTO fitnessFirstAuslastung VALUES ('{datumZeit}','{auslastung}')''')
con.commit()
