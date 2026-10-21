# Hardening guide

What the permission layer actually enforces, and how to prove it. These
notes are from a 2026-10 audit of opencode 1.18.22. They may drift; re-run
the checks after each upgrade.

## The semantics you need to know

1. **Evaluation is findLast over [defaults, global, agent], in insertion
   order.** The last matching rule wins. Wildcards: `*` → `.*`, `?` → `.`,
   and a trailing `" *"` is optional.
2. **Built-in defaults come before yours.** The default `read *.env: ask`
   sits before the user's global rules. A `read: {"*": "allow"}` therefore
   silently re-opens secret files.
3. **An agent's md frontmatter `permission:` block overrides the same key in
   opencode.jsonc.** A hardening edit in the wrong file is silently ignored.
4. **Read and edit patterns match the path relative to the worktree**, so a
   deny on `/storage/...` never matches a worktree-relative path. Write
   patterns as `*/.config/secrets/*` *and* `.config/secrets/*`, or use
   worktree-relative globs.
5. **Bash rules match each command node separately** (tree-sitter). A rule
   for `git push*` does not catch `cd /repo && git push`, nor wrapper forms
   like `rtk git commit`, absolute paths (`/usr/bin/git`), `git -C`, or
   `git -c`. In one audit, a two-rule deny pair (`git commit*`, `git push*`)
   missed 58 of 106 real commit/push commands.
6. **Bash inherits `process.env`.** A `shell.env` hook can override a
   variable but cannot delete it. Count the secret names you inherit; an
   `ask`/`deny` list cannot hide a value.
7. **A blocklist on `bash: "*": "allow"` is a tripwire, not a wall.** Any
   interpreter (`python3 -c`, `node -e`, `sh -c`) can read every file the
   user can. Use an allowlist for roles you claim are "read-only".

## How to check a config without loading it

Run the real binary in an isolated sandbox pointed at scratch dirs:

```sh
S=/tmp/opencode-probe
mkdir -p $S/cfg/opencode $S/data $S/state $S/cache $S/work
# copy the global permission block into $S/cfg/opencode/opencode.json, and
# any agent md frontmatter into $S/cfg/opencode/agents/<name>.md
cd $S/work
XDG_CONFIG_HOME=$S/cfg XDG_DATA_HOME=$S/data XDG_STATE_HOME=$S/state \
  XDG_CACHE_HOME=$S/cache OPENCODE_DISABLE_AUTOUPDATE=1 \
  opencode debug agent <name> --pure
```

The output is the resolved rule list in the order findLast sees it. Then
score your own fixtures. If you use a script, delete `BUN_BE_BUN` from the
child environment. Then evaluate each fixture under two orderings (findLast
and longest-match) so the result does not depend on an internal code path.

## The limitations that remain

- Installing a plugin counts as an edit to the config directory; the config
  and the plugins are both live code, so anyone who can edit either can
  bypass permissions.
- An agent with a network fetch tool can read any URL; a private-data leak
  via a fetch URL is not visible in the permission layer.
- Without an OS-level boundary (a different uid, chroot, or container), no
  permission overlay stops a determined interpreter inside the same user's
  shell.
