# AGENTS.md — Sistec HMI Architecture Workspace

This workspace is a **documentation-only repository** containing architecture analysis for Sistec HMI industrial software. No code, build system, CI/CD, or tests live here.

## Files

| File | Purpose | Lines |
|---|---|---|
| `analisi-unificata.md` | Main architecture document: unified analysis of LAG (5315) and FAEL (5309) codebases + greenfield blueprint for next commessa. | ~4030, 19 sections |
| `proposta-adozione-ansible.md` | Ansible adoption proposal for industrial PC deployment automation. | ~600 |

## Key Facts for Future Sessions

- **Strategic decision**: legacy LAG/FAEL will NOT be refactored. The architecture document is a blueprint for the **next greenfield commessa**.
- **Target stack**: Sistec.\<Nome>.Stack.* (5 layers: Client → Driver → Services → UI → Simulator), NuGet packages, DI container (MS.Extensions.DI), Avalonia UI, NUnit tests.
- **Dependencies to read**: `C:\Users\Sistec 32\.claude\CLAUDE.md` defines the `/graphify` skill.
- **Workspace**: `C:\Users\Sistec 32\Desktop\tmp\` — two .md files only. No CI config, no package manifests, no build scripts.

## Reference Codebases

| Codebase | Path | Scope |
|---|---|---|
| **5315 LAG** | `D:\DEV\5315_LAG` | 14 projects, pressa Safan (TCP), robot KUKA, CNC Sinumerik/ONE |
| **5309 FAEL** | `D:\DEV\5309_FAEL` | 53 projects, 3 varianti HMI (AB, C, BS), pressa ESA (Modbus), robot KUKA, bus Zebus |

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
