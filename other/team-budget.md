# Team e Budget — Big Bang Rewrite

---

## 1. Composizione Team Raccomandata

### Fase 1: Fondazioni (settimane 1-8)

| Ruolo | FTE | Settimane | Skill richieste | Note |
|---|---|---|---|---|
| Architetto .NET | 1 | 8 | DI, NuGet, CI/CD, Avalonia | Guida tecnica del progetto |
| Dev Senior C# | 2 | 8 | .NET 8+, Dapper, OPC UA, Modbus | Scrivono librerie orizzontali |
| Dev Junior/Medium | 1 | 8 | C#, git, NUnit | Test infrastructure, codegen |
| **Totale** | **4** | | | |

### Fase 2: Stack Macchina (settimane 9-18)

| Ruolo | FTE | Settimane | Note |
|---|---|---|---|
| Architetto .NET | 0.5 | 10 | Review, ADRs, supporto |
| Dev Senior C# | 2 | 10 | Stack KUKA, PLC, Safan/ESA |
| Dev Medium C# | 2 | 10 | Stack Sinumerik, simulatori, test |
| **Totale** | **4.5** | | |

### Fase 3: Applicativi + UI (settimane 15-24)

| Ruolo | FTE | Settimane | Note |
|---|---|---|---|
| Architetto .NET | 0.3 | 10 | Review, supporto layout engine |
| Dev Senior C# | 1 | 10 | Layout Engine, Recipe Engine |
| Dev UI Avalonia | 2 | 10 | Pagine HMI, design system, test UX |
| Dev Medium C# | 1 | 10 | Job Management, Alarms, Persistence |
| **Totale** | **4.3** | | |

### Fase 4: Deploy + Collaudo (settimane 22-28)

| Ruolo | FTE | Settimane | Note |
|---|---|---|---|
| Dev Senior | 1 | 6 | Ansible, WiX, UpdateAgent |
| DevOps | 0.5 | 6 | CI/CD, monitoring |
| Collaudatore | 1 | 2 | Test in fabbrica |
| **Totale** | **2.5** | | |

### Figura Trasversale (tutte le fasi)

| Ruolo | FTE | Note |
|---|---|---|
| Project Manager / Scrum Master | 0.5 | Pianificazione, stakeholder, risk management |
| Manutentore Legacy | 1 | Dedicato a bug fix su LAG/FAEL durante rewrite |

---

## 2. Organico Totale

| Periodo | Dev | Architetto | PM | Manut. Legacy | Collaudo | Totale |
|---|---|---|---|---|---|---|
| Settimane 1-8 | 3 | 1 | 0.5 | 1 | — | 5.5 |
| Settimane 9-14 | 4 | 0.5 | 0.5 | 1 | — | 6.0 |
| Settimane 15-22 | 4 | 0.3 | 0.5 | 1 | — | 5.8 |
| Settimane 23-28 | 1.5 | — | 0.5 | 1 | 1 | 4.0 |

**Picco massimo:** 6 FTE (settimane 9-14).

---

## 3. Costo del Personale

### Parameteri

| Ruolo | Costo lordo/mese | Costo totale/mese (x1.5 overhead) |
|---|---|---|
| Architetto .NET | €5.000 | €7.500 |
| Dev Senior C# | €4.000 | €6.000 |
| Dev Medium C# | €3.000 | €4.500 |
| Dev UI Avalonia | €4.000 | €6.000 |
| DevOps | €4.000 | €6.000 |
| PM | €4.000 | €6.000 |
| Manutentore Legacy | €3.000 | €4.500 |
| Collaudatore | €3.000 | €4.500 |

### Costo per Fase

| Fase | Durata | Team | Costo/mese | Costo fase |
|---|---|---|---|---|
| Fase 1 — Fondazioni | 8 settimane (2 mesi) | 5.5 FTE | €33.750 | €67.500 |
| Fase 2 — Stack Macchina | 10 settimane (2.5 mesi) | 6.0 FTE | €36.000 | €90.000 |
| Fase 3 — Applicativi | 10 settimane (2.5 mesi) | 5.8 FTE | €34.500 | €86.250 |
| Fase 4 — Deploy | 6 settimane (1.5 mesi) | 4.0 FTE | €21.000 | €31.500 |
| **Totale engineering** | **28 settimane (~7 mesi)** | | | **€275.250** |

