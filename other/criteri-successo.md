# Criteri di Successo — Big Bang Rewrite

> Metriche oggettive per valutare il successo del rewrite, per fase e complessivo.
> Ogni criterio ha: misura, soglia, metodo di verifica.

---

## 0. Criterio Supremo

> **Il nuovo HMI gestisce un ciclo produttivo completo senza differenze funzionali rispetto al legacy, e con performance percepita migliore o uguale.**

---

## 1. Successo di Progetto (complessivo)

| # | Criterio | Misura | Soglia | Verifica |
|---|---|---|---|---|
| S1 | Consegna nei tempi | Settimane effettive vs stimate | ≤ 28 settimane | Project plan |
| S2 | Consegna nel budget | Costo effettivo vs budget | ≤ €350k | Timesheet + fatture |
| S3 | Scope V1 completo | Stack P0 erogati | 100% | Demo review |
| S4 | Zero regressioni critiche | Bug in produzione (P0/P1) | 0 nei primi 30gg | Issue tracker |
| S5 | Copertura funzionale | Flussi legacy riprodotti | ≥ 95% | Test comparison matrix |

---

## 2. Successo Tecnico

### 2.1 Qualità del Codice

| # | Criterio | Misura | Soglia | Verifica |
|---|---|---|---|---|
| T1 | Code coverage | Line coverage per progetto | ≥ 70% | SonarQube |
| T2 | Duplicazione | File duplicati | < 3% | SonarQube |
| T3 | Complessità ciclomatica | Per metodo | ≤ 10 | SonarQube |
| T4 | Debt ratio | Technical debt / LOC | < 2% | SonarQube |
| T5 | Code smells | Per 1.000 LOC | < 10 | SonarQube |
| T6 | Warning di compilazione | Warning nel solution build | 0 | CI pipeline |
| T7 | ADR documentati | Decisioni architetturali registrate | ≥ 10 ADRs | docs/adr/ |

### 2.2 Architettura

| # | Criterio | Misura | Soglia | Verifica |
|---|---|---|---|---|
| T8 | Dipendenze circolari | A livello progetto | 0 | Analisi NDepend / graph |
| T9 | Dipendenze circolari | Intra-assembly (namespace) | 0 | NDepend / Roslyn |
| T10 | Fan-out medio | Numero progetti referenziati per stack | ≤ 3 | Dependency graph |
| T11 | Layer violation | UI import in Services/Driver | 0 | ArchUnit test (Roslyn) |
| T12 | God Class assente | Classe più grande del sistema (LOC) | < 500 | SonarQube |
| T13 | God Project assente | Progetto più grande (LOC) | < 10.000 | Statistiche progetto |
| T14 | NuGet packages | Numero packages prodotti dal build | = numero stack | CI pipeline |
| T15 | DI Container | Uso di `new` per servizi (eccezioni: value objects, collections) | < 10 | Roslyn analyzer |

### 2.3 Performance

| # | Criterio | Misura | Soglia | Verifica |
|---|---|---|---|---|
| T16 | Avvio applicazione | Da click a UI pronta | < 5 secondi | Stopwatch CI |
| T17 | Cambio pagina | Navigazione completa | < 200ms | Profiling |
| T18 | Aggiornamento tag OPC UA | Da cambio PLC a UI aggiornata | < 100ms | pcap analysis |
| T19 | Utilizzo CPU (idle) | Percentuale CPU quando inattivo | < 5% | Task manager / PerfMon |
| T20 | Utilizzo memoria | Working set | < 200 MB | PerfMon |
| T21 | FPS UI | Frame rate in animazioni | ≥ 30 | Avalonia diagnostics |
| T22 | Connessione OPC UA | Tempo di riconnessione dopo disconnessione | < 3 secondi | Integration test |

---

## 3. Successo Funzionale

### 3.1 Flussi Operatore

