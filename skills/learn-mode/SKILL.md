---
name: learn-mode
description: One-time setup that turns a repo into a learn-while-you-build project. Reads the repo (README, CLAUDE.md, spec/plan docs, manifests, source layout), works out the stack and the concepts the owner will meet, then writes repo-specific teaching rules to `.claude/learning.md` with a short pointer block in the repo's CLAUDE.md. Use when the user runs /learn-mode, or says "set up learning mode", "I want to learn while I vibe code this", "make Claude teach me in this repo", "add learning rules to this project". Run once per repo; on a repo that already has the section, refresh it instead of duplicating. Not for logging concepts (/learn-log) or reviewing them (/learn-review).
---

# Learn mode

The owner vibe codes and wants to come out understanding what was built.
This skill writes rules into the repo (a short block in CLAUDE.md, the detail
in `.claude/learning.md`) so that **every later session** teaches as it builds. The rules must be specific to this repo:
real concepts, real files, real stages. Generic advice is useless here.

Part of the learn-while-build plugin: `/learn-log` saves concepts at the end
of a session, `/learn-review` teaches and quizzes them on a spaced schedule.
The `<!-- learn-mode -->` marker this skill writes is what turns on the
"concepts due" nudge at session start in this repo.

## Steps

### 1. Read the repo (read-only, keep it quick)

Read, if present: `CLAUDE.md`, `README*`, any spec/plan/design doc
(`SPEC.md`, `PLAN.md`, `docs/`), manifests (`package.json`,
`pyproject.toml`, `Cargo.toml`, `go.mod`, `pubspec.yaml`, etc.), and
`git log --oneline -15`. List the top two levels of the tree. Open a few
core source files only if code exists.

Work out:
- **Stack**: languages, frameworks, key libraries.
- **Stage**: design-only, early build, or mature codebase.
- **Build order**: if a doc lists stages/milestones, note the reference (e.g. `SPEC.md §14`).
- **Concepts**: the 8–15 ideas the owner will actually meet in *this*
  project, mapped to the stage or file where each shows up. Name them
  concretely ("delta time in the render loop", not "game programming").
- **Owner rules already in CLAUDE.md** (style, approval gates, no-go
  areas). The learning rules must fit around them, never contradict them.

### 2. Show the draft, wait for a yes

Show the user both files from step 3 filled in, plus a 2–3 line note on
what you inferred (stack, stage, any conflict with existing rules and how
you resolved it). Ask one question only if something truly can't be
inferred, such as which concepts they already know. Write nothing until
they approve.

### 3. Write it

CLAUDE.md loads into every session, so keep the learning block there
**short (about 6 lines)**. Everything else goes in `.claude/learning.md`, which
Claude reads only when it starts a stage. Don't link it with an `@` import:
imports also load every session.

**a. `CLAUDE.md`**: append (create the file if missing). If a
`## Learning mode` section already exists, replace that whole section,
including any old concepts or knobs tables in it (they move to file b).

```markdown
## Learning mode
<!-- learn-mode -->
The owner is learning <stack, a few words> while building this. Before
starting or pitching a stage, read `.claude/learning.md` and name the 1–3
concepts the stage uses. Leave one `TODO(owner)` piece per stage, and
remind the owner to run `/learn-log` at the end of a stage or session.
```

**b. `.claude/learning.md`**: create or overwrite. Filled in from step 1;
drop any line that doesn't apply:

```markdown
# Learning mode

The owner knows <what they know> but not <what's new>. Teach as you build;
don't slow the build down more than needed.

- **Before each stage** (<build-order reference, if any>), name the 1–3
  concepts it uses in plain words, one line each.
- **Leave one small piece per stage for the owner** (5–10 lines, marked
  `TODO(owner)`): the part that best shows the stage's core idea. Review
  what they write; explain fixes, don't silently rewrite.
- **When asked "why"**, answer with the trade-off, not just the choice.

## Concepts in this repo
| Concept | Where it shows up |
|---|---|
| <concept> | <stage or file> |
...

## Try-it-yourself knobs
- <a concrete value in this repo to tweak and what to watch for>
...
```

Rules that fit the repo's existing ones (e.g. "ship a working placeholder
behind `TODO(owner)` so the stage stays playable", or "teaching notes go in
chat, not code comments" when the repo keeps code minimal) go in file b's
rule list, not in CLAUDE.md.

### 4. Finish

Do not commit. Tell the user what changed (CLAUDE.md lines added, and the
new `.claude/learning.md`), and suggest switching the
Claude Code output style to **Learning** for this repo (offer to do it if
a settings tool is available). This skill does not build anything.
