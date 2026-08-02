#!/usr/bin/env python3

import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
PUBLIC_FILES = (
    ROOT / "README.md",
    ROOT / "docs" / "DOWNLOADS_AND_RELEASES.md",
    ROOT / "site" / "talktoai-zsec" / "index.html",
)
REPORT_PAGE = ROOT / "site" / "talktoai-report-ai" / "index.html"
PRIVACY_PAGE = ROOT / "site" / "talktoai-privacy" / "index.html"
ZSEC_PAGE = ROOT / "site" / "talktoai-zsec" / "index.html"
ZSEC_DOCS_PAGE = ROOT / "site" / "talktoai-docs-zsec" / "index.html"
RELEASE_URL = "https://github.com/ResearchForumOnline/ZSEC-Shield/releases/tag/v0.1.2"
ASSET_URLS = (
    "https://github.com/ResearchForumOnline/ZSEC-Shield/releases/download/v0.1.2/"
    "zsec-shield-0.1.2-windows-x86_64.zip",
    "https://github.com/ResearchForumOnline/ZSEC-Shield/releases/download/v0.1.2/"
    "zsec-shield-0.1.2-macos-arm64.tar.gz",
    "https://github.com/ResearchForumOnline/ZSEC-Shield/releases/download/v0.1.2/"
    "zsec-shield-0.1.2-linux-x86_64.tar.gz",
    "https://github.com/ResearchForumOnline/ZSEC-Shield/releases/download/v0.1.2/"
    "SHA256SUMS.txt",
)


class PublicReleaseLinkTests(unittest.TestCase):
    def test_public_surfaces_promote_exact_immutable_prerelease(self):
        for path in PUBLIC_FILES:
            text = path.read_text(encoding="utf-8")
            lowered = text.lower()
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertIn(RELEASE_URL, text)
                self.assertIn("prerelease", lowered)
                self.assertIn("immutable", lowered)
                self.assertIn("unsigned", lowered)

    def test_public_surfaces_use_exact_asset_urls(self):
        for path in PUBLIC_FILES:
            text = path.read_text(encoding="utf-8")
            for url in ASSET_URLS:
                with self.subTest(path=path.relative_to(ROOT), url=url):
                    self.assertIn(url, text)

    def test_report_ai_page_uses_email_without_inventing_a_backend(self):
        report = REPORT_PAGE.read_text(encoding="utf-8")
        zsec = ZSEC_PAGE.read_text(encoding="utf-8")
        lowered = report.lower()
        self.assertIn('rel="canonical" href="https://talktoai.org/report-ai/"', report)
        self.assertIn("mailto:shaf@talktoai.org", report)
        self.assertIn("ZERO ONE", report)
        self.assertIn("OpenZero", report)
        self.assertIn("useful evidence", lowered)
        self.assertIn("do not include secrets", lowered)
        self.assertIn("does not operate a ticketing system", lowered)
        self.assertNotIn("<form", lowered)
        self.assertIn('href="/report-ai/"', zsec)
        self.assertIn('href="/privacy"', report)

    def test_privacy_page_has_scoped_desktop_and_local_scan_disclosure(self):
        privacy = PRIVACY_PAGE.read_text(encoding="utf-8")
        lowered = privacy.lower()
        self.assertIn('rel="canonical" href="https://talktoai.org/privacy"', privacy)
        self.assertIn("Effective date: 14 June 2026", privacy)
        self.assertIn("Last revised: 2 August 2026", privacy)
        self.assertIn("ZERO ONE Desktop", privacy)
        self.assertIn("ZMail", privacy)
        self.assertIn("CallChat", privacy)
        self.assertIn("exactly one folder", lowered)
        self.assertIn("does not start a background scan", lowered)
        self.assertIn("does not upload file names, paths, hashes, samples, or reports", lowered)
        self.assertIn("camera and microphone access is disabled by default", lowered)
        self.assertIn("starts ZERO ONE automatically at sign-in", privacy)
        self.assertIn("every 30 seconds", lowered)
        self.assertIn("HTTP GET reachability request", privacy)
        self.assertIn("ZERO-ONE/&lt;version&gt;", privacy)
        self.assertIn("network IP address", privacy)
        self.assertIn("configured OpenZero endpoint", privacy)
        self.assertIn("not always local", lowered)
        self.assertIn("operating-system release", lowered)
        self.assertIn("logical-core count", lowered)
        self.assertIn("total RAM", privacy)
        self.assertIn("origin-only service destinations", lowered)
        self.assertIn("excludes the computer hostname", lowered)
        self.assertIn("URL user information (userinfo), paths, queries, and fragments are not included", privacy)
        self.assertIn("remain after uninstall", lowered)
        self.assertIn("Clear desktop data removes ZERO ONE settings", privacy)
        self.assertIn("does not delete diagnostics files", lowered)
        self.assertIn("does not mean a Microsoft Store submission", privacy)
        self.assertIn("mailto:shaf@talktoai.org", privacy)
        self.assertIn('href="/report-ai/"', privacy)
        self.assertNotIn("ZERO-ONE-Desktop", privacy)
        self.assertNotIn("zero-one-store-release", privacy)

    def test_modern_zsec_pages_preserve_truthful_security_boundaries(self):
        product = ZSEC_PAGE.read_text(encoding="utf-8")
        docs = ZSEC_DOCS_PAGE.read_text(encoding="utf-8")
        for text in (product, docs):
            lowered = text.lower()
            self.assertIn("no remote command", lowered)
            self.assertIn("unsigned", lowered)
            self.assertIn("not certified antivirus", lowered)
            self.assertIn("https://github.com/ResearchForumOnline/ZSEC", text)
            self.assertIn("https://docs.talktoai.org/zsec/", text)
            self.assertIn("og-zsec.png", text)

        self.assertIn("prefers-reduced-motion", product)
        self.assertIn("prefers-contrast", product)
        self.assertIn("zsec.feed.v1", docs)
        self.assertNotIn("Take TalkToAI Quiz", docs)
        self.assertNotIn("Start Course", docs)


if __name__ == "__main__":
    unittest.main()
