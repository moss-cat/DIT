"""
Card Processor Module

This module handles loading, processing, and management of flashcard data from 
various sources including default decks and user uploads.
"""

import os
import pandas as pd
from pathlib import Path
from io import StringIO  # Add this import for StringIO
from typing import Dict, List, Optional, Union


class CardProcessor:
    """
    Handles loading and processing of flashcard data from CSV files.
    """
    
    def __init__(self):
        """Initialize the card processor with default paths."""
        self.default_decks_path = Path('data/default_decks')
        self.required_columns = ['front', 'back', 'deck']
        self.cards_df = None
        self.available_decks = []
    
    def load_default_deck(self, deck_name: str) -> pd.DataFrame:
        """
        Load a default deck from the default_decks directory.
        
        Args:
            deck_name (str): Name of the deck file without extension (e.g. 'python')
            
        Returns:
            pd.DataFrame: DataFrame containing the cards from the specified deck
            
        Raises:
            FileNotFoundError: If the deck file doesn't exist
            ValueError: If the CSV structure is invalid
        """
        file_path = self.default_decks_path / f"{deck_name}.csv"
        
        if not file_path.exists():
            raise FileNotFoundError(f"Deck file not found: {file_path}")
            
        return self._load_and_validate_csv(file_path)
    
    def load_custom_deck(self, file_content: Union[str, bytes]) -> pd.DataFrame:
        """
        Load a custom deck from uploaded content.
        
        Args:
            file_content (Union[str, bytes]): CSV content as string or bytes
            
        Returns:
            pd.DataFrame: DataFrame containing the cards from the uploaded file
            
        Raises:
            ValueError: If the CSV structure is invalid
        """
        try:
<<<<<<< HEAD
            df = pd.read_csv(
                StringIO(
                    file_content.decode("utf-8")
                    if isinstance(file_content, bytes)
                    else file_content
                )
            )
=======
            df = pd.read_csv(StringIO(file_content.decode('utf-8') 
                                     if isinstance(file_content, bytes) 
                                     else file_content))
>>>>>>> 2c70e2e173fc9249e33d250b2482cc5e5dcd3211
            return self._validate_dataframe(df)
        except Exception as e:
            raise ValueError(f"Failed to process custom deck: {str(e)}")
    
    def get_available_decks(self) -> List[str]:
        """
        Get list of available default decks.
        
        Returns:
            List[str]: List of available deck names without extension
        """
        self.available_decks = [
            f.stem for f in self.default_decks_path.glob("*.csv")
        ]
        return self.available_decks
    
    def get_cards_by_deck(self, deck_name: str) -> pd.DataFrame:
        """
        Filter cards by deck name.
        
        Args:
            deck_name (str): Name of the deck to filter by
            
        Returns:
            pd.DataFrame: DataFrame containing only cards from the specified deck
        """
        if self.cards_df is None:
            raise ValueError("No cards loaded. Load a deck first.")
            
        return self.cards_df[self.cards_df['deck'].str.lower() == deck_name.lower()]
    
    def get_card_count(self, deck_name: Optional[str] = None) -> int:
        """
        Get count of cards, optionally filtered by deck.
        
        Args:
            deck_name (Optional[str]): If provided, count only cards in this deck
            
        Returns:
            int: Number of cards
        """
        if self.cards_df is None:
            return 0
            
        if deck_name:
            return len(self.get_cards_by_deck(deck_name))
        return len(self.cards_df)
    
    def _load_and_validate_csv(self, file_path: Path) -> pd.DataFrame:
        """
        Load and validate a CSV file.
        
        Args:
            file_path (Path): Path to the CSV file
            
        Returns:
            pd.DataFrame: Validated DataFrame
            
        Raises:
            ValueError: If validation fails
        """
        try:
            df = pd.read_csv(file_path)
            return self._validate_dataframe(df)
        except pd.errors.EmptyDataError:
            raise ValueError(f"CSV file is empty: {file_path}")
        except pd.errors.ParserError:
            raise ValueError(f"CSV parsing error: {file_path}")
    
    def _validate_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Validate DataFrame structure for required columns and data types.
        
        Args:
            df (pd.DataFrame): DataFrame to validate
            
        Returns:
            pd.DataFrame: Validated DataFrame
            
        Raises:
            ValueError: If validation fails
        """
        # Check required columns
        missing_cols = set(self.required_columns) - set(df.columns)
        if missing_cols:
            raise ValueError(f"Missing required columns: {', '.join(missing_cols)}")
        
        # Ensure all required columns have data
        for col in self.required_columns:
            if df[col].isna().any():
                raise ValueError(f"Column '{col}' contains empty values")
        
        # Store the loaded cards
        self.cards_df = df
        
        return df