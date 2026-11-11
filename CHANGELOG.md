# Changelog

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
