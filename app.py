from flask import Flask
from flask import render_template
from flask import request, redirect


'''
Start script
 . venv/bin/activate
 python -m flask run
'''


class Message:
  def __init__(self, timeStamp, name, msg):
    self.timeStamp = timeStamp
    self.name = name
    self.msg = msg



timestampBool = False
nameBool = False
msgBool = False

timeStampInfo = ""
nameInfo = ""
msgInfo = ""

container = []

# for line in FileContent:
#   #
#   if "[" in line: #This next part will be a time stamp...
#     #record the next segment of data



with open("./data/data.txt") as fileobj:
  for line in fileobj:
    for char in line: 
      #  print(char)

      if char == "]":
        timestampBool = False

      elif char == "<":
        nameBool = True

      elif char == ">":
        nameBool = False
        msgBool = True

      elif char == "[":
        timestampBool = True
        if msgBool == True:
          container.append(Message(timeStampInfo, nameInfo, msgInfo))
          #re initialize temp vars
          timeStampInfo = ""
          nameInfo = ""
          msgInfo = ""
          msgBool = False
      else:
        if timestampBool == True:
          timeStampInfo += char
        #  print(timeStampInfo)

        if nameBool == True:
          nameInfo += char
        #  print(nameInfo)

        if msgBool == True:
          msgInfo += char
        #  print(msgInfo)

container.append(Message(timeStampInfo, nameInfo, msgInfo)) #after exiting the loop, the temp variables are still stored so we can append the final message...

def showSitreps(): #function that prints all sitreps of the given file
  ret = []
  for i in range(len(container)):
    temp = container[i]
    if temp.name == "115 FAB BTL NCO":
      if "SITREP" in temp.msg:

        ret.append(temp)
  return ret



def recentSitrep(): #function that prints all sitreps of the given file
  
  for i in range(len(container)):
    temp = container[i]
    if temp.name == "115 FAB BTL NCO":
      if "SITREP" in temp.msg:
          mostRecent = temp
    

        
  return mostRecent


def allSaluteReport():
    ret = [] 
    for i in range(len(container)):
        temp = container[i]
        if temp.name == "115 FAB BTL NCO":
            ret.append(temp)
    return ret
      
def recentSalute():
    for i in range(len(container)):
        temp = container[i]
        if temp.name == "115 FAB BTL NCO":
            if "SALUTE REPORT" in temp.msg:
                mostRecent = temp


    return mostRecent     

def authors():
    seen = {}

    for i in range(len(container)):
        temp = container[i]
        if temp.name in seen:
            seen[temp.name] += 1
        else:
            seen[temp.name] = 0
    return len(seen)

def ammoStat(): #displays most recent ammo status
  for i in range(len(container)):
    temp = container[i]
    if temp.name == "115 FAB BTL NCO":
      if "SITREP" in temp.msg:
        if "Ammo Status: Green" in temp.msg:
          ammo = "Green"
        elif "Ammo Status: Red" in temp.msg:
          ammo = "Red"
        elif "Ammo Status: Amber" in temp.msg:
          ammo = "Amber"
        elif "Ammo Status: Black" in temp.msg:
          ammo = "Black"
        elif "Ammo Status: N.A" in temp.msg:
          ammo = "Not Available"

  return ammo

def fuelStat(): #displays most recent fuel status 
  for i in range(len(container)):
    temp = container[i]
    if temp.name == "115 FAB BTL NCO":
      if "SITREP" in temp.msg:
        if "Fuel Status: Green" in temp.msg:
          fuel = "Green"
        elif "Fuel Status: Amber" in temp.msg:
          fuel = "Amber"
        elif "Fuel Status: Black" in temp.msg:
          fuel = "Black"
        elif "Fuel Status: Red" in temp.msg:
          fuel = "Red"
        elif "Fuel Status: N.A" in temp.msg:
          fuel = "Not Available"

  return fuel

def staffStat(): #displays most recent personnel status 
  for i in range(len(container)):
    temp = container[i]
    if temp.name == "115 FAB BTL NCO":
      if "SITREP" in temp.msg:
        if "Personnel Status: Red" in temp.msg:
          personnel = "Red"
        elif "Personnel Status: Green" in temp.msg:
          personnel = "Green"
        elif "Personnel Status: Amber" in temp.msg:
          personnel = "Amber"
        elif "Personnel Status: Black" in temp.msg:
          personnel = "Black"
        elif "Personnel Status: N.A" in temp.msg:
          personnel = "Not Available"

  return personnel
 
# for i in range(len(sitreps)):
#     temp = sitreps[i]
#     print("\n\nSITREP report at: ", temp.timeStamp)
#     print("Content of SITREP: ", temp.msg)


app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('./index.html')

'''
@app.route("/upload-txt", methods=["GET", "POST"])
def upload_image():

    if request.method == "POST":

        if request.files:

            image = request.files["text"]

            print(image)

            return redirect(request.url)


    return render_template("./index.html")
'''

@app.route("/processing", methods=["GET", "POST"])
def processing():

    if request.method == "GET":

        return render_template("./processing.html")

    return render_template("./index.html")


@app.route("/final", methods=["GET", "POST"])
def final():
    total = len(container)
    authorTotal = authors()
    mostRecent = recentSitrep()
    salute = recentSalute()
    personnel = staffStat()
    ammo = ammoStat()
    fuel = fuelStat()
    
    return render_template("./final.html", totalMessages=total, totalAuthors=authorTotal, sitRep = mostRecent, saluteReport = salute, ammoStatus = ammo, fuelStatus = fuel, personnelStatus = personnel)


@app.route("/allSitreps", methods=["GET", "POST"])
def allSitreps():
    sitreps = showSitreps()
    

    return render_template("./allSitreps.html", finalSitreps=sitreps)


@app.route("/allReports", methods=["GET", "POST"])
def reports():
    allReports = allSaluteReport()
    for report in allReports:
        if "ACK" in report.msg:
            allReports.remove(report)

    return render_template("./allReports.html", reports=allReports)


@app.route("/allMessages", methods=["GET", "POST"])
def allMessages():
    

    return render_template("./allMessages.html", messages=container)
