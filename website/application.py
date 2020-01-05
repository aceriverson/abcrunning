import os
import datetime as DT
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from math import trunc
from requests import get
import json
from datetime import datetime

from helpers import login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///runlog.db")

@app.route("/")
@login_required
def index():
    username = db.execute("SELECT username FROM users WHERE id=(:userid)", userid=session["user_id"])
    activities = db.execute("SELECT * FROM activities WHERE userid IN (SELECT userid FROM joingroups WHERE groupid IN (SELECT groupid FROM joingroups WHERE userid=(:userid))) AND userid != (:userid2) ORDER BY activities.timestamp DESC, activities.id DESC LIMIT 10", userid=session["user_id"], userid2=session["user_id"])
    persactivities = db.execute("SELECT * FROM activities WHERE userid=(:userid) ORDER BY activities.timestamp DESC, activities.id DESC LIMIT 10", userid=session["user_id"])


    distances = []
    paces = []
    times = []
    timestamps = []
    userids = []
    users = []
    names = []
    activityids = []
    types = []

    persdistances = []
    perspaces = []
    perstimes = []
    perstimestamps = []
    persnames = []
    persactivityids = []
    perstypes = []

    groupslist = []
    groupsdict = {}
    z=[]

    for activity in activities:
        distances.append(activity['distance'])
        paces.append(activity['formattedpace'])
        times.append(activity['formattedtime'])
        timestamps.append(activity['timestamp'])
        userids.append(activity['userid'])
        names.append(activity['name'])
        activityids.append(activity['id'])
        types.append(activity['runtype'])

    for a in range(len(userids)):
        gtemp = db.execute("SELECT name FROM groups WHERE id IN (SELECT groupid FROM joingroups WHERE userid=:userid) AND id IN (SELECT groupid FROM joingroups WHERE userid=:userid1)", userid=userids[a], userid1 = session['user_id'])
        groupslist.append(gtemp)
        groupsdict.update({userids[a]:groupslist})
        groupslist = []

    for persactivity in persactivities:
        persdistances.append(persactivity['distance'])
        perspaces.append(persactivity['formattedpace'])
        perstimes.append(persactivity['formattedtime'])
        perstimestamps.append(persactivity['timestamp'])
        persnames.append(persactivity['name'])
        persactivityids.append(persactivity['id'])
        perstypes.append(persactivity['runtype'])


    for userid in userids:
        user = db.execute("SELECT username FROM users WHERE id=(:userid)", userid=userid)
        for row in user:
            list.append(users, row["username"])


    i = range(len(distances))
    k = range(len(persdistances))
    z=[]
    for d in range(len(userids)):
        z.append(len(groupsdict[userids[d]][0]))
    length = len(distances)


    return render_template("index.html", username=username[0]['username'], users=users, distances=distances, paces=paces, times=times, timestamps=timestamps, names=names, types=types, i=i, persdistances=persdistances, perspaces=perspaces, perstimes=perstimes, perstimestamps=perstimestamps, persnames=persnames, k=k, groupsdict=groupsdict, userids=userids, z=z, profid=session["user_id"], activityids=activityids, persactivityids=persactivityids, perstypes=perstypes, lenght=length)


