def compose_email(matches):
    from datetime import datetime
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
            'Saturday', 'Sunday']

    meal = ["Breakfast", "Lunch", "Dinner"]

    days = [day + ": \n" for day in days]
    now = datetime.now()
    lastDate = now.weekday()
    week = [days[(lastDate + i) % 7] for i in range(7)]

    text = "Your weekly meals digest:\n\n"
    for j in range(7):
        for i in range(3):
            day = matches[i][j]

            if day:
                text += week[i]
                text += "\n"
                text += meal[i] + ": \n"
                for food, hall in day:
                    text += food + " in " + hall + "\n"
                text += "\n"

    text += "Best,\n\nAlex\n\nhttp://menu-alerts.herokuapp.com/"

    return text

def getMatches(user):
    import os
    import json
    import requests

    url = "https://tigermenus.herokuapp.com/api2"
    r = requests.get(url)
    l = json.loads(r.text)

    breakfastListList = l[0]
    lunchListList = l[1]
    dinnerListList = l[2]

    halls = ['Butler', 'CJL', 'Whitman', 'Roma', 'Forbes', 'Grad']
    matches = [[[] for i in range(7)] for j in range(3)]

    for k, mealListList in enumerate(l):
        for j, mealList in enumerate(mealListList): #each day
            for i, hall in enumerate(mealList): #each hall
                for food in hall:
                    for pref in user.prefs:
                        if pref.lower() in food['item'].lower():
                            matches[k][j].append((food['item'], halls[i]))

    return matches
