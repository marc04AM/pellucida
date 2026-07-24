# Analisi Rischi — Big Bang Rewrite

> Supplemento a §7 di analisi-unificata.md. Focus su rischi specifici dell'approccio big bang (greenfield da zero), non del refactoring incrementale.

---

## 0. Premessa: Big Bang vs Incrementale

| Approccio | Vantaggi | Svantaggi |
|---|---|---|
| **Big Bang (greenfield)** | Architettura pulita, nessun debito ereditato, decisioni tecniche coerenti | Tutto o niente, rischio delivery alto, nessun valore intermedio |
| **Incrementale (refactoring)** | Valore intermedio, rollback parziale, apprendimento progressivo | Debito tecnico persistente, architettura ibrida, tentazione di fermarsi a metà |

**Decisione:** big bang (confermata in analisi-unificata.md §3) perché il refactoring incrementale è impossibile — i cicli intra-assembly in Common (dipendenze.md §1) impediscono qualsiasi estrazione graduale.

---

## 1. Matrice Rischi

| # | Rischio | Probabilità | Impatto | Esposizione |
|---|---|---|---|---|
| R1 | Consegna in ritardo (scope creep) | ALTA | ALTO | **CRITICO** |
| R2 | Integrazione con PLC reale non testabile offline | ALTA | ALTO | **CRITICO** |
| R3 | Team non padroneggia DI/Avalonia | MEDIA | ALTO | **ALTO** |
| R4 | Layout Engine non copre tutti i casi legacy | MEDIA | ALTO | **ALTO** |
| R5 | Regressione funzionale rispetto a legacy | BASSA | MOLTO ALTO | **ALTO** |
| R6 | Codegen DUT non funziona su DUT reali | MEDIA | MEDIO | **MEDIO** |
| R7 | Performance Avalonia insufficiente su PC industriali | BASSA | ALTO | **MEDIO** |
| R8 | Conflitto con manutenzione legacy (stesso team) | ALTA | MEDIO | **MEDIO** |
| R9 | Conoscenza dominio persa (nessun dev legacy nel team) | MEDIA | ALTO | **ALTO** |
| R10 | Cambio requisiti durante sviluppo (commessa parallela) | ALTA | BASSO | **MEDIO** |

---

## 2. Dettaglio Rischi

### R1 — Consegna in ritardo (scope creep)

| Aspetto | Dettaglio |
|---|---|
| **Descrizione** | La prima commessa greenfield tenta di coprire TUTTI i casi d'uso di LAG e FAEL, allargando lo scope oltre il necessario |
| **Trigger** | "Tanto siamo in rewrite, aggiungiamo anche questa feature" |
| **Probabilità** | Alta (tipico di progetti greenfield) |
| **Impatto** | +50-100% tempo, perdita credibilità stakeholder |
| **Mitigazione 1** | MVP rigido: solo stack KUKA + PLC nella prima commessa. Safan/ESA/Sinumerik in seconda release |
| **Mitigazione 2** | Feature freeze 4 settimane prima della deadline. Solo bug fix |
| **Mitigazione 3** | Snapshot requisiti M1: firmare con stakeholder esattamente cosa include la V1 |

### R2 — Integrazione PLC non testabile offline

| Aspetto | Dettaglio |
|---|---|
| **Descrizione** | Il nuovo HMI non può essere testato contro il PLC reale fino al collaudo in fabbrica. I simulatori potrebbero non coprire edge case |
| **Trigger** | PLC CODESYS in Docker/WSL non replica esattamente il comportamento reale |
| **Probabilità** | Alta (già successo in passato) |
| **Impatto** | Scoperte in collaudo → ritorno in sviluppo |
| **Mitigazione 1** | Simulatore PLC con registrazione/riproduzione di traffico OPC UA reale (pcap) |
| **Mitigazione 2** | Test di integrazione contro CODESYS reale in CI (WSL2 + Docker) |
| **Mitigazione 3** | Periodo di parallel run: nuovo HMI in ascolto (read-only) accanto al legacy |

### R3 — Team non padroneggia DI/Avalonia

| Aspetto | Dettaglio |
|---|---|
| **Descrizione** | Il team legacy conosce WinForms e statici. DI container, Avalonia, test automatici richiedono nuove competenze |
| **Probabilità** | Media (dipende dalle skill del team) |
| **Impatto** | Codice mal progettato, anti-pattern in nuova architettura |
| **Mitigazione 1** | Settimana 0: workshop intensivo DI + Avalonia + NUnit |
| **Mitigazione 2** | Pair programming prime 4 settimane con dev senior .NET |
| **Mitigazione 3** | Code review obbligatoria ogni PR con checklist architetturale |

### R4 — Layout Engine non copre tutti i casi

| Aspetto | Dettaglio |
|---|---|
| **Descrizione** | Il Layout Engine (layout.json → UI) potrebbe non supportare layout esotici presenti in Common/Layout/ (LAG: 17 file, 3.495 LOC; FAEL: 49 file, 9.375 LOC) |
| **Probabilità** | Media (layout legacy sono molto vari) |
| **Impatto** | Necessità di pagine custom per alcuni casi → aumento LOC non preventivato |
| **Mitigazione 1** | Analizzare coverage layout.json contro tutti i layout legacy PRIMA di chiudere la specifica |
| **Mitigazione 2** | Prevedere escape hatch: `<Page x:Class="...">` per layout non coperti |
| **Mitigazione 3** | MVP Layout Engine: 80% dei casi. Il restante 20% in V2 |

### R5 — Regressione funzionale