@app.route("/activity", methods=["GET"])
def activity():
    try:
        username = db.execute("SELECT username FROM users WHERE id=(:userid)", userid=session["user_id"])[0]['username']
    except:
        username = None

    if request.method == "GET":

        """Get activity id"""
        url = request.url
        url = ''.join(reversed(url))
        url = url.split("=")[0]
        url = ''.join(reversed(url))

        """Get activity information"""
        activity = db.execute("SELECT * FROM activities WHERE id=(:activityid)", activityid=float(url))

        """Get username, gear nickname, and gear mileage"""
        if not activity[0]['gearid']:
            gear = 'N/A'
            mileage = 'N/A'
        else:
            gear = db.execute("SELECT nickname FROM gear WHERE id=(:gearid)", gearid=activity[0]['gearid'])
            mileage = db.execute("SELECT mileage FROM gear WHERE id=(:gearid)", gearid=activity[0]['gearid'])
            gear = gear[0]
            mileage = mileage[0]['mileage']
            print(mileage)
            mileage = round(float(mileage), 2)
            print(mileage)
        user = db.execute("SELECT username FROM users WHERE id=(:userid)", userid=activity[0]['userid'])

        """Void fields that were not entered by the user"""
        if not activity[0]['hrmax']:
            activity[0]['hrmax'] = 'N/A'
        if not activity[0]['hravg']:
            activity[0]['hravg'] = 'N/A'
        if not activity[0]['elevation']:
            activity[0]['elevation'] = 'N/A'

        try:
            profid = session["user_id"]
        except:
            profid = None

        return render_template("activity.html", user=user[0]['username'], distance=activity[0]['distance'], pace=activity[0]['formattedpace'], time=activity[0]['formattedtime'], timestamp=activity[0]['timestamp'], gear=gear, mileage=mileage, name=activity[0]['name'], hrmax=activity[0]['hrmax'], hravg=activity[0]['hravg'], elevation=activity[0]['elevation'], additional=activity[0]['additional'], userid=activity[0]['userid'], username=username, profid=profid)


@app.route("/gear", methods=["GET", "POST"])
@login_required
def gear():
    username = db.execute("SELECT username FROM users WHERE id=(:userid)", userid=session["user_id"])[0]["username"]

    if request.method == "GET":
        gears = db.execute("SELECT * FROM gear WHERE userid=(:userid) AND status=0", userid=session["user_id"])
        retgears = db.execute("SELECT * FROM gear WHERE userid=(:userid) AND status=1", userid=session["user_id"])

        brands = []
        models = []
        nicknames = []
        ids = []
        mileages = []
        retbrands, retmodels, retnicknames, retids, retmileages = ([] for i in range(5))

        for gear in gears:
            brands.append(gear['brand'])
            models.append(gear['model'])
            nicknames.append(gear['nickname'])
            ids.append(gear['id'])
            mileages.append(round(gear["mileage"], 2))

        for retgear in retgears:
            retbrands.append(retgear['brand'])
            retmodels.append(retgear['model'])
            retnicknames.append(retgear['nickname'])
            retids.append(retgear['id'])
            retmileages.append(round(retgear["mileage"], 2))

        i = range(len(ids))
        k = range(len(retids))

        return render_template("gear.html", brands=brands, models=models, nicknames=nicknames, ids=ids, mileages=mileages, i=i, retbrands=retbrands, retmodels=retmodels, retnicknames=retnicknames, retids=retids, retmileages=retmileages, k=k, username=username, profid=session["user_id"])

    else:
        brand = request.form.get("brand")
        model = request.form.get("model")
        nickname = request.form.get("nickname")
        db.execute("INSERT INTO gear (userid, brand, model, nickname) VALUES (:userid, :brand, :model, :nickname)", userid=session["user_id"], brand=brand, model=model, nickname=nickname)

        retireid = request.form.get("retireid")
        db.execute("UPDATE gear SET status = 1 WHERE id=(:gearid)", gearid=retireid)

        removeid = request.form.get("removeid")
        db.execute("DELETE FROM gear WHERE id=(:gearid)", gearid=removeid)

        return redirect("/gear")

