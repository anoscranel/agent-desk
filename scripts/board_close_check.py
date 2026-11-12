#!/usr/bin/env python3
"""
board_close_check.py — the gate the desk did not have.

Run before an op declares itself done. It answers, mechanically, the four
questions findings/03-CONFORMANCE measured the desk failing:

  1. Is every card in the op carrying a state the schema defines?
  2. Is every card a state other than `running`?  (a card left running is a lie)
  3. Does every card have an assignee?
  4. Does the op report name a validation artifact?  (law 6: independent validator)

Exit 0 = the op may close. Exit 1 = it may not, and the reason is printed.

    python3 board_close_check.py <op-dir>
    python3 board_close_check.py <op-dir> --json

It never edits anything. It is deliberately able to FAIL — a check that
cannot fail is a defect (see the v1.3.0 lesson in the public repo).
"""
import json
import os
import re
import sys

VALID = {"queued", "running", "blocked", "done", "failed", "cancelled"}
CLOSED = {"done", "failed", "cancelled"}
KEY = re.compile(r"^([a-z_]+):\s*(.*)$")
REPORT = re.compile(r"^(REPORT|report|99-CAPSTONE|05-CAPSTONE|99-capstone).*\.md$")
# words that indicate a validation artifact exists in the op's own report
VALIDATION = re.compile(
    r"independent audit|auditor|validator|verdict|PASS\s*/\s*FAIL|re-derived|re-derive",
    re.IGNORECASE,
)
# A keyword match is not evidence: a report can say "no independent audit was
# performed" and satisfy a bare alternation. That disclaimer is the *absence* of
# the artifact the gate exists to require, so negation near the keyword must
# reject it. (Caught by an independent reviewer, 2026-11-12.)
NEGATION = re.compile(
    r"\b(no|not|never|without|none|absent|missing|lack(?:s|ed)?|did\s+not|"
    r"was\s+not|were\s+not|has\s+not|have\s+not)\b[^.\n]{0,40}",
    re.IGNORECASE,
)


def has_real_validation(text):
    """True only if a validation artifact is asserted, not disclaimed."""
    for m in VALIDATION.finditer(text):
        start = max(0, m.start() - 60)
        window = text[start:m.start()]
        # a negation immediately before the keyword kills the match
        if NEGATION.search(window):
            continue
        return True
    return False


def frontmatter(path):
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
                    fm[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    except OSError:
        return None
    return fm


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    op = sys.argv[1].rstrip("/")
    as_json = "--json" in sys.argv

    if not os.path.isdir(op):
        print(f"FAIL  op directory does not exist: {op}")
        sys.exit(1)

    cards = []
    for dirpath, _d, files in os.walk(op):
        for f in files:
            if re.fullmatch(r"job-[0-9]+\.md", f):
                cards.append(os.path.join(dirpath, f))

    problems = []
    states = {}
    for c in cards:
        fm = frontmatter(c)
        rel = os.path.relpath(c, op)
        if fm is None:
            problems.append(("no-frontmatter", rel, "card has no readable frontmatter block"))
            continue
        st = fm.get("status", "?")
        states[st] = states.get(st, 0) + 1
        if st not in VALID:
            problems.append(("invalid-state", rel, f"status={st!r} is not in {sorted(VALID)}"))
        elif st not in CLOSED:
            problems.append(("not-closed", rel, f"status={st!r} — a card left running/queued is a lie"))
        if not fm.get("assignee"):
            problems.append(("no-assignee", rel, "card names no assignee"))

    # validation artifact in the op's own report
    have_validation = False
    for f in sorted(os.listdir(op)):
        if REPORT.match(f):
            try:
                text = open(os.path.join(op, f), encoding="utf-8", errors="replace").read()
            except OSError:
                continue
            if has_real_validation(text):
                have_validation = True
                break
    if not have_validation:
        problems.append(("no-validation-artifact", "(op root)",
                         "no report names an audit/validator/verdict — law 6 has no trace"))

    # Zero-card guard MUST run before any early return, or `--json` (a documented
    # invocation) green-lights a mistyped path. (Independent review, 2026-11-12.)
    if not cards:
        problems.append(("no-cards", "(op root)",
                         "no job-NNN.md cards found — check the path is the op directory"))

    if as_json:
        print(json.dumps({"op": op, "cards": len(cards), "states": states,
                          "problems": problems, "may_close": not problems}, indent=2))
        return 0 if not problems else 1

    print(f"op: {op}")
    print(f"cards: {len(cards)}   states: {states}")

    if not problems:
        print("\nOK — this op may close. Every card is closed, named and in-schema,")
        print("     and the report carries a validation artifact.")
        return 0

    print(f"\nBLOCKED — {len(problems)} problem(s):")
    for kind, where, why in problems:
        print(f"  [{kind}] {where}: {why}")
    print("\nFix or explain each; then re-run. Do not close on a lie.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
