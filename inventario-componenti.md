# Inventario Componenti — Mappatura Legacy → Target

> Catalogo completo di ogni componente, macchina, schermata e libreria in LAG 5315 e FAEL 5309,
> con mappatura al corrispondente stack/layer nell'architettura target.

---

## 1. Macchine / Device

| Macchina | LAG | FAEL | Protocollo | Stack target | Priorità |
|---|---|---|---|---|---|
| **KUKA KRC** (robot) | ✅ RobotLogicKuka in Common/Logic + Sistec.Core/Interfaces | ✅ Kuka.Client separato + Common/Logic | TCP KRC | `Sistec.Stack.Kuka` | P0 |
| **Pressa Safan** | ✅ Sistec.Safan (Source) + Simulator | ❌ | TCP Winsock | `Sistec.Stack.Safan` | P0 |
| **Pressa ESA** | ❌ | ✅ Esa.Client + EasyModbus | Modbus TCP | `Sistec.Stack.Esa` | P0 |
| **PLC (CODESYS)** | ✅ DUT + OpcUaClientCollection | ✅ DUT + OpcUaClientCollection | OPC UA | `Sistec.Stack.PLC` | P0 |
| **CNC Sinumerik / ONE** | ✅ Sistec.Sinumerik | ❌ | OPC UA | `Sistec.Stack.Sinumerik` | P1 |
| **ATV320** (drive) | ✅ ATV320Logic | ✅ ATV320Logic | Modbus/OPC UA | `Sistec.Stack.PLC.Driver` | P1 |
| **LXM32** (drive) | ✅ LXM32Logic | ✅ LXM32Logic | Modbus/OPC UA | `Sistec.Stack.PLC.Driver` | P1 |
| **Valvole** | ✅ ValveLogic + ValveVacuumBlowLogic | ✅ ValveLogic + ValveVacuumBlowLogic | OPC UA | `Sistec.Stack.PLC.Driver` | P1 |
| **Grippers** | ✅ GripperLogic | ✅ ChangeGripperLogic | OPC UA | `Sistec.Stack.PLC.Driver` | P1 |
| **Motori** | ✅ MotorState | ✅ MotorState | OPC UA | `Sistec.Stack.PLC.Driver` | P1 |
| **Sensori** (SheetMonitor, ThicknessCheck, ecc.) | ✅ SheetMonitor, ThicknessCheck, ManualCentering | ✅ SheetMonitor, ThicknessCheck | OPC UA | `Sistec.Stack.PLC.Services` | P1 |
| **BS2308** (pannello FAEL) | ❌ | ✅ BS2308Logic | OPC UA | `Sistec.Stack.PLC.Driver` | P2 |
| **Zebus Bus** (messaggi inter-pannello) | ❌ | ✅ Sistec.Bus | Zebus (ZeroMQ) | `Sistec.Library.Bus` | P2 |

---

## 2. Schemzate / Pagine HMI

| Schermata | LAG | FAEL AB | FAEL C | FAEL BS | Stack target |
|---|---|---|---|---|---|
| **Home / Dashboard** | MainForm | FrmHMI | FrmHMI | — | `Sistec.HMI.Shell` |
| **Produzione** | Job view, Zone pages | JobView, Production pages | JobView | — | `Sistec.Stack.Production.UI` |
| **Job management** | JobDialog | JobDialog | JobDialog | — | `Sistec.Stack.JobManagement.UI` |
| **Stazione / Cella** | Cell pages (Cells/) | CellA, CellC | CellA, CellC | — | `Sistec.Stack.Production.UI` |
| **KUKA Robot** | ucKukaInfo, RobotCommands | ucKukaInfo, RobotCommands | ucKukaInfo | — | `Sistec.Stack.Kuka.UI` |
| **Pressa (Safan)** | SafanBrake, SafanSetup | ❌ | ❌ | — | `Sistec.Stack.Safan.UI` |
| **Pressa (ESA)** | ❌ | PressBrakeView | PressBrakeView | — | `Sistec.Stack.Esa.UI` |
| **PLC / Stato** | PlcStatus, Watchdog | PlcStatus, Watchdog | PlcStatus | — | `Sistec.Stack.PLC.UI` |
| **Allarmi** | AlarmBanner, AlarmView | AlarmBanner, AlarmView | AlarmBanner | — | `Sistec.Stack.Alarms.UI` |
| **Manutenzione** | MaintenancePage | MaintenanceView | MaintenanceView | — | `Sistec.Stack.Maintenance.UI` |
| **Configurazione** | SettingView, OnOffSetting | SettingR, SettingW, ConfigView | ConfigView | — | `Sistec.Configuration.UI` |
| **Dialoghi** | 43 file in Common/Dialogs/ (CutPlan, JobEdit, ecc.) | 52 file in Common/Dialogs/ | 52 file | — | `Sistec.Stack.*.UI` (distribuiti) |
| **Login / Utenti** | — | Employee login (FAEL only) | Employee login | — | `Sistec.Infra.Authentication.UI` |
| **Statistiche** | — | EmployeeStats (FAEL only) | EmployeeStats | — | `Sistec.HMI.Shell` |

