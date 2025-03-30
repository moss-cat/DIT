"""
UI Components Module

This module provides Streamlit UI components for rendering various elements
of the flashcard application interface.
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Any, Optional, Callable
import random


def render_deck_selector(available_decks: List[str], on_select: Callable[[str], None]) -> str:
    """
    Render a dropdown selector for available decks.
    
    Args:
        available_decks (List[str]): List of available deck names
        on_select (Callable[[str], None]): Callback function when deck is selected
        
    Returns:
        str: Selected deck name
    """
    col1, col2 = st.columns([3, 1])
    
    with col1:
        selected_deck = st.selectbox(
            "Select a deck to study", 
            options=available_decks,
            format_func=lambda x: x.replace("_", " ").title(),
            key="deck_selector"
        )
    
    with col2:
        st.write("&nbsp;")  # Spacing
        if st.button("Start Studying", key="start_deck_btn"):
            on_select(selected_deck)
    
    # Display deck info if available
    if selected_deck:
        with st.expander("Deck Information"):
            st.info(f"Selected deck: **{selected_deck.replace('_', ' ').title()}**")
            st.write("Use the Start Studying button to begin with this deck.")
    
    return selected_deck


def render_card(card: Dict[str, Any], show_answer: bool = False) -> None:
    """
    Render a flashcard with question and optional answer.
    
    Args:
        card (Dict[str, Any]): Card data with 'front' and 'back' keys
        show_answer (bool): Whether to show the answer
    """
    if not card:
        st.warning("No card available")
        return
    
    # Card styling
    st.markdown("""
        <style>
        .card-container {
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
            text-align: center;
            min-height: 200px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        .card-question {
            font-size: 1.5em;
            font-weight: 500;
            margin-bottom: 20px;
        }
        .card-answer {
            font-size: 1.3em;
            color: #1f77b4;
            font-weight: 500;
            padding: 10px;
            background-color: #e9ecef;
            border-radius: 5px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Card front (question)
    st.markdown(f"""
        <div class="card-container">
            <div class="card-question">{card['front']}</div>
            {"<div class='card-answer'>" + card['back'] + "</div>" if show_answer else ""}
        </div>
    """, unsafe_allow_html=True)
    
    # Card controls rendered separately


def render_card_controls(
    on_flip: Callable[[], None],
    on_next: Callable[[], None],
    on_prev: Callable[[], None],
    on_correct: Callable[[], None],
    on_incorrect: Callable[[], None],
    show_answer: bool
) -> None:
    """
    Render controls for flashcard navigation and evaluation.
    
    Args:
        on_flip (Callable[[], None]): Callback for flipping card
        on_next (Callable[[], None]): Callback for next card
        on_prev (Callable[[], None]): Callback for previous card
        on_correct (Callable[[], None]): Callback for marking card correct
        on_incorrect (Callable[[], None]): Callback for marking card incorrect
        show_answer (bool): Whether answer is currently shown
    """
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("← Previous", key="prev_btn"):
            on_prev()
    
    with col2:
        flip_col, correct_col, incorrect_col = st.columns(3)
        
        with flip_col:
            if st.button("Flip Card", key="flip_btn"):
                on_flip()
        
        if show_answer:
            with correct_col:
                if st.button("👍 Correct", key="correct_btn"):
                    on_correct()
            
            with incorrect_col:
                if st.button("👎 Incorrect", key="incorrect_btn"):
                    on_incorrect()
    
    with col3:
        if st.button("Next →", key="next_btn"):
            on_next()


def render_progress_bar(progress: Dict[str, Any]) -> None:
    """
    Render a progress bar showing study session progress.
    
    Args:
        progress (Dict[str, Any]): Progress data with percent, seen, total, etc.
    """
    if not progress:
        return
    
    # Overall progress
    st.progress(progress["percent"] / 100)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Cards Seen", f"{progress['seen']}/{progress['total']}")
    
    with col2:
        correct_pct = (progress['correct'] / progress['seen'] * 100) if progress['seen'] > 0 else 0
        st.metric("Correct", f"{progress['correct']} ({correct_pct:.1f}%)")
    
    with col3:
        incorrect_pct = (progress['incorrect'] / progress['seen'] * 100) if progress['seen'] > 0 else 0
        st.metric("Incorrect", f"{progress['incorrect']} ({incorrect_pct:.1f}%)")


def render_study_options(
    on_mode_change: Callable[[str], None], 
    current_mode: str = "sequential"
) -> None:
    """
    Render study options like mode selection.
    
    Args:
        on_mode_change (Callable[[str], None]): Callback when mode changes
        current_mode (str): Current study mode
    """
    with st.expander("Study Options"):
        col1, col2 = st.columns(2)
        
        with col1:
            mode = st.radio(
                "Card Order",
                options=["Sequential", "Random"],
                index=0 if current_mode == "sequential" else 1,
                key="study_mode_radio"
            )
            if mode.lower() != current_mode:
                on_mode_change(mode.lower())
        
        with col2:
            st.info(
                "**Sequential**: Cards in original order\n\n"
                "**Random**: Cards in shuffled order"
            )


def render_statistics(session_stats: Dict[str, Any]) -> None:
    """
    Render session statistics.
    
    Args:
        session_stats (Dict[str, Any]): Session statistics data
    """
    if not session_stats:
        return
    
    st.subheader("Session Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Cards", session_stats.get("total_cards", 0))
        st.metric("Cards Seen", session_stats.get("cards_seen", 0))
        st.metric("Accuracy", f"{session_stats.get('accuracy', 0):.1f}%")
    
    with col2:
        st.metric("Correct", session_stats.get("cards_correct", 0))
        st.metric("Incorrect", session_stats.get("cards_incorrect", 0))
        
        # Calculate duration in minutes and seconds
        duration = session_stats.get("duration_seconds", 0)
        minutes = int(duration // 60)
        seconds = int(duration % 60)
        st.metric("Study Time", f"{minutes}m {seconds}s")
    
    # Add some motivational feedback based on performance
    accuracy = session_stats.get("accuracy", 0)
    if accuracy > 90:
        st.success("Excellent work! Your mastery of this material is impressive.")
    elif accuracy > 75:
        st.success("Great job! You're showing strong understanding.")
    elif accuracy > 50:
        st.info("Good progress. Keep reviewing the cards you missed.")
    else:
        st.info("Keep practicing! Repetition is key to mastery.")


def render_upload_form(on_upload: Callable[[bytes], None]) -> None:
    """
    Render a form for uploading custom flashcard decks.
    
    Args:
        on_upload (Callable[[bytes], None]): Callback when file is uploaded
    """
    with st.expander("Upload Custom Deck"):
        st.write("Upload a CSV file with columns: front, back, deck")
        
        uploaded_file = st.file_uploader(
            "Choose a CSV file",
            type="csv",
            help="File must have 'front', 'back', and 'deck' columns"
        )
        
        col1, col2 = st.columns([1, 3])
        with col1:
            if uploaded_file is not None and st.button("Load Deck"):
                on_upload(uploaded_file.getvalue())
                st.success("Custom deck uploaded!")
        
        with col2:
            st.markdown("""
            **CSV Format Example:**
            ```
            front,back,deck
            "What is Python?","A programming language","Programming"
            ```
            """)


def render_app_header() -> None:
    """Render the application header."""
    st.title("FlashCard Memory Tool")
    st.markdown("""
        Improve your memory and knowledge retention with spaced repetition flashcards.
        Select a deck from the available options or upload your own custom deck.
    """)


def render_end_session_button(on_end: Callable[[], None]) -> None:
    """
    Render end session button.
    
    Args:
        on_end (Callable[[], None]): Callback when session ends
    """
    if st.button("End Session", key="end_session_btn"):
        on_end()