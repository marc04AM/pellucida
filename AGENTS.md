# AGENTS.md — Progetto Pellucida

this workspace is **Progetto Pellucida** (ref: stella che collassa in buco nero ne *Il pianeta del tesoro*). Documentation-only repo: architecture analysis for Sistec HMI industrial software. No code, build system, CI/CD, or tests.

## Files

| File | Purpose | Lines |
|---|---|---|
| `analisi-unificata.md` | Main architecture document: unified analysis of LAG (5315) and FAEL (5309) codebases + greenfield blueprint for next commessa. | ~6892, 26 sections (24 numbered + 2 intro) |
| `proposta-adozione-ansible.md` | Ansible adoption proposal for industrial PC deployment automation. | ~600 |

## Key Facts for Future Sessions

- **Strategic decision**: legacy LAG/FAEL will NOT be refactored. The architecture document is a blueprint for the **next greenfield commessa**.
- **Target stack**: `Sistec.Stack.<Nome>.*` (5 layers: Client → Driver → Services → UI → Simulator), `Sistec.Library.*` (horizontal shared libs: Tcp, OpcUa, Modbus), NuGet packages, DI container (MS.Extensions.DI), Avalonia UI, NUnit tests.
- **Dependencies to read**: `C:\Users\Sistec 32\.claude\CLAUDE.md` defines the `/graphify` skill.
- **Workspace**: `C:\Users\Sistec 32\Desktop\tmp\` — two .md files only. No CI config, no package manifests, no build scripts.

## HTML Conversion (`converti_html.py`)

| Aspect | Detail |
|---|---|
| **Output** | `analisi-unificata.html` (~419 KB, 26 pages, 35 Mermaid diagrams) |
| **Mermaid CDN** | `cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js` |
| **Known syntax fixes applied** | `&lt;/&gt;` → `<`/`>`, `optional` stripped from gantt tasks, `|"..."|` → `|...|` in arrow labels |
| **Highlight.js** | cdnjs v11.11.0, languages: csharp/json/xml/yaml/sql/javascript/markdown/ini |
| **Maximize/zoom** | Each Mermaid div gets hover button → modal with pan (drag) + zoom (scroll wheel) |
| **Other features** | Sidebar navigation, keyboard arrows, progress bar, code labels |

## Reference Codebases

| Codebase | Path | Scope |
|---|---|---|
| **5315 LAG** | `\..\5315_LAG` | 14 projects, pressa Safan (TCP), robot KUKA, CNC Sinumerik/ONE |
| **5309 FAEL** | `\..\5309_FAEL` | 53 projects, 3 varianti HMI (AB, C, BS), pressa ESA (Modbus), robot KUKA, bus Zebus |

Both are **read-only references** for architecture analysis. Never modify them.

## Workflow Constraint

**Every proposed modification to `analisi-unificata.md` must be:**
1. Presented in chat first (summary of what changes and why)
2. Written to the file only after the user confirms

This includes new sections, rewrites, renumbering, or any structural change.

## Style Constraints

- Document language: Italian
- The document should never be broken into smaller files — it's a monolithic reference
- All edits go in `analisi-unificata.md` unless stated otherwise
- Never create README, documentation, or summary files unless explicitly asked
