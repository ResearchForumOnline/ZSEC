#!/usr/bin/env python3
"""Build the public ZSEC advisory feed.

The output is data-only. ZSEC clients use it to create local review TODOs;
they must never execute commands or apply policy from feed content.
"""

import argparse
import datetime
import email.utils
import html
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET

CISA_KEV_URLS = [
    "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json",
    "https://raw.githubusercontent.com/cisagov/kev-data/develop/known_exploited_vulnerabilities.json",
]
THN_RSS_URL = "https://feeds.feedburner.com/TheHackersNews"
HOME_URL = "https://talktoai.org/zsec/"

KEYWORD_TAGS = {
    "linux": ["linux", "ubuntu", "debian", "almalinux", "rocky", "rhel", "kernel", "proxmox"],
    "kernel": ["kernel"],
    "lpe": ["privilege escalation", "local privilege", "lpe"],
    "ssh": ["ssh", "openssh", "brute force", "botnet"],
    "web": ["apache", "nginx", "httpd", "php", "wordpress", "web server", "cwp", "panel"],
    "ai-exposure": ["ai", "ollama", "jupyter", "gradio", "open webui", "llm", "model context protocol", "mcp"],
    "ransomware": ["ransomware", "extortion"],
    "rce": ["remote code execution", "rce", "command injection"],
    "credential": ["credential", "password", "token", "secret", "ssh key"],
}


