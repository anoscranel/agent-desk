#!/usr/bin/env python3
"""
board_lint.py — count what the boards claim about themselves.

Read-only. Never edits a card; a card is another session's record and only its
owner (or theta) may rewrite it. This tool's job is to make the lie visible.

    python3 board_lint.py                     # summary over ./ops and ./research
    python3 board_lint.py path/to/ops path/to/research
    python3 board_lint.py --list=running      # list the stale running cards
    python3 board_lint.py --aged=7            # running cards untouched for N+ days
    python3 board_lint.py --json --aged=7

Why age matters: a card written an hour ago and still `running` is a live session
doing work. A card untouched for a month is an abandoned op. The first is normal;
the second is the lie the prompt warns about. Only age separates them.

Why it exists: the live desk prompt says "a card left `running` is a lie the
next session believes". Measured 2026-11-11: 373 such cards. A rule with no
mechanism is a hope.
"""
import json
import os
import re
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone

def parse_args(argv):
    """Split argv into (roots, opts). Handles `--aged=3`, `--aged 3`, `--list`,
    `--list=running`, `--json`. Never silently swallows a value."""
    roots, opts, i = [], {}, 0
    while i < len(argv):
        a = argv[i]
        if a.startswith("--"):
            if "=" in a:
                k, v = a[2:].split("=", 1)
                opts[k] = v
            elif a in ("--json",):
                opts[a[2:]] = True
            elif i + 1 < len(argv) and not argv[i + 1].startswith("-"):
                opts[a[2:]] = argv[i + 1]
                i += 1
            else:
                opts[a[2:]] = True
        else:
            roots.append(a)
        i += 1
    return (roots or ["ops", "research"]), opts


ROOTS, OPTS = parse_args(sys.argv[1:])
VALID = {"queued", "running", "blocked", "done", "failed", "cancelled"}
FM = re.compile(r"^---\s*$")
KEY = re.compile(r"^([a-z_]+):\s*(.*)$")


def cards():
    for root in ROOTS:
        if not os.path.isdir(root):
            continue
        for dirpath, _dirnames, filenames in os.walk(root):
            for fn in filenames:
                if re.fullmatch(r"job-[0-9]+\.md", fn) or re.fullmatch(r"job-[0-9]+\.markdown", fn):
                    yield os.path.join(dirpath, fn)


def frontmatter(path):
    """Read only the frontmatter block; never the whole file."""
    fm = {}
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            if fh.readline().strip() != "---":
                return None
            for _ in range(40):
                line = fh.readline()
                if not line or line.strip() == "---":
                    break
                m = KEY.match(line.strip())
                if m:
                    fm[m.group(1)] = m.group(2).strip()
    except OSError:
        return None
    return fm


def main():
    # A census over zero roots or a missing root must fail loudly, not print 0.
    for r in ROOTS:
        if not os.path.isdir(r):
            print(f"FAIL  root does not exist: {r}")
            return 1

    as_json = OPTS.get("json") is True
    listing = OPTS.get("list") or None
    if listing is True:
        listing = "running"

    states = Counter()
    by_state = defaultdict(list)
    no_fm = []
    bad_state = []
    no_assignee = 0
    total = 0

    for path in cards():
        total += 1
        fm = frontmatter(path)
        if fm is None:
            no_fm.append(path)
            continue
        st = (fm.get("status") or "").strip().strip('"').strip("'")
        if not st:
            no_fm.append(path)
            continue
        states[st] += 1
        by_state[st].append(path)
        if st not in VALID:
            bad_state.append((path, st))
        if not fm.get("assignee"):
            no_assignee += 1

    if as_json:
        print(json.dumps({
            "total_cards": total,
            "by_state": dict(states),
            "cards_without_frontmatter": len(no_fm),
            "invalid_states": bad_state[:50],
            "cards_without_assignee": no_assignee,
        }, indent=2))
        return

    print(f"cards found: {total}")
    print("\nby state:")
    for st, n in states.most_common():
        flag = "" if st in VALID else "   <-- NOT A VALID STATE"
        print(f"  {st:12} {n:5}{flag}")
    print(f"\nno/unreadable frontmatter: {len(no_fm)}")
    print(f"invalid state values:      {len(bad_state)}")
    print(f"cards with no assignee:    {no_assignee}")

    run = len(by_state.get("running", []))
    pct = (100.0 * run / total) if total else 0
    print(f"\n'running' CARDS: {run}  ({pct:.1f}% of all cards)")

    # age matters: a fresh running card is a live session; an old one is abandoned work
    raw = OPTS.get("aged", 7)
    if raw is True or not str(raw).isdigit():
        print(f"FAIL  --aged needs a whole number of days, got {raw!r}")
        return 2
    aged_days = int(raw)
    if aged_days is None:
        aged_days = 7
    now = time.time()
    stale, fresh = [], []
    for p in by_state.get("running", []):
        try:
            age = (now - os.path.getmtime(p)) / 86400.0
        except OSError:
            continue
        (stale if age >= aged_days else fresh).append((p, age))
    print(f"  of those, untouched {aged_days}+ days (abandoned): {len(stale)}")
    print(f"  untouched under {aged_days} days (possibly live):  {len(fresh)}")
    print("  THIS TOOL DOES NOT FIX THEM: a card belongs to the session that opened it.")

    if listing:
        print(f"\n--- cards with status={listing} (oldest first) ---")
        pool = []
        for p in by_state.get(listing, []):
            try:
                pool.append(((now - os.path.getmtime(p)) / 86400.0, p))
            except OSError:
                pool.append((0.0, p))
        for age, p in sorted(pool, reverse=True):
            print(f"  {age:6.1f}d  {p}")

    if bad_state:
        print("\n--- invalid states (top 20) ---")
        for p, st in bad_state[:20]:
            print(f"  {st!r:30} {p}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
