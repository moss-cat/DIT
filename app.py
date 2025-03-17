"""
FlashCard Memory Tool

A Streamlit application for flashcard-based learning and memory enhancement.
Main application entry point.
"""

import streamlit as st
import pandas as pd
import os
from pathlib import Path

# Import local modules
from modules.card_processor import CardProcessor
from modules.session_manager import SessionManager
from modules.ui_components import (
    render_app_header,
    render_card,
    render_card_controls,
    render_deck_selector,
    render_end_session_button,
    render_progress_bar,
    render_statistics,
    render_study_options,
    render_upload_form
)

# Configure page settings
st.set_page_config(
    page_title="FlashCard Memory Tool",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load custom CSS
def load_css():
    css_file = Path("assets/styles.css")
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize application
def initialize_app():
    # Initialize session manager
    if 'session_manager' not in st.session_state:
        st.session_state.session_manager = SessionManager()
    
    # Initialize card processor
    if 'card_processor' not in st.session_state:
        st.session_state.card_processor = CardProcessor()
    
    # Check for default decks
    if 'available_decks' not in st.session_state:
        st.session_state.available_decks = st.session_state.card_processor.get_available_decks()

# Callback functions
def start_studying(deck_name):
    try:
        cards_df = st.session_state.card_processor.load_default_deck(deck_name)
        study_mode = st.session_state.get('study_mode', 'sequential')
        st.session_state.session_manager.start_session(deck_name, cards_df, mode=study_mode)
    except Exception as e:
        st.error(f"Error loading deck: {str(e)}")

def handle_custom_deck_upload(file_content):
    try:
        cards_df = st.session_state.card_processor.load_custom_deck(file_content)
        custom_deck_name = "custom_deck"
        study_mode = st.session_state.get('study_mode', 'sequential')
        st.session_state.session_manager.start_session(custom_deck_name, cards_df, mode=study_mode)
    except Exception as e:
        st.error(f"Error loading custom deck: {str(e)}")

def handle_flip_card():
    st.session_state.session_manager.toggle_card_face()

def handle_next_card():
    st.session_state.session_manager.next_card()

def handle_prev_card():
    st.session_state.session_manager.prev_card()

def handle_mark_correct():
    st.session_state.session_manager.mark_card(correct=True)
    handle_next_card()

def handle_mark_incorrect():
    st.session_state.session_manager.mark_card(correct=False)
    handle_next_card()

def handle_end_session():
    stats = st.session_state.session_manager.end_session()
    st.session_state.last_session_stats = stats

def handle_mode_change(mode):
    st.session_state.study_mode = mode

# Main application function
def main():
    # Load CSS and initialize app
    load_css()
    initialize_app()
    
    # Render app header
    render_app_header()
    
    # Get current state
    session_manager = st.session_state.session_manager
    is_studying = getattr(st.session_state, 'is_studying', False)
    
    # Main application logic
    if not is_studying:
        # Display deck selector when not studying
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Deck selection
            render_deck_selector(
                st.session_state.available_decks, 
                on_select=start_studying
            )
        
        with col2:
            # Custom deck upload
            render_upload_form(on_upload=handle_custom_deck_upload)
        
        # Display last session statistics if available
        if hasattr(st.session_state, 'last_session_stats') and st.session_state.last_session_stats:
            render_statistics(st.session_state.last_session_stats)
    
    else:
        # Display study session interface
        st.subheader(f"Studying: {st.session_state.current_deck.replace('_', ' ').title()}")
        
        # Study options
        current_mode = getattr(st.session_state, 'study_mode', 'sequential')
        render_study_options(handle_mode_change, current_mode)
        
        # Progress tracking
        progress = session_manager.get_progress()
        render_progress_bar(progress)
        
        # Card display
        current_card = session_manager.get_current_card()
        show_answer = session_manager.is_showing_answer()
        
        if current_card:
            render_card(current_card, show_answer)
            render_card_controls(
                on_flip=handle_flip_card,
                on_next=handle_next_card,
                on_prev=handle_prev_card,
                on_correct=handle_mark_correct,
                on_incorrect=handle_mark_incorrect,
                show_answer=show_answer
            )
        else:
            st.success("You've reached the end of this deck!")
            stats = session_manager.get_progress()
            st.write(f"You've studied {stats['seen']} cards with an accuracy of {session_manager.get_accuracy():.1f}%")
        
        # End session button
        st.markdown("---")
        render_end_session_button(on_end=handle_end_session)

# Run the application
if __name__ == "__main__":
    main()