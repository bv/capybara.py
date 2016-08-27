import inspect
import os.path
import pytest

import capybara
from capybara.tests.app import app


_DIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
_FIXTURE_DIR = os.path.join(_DIR, "fixtures")


@pytest.fixture(autouse=True)
def setup_capybara():
    original_app = capybara.app
    original_app_host = capybara.app_host
    original_automatic_reload = capybara.automatic_reload
    original_default_max_wait_time = capybara.default_max_wait_time
    original_default_selector = capybara.default_selector
    try:
        capybara.app = app
        capybara.app_host = None
        capybara.default_max_wait_time = 1
        capybara.default_selector = "xpath"
        yield
    finally:
        capybara.app = original_app
        capybara.app_host = original_app_host
        capybara.automatic_reload = original_automatic_reload
        capybara.default_max_wait_time = original_default_max_wait_time
        capybara.default_selector = original_default_selector


@pytest.fixture(scope="session")
def session(driver):
    from capybara.session import Session

    return Session(driver, app)


@pytest.fixture(scope="session")
def fixture_path():
    def fixture_path(fixture_name):
        return os.path.join(_FIXTURE_DIR, fixture_name)

    return fixture_path


@pytest.fixture(autouse=True)
def reset_session(session):
    try:
        yield
    finally:
        session.reset()
