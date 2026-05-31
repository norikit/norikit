<p align="center">
  <img src="https://img.shields.io/badge/ecosystem-norikit-32C572" alt="norikit"/>
  <img src="https://img.shields.io/badge/platform-macOS-black" alt="macOS"/>
  <img src="https://img.shields.io/badge/license-AGPL--3.0-blue" alt="License"/>
</p>

<h1 align="center">norikit</h1>

<p align="center">
  <strong>Sane defaults, insane customization.</strong>
</p>

<p align="center">
  A suite of native macOS desktop-customization tools for the ricing community —<br/>
  fast, hackable, and visually cohesive by design.
</p>

---

## What is norikit?

**norikit** is an open-source ecosystem of small, focused macOS tools for people who
*rice* their desktops — that is, who care deeply about how their environment looks and
behaves. Each tool does one thing well (your menu bar, your themes, your shortcuts), and
they're built to work together as a coherent set rather than a pile of unrelated utilities.

Two ideas hold the ecosystem together:

- **Native and fast.** norikit tools are built on Apple's own frameworks (Swift, AppKit,
  CoreAnimation, the SkyLight window server) rather than wrapping web views or spawning
  shell scripts. The result is low latency, smooth animation, and idle-to-near-zero CPU.
- **Visually cohesive.** A shared theming layer ([noriglaze](https://github.com/norikit/noriglaze))
  lets you switch the active theme across *every* norikit tool at once, so your whole
  setup stays consistent instead of drifting into a patchwork.

That's the promise in the slogan above. Every tool does something sensible the moment you
install it — sane basics and configs out of the box — yet opens all the way up for those who
want more, with no point where you have to walk away from the tool to realize an idea. It's
built for both ends of that spectrum at once —

- **Beginner ricers** get a polished, cohesive setup that just works, expressed through
  clear, shareable settings.
- **Extreme enthusiasts** get a **framework**. Advanced animations and mechanics that would
  normally mean scripting from scratch are composed on top of norikit's primitives instead —
  with escape hatches throughout, so you can supply your own implementation *without
  forking*.

The name is a seaweed/bento motif — *nori* (海苔) is the seaweed that wraps sushi;
*norikit* is the kit it all comes in.

## The projects

| Project | What it is | Status |
|---|---|---|
| [**noribar**](https://github.com/norikit/noribar) | A macOS menu-bar replacement built around **native, fully-animated SF Symbols**. Swift + AppKit + a private SkyLight window, configured with embedded **Lua**. Inspired by [sketchybar](https://github.com/FelixKratz/SketchyBar). | 🚧 Active — first product skeleton (M1) landed |
| [**noriglaze**](https://github.com/norikit/noriglaze) | The **theme manager** for the ecosystem. Stores your themes, serves them to the other tools, and switches the active theme across all of them at once. | 🌱 Early development |
| [**norify**](https://github.com/norikit/norify) | _Purpose not yet documented._ | 🥚 Placeholder |
| [**noribento**](https://github.com/norikit/noribento) | _Purpose not yet documented._ | 🥚 Placeholder |
| [**noribox**](https://github.com/norikit/noribox) | _Purpose not yet documented._ | 🥚 Placeholder |
| [**noricut**](https://github.com/norikit/noricut) | _Purpose not yet documented._ | 🥚 Placeholder |
| [**template**](https://github.com/norikit/template) | Starter template for new norikit projects. | 🧩 Scaffold |

> noribar is the most mature project today. The structure, conventions, and prime
> directives that every norikit project shares are documented in [`ai-docs/`](ai-docs/) —
> read those to build a new tool, rather than copying an existing repo.

## Principles

- **Native-first, performance-first.** Use the platform's real APIs. Stay off the main
  thread's back; idle to ~0% CPU when nothing is moving.
- **One tool, one job.** Small, composable utilities over monoliths.
- **Theme everything through noriglaze.** Tools are theme-able and share a single source
  of truth for appearance.
- **Configuration is a community artifact.** Configs should be powerful, shareable, and
  hot-reloadable — not buried in opaque preference panes.
- **Graceful degradation.** Support a sensible macOS floor; gate newer-OS features behind
  availability checks so older systems still work.
- **Documented and hackable.** Durable design knowledge lives in a knowledge base, kept
  current in the same change that alters reality.

## For contributors & AI agents

Building or extending a norikit project? Read **[`ai-docs/`](ai-docs/)** first. It is the
ecosystem-level reference: the mission, the prime directives every project shares, the
naming/branding/licensing conventions, and a checklist for bootstrapping a new tool.

Individual projects also carry their own `CLAUDE.md` and `ai-docs/` — the source of truth
for that project. This repo's `ai-docs/` is the source of truth for the ecosystem as a
whole. (`ai-docs/` is the agent-facing knowledge base in every norikit repo.)

## License

All norikit projects are licensed under [**AGPL-3.0**](LICENSE).
