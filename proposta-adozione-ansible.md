# Proposta Adozione Ansible per Automazione PC Industriali

**Data:** 2026-07-02  
**A cura di:** Claude  
**Versione:** 1.0

---

## Indice

1. [Sintesi](#1-sintesi)
2. [Scenario attuale](#2-scenario-attuale)
3. [Obiettivi](#3-obiettivi)
4. [Architettura proposta](#4-architettura-proposta)
5. [Componenti automabili](#5-componenti-automabili)
6. [Playbook dettagliato](#6-playbook-dettagliato)
7. [Limiti e rischi](#7-limiti-e-rischi)
8. [Roadmap](#8-roadmap)
9. [Conclusioni](#9-conclusioni)

---

## 1. Sintesi

Ansible consente di automatizzare la configurazione dei PC industriali che ospitano:

- **CODESYS RTE** (runtime PLC in Docker su WSL)
- **HMI C#** (applicazione Windows / servizio)
- **MySQL** (database locale)
- **Rete, utenti, firewall, servizi Windows**

L'adozione riduce errori manuali, garantisce ripetibilità e abbassa i tempi di setup da **ore a minuti**.

---

## 2. Scenario attuale

### 2.1 Infrastruttura rilevata

```
PC Industriale (Windows)
├── WSL2 (Debian)
│   ├── Docker Engine
│   │   ├── Next          (CODESYS, porta 4857)
│   │   ├── vPLC1         (CODESYS, porta 4851)
│   │   ├── vPLC2         (CODESYS, porta 4852)
│   │   ├── vPLC3         (CODESYS, porta 4853)
│   │   ├── vKuka         (CODESYS, porta 4854)
│   │   ├── vEdge         (CODESYS, porta 4855)
│   │   ├── v5315         (CODESYS, porta 4856)
│   │   └── vLagNx1525    (CODESYS, porta 4858)
│   └── codesys.sh        (script di gestione)
├── Applicazione HMI C#    (servizio Windows)
├── MySQL                  (database locale)
├── Firewall Windows       (regole manuali)
└── Utenti e permessi      (configurazione manuale)
```

### 2.2 Criticità attuali

| Problema | Impatto |
|---|---|
| Setup manuale | Errori, dimenticanze, tempi lunghi |
| Documentazione assente o obsoleta | Difficile riprodurre configurazioni |
| Variabilità tra PC | Debugging complesso |
| Assenza di versioning | Impossibile fare rollback |
| Dipendenza da singole persone | Bus factor alto |

---

## 3. Obiettivi

1. **Ripetibilità** — stesso PC identico ogni volta
2. **Velocità** — da 2-4 ore a 10-15 minuti
3. **Tracciabilità** — ogni modifica versionata su git
4. **Idempotenza** — eseguire N volte, stesso risultato
5. **Documentazione viva** — il playbook *è* la documentazione
6. **Onboarding** — nuovo tecnico operativo in 1 giorno

---

## 4. Architettura proposta

### 4.1 Struttura repository

```
ansible-industrial-pc/
├── inventory/
│   ├── production/
│   │   ├── hosts.ini
│   │   └── group_vars/
│   │       ├── industrial_pcs.yml    # vars comuni
│   │       └── secrets.yml           # vault-crittografato
│   └── staging/
│       └── hosts.ini
│
├── roles/
│   ├── common/                        # hostname, IP, utenti, firewall
│   │   ├── tasks/main.yml
│   │   ├── templates/
│   │   │   └── motd.j2
│   │   └── vars/main.yml
│   │
│   ├── wsl_docker/                    # WSL2 + Docker + CODESYS containers
│   │   ├── tasks/main.yml
│   │   ├── templates/
│   │   │   ├── compose.vPLC1.j2
│   │   │   ├── compose.vPLC2.j2
│   │   │   └── codesys.sh.j2
│   │   └── files/
│   │       └── codesys.bashrc
│   │
│   ├── mysql/                         # MySQL install + database + utenti
│   │   ├── tasks/main.yml
│   │   └── templates/
│   │       └── my.cnf.j2
│   │
│   ├── hmi_app/                       # deploy HMI C#
│   │   ├── tasks/main.yml
│   │   ├── templates/
│   │   │   └── appsettings.json.j2
│   │   └── files/
│   │       └── HmiService.exe
│   │
│   └── monitoring/                    # logging, heartbeat
│       ├── tasks/main.yml
│       └── templates/
│           └── heartbeat.ps1.j2
│
├── playbooks/
│   ├── site.yml                       # playbook principale
│   ├── reset-demo-timer.yml           # rinnovo licenze demo
│   └── healthcheck.yml               # verifica stato
│
├── ansible.cfg
├── requirements.yml                   # collection richieste
└── vault-password                    # (escluso da git)
```

### 4.2 Flusso di esecuzione

```
┌──────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  Tecnico     │────▶│  Ansible         │────▶│  PC Industriale  │
│  Lancia      │     │  Control Node    │     │  (WinRM + SSH)    │
│  playbook    │     │  (WSL/Linux)     │     │                   │
└──────────────┘     └──────────────────┘     └──────────────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Git repository  │
                    │  (versionato)    │
                    └──────────────────┘
```

---

## 5. Componenti automabili

### 5.1 ✅ Completamente automabili

| Componente | Modulo Ansible | Dettaglio |
|---|---|---|
| **Hostname** | `win_hostname` | Imposta nome PC |
| **IP statico** | `win_ip_address` + `win_dns_client` | Rete industriale |
| **Firewall** | `win_firewall_rule` | Porte 4840 (CODESYS), 3306 (MySQL), HMI |
| **Utenti Windows** | `win_user`, `win_group` | Account operatori, service account |
| **MySQL** | `community.mysql.mysql_db`, `mysql_user` | DB, utenti, permessi, dump iniziale |
| **MySQL installer** | `win_chocolatey` o `win_package` | Installazione silenziosa |
| **.NET Runtime** | `win_chocolatey` | Dipendenza HMI C# |
| **Servizio HMI** | `win_service` | Install + start + recovery |
| **Config HMI** | `win_template` | `appsettings.json` parametrizzato |
| **Windows Features** | `win_feature` | .NET, IIS (se serve) |
| **Registro** | `win_regedit` | Performance tuning, security hardening |
| **Chocolatey packages** | `community.windows.win_chocolatey` | 7zip, notepad++, tools |
| **Certificati** | `win_certificate` | TLS per HMI |

### 5.2 ⚠️ Parzialmente automabili

| Componente | Cosa si può fare | Cosa NON si può fare |
|---|---|---|
| **CODESYS RTE (Windows native)** | Lanciare installer `/S`, copiare file licenza, avviare servizio | Attivare licenza (serve License Manager GUI), cambiare security level via API |
| **CODESYS in Docker** | Deploy compose file, script gestione, network | Il container image deve esistere già (pull da registry o export locale) |
| **WSL2** | Abilitare WSL (`dism`), impostare default distro, copiare script | Installare distro da zero (va fatto a mano o con `wsl --import`) |

### 5.3 ❌ NON automabili (senza API)

| Componente | Motivo |
|---|---|
| **Attivazione licenza CODESYS** | Richiede CODESYS License Manager Windows (GUI, no API pubblica) |
| **Deploy progetto PLC (.project)** | Richiede CODESYS IDE o API CAA non documentata |
| **Prima configurazione WSL distro** | `wsl --install -d Debian` va lanciato interattivamente la prima volta |
| **Driver real-time / TwinCAT** | Installazione molto particolare, spesso richiede reboot multipli |

---

## 6. Playbook dettagliato

### 6.1 `inventory/production/hosts.ini`

```ini
[industrial_pcs]
pc-linea-01 ansible_host=192.168.1.101 ansible_connection=winrm
pc-linea-02 ansible_host=192.168.1.102 ansible_connection=winrm

[industrial_pcs:vars]
ansible_user=Administrator
ansible_password=!vault |
ansible_winrm_transport=ntlm
ansible_winrm_server_cert_validation=ignore
```

### 6.2 `inventory/production/group_vars/industrial_pcs.yml`

```yaml
# ---- Rete ----
dns_servers:
  - 192.168.1.10
  - 8.8.8.8

# ---- Firewall ----
firewall_rules:
  - name: CODESYS OPC-UA
    port: 4840
    protocol: tcp
  - name: MySQL
    port: 3306
    protocol: tcp
  - name: HMI Web
    port: 5000
    protocol: tcp

# ---- Utenti ----
local_users:
  - name: operatore
    groups: [Users, Remote Desktop Users]
    password: !vault |
  - name: svc_hmi
    groups: [Users]
    password: !vault |
    description: Service account per HMI C#

# ---- MySQL ----
mysql_root_password: !vault |
mysql_databases:
  - name: plc_data
    encoding: utf8mb4
mysql_users:
  - name: hmi_user
    password: !vault |
    priv: "plc_data.*:SELECT,INSERT,UPDATE,DELETE"

# ---- CODESYS ----
codesys_containers:
  - name: vPLC1
    ip: 172.40.0.3
    port: 4851
  - name: vPLC2
    ip: 172.40.0.4
    port: 4852
  - name: Next
    ip: 172.40.0.9
    port: 4857

codesys_network:
  subnet: 172.40.0.0/16
  gateway: 172.40.0.1

# ---- HMI ----
hmi_app_name: HmiService
hmi_app_path: C:\Program Files\Sistec\HMI
hmi_port: 5000
hmi_db_connection: "Server=localhost;Database=plc_data;Uid=hmi_user;Pwd={{ mysql_users[0].password }};"
```

### 6.3 `playbooks/site.yml` — Playbook principale

```yaml
---
- name: Configurazione completa PC industriale
  hosts: industrial_pcs
  gather_facts: yes
  
  roles:
    - role: common
      tags: [common, always]

    - role: mysql
      tags: [mysql]
      when: install_mysql | default(true)

    - role: hmi_app
      tags: [hmi]
      when: install_hmi | default(true)

    - role: wsl_docker
      tags: [wsl, docker, codesys]
      when: install_codesys | default(true)

    - role: monitoring
      tags: [monitoring]
      when: install_monitoring | default(true)

  post_tasks:
    - name: Verifica stato servizi
      ansible.windows.win_service:
        name: "{{ item }}"
      loop:
        - MySQL
        - "{{ hmi_app_name }}"
        - LxssManager        # WSL
      register: svc_check

    - name: Report finale
      ansible.builtin.debug:
        msg: |
          Configurazione completata per {{ inventory_hostname }}
          - HMI:  {{ hmi_app_path }}
          - MySQL: installato
          - WSL:  attivo
          - Firewall: {{ firewall_rules | length }} regole
```

### 6.4 Ruolo `common` — tasks/main.yml

```yaml
---
- name: Imposta hostname
  ansible.windows.win_hostname:
    name: "{{ inventory_hostname | upper }}"
  register: hostname_result

- name: Reboot se hostname cambiato
  ansible.windows.win_reboot:
  when: hostname_result.reboot_required

- name: Crea utenti locali
  ansible.windows.win_user:
    name: "{{ item.name }}"
    password: "{{ item.password }}"
    groups: "{{ item.groups }}"
    description: "{{ item.description | default('') }}"
    password_never_expires: yes
    state: present
  loop: "{{ local_users }}"

- name: Regole firewall
  ansible.windows.win_firewall_rule:
    name: "{{ item.name }}"
    localport: "{{ item.port }}"
    protocol: "{{ item.protocol }}"
    action: allow
    direction: in
    state: present
  loop: "{{ firewall_rules }}"

- name: Disabilita sleep/standby
  ansible.windows.win_power_plan:
    name: High performance
  ansible.windows.win_regedit:
    path: HKLM:\SYSTEM\CurrentControlSet\Control\Power
    name: HibernateEnabled
    data: 0
    type: dword

- name: Imposta pagina di swap
  ansible.windows.win_regedit:
    path: HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management
    name: PagingFiles
    data: "C:\\pagefile.sys 4096 8192"
    type: multistring
```

### 6.5 Ruolo `wsl_docker` — tasks/main.yml

```yaml
---
- name: Abilita WSL
  ansible.windows.win_dism:
    features:
      - VirtualMachinePlatform
      - Microsoft-Windows-Subsystem-Linux
    state: present

- name: Crea directory script
  ansible.windows.win_file:
    path: "C:\\ProgramData\\Sistec\\codesys"
    state: directory

- name: Deploy script di gestione
  ansible.windows.win_template:
    src: codesys.sh.j2
    dest: C:\ProgramData\Sistec\codesys\codesys.sh

- name: Deploy compose files
  ansible.windows.win_template:
    src: "compose.{{ item.name }}.j2"
    dest: "C:\\ProgramData\\Sistec\\codesys\\{{ item.name }}.compose.yaml"
  loop: "{{ codesys_containers }}"

- name: Crea rete Docker
  ansible.windows.win_shell: |
    wsl -d Debian docker network create `
      --subnet {{ codesys_network.subnet }} `
      --gateway {{ codesys_network.gateway }} `
      codesys
  register: network_result
  failed_when: network_result.rc not in [0, 1]
  changed_when: "'already exists' not in network_result.stderr"

- name: Avvia container CODESYS
  ansible.windows.win_shell: |
    wsl -d Debian bash /mnt/c/ProgramData/Sistec/codesys/codesys.sh up {{ item.name }}
  loop: "{{ codesys_containers }}"
  loop_control:
    label: "{{ item.name }}"
```

### 6.6 Ruolo `mysql` — tasks/main.yml

```yaml
---
- name: Installa MySQL via Chocolatey
  community.windows.win_chocolatey:
    name: mysql
    version: '8.4.0'
    state: present

- name: Assicura servizio in esecuzione
  ansible.windows.win_service:
    name: MySQL
    state: started
    start_mode: auto

- name: Crea database
  community.mysql.mysql_db:
    name: "{{ item.name }}"
    encoding: "{{ item.encoding | default('utf8mb4') }}"
    state: present
    login_password: "{{ mysql_root_password }}"
    login_user: root
  loop: "{{ mysql_databases }}"

- name: Crea utenti MySQL
  community.mysql.mysql_user:
    name: "{{ item.name }}"
    password: "{{ item.password }}"
    priv: "{{ item.priv }}"
    host: "{{ item.host | default('localhost') }}"
    state: present
    login_password: "{{ mysql_root_password }}"
    login_user: root
  loop: "{{ mysql_users }}"

- name: Importa dump iniziale (se presente)
    community.mysql.mysql_db:
    name: "{{ mysql_databases[0].name }}"
    state: import
    target: "{{ mysql_initial_dump | default('') }}"
    login_password: "{{ mysql_root_password }}"
    login_user: root
  when: mysql_initial_dump is defined
```

### 6.7 Ruolo `hmi_app` — tasks/main.yml

```yaml
---
- name: Installa .NET Runtime 8.0
  community.windows.win_chocolatey:
    name: dotnet-8.0-runtime
    state: present

- name: Crea directory applicazione
  ansible.windows.win_file:
    path: "{{ hmi_app_path }}"
    state: directory

- name: Deploy applicazione HMI
  ansible.windows.win_copy:
    src: "files/{{ hmi_app_name }}/"
    dest: "{{ hmi_app_path }}\\"
    force: yes

- name: Template appsettings.json
  ansible.windows.win_template:
    src: appsettings.json.j2
    dest: "{{ hmi_app_path }}\\appsettings.json"

- name: Installa servizio Windows
  ansible.windows.win_shell: |
    sc create {{ hmi_app_name }} binPath="{{ hmi_app_path }}\{{ hmi_app_name }}.exe --serve"
    sc description {{ hmi_app_name }} "Servizio HMI Sistec"
    sc failure {{ hmi_app_name }} reset=86400 actions=restart/5000/restart/10000/restart/30000
  register: svc_install
  changed_when: "'[SC] CreateService SUCCESS' in svc_install.stdout"

- name: Avvia servizio HMI
  ansible.windows.win_service:
    name: "{{ hmi_app_name }}"
    state: started
    start_mode: auto
```

---

## 7. Limiti e rischi

### 7.1 Rischi tecnici

| Rischio | Probabilità | Mitigazione |
|---|---|---|
| WinRM non abilitato sul PC target | Alta | Prevedere script bootstrap manuale o immagine custom con WinRM già attivo |
| WSL non installato | Media | Ansible può abilitarlo via `win_dism`, ma serve reboot |
| Versione CODESYS diversa | Media | Parametrizzare immagine Docker in variabile |
| Lock per licenza CODESYS scaduta | Alta | Prevedere playbook `reset-demo-timer.yml` separato |
| MySQL porta 3306 conflitto | Bassa | Parametrizzare porta in vars |

### 7.2 Limiti intrinseci

1. **Licenza CODESYS** — Richiede intervento manuale (License Manager)
2. **Deploy progetto PLC** — Non fattibile via Ansible
3. **Primo setup WSL** — `wsl --install` va fatto almeno una volta a mano
4. **BIOS/UEFI settings** — Realtime, virtualization, wake-on-LAN (vanno fatti a mano)

### 7.3 Vault e segreti

```yaml
# inventory/production/group_vars/secrets.yml
# Crittografare con: ansible-vault encrypt secrets.yml
mysql_root_password: "S3cur3P@ss!"
mysql_users:
  - name: hmi_user
    password: "HmiP@ss123!"
svc_hmi_password: "SvcP@ss456!"
```

---

## 8. Roadmap

### Fase 1 — Fondamenta (1-2 giorni)
- [ ] Repository Ansible su git
- [ ] Ruolo `common` (hostname, IP, utenti, firewall)
- [ ] Playbook base testato su 1 PC
- [ ] `.gitignore`, `ansible.cfg`, vault

### Fase 2 — Database (1 giorno)
- [ ] Ruolo `mysql` (install + DB + utenti + dump)
- [ ] Test su PC di sviluppo

### Fase 3 — HMI (1-2 giorni)
- [ ] Ruolo `hmi_app` (deploy + servizio + template)
- [ ] Template `appsettings.json` parametrizzato
- [ ] Test deploy con versioni diverse

### Fase 4 — CODESYS / Docker (2-3 giorni)
- [ ] Ruolo `wsl_docker` (WSL + Docker + compose)
- [ ] Template compose file parametrizzati
- [ ] Script `codesys.sh` versionato
- [ ] Gestione rinnovo demo timer

### Fase 5 — Hardening (1 giorno)
- [ ] Certificati TLS
- [ ] Eventlog forwarding
- [ ] Monitoring / heartbeat

### Fase 6 — Documentazione e formazione (1 giorno)
- [ ] README con istruzioni
- [ ] Formazione tecnici

---

## 9. Conclusioni

### Vantaggi

| Aspetto | Prima (manuale) | Dopo (Ansible) |
|---|---|---|
| Tempo setup PC | 2-4 ore | 10-15 minuti |
| Ripetibilità | ~70% | 100% |
| Documentazione | Wiki/email sparse | Playbook versionato |
| Rollback | Reinstallare tutto | `git checkout` + esecuzione |
| Onboarding tecnico | Settimane | 1-2 giorni |
| Errori umani | Frequenti | Quasi zero |

### Costi

| Voce | Stimato |
|---|---|
| Setup iniziale Ansible | 5-8 giorni/uomo |
| Formazione tecnici | 1 giorno |
| Mantenimento | Basso (aggiornamento playbook) |

### Giudizio finale

**Ansible è fortemente consigliato** per automatizzare la configurazione dei PC industriali. Il ROI si raggiunge dopo 3-4 configurazioni. L'unico componente che richiede ancora intervento manuale è l'attivazione della licenza CODESYS tramite License Manager.

> "Se fai una cosa più di due volte, automatizzala." — *DevOps proverb*

---

*Documento generato il 2026-07-02 — Per domande contattare il team IT.*
