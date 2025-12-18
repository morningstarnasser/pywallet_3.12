# PyWallet – wallet.dat Schlüssel-Extractor (Python 3)

Angepasste Version von `pywallet.py` zum **Extrahieren von Private Keys, Adressen und Metadaten** aus Bitcoin-ähnlichen `wallet.dat`-Dateien.
Erweitert für **Python 3**, **JSON-sichere Dumps**, **verschlüsselte Wallets** und **Offline-Nutzung**.

> ⚠️ Nur für **eigene** Wallets verwenden. Der Zugriff auf fremde Wallets ist illegal.

## 🔒 Sicherheitsverbesserungen (Version 2.2+)

Diese Version enthält wichtige **Sicherheits- und Code-Qualitätsverbesserungen**:

- ✅ **Kryptographisch sichere Zufallszahlen**: Ersetzt `random.random()` durch `secrets.randbelow()` für NPP_rounds
- ✅ **Spezifische Exception-Behandlung**: Alle 31+ bare `except:` Klauseln durch spezifische Exceptions ersetzt
- ✅ **Python 3 Kompatibilität**: `urllib` durch `urllib.request` ersetzt, SSL-Zertifikatsvalidierung hinzugefügt
- ✅ **Verbesserte Fehlerbehandlung**: Bessere Logging und Error Messages
- ✅ **Code-Dokumentation**: Kommentare zu Bitcoin Core Wallet Format (z.B. IV-Ableitung)
- ✅ **Sicherere Imports**: Wildcard-Imports durch explizite Imports ersetzt (subprocess)

---

## Features

- Dump von **Adressen**, **Private Keys (WIF)**, **Metadaten** aus `wallet.dat`.
- **Verschlüsselte Wallets** mit `--passphrase`.
- Export nach **JSON**, **CSV**, **TXT**.
- **Offline-Modus**: keine Netzwerkabfragen.
- Recovery-Hilfen zum Scannen von **Rohdatenträgern** nach Wallet-Fragmenten.
- Verbesserte Python-3-Kompatibilität:
  - ersetzt `has_key`, `xrange`, `raw_input`, Byte-Vergleiche
  - Bytes→Hex für JSON-Dumps

---

## Systemvoraussetzungen

- Python **3.9+**
- Berkeley DB (für `bsddb3`)
- Abhängigkeiten: `bsddb3`, `ecdsa`, `simplejson`  
  Optional: `pycryptodome` (schneller AES)

---

## Installation

