from fastapi import APIRouter, Depends
import httpx
from app.core.config import Settings, get_settings

router = APIRouter()


@router.get("/sports/baseball/teams")
async def get_baseball_teams(
    season: str = "2023",
    settings: Settings = Depends(get_settings)
):
    """
    Get baseball teams from external API
    
    Args:
        season: Season year (defaults to 2023)
    """
    # Construct the API endpoint URL
    url = f"{settings.api_sports_url}/teams"
    
    # Set up query parameters
    params = {
        "league": 1, # 1 = MLB on API Sports
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
            
            # Return the response
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
