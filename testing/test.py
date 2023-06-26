from requests import get, post
from colorama import Fore
from datetime import datetime
import subprocess

totalTests = 0
successfulTests = 0

def test(testname:str, method:str, url:str, expectedCode:int):
  global totalTests, successfulTests

  startTime = datetime.now()
  totalTests += 1
  print(f"{'{:47.47}'.format(testname):}: ", end='')
  response = None
  if method == "GET":
    response = get(url)
  elif method == "POST":
    response = post(url)
  else:
    print("test error")
    return False

  duration = (datetime.now() - startTime).microseconds // 1000
  if response.status_code == expectedCode:
    print(f"{Fore.GREEN}SUCCESS {Fore.RESET}" + f"({duration}ms)".rjust(8))
    successfulTests += 1
    return True
  else:
    print(f"{Fore.RED}FAIL     {Fore.RESET}({str(duration).rjust(3)}ms) - expected {expectedCode}, got {response.status_code}")
    print("-" * 60)
    print(response.text[:300])
    print("-" * 60)
    return False


if __name__ == "__main__":

  # test parameters
  BASE_URL = "http://127.0.0.1:5000"
  FACILITY_ID = "demo"
  USER_NAME = "test"
  IMAGE_NAME = "httpd" # <-- this should already be installed
  TEST_IMAGE = "hello-world" # <-- this one should not be installed

  APP_NAME = f"{IMAGE_NAME}.{USER_NAME}"

  def startApp(app_name): subprocess.run(f"docker start {app_name}", shell=True, capture_output=True)
  def killApp(app_name): subprocess.run(f"docker kill {app_name}", shell=True, capture_output=True)
  def removeImage(image): subprocess.run(f"docker rmi {image}", shell=True, capture_output=True)
  def createApp(image, user): subprocess.run(f"docker create --name {image}.{user} {image}", shell=True, capture_output=True)
  def deleteApp(app_name): subprocess.run(f"docker rm {app_name}", shell=True, capture_output=True)

  print("\nStarting testing...")
  startTime = datetime.now()

  print()
  test("Create app - success",                           "POST", f"{BASE_URL}/{FACILITY_ID}/createApp?image={IMAGE_NAME}&user={USER_NAME}", 200)
  test("Create app - app already exists",                "POST", f"{BASE_URL}/{FACILITY_ID}/createApp?image={IMAGE_NAME}&user={USER_NAME}", 400)
  test("Create app - invalid facility ID",               "POST", f"{BASE_URL}/iaminvalid/createApp?image={IMAGE_NAME}&user={USER_NAME}", 400)
  test("Create app - invalid image name",                "POST", f"{BASE_URL}/{FACILITY_ID}/createApp?image=iaminvalid&user={USER_NAME}", 400)
  test("Create app - no image name",                     "POST", f"{BASE_URL}/{FACILITY_ID}/createApp?user={USER_NAME}", 400)
  test("Create app - no user name",                      "POST", f"{BASE_URL}/{FACILITY_ID}/createApp?image={IMAGE_NAME}", 400)

  print()
  test("Start container - success",                      "POST", f"{BASE_URL}/{FACILITY_ID}/startApp?name={APP_NAME}", 200)
  test("Start container - invalid facility ID",          "POST", f"{BASE_URL}/iaminvalid/startApp?name={APP_NAME}", 400)
  test("Start container - invalid app name",             "POST", f"{BASE_URL}/{FACILITY_ID}/startApp?name=iaminvalid", 400)
  test("Start container - no app name",                  "POST", f"{BASE_URL}/{FACILITY_ID}/startApp", 400)

  print()
  createApp(IMAGE_NAME, USER_NAME + "2")
  createApp(IMAGE_NAME, USER_NAME + "3")
  test("Batch start container",                          "POST", f"{BASE_URL}/{FACILITY_ID}/startApp?name={APP_NAME},{APP_NAME}2,{APP_NAME}3", 200)
  test("Batch stop container",                           "POST", f"{BASE_URL}/{FACILITY_ID}/stopApp?name={APP_NAME},{APP_NAME}2,{APP_NAME}3", 200)
  deleteApp(APP_NAME + "2")
  deleteApp(APP_NAME + "3")


  print()
  test("Stop container - success",                       "POST", f"{BASE_URL}/{FACILITY_ID}/stopApp?name={APP_NAME}", 200)
  test("Stop container - invalid facility ID",           "POST", f"{BASE_URL}/iaminvalid/stopApp?name={APP_NAME}", 400)
  test("Stop container - invalid app name",              "POST", f"{BASE_URL}/{FACILITY_ID}/stopApp?name=iaminvalid", 400)
  test("Stop container - no app name",                   "POST", f"{BASE_URL}/{FACILITY_ID}/stopApp", 400)
  startApp(APP_NAME)

  print()
  test("Pause container - success",                      "POST", f"{BASE_URL}/{FACILITY_ID}/pauseApp?name={APP_NAME}", 200)
  test("Pause container - invalid facility ID",          "POST", f"{BASE_URL}/iaminvalid/pauseApp?name={APP_NAME}", 400)
  test("Pause container - invalid app name",             "POST", f"{BASE_URL}/{FACILITY_ID}/pauseApp?name=iaminvalid", 400)
  test("Pause container - no app name",                  "POST", f"{BASE_URL}/{FACILITY_ID}/pauseApp", 400)

  print()
  test("Unpause container - success",                    "POST", f"{BASE_URL}/{FACILITY_ID}/unpauseApp?name={APP_NAME}", 200)
  test("Unpause container - invalid facility ID",        "POST", f"{BASE_URL}/iaminvalid/unpauseApp?name={APP_NAME}", 400)
  test("Unpause container - invalid app name",           "POST", f"{BASE_URL}/{FACILITY_ID}/unpauseApp?name=iaminvalid", 400)
  test("Unpause container - no app name",                "POST", f"{BASE_URL}/{FACILITY_ID}/unpauseApp", 400)

  print()
  test("Restart container - success",                    "POST", f"{BASE_URL}/{FACILITY_ID}/restartApp?name={APP_NAME}", 200)
  test("Restart container - invalid facility ID",        "POST", f"{BASE_URL}/iaminvalid/restartApp?name={APP_NAME}", 400)
  test("Restart container - invalid app name",           "POST", f"{BASE_URL}/{FACILITY_ID}/restartApp?name=iaminvalid", 400)
  test("Restart container - no app name",                "POST", f"{BASE_URL}/{FACILITY_ID}/restartApp", 400)

  print()
  test("Kill container - success",                       "POST", f"{BASE_URL}/{FACILITY_ID}/killApp?name={APP_NAME}", 200)
  test("Kill container - invalid facility ID",           "POST", f"{BASE_URL}/iaminvalid/killApp?name={APP_NAME}", 400)
  test("Kill container - invalid app name",              "POST", f"{BASE_URL}/{FACILITY_ID}/killApp?name=iaminvalid", 400)
  test("Kill container - no app name",                   "POST", f"{BASE_URL}/{FACILITY_ID}/killApp", 400)
  startApp(APP_NAME)

  print()
  test("Get container names - success",                  "GET", f"{BASE_URL}/{FACILITY_ID}/getAppNames", 200)
  test("Get container names - invalid facility ID",      "GET", f"{BASE_URL}/iaminvalid/getAppNames", 400)

  print()
  test("Get container status - success",                 "GET", f"{BASE_URL}/{FACILITY_ID}/getAppStatus", 200)
  test("Get container status - success (specific app)",  "GET", f"{BASE_URL}/{FACILITY_ID}/getAppStatus?name={APP_NAME}", 200)
  test("Get container status - invalid facility ID",     "GET", f"{BASE_URL}/iaminvalid/getAppStatus?name={APP_NAME}", 400)
  test("Get container status - invalid app name",        "GET", f"{BASE_URL}/{FACILITY_ID}/getAppStatus?name=iaminvalid", 400)

  print()
  test("Get container stats - success",                 "GET", f"{BASE_URL}/{FACILITY_ID}/getAppStats", 200)
  test("Get container stats - success (specific app)",  "GET", f"{BASE_URL}/{FACILITY_ID}/getAppStats?name={APP_NAME}", 200)
  test("Get container stats - invalid facility ID",     "GET", f"{BASE_URL}/iaminvalid/getAppStats?name={APP_NAME}", 400)
  test("Get container stats - invalid app name",        "GET", f"{BASE_URL}/{FACILITY_ID}/getAppStats?name=iaminvalid", 400)

  print()
  test("Get container info - success",                   "GET", f"{BASE_URL}/{FACILITY_ID}/getAppInfo?name={APP_NAME}", 200)
  test("Get container info - invalid facility ID",       "GET", f"{BASE_URL}/iaminvalid/getAppInfo?name={APP_NAME}", 400)
  test("Get container info - invalid app name",          "GET", f"{BASE_URL}/{FACILITY_ID}/getAppInfo?name=iaminvalid", 400)
  test("Get container info - no app name",               "GET", f"{BASE_URL}/{FACILITY_ID}/getAppInfo", 400)

  print()
  test("Get uptime summary - success",                   "GET", f"{BASE_URL}/{FACILITY_ID}/getUptimeSummary?name={APP_NAME}&duration=day", 200)
  test("Get uptime summary - invalid facility ID",       "GET", f"{BASE_URL}/iaminvalid/getUptimeSummary?name={APP_NAME}&duration=day", 400)
  test("Get uptime summary - invalid app name",          "GET", f"{BASE_URL}/{FACILITY_ID}/getUptimeSummary?name=iaminvalid&duration=day", 400)
  test("Get uptime summary - invalid duration",          "GET", f"{BASE_URL}/{FACILITY_ID}/getUptimeSummary?name={APP_NAME}&duration=bad", 400)
  test("Get uptime summary - no duration",               "GET", f"{BASE_URL}/{FACILITY_ID}/getUptimeSummary?name={APP_NAME}", 400)

  print()
  test("Get images - success",                           "GET", f"{BASE_URL}/{FACILITY_ID}/getImages", 200)
  test("Get images - invalid facility ID",               "GET", f"{BASE_URL}/iaminvalid/getImages", 400)

  print()
  test("Request Image - success",                        "POST", f"{BASE_URL}/{FACILITY_ID}/requestImage?image={TEST_IMAGE}", 200)
  test("Request Image - invalid facility ID",            "POST", f"{BASE_URL}/iaminvalid/requestImage?image={TEST_IMAGE}", 400)
  test("Request Image - invalid image name",             "POST", f"{BASE_URL}/{FACILITY_ID}/requestImage?image=iaminvalid", 400)
  test("Request Image - no image name",                  "POST", f"{BASE_URL}/{FACILITY_ID}/requestImage?", 400)
  removeImage(TEST_IMAGE)

  print()
  test("Delete container - invalid facility ID",         "POST", f"{BASE_URL}/iaminvalid/deleteApp?name={APP_NAME}", 400)
  test("Delete container - invalid app name",            "POST", f"{BASE_URL}/{FACILITY_ID}/deleteApp?name=iaminvalid", 400)
  test("Delete container - no app name",                 "POST", f"{BASE_URL}/{FACILITY_ID}/deleteApp", 400)
  test("Delete container - success",                     "POST", f"{BASE_URL}/{FACILITY_ID}/deleteApp?name={APP_NAME}", 200)

  duration = datetime.now() - startTime
  print(f"\n\nCompleted testing, {successfulTests}/{totalTests} tests successful (took {round(duration.total_seconds(), 2)} seconds)")