@app.route("/group", methods=["GET", "POST"])
@login_required
def group():
    username = db.execute("SELECT username FROM users WHERE id=(:userid)", userid=session["user_id"])[0]["username"]

    if request.method == "GET":
        try:
            """Select groupid of all groups the user is a member of"""
            groups = db.execute("SELECT groupid FROM joingroups WHERE userid=(:userid) GROUP BY groupid", userid=session["user_id"])
            groupinfos = []
            print(groups)
            print(groupinfos)

            """Select name of all groups the user is a member of"""
            for row in groups:
                list.append(groupinfos, db.execute("SELECT name FROM groups WHERE id IN (:groups)", groups=row["groupid"]))

            print(groupinfos)

            groupids = []
            groupnames = []

            """Convert dictionary to list of group ids"""
            for group in groups:
                groupids.append(group["groupid"])


            print(groupids)

            for groupinfo in groupinfos:
                groupnames.append(groupinfo[0]["name"])

            print(groupnames)
            print("here2")

            i = range(len(groups))
            page1 = 1

            """Get arguments for userid and page number"""
            try:
                args = request.args
                print("249")
                page = int(args["page"])
                print("251")
                groupid = int(args["groupid"])
                print("253")
            except:
                args["groupid"][0] = None
                args["page"][0] = 1
                return render_template("group.html", i=i, groupnames=groupnames, groupids=groupids, page1=page1, username=username, page=1, noshow=1)

            print(args)
            print(page)
            print(groupid)
            print("here2")

            try:
                groupname = db.execute("SELECT name FROM groups WHERE id=(:groupid)", groupid=int(args["groupid"]))
                print(groupname)
                groupname = groupname[0]['name']
                print("1")
                groupid = int(args["groupid"])
            except:
                groupname = None
                groupid = 5
                print("Here")

            print(groupname)
            print(groupid)
            print("here")

            offset = (-1 + int(args["page"])) * 15

            try:
                details = db.execute("SELECT * FROM groups WHERE id=(:groupid)", groupid=groupid)
                name = details[0]["name"]
                bio = details[0]["bio"]
                adminid = details[0]["adminid"]

                print("281")
                adminname = db.execute("SELECT username FROM users WHERE id=(:adminid)", adminid=adminid)
            except:
                name = None
                bio = None
                print(286)

            print(288)

            backpage = int(args["page"]) - 1
            nextpage = int(args["page"]) + 1

            userids = []

            try:
                usersids = db.execute("SELECT userid FROM joingroups WHERE groupid=(:groupid)", groupid=groupid)
                for usersid in usersids:
                    userids.append(usersid["userid"])
                activities = db.execute("SELECT * FROM activities WHERE userid IN (:usersids) ORDER BY activities.timestamp DESC, activities.id DESC LIMIT 15 OFFSET (:offset)", usersids=userids, offset=offset)
            except:
                activities = None

            k = range(len(activities))

            distances = []
            paces = []
            times = []
            timestamps = []
            users = []
            names = []
            ids = []
            runtypes = []
            runuserids = []
            runusernames = []

            try:
                for activity in activities:
                    distances.append(activity['distance'])
                    paces.append(activity['formattedpace'])
                    times.append(activity['formattedtime'])
                    timestamps.append(activity['timestamp'])
                    names.append(activity['name'])
                    ids.append(activity['id'])
                    runtypes.append(activity['runtype'])
                    runuserids.append(activity['userid'])
            except:
                groupid = None

            print(runuserids)

            try:
                for runuserid in runuserids:
                    runusername = db.execute("SELECT username FROM users WHERE id=(:runuserid)", runuserid=runuserid)
                    print('292')
                    runusernames.append(runusername[0]['username'])
                    print('294')
            except:
                runusernames = None

            page = int(args["page"])

            if not page:
                page = 1

            return render_template("group.html", runusernames=runusernames, name=name, bio=bio, runtypes=runtypes, runuserids=runuserids, i=i, k=k, username=username, groupid=groupid, groupids=groupids, groupnames=groupnames, distances=distances, paces=paces, times=times, timestamps=timestamps, users=users, names=names, ids=ids, page1 = page1, page=page, backpage=backpage, nextpage=nextpage, profid=session["user_id"], noshow=0, adminname=adminname, adminid=adminid)

        except:
            print("Exception")
            return render_template("group.html", groupids=groupids, groupnames=groupnames, page1=page1, username=username, profid=session["user_id"], i=i)

    else:
        return render_template("group.html")


