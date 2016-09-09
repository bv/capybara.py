import pytest
import re

import capybara


class TestHasSelector:
    @pytest.fixture(autouse=True)
    def setup_session(self, session):
        session.visit("/with_html")

    def test_is_true_if_the_given_selector_is_on_the_page(self, session):
        assert session.has_selector("xpath", "//p")
        assert session.has_selector("css", "p a#foo")
        assert session.has_selector("//p[contains(.,'est')]")

    def test_is_false_if_the_given_selector_is_not_on_the_page(self, session):
        assert not session.has_selector("xpath", "//abbr")
        assert not session.has_selector("css", "p a#doesnotexist")
        assert not session.has_selector("//p[contains(.,'thisstringisnotonpage')]")

    def test_uses_default_selector(self, session):
        capybara.default_selector = "css"
        assert not session.has_selector("p a#doesnotexist")
        assert session.has_selector("p a#foo")

    def test_respects_scopes(self, session):
        with session.scope("//p[@id='first']"):
            assert session.has_selector(".//a[@id='foo']")
            assert not session.has_selector(".//a[@id='red']")

    def test_is_true_if_the_content_is_on_the_page_the_given_number_of_times(self, session):
        assert session.has_selector("//p", count=3)
        assert session.has_selector("//p//a[@id='foo']", count=1)
        assert session.has_selector("//p[contains(.,'est')]", count=1)

    def test_is_false_if_the_content_is_not_on_the_page_the_given_number_of_times(self, session):
        assert not session.has_selector("//p", count=6)
        assert not session.has_selector("//p//a[@id='foo']", count=2)
        assert not session.has_selector("//p[contains(.,'est')]", count=5)

    def test_is_false_if_the_content_is_not_on_the_page_at_all(self, session):
        assert not session.has_selector("//abbr", count=2)
        assert not session.has_selector("//p//a[@id='doesnotexist']", count=1)

    def test_discards_all_matches_where_the_given_string_is_not_contained(self, session):
        assert session.has_selector("//p//a", text="Redirect", count=1)
        assert not session.has_selector("//p", text="Doesnotexist")

    def test_respects_visibility_setting(self, session):
        assert session.has_selector("id", "hidden-text", text="Some of this text is hidden!", visible=False)
        assert not session.has_selector("id", "hidden-text", text="Some of this text is hidden!", visible=True)
        capybara.ignore_hidden_elements = False
        assert session.has_selector("id", "hidden-text", text="Some of this text is hidden!", visible=False)
        capybara.visible_text_only = True
        assert not session.has_selector("id", "hidden-text", text="Some of this text is hidden!", visible=True)

    def test_discards_all_matches_where_the_given_regex_is_not_matched(self, session):
        assert session.has_selector("//p//a", text=re.compile("re[dab]i", re.IGNORECASE), count=1)
        assert not session.has_selector("//p//a", text=re.compile("Red$"))
