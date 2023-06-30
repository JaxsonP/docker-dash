import json
import flask
from . import internal_methods


@internal_methods.verifyFacilityID
@internal_methods.verifyDockerEngine(swarm_method=True)
def swarmGetAppNames(facility_id) -> flask.Response:
  """
  Returns an array of all running apps

  parameters:
    facility_id - this value is passed in the API route, for demo purposes this should always be "demo"
  """

  # executing system command
  completedProcess = internal_methods.subprocessRun(f"docker service ls --format \"{{{{.Name}}}}\"")
  if completedProcess.returncode != 0:
    return flask.make_response("Unknown error:\n"+completedProcess.stdout.decode()+"\n"+completedProcess.stderr.decode(), 500)

  arr = [s for s in completedProcess.stdout.decode().split("\n") if s != ""]

  return flask.make_response(json.dumps(arr), 200)