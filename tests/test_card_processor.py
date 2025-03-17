import os
import pytest
import pandas as pd
from io import StringIO
from pathlib import Path
from unittest.mock import patch, mock_open

from modules.card_processor import CardProcessor


class TestCardProcessor:
    """Test suite for the CardProcessor class."""

    @pytest.fixture
    def processor(self):
        """Create a CardProcessor instance for testing."""
        return CardProcessor()

    @pytest.fixture
    def sample_csv_content(self):
        """Sample valid CSV content for testing."""
        return """front,back,deck
"What is Python?","A programming language","Programming"
"What is a variable?","A named storage location","Programming"
"What is a function?","A reusable block of code","Programming"
"""

    @pytest.fixture
    def sample_dataframe(self, sample_csv_content):
        """Create a sample DataFrame from the CSV content."""
        return pd.read_csv(StringIO(sample_csv_content))

    def test_initialization(self, processor):
        """Test that CardProcessor initializes correctly."""
        assert processor.default_decks_path == Path("data/default_decks")
        assert processor.required_columns == ["front", "back", "deck"]
        assert processor.cards_df is None
        assert processor.available_decks == []

    def test_get_available_decks(self, processor):
        """Test getting available decks."""
        # Mock the glob method to return fake file paths
        with patch("pathlib.Path.glob") as mock_glob:
            mock_glob.return_value = [
                Path("data/default_decks/python.csv"),
                Path("data/default_decks/algorithms.csv"),
                Path("data/default_decks/cs_basics.csv"),
            ]

            decks = processor.get_available_decks()

            assert decks == ["python", "algorithms", "cs_basics"]
            assert processor.available_decks == decks

    def test_load_default_deck_file_not_found(self, processor):
        """Test that loading a non-existent deck raises FileNotFoundError."""
        with patch("pathlib.Path.exists", return_value=False):
            with pytest.raises(FileNotFoundError):
                processor.load_default_deck("nonexistent_deck")

    def test_load_default_deck_success(self, processor, sample_dataframe):
        """Test loading a default deck successfully."""
        with patch("pathlib.Path.exists", return_value=True):
            with patch.object(
                processor, "_load_and_validate_csv", return_value=sample_dataframe
            ) as mock_load:
                df = processor.load_default_deck("python")

                # Verify the correct file path was passed to _load_and_validate_csv
                mock_load.assert_called_once_with(Path("data/default_decks/python.csv"))
                assert df is sample_dataframe

    def test_load_custom_deck_success(
        self, processor, sample_csv_content, sample_dataframe
    ):
        """Test loading a custom deck successfully."""
        with patch.object(
            processor, "_validate_dataframe", return_value=sample_dataframe
        ) as mock_validate:
            df = processor.load_custom_deck(sample_csv_content)

            assert df is sample_dataframe

    def test_load_custom_deck_invalid(self, processor):
        """Test loading an invalid custom deck."""
        invalid_csv = "not,a,valid,csv"

        with pytest.raises(ValueError):
            processor.load_custom_deck(invalid_csv)

    def test_validate_dataframe_missing_columns(self, processor):
        """Test validating a DataFrame with missing required columns."""
        df = pd.DataFrame(
            {
                "front": ["Question 1", "Question 2"],
                "back": ["Answer 1", "Answer 2"],
                # Missing 'deck' column
            }
        )

        with pytest.raises(ValueError, match="Missing required columns: deck"):
            processor._validate_dataframe(df)

    def test_validate_dataframe_empty_values(self, processor):
        """Test validating a DataFrame with empty values."""
        df = pd.DataFrame(
            {
                "front": ["Question 1", "Question 2"],
                "back": ["Answer 1", None],  # None/NaN value
                "deck": ["Deck 1", "Deck 2"],
            }
        )

        with pytest.raises(ValueError, match="Column 'back' contains empty values"):
            processor._validate_dataframe(df)

    def test_validate_dataframe_success(self, processor, sample_dataframe):
        """Test validating a valid DataFrame."""
        result_df = processor._validate_dataframe(sample_dataframe)

        assert result_df is sample_dataframe
        assert processor.cards_df is sample_dataframe

    def test_get_cards_by_deck(self, processor):
        """Test filtering cards by deck name."""
        # Create a test DataFrame with multiple decks
        processor.cards_df = pd.DataFrame(
            {
                "front": ["Q1", "Q2", "Q3", "Q4"],
                "back": ["A1", "A2", "A3", "A4"],
                "deck": ["Python", "Algorithms", "python", "Algorithms"],
            }
        )

        # Test case-insensitive filtering
        python_cards = processor.get_cards_by_deck("python")
        assert len(python_cards) == 2
        assert list(python_cards["front"]) == ["Q1", "Q3"]

        algorithms_cards = processor.get_cards_by_deck("algorithms")
        assert len(algorithms_cards) == 2
        assert list(algorithms_cards["front"]) == ["Q2", "Q4"]

    def test_get_cards_by_deck_no_cards_loaded(self, processor):
        """Test that get_cards_by_deck raises ValueError when no cards are loaded."""
        with pytest.raises(ValueError, match="No cards loaded"):
            processor.get_cards_by_deck("python")

    def test_get_card_count(self, processor):
        """Test counting cards."""
        # Create a test DataFrame
        processor.cards_df = pd.DataFrame(
            {
                "front": ["Q1", "Q2", "Q3", "Q4"],
                "back": ["A1", "A2", "A3", "A4"],
                "deck": ["Python", "Algorithms", "Python", "Algorithms"],
            }
        )

        # Test total count
        assert processor.get_card_count() == 4

        # Test count by deck
        assert processor.get_card_count("Python") == 2
        assert processor.get_card_count("Algorithms") == 2
        assert processor.get_card_count("NonExistent") == 0
