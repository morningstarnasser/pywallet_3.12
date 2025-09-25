# PyWallet – wallet.dat Schlüssel-Extractor (Python 3)

Angepasste Version von `pywallet.py` zum **Extrahieren von Private Keys, Adressen und Metadaten** aus Bitcoin-ähnlichen `wallet.dat`-Dateien.  
Erweitert für **Python 3**, **JSON-sichere Dumps**, **verschlüsselte Wallets** und **Offline-Nutzung**.

> ⚠️ Nur für **eigene** Wallets verwenden. Der Zugriff auf fremde Wallets ist illegal.

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
git clone https://github.com/DEIN-USER/pywallet.git
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
