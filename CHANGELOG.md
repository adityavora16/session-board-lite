# Changelog

## v1.0.1, 12 November 2026

- Plugin icon added.
- INSTALL.md: the copy-by-hand routes start from a downloaded ZIP instead of `git clone`.

## v1.0, 23 October 2026

First release.

- The `session-board-lite` skill: splits one job into sessions and waves, writes one paste-ready
  prompt per session, picks a model for each, and builds a local board with a Copy prompt button
  on every card.
- `scripts/build.py` and `assets/template.html` are the same files as in the full Session Board.
  The build script validates the plan (models, waves, dependencies, prompt length, a "Done when"
  section) and fails when two sessions in the same wave own the same path, or when one owns a
  folder that contains the other's.
- A plan with more than six sessions or more than three waves still builds, and the board says the
  job is big enough for the full Session Board.
- Not in Lite: updating the board from a session's report, publishing it as a shareable page, the
  model table and the worked example. They are in the full Session Board.
