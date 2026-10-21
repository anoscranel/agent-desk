---
topic: agent operation desks — distilled doctrine
version: 1.1.1
---

# Agent Desk Doctrine

How to run a multi-step job as a one-human desk, and what to enforce in the
harness. It distils a private research corpus (19 study cycles, 2026-09).
Where a law rests on a public paper, the paper is cited inline. Where it rests
on the private corpus or on one field audit, it says so. Numbers are figures
reported by their source, not guarantees for your setup.

## The architecture in five parts

1. **A file board.** One markdown card per job, with frontmatter state, and
   one dispatcher. The disk is the checkpoint and the board is the audit
   trail.
2. **A two-tier split.** A frontier planner that never implements, plus cheap
   workers that start with a fresh context.
3. **Graduated autonomy.** Write down when a task class moves from ask to
   allow. Roll back on an unapproved irreversible attempt, an error spike, or
   frequent interrupts.
4. **Verbatim constraint handoff.** Restate must and must-not rules at every
   hop.
5. **Deterministic gates with an independent validator.** Never a worker's
   self-check, and never an LLM judge as the final word.

## The laws

1. **The file board is the spine.** Markdown cards and a dispatcher beat
   message brokers for a small desk on one machine. The disk is the
   checkpoint, `grep` is the observability. A card left `running` is a lie the
   next session believes.
2. **Two tiers, shallow depth.** Keep pipeline depth to 3–4 stages. In
   controlled probes, mean cascade radius grew from 0.9 to 4.7 corrupted
   stages as depth went from 3 to 7 (OrchestraBench,
   [arXiv:2608.05263](https://arxiv.org/abs/2608.05263)).
3. **Constraints travel verbatim.** Handoff summaries erode blocking
   requirements: multihop compression deactivated 97.2% of blockers, and
   restoring the full blocker text cut forbidden actions from 85.2% to 0.0%
   ([arXiv:2608.24569](https://arxiv.org/abs/2608.24569)). Vague boundary
   language leaked in 73% of GPT cases, explicit constraints in under 15%
   ([arXiv:2608.29028](https://arxiv.org/abs/2608.29028)).
4. **Trajectories travel asymmetrically.** When escalating cheap→strong, pass
   less of the cheap model's trajectory; when downshifting, pass more. Full
   trajectory escalation recovered less than half the quality gap
   ([arXiv:2608.24358](https://arxiv.org/abs/2608.24358)).
5. **Verification first.** In the corpus's production case studies, failures
   came mostly from missing verification and incomplete tasks, not from agents
   misunderstanding each other. Budget for checking before you add agents.
6. **Validators are independent; gates are deterministic; skills are vetted.**
   Agents can game a judge: in one report, cached answer keys produced a 100%
   pass rate that concealed 68% true capability (position paper,
   [arXiv:2609.02246](https://arxiv.org/abs/2609.02246)). Of 98,380 registry
   skills, 157 were confirmed malicious
   ([arXiv:2602.06547](https://arxiv.org/abs/2602.06547)). Gate every skill
   before install.
7. **Delete coordination layers unless they prove their worth.** An extra
   integrator or mediator tier is a cost until it shows a measured gain.
8. **Cost-normalise and self-instrument.** No public benchmark measures human
   minutes, multi-day durability or cost per verified outcome. Keep a per-task
   ledger and compute leverage weekly.
9. **Constrained hardware caps the desk first.** On a phone, the OS kills
   background processes and free API tiers cap requests per day. Run one
   dispatcher and at most two workers, in batches, and checkpoint to disk.
10. **Money is never autonomous.** Orders, key rotation and kill switches stay
    human. Reported alpha from LLM trading agents is not deployment evidence
    ([arXiv:2605.16895](https://arxiv.org/abs/2605.16895)).
11. **Autonomy graduates on evidence and rolls back on signal.** Start every
    task class at ask. Promote it after a clean streak you define in writing
    (for example, 10 runs). Demote it on any unapproved irreversible attempt.
12. **An audit validates only the version it looked at.** Permissions and
    plugins drift. Re-check the resolved rules after every config change.
13. **A gate that looks green but fails silently is worse than no gate.**
    Test the false-green path on purpose. In one field audit, a sync job
    reported "synced" for 12 days while nothing left the device
    (`docs/AUDIT.md`).
14. **Irreversibility has two classes.** The physical kind (a push, a spend, a
    delete) is obvious. The record kind (a published claim, a committed
    report) can be corrected but never unpublished. Gate both. Give every
    shared identifier one named owner.
15. **A gate may not speak the language of the outcome.** No artifact may call
    a system "compliant" or a protection "adequate". A gate checks one step;
    reading it as the outcome is the failure.

## What humans keep

- Approval of irreversible actions.
- Money and order execution.
- Judgment where no verifiable gate exists.
- Legal accountability.

A well-run desk turns the human into an exception queue: you review what the
gates flag, not every step. `docs/HARDENING.md` shows how to check that your
harness actually enforces the gates the desk relies on.
