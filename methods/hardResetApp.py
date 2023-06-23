import subprocess
from flask import Response, request
from . import internal_methods

@internal_methods.verifyFacilityID
@internal_methods.verifyDockerEngine
@internal_methods.verifyAppName
def hardResetApp(facility_id, app_name="", app_id="") -> Response:
  """
  This method deletes then re-creates a container, clearing all data

  parameters:
    facility_id - this value is passed in the API route, for demo purposes this should always be "demo"
    app_name - this value is passed as an http parameter
  """

  completedProcess = subprocess.run(f"docker inspect {app_name} --format \"{{{{.Config.Image}}}}\"", capture_output=True)
  image_name = completedProcess.stdout.decode().strip()

  # stopping container
  subprocess.run(f"docker stop {app_id}", capture_output=True)
  # deleting container
  completedProcess = subprocess.run(f"docker rm {app_id}", capture_output=True)
  if completedProcess.returncode != 0:
    return Response(f"Failed to delete app", status=500)

  # re-creating container
  completedProcess = subprocess.run(f"docker create --name \"{app_name}\" --pull never \"{image_name}\"", capture_output=True)
  if completedProcess.returncode != 0:
    return Response(f"Failed to create app {image_name}", status=500)

  return Response("Success", status=200)