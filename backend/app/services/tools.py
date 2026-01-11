from datetime import datetime, timedelta
import random

def detect_zone_and_coords(location_name: str):
    """
    Mock function to detect zone and coordinates from a location name.
    """
    # Simply mapping some locations for demo purposes
    zones = {
        "Delhi": ("Central Zone", (28.6139, 77.2090)),
        "Karol Bagh": ("Karol Bagh Zone", (28.6528, 77.1906)),
        "Rohini": ("Rohini Zone", (28.7041, 77.1025)),
        "Dwarka": ("Najafgarh Zone", (28.5921, 77.0460)),
    }
    
    # Default to Central Zone if not found
    zone_info = zones.get(location_name, ("Central Zone", (28.6139, 77.2090)))
    return zone_info

def calculate_sla(category: str):
    """
    Calculate SLA (Service Level Agreement) based on complaint category.
    Returns (sla_hours, deadline_datetime).
    """
    sla_map = {
        "Garbage": 24,
        "Street Light": 48,
        "Pothole": 72,
        "Drainage": 24,
        "General": 48
    }
    
    sla_hours = sla_map.get(category, 48)  # Default 48 hours
    deadline = (datetime.now() + timedelta(hours=sla_hours)).isoformat()
    
    return sla_hours, deadline