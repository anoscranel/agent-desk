# Changelog

## 1.4.0 — 2026-11-12

### Added
- `scripts/board_lint.py` — census of board cards: states in use, assignees,
  frontmatter, and `running` cards split by age (abandoned vs possibly live).
- `scripts/board_close_check.py` — the close gate. Refuses to let an operation
  close while any card is open, unnamed, or outside the schema, or while its
  report carries no validation artifact. Exits 1 and names every problem.
- `check-release.sh`: two new checks — the board tools carry no home-directory
  paths, and `board_close_check.py` is *observed* to reject a bad op (a tool that
  cannot fail is decoration).

### Changed
- README: documents both tools and adds a "Check your own board" section.
- docs/DOCTRINE.md: version bump to 1.4.0.

### Why
These tools exist because a rule with no mechanism is a hope. In the desk that
built them, 1,284 of 11,613 cards carried a state the schema does not define —
across 34 distinct values, including prose written into the state field
(`done   # verified 1790w on disk 2026-10-11`). A field every writer fills and no
reader validates always ends up like that.

## 1.3.1 — 2026-11-11

### Added
- CI: `.github/workflows/check.yml` runs `scripts/check-release.sh` on every push and
  pull request (read-only, `contents: read`, no secrets, no network). A claim that drifts
  from the bytes now fails on its own instead of waiting for someone to notice.

### Changed
- README: the "Check it yourself" section says the checker also runs in CI.
- docs/DOCTRINE.md: version bump to 1.3.1.

## 1.3.0 — 2026-11-11

### Added
- `scripts/check-release.sh` — verifies this repository's own claims against
  its own bytes: promised files exist, every pointer in the prompt resolves, the doctrine
  holds 15 laws, arXiv IDs are well-formed, no private path or key shape is in the tree,
  the uncapped-spend default stays removed, CHANGELOG and DOCTRINE versions agree, the
  job template carries every state the prompt requires, and the prompt fits the 12,000
  character rule-file cap. Read-only, offline, exit 1 on any false claim.
  Validated both ways: it passes on this tree, and planted defects (a dangling
  pointer, a short law list, a version mismatch, a private path, a key shape, a
  malformed arXiv ID) each make it exit 1.

### Changed
- README: documents the checker (what-you-get table row + a "Check it yourself" section).
- docs/DOCTRINE.md: version bump to 1.3.0.

## 1.2.0 — 2026-11-11

### Fixed
- README: Windsurf docs URL updated — the old page now redirects to the merged
  Devin Local docs and no longer states the 12,000-character rule-file cap
  (caught by an independent claims audit, 2026-11-11).

### Changed
- README: "about 6,200" → "about 6,100 characters" (the cap counts characters;
  `wc -m` on agent-desk.md gives 6,095).
- docs/DOCTRINE.md: added a distillation-date line ("as of its
  2026-10-12 amendment state"; frontmatter version 1.1.1 -> 1.2.0), applying the repo's own
  date-every-number rule to itself.

## 1.1.1 — 2026-10-22

### Fixed
- The desk and the ledger template no longer ship "no budget or retry caps" as a default. They now tell you to set a spend ceiling and a retry limit that suit your account.
- LICENSE holder name matches the author's other repos: Anos Cranel.

### Added
- CHANGELOG, SECURITY.

## 1.1.0 — 2026-10-22

Honest harness-support table, inline citations in the doctrine, templates.

## 1.0.0 — 2026-10-21

First release.
