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

# Initialize layout preference before page config
if 'layout_preference' not in st.session_state:
    st.session_state.layout_preference = 'centered'  # Default to centered layout

# Configure page settings
st.set_page_config(
    page_title="FlashCard Memory Tool",
    page_icon="📚",
    layout=st.session_state.layout_preference,  # Use the preference we just set
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

def handle_layout_change(new_layout):
    """Handle layout preference change."""
    if new_layout != st.session_state.layout_preference:
        st.session_state.layout_preference = new_layout
        st.experimental_rerun()

# Main application function
def main():
    # Load CSS and initialize app
    load_css()
    initialize_app()
    
    # Layout toggle in sidebar
    with st.sidebar:
        st.header("Display Settings")
        layout_options = ["Centered", "Wide"]  # Changed order to make centered first
        current_index = 0 if st.session_state.layout_preference == 'centered' else 1
        
        selected_layout = st.radio(
            "Layout Mode",
            options=layout_options,
            index=current_index
        )
        
        # Convert display name to internal value and update if needed
        new_layout_value = selected_layout.lower()
        if new_layout_value != st.session_state.layout_preference:
            handle_layout_change(new_layout_value)
    
    # Render app header
    render_app_header()
    
    # Get current state
    session_manager = st.session_state.session_manager
    is_studying = getattr(st.session_state, 'is_studying', False)
    
    # Main application logic
    if not is_studying:
        # Display deck selector when not studying
        with st.container():
            st.markdown("""
            <style>
            /* Force consistent container widths for start page */
            .start-page-container [data-testid="stHorizontalBlock"] {
                align-items: flex-start;
            }
            </style>
            <div class="start-page-container"></div>
            """, unsafe_allow_html=True)
            
            # Use balanced columns for deck selection and upload
            col1, col2 = st.columns([3, 2])
            
            with col1:
                # Deck selection with consistent styling
                render_deck_selector(
                    st.session_state.available_decks, 
                    on_select=start_studying
                )
            
            with col2:
                # Custom deck upload with consistent styling
                render_upload_form(on_upload=handle_custom_deck_upload)
        
        # Full width container for statistics
        if hasattr(st.session_state, 'last_session_stats') and st.session_state.last_session_stats:
            st.markdown("<hr style='margin: 30px 0 15px 0; opacity: 0.2;'>", unsafe_allow_html=True)
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