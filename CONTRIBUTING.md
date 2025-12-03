# Contributing to This Project

Thank you for your interest in contributing!  
This repository follows a clean separation of architecture between:

- **Client Library (`raceControlClient`)** – data, services, logic  
- **Core Application (`racecontrol-core`)** – UI, visualizations, user experience  

Before contributing, please review the guidelines below.

---

# 🧭 Contribution Workflow

### 1. Fork the repository
Click **Fork** on GitHub and clone your copy.

### 2. Create a feature branch
```bash
git checkout -b feature/my-new-feature
```
### 3. Make your changes
Follow the architectural boundaries described in `ARCHITECTURE.md`.

### 4. Run tests (if contributing to the client package)
```bash
pytest
```
### 5. Commit with a clear message
```bash
git commit -m “Add new feature: description”
```
### 6. Push and open a Pull Request
Create a PR into the `main` branch.

---

# 🧱 Coding Standards

## For `raceControlClient` (Backend Library)
- Place **business logic** in `services/`
- Place **data fetching** in `data/`
- Place **shared helpers** in `utils/`
- Do NOT add UI or framework-specific logic
- Keep the public API clean (`__init__.py`)
- Add tests for new or modified logic
- Maintain Semantic Versioning

## For `racecontrol-core` (Frontend App)
- Place **UI components** in `ui/`
- Place **app-specific helpers** in `services/`
- Place formatting/utility functions in `utils/`
- Do NOT re-implement backend logic here
- All data must come from the client package

---

# 🧪 Testing Guidelines

### For the client library:
- Use `pytest`
- Cover new logic with meaningful tests
- Avoid unnecessary mocks; prefer real or fixture data

### For the core app:
- UI snapshots or component tests (optional)
- Keep UI logic simple and testable in isolation

---

# 🎨 Code Style
- Follow PEP8 for Python
- Use descriptive function and variable names
- Avoid deeply nested logic when possible
- Document complex functions with docstrings

---

# 📝 Pull Request Requirements
- Clear summary of changes
- Explanation of why the change is needed
- Tests for backend changes
- Screenshots for UI changes (if applicable)
- Update documentation if needed
- Update version numbers (client library only)

---

# 👥 Community Guidelines
- Be respectful and collaborative  
- Keep discussions focused and constructive  
- Offer help to new contributors  
- Celebrate improvements, even small ones 🎉

---

# 🙌 Thank You!
Your contributions make the project better for everyone.