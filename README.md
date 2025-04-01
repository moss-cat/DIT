# FlashCard Memory Tool

A Streamlit-driven web app that helps users study flashcards interactively.


debugging showen here: <https://docs.google.com/spreadsheets/d/1ZcmgWSVG_q8s4AN4rV4EP_TQ-BU4sYPGXpqZ8CcAXHc/edit?usp=sharing>

## Overview

This tool allows you to:

* Upload or load existing CSV flashcard sets.
* Quickly flip through the cards with intuitive UI elements.
* Track progress using session state to remember how many cards have been studied.

## Tech Stack

* **Python 3.13** for backend logic.
* **Streamlit** for rapid UI development and deployment.
* **Pandas** for CSV parsing and data handling.

## Implementation Details

```python
# Features:
# 1. CSV parsing with Pandas
# 2. Streamlit-based rendering
# 3. Session-based study tracking
```

## CSV Schema

```
front,back,deck
"What is Time Complexity?","A measure of algorithm efficiency",CS
"What is Big O?","An upper bound of growth rate",Algorithms
```

## Features

* Session-aware progress and deck management.
* Clean, responsive UI with card flipping animations.
* Option to upload custom CSV card sets.

## Setup & Running

```bash
git clone <repo-url>
cd flashcard-tool
pip install -r requirements.txt
streamlit run app.py
```

## Planned Enhancements

- [ ] Implement spaced repetition.
- [ ] Add localStorage support for persisting stats.
- [ ] Allow card difficulty ranking.

## Notes

This project is for academic exploration and not intended for public production.