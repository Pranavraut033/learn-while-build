---
name: learn-mode
description: One-time setup that turns a repo into a learn-while-you-build project. Reads the repo (README, CLAUDE.md, spec/plan docs, manifests, source layout), works out the stack and the concepts the owner will meet, then adds a repo-specific "Learning mode" section to the repo's CLAUDE.md. Use when the user runs /learn-mode, or says "set up learning mode", "I want to learn while I vibe code this", "make Claude teach me in this repo", "add learning rules to this project". Run once per repo; on a repo that already has the section, refresh it instead of duplicating. Not for logging concepts (/learn-log) or reviewing them (/learn-review).
---

# Learn mode

The owner vibe codes and wants to come out understanding what was built.
This skill writes rules into the repo's own CLAUDE.md so that **every later
session** teaches as it builds. The rules must be specific to this repo:
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

Show the user the section from step 3 filled in, plus a 2–3 line note on
what you inferred (stack, stage, any conflict with existing rules and how
you resolved it). Ask one question only if something truly can't be
inferred, such as which concepts they already know. Write nothing until
they approve.

### 3. Write it

Append to the repo's `CLAUDE.md` (create it if missing). If a
`## Learning mode` section already exists, replace that section only.
Template, filled in from step 1; drop any line that doesn't apply:

```markdown
## Learning mode
<!-- learn-mode -->

The owner is learning <stack> while building this. Teach as you build;
don't slow the build down more than needed.

- **Before each stage** (<build-order reference, if any>), name the 1–3
  concepts it uses in plain words, one line each.
- **Leave one small piece per stage for the owner** (5–10 lines, marked
  `TODO(owner)`): the part that best shows the stage's core idea. Review
  what they write; explain fixes, don't silently rewrite.
- **At the end of a stage or session**, remind the owner to run
  `/learn-log` so the concepts get saved for review.
- **When asked "why"**, answer with the trade-off, not just the choice.
- Explain to someone who knows <what they know> but not <what's new>.

### Concepts in this repo
| Concept | Where it shows up |
|---|---|
| <concept> | <stage or file> |
...

### Try-it-yourself knobs
- <a concrete value in this repo to tweak and what to watch for>
...
```

If existing rules say to keep code/prose minimal, add one line making
clear that teaching notes go in chat, not in code comments, so the two
don't clash.

### 4. Finish

Do not commit. Tell the user what changed, and suggest switching the
Claude Code output style to **Learning** for this repo (offer to do it if
a settings tool is available). This skill does not build anything.
