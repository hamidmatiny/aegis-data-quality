#!/usr/bin/env python3
"""Refresh dashboard.yaml from memory/review-baselines.md and memory/findings.md.

Deterministic, no network, no MCP. Replaces the LLM-driven /update-dashboard
loop that timed out on the 6-hourly schedule (2026-10-09 12:00 / 18:00 UTC).

Usage: python3 scripts/update_dashboard.py [--root DIR] [--dry-run]
Prints a one-line JSON summary of what was written.
"""
import argparse
import json
import os
import re
import sys

ENTRY_RE = re.compile(r"^- (\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z):\s*(.*)$")
SUB_RE = re.compile(r"^\s+- (Clean|Flagged):\s*(.*)$")
COUNT_RE = re.compile(r"Reviewed (\d+) reports", re.IGNORECASE)
ID_RE = re.compile(r"`([0-9a-f]{8})[0-9a-f\-\.]*`")


def parse_baselines(text):
    """Return review entries (newest first). Stops at the '# Schema Rules' section."""
    entries = []
    cur = None
    for line in text.splitlines():
        if line.startswith("# ") and "schema" in line.lower():
            break
        m = ENTRY_RE.match(line)
        if m:
            cur = {"ts": m.group(1), "head": m.group(2).strip(), "clean": None, "flagged": []}
            entries.append(cur)
            continue
        s = SUB_RE.match(line)
        if s and cur is not None:
            if s.group(1) == "Flagged":
                cur["flagged"] = sorted(set(ID_RE.findall(s.group(2)))) or ["unidentified"]
            else:
                cur["clean"] = True
    for e in entries:
        c = COUNT_RE.search(e["head"])
        if c:
            e["reviewed"] = int(c.group(1))
        else:
            ids = set(ID_RE.findall(e["head"]))
            # Never invent a count: unknown stays None and renders as an em dash.
            e["reviewed"] = len(ids) if ids else None
    entries.sort(key=lambda e: e["ts"], reverse=True)
    return entries


def count_findings(text):
    """Count escalated findings: top-level '- ' items or '## ' headings after the title."""
    n = 0
    for line in text.splitlines():
        if line.startswith("## ") or line.startswith("- "):
            n += 1
    return n


def _set_widget_value(yaml_text, label, value):
    pat = re.compile(r'(label: "%s"\n(?:\s+\w+: .*\n)*?\s+value: )".*?"' % re.escape(label))
    return pat.sub(lambda m: m.group(1) + json.dumps(value), yaml_text, count=1)


def _set_color_after_label(yaml_text, label, color):
    pat = re.compile(r'(label: "%s"\n(?:\s+\w+: .*\n)*?\s+color: )\w+' % re.escape(label))
    return pat.sub(lambda m: m.group(1) + color, yaml_text, count=1)


def render(yaml_text, entries, findings_count, max_items=5):
    if entries:
        last = entries[0]
        updated = last["ts"][:10]
        last_review = last["ts"]
        reviewed = "—" if last["reviewed"] is None else str(last["reviewed"])
        flags = str(len(last["flagged"]))
        status, status_color = "Active", "green"
    else:
        updated, last_review, reviewed, flags = None, "—", "—", "—"
        status, status_color = "Scaffolded", "yellow"

    if updated:
        yaml_text = re.sub(r'^updated: ".*?"', 'updated: "%s"' % updated, yaml_text, count=1, flags=re.M)
    yaml_text = _set_widget_value(yaml_text, "Agent Status", status)
    yaml_text = _set_color_after_label(yaml_text, "Agent Status", status_color)
    yaml_text = _set_widget_value(yaml_text, "Last Review", last_review)
    yaml_text = _set_widget_value(yaml_text, "Reports Reviewed (last run)", reviewed)
    yaml_text = _set_widget_value(yaml_text, "Flags Raised (last run)", flags)
    drift = "None" if findings_count == 0 else "%d escalated" % findings_count
    yaml_text = _set_widget_value(yaml_text, "Drift Flags", drift)
    yaml_text = _set_color_after_label(yaml_text, "Drift Flags", "green" if findings_count == 0 else "red")

    items = []
    for e in entries[:max_items]:
        verdict = "flagged " + ", ".join(e["flagged"]) if e["flagged"] else ("clean" if e["clean"] else "recorded")
        n = "?" if e["reviewed"] is None else e["reviewed"]
        items.append("%s — %s reports, %s" % (e["ts"], n, verdict))
    m = re.search(r'(title: "Recent Reviews"\n(\s+)items:)[^\n]*\n(?:\2  - .*\n)*', yaml_text)
    if m:
        indent = m.group(2)
        block = m.group(1) + (" []\n" if not items else "\n" + "".join(
            "%s  - %s\n" % (indent, json.dumps(i, ensure_ascii=False)) for i in items))
        yaml_text = yaml_text[:m.start()] + block + yaml_text[m.end():]
    return yaml_text, {"updated": updated, "last_review": last_review, "reports_reviewed": reviewed,
                       "flags_raised": flags, "findings_escalated": findings_count, "recent": len(items)}


def _read(path):
    if not os.path.exists(path):
        return ""
    with open(path, encoding="utf-8") as f:
        return f.read()


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    dash_path = os.path.join(args.root, "dashboard.yaml")
    if not os.path.exists(dash_path):
        print(json.dumps({"error": "dashboard.yaml not found", "path": dash_path}))
        return 1
    entries = parse_baselines(_read(os.path.join(args.root, "memory", "review-baselines.md")))
    findings = count_findings(_read(os.path.join(args.root, "memory", "findings.md")))
    old = _read(dash_path)
    new, summary = render(old, entries, findings)
    summary["changed"] = new != old
    if summary["changed"] and not args.dry_run:
        with open(dash_path, "w", encoding="utf-8") as f:
            f.write(new)
    print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
