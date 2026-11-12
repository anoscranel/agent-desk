#!/usr/bin/env bash
# check-release.sh — verify this repository's own claims against its own bytes.
#
# The desk doctrine says: verify what your harness actually enforces, never
# what a document promises. This script applies that rule to the repository
# itself. Every check below re-derives a claim from disk. Exit 0 = all claims
# hold. Exit 1 = at least one claim is false today.
#
# Read-only. No network. Needs bash (uses process substitution), plus grep,
# awk, find and wc. Nothing else.
#
#   ./scripts/check-release.sh            # run all checks
#   ./scripts/check-release.sh --quiet    # only failures
#
set -u

cd "$(dirname "$0")/.." || exit 1
QUIET=0
[ "${1:-}" = "--quiet" ] && QUIET=1

fails=0
checks=0
skips=0

ok()   { checks=$((checks+1)); [ "$QUIET" -eq 1 ] || printf 'PASS  %s\n' "$1"; }
skip() { skips=$((skips+1)); printf 'SKIP  %s\n        %s\n' "$1" "$2"; }
bad()  { checks=$((checks+1)); fails=$((fails+1)); printf 'FAIL  %s\n        %s\n' "$1" "$2"; }

# --- 1. The files the README promises actually exist -----------------------
for f in agent-desk.md README.md LICENSE CHANGELOG.md SECURITY.md \
         docs/DOCTRINE.md docs/HARDENING.md docs/AUDIT.md \
         templates/job-NNN.md templates/LEDGER.md \
         scripts/check-release.sh scripts/board_lint.py scripts/board_close_check.py; do
    if [ -f "$f" ]; then ok "exists: $f"; else bad "exists: $f" "README promises this file; it is missing"; fi
done

# --- 2. Every pointer inside agent-desk.md resolves ------------------------
# The prompt names files it tells the agent to read. A dangling pointer means
# the desk starts work with a rule it cannot load.
n=0
while IFS= read -r p; do
    n=$((n+1))
    if [ -e "$p" ]; then ok "pointer resolves: $p"; else bad "pointer resolves: $p" "agent-desk.md references a path that does not exist"; fi
done < <(grep -oE '(docs|templates)/[A-Za-z0-9._-]+\.md' agent-desk.md | sort -u)
[ "$n" -gt 0 ] || bad "pointers present" "no docs/ or templates/ pointer found in agent-desk.md — check the grep pattern"

# --- 3. The doctrine's law count is true ----------------------------------
# Count only the law list: between the laws heading and the next heading.
laws=$(awk '/^## The laws/{f=1;next} /^## /{f=0} f && /^[0-9]+\. /' docs/DOCTRINE.md | wc -l | tr -d ' ')
if [ "$laws" -eq 15 ]; then ok "doctrine: 15 laws"; else bad "doctrine: 15 laws" "counted $laws law lines in docs/DOCTRINE.md — README and DOCTRINE both say 15"; fi

# --- 4. Every cited arXiv ID is well-formed -------------------------------
# Extract LOOSELY (anything arXiv-ish), then validate shape. Extracting with
# the strict pattern would make this check a tautology: -o only emits strings
# that already match, so malformed IDs would be invisible and the check could
# never fail. (Regression guard from an independent review, 2026-11-11.)
total_ids=$(grep -oE 'arXiv:[^ )"`]*' docs/DOCTRINE.md agent-desk.md README.md 2>/dev/null | wc -l | tr -d ' ')
shape_ids=$(grep -ohE 'arXiv:[0-9]{4}\.[0-9]{4,5}(v[0-9]+)?|arXiv:[a-z-]+(\.[A-Z]{2})?/[0-9]{7}' docs/DOCTRINE.md agent-desk.md README.md 2>/dev/null | wc -l | tr -d ' ')
if [ "$total_ids" -eq "$shape_ids" ] && [ "$total_ids" -gt 0 ]; then
    ok "arXiv IDs well-formed ($total_ids cited)"
else
    bad "arXiv IDs well-formed" "$total_ids arXiv-ish token(s) found, only $shape_ids well-formed — a malformed ID cannot be verified by anyone"
fi
count_ids=$(grep -ohE 'arXiv:[0-9]{4}\.[0-9]{4,5}' docs/DOCTRINE.md | sort -u | wc -l | tr -d ' ')
[ "$count_ids" -ge 5 ] && ok "doctrine cites $count_ids distinct arXiv IDs" || bad "doctrine citations" "only $count_ids distinct IDs found; README claims inline citations"

# --- 5. No private paths or key shapes in the tree -----------------------
# A release must not carry the operator's own environment.
priv=$(grep -rniE '/data/data/com\.termux|/storage/emulated|theta-db|keys\.env|auth\.json' \
        --include='*.md' --include='*.sh' . 2>/dev/null | grep -v '^./scripts/check-release.sh' | head -5)
