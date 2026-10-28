"""End-to-end Playwright tests with a real server and real Chromium browser."""

import os
import shutil
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

import pytest
from playwright.sync_api import expect, sync_playwright

PROJECT_DIR = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def live_server():
    # Find a free local port so tests don't conflict with a running app.
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", str(port)],
        cwd=PROJECT_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
    )
    url = f"http://127.0.0.1:{port}"
    try:
        for _ in range(100):
            if process.poll() is not None:
                pytest.fail("FastAPI server exited before the tests started")
            try:
                with urllib.request.urlopen(url + "/health", timeout=0.2) as response:
                    if response.status == 200:
                        break
            except Exception:
                time.sleep(0.1)
        else:
            pytest.fail("FastAPI server did not become ready")
        yield url
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)


@pytest.fixture
def page():
    with sync_playwright() as playwright:
        # Use Playwright's installed browser, or a local Chromium if this system
        # has not downloaded Playwright's separate browser yet.
        browser_path = os.getenv("PLAYWRIGHT_CHROMIUM_EXECUTABLE")
        if not browser_path and not Path(playwright.chromium.executable_path).exists():
            browser_path = shutil.which("chromium") or shutil.which("chromium-browser")
        browser = playwright.chromium.launch(
            headless=True,
            executable_path=browser_path,
            args=["--no-sandbox"] if browser_path else [],
        )
        page = browser.new_page(viewport={"width": 1280, "height": 900}, device_scale_factor=1)
        yield page
        browser.close()


def test_user_can_add_and_screenshot(page, live_server):
    page.goto(live_server)
    page.get_by_label("Operation").select_option("add")
    page.get_by_label("First number (a)").fill("12")
    page.get_by_label("Second number (b)").fill("3")
    page.get_by_role("button", name="Calculate").click()
    expect(page.locator("#result-value")).to_have_text("15")
    screenshot_dir = PROJECT_DIR / "screenshots"
    screenshot_dir.mkdir(exist_ok=True)
    page.screenshot(path=str(screenshot_dir / "application-running.png"), full_page=True)


def test_user_can_see_division_error(page, live_server):
    page.goto(live_server)
    page.get_by_label("Operation").select_option("divide")
    page.get_by_label("First number (a)").fill("9")
    page.get_by_label("Second number (b)").fill("0")
    page.get_by_role("button", name="Calculate").click()
    page.get_by_text("Cannot divide by zero").wait_for()


def test_user_can_take_root(page, live_server):
    page.goto(live_server)
    page.get_by_label("Operation").select_option("root")
    page.get_by_label("First number (a)").fill("81")
    page.get_by_label("Second number (b)").fill("4")
    page.get_by_role("button", name="Calculate").click()
    expect(page.locator("#result-value")).to_have_text("3")
