import requests
import os
import ssl
import urllib3
import time
import sys

pick = sys.argv[1]


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


with open(os.getenv("LOCALAPPDATA")+"\\Riot Games\\Riot Client\\Config\\lockfile", "r") as f:
    data = f.read().split(":")
 
s = requests.Session()
s.auth = ("riot", data[3])
base64_access = (s.get(f"{data[4]}://127.0.0.1:{data[2]}" + "/entitlements/v1/token", verify=ssl.CERT_NONE).json()["accessToken"])

h = {"Authorization": f'Bearer {base64_access}', "Content-Type": "application/json"}
uuid = (requests.get("https://auth.riotgames.com/userinfo", headers=h).json()["sub"])
entitlements_token = (requests.post("https://entitlements.auth.riotgames.com/api/token/v1", headers=h).json()["entitlements_token"])
h2 = {"X-Riot-Entitlements-JWT": entitlements_token, "Authorization": f"Bearer {base64_access}"}
agents = {}
for agent in requests.get("https://valorant-api.com/v1/agents?isPlayableCharacter=true").json()["data"]:
    agents[agent["displayName"]] = agent["uuid"]

print(agents[pick])
matchid = None
c = 0
while not matchid:
    try: 
        matchid = (requests.get('https://glz-eu-1.eu.a.pvp.net/pregame/v1/players/'+uuid,headers=h2).json()['MatchID'])
        print("Locking")
    except:
        c += 1
        print(f"Waiting.. {c}")
        time.sleep(1)
#Instalock delay to avoid 🅱an
time.sleep(2.5)
requests.post(f"https://glz-eu-1.eu.a.pvp.net/pregame/v1/matches/{matchid}/lock/{agents[pick]}",headers=h2)
print("Locked!")