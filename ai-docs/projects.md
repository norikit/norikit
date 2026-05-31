# Project roster

The tools that make up the norikit ecosystem, as of this writing. Statuses and purposes for
the placeholder repos should be filled in as they're defined.

## Established

### [noribar](https://github.com/norikit/noribar) — menu-bar replacement · 🚧 active
A macOS menu-bar replacement built around **native, fully-animated SF Symbols**. Stack:
Swift + AppKit/CALayer rendering, a private **SkyLight (SLS/CGS)** window (all-Spaces,
over-fullscreen, non-activating), configured with **embedded Lua** (hot-reloadable).
Inspired by [sketchybar](https://github.com/FelixKratz/SketchyBar), but native rendering
lets it use Apple's symbol-effect engine that sketchybar's CoreGraphics glyphs can't reach.
Floor: macOS 13. The most mature project in the ecosystem to date.

### [noriglaze](https://github.com/norikit/noriglaze) — theme manager · 🌱 early
The **theming backbone** of the ecosystem. Stores your themes, serves them to the other
norikit tools, and switches the active theme across all of them at once so the whole setup
stays visually cohesive. Any tool that has appearance should integrate with noriglaze rather
than inventing its own theming.

## Placeholders (purpose not yet documented)

These repos exist with `LICENSE` and (some) hero art, but no stated purpose yet. **Do not
assume their scope** — confirm with the owner before building. Names suggest a direction but
are not authoritative:

- [**norify**](https://github.com/norikit/norify) — `nori` + `-ify`/notify. _TBD._
- [**noribento**](https://github.com/norikit/noribento) — *bento* = compartmented box /
  grid. _TBD._
- [**noribox**](https://github.com/norikit/noribox) — _TBD._
- [**noricut**](https://github.com/norikit/noricut) — `cut` (shortcuts? clipboard?). _TBD._

## Infrastructure

- [**norikit**](https://github.com/norikit/norikit) — this repo: the org's front door and
  the home of the ecosystem `ai-docs/`.
- [**template**](https://github.com/norikit/template) — starter scaffold for new norikit
  projects.

## How they relate

```
        noriglaze  ── themes ──▶  every tool that has appearance
            ▲                         (noribar, …)
            │
   (single theme switch restyles the whole setup)

   each tool: one job, native, fast, theme-able, AGPL-3.0
```

> When a placeholder's purpose is decided, move it to **Established**, give it a one-line
> definition here, and link its knowledge base.
