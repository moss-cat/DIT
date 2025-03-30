"""
FlashCard Memory Tool

A Streamlit application for flashcard-based learning and memory enhancement.
Main application entry point.
"""

import streamlit as st
import pandas as pd
import os
from pathlib import Path

# Initialize layout preference before any other Streamlit commands
if "layout_preference" not in st.session_state:
    st.session_state.layout_preference = "centered"  # Default to centered layout

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

# Configure page settings with dynamic layout
st.set_page_config(
    page_title="FlashCard Memory Tool",
    page_icon="📚",
    layout=st.session_state.layout_preference,
    initial_sidebar_state="collapsed"
)

# Load custom CSS
def load_css():
    css_file = Path("assets/styles.css")
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
            
    # Add custom button alignment CSS
    button_alignment_css = """
    /* Button alignment fixes */
    .home-page-buttons .stButton {
        position: relative;
        display: flex;
        justify-content: flex-start;
        margin-top: 31px;  /* Aligns with selectbox */
    }
    
    .home-page-buttons .stButton > button {
        width: 100%;
    }
    
    /* Upload form button alignment */
    .upload-button .stButton {
        margin-top: 24px;  /* Specific margin for upload button */
    }
    """
    st.markdown(f"<style>{button_alignment_css}</style>", unsafe_allow_html=True)

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

# Function to toggle between layout modes
def toggle_layout():
    if st.session_state.layout_preference == "wide":
        st.session_state.layout_preference = "centered"
    else:
        st.session_state.layout_preference = "wide"
    st.rerun()  # Required to apply the new layout

# Process actions function to handle action queue
def process_actions():
    """Process any pending actions in the queue at the beginning of each render cycle."""
    if "action_queue" not in st.session_state:
        st.session_state.action_queue = None
        
    if st.session_state.action_queue:
        action = st.session_state.action_queue
        st.session_state.action_queue = None
        
        # Process the queued action
        if action.startswith("mark_"):
            if action == "mark_correct":
                st.session_state.session_manager.mark_card(correct=True)
                st.session_state.session_manager.next_card()
            elif action == "mark_incorrect":
                st.session_state.session_manager.mark_card(correct=False)
                st.session_state.session_manager.next_card()
        elif action == "flip_card":
            st.session_state.session_manager.toggle_card_face()
        elif action == "next_card":
            st.session_state.session_manager.next_card()
        elif action == "prev_card":
            st.session_state.session_manager.prev_card()

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

# Updated button handlers using the action queue pattern
def handle_flip_card():
    st.session_state.action_queue = "flip_card"
    st.rerun()

def handle_next_card():
    st.session_state.action_queue = "next_card"
    st.rerun()

def handle_prev_card():
    st.session_state.action_queue = "prev_card"
    st.rerun()

def handle_mark_correct():
    st.session_state.action_queue = "mark_correct"
    st.rerun()

def handle_mark_incorrect():
    st.session_state.action_queue = "mark_incorrect"
    st.rerun()

def handle_end_session():
    stats = st.session_state.session_manager.end_session()
    st.session_state.last_session_stats = stats

def handle_mode_change(mode):
    st.session_state.study_mode = mode

# Main application function
def main():
    # Process any pending actions
    process_actions()
    
    # Load CSS and initialize app
    load_css()
    initialize_app()
    
    # Get current state
    session_manager = st.session_state.session_manager
    is_studying = getattr(st.session_state, 'is_studying', False)
    
    # Render app header with context
    render_app_header(is_studying=is_studying)
    
    # Add layout toggle in sidebar
    with st.sidebar:
        st.title("Settings")
        current_layout = "Wide" if st.session_state.layout_preference == "wide" else "Centered"
        if st.button(f"Switch to {'Centered' if current_layout == 'Wide' else 'Wide'} Layout"):
            toggle_layout()
        st.write(f"Current layout: {current_layout}")
    
    # Main application logic
    if not is_studying:
        # Display deck selector when not studying
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Use columns to properly align the deck selector components
            select_col, button_col = st.columns([3, 1])
            
            with select_col:
                selected_deck = st.selectbox(
                    "Select a deck to study", 
                    options=st.session_state.available_decks,
                    format_func=lambda x: x.replace("_", " ").title(),
                    key="deck_selector"
                )
            
            with button_col:
                # Apply CSS class for button alignment
                with st.container():
                    st.markdown('<div class="home-page-buttons">', unsafe_allow_html=True)
                    if st.button("Start Studying", key="start_deck_btn"):
                        start_studying(selected_deck)
                    st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            # Custom deck upload with aligned button
            with st.expander("Upload Custom Deck"):
                st.write("Upload a CSV file with columns: front, back, deck")
                
                uploaded_file = st.file_uploader(
                    "Choose a CSV file",
                    type="csv",
                    help="File must have 'front', 'back', and 'deck' columns"
                )
                
                # Apply CSS class for upload button alignment
                st.markdown('<div class="upload-button">', unsafe_allow_html=True)
                if uploaded_file is not None and st.button("Load Deck"):
                    handle_custom_deck_upload(uploaded_file.getvalue())
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown("""
                **CSV Format Example:**
                ```
                front,back,deck
                "What is Python?","A programming language","Programming"
                ```
                """)
            
            # Display deck info if available
            if selected_deck:
                with st.expander("Deck Information"):
                    st.info(f"Selected deck: **{selected_deck.replace('_', ' ').title()}**")
                    st.write("Use the Start Studying button to begin with this deck.")
        
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