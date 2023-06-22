import subprocess
from flask import Response, request
from . import internal_methods


@internal_methods.verifyFacilityID
@internal_methods.verifyDockerEngine
@internal_methods.verifyAppName
def deleteApp(facility_id, app_name="", app_id="") -> Response:
  """
  This method stops and deletes a container

  parameters:
    facility_id - this value is passed in the API route, for demo purposes this should always be "demo"
    image - this value is passed as an http parameter
  """

  # executing system commands
  subprocess.run(f"docker stop \"{app_name}\"")
  completedProcess = subprocess.run(f"docker rm \"{app_name}\"", capture_output=True)
  if completedProcess.returncode != 0:
    # uncaught error
    return Response(f"Failed to create app", status=500)

  return Response("Success", status=200)