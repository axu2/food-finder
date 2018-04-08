import os
import json
import emails
import requests
from mongoengine import connect
from datetime import datetime
from app.models import User
from app import MONGODB_URI

connect("users", host=MONGODB_URI)

url = "https://tigermenus.herokuapp.com/api2"
r = requests.get(url)
l = json.loads(r.text)

breakfastListList = l[0]
lunchListList = l[1]
dinnerListList = l[2]

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
        'Saturday', 'Sunday']

days = [day + ": \n" for day in days]

halls = ['Butler', 'CJL', 'Whitman', 'Roma', 'Forbes', 'Grad']

now = datetime.now()
lastDate = now.weekday()
week = [days[(lastDate + i) % 7] for i in range(7)]

def compose_email(matches):
    text = "Your weekly dinner meals digest:\n\n"
    for i, day in enumerate(matches):
        if day:
            text += week[i]
            for food, hall in day:
                text += food + " in " + hall + "\n"
            text += "\n"
    text += "Best,\n\nAlex\n\nhttp://menu-alerts.herokuapp.com/"

    return text


for user in User.objects():
    matches = [[] for i in range(7)]
    for j, dinnerList in enumerate(dinnerListList): #each day
        for i, hall in enumerate(dinnerList): #each hall
            for food in hall:
                for pref in user.prefs:
                    if pref.lower() in food['item'].lower():
                        matches[j].append((food['item'], halls[i]))
    #print(matches)
    if matches != [[] for i in range(7)]:
        text = compose_email(matches)
        print(text + "\n")

        message = emails.html(text=text,
                              subject='Meals Mail',
                              mail_from='tigermenu@gmail.com')

        smtp = {'host':'smtp.googlemail.com',
                'port': 465,
                'ssl': True,
                'user': 'tigermenu',
                'password': os.getenv('MAIL_PASSWORD')}

        #r = message.send(to=user.email, smtp=smtp)

        #assert r.status_code == 250
