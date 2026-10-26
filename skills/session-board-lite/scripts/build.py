#!/usr/bin/env python3
"""Validate a session plan JSON and render it into the board template.

Usage: python3 build.py plan.json out.html [--local]

--local writes a complete HTML document (doctype and <html>) for opening the file straight in a
browser. Without it the output is the page body the Artifact tool expects.

Exits non-zero on errors; prints warnings and a one-line summary otherwise.
"""
import html
import json
import sys
from pathlib import Path

MODELS = {"Fable", "Opus", "Sonnet"}
STATUSES = {"todo", "running", "done", "blocked", "skip"}
EFFORTS = {"low", "medium", "high", "xhigh", "max"}
TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "template.html"


def norm(path):
    """'./src//auth/' -> 'src/auth' so equal paths compare equal."""
    parts = [p for p in str(path).strip().split("/") if p not in ("", ".")]
    return "/".join(parts)


def overlaps(a, b):
    """True when two owned paths are the same or one is inside the other."""
    a, b = norm(a), norm(b)
    if not a or not b:
        return True  # an empty path means the whole project
    return a == b or a.startswith(b + "/") or b.startswith(a + "/")


def validate(plan):
    errors, warnings = [], []
    sessions = plan.get("sessions") or []
    if not plan.get("title"):
        errors.append("plan.title is missing")
    if not sessions:
        errors.append("plan.sessions is empty")
    ids = [s.get("id") for s in sessions]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        errors.append(f"duplicate ids: {sorted(dupes)}")
    by_id = {s.get("id"): s for s in sessions}

    for s in sessions:
        sid = s.get("id", "?")
        for key in ("id", "title", "model", "wave", "prompt"):
            if s.get(key) in (None, ""):
                errors.append(f"{sid}: missing {key}")
        if s.get("model") not in MODELS:
            errors.append(f"{sid}: model must be one of {sorted(MODELS)}, got {s.get('model')!r}")
        if not isinstance(s.get("wave"), int):
            errors.append(f"{sid}: wave must be an integer")
        if s.get("status", "todo") not in STATUSES:
            errors.append(f"{sid}: status must be one of {sorted(STATUSES)}")
        if s.get("effort") and s["effort"] not in EFFORTS:
            errors.append(f"{sid}: effort must be one of {sorted(EFFORTS)}")
        for dep in s.get("needs", []):
            if dep not in by_id:
                errors.append(f"{sid}: needs unknown session {dep}")
            elif isinstance(s.get("wave"), int) and isinstance(by_id[dep].get("wave"), int) and by_id[dep]["wave"] >= s["wave"]:
                errors.append(f"{sid} (wave {s['wave']}) needs {dep} (wave {by_id[dep]['wave']}); a dependency must sit in an earlier wave")
        prompt = s.get("prompt") or ""
        if len(prompt) < 300:
            warnings.append(f"{sid}: prompt is only {len(prompt)} chars; a fresh session needs enough context to work alone")
        if "done when" not in prompt.lower():
            warnings.append(f"{sid}: prompt has no 'Done when' section")

    # Two code-writing sessions in the same wave must not own the same files.
    waves = {}
    for s in sessions:
        waves.setdefault(s.get("wave"), []).append(s)
    for n, group in waves.items():
        writers = [s for s in group if s.get("owns")]
        for i, a in enumerate(writers):
            for b in writers[i + 1:]:
                clash = sorted({f"{x} / {y}" for x in a["owns"] for y in b["owns"] if overlaps(x, y)})
                if clash:
                    errors.append(f"wave {n}: {a['id']} and {b['id']} both own overlapping paths ({'; '.join(clash)}); move one to a later wave or split the files")
        if len(group) > 1:
            for s in group:
                if s.get("owns") and not s.get("worktree"):
                    warnings.append(f"{s['id']}: writes code alongside other sessions but worktree is off")
    return errors, warnings


def main():
    args = [a for a in sys.argv[1:] if a != "--local"]
    local = "--local" in sys.argv[1:]
    if len(args) != 2:
        sys.exit(__doc__)
    plan_path, out_path = Path(args[0]), Path(args[1])
    try:
        plan = json.loads(plan_path.read_text())
    except (OSError, json.JSONDecodeError) as e:
        sys.exit(f"ERROR: cannot read {plan_path}: {e}")
    errors, warnings = validate(plan)
    for w in warnings:
        print("warn:", w)
    if errors:
        for e in errors:
            print("ERROR:", e)
        sys.exit(1)
    data = json.dumps(plan, ensure_ascii=False).replace("</", "<\\/")
    page = TEMPLATE.read_text().replace("__TITLE__", html.escape(plan["title"])).replace("__DATA__", data)
    if local:
        page = '<!doctype html>\n<html lang="en">\n' + page + "\n</html>\n"
    out_path.write_text(page)
    s = plan["sessions"]
    models = {m: sum(1 for x in s if x["model"] == m) for m in sorted(MODELS)}
    waves = sorted({x["wave"] for x in s})
    done = sum(1 for x in s if x.get("status") in ("done", "skip"))
    print(f"ok: {len(s)} sessions, {len(waves)} waves, {done} done; " + ", ".join(f"{k} {v}" for k, v in models.items() if v) + f" -> {out_path}")


if __name__ == "__main__":
    main()
