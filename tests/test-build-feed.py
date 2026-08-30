#!/usr/bin/env python3

import importlib.util
import os
import pathlib
import stat
import tempfile
import unittest
from unittest import mock


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

    def test_ai_found_vulnerability_is_not_ai_exposure(self):
        tags = BUILD_FEED.tags_for_text("NodeBB patches eight AI-found vulnerabilities")
        self.assertNotIn("ai-exposure", tags)
        self.assertIn("web", tags)

    def test_jupyter_file_format_is_not_ai_exposure(self):
        tags = BUILD_FEED.tags_for_text("GitLab exploit uses a crafted Jupyter notebook")
        self.assertNotIn("ai-exposure", tags)

    def test_source_word_does_not_imply_rce_severity(self):
        severity = BUILD_FEED.severity_for_text("Open source project publishes an advisory")
        self.assertEqual("info", severity)

    def test_extortion_language_gets_ransomware_severity(self):
        severity = BUILD_FEED.severity_for_text("Attackers made an extortion demand after stealing data")
        self.assertEqual("high", severity)

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
        self.assertIn("ai-exposure", tags)
        self.assertTrue(BUILD_FEED.news_is_relevant(title, "", tags))

    def test_generic_botnet_is_not_mislabeled_as_ssh(self):
        tags = BUILD_FEED.tags_for_text("Botnet hunts exposed web services")
        self.assertIn("botnet", tags)
        self.assertNotIn("ssh", tags)

    def test_botnet_only_device_story_is_excluded(self):
        title = "Android car malware creates a proxy botnet"
        tags = BUILD_FEED.tags_for_text(title)
        self.assertEqual(["botnet"], tags)
        self.assertFalse(BUILD_FEED.news_is_relevant(title, "Vehicle head unit malware", tags))

    def test_ssh_botnet_retains_both_tags(self):
        tags = BUILD_FEED.tags_for_text("SSH botnet brute-forces OpenSSH servers")
        self.assertIn("botnet", tags)
        self.assertIn("ssh", tags)

    def test_stolen_ssh_keys_do_not_imply_ssh_service_exposure(self):
        title = "Malicious package contains credential-stealing code"
        summary = "The malware harvested cloud keys, SSH keys, and database passwords."
        tags = BUILD_FEED.news_tags_for_text(title, summary)
        self.assertIn("credential", tags)
        self.assertNotIn("ssh", tags)

    def test_linux_only_vendor_internal_story_is_excluded(self):
        title = "Bing Images flaw runs commands on Microsoft servers"
        summary = "The issue reached root on Linux machines in Microsoft's fleet."
        tags = BUILD_FEED.tags_for_text(title, summary)
        self.assertEqual(["linux"], tags)
        self.assertFalse(BUILD_FEED.news_is_relevant(title, summary, tags))

    def test_linux_titled_story_is_included(self):
        title = "Linux kernel flaw is actively exploited"
        tags = BUILD_FEED.tags_for_text(title)
        self.assertTrue(BUILD_FEED.news_is_relevant(title, "", tags))

    def test_windows_kernel_story_is_not_tagged_as_linux_or_included(self):
        title = "Microsoft patches Windows kernel driver flaw"
        tags = BUILD_FEED.tags_for_text(title)
        self.assertNotIn("linux", tags)
        self.assertIn("kernel", tags)
        self.assertFalse(BUILD_FEED.news_is_relevant(title, "", tags))

    def test_failed_required_source_preserves_existing_feed(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output = pathlib.Path(temp_dir) / "feed.json"
            output.write_text("known-good\n", encoding="utf-8")
            with mock.patch.object(BUILD_FEED, "build_cisa_items", return_value=([], {"name": "CISA KEV", "status": "error", "error": "offline"})), mock.patch.object(BUILD_FEED, "build_thn_items", return_value=([], {"name": "The Hacker News RSS", "status": "ok", "items": 0})):
                result = BUILD_FEED.main(["--output", str(output)])
            self.assertEqual(1, result)
            self.assertEqual("known-good\n", output.read_text(encoding="utf-8"))

    def test_feed_writer_uses_lf_newlines(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output = pathlib.Path(temp_dir) / "feed.json"
            BUILD_FEED.write_feed({"schema": "zsec.feed.v1", "items": []}, str(output))
            self.assertNotIn(b"\r\n", output.read_bytes())

    @unittest.skipIf(os.name == "nt", "POSIX mode semantics are not available on Windows")
    def test_feed_writer_preserves_existing_mode(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output = pathlib.Path(temp_dir) / "feed.json"
            output.write_text("known-good\n", encoding="utf-8")
            output.chmod(0o640)
            BUILD_FEED.write_feed({"schema": "zsec.feed.v1", "items": []}, str(output))
            self.assertEqual(0o640, stat.S_IMODE(output.stat().st_mode))


if __name__ == "__main__":
    unittest.main()
