from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from app.models.team import Team


class TeamService:
    """Service for managing team data"""
    
    # IDs to filter out (American League and National League)
    EXCLUDED_TEAM_IDS = [1, 23]  # 1 = American League, 23 = National League on API Sports
    
    def __init__(self, db: Session):
        self.db = db
    
    def upsert_teams(self, teams_data: List[Dict[str, Any]]) -> List[Team]:
        """
        Insert or update teams from API response.
        Filters out American League and National League.
        
        Args:
            teams_data: List of team dictionaries from API Sports
            
        Returns:
            List of Team objects that were upserted
        """        
        upserted_team_ids = []
        
        for team_data in teams_data:
            # Extract team info from API response
            api_sports_id = team_data.get("id")
            name = team_data.get("name")
            logo = team_data.get("logo")
            
            # Skip if missing required data
            if not all([api_sports_id, name, logo]):
                continue
            
            # Filter out American League and National League
            if api_sports_id in self.EXCLUDED_TEAM_IDS:
                print(f"⏭️  Skipping {name} (ID: {api_sports_id})")
                continue
            
            # Upsert (insert or update if exists)
            stmt = insert(Team).values(
                api_sports_id=api_sports_id,
                name=name,
                logo=logo
            )
            
            # On conflict (duplicate api_sports_id), update the record
            stmt = stmt.on_conflict_do_update(
                index_elements=["api_sports_id"],
                set_={
                    "name": name,
                    "logo": logo
                }
            )
            
            self.db.execute(stmt)
            upserted_team_ids.append(api_sports_id)
            print(f"💾 Saved team: {name} (API Sports ID: {api_sports_id})")
        
        # Commit all changes
        self.db.commit()
        
        # Fetch and return all upserted teams
        upserted_teams = self.db.query(Team).filter(
            Team.api_sports_id.in_(upserted_team_ids)
        ).all()
        
        return upserted_teams
    
    def get_all_teams(self) -> List[Team]:
        """Get all teams from database"""
        return self.db.query(Team).all()
    
    def get_team_by_api_sports_id(self, api_sports_id: int) -> Team | None:
        """Get a specific team by its API Sports ID"""
        return self.db.query(Team).filter(Team.api_sports_id == api_sports_id).first()

