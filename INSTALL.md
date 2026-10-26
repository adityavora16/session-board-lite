# Install Session Board Lite

Session Board Lite is one Claude Code skill in `skills/session-board-lite/`. Nothing runs in the
background and nothing is downloaded at install time.

## What you need

- **Claude Code 2.1.116 or newer** (the version this skill was tested with), on any paid Claude
  plan that includes Claude Code.
- **Python 3.** The build script uses only the standard library, so there is nothing to install.
  Check with `python3 --version`.
- A browser, to open the board.

## Route A: the plugin marketplace (recommended)

```bash
claude plugin marketplace add adityavora16/claude-plugins
claude plugin install session-board-lite@adityavora
```

Inside a session, `/plugin marketplace add adityavora16/claude-plugins` and
`/plugin install session-board-lite@adityavora` do the same. Plugin skills are namespaced, so the
command is `/session-board-lite:session-board-lite`. It also starts on its own when you ask in plain
words, for example "split this into sessions I can run in parallel".

**Update:** `claude plugin update session-board-lite@adityavora`, then restart Claude Code.
**Remove:** `claude plugin uninstall session-board-lite@adityavora`.

## Route B: copy the skill folder

```bash
git clone https://github.com/adityavora16/session-board-lite.git
mkdir -p ~/.claude/skills && cp -R session-board-lite/skills/* ~/.claude/skills/
```

That makes the skill available in every project as `/session-board-lite`. For one project only,
copy it into that project's `.claude/skills/` folder instead. To remove it, delete
`~/.claude/skills/session-board-lite`.

If you also own the full Session Board, the two sit side by side: this one is
`/session-board-lite`, the full one is `/session-board`.

## Route C: try it for one session

```bash
git clone https://github.com/adityavora16/session-board-lite.git
claude --plugin-dir ./session-board-lite
```

## Try it

Start Claude Code in a project folder (an empty one works) and type:

```
/session-board-lite:session-board-lite Plan a small recipe website with a recipe format, page templates and a search box.
```

(Use `/session-board-lite` if you installed with Route B.) Claude reads the folder, splits the job,
writes `docs/sessions/plan.json`, builds the board and gives you the path to an HTML file. Open it
in a browser.

## What it does and does not do

It plans and writes prompts. It does not start the sessions for you; you copy each prompt into a
new Claude Code session. It does not check that your sessions followed their prompts. It builds
the board once. To change it, edit `docs/sessions/plan.json` (for example set a session's `status`
to `done`) and run the build again with the script in the skill folder:

```bash
python3 <skill folder>/scripts/build.py docs/sessions/plan.json session-board.html --local
```

Build to the same file name each time: the Done checkmarks you tick on the board are saved in the
browser for that file path.
