from flask import Flask, request, Response
import subprocess
import json
import threading

from methods import internal_methods
from logger import loggingThreadFunc, getHealthSummary


app = Flask(__name__)



from methods.getAppStatus import getAppStatus

@app.route('/<facility_id>/getAppStatus')
def getAppStatusWrapper(facility_id) -> Response:
  return getAppStatus(facility_id)



from methods.getAppInfo import getAppInfo

@app.route('/<facility_id>/getAppInfo')
def getAppInfoWrapper(facility_id) -> Response:
  return getAppInfo(facility_id)



from methods.startApp import startApp

@app.route('/<facility_id>/startApp', methods=['POST'])
def startAppWrapper(facility_id) -> Response:
  return startApp(facility_id)



from methods.stopApp import stopApp

@app.route('/<facility_id>/stopApp', methods=['POST'])
def stopAppWrapper(facility_id) -> Response:
  return stopApp(facility_id)



from methods.pauseApp import pauseApp

@app.route('/<facility_id>/pauseApp', methods=['POST'])
def pauseAppWrapper(facility_id) -> Response:
  return pauseApp(facility_id)



from methods.unpauseApp import unpauseApp

@app.route('/<facility_id>/unpauseApp', methods=['POST'])
def unpauseAppWrapper(facility_id) -> Response:
  return unpauseApp(facility_id)



from methods.restartApp import restartApp

@app.route('/<facility_id>/restartApp', methods=['POST'])
def restartAppWrapper(facility_id) -> Response:
  return restartApp(facility_id)




from methods.killApp import killApp

@app.route('/<facility_id>/killApp', methods=['POST'])
def killAppWrapper(facility_id) -> Response:
  return killApp(facility_id)



from methods.getAppNames import getAppNames

@app.route('/<facility_id>/getAppNames')
def getAppNamesWrapper(facility_id):
  return getAppNames(facility_id)




@app.route('/<facility_id>/getHealthSummary')
@internal_methods.verifyFacilityID
@internal_methods.verifyDockerEngine
@internal_methods.verifyAppName
def getHealthSummaryWrapper(facility_id, app_name="", app_id="") -> Response:

  # validating duration
  duration = request.args.get("duration")
  if duration == None:
    return Response("No summary duration provided", status=400)

  if duration not in ["hour", "day", "week", "month"]:
    return Response("Invalid duration", status=400)

  # getting summary from logger
  output = getHealthSummary(app_name, duration)
  if output == None:
    return Response(f"Could not find log for \"{app_name}\"", status=400)
  return Response(json.dumps(output), 200)




if __name__ == '__main__':
  print("\n\n\n")

  print("Starting logging thread")
  logThread = threading.Thread(target=loggingThreadFunc, daemon=True)
  logThread.start()
  print("Starting flask server")
  app.run()