### Costi Aggiuntivi

| Voce | Costo | Note |
|---|---|---|
| Licenze SonarQube (self-hosted) | €0 | Community Edition |
| Licenze Azure DevOps / GitHub | €0-50/mese | Già presenti |
| PC industriale per test | €2.500 | Investimento una tantum |
| Licenze CODESYS per CI | €1.000 | SE necessario runtime licenze |
| Contrattempi / viaggio per collaudo | €3.000 | Trasferte in fabbrica |
| **Costi accessori totali** | **€6.500** | |

### Budget Totale

| Voce | Importo |
|---|---|
| Engineering | €275.250 |
| Accessori | €6.500 |
| Buffer imprevisti (20%) | €56.000 |
| **Budget totale** | **~€338.000** |

---

## 4. Confronto: Costo Rewrite vs Costo Manutenzione

| Scenario | Costo annuo | 3 anni | 5 anni |
|---|---|---|---|
| **Stato attuale** (manutenzione LAG + FAEL) | €70.000 | €210.000 | €350.000 |
| **Big bang** (investimento una tantum) | €338.000 | €338.000 | €338.000 |
| **Post-rewrite** (manutenzione nuova piattaforma) | €25.000 | €75.000 | €125.000 |
| **Rewrite + 5 anni manutenzione** | — | — | **€463.000** |
| **Stato attuale 5 anni** | — | — | **€350.000** |

### Break-even

| Anno | Costo cumulativo rewrite | Costo cumulativo legacy |
|---|---|---|
| 0 (investimento) | €338.000 | €70.000 |
| 1 | €363.000 | €140.000 |
| 2 | €388.000 | €210.000 |
| 3 | €413.000 | €280.000 |
| 4 | €438.000 | €350.000 |
| 5 | **€463.000** | **€420.000** |

Break-even: **~4 anni** considerando solo manutenzione.

### Se si considera anche la produttività nuove commesse

| Scenario | 1 nuova commessa/anno | Costo per commessa | Costo 5 anni |
|---|---|---|---|
| Legacy (5 anni) | 5 nuove commesse | €140.000 | €350.000 + €700.000 = **€1.050.000** |
| Rewrite (investimento + 5 anni) | 5 nuove commesse | €60.000 | €338.000 + €125.000 + €300.000 = **€763.000** |
| **Risparmio** | | | **~€287.000 in 5 anni** |

---

## 5. Profili di Assunzione (se necessario)

### Se il team interno non ha tutte le skill

| Profilo | Skill | Quando serve | Durata |
|---|---|---|---|
| **Contractor Avalonia** | UI cross-platform, design system, MVVM | Fase 3 | 8-10 settimane |
| **Contracto DevOps** | Azure Pipelines, GitHub Actions, SonarQube, NuGet | Fase 1 | 4-6 settimane |
| **Consulente OPC UA** | OPC UA Foundation SDK, certificati, performance | Fase 1-2 | 2-4 settimane |

Costo contractor: ~€500-700/giorno. Budget aggiuntivo: €20.000-40.000.

---

## 6. Timeline Hiring

| Quando | Azione |
|---|---|
| **T-1 mese** (prima del via) | Identificare architetto .NET (interno o esterno) |
| **Settimana 0** | Avvio con architetto + 2 senior. Workshop DI/Avalonia |
| **Settimana 4** | Aggiungere 1-2 dev medium (se il budget lo permette) |
| **Settimana 8** | Inizio Fase 2. Team al completo (4-5 dev) |
| **Settimana 15** | Inizio Fase 3. Aggiungere contractor Avalonia |
| **Settimana 22** | Inizio Fase 4. Rilasciare contractor. Ridurre team |

---

## 7. Metriche di Efficienza del Team

| Metrica | Target | Misura |
|---|---|---|
| Velocity (story point / sprint) | 30-40 | Sprint review |
| LOC produttivi / dev / mese | 1.500-2.000 | Git stats (escludendo test e config) |
| Code coverage | ≥ 70% | SonarQube |
| Bug trovati in produzione | < 5 nel primo mese | Issue tracker |
| Tempo di onboarding | < 4 settimane | Prova pratica |
| Deploy frequency | ≥ 1/settimana in Fase 2-3 | CI/CD pipeline |
| Time to restore (rollback) | < 1 ora | Procedura documentata |
