"""
Session Manager Module

This module handles user session management, tracking study progress,
and managing the state of the flashcard application.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional, Any, Union


class SessionManager:
    """
    Manages user session state and tracks study progress.
    """
    
    def __init__(self):
        """Initialize the session manager with default session state."""
        # Initialize session state if doesn't exist
        if 'initialized' not in st.session_state:
            self._initialize_session_state()
    
    def _initialize_session_state(self) -> None:
        """Initialize the session state variables."""
        st.session_state.initialized = True
        st.session_state.current_deck = None
        st.session_state.cards = []
        st.session_state.current_card_index = 0
        st.session_state.cards_seen = set()
        st.session_state.cards_correct = set()
        st.session_state.cards_incorrect = set()
        st.session_state.study_start_time = None
        st.session_state.session_history = []
        st.session_state.show_answer = False
        st.session_state.study_mode = "sequential"  # or "random"
        st.session_state.is_studying = False
    
    def start_session(self, deck_name: str, cards_df: pd.DataFrame, mode: str = "sequential") -> None:
        """
        Start a new study session.
        
        Args:
            deck_name (str): Name of the deck being studied
            cards_df (pd.DataFrame): DataFrame containing the cards to study
            mode (str): Study mode - "sequential" or "random"
        """
        st.session_state.current_deck = deck_name
        st.session_state.cards = cards_df.to_dict('records')
        st.session_state.current_card_index = 0
        st.session_state.cards_seen = set()
        st.session_state.cards_correct = set()
        st.session_state.cards_incorrect = set()
        st.session_state.study_start_time = datetime.now()
        st.session_state.show_answer = False
        st.session_state.study_mode = mode
        st.session_state.is_studying = True
        
        # Shuffle cards if in random mode
        if mode == "random":
            import random
            random.shuffle(st.session_state.cards)
    
    def end_session(self) -> Dict[str, Any]:
        """
        End the current study session and record statistics.
        
        Returns:
            Dict[str, Any]: Session statistics
        """
        if not st.session_state.is_studying:
            return {}
            
        end_time = datetime.now()
        
        # Calculate session stats
        stats = {
            "deck": st.session_state.current_deck,
            "total_cards": len(st.session_state.cards),
            "cards_seen": len(st.session_state.cards_seen),
            "cards_correct": len(st.session_state.cards_correct),
            "cards_incorrect": len(st.session_state.cards_incorrect),
            "accuracy": self.get_accuracy(),
            "start_time": st.session_state.study_start_time,
            "end_time": end_time,
            "duration_seconds": (end_time - st.session_state.study_start_time).total_seconds()
        }
        
        # Save session history
        st.session_state.session_history.append(stats)
        st.session_state.is_studying = False
        
        return stats
    
    def next_card(self) -> Dict[str, Any]:
        """
        Move to the next card in the deck.
        
        Returns:
            Dict[str, Any]: The next card or None if at the end
        """
        if not st.session_state.is_studying or not st.session_state.cards:
            return None
            
        if st.session_state.current_card_index < len(st.session_state.cards) - 1:
            st.session_state.current_card_index += 1
            st.session_state.show_answer = False
            return self.get_current_card()
        else:
            return None  # End of cards
    
    def prev_card(self) -> Dict[str, Any]:
        """
        Move to the previous card in the deck.
        
        Returns:
            Dict[str, Any]: The previous card or None if at the beginning
        """
        if not st.session_state.is_studying or not st.session_state.cards:
            return None
            
        if st.session_state.current_card_index > 0:
            st.session_state.current_card_index -= 1
            st.session_state.show_answer = False
            return self.get_current_card()
        else:
            return None  # Beginning of cards
    
    def get_current_card(self) -> Optional[Dict[str, Any]]:
        """
        Get the current card being studied.
        
        Returns:
            Optional[Dict[str, Any]]: Current card or None if not studying
        """
        if not st.session_state.is_studying or not st.session_state.cards:
            return None
            
        if 0 <= st.session_state.current_card_index < len(st.session_state.cards):
            card = st.session_state.cards[st.session_state.current_card_index]
            card_id = f"{card['front']}:{card['back']}"
            st.session_state.cards_seen.add(card_id)
            return card
        return None
    
    def mark_card(self, correct: bool) -> None:
        """
        Mark the current card as correct or incorrect.
        
        Args:
            correct (bool): Whether the card was answered correctly
        """
        card = self.get_current_card()
        if not card:
            return
            
        card_id = f"{card['front']}:{card['back']}"
        
        if correct:
            st.session_state.cards_correct.add(card_id)
            if card_id in st.session_state.cards_incorrect:
                st.session_state.cards_incorrect.remove(card_id)
        else:
            st.session_state.cards_incorrect.add(card_id)
            if card_id in st.session_state.cards_correct:
                st.session_state.cards_correct.remove(card_id)
    
    def toggle_card_face(self) -> bool:
        """
        Toggle between showing question and answer.
        
        Returns:
            bool: New state of show_answer
        """
        st.session_state.show_answer = not st.session_state.show_answer
        return st.session_state.show_answer
    
    def is_showing_answer(self) -> bool:
        """
        Check if currently showing answer side of card.
        
        Returns:
            bool: True if showing answer, False if showing question
        """
        return st.session_state.show_answer
    
    def get_progress(self) -> Dict[str, Union[int, float]]:
        """
        Get the current session progress statistics.
        
        Returns:
            Dict[str, Union[int, float]]: Dictionary with progress statistics
        """
        if not st.session_state.is_studying:
            return {"percent": 0, "seen": 0, "total": 0, "correct": 0, "incorrect": 0}
            
        total = len(st.session_state.cards)
        seen = len(st.session_state.cards_seen)
        correct = len(st.session_state.cards_correct)
        incorrect = len(st.session_state.cards_incorrect)
        
        return {
            "percent": (seen / total * 100) if total > 0 else 0,
            "seen": seen,
            "total": total,
            "correct": correct,
            "incorrect": incorrect,
            "current_index": st.session_state.current_card_index + 1 if total > 0 else 0
        }
    
    def get_accuracy(self) -> float:
        """
        Calculate the current accuracy rate.
        
        Returns:
            float: Percentage of correct answers (0-100)
        """
        correct = len(st.session_state.cards_correct)
        total_answered = correct + len(st.session_state.cards_incorrect)
        
        return (correct / total_answered * 100) if total_answered > 0 else 0
    
    def get_session_history(self) -> List[Dict[str, Any]]:
        """
        Get the history of completed study sessions.
        
        Returns:
            List[Dict[str, Any]]: List of session statistics
        """
        return st.session_state.session_history
    
    def reset_progress(self) -> None:
        """Reset the current session progress."""
        st.session_state.cards_seen = set()
        st.session_state.cards_correct = set()
        st.session_state.cards_incorrect = set()
        st.session_state.current_card_index = 0
        st.session_state.show_answer = False
    
    def clear_session_data(self) -> None:
        """Clear all session data."""
        self._initialize_session_state()