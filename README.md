# FlashCard Memory Tool

A Streamlit application for flashcard-based learning and memory enhancement.

## Overview

This project implements a web-based flashcard system using Streamlit that allows users to:
- Load pre-existing CSV flashcard sets from the repository
- Upload custom CSV flashcard sets
- Study and review flashcards through an intuitive UI

## Tech Stack

- **Frontend/Backend**: Streamlit
- **Data Handling**: Pandas
- **Language**: Python 3.13

## Implementation Details

```python
# Core components:
# - CSV parser with Pandas
# - Streamlit UI components
# - State management for tracking study progress
```

## CSV Schema

```
front,back,deck
"What is Time Complexity?","A measure of algorithm efficiency as input grows",CS
"Define Big O Notation","Upper bound of growth rate",Algorithms
```

## Features

- Stateless architecture with session-based user data
- Dynamic card rendering based on user interaction
- Progress tracking through session state variables
- Customizable study parameters

## Setup & Running

```bash
git clone <repo-url>
cd flashcard-tool
pip install -r requirements.txt
streamlit run app.py
```

## Planned Enhancements

- [ ] Implement spaced repetition algorithm
- [ ] Add localStorage support for progress persistence
- [ ] Implement card difficulty ranking

## Notes

Academic project, not intended for public deployment.