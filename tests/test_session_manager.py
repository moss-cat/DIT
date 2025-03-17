import pytest
import pandas as pd
from datetime import datetime
from unittest.mock import patch, MagicMock

from modules.session_manager import SessionManager

<<<<<<< HEAD

class TestSessionManager:
    """Test suite for the SessionManager class."""

=======
class TestSessionManager:
    """Test suite for the SessionManager class."""
    
>>>>>>> 2c70e2e173fc9249e33d250b2482cc5e5dcd3211
    @pytest.fixture
    def mock_session_state(self, monkeypatch):
        """Mock streamlit's session_state."""
        mock_state = {}
<<<<<<< HEAD

=======
        
>>>>>>> 2c70e2e173fc9249e33d250b2482cc5e5dcd3211
        class MockSt:
            class session_state(dict):
                def __init__(self):
                    super().__init__()
<<<<<<< HEAD

=======
                
>>>>>>> 2c70e2e173fc9249e33d250b2482cc5e5dcd3211
                def __getattr__(self, attr):
                    if attr in self:
                        return self[attr]
                    return None
<<<<<<< HEAD

                def __setattr__(self, attr, value):
                    self[attr] = value

            session_state = session_state()

        monkeypatch.setattr("streamlit.session_state", MockSt.session_state)

        return MockSt.session_state

=======
                
                def __setattr__(self, attr, value):
                    self[attr] = value
            
            session_state = session_state()
        
        monkeypatch.setattr("streamlit.session_state", MockSt.session_state)
        
        return MockSt.session_state
    
>>>>>>> 2c70e2e173fc9249e33d250b2482cc5e5dcd3211
    @pytest.fixture
    def session_manager(self, mock_session_state):
        """Create a SessionManager instance for testing."""
        return SessionManager()
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
        return pd.DataFrame({
            'front': ['Q1', 'Q2', 'Q3'],
            'back': ['A1', 'A2', 'A3'],
            'deck': ['Test', 'Test', 'Test']
        })
    
>>>>>>> 2c70e2e173fc9249e33d250b2482cc5e5dcd3211
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
        assert len(mock_session_state.cards) == 3
        assert mock_session_state.current_card_index == 0
        assert mock_session_state.cards_seen == set()
        assert mock_session_state.cards_correct == set()
        assert mock_session_state.cards_incorrect == set()
        assert isinstance(mock_session_state.study_start_time, datetime)
        assert mock_session_state.show_answer is False
<<<<<<< HEAD
        assert mock_session_state.study_mode == "sequential"
        assert mock_session_state.is_studying is True

        # Verify card order is preserved in sequential mode
        assert mock_session_state.cards[0]["front"] == "Q1"
        assert mock_session_state.cards[1]["front"] == "Q2"
        assert mock_session_state.cards[2]["front"] == "Q3"

    def test_start_session_random(
        self, session_manager, mock_session_state, sample_cards_df
    ):
        """Test starting a study session in random mode."""
        # Mock random.shuffle to track if it was called
        with patch("random.shuffle") as mock_shuffle:
            session_manager.start_session("test_deck", sample_cards_df, mode="random")

            assert mock_session_state.study_mode == "random"
            assert mock_session_state.is_studying is True
            mock_shuffle.assert_called_once()

    def test_end_session(self, session_manager, mock_session_state, sample_cards_df):
        """Test ending a study session."""
        # Start a session first
        session_manager.start_session("test_deck", sample_cards_df)

        # Add some test data
        mock_session_state.cards_seen = {"Q1:A1", "Q2:A2"}
        mock_session_state.cards_correct = {"Q1:A1"}
        mock_session_state.cards_incorrect = {"Q2:A2"}

        # End the session
        stats = session_manager.end_session()

        # Verify stats
        assert stats["deck"] == "test_deck"
        assert stats["total_cards"] == 3
        assert stats["cards_seen"] == 2
        assert stats["cards_correct"] == 1
        assert stats["cards_incorrect"] == 1
        assert stats["accuracy"] == 50.0
        assert isinstance(stats["duration_seconds"], float)

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
        
>>>>>>> 2c70e2e173fc9249e33d250b2482cc5e5dcd3211
        # Verify session state
        assert mock_session_state.is_studying is False
        assert len(mock_session_state.session_history) == 1
        assert mock_session_state.session_history[0] is stats
<<<<<<< HEAD

=======
    
>>>>>>> 2c70e2e173fc9249e33d250b2482cc5e5dcd3211
    def test_end_session_not_studying(self, session_manager, mock_session_state):
        """Test ending a session when not studying."""
        mock_session_state.is_studying = False
        stats = session_manager.end_session()
