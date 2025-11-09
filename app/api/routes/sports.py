from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import httpx
from app.core.config import Settings, get_settings
from app.core.database import get_db
from app.services.team_service import TeamService

router = APIRouter()


@router.get("/sports/baseball/teams")
async def get_baseball_teams(
    season: str = "2023",
    settings: Settings = Depends(get_settings)
):
    """
    Get baseball teams from external API (read-only).
    
    Args:
        season: Season year (defaults to 2023)
    """
    # Construct the API endpoint URL
    url = f"{settings.api_sports_url}/teams"
    
    # Set up query parameters
    params = {
        "league": 1,  # 1 = MLB on API Sports
        "season": season
    }
    
    # Set up headers with API key
    headers = {
        "x-rapidapi-key": settings.api_sports_key,
        "x-rapidapi-host": settings.api_sports_url,
        "Content-Type": "application/json"
    }
    
    try:
        # Make the external API call
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=params, timeout=10.0)
            response.raise_for_status()  # Raise exception for 4xx/5xx status codes
            
            data = response.json()
            
            # Return the API response as-is
            return {
                "status": "success",
                "data": data
            }
            
    except httpx.HTTPStatusError as e:
        print(f"✗ HTTP Error: {e.response.status_code} - {e.response.text}")
        return {
            "status": "error",
            "message": f"External API returned {e.response.status_code}",
            "details": str(e)
        }
    except httpx.RequestError as e:
        print(f"✗ Request Error: {str(e)}")
        return {
            "status": "error",
            "message": "Failed to connect to external API",
            "details": str(e)
        }
    except Exception as e:
        print(f"✗ Unexpected Error: {str(e)}")
        return {
            "status": "error",
            "message": "Unexpected error occurred",
            "details": str(e)
        }


@router.post("/sports/baseball/teams/sync")
async def sync_baseball_teams(
    season: str = "2023",
    settings: Settings = Depends(get_settings),
    db: Session = Depends(get_db)
):
    """
    Fetch baseball teams from external API and sync to database.
    Filters out American League and National League records.
    
    Args:
        season: Season year (defaults to 2023)
    """
    # Construct the API endpoint URL
    url = f"{settings.api_sports_url}/teams"
    
    # Set up query parameters
    params = {
        "league": 1,  # 1 = MLB on API Sports
        "season": season
    }
    
    # Set up headers with API key
    headers = {
        "x-rapidapi-key": settings.api_sports_key,
        "x-rapidapi-host": settings.api_sports_url,
        "Content-Type": "application/json"
    }
    
    try:
        # Make the external API call
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=params, timeout=10.0)
            response.raise_for_status()  # Raise exception for 4xx/5xx status codes
            
            data = response.json()
            
            # Extract teams from response (adjust based on actual API structure)
            teams_list = data.get("response", [])
            
            # Save teams to database using service
            team_service = TeamService(db)
            upserted_teams = team_service.upsert_teams(teams_list)
            
            print(f"✅ Synced {len(upserted_teams)} teams to database")
            
            # Convert Team models to dictionaries for JSON response
            upserted_teams_data = [
                {
                    "id": team.id,
                    "api_sports_id": team.api_sports_id,
                    "name": team.name,
                    "logo": team.logo
                }
                for team in upserted_teams
            ]
            
            # Return both API data and upserted teams from database
            return {
                "status": "success",
                "teams_synced": len(upserted_teams),
                "api_sports_response": data,
                "upserted_teams": upserted_teams_data
            }
            
    except httpx.HTTPStatusError as e:
        print(f"✗ HTTP Error: {e.response.status_code} - {e.response.text}")
        return {
            "status": "error",
            "message": f"External API returned {e.response.status_code}",
            "details": str(e)
        }
    except httpx.RequestError as e:
        print(f"✗ Request Error: {str(e)}")
        return {
            "status": "error",
            "message": "Failed to connect to external API",
            "details": str(e)
        }
    except Exception as e:
        print(f"✗ Unexpected Error: {str(e)}")
        return {
            "status": "error",
            "message": "Unexpected error occurred",
            "details": str(e)
        }
