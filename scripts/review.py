#!/usr/bin/env python3
"""Concept store + spaced-repetition scheduler for learn-while-build.

  review.py due                  due concepts as JSON
  review.py list                 all concepts as JSON
  review.py add < concepts.json  add/merge a JSON list of concepts
  review.py grade ID RESULT      RESULT: clear | retouch | unclear
  review.py serve [PORT]         cards page on http://127.0.0.1:PORT (default 8777)
  review.py hook                 session-start nudge (learn-mode repos only)
  review.py test                 self-check
"""
import datetime as dt
import json
import os
import sys
import tempfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

STAGES = [1, 2, 7, 14, 30, 60]  # days until next review, by stage
MARKER = "<!-- learn-mode -->"
ROOT = Path(__file__).resolve().parent.parent


def store_path():
    return Path(os.environ.get("LEARN_STORE", Path.home() / ".claude/learning/concepts.json"))


def today():
    return dt.date.today()


def load():
    p = store_path()
    return json.loads(p.read_text()) if p.exists() else {"concepts": []}


def save(data):
    p = store_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=p.parent, suffix=".tmp")
    with os.fdopen(fd, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, p)  # atomic: a crash never leaves a half-written store


def due(data):
    t = today().isoformat()
    return [c for c in data["concepts"] if c["due"] <= t]


def add(data, new):
    by_id = {c["id"]: c for c in data["concepts"]}
    for n in new:
        c = by_id.get(n["id"])
        if c:  # seen before: keep its schedule, just note the extra repo
            for r in n.get("repos", []):
                if r not in c["repos"]:
                    c["repos"].append(r)
            continue
        c = {"repos": [], "where": "", **n, "stage": 0,
             "due": (today() + dt.timedelta(days=STAGES[0])).isoformat(), "history": []}
        data["concepts"].append(c)
        by_id[c["id"]] = c
    return data


def next_stage(stage, result):
    if result == "clear":
        return min(stage + 1, len(STAGES) - 1)
    if result == "retouch":
        return max(stage - 1, 0)
    if result == "unclear":
        return 0
    raise ValueError("result must be clear, retouch or unclear")


def with_next(c):
    """Card plus days-until-next-review for each grade, for the buttons."""
    return {**c, "next": {r: STAGES[next_stage(c["stage"], r)] for r in ("unclear", "retouch", "clear")}}


def grade(data, cid, result, by="claude"):
    c = next((c for c in data["concepts"] if c["id"] == cid), None)
    if c is None:
        raise KeyError(f"no concept {cid!r}")
    c["stage"] = next_stage(c["stage"], result)
    c["due"] = (today() + dt.timedelta(days=STAGES[c["stage"]])).isoformat()
    c["history"].append({"date": today().isoformat(), "result": result, "by": by})
    return c


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json"):
        b = body if isinstance(body, bytes) else json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        if self.path == "/":
            self._send(200, (ROOT / "web/cards.html").read_bytes(), "text/html; charset=utf-8")
        elif self.path == "/api/due":
            self._send(200, [with_next(c) for c in due(load())])
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/api/grade":
            return self._send(404, {"error": "not found"})
        try:
            req = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
            data = load()
            c = grade(data, req["id"], req["result"], by="cards")
            save(data)
            self._send(200, c)
        except (KeyError, ValueError) as e:
            self._send(400, {"error": str(e)})

    def log_message(self, *args):
        pass


def hook():
    md = Path.cwd() / "CLAUDE.md"
    if not (md.exists() and MARKER in md.read_text(errors="ignore")):
        return
    n = len(due(load()))
    if n:
        msg = (f"📚 {n} concept{'s' * (n != 1)} due for review. Run /learn-review, "
               f"or drill cards with: python3 \"{ROOT / 'scripts/review.py'}\" serve")
        # systemMessage shows it to the user; additionalContext tells Claude
        print(json.dumps({"systemMessage": msg, "hookSpecificOutput": {
            "hookEventName": "SessionStart", "additionalContext": msg}}))


def test():
    global today
    real = today
    with tempfile.TemporaryDirectory() as d:
        os.environ["LEARN_STORE"] = str(Path(d) / "c.json")
        today = lambda: dt.date(2026, 1, 1)
        data = add(load(), [{"id": "a", "name": "A", "repos": ["r1"], "question": "q", "answer": "x"}])
        assert data["concepts"][0]["due"] == "2026-01-02"
        add(data, [{"id": "a", "name": "A", "repos": ["r2"]}])
        assert len(data["concepts"]) == 1 and data["concepts"][0]["repos"] == ["r1", "r2"]
        assert due(data) == []
        assert grade(data, "a", "clear")["due"] == "2026-01-03"    # stage 1 -> +2
        grade(data, "a", "clear")
        assert grade(data, "a", "retouch")["stage"] == 1           # 2 -> 1
        assert grade(data, "a", "unclear")["due"] == "2026-01-02"  # back to +1
        for _ in range(10):
            grade(data, "a", "clear")
        assert data["concepts"][0]["stage"] == len(STAGES) - 1     # capped
        assert with_next(data["concepts"][0])["next"] == {"unclear": 1, "retouch": 30, "clear": 60}
        save(data)
        assert load() == data
        today = lambda: dt.date(2026, 6, 1)
        assert len(due(load())) == 1
    today = real
    print("ok")


def main(argv):
    cmd = argv[0] if argv else ""
    if cmd == "due":
        print(json.dumps(due(load()), indent=2, ensure_ascii=False))
    elif cmd == "list":
        print(json.dumps(load()["concepts"], indent=2, ensure_ascii=False))
    elif cmd == "add":
        data = add(load(), json.load(sys.stdin))
        save(data)
        print(f"{len(data['concepts'])} concepts in store")
    elif cmd == "grade" and len(argv) == 3:
        data = load()
        try:
            c = grade(data, argv[1], argv[2])
        except (KeyError, ValueError) as e:
            print(f"error: {e}", file=sys.stderr)
            return 1
        save(data)
        print(json.dumps({"id": c["id"], "stage": c["stage"], "due": c["due"]}))
    elif cmd == "serve":
        port = int(argv[1]) if len(argv) > 1 else 8777
        print(f"cards on http://127.0.0.1:{port}  (Ctrl+C to stop)")
        ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
    elif cmd == "hook":
        hook()
    elif cmd == "test":
        test()
    else:
        print(__doc__)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
