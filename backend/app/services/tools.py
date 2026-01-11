from datetime import datetime, timedelta

DELHI_ZONES = {
    "ROHINI": {"coords": (28.7041, 77.1025), "areas": ["rohini", "pitampura"]},
    "SOUTH": {"coords": (28.5494, 77.2001), "areas": ["saket", "hauz khas"]},
    "CENTRAL": {"coords": (28.6448, 77.2115), "areas": ["karol bagh", "paharganj"]},
    "WEST": {"coords": (28.6219, 77.0878), "areas": ["janakpuri", "dwarka"]}
}

def detect_zone_and_coords(text: str):
    text = text.lower() if text else ""
    for zone, data in DELHI_ZONES.items():
        for area in data["areas"]:
            if area in text: return zone, data["coords"]
    return "CENTRAL", (28.6139, 77.2090)

def calculate_sla(category: str):
    hours = 24 if "clean" in category.lower() else 48
    deadline = (datetime.now() + timedelta(hours=hours)).isoformat()
    return hours, deadline