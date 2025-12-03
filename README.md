# racecontrol-client

Backend data and service layer for the RaceControl F1 dashboard.

- Fetches live F1 data from the Jolpica (Ergast-compatible) API
- Uses pandas for data manipulation
- Exposes clean functions returning JSON-like `list[dict]` structures,
  ready for any frontend (Streamlit, web, mobile, etc.)

Install locally:

```bash
pip install -e .
---

### `racecontrol/__init__.py`

```python
from .data.client import (
    get_completed_round,
    get_schedule,
    get_driver_standings,
    get_constructor_standings,
    get_all_results_up_to,
    get_fantasy_scores,
)

__all__ = [
    "get_completed_round",
    "get_schedule",
    "get_driver_standings",
    "get_constructor_standings",
    "get_all_results_up_to",
    "get_fantasy_scores",
]