| # | Criterio | Misura | Soglia | Verifica |
|---|---|---|---|---|
| F1 | Login → Produzione | Tempo per completare login e avviare un job | Come legacy o meglio | Benchmark comparativo |
| F2 | Ciclo produzione completo | Job → Preleva lamiera → Punzona → Piega → Scarica → Completa | Uguale al legacy | Test end-to-end |
| F3 | Gestione allarmi | Allarme → Visualizzazione → Ack → Reset | Uguale al legacy | Test comparativo |
| F4 | Emergenza | Premere emergenza → Macchina ferma → Reset → Ripartenza | Uguale al legacy | Test di sicurezza |
| F5 | Cambio job | Job attivo → Stop → Nuovo job → Avvio | Uguale al legacy | Test |
| F6 | Manutenzione | Accedere a pagine manutenzione, visualizzare storico, reset contatori | Uguale o meglio | Test |
| F7 | Multilingua | Italiano, Inglese (almeno) | Tutte le schermate | Test linguistico |

### 3.2 Copertura Funzionale Legacy

| # | Criterio | Misura | Soglia | Verifica |
|---|---|---|---|---|
| F8 | Job management legacy | Feature match col legacy | 100% | Comparison matrix |
| F9 | Tag OPC UA letti | Stessi tag legacy + eventuali nuovi | 100% | Tag inventory diff |
| F10 | Allarmi legacy | Stessa codifica, stesso formato | 100% | DB comparison |
| F11 | DB schema | Backward compatibile | Nessuna colonna rimossa | Schema diff |
| F12 | Workflow produzione | Stessa sequenza di stati | Identica | State machine comparison |

---

## 4. Successo di Migrazione

| # | Criterio | Misura | Soglia | Verifica |
|---|---|---|---|---|
| M1 | Downtime cutover | Ore di fermo impianto per installazione | ≤ 16 ore (2 giorni) | Timesheet |
| M2 | Rollback attivato? | Numero di rollback durante finestra cutover | 0 necessari | Incident report |
| M3 | Dati migrati | Completezza migrazione DB/config | 100% | Diff backup |
| M4 | Formazione operatore | Ore di formazione necessarie | ≤ 2 ore | Training log |
| M5 | Curva apprendimento | Tempo per operatore esperto per tornare a produttività normale | ≤ 2 giorni | Tempi ciclo |
| M6 | Downtime imprevisto | Fermo impianto NON pianificato nei primi 30gg | 0 ore | Incident report |

---

## 5. Successo di Business

| # | Criterio | Misura | Soglia | Verifica |
|---|---|---|---|---|
| B1 | Produttività operatore | Tempo medio per ciclo produttivo | Uguale o meglio del legacy | Cronometraggio |
| B2 | Errori operatore | Numero errori/giorno segnalati | Meno del legacy | Issue tracker |
| B3 | Richieste di assistenza | Ticket di supporto dal cliente | ≤ 3 nel primo mese | Helpdesk |
| B4 | Nuova commessa time-to-market | Tempo da kickoff a deploy per prossima commessa | ≤ 11 settimane | Project plan |
| B5 | Soddisfazione operatore | Survey dopo 1 mese | ≥ 4/5 | Questionario |
| B6 | Soddisfazione manutenzione | Survey dopo 1 mese | ≥ 4/5 | Questionario |

---

## 6. Matrice di Verifica per Stack

### Stack KUKA

| Verifica | Criterio specifico |
|---|---|
| Connessione KRC | Handshake TCP completo, heartbeat stabile |
| Lettura stato | Posizione, override, programma corrente, modalità |
| Comandi | Start/stop programma, override change, reset |
| Allarmi KUKA | Ricezione e visualizzazione allarmi robot |
| Follow service | Robot segue logica di cella (chiamata da Production) |

### Stack Safan / ESA

| Verifica | Criterio specifico |
|---|---|
| Connessione pressa | TCP (Safan) / Modbus (ESA) stabile |
| Stato pressa | Pronta, in ciclo, errore, emergenza |
| Ciclo piega | Avvio, monitoraggio, completamento |
| Parametri piega | Lettura e scrittura parametri programma |

### Stack PLC