---

## 3. Controlli UI WinForms (da migrare ad Avalonia)

| Controllo | LAG (Sistec.Controls + Common/Controls) | FAEL (Sistec.Controls + Common/Controls) | Nuovo design system |
|---|---|---|---|
| **Button** | ✅ Button.cs (custom) | ✅ Button.cs | `Sistec.Controls.Button` (Avalonia) |
| **Led** | ✅ Led.cs | ✅ Led.cs | `Sistec.Controls.Led` |
| **NumericUpDown** | ✅ NumericUpDown.cs | ✅ NumericUpDown.cs | `Sistec.Controls.Numeric` |
| **Valve** | ✅ ValveControl | ✅ ValveControl | `Sistec.Controls.Valve` |
| **Motor** | ✅ MotorControl | ✅ MotorControl | `Sistec.Controls.Motor` |
| **MotionEncoder** | ✅ MotionEncoder | ✅ MotionEncoder | `Sistec.Controls.Motion` |
| **AnalogScaling** | ✅ AnalogScalingView | ✅ AnalogScalingView | `Sistec.Controls.Analog` |
| **Banner (allarmi)** | ✅ Banner | ✅ Banner | `Sistec.Controls.AlarmBanner` |
| **GripperControl** | ✅ GripperControl | ✅ GripperControl | `Sistec.Controls.Gripper` |
| **RobotCommandsControl** | ✅ RobotCommands | ✅ RobotCommands | `Sistec.Stack.Kuka.UI` |
| **KukaInfo** | ✅ ucKukaInfo | ✅ ucKukaInfo | `Sistec.Stack.Kuka.UI` |
| **JobView** | ✅ JobView | ✅ JobView | `Sistec.Stack.JobManagement.UI` |
| **CutPlanView** | ✅ CutPlanView | ✅ CutPlanView | `Sistec.Stack.Production.UI` |
| **ZonePage** (Layout) | 7 Zone pages | 49 Zone pages | Layout Engine (layout.json) |
| **SettingRight/Weld/Saw** | ✅ SettingRight, Weld, Saw | ✅ SettingR, SettingW | `Sistec.Configuration.UI` |
| **PalletState** | ✅ PalletState | ✅ PalletStateView | `Sistec.Stack.JobManagement.UI` |
| **Containers** (PanelGroup, SistecGroupBox) | ✅ Containers/ | ✅ Containers/ | `Sistec.Controls.Container` |
| **Safety** | ✅ SafetyControl | ✅ SafetyConfig | `Sistec.Stack.Maintenance.UI` |

---

## 4. Librerie e Protocolli

| Libreria | LAG | FAEL | Target | Note |
|---|---|---|---|---|
| OPC UA Client | Sistec.Opc.Ua (19 file, 2.387 LOC) | Sistec.Opc.Ua (19 file, 2.153 LOC) | `Sistec.Library.OpcUa` | Baseline FAEL bugfix |
| EasyModbus | ❌ | EasyModbus (28 file, 6.681 LOC) | `Sistec.Library.Modbus` | Snellire: ~3.000 LOC |
| TCP Client | N/A (Winsock diretto in SafanClient) | N/A (Winsock in Kuka.Client) | `Sistec.Library.Tcp` | Nuovo: connection pool, reconnect |
| Zebus Bus | ❌ | Sistec.Bus (11 file, 565 LOC) | `Sistec.Library.Bus` | Mantenere Zebus o sostituire con Redis |
| MySQL | ✅ Dapper + MySqlConnector | ✅ Dapper + MySqlConnector | `Sistec.Infra.Persistence.MySql` | Stessa libreria, rifinire |
| Dapper | ✅ Sì | ✅ Sì | `Sistec.Infra.Persistence.Dapper` | Stessa libreria |
| System.Text.Json | Misto (JSON.NET) | Misto (JSON.NET) | `System.Text.Json` | Standardizzare |
| Serilog | ✅ Sì | ✅ Sì | `Serilog` + `ILogger<T>` | Già in uso |
| BCrypt | ❌ | ❌ | `BCrypt.Net-Next` | Nuovo |
| Polly | ❌ | ❌ | `Polly.Core` | Circuit breaker, retry |

---

## 5. Progetti di Test

| Progetto Test | LAG | FAEL | Target |
|---|---|---|---|
| SafanUnitTest | ✅ (NUnit 4.3.2, net10.0) | ❌ | `Sistec.Stack.Safan.Tests` |
| SafanTestCLI | ✅ (Console) | ❌ | Assorbito in test NUnit |
| SafanTestForm | ✅ (WinForms test) | ❌ | Eliminato (test automation) |
| SinumericTestCLI | ✅ (Console) | ❌ | `Sistec.Stack.Sinumerik.Tests` |
| TcpClientUnitTest | ✅ (NUnit) | ❌ | `Sistec.Library.Tcp.Tests` |
| OpcuaTest | ❌ | ✅ | `Sistec.Library.OpcUa.Tests` |
| KukaClientTest | ❌ | ✅ | `Sistec.Stack.Kuka.Tests` |
| KukaCLI | ❌ | ✅ | Eliminato (test automation) |
| ModbusTest | ❌ | ✅ | `Sistec.Library.Modbus.Tests` |
| 13× FakeOpcUa | Sparsi nei test | Sparsi nei test | `Sistec.Infra.TestHelpers.FakeOpcUa` (unico) |
| > 20 test projects vari | ❌ | ✅ (test UI, controlli, ecc.) | Test NUnit per ogni stack |