```bash
# 1) Homebrew: Berkeley DB bereitstellen (empfohlen v5 auf macOS)
brew install berkeley-db@5

# 2) Projekt holen
git clone https://github.com/morningstarnasser/pywallet_3.12.git
cd pywallet

# 3) Virtuelle Umgebung
python3 -m venv venv
source venv/bin/activate

# 4) bsddb3 gegen BDB bauen (Pfad setzen)
export BERKELEYDB_DIR=$(brew --prefix berkeley-db@5)

# 5) Abhängigkeiten
pip install --upgrade pip
pip install bsddb3 ecdsa simplejson pycryptodome

### Linux (Debian/Ubuntu)
sudo apt update
sudo apt install -y build-essential libdb-dev libdb5.3-dev python3-venv

git clone https://github.com/DEIN-USER/pywallet.git
cd pywallet

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install bsddb3 ecdsa simplejson pycryptodome

### Windows

git clone https://github.com/DEIN-USER/pywallet.git
cd pywallet

py -3 -m venv venv
.\venv\Scripts\activate

pip install --upgrade pip
pip install bsddb3 ecdsa simplejson pycryptodome


### Schnelleinstieg

# Adressen + Keys als JSON ausgeben
python3 pywallet.py -w /pfad/zu/wallet.dat -d

# Verschlüsselte Wallet: Passphrase angeben
python3 pywallet.py -w wallet.dat --passphrase "DEINE_PASSWORTPHRASE" -d

# Nur Adressen dumpen
python3 pywallet.py -w wallet.dat -d --dumpformat addr

# Dump in Datei
python3 pywallet.py -w wallet.dat -d > dump.json

### Exportformate
# Als JSON/CSV/TXT direkt schreiben (falls Export-Schalter vorhanden)
python3 pywallet.py -w wallet.dat --export json --out dump.json
python3 pywallet.py -w wallet.dat --export csv  --out dump.csv
python3 pywallet.py -w wallet.dat --export txt  --out dump.txt


### Typische Optionen (Auszug)
	•	-w, --wallet PATH – Pfad zur wallet.dat (Standard: wallet.dat im Arbeitsverzeichnis)
	•	--passphrase TEXT – Passphrase für verschlüsselte Wallets
	•	-d, --dump – Ausgabe als strukturierter Dump
	•	--dumpformat {addr,keys,all} – Filter für den Dump
	•	--export {json,csv,txt} – Exportformat
	•	--out DATEI – Zieldatei für Export
	•	--dont_check_walletversion – Versionsprüfung der Wallet ignorieren
	•	--network {btc,btctest,ltc,eth} – Netzwerkpräfixe setzen
	•	--with-balance – Salden je Adresse ermitteln (online, nicht offline)

Nicht alle Forks haben jede Option. Falls unbekannt: weglassen.

⸻

### Beispiele
# 1) Voller JSON-Dump, verschlüsselte Wallet
python3 pywallet.py -w wallet.dat --passphrase "meinPass" -d > dump.json

# 2) Nur Adressen
python3 pywallet.py -w wallet.dat -d --dumpformat addr > addresses.txt

# 3) CSV-Export
python3 pywallet.py -w wallet.dat --export csv --out keys.csv

# 4) Versionskonflikt umgehen
python3 pywallet.py -w wallet.dat --dont_check_walletversion -d

### Windows GUI starten

Wenn du lieber eine Oberfläche nutzen möchtest, starte die neue Tkinter-GUI:

```cmd
py -3 wallet_gui.py
```

**Funktionen:**

- Wallet-Datei auswählen (wallet.dat)
- Passphrase eingeben (optional)
- Dump-Format wählen (`all`, `addr`, `keys`)
- Version-Check überspringen (für neuere Wallet-Versionen)
- Testlauf (keine Datei) oder Dump speichern

### Troubleshooting

„The wallet is encrypted but no passphrase is used“

Lösung: --passphrase "DEIN_PASS" mitgeben.

„Version mismatch (must be <= 81000)“

Die Wallet hat eine höhere Version. Starte mit:

python3 pywallet.py -w wallet.dat --dont_check_walletversion -d

„Object of type bytes is not JSON serializable“

Diese Version konvertiert Bytes beim Dump in Hex-Strings.
Wenn es trotzdem auftritt: prüfe, ob du diese pywallet.py nutzt.

„Wallet data not recognized: … (bestblock/orderposnext/…)“

Informative Metadaten. Ignorierbar. In dieser Version stummgeschaltet.

IndentationError

Deutet auf manuelle Änderungen hin. Stelle sicher:
	•	Nur Spaces, keine Tabs. 4 Spaces pro Ebene.
	•	Nutze die bereitgestellte unveränderte Datei.

ModuleNotFoundError: bsddb3
	•	macOS: brew install berkeley-db@5 und export BERKELEYDB_DIR=$(brew --prefix berkeley-db@5) vor pip install bsddb3.
	•	Linux: sudo apt install libdb-dev libdb5.3-dev, dann pip install bsddb3.

---

## 🔐 Sicherheitshinweise

**Private Keys:**
- Private Keys werden im Klartext in den Speicher geladen und sollten nach Gebrauch gelöscht werden
- JSON/CSV-Exports enthalten sensible Daten – sicher aufbewahren oder verschlüsseln
- Nie Wallet-Dumps unverschlüsselt über unsichere Kanäle versenden

**Passphrasen:**
- Passphrases werden via Kommandozeile übergeben (können in Shell-History erscheinen)
- Für Produktivnutzung: Nutze getpass oder Umgebungsvariablen
- Niemals Passphrasen in Skripten hardcoden

**Netzwerk:**
- Balance-Abfragen kontaktieren externe APIs (blockchain.info, blockcypher.com)
- Für maximale Privatsphäre: Offline-Modus nutzen (keine `--with-balance` Option)
- Netzwerkanfragen nutzen SSL/TLS-Verschlüsselung

---

## 📝 Changelog (v2.2)

### Sicherheit
- Ersetzt unsichere `random.random()` durch kryptographisch sicheren `secrets.randbelow()`
- Alle 31+ bare `except:` Klauseln durch spezifische Exception-Typen ersetzt (ImportError, IOError, ValueError, etc.)
- Deprecated `urllib.urlopen()` durch `urllib.request.urlopen()` mit SSL-Validierung ersetzt
- Timeout-Parameter für Netzwerk-Requests hinzugefügt (verhindert Hänger)
- Verbesserte Input-Validierung und Error-Handling

### Code-Qualität
- Wildcard-Import `from subprocess import *` durch expliziten Import ersetzt
- Kommentare zu Bitcoin Core Wallet Format hinzugefügt (IV-Ableitung ist intentional)
- Besseres Logging mit spezifischen Fehlermeldungen
- File-Handling mit Context-Manager (`with open()`) verbessert
- Type-Safety-Verbesserungen (bytes vs. strings)

### Kompatibilität
- Python 3.9+ vollständig unterstützt
- Behält Kompatibilität mit Bitcoin Core wallet.dat Format bei
- Alle Tests bestanden

---

## 👨‍💻 Entwicklung

### Code-Stil
- PEP 8 konform
- Spezifische Exception-Handling
- Kryptographisch sichere Zufallszahlen
- Dokumentierte Sicherheitsannahmen

### Testing
```bash
# Basic functionality test
python3 pywallet.py -w wallet.dat -d

# Mit verschlüsselter Wallet
python3 pywallet.py -w wallet.dat --passphrase "test" -d
```
