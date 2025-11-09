import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.models.base import Base
from app.models.team import Team
from app.services.team_service import TeamService


@pytest.fixture(scope="function")
def db_session():
    """Create a test database session"""
    # Use in-memory SQLite for testing
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    
    yield session
    
    session.close()


@pytest.fixture
def team_service(db_session: Session):
    """Create a TeamService instance with test database"""
    return TeamService(db_session)


@pytest.fixture
def sample_teams_data():
    """Sample team data from API Sports"""
    return [
        {
            "id": 16,
            "name": "New York Mets",
            "logo": "https://example.com/mets.png"
        },
        {
            "id": 17,
            "name": "Colorado Rockies",
            "logo": "https://example.com/rockies.png"
        },
        {
            "id": 25,
            "name": "Los Angeles Dodgers",
            "logo": "https://example.com/dodgers.png"
        },
        {
            "id": 1,  # American League - should be filtered
            "name": "American League",
            "logo": "https://example.com/al.png"
        },
        {
            "id": 23,  # National League - should be filtered
            "name": "National League",
            "logo": "https://example.com/nl.png"
        }
    ]


class TestTeamService:
    """Tests for TeamService"""
    
    def test_upsert_teams_inserts_new_teams(self, team_service: TeamService, sample_teams_data):
        """Test that upsert_teams successfully inserts new teams"""
        # Arrange
        teams_data = sample_teams_data[:3]  # Only the real teams
        
        # Act
        result = team_service.upsert_teams(teams_data)
        
        # Assert
        assert len(result) == 3
        assert result[0].name == "New York Mets"
        assert result[0].api_sports_id == 16
        assert result[1].name == "Colorado Rockies"
        assert result[2].name == "Los Angeles Dodgers"
    
    def test_upsert_teams_filters_excluded_teams(self, team_service: TeamService, sample_teams_data):
        """Test that American League and National League are filtered out"""
        # Act
        result = team_service.upsert_teams(sample_teams_data)
        
        # Assert
        assert len(result) == 3  # Only 3 teams, not 5
        team_ids = [team.api_sports_id for team in result]
        assert 1 not in team_ids  # American League filtered
        assert 23 not in team_ids  # National League filtered
    
    def test_upsert_teams_updates_existing_teams(self, team_service: TeamService, db_session: Session):
        """Test that upsert updates existing teams when api_sports_id matches"""
        # Arrange - Insert initial team
        initial_data = [
            {
                "id": 16,
                "name": "New York Mets",
                "logo": "https://example.com/old-logo.png"
            }
        ]
        team_service.upsert_teams(initial_data)
        
        # Act - Update with new data
        updated_data = [
            {
                "id": 16,
                "name": "New York Mets Updated",
                "logo": "https://example.com/new-logo.png"
            }
        ]
        result = team_service.upsert_teams(updated_data)
        
        # Assert
        assert len(result) == 1
        assert result[0].name == "New York Mets Updated"
        assert result[0].logo == "https://example.com/new-logo.png"
        
        # Verify only one record exists (not duplicated)
        all_teams = db_session.query(Team).all()
        assert len(all_teams) == 1
    
    def test_upsert_teams_skips_incomplete_data(self, team_service: TeamService):
        """Test that teams with missing required fields are skipped"""
        # Arrange
        incomplete_data = [
            {
                "id": 16,
                "name": "New York Mets",
                # Missing logo
            },
            {
                "id": 17,
                # Missing name
                "logo": "https://example.com/rockies.png"
            },
            {
                # Missing id
                "name": "Dodgers",
                "logo": "https://example.com/dodgers.png"
            },
            {
                "id": 25,
                "name": "Valid Team",
                "logo": "https://example.com/valid.png"
            }
        ]
        
        # Act
        result = team_service.upsert_teams(incomplete_data)
        
        # Assert - Only the complete team should be inserted
        assert len(result) == 1
        assert result[0].name == "Valid Team"
    
    def test_get_all_teams(self, team_service: TeamService, sample_teams_data):
        """Test retrieving all teams from database"""
        # Arrange
        team_service.upsert_teams(sample_teams_data[:3])
        
        # Act
        result = team_service.get_all_teams()
        
        # Assert
        assert len(result) == 3
        assert isinstance(result[0], Team)
    
    def test_get_team_by_api_sports_id_found(self, team_service: TeamService, sample_teams_data):
        """Test retrieving a specific team by API Sports ID"""
        # Arrange
        team_service.upsert_teams(sample_teams_data[:3])
        
        # Act
        result = team_service.get_team_by_api_sports_id(16)
        
        # Assert
        assert result is not None
        assert result.name == "New York Mets"
        assert result.api_sports_id == 16
    
    def test_get_team_by_api_sports_id_not_found(self, team_service: TeamService):
        """Test retrieving a team that doesn't exist returns None"""
        # Act
        result = team_service.get_team_by_api_sports_id(9999)
        
        # Assert
        assert result is None
    
    def test_upsert_teams_returns_empty_list_when_no_valid_teams(self, team_service: TeamService):
        """Test that upsert returns empty list when all teams are filtered or invalid"""
        # Arrange - Only excluded teams
        excluded_only = [
            {
                "id": 1,
                "name": "American League",
                "logo": "https://example.com/al.png"
            },
            {
                "id": 23,
                "name": "National League",
                "logo": "https://example.com/nl.png"
            }
        ]
        
        # Act
        result = team_service.upsert_teams(excluded_only)
        
        # Assert
        assert len(result) == 0
    
    def test_upsert_teams_handles_empty_list(self, team_service: TeamService):
        """Test that upsert handles empty input gracefully"""
        # Act
        result = team_service.upsert_teams([])
        
        # Assert
        assert len(result) == 0

