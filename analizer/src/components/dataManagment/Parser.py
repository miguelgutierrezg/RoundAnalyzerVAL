import orjson

def parse_instants(round_data):
    instants = {}
    alive_players = {p["puuid"] for p in round_data["playerStats"]}

    def add_event(time_ms, event):
        time_s = round(time_ms / 1000, 2)
        if time_s == 0.0:
            print(f"⚠️ Ignorando evento '{event['type']}' en roundTime 0.0s")
            return
        if time_s not in instants:
            instants[time_s] = {
                "roundTime": time_s,
                "players": [],
                "event": None
            }
        instants[time_s]["event"] = event
        print(f"🟢 Evento '{event['type']}' añadido en {time_s}s")

    def add_locations(time_ms, player_locations):
        time_s = round(time_ms / 1000, 2)
        if time_s == 0.0:
            return
        if time_s not in instants:
            instants[time_s] = {
                "roundTime": time_s,
                "players": [],
                "event": None
            }

        count = 0
        for loc in player_locations or []:
            if loc["puuid"] in alive_players:
                instants[time_s]["players"].append({
                    "puuid": loc["puuid"],
                    "location": loc["location"],
                    "viewRadians": loc["viewRadians"]
                })
                count += 1
        print(f"📍 Añadidas {count} ubicaciones en {time_s}s")

    # PLANT
    if round_data.get("plantRoundTime") is not None:
        plant_time_s = round(round_data["plantRoundTime"] / 1000, 2)
        if plant_time_s != 0.0:
            print("🌱 Procesando plant...")
            add_event(round_data["plantRoundTime"], {
                "type": "plant",
                "player": round_data.get("bombPlanter"),
                "location": round_data.get("plantLocation"),
                "site": round_data.get("plantSite")
            })
            add_locations(round_data["plantRoundTime"], round_data.get("plantPlayerLocations"))

    # DEFUSE
    if round_data.get("defuseRoundTime") is not None:
        defuse_time_s = round(round_data["defuseRoundTime"] / 1000, 2)
        if defuse_time_s != 0.0:
            print("🛡️ Procesando defuse...")
            add_event(round_data["defuseRoundTime"], {
                "type": "defuse",
                "player": round_data.get("bombDefuser"),
                "location": round_data.get("defuseLocation")
            })
            add_locations(round_data["defuseRoundTime"], round_data.get("defusePlayerLocations"))

    # KILLS
    print("🔫 Procesando kills...")
    for p in round_data["playerStats"]:
        for kill in p.get("kills", []):
            rt = kill["roundTime"]
            time_s = round(rt / 1000, 2)
            victim = kill["victim"]
            alive_players.discard(victim)

            add_event(rt, {
                "type": "kill",
                "killer": kill["killer"],
                "victim": victim,
                "assistants": kill.get("assistants", []),
                "location": kill["victimLocation"],
                "weapon": kill.get("finishingDamage", {}).get("damageItem")
            })

            add_locations(rt, kill.get("playerLocations") or [])

    sorted_instants = [instants[k] for k in sorted(instants.keys())]
    print(f"📦 Total de instantes generados: {len(sorted_instants)}")
    return sorted_instants


# Cargar y ejecutar
print("📂 Leyendo archivo roundData.json...")
with open("analizer/src/assets/games/roundData.json", "rb") as f:
    round_data = orjson.loads(f.read())

print("⚙️ Procesando ronda...")
instants = parse_instants(round_data)

print("💾 Guardando archivo instants.json...")
with open("analizer/src/assets/rounds/instants.json", "wb") as f:
    f.write(orjson.dumps(instants, option=orjson.OPT_INDENT_2))

print("✅ instants.json generado correctamente.")










import orjson
from collections import defaultdict

