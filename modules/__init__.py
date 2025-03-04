"""
FlashCard Memory Tool - Core Modules Package

This package contains the core modules for the flashcard application:
- card_processor: Handles loading and processing of flashcard data
- session_manager: Manages user session state and progress tracking
- ui_components: Provides Streamlit UI components for the application
"""

from modules.card_processor import CardProcessor
from modules.session_manager import SessionManager
from modules.ui_components import (
    render_card,
    render_deck_selector,
    render_progress_bar,
    render_statistics
)

__all__ = [
    'CardProcessor',
    'SessionManager',
    'render_card',
    'render_deck_selector',
    'render_progress_bar',
    'render_statistics'
]