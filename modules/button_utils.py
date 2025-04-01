"""
Button Utilities Module

This module provides utilities for consistent button handling in the Streamlit application,
using an action queue pattern to ensure reliable button behavior.
"""

import streamlit as st
from typing import Any, Optional, Dict, List, Callable
import time
import uuid
from streamlit.components.v1 import html

# Global tracking variables
_DEBOUNCE_INTERVAL = 0.2  # seconds

# JavaScript for keyboard shortcuts only (more reliable)
_KEYBOARD_SHORTCUTS_JS = """
<script>
// Keyboard shortcuts - reliable implementation that doesn't interfere with normal buttons
document.addEventListener('keydown', function(e) {
    // Only if not in input fields
    if (!['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName)) {
        let buttonKey = null;
        
        switch(e.key) {
            case 'ArrowRight':
                buttonKey = 'next_btn';
                break;
            case 'ArrowLeft':
                buttonKey = 'prev_btn';
                break;
            case ' ':
                buttonKey = 'flip_btn';
                e.preventDefault();  // Prevent page scroll
                break;
            case 'j':
                buttonKey = 'correct_btn';
                break;
            case 'k':
                buttonKey = 'incorrect_btn';
                break;
        }
        
        if (buttonKey) {
            // Find appropriate button and click it
            const buttons = Array.from(document.querySelectorAll('button'));
            const targetButton = buttons.find(btn => 
                btn.getAttribute('key') === buttonKey ||
                btn.getAttribute('data-testid') === buttonKey
            );
            
            if (targetButton) {
                // Click the button and provide visual feedback
                targetButton.click();
                targetButton.style.transform = "scale(0.95)";
                setTimeout(() => {
                    targetButton.style.transform = "scale(1)";
                }, 200);
            }
        }
    }
});
</script>
"""


class ActionHandler:
    """Centralized handler for all application actions."""

    def __init__(self):
        self._initialize_state()
        self._keyboard_shortcuts_initialized = False

    def _initialize_state(self):
        """Initialize or reset the action state."""
        if "action_handler" not in st.session_state:
            st.session_state.action_handler = {
                "pending_actions": [],
                "last_action_time": {},
                "action_counter": {},
                "session_id": str(uuid.uuid4()),
            }

    def register_keyboard_shortcuts(self):
        """Register keyboard shortcuts for common actions."""
        if not self._keyboard_shortcuts_initialized:
            html(_KEYBOARD_SHORTCUTS_JS, height=0, width=0)
            self._keyboard_shortcuts_initialized = True

    def register_action(self, action_id: str) -> bool:
        """
        Register an action to be processed on next render cycle.

        Args:
            action_id (str): Unique identifier for the action

        Returns:
            bool: Whether the action was registered
        """
        # Simple debouncing to prevent double-clicks
        current_time = time.time()
        last_time = st.session_state.action_handler["last_action_time"].get(
            action_id, 0
        )

        if current_time - last_time > _DEBOUNCE_INTERVAL:
            # Add to pending actions
            st.session_state.action_handler["pending_actions"].append(action_id)
            st.session_state.action_handler["last_action_time"][
                action_id
            ] = current_time
            return True

        return False

    def process_actions(self) -> None:
        """Process any pending actions."""
        if "action_handler" not in st.session_state:
            return

        # Get and clear the pending actions
        actions = st.session_state.action_handler["pending_actions"].copy()
        st.session_state.action_handler["pending_actions"] = []

        # Process each action
        for action in actions:
            self._execute_action(action)

    def _execute_action(self, action: str) -> None:
        """
        Execute a single action based on its identifier.

        Args:
            action (str): Action identifier
        """
        if "session_manager" not in st.session_state:
            return

        session_manager = st.session_state.session_manager

        if action.startswith("mark_"):
            if action == "mark_correct":
                session_manager.mark_card(correct=True)
                session_manager.next_card()
            elif action == "mark_incorrect":
                session_manager.mark_card(correct=False)
                session_manager.next_card()
        elif action == "flip_card":
            session_manager.toggle_card_face()
        elif action == "next_card":
            session_manager.next_card()
        elif action == "prev_card":
            session_manager.prev_card()
        elif action == "end_session":
            stats = session_manager.end_session()
            st.session_state.last_session_stats = stats
        elif action.startswith("start_deck_"):
            deck_name = action.replace("start_deck_", "")
            if hasattr(session_manager, "start_deck"):
                session_manager.start_deck(deck_name)
        elif action == "load_custom_deck":
            # This would require specific handling based on your implementation
            pass


# Create a global instance of the action handler
action_handler = ActionHandler()


def create_action_button(
    label: str,
    action_id: str,
    key: Optional[str] = None,
    use_container_width: bool = True,
) -> bool:
    """
    Create a consistently styled action button with reliable behavior.

    Args:
        label (str): Button label
        action_id (str): Action identifier
        key (str, optional): Streamlit widget key
        use_container_width (bool): Whether button should use full container width

    Returns:
        bool: Whether button was clicked in this render cycle
    """
    # Generate a unique key if not provided
    if key is None:
        key = f"btn_{action_id}_{id(label)}"

    # Create the button with standard Streamlit API
    clicked = st.button(label, key=key, use_container_width=use_container_width)

    if clicked:
        # Register the action to be processed
        return action_handler.register_action(action_id)

    return False


def process_actions():
    """Process any pending actions at the beginning of each render cycle."""
    # First make sure keyboard shortcuts are registered
    action_handler.register_keyboard_shortcuts()

    # Then process actions from previous cycle
    action_handler.process_actions()

    # Process legacy action lists for backward compatibility
    if "actions" in st.session_state and st.session_state.actions:
        actions = st.session_state.actions.copy()
        st.session_state.actions = []
        for action in actions:
            action_handler._execute_action(action)

    if "action_queue" in st.session_state and st.session_state.action_queue:
        action = st.session_state.action_queue
        st.session_state.action_queue = None
        action_handler._execute_action(action)


# For backward compatibility with existing code
def _execute_action(action: str) -> None:
    """Execute a single action (legacy method)."""
    action_handler._execute_action(action)