@app.route("/creategroup", methods=["GET", "POST"])
@login_required
def creategroup():
    """Create a group"""
    username = db.execute("SELECT username FROM users WHERE id=(:userid)", userid=session["user_id"])[0]["username"]

    if request.method == "GET":
        return render_template("creategroup.html", username=username, profid=session["user_id"])

    else:
        groupname = request.form.get("groupname")
        bio = request.form.get("bio")
        if not groupname:
            return apology("Must enter a name", 403)
        elif not bio:
            return apology("Must enter a description", 403)
        elif db.execute("SELECT COUNT(adminid) FROM groups WHERE adminid=(:userid)", userid=session["user_id"])[0]['COUNT(adminid)'] >= 3:
            return apology("No more than 3 groups can be created per user", 403)
        elif not db.execute("SELECT id FROM groups WHERE name=:groupname", groupname=groupname):
            db.execute("INSERT INTO groups (name, bio, adminid) VALUES (:groupname, :bio, :userid)", groupname=groupname, bio=bio, userid=session["user_id"])
            groupid = db.execute("SELECT id FROM groups WHERE name=:groupname", groupname=groupname)
            groupint = int(groupid[0]["id"])
            db.execute("INSERT INTO joingroups (groupid, userid) VALUES (:groupid, :userid)", groupid=groupint, userid=session["user_id"])
            return redirect("/")
        else:
            return apology("This name is taken", 403)

@app.route("/joingroup", methods=["GET", "POST"])
@login_required
def joingroup():
    """Join a group"""
    username = db.execute("SELECT username FROM users WHERE id=(:userid)", userid=session["user_id"])[0]["username"]

    if request.method == "GET":
        rows = db.execute("SELECT * FROM groups ORDER BY members DESC")
        currentgroupssql = db.execute("SELECT groupid FROM joingroups WHERE userid=:user_id", user_id=session["user_id"])
        currentgroups = []
        for row in currentgroupssql:
            list.append(currentgroups, row["groupid"])

        for row in rows:
            if row["id"] in currentgroups:
                alltest = True
            else:
                alltest = False

        """Convert current url to just group id after clicking 'Join'"""
        url = request.url
        url = ''.join(reversed(url))
        url = url.split("=")[0]
        url = ''.join(reversed(url))

        try:
            if db.execute("SELECT * FROM joingroups WHERE groupid=(:groupid) AND userid=(:userid)", groupid=float(url), userid=session["user_id"]):
                message = "Can't join this group now"
            else:
                db.execute("INSERT INTO joingroups (groupid, userid) VALUES (:groupid, :userid)", groupid=float(url), userid=session["user_id"])

                members = db.execute("SELECT members FROM groups WHERE id=(:groupid)", groupid=float(url))
                members = int(members[0]['members']) + 1
                db.execute("UPDATE groups SET members=(:members) WHERE id=(:groupid)", members=members, groupid=float(url))
        except:
            url = None

        return render_template("joingroup.html", rows=rows, url=url, currentgroups=currentgroups, username=username, profid=session["user_id"], alltest=alltest)

    else:
        groupid = request.form.get("joingroupid")
        try:
            if db.execute("SELECT * FROM joingroups WHERE groupid=(:groupid) AND userid=(:userid)", groupid=groupid, userid=session["user_id"]):
                return apology("Already joined group", 403)
            elif not db.execute("SELECT * FROM groups WHERE id=(:groupid)", groupid=groupid):
                return apology("Nonexistent Group ID", 403)
            else:
                db.execute("INSERT INTO joingroups (groupid, userid) VALUES (:groupid, :userid)", groupid=groupid, userid=session["user_id"])

                members = db.execute("SELECT members FROM groups WHERE id=(:groupid)", groupid=groupid)
                members = int(members[0]['members']) + 1
                db.execute("UPDATE groups SET members=(:members) WHERE id=(:groupid)", members=members, groupid=groupid)
        except:
            url = None

        return redirect("/joingroup")