def parse_instants(round_data):
    instants = {}
    alive_players = {p["puuid"] for p in round_data["playerStats"]}

    def add_event(time_ms, event):
        time_s = round(time_ms / 1000, 2)
        if time_s == 0.0:
            print(f"⚠️ Ignorando evento '{event['type']}' en roundTime 0.0s")
            return
        if time_s not in instants:
            instants[time_s] = {
                "roundTime": time_s,
                "players": [],
                "event": None
            }
        instants[time_s]["event"] = event
        print(f"🟢 Evento '{event['type']}' añadido en {time_s}s")

    def add_locations(time_ms, player_locations):
        time_s = round(time_ms / 1000, 2)
        if time_s == 0.0:
            return
        if time_s not in instants:
            instants[time_s] = {
                "roundTime": time_s,
                "players": [],
                "event": None
            }

        count = 0
        for loc in player_locations or []:
            if loc["puuid"] in alive_players:
                instants[time_s]["players"].append({
                    "puuid": loc["puuid"],
                    "location": loc["location"],
                    "viewRadians": loc["viewRadians"]
                })
                count += 1
        print(f"📍 Añadidas {count} ubicaciones en {time_s}s")

    # PLANT
    if round_data.get("plantRoundTime") is not None:
        plant_time_s = round(round_data["plantRoundTime"] / 1000, 2)
        if plant_time_s != 0.0:
            print("🌱 Procesando plant...")
            add_event(round_data["plantRoundTime"], {
                "type": "plant",
                "player": round_data.get("bombPlanter"),
                "location": round_data.get("plantLocation"),
                "site": round_data.get("plantSite")
            })
            add_locations(round_data["plantRoundTime"], round_data.get("plantPlayerLocations"))

    # DEFUSE
    if round_data.get("defuseRoundTime") is not None:
        defuse_time_s = round(round_data["defuseRoundTime"] / 1000, 2)
        if defuse_time_s != 0.0:
            print("🛡️ Procesando defuse...")
            add_event(round_data["defuseRoundTime"], {
                "type": "defuse",
                "player": round_data.get("bombDefuser"),
                "location": round_data.get("defuseLocation")
            })
            add_locations(round_data["defuseRoundTime"], round_data.get("defusePlayerLocations"))

    # KILLS
    print("🔫 Procesando kills...")
    for p in round_data["playerStats"]:
        for kill in p.get("kills", []):
            rt = kill["roundTime"]
            time_s = round(rt / 1000, 2)
            victim = kill["victim"]
            alive_players.discard(victim)

            add_event(rt, {
                "type": "kill",
                "killer": kill["killer"],
                "victim": victim,
                "assistants": kill.get("assistants", []),
                "location": kill["victimLocation"],
                "weapon": kill.get("finishingDamage", {}).get("damageItem")
            })

            add_locations(rt, kill.get("playerLocations") or [])

    sorted_instants = [instants[k] for k in sorted(instants.keys())]
    print(f"📦 Total de instantes generados: {len(sorted_instants)}")

    # Obtener economía individual y por equipo
    print("💰 Calculando loadouts...")
    player_loadouts = {}
    team_loadouts = defaultdict(int)

    for p in round_data["playerStats"]:
        spent = p.get("economy", {}).get("spent", 0)
        puuid = p["puuid"]
        team = p.get("team", "Unknown")  # Si viene incluido el team
        player_loadouts[puuid] = spent
        team_loadouts[team] += spent

    return {
        "roundResultCode": round_data.get("roundResultCode", "Unknown"),
        "loadouts": {
            "players": player_loadouts,
            "teams": dict(team_loadouts)
        },
        "instants": sorted_instants
    }

# Cargar y ejecutar
print("📂 Leyendo archivo roundData.json...")
with open("analizer/src/assets/games/roundData.json", "rb") as f:
    round_data = orjson.loads(f.read())

print("⚙️ Procesando ronda...")
data = parse_instants(round_data)

print("💾 Guardando archivo instants.json...")
with open("analizer/src/data/instants.json", "wb") as f:
    f.write(orjson.dumps(data, option=orjson.OPT_INDENT_2))

print("✅ instants.json generado correctamente.")
