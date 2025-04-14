import requests

API_KEY = "RGAPI-2b2cb7ea-8791-420e-b4da-ebe4ccb12494"

GAME_NAME = "MiguelGG ツ"
TAG_LINE = "GANG"
REGION = "europe" 

HEADERS = {
    "X-Riot-Token": API_KEY
}

def get_puuid(game_name, tag_line):
    url = f"https://{REGION}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    res = requests.get(url, headers=HEADERS)
    if res.status_code == 200:
        return res.json()["puuid"]
    else:
        print("❌ Error al obtener PUUID:", res.status_code, res.text)
        return None

def get_match_history(puuid):
    url = f"https://{REGION}.api.riotgames.com/val/match/v1/matchlists/by-puuid/{puuid}"
    res = requests.get(url, headers=HEADERS)
    if res.status_code == 200:
        return res.json()["history"]
    else:
        print("❌ Error al obtener historial:", res.status_code, res.text)
        return []

def get_match_details(match_id):
    url = f"https://{REGION}.api.riotgames.com/val/match/v1/matches/{match_id}"
    res = requests.get(url, headers=HEADERS)
    if res.status_code == 200:
        return res.json()
    else:
        print("❌ Error al obtener detalles:", res.status_code, res.text)
        return None

puuid = get_puuid(GAME_NAME, TAG_LINE)
if puuid:
    print(f"✅ PUUID: {puuid}")
    matches = get_match_history(puuid)
    if matches:
        print(f"📊 Últimas partidas:")
        for match in matches[:3]: 
            print(f"- {match['matchId']}")
            match_data = get_match_details(match["matchId"])
            if match_data:
                print(f"  🗺️ Mapa: {match_data['mapId']}")
                print(f"  🎮 Jugadores: {len(match_data['players']['all_players'])}")