@app.route("/leavegroup", methods=["GET", "POST"])
@login_required
def leavegroup():
    """Leave a group"""
    username = db.execute("SELECT username FROM users WHERE id=(:userid)", userid=session["user_id"])[0]["username"]

    if request.method == "GET":
        rows = db.execute("SELECT * FROM groups WHERE id IN (SELECT groupid FROM joingroups WHERE userid=:user_id) AND adminid!=:user_id;", user_id=session["user_id"])
        return render_template("leavegroup.html", username=username, rows=rows, profid=session["user_id"])

    else:
        groupid = request.form.get("groupid")
        db.execute("DELETE FROM joingroups WHERE groupid=:groupid AND userid=:user_id;", groupid=int(groupid), user_id=session["user_id"])
        members = db.execute("SELECT members FROM groups WHERE id=:groupid", groupid=int(groupid))
        members = int(members[0]['members']) - 1
        return redirect("/")

@app.route("/login", methods=["GET", "POST"]) # Carried over from finance
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout") # Carried over from finance
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/new", methods=["GET", "POST"])
@login_required
def new():
    if request.method == "GET":
        gear = db.execute("SELECT nickname, id FROM gear WHERE userid = :userid AND status = 0", userid = session['user_id'])
        username = db.execute("SELECT username FROM users WHERE id=:userid", userid=session['user_id'])
        today = datetime.today().strftime('%Y-%m-%d')
        return render_template("new.html", gear = gear, length = len(gear), username=username[0]["username"], profid=session["user_id"], today=today)
    else:
        hours = request.form.get("hours")
        minutes = request.form.get("minutes")
        seconds = request.form.get("seconds")
        distance = float(request.form.get("distance"))
        name = request.form.get("name")
        date = request.form.get("date")
        shoeid = request.form.get("gearid")
        runtype = request.form.get("type")

        try:
            additional = request.form.get("additional")
        except:
            additional = None
        try:
            hravg = float(request.form.get("hravg"))
        except:
            hravg = None
        try:
            hrmax = float(request.form.get("hrmax"))
        except:
            hrmax = None
        try:
            elevation = float(request.form.get("elevation"))
        except:
            elevation = None

        if shoeid:
            gearmileage = db.execute("SELECT mileage FROM gear WHERE id=:gearid", gearid=shoeid)
            newgearmileage = gearmileage[0]["mileage"] + distance
            db.execute("UPDATE gear SET mileage=:newgearmileage WHERE id=:gearid", gearid=shoeid, newgearmileage=newgearmileage)

        if int(seconds) < 10:
            seconds = "0" + seconds

        if not hours or hours == 0:
            minutetime = float(minutes) + float(seconds)/60
            formattedtime = minutes + ":" + seconds
        else:
            if int(minutes) < 10:
                minutes = "0" + minutes
            minutetime = float(hours) * 60 + float(minutes) + float(seconds)/60
            formattedtime = hours + ":" + minutes + ":" + seconds

        pace = minutetime/distance

        paceminutes = trunc(pace)
        paceseconds = round((pace % 1) * 60)

        if paceseconds < 10:
            formattedpace = str(paceminutes) + ":0" + str(paceseconds)
        else:
            formattedpace = str(paceminutes) + ":" + str(paceseconds)

        try:
            db.execute("INSERT INTO activities (userid, distance, timestamp, pace, time, gearid, name, hravg, hrmax, elevation, formattedtime, formattedpace, additional, runtype) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", session['user_id'], round(distance, 2), date, round(pace, 2), round(minutetime, 2), shoeid, name, hravg, hrmax, elevation, formattedtime, formattedpace, additional, runtype)
        except:
            db.execute("INSERT INTO activities (userid, distance, pace, timestamp, time, name, hravg, hrmax, elevation, formattedtime, formattedpace, additional, runtype) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", session['user_id'], round(distance, 2), round(pace, 2), date, round(minutetime, 2), name, hravg, hrmax, elevation, formattedtime, formattedpace, additional, runtype)

        return redirect("/")

