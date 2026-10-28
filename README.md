# IS601 — Module 8 FastAPI Calculator

A working FastAPI calculator with arithmetic operations, logging, unit tests, API integration tests, Playwright end-to-end browser tests, and GitHub Actions continuous integration (CI).

## Prerequisites

- Python 3.10 or newer
- Internet access to install the Python dependencies and Chromium the first time

## Fast Windows setup

For the simplest setup, double-click `1_SETUP_WINDOWS.bat`, then `2_START_APP_WINDOWS.bat` to run the calculator, and `3_RUN_TESTS_WINDOWS.bat` to test it. If Windows blocks batch files or you prefer VS Code, use the commands below.

## Install (Windows / VS Code terminal)

```powershell
py -m pip install -r requirements.txt
py -m playwright install chromium
```

If `py` doesn't work, replace `py` with `python`.

## Start the web application

```powershell
py -m uvicorn main:app --reload
```

Open http://127.0.0.1:8000 in Chrome or Edge. Enter two numbers, choose Add, Subtract, Multiply, Divide, Power, or Root, and click **Calculate**. Press `Ctrl+C` in the terminal to stop the app.

API docs: http://127.0.0.1:8000/docs

## Run all tests

Open a **second terminal** in the project folder and run:

```powershell
py -m pytest -v
```

The tests include:

- `tests/test_operations.py`: unit tests for **all six operations** plus error cases.
- `tests/test_api.py`: integration tests for **all four API routes** plus input validation, logging, and static assets.
- `tests/test_e2e.py`: Playwright browser tests of Add, Divide by zero, and Root; they launch a temporary real FastAPI server automatically.

After `pytest` passes, the Playwright test generates `screenshots/application-running.png`.

## Logging

Successful calculations and errors are logged to the VS Code terminal and to `logs/calculator.log`.

## GitHub Actions

`.github/workflows/tests.yml` automatically runs the complete suite on every push and pull request. It installs Python 3.12, Python packages, and Chromium before running tests. After pushing the repository to GitHub:

1. Open your GitHub repository.
2. Click **Actions** > **FastAPI Calculator Tests**.
3. Click the latest successful run with a **green checkmark**.
4. Take a screenshot showing the successful workflow run. This is one required screenshot.
5. For the second required screenshot, show the **working application in the browser** with the result visible. (You can use `screenshots/application-running.png` or take your own screenshot.)

## Assignment submission checklist

- [ ] GitHub repository accessible to instructor and contains `main.py`, `operations.py`, `requirements.txt`, `tests/`, `.github/workflows/tests.yml` and UI files.
- [ ] All six calculator operations work, including error handling.
- [ ] `py -m pytest -v` passes locally (unit, integration, e2e).
- [ ] GitHub Actions workflow shows a green checkmark.
- [ ] Screenshot of the successful GitHub Actions run.
- [ ] Screenshot of the working calculator in the browser.
- [ ] Submit your **GitHub repository URL** and upload both screenshots to the assignment.

**Note:** If your instructor gave you an existing starter FastAPI project, verify whether the assignment requires modifying that exact starter. This folder is a complete standalone solution and may need to be integrated into the instructor's starter code.
