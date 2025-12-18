"""
Einfache Tkinter-Oberfläche für pywallet.py, optimiert für Windows-Nutzung.

Die App ermöglicht:
- Auswahl einer wallet.dat-Datei
- Eingabe einer Passphrase
- Starten eines JSON-Dumps (Standard: alle Daten)
- Optionales Ignorieren der Wallet-Versionsprüfung
- Testlauf ohne Dateiausgabe zur schnellen Prüfung

Das GUI ruft pywallet.py über den aktuellen Python-Interpreter auf, um
kompatible Umgebungspfade sicherzustellen.
"""
from __future__ import annotations

import subprocess
import sys
import threading
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext


class PyWalletGUI:
    """Tkinter-basierte Oberfläche für pywallet.py."""

    def __init__(self, master: tk.Tk):
        self.master = master
        master.title("PyWallet GUI (Windows)")
        master.resizable(False, False)

        self.pywallet_path = Path(__file__).resolve().parent / "pywallet.py"

        default_wallet = Path("wallet.dat")
        self.wallet_path_var = tk.StringVar(value=str(default_wallet.resolve() if default_wallet.exists() else default_wallet))
        self.output_path_var = tk.StringVar(value="wallet_dump.json")
        self.passphrase_var = tk.StringVar()
        self.dumpformat_var = tk.StringVar(value="all")
        self.skip_version_check_var = tk.BooleanVar(value=False)

        self._build_form()
        self._build_log()

    def _build_form(self) -> None:
        padding = {"padx": 10, "pady": 5}

        tk.Label(self.master, text="Wallet-Datei:").grid(row=0, column=0, sticky="w", **padding)
        tk.Entry(self.master, textvariable=self.wallet_path_var, width=40).grid(row=0, column=1, **padding)
        tk.Button(self.master, text="Durchsuchen", command=self.select_wallet).grid(row=0, column=2, **padding)

        tk.Label(self.master, text="Passphrase (optional):").grid(row=1, column=0, sticky="w", **padding)
        tk.Entry(self.master, textvariable=self.passphrase_var, show="*", width=40).grid(row=1, column=1, **padding)

        tk.Label(self.master, text="Dump-Format:").grid(row=2, column=0, sticky="w", **padding)
        format_box = tk.OptionMenu(self.master, self.dumpformat_var, "all", "addr", "keys")
        format_box.grid(row=2, column=1, sticky="w", **padding)

        tk.Checkbutton(
            self.master,
            text="Wallet-Versionsprüfung überspringen",
            variable=self.skip_version_check_var,
        ).grid(row=3, column=1, sticky="w", **padding)

        tk.Label(self.master, text="Ausgabe-Datei:").grid(row=4, column=0, sticky="w", **padding)
        tk.Entry(self.master, textvariable=self.output_path_var, width=40).grid(row=4, column=1, **padding)
        tk.Button(self.master, text="Speicherort", command=self.select_output).grid(row=4, column=2, **padding)

        button_frame = tk.Frame(self.master)
        button_frame.grid(row=5, column=0, columnspan=3, pady=(10, 5))
        tk.Button(button_frame, text="Dump starten", command=lambda: self.start_run(save_output=True)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Testlauf", command=lambda: self.start_run(save_output=False)).pack(side=tk.LEFT, padx=5)

        self.status_var = tk.StringVar(value="Bereit")
        tk.Label(self.master, textvariable=self.status_var, fg="blue").grid(row=6, column=0, columnspan=3, sticky="w", padx=10, pady=(0, 5))

    def _build_log(self) -> None:
        tk.Label(self.master, text="Protokoll:").grid(row=7, column=0, columnspan=3, sticky="w", padx=10)
        self.log_text = scrolledtext.ScrolledText(self.master, width=70, height=18, state=tk.DISABLED)
        self.log_text.grid(row=8, column=0, columnspan=3, padx=10, pady=(0, 10))

    def select_wallet(self) -> None:
        filename = filedialog.askopenfilename(title="Wallet auswählen", filetypes=[("Bitcoin Wallet", "wallet.dat"), ("Alle Dateien", "*.*")])
        if filename:
            self.wallet_path_var.set(filename)

    def select_output(self) -> None:
        filename = filedialog.asksaveasfilename(
            title="Ausgabedatei wählen",
            defaultextension=".json",
            filetypes=[("JSON", "*.json"), ("Text", "*.txt"), ("Alle Dateien", "*.*")],
        )
        if filename:
            self.output_path_var.set(filename)

    def start_run(self, save_output: bool) -> None:
        command = self._build_command()
        if not command:
            return

        self._clear_log()
        self._set_status("Läuft...")
        thread = threading.Thread(target=self._run_command, args=(command, save_output), daemon=True)
        thread.start()

    def _build_command(self) -> list[str] | None:
        wallet_path = Path(self.wallet_path_var.get()).expanduser()
        if not wallet_path.exists():
            messagebox.showerror("Wallet nicht gefunden", f"Die Datei {wallet_path} existiert nicht.")
            return None

        cmd = [sys.executable, str(self.pywallet_path), "-w", str(wallet_path), "-d"]

        if self.passphrase_var.get().strip():
            cmd.extend(["--passphrase", self.passphrase_var.get().strip()])

        if self.dumpformat_var.get() != "all":
            cmd.extend(["--dumpformat", self.dumpformat_var.get()])

        if self.skip_version_check_var.get():
            cmd.append("--dont_check_walletversion")

        return cmd

    def _run_command(self, command: list[str], save_output: bool) -> None:
        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        except OSError as exc:
            self._append_log(f"Fehler beim Starten von pywallet: {exc}\n")
            self._set_status("Fehler")
            return

        output_lines: list[str] = []
        if process.stdout:
            for line in process.stdout:
                output_lines.append(line)
                self._append_log(line)

        exit_code = process.wait()

        if save_output:
            output_path = Path(self.output_path_var.get()).expanduser()
            try:
                output_path.write_text("".join(output_lines), encoding="utf-8")
                self._append_log(f"\n✅ Dump gespeichert unter: {output_path}\n")
            except OSError as exc:
                self._append_log(f"\n⚠️ Konnte Datei nicht speichern: {exc}\n")

        if exit_code == 0:
            self._set_status("Fertig - keine Fehler")
        else:
            self._set_status(f"Fehlgeschlagen (Exit-Code {exit_code})")

    def _append_log(self, text: str) -> None:
        self.log_text.after(0, self._write_to_log, text)

    def _write_to_log(self, text: str) -> None:
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.insert(tk.END, text)
        self.log_text.see(tk.END)
        self.log_text.configure(state=tk.DISABLED)

    def _clear_log(self) -> None:
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.configure(state=tk.DISABLED)

    def _set_status(self, status: str) -> None:
        self.status_var.set(status)


def main() -> None:
    root = tk.Tk()
    PyWalletGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
