"""
conftest.py = the BaseTest (Framework step 12).
Every test file gets these fixtures automatically, like classes that extend BaseTest in TestNG.

  driver         - a fresh browser for ONE test (like @BeforeMethod / @AfterMethod)
  logged_in      - one logged-in browser shared by a whole test file (like @BeforeClass / @AfterClass)
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pages.login_page import LoginPage          # noqa: E402
from utils import config_reader as cfg          # noqa: E402
from utils.driver_factory import create_driver  # noqa: E402
from utils.logger import get_logger             # noqa: E402

log = get_logger("BaseTest")
ROOT = os.path.dirname(os.path.abspath(__file__))


def pytest_addoption(parser):
    # Run in any browser:  pytest --browser firefox   (Framework step 16)
    parser.addoption("--browser", default=cfg.get("run", "browser"), help="chrome, firefox or edge")
    parser.addoption("--headless", action="store_true", default=cfg.get("run", "headless") == "true")


def _new_driver(request):
    browser = request.config.getoption("--browser")
    log.info("Starting %s browser", browser)
    drv = create_driver(browser, request.config.getoption("--headless"))
    drv.implicitly_wait(int(cfg.get("run", "implicit_wait")))
    return drv


@pytest.fixture
def driver(request):
    drv = _new_driver(request)
    request.node._driver = drv
    yield drv
    log.info("Closing browser")
    drv.quit()


@pytest.fixture(scope="module")
def logged_in(request):
    drv = _new_driver(request)
    assert LoginPage(drv).load().login_as_training_user(), "Login failed - check the credentials in config.ini"
    log.info("Logged in as training user")
    yield drv
    drv.quit()


@pytest.fixture(autouse=True)
def _remember_module_driver(request):
    """Lets the screenshot hook find the browser for tests that use 'logged_in'."""
    if "logged_in" in request.fixturenames:
        request.node._driver = request.getfixturevalue("logged_in")
    yield


# ---- dependsOnMethods: @pytest.mark.depends_on("test_name") ----
_results = {}


def pytest_configure(config):
    config.addinivalue_line("markers", "depends_on(name): skip this test if the named test did not pass")


def pytest_runtest_setup(item):
    for mark in item.iter_markers(name="depends_on"):
        for name in mark.args:
            if _results.get(name) != "passed":
                pytest.skip(f"depends on {name}, which did not pass")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Record results and take a screenshot automatically when a test fails."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call":
        _results[item.originalname or item.name] = report.outcome
    drv = getattr(item, "_driver", None)
    if report.when == "call" and report.failed and drv is not None:
        folder = os.path.join(ROOT, "reports", "screenshots")
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, item.name + ".png")
        try:
            drv.save_screenshot(path)
            log.error("Test failed - screenshot saved: %s", path)
        except Exception:
            pass