| Verifica | Criterio specifico |
|---|---|
| Connessione OPC UA | Connect/Reconnect/Disconnect |
| Lettura tag | 200+ tag letti correttamente |
| Scrittura tag | Scrittura con risposta |
| Watchdog | Heartbeat HMI ↔ PLC funzionante |
| DUT generati | Compilano, matchano i tag reali, stessi valori |
| Subscription OPC UA | MonitoredItem notify su cambiamento |

### Stack Production

| Verifica | Criterio specifico |
|---|---|
| Job lifecycle | Crea → Assegna → Avvia → Completa → Archivia |
| Orchestrazione | KUKA + Pressa + PLC coordinati |
| Tracking pallet | Stato pallet aggiornato in tempo reale |
| Cut Plan | Generazione e visualizzazione piano di taglio |

### Stack UI / Layout Engine

| Verifica | Criterio specifico |
|---|---|
| layout.json → pagine | Ogni zona/device mappato correttamente |
| Navigazione | Menu → Pagina, back, breadcrumb |
| Touch input | Target ≥ 48px, funziona con guanti |
| Responsive | Adattamento a risoluzione pannello (800×600 a 1920×1080) |

---

## 7. Go/No-Go Gates

### Gate 1: Fine Fase 1 → Via libera Fase 2

Superare tutti:
- [ ] Progetti fondazione compilano e producono NuGet packages
- [ ] CI/CD pipeline verde: build → test → SonarQube → publish
- [ ] Code coverage fondazioni ≥ 60%
- [ ] Codegen DUT produce output valido per ≥ 90% DUT legacy
- [ ] Layout Engine POC funzionante (3 layout diversi)
- [ ] ADR per ogni decisione architetturale

### Gate 2: Fine Fase 2 → Via libera Fase 3

Superare tutti:
- [ ] Stack PLC + KUKA completi, integration test passano
- [ ] Stack pressa (Safan o ESA) completo
- [ ] Simulatori funzionanti per tutti gli stack sviluppati
- [ ] Code coverage stack ≥ 70%
- [ ] Zero dipendenze circolari (progetto e namespace)
- [ ] Zero SafeInvoke / Control in layer non UI
- [ ] HMI si avvia su PC industriale

### Gate 3: Fine Fase 3 → Via libera Collaudo

Superare tutti:
- [ ] Production flow end-to-end testato con simulatori
- [ ] UI performance: FPS ≥ 30, avvio < 5s, memoria < 200MB
- [ ] Test utente con operatore: completamento task ≥ 90%
- [ ] Behavior test suite legacy: 100% pass
- [ ] Documentazione utente e manutenzione pronta
- [ ] Piano di rollback testato (tempo < 1 ora)

### Gate 4: Collaudo in Fabbrica → Via libera Produzione

Superare tutti:
- [ ] Connessione a PLC reale OK
- [ ] Connessione a KUKA reale OK
- [ ] Connessione a pressa reale OK
- [ ] Ciclo produttivo reale completato con successo
- [ ] Emergenza testata con macchina reale
- [ ] Performance su PC industriale OK
- [ ] Operatore approva (firma UAT)

---

## 8. Criteri di Insuccesso

Il rewrite è considerato **fallito** se:

| Condizione | Azione |
|---|---|
| Dopo 28 settimane nessuno stack P0 è in produzione | Attivare Piano B (rewrite ibrido) |
| Costo supera €500k senza stack P0 completati | Attivare Piano C (abbandono) |
| Regressione causa danno a macchinario | Rollback immediato + audit |
| Operatore rifiuta di usare il nuovo HMI dopo 1 mese | Piano B: mantenere legacy come opzione |
| Tre rollback nella finestra di cutover | Block & review: fermare rilascio |

---

## 9. Frequenza di Misurazione

| Cosa | Frequenza | Chi |
|---|---|---|
| Code coverage, duplicazione, complessità | Ogni build CI | Automatico (SonarQube) |
| Performance (avvio, FPS, memoria) | Ogni sprint | Dev |
| Velocità team (velocity) | Ogni sprint | PM |
| Bug in produzione | Continuo | Issue tracker |
| Soddisfazione operatore | M+1, M+3, M+6 | PM |
| Confronto produttività (legacy vs nuovo) | M+1, M+3, M+6, M+12 | PM |