def utc_now():
    return datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fetch_text(url, timeout=25):
    request = urllib.request.Request(url, headers={"User-Agent": "ZSEC-FeedBuilder/1.0"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", "replace")


def clean_text(value, limit=520):
    value = html.unescape(value or "")
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    if len(value) > limit:
        return value[: limit - 1].rstrip() + "..."
    return value


def tags_for_text(*values):
    blob = " ".join(value or "" for value in values).lower()
    tags = set()
    for tag, words in KEYWORD_TAGS.items():
        if any(word in blob for word in words):
            tags.add(tag)
    if "cve-" in blob:
        tags.add("cve")
    return sorted(tags)


def severity_for_text(*values):
    blob = " ".join(value or "" for value in values).lower()
    if any(word in blob for word in ["actively exploited", "known exploited", "rce", "remote code execution", "kernel", "openssh"]):
        return "high"
    if any(word in blob for word in ["ransomware", "botnet", "privilege escalation", "credential"]):
        return "high"
    if any(word in blob for word in ["linux", "ssh", "apache", "nginx", "php", "ai"]):
        return "medium"
    return "info"


def parse_rss_date(value):
    if not value:
        return ""
    try:
        dt = email.utils.parsedate_to_datetime(value)
        if dt.tzinfo:
            dt = dt.astimezone(datetime.timezone.utc).replace(tzinfo=None)
        return dt.date().isoformat()
    except Exception:
        return clean_text(value, 64)


def build_cisa_items(limit):
    last_error = None
    data = None
    source_url = None
    for url in CISA_KEV_URLS:
        try:
            data = json.loads(fetch_text(url))
            source_url = url
            break
        except Exception as exc:
            last_error = exc
    if data is None:
        return [], {"name": "CISA KEV", "url": CISA_KEV_URLS[0], "status": "error", "error": str(last_error)}

    vulns = data.get("vulnerabilities") or []
    vulns = sorted(vulns, key=lambda row: row.get("dateAdded", ""), reverse=True)
    items = []
    for vuln in vulns[:limit]:
        cve = clean_text(vuln.get("cveID"), 64)
        vendor = clean_text(vuln.get("vendorProject"), 120)
        product = clean_text(vuln.get("product"), 160)
        name = clean_text(vuln.get("vulnerabilityName"), 220)
        notes = clean_text(vuln.get("notes"), 280)
        action = "Apply vendor security updates if this product is present. ZSEC clients may only auto-apply OS security packages; this feed creates a review TODO."
        title = " ".join(part for part in [vendor, product, name] if part)
        tags = sorted(set(["cisa-kev", "known-exploited"] + tags_for_text(vendor, product, name, notes)))
        items.append({
            "id": "cisa-kev:%s" % cve,
            "kind": "vulnerability",
            "severity": "high",
            "title": title or cve,
            "summary": notes or clean_text(vuln.get("shortDescription"), 280),
            "published": clean_text(vuln.get("dateAdded"), 32),
            "cves": [cve] if cve else [],
            "affected": {
                "vendors": [vendor] if vendor else [],
                "products": [product] if product else [],
                "keywords": tags,
            },
            "tags": tags,
            "source": {
                "name": "CISA Known Exploited Vulnerabilities Catalog",
                "url": source_url,
            },
            "zsec_action": action,
        })
    return items, {"name": "CISA KEV", "url": source_url, "status": "ok", "items": len(items)}


def build_thn_items(limit):
    try:
        text = fetch_text(THN_RSS_URL)
        root = ET.fromstring(text)
    except Exception as exc:
        return [], {"name": "The Hacker News RSS", "url": THN_RSS_URL, "status": "error", "error": str(exc)}

    items = []
    for node in root.findall("./channel/item")[:limit]:
        title = clean_text(node.findtext("title"), 180)
        link = clean_text(node.findtext("link"), 260)
        summary = clean_text(node.findtext("description"), 360)
        published = parse_rss_date(node.findtext("pubDate"))
        tags = sorted(set(["news", "the-hacker-news"] + tags_for_text(title, summary)))
        if not set(tags).intersection({"linux", "kernel", "ssh", "web", "ai-exposure", "rce", "credential", "ransomware"}):
            continue
        items.append({
            "id": "thn:%s" % re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:90],
            "kind": "news",
            "severity": severity_for_text(title, summary),
            "title": title,
            "summary": summary,
            "published": published,
            "affected": {
                "vendors": [],
                "products": [],
                "keywords": tags,
            },
            "tags": tags,
            "source": {
                "name": "The Hacker News",
                "url": link or THN_RSS_URL,
            },
            "zsec_action": "Review exposure and patch through normal vendor/security channels. ZSEC will not execute actions from news items.",
        })
    return items, {"name": "The Hacker News RSS", "url": THN_RSS_URL, "status": "ok", "items": len(items)}


def static_zsec_items():
    return [
        {
            "id": "zsec:public-ai-dev-port-review",
            "kind": "zsec-todo",
            "severity": "high",
            "title": "Review public AI and development service ports",
            "summary": "Attackers and automated scanners target exposed dashboards, notebooks, model servers, and development ports.",
            "published": datetime.date.today().isoformat(),
            "affected": {
                "vendors": [],
                "products": [],
                "keywords": ["ai-exposure", "ollama", "jupyter", "gradio", "dev service", "port 3000", "port 11434"],
            },
            "tags": ["ai-exposure", "web"],
            "source": {
                "name": "ZSEC baseline",
                "url": HOME_URL,
            },
            "zsec_action": "Run zsec check. Public AI/dev listeners should usually bind to 127.0.0.1 and sit behind nginx/Apache/auth, unless intentionally public.",
        },
        {
            "id": "zsec:ssh-botnet-watch",
            "kind": "zsec-todo",
            "severity": "high",
            "title": "Keep SSH brute-force protection active",
            "summary": "SSH brute-force and botnet activity is a constant Linux server risk.",
            "published": datetime.date.today().isoformat(),
            "affected": {
                "vendors": [],
                "products": ["OpenSSH", "fail2ban"],
                "keywords": ["ssh", "botnet", "brute force"],
            },
            "tags": ["ssh", "linux", "credential"],
            "source": {
                "name": "ZSEC baseline",
                "url": HOME_URL,
            },
            "zsec_action": "Keep fail2ban active, keep SSH keys backed up, and keep the admin IP allowlist current.",
        },
    ]


def main():
    parser = argparse.ArgumentParser(description="Build talktoai.org/zsec advisory feed")
    parser.add_argument("--output", default="site/talktoai-zsec/feed.json")
    parser.add_argument("--limit-kev", type=int, default=60)
    parser.add_argument("--limit-news", type=int, default=16)
    args = parser.parse_args()

    cisa_items, cisa_source = build_cisa_items(args.limit_kev)
    thn_items, thn_source = build_thn_items(args.limit_news)
    items = static_zsec_items() + cisa_items + thn_items
    items = sorted(items, key=lambda row: row.get("published", ""), reverse=True)

    feed = {
        "schema": "zsec.feed.v1",
        "generated_at": utc_now(),
        "home_url": HOME_URL,
        "policy": {
            "remote_commands_allowed": False,
            "auto_update_scope": "OS security packages only",
            "client_behavior": "Create local TODOs and warnings only.",
        },
        "sources": [cisa_source, thn_source],
        "items": items,
    }

    with open(args.output, "w", encoding="utf-8") as fh:
        json.dump(feed, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print("wrote %s with %d items" % (args.output, len(items)))


if __name__ == "__main__":
    main()
