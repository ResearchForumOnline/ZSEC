#!/usr/bin/env python3

import importlib.util
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("build_feed", ROOT / "tools" / "build-feed.py")
BUILD_FEED = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILD_FEED)


class FeedClassificationTests(unittest.TestCase):
    def test_short_keywords_require_token_boundaries(self):
        tags = BUILD_FEED.tags_for_text("Ukrainian campaign gains access through a supply chain")
        self.assertNotIn("ai-exposure", tags)
        self.assertNotIn("rce", tags)

    def test_explicit_ai_and_rce_terms_are_classified(self):
        tags = BUILD_FEED.tags_for_text("Exposed AI service allows remote code execution (RCE)")
        self.assertIn("ai-exposure", tags)
        self.assertIn("rce", tags)

    def test_source_word_does_not_imply_rce_severity(self):
        severity = BUILD_FEED.severity_for_text("Open source project publishes an advisory")
        self.assertEqual("info", severity)

    def test_run_code_wording_is_rce(self):
        tags = BUILD_FEED.tags_for_text("Unauthenticated attackers can run code")
        self.assertIn("rce", tags)
        self.assertEqual("high", BUILD_FEED.severity_for_text("Unauthenticated attackers can run code"))

    def test_non_security_ai_policy_news_is_excluded(self):
        title = "Regulator issues new rules for rival AI assistants"
        tags = BUILD_FEED.tags_for_text(title)
        self.assertFalse(BUILD_FEED.news_is_relevant(title, "", tags))

    def test_exposed_ai_service_news_is_included(self):
        title = "Botnet hunts exposed AI services for cloud keys"
        tags = BUILD_FEED.tags_for_text(title)
        self.assertTrue(BUILD_FEED.news_is_relevant(title, "", tags))


if __name__ == "__main__":
    unittest.main()
