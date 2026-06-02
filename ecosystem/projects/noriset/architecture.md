<!-- DO NOT EDIT — generated mirror of noriset/ai-docs/architecture.md by tools/aggregate_docs.py. Edit the source. -->

# Architecture

The evolving system design for noriset — modules, data flow, threading, and any
render/update loop. Keep this current as the design changes (see the
[maintenance protocol](README.md)).

> Early-stage placeholder. Replace with the real design as it emerges. The locked
> constraints it must respect live in [decisions.md](decisions.md).

## Overview

<!-- One paragraph: what the system is and how its parts fit together. -->

## Modules

<!--
Product code is grouped by responsibility — one directory per architectural layer under
Sources/, named for what it does. List the layers here as they appear, e.g.:

- `Sources/noriset/<Layer>/` — <responsibility>
-->

## Data flow

<!-- How information moves through the system: inputs → processing → output/render. -->

## Concurrency / threading

<!-- Which work runs where; main-thread-safety rules; any serial queues or loops. -->

## Entry points

<!-- The app bootstrap, and the headless self-test path that CI runs without a GUI. -->
