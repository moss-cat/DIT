"""
UI Components Module

This module provides Streamlit UI components for rendering various elements
of the flashcard application interface.
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Any, Optional, Callable
import random


def render_deck_selector(
    available_decks: List[str], on_select: Callable[[str], None]
) -> str:
    """
    Render a grid of available decks to select from.

    Args:
        available_decks (List[str]): List of available deck names
        on_select (Callable[[str], None]): Callback function when deck is selected

    Returns:
        str: Selected deck name for form compatibility
    """
    # Custom container styling for grid layout
    st.markdown(
        """
    <style>
    /* Updated deck grid for better responsiveness */
    .deck-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
        gap: 20px;
        margin-bottom: 20px;
    }
    
    /* Deck card with adaptive height */
    .deck-card {
        background-color: white;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        transition: transform 0.2s, box-shadow 0.2s;
        min-height: auto;
    }
    
    .deck-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    .deck-title {
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 15px;
    }
    
    /* Put deck button at bottom of card */
    .deck-button-container {
        width: 100%;
        margin-top: 10px;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    st.subheader("Choose a Deck to Study")

    # Begin deck grid container
    st.markdown('<div class="deck-grid">', unsafe_allow_html=True)

    # Track selected deck
    selected_deck = None

    # Generate deck cards directly in the grid
    for deck_name in available_decks:
        display_name = deck_name.replace("_", " ").title()

        # Create deck card
        st.markdown(
            f"""
        <div class="deck-card">
            <div class="deck-button-container"></div>
            <div class="deck-title">{display_name}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Standardized button size
        if st.button(
            f"Study",
            key=f"study_{deck_name}",
            on_click=lambda d=deck_name: on_select(d),
            use_container_width=True,
        ):
            selected_deck = deck_name

    # End deck grid container
    st.markdown("</div>", unsafe_allow_html=True)

    # Additional information section
    with st.expander("Deck Information", expanded=False):
        st.info("Select a deck from above to begin studying")
        st.write("Click any 'Study' button to begin with your selected deck.")

    # Return the first deck as default for form compatibility
    return selected_deck or available_decks[0] if available_decks else ""


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
    st.markdown(
        """
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
    """,
        unsafe_allow_html=True,
    )

    # Card front (question)
    st.markdown(
        f"""
        <div class="card-container">
            <div class="card-question">{card['front']}</div>
            {"<div class='card-answer'>" + card['back'] + "</div>" if show_answer else ""}
        </div>
    """,
        unsafe_allow_html=True,
    )

    # Card controls rendered separately


def render_card_controls(
    on_flip: Callable[[], None],
    on_next: Callable[[], None],
    on_prev: Callable[[], None],
    on_correct: Callable[[], None],
    on_incorrect: Callable[[], None],
    show_answer: bool,
) -> None:
    """Render card control buttons with consistent alignment."""

    # Create fixed-height container for all controls
    with st.container():
        st.markdown(
            """
        <style>
        /* Force consistent button container height */
        [data-testid="stHorizontalBlock"] {
            align-items: center;
            margin-bottom: 1rem;
        }
        /* Container for all buttons to maintain consistent height */
        .controls-container {
            min-height: 50px;
            margin: 10px 0;
        }
        </style>
        <div class="controls-container"></div>
        """,
            unsafe_allow_html=True,
        )

        # Navigation row - always visible
        nav_cols = st.columns([1, 4, 1])

        with nav_cols[0]:
            st.button(
                "← Previous", key="prev_btn", on_click=on_prev, use_container_width=True
            )

        # Center column - either empty or used for instructions
        with nav_cols[1]:
            if not show_answer:
                st.markdown(
                    "<div style='text-align:center; color:#666;'>Use keyboard: ← → to navigate, Space to flip</div>",
                    unsafe_allow_html=True,
                )

        with nav_cols[2]:
            st.button(
                "Next →", key="next_btn", on_click=on_next, use_container_width=True
            )

        # Add separator for visual distinction
        st.markdown(
            "<hr style='margin: 10px 0; opacity: 0.2;'>", unsafe_allow_html=True
        )

        # Action buttons (flip/correct/incorrect)
        if not show_answer:
            # When answer is hidden - center the flip button
            action_cols = st.columns([1, 2, 1])
            with action_cols[1]:
                st.button(
                    "Flip Card",
                    key="flip_btn",
                    on_click=on_flip,
                    use_container_width=True,
                )
        else:
            # When answer is showing - show all three action buttons
            action_cols = st.columns([1, 1, 1])

            with action_cols[0]:
                st.button(
                    "👍 Correct",
                    key="correct_btn",
                    on_click=on_correct,
                    use_container_width=True,
                )

            with action_cols[1]:
                st.button(
                    "🔄 Flip",
                    key="flip_btn_shown",
                    on_click=on_flip,
                    use_container_width=True,
                )

            with action_cols[2]:
                st.button(
                    "👎 Incorrect",
                    key="incorrect_btn",
                    on_click=on_incorrect,
                    use_container_width=True,
                )


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
        correct_pct = (
            (progress["correct"] / progress["seen"] * 100)
            if progress["seen"] > 0
            else 0
        )
        st.metric("Correct", f"{progress['correct']} ({correct_pct:.1f}%)")

    with col3:
        incorrect_pct = (
            (progress["incorrect"] / progress["seen"] * 100)
            if progress["seen"] > 0
            else 0
        )
        st.metric("Incorrect", f"{progress['incorrect']} ({incorrect_pct:.1f}%)")


def render_study_options(
    on_mode_change: Callable[[str], None], current_mode: str = "sequential"
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
                key="study_mode_radio",
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
    # Custom container styling for consistent appearance with deck grid
    st.markdown(
        """
    <style>
    .upload-container {
        background-color: white;
        border-radius: 8px;
        padding: 15px 15px 25px 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 15px;
    }
    .upload-button-container {
        margin-top: 15px;
        display: flex;
        justify-content: flex-start;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    st.subheader("Upload Custom Deck")

    # File uploader in a cleaner container
    with st.container():
        # File uploader component
        uploaded_file = st.file_uploader(
            "Upload a CSV file with your flashcards",
            type=["csv"],
            help="CSV must have 'front', 'back', and 'deck' columns",
        )

        # Button container with standardized sizing
        if uploaded_file is not None:
            st.button(
                "Load Custom Deck",
                key="upload_deck_btn",
                on_click=lambda: on_upload(uploaded_file.getvalue()),
                use_container_width=False,
            )

    # Example format in an expander
    with st.expander("CSV Format Example"):
        st.code(
            """front,back,deck
"What is Python?","A programming language","Programming"
"What is a variable?","A storage location with a name","Programming"
""",
            language="csv",
        )


def render_app_header() -> None:
    """Render the application header."""
    st.title("FlashCard Memory Tool")
    st.markdown(
        """
        Improve your memory and knowledge retention with spaced repetition flashcards.
        Select a deck to study or upload your own custom deck.
    """
    )


def render_end_session_button(on_end: Callable[[], None]) -> None:
    """
    Render end session button.

    Args:
        on_end (Callable[[], None]): Callback when session ends
    """
    # Add a container for consistent button sizing
    st.markdown(
        '<div style="max-width: 200px; margin: 0 auto;">', unsafe_allow_html=True
    )
    if st.button("End Session", key="end_session_btn", on_click=on_end):
        pass  # The on_click handler will be called
    st.markdown("</div>", unsafe_allow_html=True)
