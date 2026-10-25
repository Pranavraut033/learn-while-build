# Learn While Build

A Claude Code plugin for learning while you vibe code. Claude teaches as it
builds, saves what you met at the end of a session, then quizzes you on it
on a spaced-repetition schedule.

| Command | What it does |
|---|---|
| `/learn-mode` | Run once per repo. Reads the repo and adds repo-specific teaching rules to its `CLAUDE.md`. |
| `/learn-log` | Run at the end of a session. Saves the concepts you met, each with a question and answer. |
| `/learn-review` | Claude explains each due concept with your own code, quizzes you, and grades you. |

In repos set up with `/learn-mode`, a new session tells you when concepts are due.

## Schedule

Reviews come back after **1, 2, 7, 14, 30, 60** days.

- **clear**: next stage
- **retouch**: one stage back
- **unclear**: back to 1 day

## Flashcards page

For quick drills without a full Claude session:

```bash
python3 scripts/review.py serve
```

Open http://127.0.0.1:8777. Again / Hard / Good grade the card and move it on
the same schedule. The page uses Alpine.js and Pico.css from a CDN; the server
is Python's standard library, no installs.

## Where notes live

One central file: `~/.claude/learning/concepts.json` (set `LEARN_STORE` to
move it). Concepts are tagged with the repos they appeared in, so an idea you
meet in two projects has one schedule.

## Install

```bash
claude plugin marketplace add Pranavraut033/learn-while-build
```

```bash
claude plugin install learn-while-build@learn-while-build
```

Requires `python3`.

## Script

`scripts/review.py due | list | add | grade ID RESULT | serve [PORT] | hook | test`

## License

MIT
