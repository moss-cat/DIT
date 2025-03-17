import pytest
import pandas as pd
from datetime import datetime
from unittest.mock import patch, MagicMock

from modules.session_manager import SessionManager

<<<<<<< HEAD
<<<<<<< HEAD

class TestSessionManager:
    """Test suite for the SessionManager class."""

=======
class TestSessionManager:
    """Test suite for the SessionManager class."""
    
>>>>>>> 2c70e2e173fc9249e33d250b2482cc5e5dcd3211
=======
class TestSessionManager:
    """Test suite for the SessionManager class."""
    
>>>>>>> parent of 48f10d7 (updated some modules to improve performance working on fixing button alinement)
    @pytest.fixture
    def mock_session_state(self, monkeypatch):
        """Mock streamlit's session_state."""
        mock_state = {}
<<<<<<< HEAD
<<<<<<< HEAD

=======
        
>>>>>>> 2c70e2e173fc9249e33d250b2482cc5e5dcd3211
=======
        
>>>>>>> parent of 48f10d7 (updated some modules to improve performance working on fixing button alinement)
        class MockSt:
            class session_state(dict):
                def __init__(self):
                    super().__init__()
<<<<<<< HEAD
<<<<<<< HEAD

=======
                
>>>>>>> 2c70e2e173fc9249e33d250b2482cc5e5dcd3211
=======
                
>>>>>>> parent of 48f10d7 (updated some modules to improve performance working on fixing button alinement)
                def __getattr__(self, attr):
                    if attr in self:
                        return self[attr]
                    return None
<<<<<<< HEAD
<<<<<<< HEAD

=======
                
>>>>>>> parent of 48f10d7 (updated some modules to improve performance working on fixing button alinement)
                def __setattr__(self, attr, value):
                    self[attr] = value
            
            session_state = session_state()
        
        monkeypatch.setattr("streamlit.session_state", MockSt.session_state)
        
        return MockSt.session_state
<<<<<<< HEAD

=======
                
                def __setattr__(self, attr, value):
                    self[attr] = value
            
            session_state = session_state()
        
        monkeypatch.setattr("streamlit.session_state", MockSt.session_state)
        
        return MockSt.session_state
    
>>>>>>> 2c70e2e173fc9249e33d250b2482cc5e5dcd3211
=======
    
>>>>>>> parent of 48f10d7 (updated some modules to improve performance working on fixing button alinement)
    @pytest.fixture
    def session_manager(self, mock_session_state):
        """Create a SessionManager instance for testing."""
        return SessionManager()
<<<<<<< HEAD
<<<<<<< HEAD

    @pytest.fixture
    def sample_cards_df(self):
        """Sample DataFrame with flashcards for testing."""
        return pd.DataFrame(
            {
                "front": ["Q1", "Q2", "Q3"],
                "back": ["A1", "A2", "A3"],
                "deck": ["Test", "Test", "Test"],
            }
        )

=======
    
    @pytest.fixture
    def sample_cards_df(self):
        """Sample DataFrame with flashcards for testing."""
=======
    
    @pytest.fixture
    def sample_cards_df(self):
        """Sample DataFrame with flashcards for testing."""
>>>>>>> parent of 48f10d7 (updated some modules to improve performance working on fixing button alinement)
        return pd.DataFrame({
            'front': ['Q1', 'Q2', 'Q3'],
            'back': ['A1', 'A2', 'A3'],
            'deck': ['Test', 'Test', 'Test']
        })
    
<<<<<<< HEAD
>>>>>>> 2c70e2e173fc9249e33d250b2482cc5e5dcd3211
=======
>>>>>>> parent of 48f10d7 (updated some modules to improve performance working on fixing button alinement)
    def test_initialization(self, session_manager, mock_session_state):
        """Test that SessionManager initializes session state correctly."""
        assert mock_session_state.initialized is True
        assert mock_session_state.current_deck is None
        assert mock_session_state.cards == []
        assert mock_session_state.current_card_index == 0
        assert mock_session_state.cards_seen == set()
        assert mock_session_state.cards_correct == set()
        assert mock_session_state.cards_incorrect == set()
        assert mock_session_state.study_start_time is None
        assert mock_session_state.session_history == []
        assert mock_session_state.show_answer is False
        assert mock_session_state.study_mode == "sequential"
        assert mock_session_state.is_studying is False
<<<<<<< HEAD
<<<<<<< HEAD

    def test_start_session_sequential(
        self, session_manager, mock_session_state, sample_cards_df
    ):
        """Test starting a study session in sequential mode."""
        session_manager.start_session("test_deck", sample_cards_df, mode="sequential")

        assert mock_session_state.current_deck == "test_deck"
=======
    
    def test_start_session_sequential(self, session_manager, mock_session_state, sample_cards_df):
        """Test starting a study session in sequential mode."""
        session_manager.start_session('test_deck', sample_cards_df, mode='sequential')
        
        assert mock_session_state.current_deck == 'test_deck'