<<<<<<< HEAD

        assert stats == {}

    def test_navigation_next_card(
        self, session_manager, mock_session_state, sample_cards_df
    ):
        """Test navigating to the next card."""
        # Start a session
        session_manager.start_session("test_deck", sample_cards_df)

        # Initial state
        assert mock_session_state.current_card_index == 0

        # Move to next card
        next_card = session_manager.next_card()

        assert mock_session_state.current_card_index == 1
        assert mock_session_state.show_answer is False
        assert next_card["front"] == "Q2"
        assert next_card["back"] == "A2"

        # Move to last card
        next_card = session_manager.next_card()

        assert mock_session_state.current_card_index == 2
        assert next_card["front"] == "Q3"

        # Try to move beyond last card
        beyond_last = session_manager.next_card()

        assert beyond_last is None
        assert mock_session_state.current_card_index == 2  # Index doesn't change

    def test_navigation_prev_card(
        self, session_manager, mock_session_state, sample_cards_df
    ):
        """Test navigating to the previous card."""
        # Start a session
        session_manager.start_session("test_deck", sample_cards_df)

        # Move to card 2
        session_manager.next_card()
        assert mock_session_state.current_card_index == 1

        # Move back to card 1
        prev_card = session_manager.prev_card()

        assert mock_session_state.current_card_index == 0
        assert mock_session_state.show_answer is False
        assert prev_card["front"] == "Q1"

        # Try to move before first card
        before_first = session_manager.prev_card()

        assert before_first is None
        assert mock_session_state.current_card_index == 0  # Index doesn't change

    def test_mark_card(self, session_manager, mock_session_state, sample_cards_df):
        """Test marking cards as correct or incorrect."""
        # Start a session
        session_manager.start_session("test_deck", sample_cards_df)

        # Get the first card and its ID
        card = session_manager.get_current_card()
        card_id = f"{card['front']}:{card['back']}"

        # Mark as correct
        session_manager.mark_card(True)

        assert card_id in mock_session_state.cards_correct
        assert card_id not in mock_session_state.cards_incorrect

        # Mark as incorrect
        session_manager.mark_card(False)

        assert card_id in mock_session_state.cards_incorrect
        assert card_id not in mock_session_state.cards_correct

=======
        
        assert stats == {}
    
    def test_navigation_next_card(self, session_manager, mock_session_state, sample_cards_df):
        """Test navigating to the next card."""
        # Start a session
        session_manager.start_session('test_deck', sample_cards_df)
        
        # Initial state
        assert mock_session_state.current_card_index == 0
        
        # Move to next card
        next_card = session_manager.next_card()
        
        assert mock_session_state.current_card_index == 1
        assert mock_session_state.show_answer is False
        assert next_card['front'] == 'Q2'
        assert next_card['back'] == 'A2'
        
        # Move to last card
        next_card = session_manager.next_card()
        
        assert mock_session_state.current_card_index == 2
        assert next_card['front'] == 'Q3'
        
        # Try to move beyond last card
        beyond_last = session_manager.next_card()
        
        assert beyond_last is None
        assert mock_session_state.current_card_index == 2  # Index doesn't change
    
    def test_navigation_prev_card(self, session_manager, mock_session_state, sample_cards_df):
        """Test navigating to the previous card."""
        # Start a session
        session_manager.start_session('test_deck', sample_cards_df)
        
        # Move to card 2
        session_manager.next_card()
        assert mock_session_state.current_card_index == 1
        
        # Move back to card 1
        prev_card = session_manager.prev_card()
        
        assert mock_session_state.current_card_index == 0
        assert mock_session_state.show_answer is False
        assert prev_card['front'] == 'Q1'
        
        # Try to move before first card
        before_first = session_manager.prev_card()
        
        assert before_first is None
        assert mock_session_state.current_card_index == 0  # Index doesn't change
    
    def test_mark_card(self, session_manager, mock_session_state, sample_cards_df):
        """Test marking cards as correct or incorrect."""
        # Start a session
        session_manager.start_session('test_deck', sample_cards_df)
        
        # Get the first card and its ID
        card = session_manager.get_current_card()
        card_id = f"{card['front']}:{card['back']}"
        
        # Mark as correct
        session_manager.mark_card(True)
        
        assert card_id in mock_session_state.cards_correct
        assert card_id not in mock_session_state.cards_incorrect
        
        # Mark as incorrect
        session_manager.mark_card(False)
        
        assert card_id in mock_session_state.cards_incorrect
        assert card_id not in mock_session_state.cards_correct
    
>>>>>>> 2c70e2e173fc9249e33d250b2482cc5e5dcd3211
    def test_toggle_card_face(self, session_manager, mock_session_state):
        """Test toggling between question and answer."""
        # Initial state
        assert mock_session_state.show_answer is False
<<<<<<< HEAD

        # Toggle to answer
        result = session_manager.toggle_card_face()

        assert result is True
        assert mock_session_state.show_answer is True

        # Toggle back to question
        result = session_manager.toggle_card_face()

        assert result is False
        assert mock_session_state.show_answer is False

    def test_get_progress(self, session_manager, mock_session_state, sample_cards_df):
        """Test getting progress statistics."""
        # Start a session
=======
        
        # Toggle to answer
        result = session_manager.toggle_card_face()
        
        assert result is True
        assert mock_session_state.show_answer is True
        
        # Toggle back to question
        result = session_manager.toggle_card_face()
        
        assert result is False
        assert mock_session_state.show_answer is False
    
    def test_get_progress(self, session_manager, mock_session_state, sample_cards_df):
        """Test getting progress statistics."""
        # Start a session
>>>>>>> 2c70e2e173fc9249e33d250b2482cc5e5dcd3211
