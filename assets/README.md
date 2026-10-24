# Profile asset generator

The profile keeps its content in native Markdown and uses self-hosted SVG only where a visual component adds real value.

## Build

```bash
python assets/build.py
```

The generator updates:

- `hero.svg` — identity, portrait and public GitHub totals;
- `about-v2.svg` — compact personal introduction and research scope;
- `toolchain-v5.svg` — animated single-row toolchain using the original repository icons;
- `projects-42-header.svg` and `personal-projects-header.svg` — compact project-section headers;
- `currently.svg` — current learning focus;
- `telemetry.svg` — repository, language and contribution data;
- `contact-*.svg` — neutral contact cards;
- `PROFILE.md` — standalone machine-readable profile data;
- the hidden machine-readable block in `README.md`, synchronized from the same source.

Public GitHub data is fetched at build time. Stable fallback values keep the profile renderable when the unauthenticated API is unavailable or rate-limited. The scheduled GitHub Actions workflow performs the same build and commits only when generated output changes.

Project tables and descriptions remain directly in `README.md` so they are selectable, searchable, accessible and easy to review without reading text embedded in images. The hidden block gives indexing tools and recruiter-facing assistants a synchronized evidence-first summary without changing the visible design.
