from app import app, cas
from flask import render_template, flash, redirect, url_for, request
from flask_cas import login_required
from app.models import User
from app.forms import AddFoodForm
from app.compose import getMatches, compose_email

def getUser(netid):
    email = netid + '@princeton.edu'
    users = User.objects(email=email)
    user = None
    if users:
        user = User.objects(email=email).first()
    else:
        user = User(email=email)
        user.prefs.append('chicken parm')
        user.prefs.append('dim sum')
        user.prefs.append('egg roll')
        user.save()
    return user


@app.route('/', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = getUser(cas.username)

    form = AddFoodForm()
    if form.validate_on_submit():
        food = form.food.data.lower()
        form.food.data = None
        if food not in user.prefs:
            if len(food) > 40:
                flash("pls don't spam", "error")
            else:
                user.prefs.append(food)
                user.save()
        return redirect(url_for('edit_profile'))
        #flash("New entry added!", "success")

    matches = getMatches(user)
    email = compose_email(matches)

    return render_template('edit_profile.html', prefs=user.prefs,
        form=form, email=email)

@app.route('/r', methods=['POST'])
def r():
    user = getUser(cas.username)

    food = request.form['food']
    if food in user.prefs:
        user.prefs.remove(food)
        user.save()

    return redirect(url_for('edit_profile'))
