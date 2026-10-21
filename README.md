# agent-desk

A one-human operation desk: one agent plans, fresh worker agents do the
tasks, a file board records everything, and you approve anything that cannot
be undone. It comes with the doctrine behind each rule and a guide to checking
what your harness really enforces.

Built and tested on [opencode](https://opencode.ai). Other harnesses can run
the loop where they support subagents; see the table.

## What you get

| File | What it is |
|---|---|
| `agent-desk.md` | The desk prompt (opencode agent format). |
| `templates/job-NNN.md`, `templates/LEDGER.md` | A job card and a ledger to copy into each board. |
| `docs/DOCTRINE.md` | The 15 laws, with sources. |
| `docs/HARDENING.md` | How to check which permission rules your harness actually enforces. |
| `docs/AUDIT.md` | Case study: the audit that shaped these rules. |
| `LICENSE` | MIT. |

## Install

| Harness | Where the file goes | Notes |
|---|---|---|
| opencode | `~/.config/opencode/agents/agent-desk.md` (global) or `.opencode/agents/agent-desk.md` (project) | Works as shipped; restart opencode. Docs: https://opencode.ai/docs/agents/ |
| Claude Code | `.claude/agents/agent-desk.md` | Add `name: agent-desk` to the frontmatter. It runs as a subagent there, so start it from your main session. Docs: https://code.claude.com/docs/en/sub-agents |
| Cursor | `.cursor/rules/agent-desk.mdc` | Loaded as a rule, not an agent: replace the frontmatter with `description:` and `alwaysApply: false`. Cursor has no subagent dispatch, so you run the worker steps yourself. Docs: https://cursor.com/docs/rules |
| Windsurf / Devin Desktop | `.devin/rules/agent-desk.md` (legacy: `.windsurf/rules/`) | Also a rule, not an agent, with the same limit as Cursor: set `trigger: manual` and start it with `@agent-desk`. Rule files are capped at 12,000 characters (`agent-desk.md` is about 6,200). Docs: https://docs.windsurf.com/windsurf/cascade/memories |

Copy `docs/` and `templates/` beside your project, so the prompt's pointers
resolve.

## How to use it

1. Start the desk agent and state the mission in one line.
2. The desk creates `ops/<slug>/` with job cards and a `LEDGER.md`, then
   dispatches workers one task at a time.
3. It stops and asks you before anything irreversible: pushes, deletes,
   installs, spends.
4. Review the board, not the chat. Each card names its output file and
   verdict.

## What you must decide

1. **Can the desk see your secrets?** The harness decides, not the prompt.
   Deny your config and `*.env` paths explicitly, then verify with
   `docs/HARDENING.md`.
2. **Do workers inherit your shell environment?** In opencode they do: every
   exported variable reaches every bash call. Permission rules cannot hide a
   variable's value. Run the desk from a shell without secrets, or isolate it
   (a separate user or a container).
3. **How do you install skills?** Registry skills have shipped with malicious
   hooks. Install through one gated installer, and never copy a skill in by
   hand.

## Provenance

The doctrine distils a private research corpus (19 study cycles, September
2026) and one field audit of a real setup (October 2026, summarised in
`docs/AUDIT.md`). Laws that rest on public papers cite them inline. The rest
are marked as practice, not proof.