---

## 6. Configurazione e Deploy

| Componente | LAG | FAEL | Target |
|---|---|---|---|
| INI config files | ✅ Kuka.ini, Safan.ini | ✅ Kuka.ini | Eliminati → appsettings.json |
| XML config | ✅ Config.xml | ✅ Config.xml | Eliminati → IOptions<T> |
| layout.json | ❌ | ❌ | Nuovo |
| manifest.json | ❌ | ❌ | Nuovo |
| Ansible playbook | ❌ | ❌ | Nuovo |
| WiX installer | ❌ | ❌ | Nuovo (upgrade automatico) |
| UpdateAgent | ❌ | ❌ | Nuovo (servizio Windows) |
| Docker / WSL per CODESYS | ❌ | ❌ | Nuovo (solo per CI/test) |

---

## 7. Riepilogo per Stack Target

| Stack target | Da LAG | Da FAEL | Nuovo | LOC stimati |
|---|---|---|---|---|
| `Sistec.Core` | 15.099 LOC | 15.908 LOC | Unione + pulizia | ~8.000 |
| `Sistec.Controls` | 14.403 LOC | 14.603 LOC | Design system Avalonia | ~10.000 |
| `Sistec.UI` | 9.895 LOC | 8.577 LOC | Layout Engine | ~6.000 |
| `Sistec.Library.OpcUa` | 2.387 LOC | 2.153 LOC | Baseline FAEL | ~1.500 |
| `Sistec.Library.Modbus` | — | 6.681 LOC | Snellito | ~3.000 |
| `Sistec.Library.Tcp` | Nuovo | Nuovo | Da zero | ~1.500 |
| `Sistec.Library.Bus` | — | 565 LOC | Esteso | ~1.000 |
| `Sistec.Stack.Kuka` | 1 file RobotLogic | 1.928 Kuka.Client + Logic | Stack 5 layer | ~4.000 |
| `Sistec.Stack.Safan` | 2.163 LOC (+ Simulator) | — | Stack 5 layer | ~3.000 |
| `Sistec.Stack.Esa` | — | 1.256 Esa.Client + Logic | Stack 5 layer | ~3.000 |
| `Sistec.Stack.PLC` | DUT 4.710 + Logic | DUT 7.024 + Logic | Stack 5 layer + codegen | ~4.000 |
| `Sistec.Stack.Sinumerik` | 1.627 LOC | — | Stack 5 layer | ~3.000 |
| `Sistec.Stack.Production` | CellLogic | CellA/CellC | Nuovo + orchestrazione | ~3.000 |
| `Sistec.Stack.JobManagement` | JobDialog, DB | JobDialog, DB | Nuovo | ~2.500 |
| `Sistec.Stack.Maintenance` | MaintenancePage | MaintenanceView | Nuovo | ~1.500 |
| `Sistec.Stack.Alarms` | AlarmBanner | AlarmBanner | Nuovo | ~1.500 |
| `Sistec.Infra.Persistence` | Dapper esistente | Dapper esistente | Rifinito | ~1.500 |
| `Sistec.Infra.Configuration` | INI/XML reader | INI/XML reader | IOptions<T> | ~800 |
| `Sistec.Infra.Authentication` | — | Employee login | Nuovo + BCrypt | ~1.200 |
| `Sistec.HMI.Shell` | MainForm 11.986 | FrmHMI 13.104 | Thin DI + Layout Engine | ~3.000 |

---

## 8. Coverage: Quanto del Legacy viene Catturato

| Componente | Legacy LOC | Coperto dal target | Non coperto (V2) |
|---|---|---|---|
| Core (modelli, interfacce) | 31.007 | 90% | 10% (classi deprecated) |
| Controls (UI) | 29.006 | 80% | 20% (controlli esotici: rimpiazzabili da layout JSON) |
| OPC UA | 4.540 | 100% | — |
| Common Logic | 7.169 | 95% | 5% (logiche specifiche variante FAEL BS) |
| Common DUT | 11.734 | 90% (codegen) | 10% (DUT annidati complessi) |
| Common Dialogs | 17.486 | 70% (framework) | 30% (dialoghi specifici da reimplementare) |
| Common Layout | 12.870 | 80% (Layout Engine) | 20% (layout esotici: escape hatch Avalonia) |
| HMI Varianti | 34.000 | 85% (Composition Root) | 15% (pagine altamente custom → V2) |
| **Totale** | **~200.000** | **~85%** | **~15%** |

Il restante 15% non coperto in V1 include:
- Pagine layout esotiche (Layout Engine V2)
- Dialoghi FAEL BS (variante minore, poche richieste)
- Funzioni amministrative legacy (non critiche per produzione)
- Integrazioni con hardware obsoleto (non più in uso)
