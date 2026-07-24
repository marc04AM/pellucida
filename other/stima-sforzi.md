# Stima Sforzi — Big Bang Rewrite

> Basata su LOC/file reali di LAG 5315 e FAEL 5309.
> Metriche COCOMO II (Constructive Cost Model) adattate a contesto HMI industriale C#/.NET.

---

## 0. Riepilogo

| Voce | Valore |
|---|---|
| LOC legacy totali (LAG + FAEL) | ~215.000 |
| LOC da riscrivere (unione, non somma) | ~140.000 |
| Stima COCOMO Organic (persona-mesi) | 28-36 PM |
| Team medio | 4-5 dev |
| Durata stimata prima commessa | 16-20 settimane |
| Costo stimato (solo engineering) | €160k-220k |
| Riuso commesse successive | ~60% (Fase 1 già fatta) |

---

## 1. Perimetro: cosa si riscrive

Non tutto il legacy va riscritto. Molto è duplicato tra LAG e FAEL.

| Categoria | LOC legacy | LOC target | Note |
|---|---|---|---|
| **Sistec.Core** (modelli, interfacce, enum) | 15.000 + 16.000 | ~8.000 | Unione + pulizia dead code |
| **Sistec.Controls** (bottoni, led, motori, valvole) | 14.400 + 14.600 | ~10.000 | Design system unificato |
| **Sistec.Opc.Ua** | 2.400 + 2.200 | ~1.500 | Baseline FAEL + fix §1.6 |
| **Sistec.UI** | 9.900 + 8.600 | ~6.000 | Layout Engine replace |
| **Common Logic** | 3.500 + 3.600 | ~5.000 | Distribuito negli stack Services |
| **Common Controls** | 12.300 + 8.800 | ~0 | Sostituito da stack UI + Layout Engine |
| **Common DUT** | 4.700 + 7.000 | ~0 | Code generation da CODESYS |
| **Common DTO** | 500 + 500 | ~500 | Minimo (generato in parte) |
| **Common Model** | 1.800 + 1.200 | ~1.500 | Modelli dominio puri |
| **Common DB** | 800 + 600 | ~500 | 10 repository → 1 |
| **Common Dialogs** | 7.900 + 9.600 | ~3.000 | Framework dialoghi unificato |
| **Common Layout** | 3.500 + 9.400 | ~500 | layout.json → Layout Engine |
| **Sistec.5315/HMI + FAEL varianti** | 12.000 + 22.000 | ~3.000 | Thin Composition Root + DI |
| **Kuka.Client** | 0 + 1.900 | ~2.000 | Stack Kuka.Client |
| **Esa.Client** | 0 + 1.300 | ~1.500 | Stack Esa.Client |
| **Sistec.Safan** | 2.200 + 0 | ~2.000 | Stack Safan.Client |
| **Sistec.Sinumerik** | 1.600 + 0 | ~2.000 | Stack Sinumerik (client + simulatore) |
| **EasyModbus** | 0 + 6.700 | ~3.000 | Sistec.Library.Modbus (snellito) |
| **Sistec.Bus** | 0 + 600 | ~1.000 | Sistec.Library.Bus (esteso) |
| **Test legacy** | 1.500 + 47.600 | ~15.000 | NUnit + Simulator per stack |
| **Ansible + Installer + CI/CD** | 0 | ~5.000 | Nuovo (YAML + WiX + PS) |
| **Totale** | **~215.000** | **~70.000** | |

Fattore di riduzione: **~3×** (da 215k a 70k LOC), grazie a:
- Eliminazione duplicazione LAG vs FAEL
- Code generation DUT (11.700 LOC manuali → script CODESYS)
- Layout Engine (13.000 LOC pagine WinForms → layout.json)
- Design system unico (Controls unificati)

---

## 2. Stima per Stack (COCOMO II adattato)

Parametri: team C# senior, contesto HMI industriale, requisiti noti.

| Stack | LOC stimati | Fattore scala | Persona-mesi | Dev assegnati | Settimane |
|---|---|---|---|---|---|
| **Fase 1: Fondazioni** | | | | | |
| Sistec.Infra.Persistence | 1.500 | 1.0 | 1.0 | 1 | 4 |
| Sistec.Infra.Configuration | 800 | 0.8 | 0.5 | 1 | 2 |
| Sistec.Infra.Authentication | 1.200 | 1.0 | 0.8 | 1 | 3 |
| Sistec.Infra.Logging | 500 | 0.6 | 0.3 | 1 | 1 |
| Sistec.Platform.Controls (Design System) | 4.000 | 1.2 | 2.5 | 1 | 5 |
| Sistec.Platform.OpcUa | 1.500 | 1.5 | 1.5 | 1 | 3 |
| Sistec.Platform.Modbus | 3.000 | 1.2 | 2.0 | 1 | 4 |
| Sistec.Infra.CodeGen (DUT) | 2.000 | 1.5 | 1.5 | 1 | 3 |
| Testing infrastructure | 2.000 | 0.8 | 1.0 | 1 | 2 |
| CI/CD pipeline (YAML + SonarQube + NuGet) | 1.000 | 1.0 | 0.5 | 0.5 | 2 |
| *Subtotale Fase 1* | *17.500* | | *11.6 PM* | *2-3* | *6-8 settimane* |

| **Fase 2: Stack Macchina** | | | | | |
| Sistec.Stack.Kuka (5 layer) | 4.000 | 1.3 | 3.0 | 1.5 | 4 |
| Sistec.Stack.Safan (5 layer) | 3.000 | 1.2 | 2.0 | 1 | 4 |
| Sistec.Stack.Esa (5 layer) | 3.000 | 1.2 | 2.0 | 1 | 4 |
| Sistec.Stack.PLC (5 layer) | 4.000 | 1.5 | 3.0 | 1.5 | 4 |
| Sistec.Stack.Sinumerik (5 layer) | 3.000 | 1.3 | 2.0 | 1 | 4 |
| *Subtotale Fase 2* | *17.000* | | *12.0 PM* | *2-3* | *8-12 settimane* |

