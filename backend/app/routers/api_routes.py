from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List
from datetime import datetime, timedelta
import random
import os
from ..database import supabase

router = APIRouter()

# --- Helpers ---
def get_mock_heatmap_points():
    points = []
    # Generate some random points around Delhi
    center_lat, center_lng = 28.6139, 77.2090
    for _ in range(50):
        points.append([
            center_lat + (random.random() - 0.5) * 0.1,
            center_lng + (random.random() - 0.5) * 0.1,
            random.random() # intensity
        ])
    return points

# --- Endpoints ---

@router.get("/dashboard-stats")
def get_dashboard_stats(zone: Optional[str] = None):
    try:
        # Try to fetch real stats if possible
        # For now, return mock data mixed with real DB counts if available
        total_complaints = 0
        resolved_today = 0
        try:
            total_response = supabase.table("complaints").select("id", count="exact").execute()
            total_complaints = total_response.count if total_response.count is not None else 120
            
            # resolved_today query (mocked logic for now as we might not have `resolved_at`)
            resolved_today = int(total_complaints * 0.4) 
        except:
            total_complaints = 124
            resolved_today = 45

        return {
            "total_complaints": total_complaints,
            "resolved": resolved_today,
            "active_agents": 12,
            "avg_resolution_hours": 24.5,
            "complaint_trend": 12, # +12%
            "resolution_trend": 5, # +5%
             "open_complaints": total_complaints - resolved_today,
            "sla_breached": 2,
            "sla_compliance": 98.5
        }
    except Exception as e:
        print(f"Error fetching stats: {e}")
        return {
            "total_complaints": 0, "resolved": 0, "active_agents": 0, "avg_resolution_hours": 0
        }

@router.get("/activity")
def get_activity_feed(limit: int = 5, zone: Optional[str] = None):
    try:
        # Fetch actual complaints
        response = supabase.table("complaints")\
            .select("*")\
            .order("created_at", desc=True)\
            .limit(limit)\
            .execute()
        
        complaints = response.data or []
        
        activities = []
        for c in complaints:
            activities.append({
                "id": c.get("id"),
                "type": "complaint" if c.get("source") != "vapi" else "voice",
                "title": f"New Complaint: {c.get('category', 'General')}",
                "location": c.get("location", "Delhi"),
                "time": c.get("created_at"), # Frontend handles formatting
                "zone": c.get("zone")
            })
            
        # If not enough data, pad with mock data for demo
        if len(activities) < limit:
            activities.append({
                "id": "mock-1",
                "type": "resolved",
                "title": "Pothole fixed in Karol Bagh",
                "location": "Karol Bagh",
                # valid ISO date string
                "time": datetime.now().isoformat(),
                "zone": "Karol Bagh Zone"
            })
            
        return {"activities": activities}
    except Exception as e:
         print(f"Error fetching activity: {e}")
         return {"activities": []}

@router.get("/heatmap")
def get_heatmap(zone: Optional[str] = None):
    return {"points": get_mock_heatmap_points()}

@router.get("/config")
def get_config():
    return {
        "vapi_public_key": os.getenv("VAPI_PUBLIC_KEY", ""),
        "vapi_assistant_id": os.getenv("VAPI_ASSISTANT_ID", "")
    }

@router.get("/complaints")
def get_complaints(limit: int = 50):
    try:
        response = supabase.table("complaints")\
            .select("*")\
            .order("created_at", desc=True)\
            .limit(limit)\
            .execute()
        return {"complaints": response.data or []}
    except Exception as e:
        print(f"Error fetching complaints: {e}")
        return {"complaints": []}