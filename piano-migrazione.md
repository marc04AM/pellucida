# Piano di Migrazione — Dal Legacy al Greenfield

> Strategia per passare da LAG 5315 / FAEL 5309 al nuovo HMI a stack verticali.
> Big bang, ma con fasi di atterraggio controllate.

---

## 0. Principi

1. **Nuovo HMI non tocca il legacy.** Zero file condivisi, zero dipendenze
2. **Cutover in finestra temporale stretta** (max 2 giorni). Impianto fermo per installazione
3. **Rollback sempre possibile** in < 1 ora (si ripristina il legacy)
4. **Dati migrati, non convertiti.** Il nuovo HMI legge lo stesso database MySQL
5. **Operatore non deve ri- imparare da zero.** Stessa logica, nuova UI

---

## 1. Strategia di Migrazione Dati

### 1.1 Database MySQL

| Tabella | Legacy | Nuovo HMI | Strategia |
|---|---|---|---|
| `utenti` | Plain text password | BCrypt hash | Migrazione batch: convertire hash al primo login (BCrypt compatibile) |
| `job` | Schema esistente | Schema identico + nuove colonne | Stessa tabella, ALTER TABLE per nuove colonne |
| `produzione` | Schema esistente | Schema esteso (FK employee, metriche) | Stessa tabella, backward compat |
| `configurazione` | File INI + tabelle | IOptions<T> + tabelle | Letto da file al boot, scritto su DB |
| `log_allarmi` | Schema esistente | Schema identico | Stessa tabella |
| `manutenzione` | Schema esistente | Schema esteso | Stessa tabella + nuove colonne |

**Regola:** Il nuovo HMI è **backward compatible** col DB legacy. Legge tutto ciò che il legacy ha scritto. Le nuove feature (statistiche dipendente, metriche) scrivono colonne aggiuntive che il legacy ignora.

### 1.2 File di Configurazione

| File | Legacy | Nuovo HMI |
|---|---|---|
| `Kuka.ini` | INI file | `appsettings.json` → `IOptions<KukaOptions>` |
| `PLC config` | XML config | `appsettings.json` → `IOptions<PlcOptions>` |
| `Safan config` | INI file | `appsettings.json` → `IOptions<SafanOptions>` |
| `layout.json` | Non esiste (pagine WinForms) | Nuovo file, cuore del Layout Engine |
| `manifest.json` | Non esiste | Nuovo file: quali stack attivare |

**Migrazione:** Script PowerShell che legge INI/XML e produce JSON strutturato convalidato. Eseguito UNA volta al deploy.

### 1.3 DUT OPC UA

| Aspetto | Legacy | Nuovo HMI |
|---|---|---|
| Provenienza | Scritti a mano (31 LAG + 39 FAEL) | Generati da CODESYS |
| Formato | POCO + EncodeableBase | POCO puri + mapping separato |
| Tag | Stringhe hardcoded | TagConstants type-safe |

**Migrazione:** Il codegen produce gli stessi nomi di tag OPC UA, quindi il PLC non sa se sta parlando con legacy o nuovo HMI.

---

## 2. Deploy Graduale per Stack

Non tutto il nuovo HMI viene attivato in una volta. Si attivano stack uno alla volta.

### Fase 0: Preparazione (1-2 settimane prima del cutover)

| Azione | Chi | Durata |
|---|---|---|
| Backup completo DB MySQL | IT | 30 min |
| Snapshot VM PC industriale | IT | 15 min |
| Installare .NET 8 runtime su PC industriale (accanto a legacy) | IT | 1h |
| Verificare connettività nuovo HMI → PLC (solo lettura) | Dev | 2h |
| Verificare connettività nuovo HMI → DB (solo lettura) | Dev | 1h |
| Formazione operatore: 1h su simulatore nuovo HMI | Dev + Op | 1h |

### Fase 1: Cutover (2 giorni, impianto fermo)

**Giorno 1 — Foundation + PLC Stack**

| Orario | Azione | Rollback point |
|---|---|---|
| 08:00 | Fermo impianto. Disabilitare avvii automatici legacy | — |
| 08:30 | Installare nuovo HMI su partizione separata | OK (legacy intatto) |
| 09:00 | Eseguire script migrazione config (INI → JSON) | OK (file sorgenti copiati) |
| 10:00 | Verificare connessione OPC UA al PLC | OK se fallisce → rollback |
| 11:00 | Verificare lettura tag (200+ tag) | OK |
| 12:00 | Verificare scrittura su tag di test | OK |
| 13:00 | Attivare Watchdog PLC ↔ HMI | OK |
| 15:00 | Test manually: Mode switch (Auto → Manuale → Auto) | OK |
| 17:00 | Test automatically: Job start/stop su simulatore | OK |
| 18:00 | Chiusura giorno 1. HMI in modalità **sola lettura** (monitoraggio affiancato) | — |

**Giorno 2 — Production + KUKA Stack**

