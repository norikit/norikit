<!-- DO NOT EDIT — generated from ai-docs/projects.toml by tools/gen_roster.py. -->

# norikit — project roster

The toolkit, generated from `ai-docs/projects.toml`. To change it, edit the TOML and run
`tools/gen_roster.py` — never hand-edit this file.

| Tool | What it is | Status |
|---|---|---|
| [noribar](https://github.com/norikit/noribar) | Menu-bar replacement built around native, fully-animated SF Symbols. Swift + AppKit + embedded Lua. | 🚧 Active |
| [noricore](https://github.com/norikit/noricore) | Event broker & data backbone — aggregates system state and serves it to every tool. | 🌱 Early |
| [noricut](https://github.com/norikit/noricut) | Cross-app hotkey/shortcut daemon (NWP protocol). | 🌱 Early |
| [noriglaze](https://github.com/norikit/noriglaze) | Theme manager — one switch retheme every norikit tool at once. | 🌱 Early |
| [noribento](https://github.com/norikit/noribento) | Fast, keyboard-driven tiling window manager, i3-style. | 🥚 Stub |
| [noribox](https://github.com/norikit/noribox) | Omnibox launcher — apps, commands, and search in one box. | 🥚 Stub |
| [norify](https://github.com/norikit/norify) | Notification engine for the ecosystem. | 🥚 Stub |
| [noripad](https://github.com/norikit/noripad) | Clipboard manager — searchable history, pinning, quick paste. | 🥚 Stub |
| [noripaper](https://github.com/norikit/noripaper) | Wallpaper engine — static and animated, hot-swapped on theme change. | 🥚 Stub |
| [noriset](https://github.com/norikit/noriset) | The bundler — combines all norikit tooling into one plug-and-play package. | 🥚 Stub |

## Infrastructure

- [norikit](https://github.com/norikit/norikit) — Org front door — ecosystem ai-docs, central asset store, framework tooling.
- [template](https://github.com/norikit/template) — Starter scaffold every new norikit project clones.
- [.github](https://github.com/norikit/.github) — Org profile + reusable workflows + org defaults.

## Ecosystem integration

*Optional, availability-gated progressive enhancement — never a hard dependency.*

- **noribar** — consumes noricore, noriglaze
- **noricore** — provides system-events
- **noricut** — provides hotkeys
- **noriglaze** — provides themes
