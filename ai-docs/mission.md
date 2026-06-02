# Mission & prime directives

## Mission

> **norikit is a suite of native macOS desktop-customization ("ricing") tools — fast,
> hackable, and visually cohesive by design.**

**Slogan: _sane defaults, insane customization._**

It serves the **ricing community**: people who care intensely about how their desktop looks
and behaves. The bet is that this audience is best served not by one monolith but by a set
of small, focused, *native* tools that look and feel like one coherent system — unified by
a shared theming layer ([noriglaze](https://github.com/norikit/noriglaze)) so the whole
setup stays consistent.

### Sane defaults, insane customization

In a line: norikit gives you **sane basics and configs out of the box, and an insane level
of customization underneath.** Every tool is designed so the easy path is the default and
the ambitious path stays open — it does something sensible the moment you install it, with
no setup ceremony, yet opens all the way up so a user can reshape it into precisely what they
want. There should never be a point at which someone must abandon the tool — or fork it — to
realize an idea.

This is a deliberate commitment to **two audiences on one continuum**:

- **Beginner ricers** — who want a polished, cohesive setup that simply works, expressed
  through clear, shareable settings.
- **Extreme enthusiasts** — who build advanced animations and mechanics that would otherwise
  demand bespoke scripting from scratch. For them a norikit tool is a **framework**: the
  hard, low-level groundwork is already solved, so they compose their ideas *on top of* our
  primitives rather than reinventing them — without forking
  ([directive #9](#9-flexibility--escape-hatches-never-a-fork)).

A tool must serve both ends without forcing a choice: approachable defaults for the
newcomer, exposed seams and escape hatches for the power user, with no hard ceiling between
them.

The competitive thesis: the incumbents in this space are typically C + CoreGraphics +
shell-script glue. Going **native + a real embedded config language** unlocks capabilities
the incumbents structurally can't reach (e.g. Apple's animated SF Symbol engine), while
being safer to build and friendlier to contribute to.

## Prime directives

Every norikit project inherits these. They are *constraints*, not suggestions — change them
only with explicit owner direction, and record the change here.

### 1. Native-first
Build on the platform's real APIs (Swift, AppKit/SwiftUI, CoreAnimation, SkyLight/CGS where
warranted) — not web views, not Electron, not shelling out to `pmset`/`osascript` on every
tick. In-process native providers beat spawning processes: lower latency, richer data,
nothing to glue.

**Platform:** macOS-first today, and possibly broader later — so *native-first* means
"native to the platform you target," not "Swift forever." **Stack is chosen per project for
the best performance and feature set**, not dictated by a house language. Swift + native
frameworks is the proven default on macOS, but it is a per-project decision, not a mandate.
Keep platform-locked assumptions out of shared infrastructure where it's cheap to.

### 2. Performance-first
Low latency and smooth animation are features, not polish. Prefer display-synced rendering;
**idle to ~0% CPU when nothing is moving.** Keep UI work main-thread-safe and cheap.

### 3. Visually cohesive — theme through noriglaze
Appearance is shared infrastructure. Tools should be theme-able and consume themes from
noriglaze so a single switch restyles the entire setup — this is a **strong default**, the
direction every tool with visible UI should head, though not a hard blocking requirement
while noriglaze itself is early. Don't invent a private, non-interoperable theming scheme;
if you can't integrate noriglaze yet, design so you can later.

### 4. Configuration is a community artifact
Configs should be powerful (variables, functions, reuse), **shareable**, and
**hot-reloadable** — designed to be passed around the ricing community, not locked in a
preference pane. An **embedded scripting language** (variables, functions, reusable modules,
hot reload) is the strongest expression of this.

### 5. Graceful degradation
Pick a sensible OS floor and honor it. Gate newer-OS capabilities behind availability
checks (`if #available`) so the tool still runs — degraded, not broken — on the floor.

### 6. One tool, one job
Small, composable utilities over feature-sprawl. If a capability is really a separate
concern (theming, notifications, shortcuts…), it's probably a separate norikit tool.

### 7. Documented & hackable
Durable design knowledge lives in a knowledge base and is kept current **in the same change
that alters reality.** A memory-safe, readable codebase that newcomers can contribute to is
itself a goal. Open source under AGPL-3.0.

### 8. Always branch, always PR
Never commit directly to `main`. Branch from an up-to-date `main`, do the work, and open a
pull request as the deliverable. (Full workflow in [conventions.md](conventions.md).)

### 9. Flexibility — escape hatches, never a fork
Strive for **absolute flexibility**. Sensible defaults serve the common case, but a user
with extremely advanced needs must be able to **supply their own implementation without
forking the project**. Design the seams as first-class extension points — pluggable
providers/backends, user-supplied scripts or modules, overridable behavior — so the answer
to "the built-in doesn't do what I need" is *plug in your own*, never *maintain a fork*.
Forking is a failure of this directive.

### 10. Standalone-first — ecosystem is progressive enhancement
Every tool must be **fully usable on its own**, alongside a user's existing (non-norikit) setup. Running
it inside the ecosystem should *add* capability and benefits — never be a precondition. Ecosystem
couplings — system data from [noricore](https://github.com/norikit/noricore), themes from
[noriglaze](https://github.com/norikit/noriglaze), notifications from
[norify](https://github.com/norikit/norify), … — are **optional, availability-gated progressive
enhancements**: detect them, enrich when present, degrade cleanly when absent. A tool that *requires*
another norikit tool in order to function has violated this directive. (Makes explicit what directives
#3, #5, #6 and #9 already imply.)

---

*These directives are the foundation every norikit project inherits. The concrete shape they
take — repo layout, knowledge base, task system, CI — is described in
[project-structure.md](project-structure.md); reproduce it for each new tool.*
