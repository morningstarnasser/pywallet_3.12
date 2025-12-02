#!/usr/bin/env python3
"""
decrypt_wallet.py - Spezialisiertes Tool zum Entschlüsseln von Bitcoin Wallets

Dieses Tool versucht verschlüsselte Private Keys aus wallet.dat zu extrahieren
und zu entschlüsseln mit verschiedenen Methoden.
"""

import sys
import os
import json
import getpass
import argparse
from datetime import datetime

# Import PyWallet modules
sys.path.insert(0, os.path.dirname(__file__))


def test_single_passphrase(wallet_file, passphrase, verbose=False):
    """Testet eine einzelne Passphrase"""
    import subprocess

    cmd = [
        'python3', 'pywallet.py',
        '-w', wallet_file,
        '--passphrase', passphrase,
        '-d'
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        output = result.stdout

        # Check if decryption was successful
        if 'The wallet is encrypted and the passphrase is correct' in output:
            return True, output
        elif 'The wallet is encrypted and the passphrase is incorrect' in output:
            return False, "Incorrect passphrase"
        else:
            # Parse JSON to check for decrypted keys
            try:
                data = json.loads(output)
                if 'keys' in data and len(data['keys']) > 0:
                    # Check if any key has 'sec' or 'secret' field (decrypted)
                    for key in data['keys']:
                        if 'sec' in key or ('secret' in key and key['secret']):
                            return True, output
            except:
                pass

            return False, "Unknown response"
    except subprocess.TimeoutExpired:
        return False, "Timeout"
    except Exception as e:
        return False, f"Error: {str(e)}"


def test_passphrase_list(wallet_file, passphrase_file, output_file=None):
    """Testet eine Liste von Passphrases aus einer Datei"""
    print("="*70)
    print("PASSPHRASE BRUTE-FORCE / DICTIONARY ATTACK")
    print("="*70)
    print(f"\nWallet: {wallet_file}")
    print(f"Passphrase list: {passphrase_file}\n")

    if not os.path.exists(passphrase_file):
        print(f"ERROR: Passphrase file not found: {passphrase_file}")
        return

    with open(passphrase_file, 'r', encoding='utf-8', errors='ignore') as f:
        passphrases = [line.strip() for line in f if line.strip()]

    total = len(passphrases)
    print(f"Testing {total} passphrases...\n")

    start_time = datetime.now()

    for i, passphrase in enumerate(passphrases, 1):
        if i % 10 == 0:
            elapsed = (datetime.now() - start_time).total_seconds()
            rate = i / elapsed if elapsed > 0 else 0
            eta = (total - i) / rate if rate > 0 else 0
            print(f"[{i}/{total}] Tested {i} passphrases ({rate:.2f}/sec, ETA: {eta:.0f}s)")

        success, result = test_single_passphrase(wallet_file, passphrase)

        if success:
            print("\n" + "="*70)
            print("✓ SUCCESS! PASSPHRASE FOUND!")
            print("="*70)
            print(f"Passphrase: {passphrase}")
            print("="*70 + "\n")

            if output_file:
                with open(output_file, 'w') as f:
                    f.write(result)
                print(f"Decrypted wallet saved to: {output_file}\n")
            else:
                print("Decrypted wallet output:\n")
                print(result)

            return True

    elapsed = (datetime.now() - start_time).total_seconds()
    print(f"\n✗ No matching passphrase found. Tested {total} passphrases in {elapsed:.2f} seconds.")
    return False


def extract_encryption_info(wallet_file):
    """Extrahiert Verschlüsselungsinformationen für externe Tools (hashcat, john)"""
    import subprocess

    print("="*70)
    print("EXTRACTING ENCRYPTION INFO FOR PASSWORD CRACKING TOOLS")
    print("="*70)
    print(f"\nWallet: {wallet_file}\n")

    cmd = ['python3', 'pywallet.py', '-w', wallet_file, '-d']

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        data = json.loads(result.stdout)

        if 'mkey' not in data:
            print("ERROR: No master key found in wallet (wallet not encrypted?)")
            return

        mkey = data['mkey']

        print("[MASTER KEY INFORMATION]")
        print("-"*70)

        salt = mkey.get('salt', '')
        if isinstance(salt, str) and len(salt) > 0:
            print(f"Salt (hex): {salt}")

        iterations = mkey.get('nDerivationIterations', 0)
        print(f"Iterations: {iterations}")

        method = mkey.get('nDerivationMethod', 0)
        print(f"Method: {method} {'(SHA512)' if method == 0 else ''}")

        encrypted_key = mkey.get('encrypted_key', '')
        if isinstance(encrypted_key, str) and len(encrypted_key) > 0:
            print(f"Encrypted Master Key (hex): {encrypted_key}")

        # Format for hashcat
        print("\n[HASHCAT FORMAT]")
        print("-"*70)
        if salt and encrypted_key:
            # Bitcoin Core wallet format for hashcat
            print(f"$bitcoin$64${encrypted_key}${salt}${iterations}$0$0")
            print("\nUsage:")
            print(f"  hashcat -m 11300 -a 0 hash.txt wordlist.txt")
            print(f"  (Mode 11300 = Bitcoin Core wallet)")

        # Show sample encrypted keys
        print("\n[ENCRYPTED PRIVATE KEYS]")
        print("-"*70)
        if 'keys' in data:
            for i, key in enumerate(data['keys'][:3], 1):
                if 'encrypted_privkey' in key:
                    print(f"\nKey #{i}:")
                    print(f"  Address: {key.get('addr', 'N/A')}")
                    print(f"  Public Key: {key.get('pubkey', 'N/A')[:64]}...")
                    print(f"  Encrypted Private Key: {key.get('encrypted_privkey', 'N/A')[:64]}...")

        print("\n" + "="*70)
        print("Use these values with password cracking tools:")
        print("  - hashcat: https://hashcat.net/hashcat/")
        print("  - John the Ripper: https://www.openwall.com/john/")
        print("="*70 + "\n")

    except json.JSONDecodeError:
        print("ERROR: Could not parse wallet data")
        print(result.stdout)
    except Exception as e:
        print(f"ERROR: {str(e)}")


def interactive_decrypt(wallet_file):
    """Interaktiver Modus - fragt nach Passphrase"""
    print("="*70)
    print("INTERACTIVE WALLET DECRYPTION")
    print("="*70)
    print(f"\nWallet: {wallet_file}\n")

    passphrase = getpass.getpass("Enter passphrase (input hidden): ")

    if not passphrase:
        print("ERROR: No passphrase provided")
        return

    print("\nTesting passphrase...")
    success, result = test_single_passphrase(wallet_file, passphrase)

    if success:
        print("\n✓ SUCCESS! Passphrase is correct!\n")

        save = input("Save decrypted wallet to file? (y/n): ").lower()
        if save == 'y':
            output_file = input("Output filename [decrypted_wallet.json]: ").strip()
            if not output_file:
                output_file = "decrypted_wallet.json"

            with open(output_file, 'w') as f:
                f.write(result)
            print(f"\n✓ Decrypted wallet saved to: {output_file}\n")

            # Show summary
            try:
                data = json.loads(result)
                if 'keys' in data:
                    decrypted_count = sum(1 for k in data['keys'] if 'sec' in k)
                    print(f"Total keys decrypted: {decrypted_count}")

                    print("\nFirst 3 decrypted private keys (WIF format):")
                    for i, key in enumerate(data['keys'][:3], 1):
                        if 'sec' in key:
                            print(f"  {i}. {key['addr']}: {key['sec']}")
            except:
                pass
        else:
            print("\nDecrypted wallet output:")
            print(result)
    else:
        print(f"\n✗ FAILED: {result}\n")


def main():
    parser = argparse.ArgumentParser(
        description='Specialized tool for decrypting Bitcoin Core wallet.dat files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode (prompts for passphrase)
  python3 decrypt_wallet.py -w wallet.dat -i

  # Test a single passphrase
  python3 decrypt_wallet.py -w wallet.dat -p "mypassword"

  # Brute-force with passphrase list
  python3 decrypt_wallet.py -w wallet.dat -l passwords.txt -o decrypted.json

  # Extract info for hashcat/john
  python3 decrypt_wallet.py -w wallet.dat -e
        """
    )

    parser.add_argument('-w', '--wallet', required=True,
                        help='Path to wallet.dat file')

    parser.add_argument('-p', '--passphrase',
                        help='Single passphrase to test')

    parser.add_argument('-l', '--list',
                        help='File with list of passphrases (one per line)')

    parser.add_argument('-i', '--interactive', action='store_true',
                        help='Interactive mode (prompts for passphrase)')

    parser.add_argument('-e', '--extract-info', action='store_true',
                        help='Extract encryption info for hashcat/john')

    parser.add_argument('-o', '--output',
                        help='Output file for decrypted wallet (JSON format)')

    args = parser.parse_args()

    if not os.path.exists(args.wallet):
        print(f"ERROR: Wallet file not found: {args.wallet}")
        sys.exit(1)

    # Extract info mode
    if args.extract_info:
        extract_encryption_info(args.wallet)
        return

    # Interactive mode
    if args.interactive:
        interactive_decrypt(args.wallet)
        return

    # Single passphrase mode
    if args.passphrase:
        print("Testing passphrase...")
        success, result = test_single_passphrase(args.wallet, args.passphrase)

        if success:
            print("\n✓ SUCCESS! Passphrase is correct!\n")

            if args.output:
                with open(args.output, 'w') as f:
                    f.write(result)
                print(f"Decrypted wallet saved to: {args.output}\n")
            else:
                print(result)
        else:
            print(f"\n✗ FAILED: {result}\n")
        return

    # Passphrase list mode
    if args.list:
        test_passphrase_list(args.wallet, args.list, args.output)
        return

    # No mode specified
    parser.print_help()


if __name__ == '__main__':
    main()