| Orario | Azione | Rollback point |
|---|---|---|
| 08:00 | Attivare KUKA stack (sola lettura posizione) | OK (KUKA legacy è ancora in ascolto via Kuka.Client) |
| 09:00 | Verificare comunicazione KRC (stato robot, override) | OK |
| 10:00 | Test follow service: robot segue programma | OK |
| 11:00 | Attivare Production stack (Job management) | OK |
| 12:00 | Test: creare job → assegnare → avviare produzione | OK |
| 14:00 | Test: emergenza → reset → ripartenza | OK |
| 16:00 | Full cycle test: Job → Produzione → Completamento → Tracking | **GO/NO-GO** |
| 17:00 | Se GO: disabilitare avvio automatico legacy. Abilitare nuovo HMI | — |
| 18:00 | Se NO-GO: rollback a legacy | **< 1 ora** |

### Fase 2: Validazione (1 settimana dopo cutover)

| Giorno | Attività |
|---|---|
| **Lunedì** | Produzione reale con nuovo HMI. Dev in fabbrica |
| **Martedì** | Monitoraggio log, performance, allarmi |
| **Mercoledì** | Fix bug minori emersi in produzione |
| **Giovedì** | Test copertura: verificare che tutti i flussi legacy siano testati |
| **Venerdì** | Debrief operatore. Raccolta feedback. **GO/NOGO** per rimozione legacy |

### Fase 3: Disattivazione Legacy (solo dopo GO della validazione)

| Azione | Quando |
|---|---|
| Disinstallare legacy HMI dal PC industriale | Dopo 1 settimana di validazione |
| Rimuovere collegamento legacy dal menu avvio | Dopo 1 mese |
| Eliminare codice legacy dal repository | Dopo 3 mesi (solo se nessun rollback) |
| Archiviare repository legacy in sola lettura | Dopo 3 mesi |

---

## 3. Rollback Plan

### Procedura di Rollback Rapido (< 1 ora)

```
1. Fermare nuovo HMI (servizio Windows → Stop)
2. Abilitare avvio automatico legacy (servizio Windows → Start)
3. Verificare connettività legacy → PLC (1 min)
4. Verificare lettura tag correnti (1 min)
5. Riprendere produzione

Rollback NON cancella i dati scritti dal nuovo HMI.
Il DB è condiviso, il nuovo HMI scrive solo colonne backward compat.
```

### Quando fare rollback

| Condizione | Rollback? |
|---|---|
| Watchdog PLC segnala HMI offline > 5s | ✅ Immediato |
| KUKA non risponde ai comandi > 10s | ✅ Immediato |
| Errore OPC UA > 10 tag in errore | ✅ Immediato |
| Performance UI lenta (FPS < 15) | Dipende (si può ottimizzare) |
| Layout errato (pagine non corrette) | ⬜ Si fixa senza rollback |
| Feature mancante (non bloccante) | No (si aggiunge in V2) |

### Dati durante rollback

| Cosa succede ai dati | |
|---|---|
| Job aperti | Restano sul DB. Legacy li vede (stessa tabella) |
| Produzione completata | Registrata nel DB. Legacy ignora le nuove colonne |
| Allarmi generati | Scritti su DB. Legacy legge solo i campi che conosce |
| Configurazione nuova (layout.json) | Ignorata dal legacy. Non causa problemi |
| Statistiche dipendente | Scritte nel DB. Legacy non le usa |

---

## 4. Strategia Ambienti

| Ambiente | Scopo | Dove | PLC reale? |
|---|---|---|---|
| **Dev** | Sviluppo stack individuali | Laptop dev | Simulatori |
| **CI** | Build + test automatici | GitHub Actions | CODESYS in Docker |
| **Staging** | Integration test end-to-end | Server ufficio | CODESYS + KUKA Simulator |
| **Pre-prod** | Validazione con operatore | PC industriale lab | PLC reale (banco prova) |
| **Produzione** | HMI reale | PC industriale fabbrica | PLC + KUKA reali |

### Promotion flow

```
Dev → PR → CI (test) → Staging (integration) → Pre-prod (UAT) → Produzione
```

Ogni passaggio richiede:
- Dev → CI: PR approvata, test passano, SonarQube gate OK
- CI → Staging: Build stabile, coverage ≥ 70%
- Staging → Pre-prod: Integration test passano, smoke test manuale OK
- Pre-prod → Produzione: UAT firmato da operatore, collaudo completato

---

## 5. Comunicazioni

| Stakeholder | Cosa | Quando | Canale |
|---|---|---|---|
| **Operatore** | Training nuovo HMI | 1 settimana prima del cutover | Simulatore + manuale |
| **Manutenzione** | Procedure di ripristino | 1 settimana prima | Documento rollback |
| **Produzione** | Fermo impianto per cutover | 2 settimane prima | Calendario produzione |
| **IT** | Requisiti sistema e rete | 1 mese prima | Specifica tecnica |
| **Direzione** | Stato avanzamento | Ogni 2 settimane | Demo funzionante |
| **Cliente finale** | Tempistiche e impatto | 2 mesi prima | Riunione formale |

---

## 6. Formazione

| Ruolo | Quando | Durata | Contenuto |
|---|---|---|---|
| **Operatore** | Settimana -1 | 2h | Nuova UI, differenze, come segnalare problemi |
| **Manutentore** | Settimana -1 | 1h | Come ripristinare legacy, backup, log |
| **Sviluppatore** | Settimana 0 (Fase 1) | 40h | DI, Avalonia, stack architecture, test |
| **IT** | Settimana -2 | 2h | Deploy Ansible, monitoring, UpdateAgent |
