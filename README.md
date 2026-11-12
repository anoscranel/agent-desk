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
| `scripts/check-release.sh` | Verifies this repository's own claims against its own bytes. Run it after any edit. |
| `scripts/board_lint.py` | Census of your board cards: states used, assignees, frontmatter, and `running` cards split by age (abandoned vs possibly live). |
| `scripts/board_close_check.py` | The close gate: refuses to let an operation close while any card is open, unnamed, or outside the schema. |
| `LICENSE` | MIT. |

## Install

| Harness | Where the file goes | Notes |
|---|---|---|
| opencode | `~/.config/opencode/agents/agent-desk.md` (global) or `.opencode/agents/agent-desk.md` (project) | Works as shipped; restart opencode. Docs: https://opencode.ai/docs/agents/ |
| Claude Code | `.claude/agents/agent-desk.md` | Add `name: agent-desk` to the frontmatter. It runs as a subagent there, so start it from your main session. Docs: https://code.claude.com/docs/en/sub-agents |
| Cursor | `.cursor/rules/agent-desk.mdc` | Loaded as a rule, not an agent: replace the frontmatter with `description:` and `alwaysApply: false`. Cursor's agent can delegate to subagents (`.cursor/agents/`, and it also reads `.claude/agents/`), so the worker steps can run as subagents. Docs: https://cursor.com/docs/rules, https://cursor.com/docs/agent/subagents |
| Windsurf / Devin Desktop | `.devin/rules/agent-desk.md` (legacy: `.windsurf/rules/`) | Also a rule, not an agent: set `trigger: manual` and start it with `@agent-desk`. Rule files are capped at 12,000 characters (`agent-desk.md` is about 6,100 characters). Docs: https://docs.windsurf.com/plugins/cascade/memories |

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

## Check it yourself

The repository makes claims about itself — that its pointers resolve, that the doctrine
holds 15 laws, that no private path or key shape leaked into the tree. Verify them:

```sh
./scripts/check-release.sh          # prints every check; exits 1 on any false claim
```

Read-only and offline; needs only bash and core text utilities. If you edit the tree, run it
before you push; a claim and its bytes should never disagree in public.

The same script runs in CI on every push and pull request
(`.github/workflows/check.yml`, read-only), so a claim that drifts from the bytes
fails on its own.

## Check your own board

The two board tools are the mechanical half of the loop. Both are read-only and neither
has a write path. They differ in how they fail, and the difference matters:

- `board_close_check.py` **gates**: it exits 1 and names every problem when an operation
  tries to close with a card open, unnamed, out of schema, or a report whose validation
  claim is missing or explicitly disclaimed.
- `board_lint.py` **reports**: it exits 0 on a normal census, and fails (1) only when a
  root you named does not exist or a flag is malformed (2). It is a measuring instrument,
  not a gate — do not wire it as one.

```sh
python3 scripts/board_lint.py ops research     # what do your cards claim?
python3 scripts/board_lint.py --list=running   # the ones that are lies, oldest first
python3 scripts/board_close_check.py ops/<slug> # may this operation close?
```

`board_close_check.py` exits 1 and names every problem when an operation tries to close
with a card left `running`, a state outside the schema, or a report that neither names a
validation artifact nor disclaims one in the plain form the gate detects ("no independent
audit was performed" used to pass on the keyword alone). ⚠️ That detection is a heuristic,
not an understanding: it looks for a negation within ~60 characters *before* the keyword,
so "the independent audit was not performed" (negation after) still passes. The gate raises
the cost of a careless close; it does not make a dishonest one impossible. It also refuses to close an
operation that has no cards at all, which catches a mistyped path. In one desk it found 1,284 cards carrying a state the schema does not define —
across 34 distinct values, including prose written into the state field. A field every
writer fills and no reader validates always ends up like that.

## Provenance

The doctrine distils a private research corpus (19 study cycles, September
2026) and one field audit of a real setup (October 2026, summarised in
`docs/AUDIT.md`). Laws that rest on public papers cite them inline. The rest
are marked as practice, not proof.
