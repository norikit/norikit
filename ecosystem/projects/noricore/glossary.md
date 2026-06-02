<!-- DO NOT EDIT — generated mirror of noricore/ai-docs/glossary.md by tools/aggregate_docs.py. Edit the source. -->

# Glossary

Domain terms used across noricore's docs and code. Keep entries short; link out for depth.

- **norikit** — the ecosystem this project belongs to: a suite of native macOS
  desktop-customization ("ricing") tools, unified by shared theming.
- **noriglaze** — the ecosystem's theme manager; the shared source of truth for appearance.
- **ricing** — customizing a desktop environment's look and behavior to a high degree.
- **event broker** — a process that receives events from producers and forwards them to
  interested subscribers; noricore is the norikit event broker.
- **provider** — a noricore module that monitors one system data source (battery, network,
  active app, etc.) and publishes typed events to the Broker when that source changes.
- **topic** — a named channel within the Broker (e.g. `battery.level`, `network.ssid`);
  subscribers register interest in topics; providers publish to topics.
- **subscriber / client** — a process (noribar, noriglaze, a third-party tool) that
  connects to noricore to receive push events or send pull queries.
- **push** — the event-stream interaction mode: noricore delivers events to clients as
  they happen, without the client polling.
- **pull / query** — the request/response interaction mode: a client asks for the current
  value of a topic and noricore responds immediately from its state cache.
- **state cache** — the Broker's in-memory store of the most recent value for each topic,
  used to seed new subscribers with a consistent initial view.
- **LaunchAgent** — a macOS mechanism for running a per-user daemon automatically at login,
  managed by `launchd`. noricore is distributed as a LaunchAgent.
- **IPC** — inter-process communication; the mechanism by which the noricore daemon and
  its clients exchange events and queries. Type TBD (see Q1 in open-questions.md).