| Aspetto | Dettaglio |
|---|---|
| **Descrizione** | Il nuovo HMI si comporta diversamente dal legacy in scenari edge (timing, messaggi errore, sequenze sicurezza) |
| **Probabilità** | Bassa (se testata bene) ma impatto potenzialmente grave (danni a macchinario) |
| **Mitigazione 1** | Regression test automatizzato: registrare traffico OPC UA da legacy, riprodurre su nuovo |
| **Mitigazione 2** | Behavior-driven test (Gherkin) per ogni sequenza critica (avvio, emergenza, cambio job) |
| **Mitigazione 3** | Collaudo in fabbrica con operatore legacy presente |

### R6 — Codegen DUT fallisce su DUT reali

| Aspetto | Dettaglio |
|---|---|
| **Descrizione** | I file CODESYS di input potrebbero avere formati imprevisti (encoding, tipi annidati, array multidimensionali) non gestiti dal generatore |
| **Probabilità** | Media (sempre così con codegen) |
| **Impatto** | Necessità di lavoro manuale sui DUT generati |
| **Mitigazione 1** | Testare codegen su TUTTI i DUT reali di LAG (31 file) e FAEL (39 file) prima di considerarlo completo |
| **Mitigazione 2** | Fallback a DUT scritti a mano per i casi non coperti (con test di regressione) |
| **Mitigazione 3** | Validazione automatica: il DUT generato compila? I tag matchano? |

---

## 3. Fallback Plan

Se il big bang fallisce, si attuano queste contromisure graduate:

### Livello 1: Ritardo < 4 settimane
- Tagliare scope: rimuovere stack non essenziali (Sinumerik, ESA) dalla V1
- Aumentare risorse (1-2 dev contractor)
- Niente rientro sul legacy

### Livello 2: Ritardo 4-8 settimane
- Congelare Layout Engine: le pagine critiche vengono scritte in Avalonia manualmente
- Ridurre test: solo smoke test + integration critical path
- Valutare rilascio graduale: prima il solo stack KUKA in produzione, poi il resto

### Livello 3: Ritardo > 8 settimane OPPURE fallimento tecnico irreversibile
- **Piano B: Rewrite ibrido.** Invece di sostituire tutto, si estrae solo `Sistec.Stack.PLC` e `Sistec.Stack.Kuka` (i due stack più critici) come librerie NuGet utilizzabili ANCHE dal legacy WinForms
- Il legacy rimane la UI principale; i nuovi stack sono back-end condiviso
- Transizione graduale: sostituire un pezzo per volta, iniziando dal PLC Client
- Accettare convivenza WinForms + nuovi stack per 12-18 mesi

### Livello 4: Fallimento totale
- **Piano C: Abbandono.** Si mantengono LAG e FAEL in manutenzione correttiva. L'investimento in Fase 1 (fondazioni condivise) viene comunque riusato: le librerie orizzontali (Persistence, Configuration, OpcUa, Modbus) vengono backportate come dipendenze NuGet nei progetti legacy
- L'architettura a stack verticali rimane un blueprint teorico, applicabile solo se nasce una nuova commessa con requisiti veramente greenfield

---

## 4. Go/No-Go Criteria per Fase

### Fine Fase 1 (Fondazioni): Go/No-Go

| Criterio | Misura | Soglia Go |
|---|---|---|
| Codegen DUT funzionante | % DUT legacy generati correttamente | ≥ 90% |
| Layout Engine proof-of-concept | 3 layout diversi da JSON renderizzati | OK |
| CI/CD pipeline | Build → Test → SonarQube → NuGet | Verde |
| Copertura test fondazioni | Line coverage | ≥ 60% |
| Workshop Avalonia completato | Tutti i dev hanno consegnato una pagina semplice | OK |

**No-Go:** Se codegen non funziona al 90%, si rinvia a Fase 1b (2 settimane extra). Se workshop fallisce, si assume contractor Avalonia.

### Fine Fase 2 (Stack Macchina): Go/No-Go

| Criterio | Misura | Soglia Go |
|---|---|---|
| Stack KUKA completo | Integration test Client → Simulator → Services | Verde |
| Stack PLC completo | Lettura/scrittura tag su CODESYS reale | OK |
| Stack Safan OPPURE ESA | Integration test | Verde |
| Coverage stack macchina | Line coverage per stack | ≥ 70% |
| Smoke test su PC industriale | HMI si avvia, connessione OK, pagine navigabili | OK |

**No-Go:** Se stack KUKA non passa integration test, si attiva Piano B (stack NuGet usabili da legacy).

### Fine Fase 3 (Applicativi): Go/No-Go

| Criterio | Misura | Soglia Go |
|---|---|---|
| Production flow end-to-end | Job → Produzione → Completamento → Tracking | OK |
| Emergency stop test | Macchina si ferma in < 200ms | OK |
| UI performance su pannello | FPS ≥ 30, avvio < 5s | OK |
| Test utente con operatore | Task completion rate | ≥ 90% |
| Regressione funzionale | Behavior test suite legacy | 100% pass |

**No-Go:** Se performance UI insufficiente, si valuta Avalonia VS WinForms hybrid. Se regression test fallisce, si blocca il rilascio.

---

## 5. Rischi Non Tecnici

| Rischio | Descrizione | Mitigazione |
|---|---|---|
| **Politico** | Stakeholder non vede progresso per 16 settimane | Demo ogni 2 settimane (stack funzionante) |
| **Organizzativo** | Team diviso tra manutenzione legacy e rewrite | Dedicare 1 dev fisso al legacy, resto al rewrite |
| **economico** | Budget tagliato a metà del percorso | MVP prioritizzato per stack. Se budget cala, si taglia dal fondo (Sinumerik, Ansible) |
| **Conoscenza** | Dev legacy lascia l'azienda | Documentazione (ADRs) + pair programming + registrazione sessioni |