if [ -z "$priv" ]; then ok "no private paths"; else bad "no private paths" "found: $(printf '%s' "$priv" | head -3)"; fi

keys=$(grep -rnE '(sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|xox[baprs]-[A-Za-z0-9-]{10,})' \
        --include='*.md' --include='*.sh' . 2>/dev/null | head -3)
if [ -z "$keys" ]; then ok "no key-shaped strings"; else bad "no key-shaped strings" "possible secret: $(printf '%s' "$keys" | head -2)"; fi

# --- 6. No dangling "no X" claim: the no-caps default really is gone ------
# CHANGELOG 1.1.1 claims the uncapped default was removed. Verify the bytes.
hits=$(grep -rniE 'no budget or retry caps|ceilings do not exist' --include='*.md' . 2>/dev/null \
        | grep -v 'CHANGELOG.md' | head -3)
if [ -z "$hits" ]; then ok "no uncapped-spend default remains"; else bad "no uncapped-spend default remains" "still present: $hits"; fi

# --- 7. CHANGELOG's newest version matches the DOCTRINE frontmatter ------
cl=$(grep -m1 -oE '^## [0-9]+\.[0-9]+\.[0-9]+' CHANGELOG.md | awk '{print $2}')
dv=$(grep -m1 -E '^version:' docs/DOCTRINE.md | awk '{print $2}')
if [ -n "$cl" ] && [ "$cl" = "$dv" ]; then ok "version consistent: $cl across CHANGELOG and DOCTRINE"
else bad "version consistent" "CHANGELOG says '${cl:-none}', DOCTRINE says '${dv:-none}'"; fi

# --- 8. Templates keep the state vocabulary the prompt requires ----------
for state in queued running done failed cancelled; do
    grep -q "$state" templates/job-NNN.md && ok "template state: $state" || bad "template state: $state" "job-NNN.md does not name this state; the prompt makes cards carry one"
done

# --- 9. The Windsurf size claim still fits the real cap ------------------
# README says the rule file cap is 12,000 characters and agent-desk.md fits.
chars=$(wc -m < agent-desk.md | tr -d ' ')
if [ "$chars" -lt 12000 ]; then ok "agent-desk.md fits the 12,000-char rule-file cap ($chars chars)"; else bad "agent-desk.md size" "$chars chars exceeds the documented 12,000 cap"; fi

# --- 10. The board tools know no home directory -------------------------
# They ship to strangers. A hardcoded /home/<user> or /storage path makes them
# somebody else's tool, not a tool.
hardcoded=$(grep -nE '/(home|Users)/[a-z]|/storage/emulated' scripts/board_lint.py scripts/board_close_check.py 2>/dev/null | head -3)
if [ -z "$hardcoded" ]; then ok "board tools carry no home-directory paths"
else bad "board tools carry no home-directory paths" "found: $hardcoded"; fi

# --- 11. The board tools run, and can fail ------------------------------
# A tool that only ever succeeds is decoration. Run each against a throwaway
# tree with a deliberate defect and require a non-zero exit.
#
# This check is only evidence if it actually RAN. A skip prints SKIP and is not
# counted among passing checks — a PASS for work not done is the exact defect
# class this script exists to catch. (Independent review, 2026-11-12.)
if command -v python3 >/dev/null 2>&1; then
    T=$(mktemp -d 2>/dev/null || true)
    if [ -z "${T:-}" ] || [ ! -d "${T:-/nonexistent}" ]; then
        skip "board_close_check rejects a bad op" "no temp dir available; nothing was verified"
    else
        mkdir -p "$T/ops/bad"
        printf -- '---\nstatus: completed\n---\n' > "$T/ops/bad/job-001.md"
        rc=0
        python3 scripts/board_close_check.py "$T/ops/bad" >/dev/null 2>&1 || rc=$?
        if [ "$rc" -eq 1 ]; then
            ok "board_close_check rejects a bad op (exit 1)"
        elif [ "$rc" -eq 2 ]; then
            bad "board_close_check rejects a bad op" "exit 2 (usage error): the tool could not evaluate the tree"
        else
            bad "board_close_check rejects a bad op" "exited $rc on a card with status 'completed'"
        fi
        rm -f "$T/ops/bad/job-001.md"
        rmdir "$T/ops/bad" "$T/ops" "$T" 2>/dev/null || true
    fi
else
    skip "board_close_check rejects a bad op" "python3 not installed; nothing was verified"
fi

# --- summary -------------------------------------------------------------
echo
if [ "$fails" -eq 0 ]; then
    printf 'OK — %d checks passed' "$checks"
    [ "$skips" -gt 0 ] && printf ', %d skipped (not counted as passing)' "$skips"
    printf '. Every claim this repository makes about itself holds today.\n'
    exit 0
else
    printf 'FAILED — %d of %d checks (%d skipped). Fix the claims or fix the bytes; do not ship both.\n' "$fails" "$checks" "$skips"
    exit 1
fi