@app.route("/password", methods=["GET", "POST"]) # Carried over from finance
@login_required
def password():
    """Changes Password"""
    if request.method == "GET":
        return render_template("password.html")
    else:

        # Stores Form Input
        current = request.form.get("current")
        new = request.form.get("password")
        confirmation = request.form.get("confirmation")
        sqlhash = db.execute("SELECT hash FROM users WHERE id=:user_id", user_id=session["user_id"])

        # Checks conditions
        if not current or not new or not confirmation:
            return apology("Must complete all fields", 403)
        elif not check_password_hash(sqlhash[0]["hash"], current):
            return apology("Current password incorrect", 403)
        elif new != confirmation:
            return apology("New passwords do not match", 403)
        if new == current:
            return apology("New password cannot be the same as the current password", 403)
        else:

            # Changes password in users
            hashword = generate_password_hash(new)
            db.execute("UPDATE users SET hash=:hashword WHERE id=:user_id", user_id=session["user_id"], hashword=hashword)
            return render_template("psuccess.html")


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():

    username = db.execute("SELECT username FROM users WHERE id=(:userid)", userid=session["user_id"])[0]["username"]

    """Get arguments for userid and page number"""
    try:
        args = request.args
    except:
        args["userid"] = session["user_id"]
        args["page"] = 1

    try:
        profname = db.execute("SELECT username FROM users WHERE id=(:userid)", userid=float(args["userid"]))
        profname = profname[0]['username']
        userid = int(args["userid"])
    except:
        profname = db.execute("SELECT username FROM users WHERE id=(:userid)", userid=session["user_id"])
        profname = profname[0]['username']
        userid = session["user_id"]

    details = db.execute("SELECT * FROM users WHERE id=(:userid)", userid=userid)

    offset = (-1 + float(args["page"])) * 15
    activities = db.execute("SELECT * FROM activities WHERE userid=(:userid) ORDER BY activities.timestamp DESC, activities.id DESC LIMIT 15 OFFSET (:offset)", userid=userid, offset=offset)

    backpage = int(args["page"]) - 1
    nextpage = int(args["page"]) + 1

    distances = []
    paces = []
    times = []
    timestamps = []
    userids = []
    users = []
    names = []
    ids = []
    runtypes = []
    week = []

    for activity in activities:
        distances.append(activity['distance'])
        paces.append(activity['formattedpace'])
        times.append(activity['formattedtime'])
        timestamps.append(activity['timestamp'])
        userids.append(activity['userid'])
        names.append(activity['name'])
        ids.append(activity['id'])
        runtypes.append(activity['runtype'])

    sumsql = db.execute("SELECT SUM(distance), SUM(pace), COUNT(id), SUM(time) FROM activities WHERE userid=(:user_id)", user_id=userid)
    if not sumsql[0]["SUM(distance)"]:
        totaldist = 0
    else:
        totaldist = round(sumsql[0]["SUM(distance)"], 1)

    totalpace = sumsql[0]["SUM(pace)"]
    totalnumofruns = sumsql[0]["COUNT(id)"]

    if not totalnumofruns:
        totalavgdist = 0
        totalavgpace = 0
    else:
        totalavgdist = round(totaldist/totalnumofruns, 1)
        totalavgpace = totalpace/totalnumofruns

    if not sumsql[0]["SUM(time)"]:
        totaltime = 0
    else:
        totaltime = round(sumsql[0]["SUM(time)"]/60, 1)

    if not totalpace:
        totalpace = 0

    paceminutes = trunc(totalavgpace)
    paceseconds = round((totalavgpace % 1) * 60)

    if paceseconds < 10:
        formattedtotalavgpace = str(paceminutes) + ":0" + str(paceseconds)
    else:
        formattedtotalavgpace = str(paceminutes) + ":" + str(paceseconds)

    year = int(datetime.today().strftime('%Y'))
    month = int(datetime.today().strftime('%m'))
    day = int(datetime.today().strftime('%d'))

    dayweek = day - 7

    if dayweek < 1:
        if month in [1, 3, 5, 7, 8, 10, 12]:
            day = 31 + dayweek
        elif month in [4, 6, 9, 11]:
            day = 30 + dayweek
        elif year % 4 == 0:
            day = 29 + dayweek
        else:
            day = 28 + dayweek
        month = month - 1
    else:
        day = dayweek

    if month < 1:
        year = year - 1
        month = 12

    if day < 10:
        strday = "0" + str(day)
    else:
        strday = str(day)

    if month < 10:
        strmonth = "0" + str(month)
    else:
        strmonth = str(month)

    date = str(year) + "-" + strmonth + "-" + strday

    weeksql = db.execute("SELECT SUM(distance), SUM(pace), COUNT(id), SUM(time) FROM activities WHERE (timestamp BETWEEN :date AND CURRENT_DATE) AND userid=:userid;", userid=userid, date=date)

    if not weeksql[0]["SUM(distance)"]:
        weekdist = 0
    else:
        weekdist = round(weeksql[0]["SUM(distance)"], 1)
    totalweekpace = weeksql[0]["SUM(pace)"]
    if not weeksql[0]["SUM(time)"]:
        weektime = 0
    else:
        weektime = round(weeksql[0]["SUM(time)"]/60, 1)

    if not weeksql[0]["COUNT(id)"]:
        totalweeknumofruns = 0
        avgweekdist = 0
        avgweekpace = 0
    else:
        totalweeknumofruns = weeksql[0]["COUNT(id)"]
        avgweekdist = round(weekdist/totalweeknumofruns, 1)
        avgweekpace = totalweekpace/totalweeknumofruns


    wpaceminutes = trunc(avgweekpace)
    wpaceseconds = round((avgweekpace % 1) * 60)

    if wpaceseconds < 10:
        weekpace = str(wpaceminutes) + ":0" + str(wpaceseconds)
    else:
        weekpace = str(wpaceminutes) + ":" + str(wpaceseconds)

    i = range(len(ids))

    showchangepass = 0
    if userid==session['user_id']:
        showchangepass = 1

    currentgroups = db.execute("SELECT name, bio, id FROM groups WHERE id IN (SELECT groupid FROM joingroups WHERE userid=:userid)", userid=userid)

    return render_template("profile.html", LifetimeDistance=totaldist, weektime=weektime, avgweekdist=avgweekdist, avgdist = totalavgdist, currentgroups=currentgroups, LifetimePace=formattedtotalavgpace, totaltime=totaltime, date=date, weekdist=weekdist, weekpace=weekpace, username=username, profname=profname, args=args, distances=distances, paces=paces, times=times, timestamps=timestamps, names=names, ids=ids, runtypes=runtypes, i=i, page=int(args["page"][0]), userid=userid, backpage=backpage, nextpage=nextpage, profid=session["user_id"], showchangepass=showchangepass)


