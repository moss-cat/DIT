import pytest
import pandas as pd
from datetime import datetime
from unittest.mock import patch, MagicMock

from modules.session_manager import SessionManager


class TestSessionDataPersistence:
    """Test suite for session data persistence issues in SessionManager."""

    @pytest.fixture
    def mock_session_state(self, monkeypatch):
        """Mock streamlit's session_state."""

        class MockSt:
            class session_state(dict):
                def __init__(self):
                    super().__init__()

                def __getattr__(self, attr):
                    if attr in self:
                        return self[attr]
                    return None

                def __setattr__(self, attr, value):
                    self[attr] = value

            session_state = session_state()

        monkeypatch.setattr("streamlit.session_state", MockSt.session_state)
        return MockSt.session_state

    @pytest.fixture
    def session_manager(self, mock_session_state):
        """Create a SessionManager instance for testing."""
        return SessionManager()

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

    def test_session_state_persistence_during_interaction(
        self, session_manager, mock_session_state, sample_cards_df
    ):
        """Test that session data persists during normal user interaction flow."""
        # Start a session
        session_manager.start_session("test_deck", sample_cards_df)

        # Record initial state
        initial_card_index = mock_session_state.current_card_index

        # Simulate answering the first card correctly
        card_id = f"{mock_session_state.cards[0]['front']}:{mock_session_state.cards[0]['back']}"
        session_manager.mark_card(correct=True)
        session_manager.next_card()  # Add this line to advance to next card

        # Verify card was marked correctly
        assert card_id in mock_session_state.cards_correct
        assert card_id in mock_session_state.cards_seen
        assert card_id not in mock_session_state.cards_incorrect

        # Check that current_card_index advanced
        assert mock_session_state.current_card_index == initial_card_index + 1

        # Verify the state persisted after showing answer for next card
        session_manager.toggle_card_face()
        assert card_id in mock_session_state.cards_correct
        assert mock_session_state.current_card_index == initial_card_index + 1

        # Verify state persists after marking next card incorrect
        next_card_id = f"{mock_session_state.cards[1]['front']}:{mock_session_state.cards[1]['back']}"
        session_manager.mark_card(correct=False)
        session_manager.next_card()  # Add this line to advance to next card

        assert card_id in mock_session_state.cards_correct
        assert next_card_id in mock_session_state.cards_incorrect
        assert mock_session_state.current_card_index == initial_card_index + 2

    def test_session_history_persistence(
        self, session_manager, mock_session_state, sample_cards_df
    ):
        """Test that completed session data is saved to session history."""
        # Start and complete a session
        session_manager.start_session("test_deck", sample_cards_df)

        # Mark some cards
        card1_id = f"{mock_session_state.cards[0]['front']}:{mock_session_state.cards[0]['back']}"
        card2_id = f"{mock_session_state.cards[1]['front']}:{mock_session_state.cards[1]['back']}"
        session_manager.mark_card(correct=True)
        session_manager.next_card()  # Add this line to advance to next card
        session_manager.mark_card(correct=False)
        session_manager.next_card()  # Add this line to advance to next card

        # End the session
        stats = session_manager.end_session()

        # Verify session was added to history
        assert len(mock_session_state.session_history) == 1
        assert mock_session_state.session_history[0] == stats

        # Start another session
        session_manager.start_session("test_deck", sample_cards_df)

        # Verify history persists
        assert len(mock_session_state.session_history) == 1

        # End the new session without interaction
        session_manager.end_session()

        # Verify history has both sessions
        assert len(mock_session_state.session_history) == 2

    def test_reset_vs_clear(self, session_manager, mock_session_state, sample_cards_df):
        """Test the difference between reset_progress and clear_session_data."""
        # Start session
        session_manager.start_session("test_deck", sample_cards_df)

        # Add some data
        card_id = f"{mock_session_state.cards[0]['front']}:{mock_session_state.cards[0]['back']}"
        session_manager.mark_card(correct=True)
        session_manager.next_card()  # Add this line to advance to next card

        # End session
        session_manager.end_session()
        assert len(mock_session_state.session_history) == 1

        # Reset progress
        session_manager.reset_progress()

        # Verify reset only cleared progress but kept history
        assert len(mock_session_state.cards_seen) == 0
        assert len(mock_session_state.cards_correct) == 0
        assert len(mock_session_state.cards_incorrect) == 0
        assert len(mock_session_state.session_history) == 1

        # Clear all data
        session_manager.clear_session_data()

        # Verify everything was reset
        assert len(mock_session_state.session_history) == 0
        assert mock_session_state.current_deck is None
