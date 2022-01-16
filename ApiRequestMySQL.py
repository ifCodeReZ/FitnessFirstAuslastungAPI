import mysql.connector
import requests
import datetime

# Get time only
timeCode = datetime.datetime.now()
currentTime = timeCode.strftime("%H:%M")
currentHourStr = timeCode.strftime("%H")
currentHour = int(currentHourStr)
print(currentHour)
# Create Database
dateObj = datetime.date.today()
dateStr = dateObj.strftime("%d%b%Y")
mydb = mysql.connector.connect(user='USER', password='PASSWORD',
                               host='HOSTIP',
                               database='DATABASE')
dbcursor = mydb.cursor()
dbcursor.execute(
    "CREATE TABLE IF NOT EXISTS Auslastung" + dateStr + "(Zeit text, Gendarmenmarkt double, PrenzlauerBerg "
                                                        "double, Steglitz double, Wilmersdorf double, "
                                                        "Zehlendorf double)")


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

    # Check Time and Copy data to database
    if 23 > currentHour > 5:
        dbcursor.execute(f'''INSERT INTO Auslastung{dateStr} VALUES ('{currentTime}',
        '{auslastungGedarmenmarkt}',
        '{auslastungPrenzlauerBerg}',
        '{auslastungSteglitz}',
        '{auslastungWilmersdorf}',
        '{auslastungZehlendorf}')''')
        mydb.commit()
        dbcursor.close()
        mydb.close()
    else:
        exit()
