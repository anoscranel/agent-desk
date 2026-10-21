---
status: verified
created: 2026-10-17
---

# agent-desk

A one-human operation desk for any harness that lets you define a primary
agent or agents file: opencode, Claude Code, Cursor, Windsurf and similar.
File-board spine, two-tier worker dispatch, verbatim briefs, independent
validation, executable harness checks, operator-gated irreversibles. The
report behind it is in `docs/DOCTRINE.md`.

# What you get

- `agent-desk.md` — the desk prompt. The frontmatter is opencode's adapter
  format (`mode: primary`, `tools: task`); other harnesses use their own
  (Claude Code: `.claude/agents/`, Cursor: `.cursor/rules/`, AGENTS.md
  convention: paste the body). The six loop steps and the constraint block
  are harness-neutral.
- `docs/DOCTRINE.md` — the 15 laws and the "what humans keep forever" limits.
- `docs/HARDENING.md` — how to verify the rules your config really enforces
  (real-binary hermetic checks).
- `docs/AUDIT.md` — a case study: how the above was measured on a real setup.
- `LICENSE` — MIT.

# How to use it

1. Create `ops/<slug>/` beside your project. Put the job cards
   (`job-NNN.md`) and `LEDGER.md` there. Add it to `.gitignore` if it's private.
2. Start the agent with the `agent-desk` prompt.
3. State the mission in one line. Mark every irreversible action explicitly.
4. Review the board (`ops/<slug>/job-*.md`), sign off on the fixes you want.
   Nothing mutates outside the board until you say so.

# What the operator must decide

1. Whether the desk needs to see your secrets at all. The desk runs on least
   privilege: deny the config and `*.env` patterns explicitly (see
   `docs/HARDENING.md`).
2. Whether subagents inherit your shell environment at all. The tool passes
   `process.env` to bash, so every secret variable you export is visible to
   every worker by default. The mitigation is process isolation, not a
   permission rule.
3. How to install and sign skills. Untrusted skills have shipped malicious
   hooks; one `SKILL.md` can run a command.

# License and provenance

Doctrine sourced from a 19-cycle research program and a 5-week audit of a real
phone-class setup (both kept private; see docs/AUDIT.md for the dashboard)
available on request. Text and templates are MIT-licensed.