>>>>>>> 2c70e2e173fc9249e33d250b2482cc5e5dcd3211
=======
    
    def test_start_session_sequential(self, session_manager, mock_session_state, sample_cards_df):
        """Test starting a study session in sequential mode."""
        session_manager.start_session('test_deck', sample_cards_df, mode='sequential')
        
        assert mock_session_state.current_deck == 'test_deck'
>>>>>>> parent of 48f10d7 (updated some modules to improve performance working on fixing button alinement)
        assert len(mock_session_state.cards) == 3
        assert mock_session_state.current_card_index == 0
        assert mock_session_state.cards_seen == set()
        assert mock_session_state.cards_correct == set()
        assert mock_session_state.cards_incorrect == set()
        assert isinstance(mock_session_state.study_start_time, datetime)
        assert mock_session_state.show_answer is False
<<<<<<< HEAD
<<<<<<< HEAD
        assert mock_session_state.study_mode == "sequential"
=======
        assert mock_session_state.study_mode == 'sequential'
>>>>>>> parent of 48f10d7 (updated some modules to improve performance working on fixing button alinement)
        assert mock_session_state.is_studying is True
        
        # Verify card order is preserved in sequential mode
        assert mock_session_state.cards[0]['front'] == 'Q1'
        assert mock_session_state.cards[1]['front'] == 'Q2'
        assert mock_session_state.cards[2]['front'] == 'Q3'
    
    def test_start_session_random(self, session_manager, mock_session_state, sample_cards_df):
        """Test starting a study session in random mode."""
        # Mock random.shuffle to track if it was called
        with patch('random.shuffle') as mock_shuffle:
            session_manager.start_session('test_deck', sample_cards_df, mode='random')
            
            assert mock_session_state.study_mode == 'random'
            assert mock_session_state.is_studying is True
            mock_shuffle.assert_called_once()
    
    def test_end_session(self, session_manager, mock_session_state, sample_cards_df):
        """Test ending a study session."""
        # Start a session first
        session_manager.start_session('test_deck', sample_cards_df)
        
        # Add some test data
        mock_session_state.cards_seen = {'Q1:A1', 'Q2:A2'}
        mock_session_state.cards_correct = {'Q1:A1'}
        mock_session_state.cards_incorrect = {'Q2:A2'}
        
        # End the session
        stats = session_manager.end_session()
        
        # Verify stats
        assert stats['deck'] == 'test_deck'
        assert stats['total_cards'] == 3
        assert stats['cards_seen'] == 2
        assert stats['cards_correct'] == 1
        assert stats['cards_incorrect'] == 1
        assert stats['accuracy'] == 50.0
        assert isinstance(stats['duration_seconds'], float)
        
        # Verify session state
<<<<<<< HEAD
        assert mock_session_state.is_studying is False
=======
        assert mock_session_state.study_mode == 'sequential'
        assert mock_session_state.is_studying is True
        
        # Verify card order is preserved in sequential mode
        assert mock_session_state.cards[0]['front'] == 'Q1'
        assert mock_session_state.cards[1]['front'] == 'Q2'
        assert mock_session_state.cards[2]['front'] == 'Q3'
    
    def test_start_session_random(self, session_manager, mock_session_state, sample_cards_df):
        """Test starting a study session in random mode."""
        # Mock random.shuffle to track if it was called
        with patch('random.shuffle') as mock_shuffle:
            session_manager.start_session('test_deck', sample_cards_df, mode='random')
            
            assert mock_session_state.study_mode == 'random'
            assert mock_session_state.is_studying is True
            mock_shuffle.assert_called_once()
    
    def test_end_session(self, session_manager, mock_session_state, sample_cards_df):
        """Test ending a study session."""
        # Start a session first
        session_manager.start_session('test_deck', sample_cards_df)
        
        # Add some test data
        mock_session_state.cards_seen = {'Q1:A1', 'Q2:A2'}
        mock_session_state.cards_correct = {'Q1:A1'}
        mock_session_state.cards_incorrect = {'Q2:A2'}
        
        # End the session
        stats = session_manager.end_session()
        
        # Verify stats
        assert stats['deck'] == 'test_deck'
        assert stats['total_cards'] == 3
        assert stats['cards_seen'] == 2
        assert stats['cards_correct'] == 1
        assert stats['cards_incorrect'] == 1
        assert stats['accuracy'] == 50.0
        assert isinstance(stats['duration_seconds'], float)
        
        # Verify session state
        assert mock_session_state.is_studying is False
>>>>>>> 2c70e2e173fc9249e33d250b2482cc5e5dcd3211
=======
        assert mock_session_state.is_studying is False
>>>>>>> parent of 48f10d7 (updated some modules to improve performance working on fixing button alinement)
