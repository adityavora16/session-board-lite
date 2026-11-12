# Credits

Every third-party part of Session Board Lite, what it is used for, and its licence. Nothing is
bundled in the repo: the page loads fonts from Google Fonts at view time and runs without them.

## Fetched when a board is viewed, not in the repo

| Part | Author | Licence | Used by | Link |
|---|---|---|---|---|
| Bricolage Grotesque | Mathieu Triay | SIL Open Font License 1.1 | board headings | https://fonts.google.com/specimen/Bricolage+Grotesque |
| Figtree | Erik Kennedy | SIL Open Font License 1.1 | board body text | https://fonts.google.com/specimen/Figtree |
| JetBrains Mono | JetBrains | SIL Open Font License 1.1 | prompts, ids, tags | https://fonts.google.com/specimen/JetBrains+Mono |

## Run by you, not in the repo

| Part | Author | Licence | Used by | Link |
|---|---|---|---|---|
| Python 3 (standard library only) | Python Software Foundation | PSF License | `scripts/build.py` | https://www.python.org |

The build script imports only `html`, `json`, `sys` and `pathlib`. There is nothing to `pip install`.

## Data

The screenshot in the screenshot folder shows a board built from an invented three-session job. It describes
an invented project and contains no data from any source.