| **Fase 3: Applicativi + UI** | | | | | |
| Sistec.Stack.Production | 3.000 | 1.3 | 2.0 | 1.5 | 3 |
| Sistec.Stack.JobManagement | 2.500 | 1.2 | 1.5 | 1 | 3 |
| Sistec.Stack.Maintenance | 1.500 | 1.0 | 1.0 | 1 | 2 |
| Sistec.Stack.Alarms | 1.500 | 1.0 | 1.0 | 1 | 2 |
| RecipeEngine + PalletStateMachine | 3.000 | 1.5 | 2.0 | 1 | 4 |
| Layout Engine (layout.json → UI) | 3.000 | 1.5 | 2.0 | 1 | 4 |
| Sistec.HMI.Shell (Composition Root) | 1.500 | 0.8 | 0.8 | 1 | 2 |
| *Subtotale Fase 3* | *16.000* | | *10.3 PM* | *2-3* | *8-10 settimane* |

| **Fase 4: Deploy + Collaudo** | | | | | |
| Ansible playbook | 1.500 | 0.8 | 0.5 | 0.5 | 2 |
| WiX installer + UpdateAgent | 3.000 | 1.2 | 2.0 | 1 | 4 |
| Smoke test + collaudo | — | — | 1.0 | 1 | 2 |
| *Subtotale Fase 4* | *4.500* | | *3.5 PM* | *1-2* | *4-6 settimane* |

| **Totale** | **~55.000** | | **~37 PM** | **4-5 dev** | **16-20 settimane** |

---

## 3. Confronto con Dati Legacy

### Costo attuale di manutenzione

| Voce | LAG | FAEL | Totale |
|---|---|---|---|
| LOC legacy | 97.662 | 117.674 | 215.336 |
| Bug fix / anno (stima 5% LOC) | 4.883 | 5.884 | 10.767 |
| Ore dev per fix | 0.5h/fix | 0.5h/fix | — |
| Ore/uomo anno manutenzione | ~600 | ~800 | ~1.400 |
| Costo annuo manutenzione (€50/h) | €30.000 | €40.000 | **€70.000** |

### Costo rewrite

| Voce | Valore |
|---|---|
| Persona-mesi totali | 37 PM |
| Costo medio dev/mese (€5.000 lordo + overhead) | €7.500 |
| Costo engineering | €277.500 |
| Buffer imprevisti (20%) | €55.500 |
| **Costo totale rewrite** | **€333.000** |
| **Break-even** | **~4.8 anni** |

### Costo commesse future (dopo rewrite)

| Voce | Legacy (stima) | Greenfield |
|---|---|---|
| Nuova commessa (stack + variante) | 6-8 mesi | 7-11 settimane |
| Costo nuova commessa | €120k-160k | €50k-70k |
| Rischio regressione | Alto | Basso |
| Onboarding nuovo dev | 3-6 mesi | 2-4 settimane |

---

## 4. Assunzioni e Fattori di Rischio

| Assunzione | Impatto | Se falsa |
|---|---|---|
| Team C# senior con esperienza .NET DI | -30% tempo | +50% se junior |
| Layout Engine già progettato (non da zero) | -20% Fase 3 | +100% se da inventare |
| Codegen DUT fattibile (CODESYS txt/xml in input) | -20% DUT | +50% se formato proprietario |
| Requisiti HMI noti (dalle codebase legacy) | -15% Fase 2-3 | +50% se da intervistare stakeholder |
| Avalonia maturo per HMI industriale | -10% UI | +50% se bug/carenze gravi |

---

## 5. Buffer Consigliato

| Tipo | % | Settimane | Note |
|---|---|---|---|
| Imprevisti tecnici | 15% | 3 | Deadlock DI, performance Avalonia, OPC UA edge case |
| Cambi requisiti | 10% | 2 | Il cliente vuole feature nuove durante sviluppo |
| Malattia/turnover | 5% | 1 | Team piccolo, una persona fuori rallenta tutto |
| Collaudo in fabbrica | 10% | 2 | Ritardi impianto, PLC non pronto, KUKA non disponibile |
| **Buffer totale** | **40%** | **6-8 settimane** | ||

**Durata finale consigliata: 22-28 settimane** (includendo buffer).

---

## 6. Paragone: COCOMO II Formale

Applicando COCOMO II a 55.000 LOC stimati, modalità **Organic** (team piccolo, requisiti stabili, ambiente familiare):

| Parametro | Valore |
|---|---|
| A (costante Organic) | 2.94 |
| B (exponent Organic) | 1.10 |
| EAF (Effort Adjustment Factor) medio | 1.00 |
| PM = A × (KSLOC)^B × EAF | 2.94 × 55^1.10 |
| **Persona-mesi COCOMO** | **~225 PM** |

Questo numero (225 PM) è molto più alto della stima a dettaglio (37 PM) perché COCOMO II assume waterfall classico con documentazione formale, revisioni, QA formale, management overhead. In pratica, con team agile e stack moderno (.NET 8+, DI, test automatici), i fattori di scala sono molto più favorevoli. La stima realistica è **30-40 PM**.

**Riferimento:** il solo Common di LAG (38.645 LOC) è stato scritto da ~2-3 dev in ~2 anni senza DI, test o architettura — un rate di ~800 LOC/dev/mese. Con DI + test + architettura pulita, il rate atteso è **1.500-2.000 LOC/dev/mese**.
