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

halls = ['Butler', 'CJL', 'Whitman', 'Roma', 'Forbes', 'Grad']

now = datetime.now()
lastDate = now.weekday()
week = [days[(lastDate + i) % 7] for i in range(7)]

for user in User.objects():
    email = []
    for j, dinnerList in enumerate(dinnerListList): #each day
        for i, hall in enumerate(dinnerList): #each hall
            for food in hall:
                if food['item'] in user.prefs:
                    email.append(week[j] + ": " + food['item'] + " in " + halls[i])
        if email:
            email.append('\n')

    if email:
        text = "Your Food Alerts for the week:\n\n"
        text += "\n".join(email)
        text += "\n\nBest,\n\nMenu Alerts\n\n"
        text += "https://menu-alerts.herokuapp.com/admin"

        message = emails.html(text=text,
                              subject='Meals Mail',
                              mail_from='tigermenu@gmail.com')
        smtp = {'host':'smtp.googlemail.com',
                'port': 465,
                'ssl': True,
                'user': 'tigermenu',
                'password': os.getenv('MAIL_PASSWORD')}

        r = message.send(to=user.email, smtp=smtp)

        assert r.status_code == 250
