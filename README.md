# 🏎️ racecontrol-client  
### A Lightweight, Modular Python Client Library for Data, Analytics, and Application Backends

`racecontrol-client` is a clean, extensible Python package that provides the
data-access layer, transformation logic, and analytical services used by
applications such as **RaceControl**, dashboards, automation scripts, and future
API servers.

This library is designed to be **framework-agnostic**, **UI-independent**, and
**easily reusable** across multiple projects.

---

## ✨ Features

- 📡 **Unified API wrapper** for external data sources  
- 🔍 **Structured data → transformed analysis** using service layers  
- 🛠️ **Utility modules** for HTTP, configuration, and shared helpers  
- 📦 **Installable Python package** (`pip install`)  
- 🌱 Clean architecture using `data/`, `services/`, and `utils/`  
- 🔁 Designed for use in apps, dashboards, scripts, and automation workflows  

---

## 📁 Project Structure
```
racecontrolClient/
    ├─ data/         → API providers, data fetching, raw ingestion
    ├─ services/     → Business logic, analysis, scoring, transformations
    ├─ utils/        → Config, constants, HTTP helpers
    └─ init.py   → Public API exports
```

This structure ensures the client library remains **decoupled**, **testable**,
and **extendable**.

---

## 🚀 Installing

### Local development installation:
```bash
pip install -e .
```
## Uninstall:
```bash
pip uninstall racecontrolClient -y
```

## 🧩 Using the Client
```python
from racecontrolClient import (
    get_schedule,
    get_driver_standings,
    get_constructor_standings,
    get_fantasy_scores,
)

schedule = get_schedule("2025")
standings = get_driver_standings("2025")
scores = get_fantasy_scores("2025")
```

## 🛠️ Development
Installing dependencies
```bash
pip install -r requirements-dev.txt
```
Project guidelines
- All business logic belongs in services/
- All data access belongs in data/
- All shared helpers belong in utils/
- Avoid placing UI or framework logic in this repo

## 🧪 Versioning
Follow Semantic Versioning:
- 1.0.0 — First stable release
- 1.1.x — New features, no breaking changes
- 2.0.0 — Breaking API changes

## 🤝 Contributing
Contributions are welcome! Please open issues or pull requests on GitHub.

Please follow the guidelines in CONTRIBUTING.md, which explains:
- Branching strategy
- Opening pull requests
- Adding tests
- Updating the public API

## 📄 License
This project is licensed under the MIT [License](LICENSE). See the LICENSE file for details.