# Carried over from finance
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    """User sumbit"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        """Check if all inputs are valid and not an existing user"""
        if username == "":
            return apology("missing username", 403)
        if password == "":
            return apology("missing password", 403)
        if confirmation == "":
            return apology("missing confirm password", 403)
        if password != confirmation:
            return apology("passwords do not match", 403)
        existinguser = db.execute("SELECT id FROM users WHERE username=(:username)", username=username)
        if existinguser:
            return apology("username already taken", 403)

        """If all inputs are valid, insert into users table"""
        hashed = generate_password_hash(request.form.get("password"))
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hashed)", username=username, hashed=hashed)

        session.clear()

        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=username)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")


@app.route("/weather", methods=["GET", "POST"])
@login_required
def weather():
    if request.method == "GET":
        username = db.execute("SELECT username FROM users WHERE id=(:userid)", userid=session["user_id"])[0]["username"]
        return render_template("weather.html", username=username)

    else:
        username = db.execute("SELECT username FROM users WHERE id=(:userid)", userid=session["user_id"])[0]["username"]

        zipcode = str(request.form.get("zipcode"))
        city = request.form.get("city")
        countrycode = request.form.get("countrycode").lower()

        zcode = False
        c = False

        if zipcode:
            weatherurl = "http://api.openweathermap.org/data/2.5/weather?zip=" + zipcode + "," + countrycode + "&appid=7951f057c7201e2dd6fbba8c418e2ce3&units=imperial"
            zcode = True
        elif city:
            weatherurl = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "," + countrycode + "&appid=7951f057c7201e2dd6fbba8c418e2ce3&units=imperial"
            c = True

        if not weatherurl and zcode == False and c == False:
            return apology("Please enter a zipcode and/or city")
        elif not weatherurl and zcode == True and c == True:
            return apology("This feature is not supported in your location")
        elif not weatherurl and zcode == True:
            return apology("This feature is not supported for your zipcode. Try using your city instead!")
        elif not weatherurl and c == True:
            return apology("This feature is not supported for your city. Try using your zipcode instead!")

        # Thanks to openweathermap.org for the API
        forecast = get(weatherurl)

        # Getting necessary weather info
        temp = round(forecast.json()['main']['temp'])
        wind = forecast.json()['wind']['speed']
        weatherid = forecast.json()['weather'][0]['id']
        description = forecast.json()['weather'][0]['description'].capitalize()

        # Generating recommendations
        if weatherid in [200, 201, 202, 210, 211, 212, 221, 230, 231, 232]:
            idrec = "Stay indoors; running in a thunderstorm is unsafe."
        elif weatherid == 781:
            idrec = "Stay indoors; there's literally a tornado."
        elif weatherid == 771:
            idrec = "Stay indoors; the weather is unsafe for running."
        elif weatherid in [602, 621, 622]:
            idrec = "Stay indoors; running in these snowy coniditions is unsafe."
        elif weatherid in [300, 301, 302, 310, 311, 312, 500, 501, 520]:
            idrec = "It is raining; wear suitable warm clothing."
        elif weatherid in [502, 503, 504, 521, 522, 531]:
            idrec = "It is raining heavily; wear suitable waterproof clothing."
        elif weatherid in [511, 611, 612, 613, 616]:
            idrec = "It is both raining and cold; make sure to wear waterproof layers."
        elif weatherid in [600, 601, 620]:
            idrec = "It is snowing; wear warm clothes and procede with caution."
        elif weatherid in [711, 721, 731, 751, 761, 762]:
            idrec = "Stay indoors; the air quality is unsafe for running."
        elif weatherid in [800, 801, 802]:
            idrec = "Ideal running conditions."
        elif weatherid in [701, 741]:
            idrec = "Low visibility; procede with caution."
        elif weatherid in [803, 804]:
            idrec = "Overcast conditions; procede with caution."

        if temp > 75 and temp < 95:
            trec = "Wear minimal clothing, and remember to stay hydrated."
        elif temp >= 95:
            trec = "Wear as minimal clothing as possible, stay hydrated, and procede with caution."
        elif temp >= 60 and temp <= 75:
            trec = "Wear shorts and a shirt."
        elif temp >= 50 and temp < 60:
            trec = "Wear shorts and a shirt."
        elif temp >= 40 and temp < 50:
            trec = "Wear shorts and a longsleeve shirt."
        elif temp >= 25 and temp < 40:
            trec = "Wear a longsleeve shirt, jacket, gloves, and a hat."
        elif temp <= 20:
            trec = "Wear several layers of clothing, and procede with caution."

        return render_template("forecast.html", username=username, temp=temp, wind=wind, description=description, idrec=idrec, trec=trec)


def errorhandler(e): # Carried over from finance
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

def apology(message, code=400):
    """Render message as an apology to user."""
    username = db.execute("SELECT username FROM users WHERE id=(:userid)", userid=session["user_id"])[0]["username"]
    message = message.capitalize()

    return render_template("apology.html", top=code, bottom=message, code=code, username=username)