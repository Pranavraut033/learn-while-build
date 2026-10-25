---
name: learn-log
description: End-of-session concept log for the learn-while-build plugin. Looks at what was built in this session, drafts the concepts the owner should learn from it (each with a question and answer), and after approval saves them to the central spaced-repetition store. Run with /learn-log at the end of a session or stage.
disable-model-invocation: true
---

# Learn log

Save what this session taught, so `/learn-review` can teach and quiz it later.

The store script is `../../scripts/review.py`, relative to this skill's base
directory. Below, `review.py` means `python3 "<that path>"`.

## Steps

1. **See what happened.** Use this conversation first. Add `git status`,
   `git diff` and `git log --oneline` for commits made this session. The repo
   name is the basename of the git root (or the current folder).

2. **Pick concepts.** 1–6 ideas the owner actually met this session and
   should be able to explain without help. Skip trivia (renames, config
   values) and anything the owner clearly already knew. If the repo's
   CLAUDE.md has a "Concepts in this repo" table, prefer its names so they
   stay consistent.

3. **Check what's stored.** Run `review.py list`. A concept already in the store
   is reused by id (only the repo gets added); don't make a near-duplicate
   under a new id.

4. **Draft each concept:**
   - `id`: short kebab-case slug, stable across repos (`delta-time`, not `marvin-delta-time`)
   - `name`: a few words
   - `repos`: `[<repo name>]`
   - `where`: repo-relative file (and function) where it shows up
   - `question`: one question that needs understanding, not recall
     ("Why multiply speed by delta time?", not "What is delta time?")
   - `answer`: 2–4 plain sentences that refer to this repo's code

   Show the draft as a short list and wait for a yes or edits.

5. **Save.** Pipe the approved list to the script:
   ```bash
   python3 "<path>/review.py" add <<'EOF'
   [ {...}, {...} ]
   EOF
   ```
   Report how many were added and that the first review is tomorrow.
