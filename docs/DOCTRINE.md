---
topic: agent operation desks — distilled doctrine
status: verified
version: 1.0.0
---

# Agent Desk Doctrine

How to run a multi-step job as a one-human desk, and what to enforce in the
harness. Every claim cites its source cycle; the underlying private corpus
stays private by design.

## The one-paragraph version

The proven minimal architecture is five parts:

1. A file board — one markdown card per job with frontmatter state, one
   dispatcher polling. Disk is the checkpoint; git is the audit trail.
2. A two-tier split — a frontier planner that never implements, then cheap
   sealed-context workers.
3. Graduated autonomy — documented ask→allow promotions; roll back on any
   interrupt spike.
4. Verbatim constraint handoff — restated at every hop, because summaries
   leak ~54% of forbidden actions.
5. Deterministic pre-execution gates with an independent validator. Never a
   worker self-check or an LLM judge.

## The laws (evidence-backed, in order of cost if violated)

1. **The file board is the spine.** Markdown tasks + a polling dispatcher beat
   message brokers; the disk is the checkpoint, `grep` is the observability.
   A card left `running` is a lie the next session believes.
2. **Two tiers, shallow depth.** A frontier planner that never implements,
   then parallel cheap workers; keep pipeline depth ≤ 4, because each extra
   stage adds ~0.9 corrupted-downstream stages.
3. **Constraints travel verbatim; trajectories travel asymmetrically.**
   Restate must/forbidden rules at every hop. A compression step deactivates
   about 100% of must-do rules and leaks 54% of forbidden actions; explicit
   verbatim restatement cuts leakage from 73% to under 15%.
4. **Verification first.** Verification gaps and task incompleteness dominate
   production failures, not inter-agent misalignment. Budget for it.
5. **Validators are independent, gates are deterministic, skills are vetted.**
   A worker self-check doesn't count; an LLM judge can be gamed (one study:
   100% "pass" against 68% verifiable truth). Skills from public registries
   need a gate: one scan found 157 malicious skills.
6. **Delete coordination layers unless they prove their worth.** A
   merge-integrator added more bottlenecks than it solved.
7. **Cost-normalize everything, and self-instrument.** No public benchmark
   measures human minutes, multi-day durability or cost-per-verified-outcome.
   Keep a per-task ledger; compute leverage weekly.
8. **Cost-normalize everything, and self-instrument.** See law 7's canonical
text and law 5's verification emphasis.
9. **Phone-class caps bind first.** On mobile/constrained hardware, allow at
   most 1 dispatcher + 2 workers; errors double under sustained load; file
   checkpoints are mandatory because the OS kills processes.
10. **Money is never autonomous.** Order placement, key rotation, and the
    kill-switch stay human. No LLM-trader alpha survives friction accounting,
    and every live institutional deployment caps agents below order entry.
11. **Autonomy graduates on evidence and rolls back on signal.** Start at
    ask-level; promote on a clean streak (≈10 runs); demote on any unapproved
    irreversible attempt. Regulation documents the criteria.
12. **An audit only validates the era it looked at.** Permissions and plugins
    drift. Re-check the resolved rule set after any config change.
13. **A gate that looks green but fails silent is worse than no gate.**
    Measure the false-green path explicitly (once: an autosync reported
    "Synced" for 12 days while nothing left the device).
14. **Irreversibility has two classes.** The physical kind (a push, a spend, a
    delete) is obvious. The record kind (a committed report, a published
    claim) is reversible in the world but irreversible in the audit trail.
    Gate the second one just as hard: divergence detection, single writer,
    one named owner for shared identifiers.
15. **A gate may never speak the language of the outcome.** No artifact may
    call a chain "compliant" or a protection "adequate". A deterministic gate
    constrains one step, and calling it the outcome is the failure mode.

## What humans keep forever

- Approvals on irreversible actions (Class P).
- Money and order execution.
- Judgment where no verifiable gate exists.
- Legal accountability.

The desk compresses the human into a ~13:1 exception queue; the instruction
manual to keep that queue is `docs/HARDENING.md`.
