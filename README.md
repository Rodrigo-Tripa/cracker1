# cracker1

Minimal SHA-256 hash cracking tool using wordlists.

Designed for Alpine Linux. Fully compatible with Kali Linux and other Linux distributions.

---

## Features

- SHA-256 hash cracking
- Wordlist-based attack
- Flag-based CLI (no interactive menus)
- One-hash-per-file workflow
- Optional custom wordlist support
- Clean input/output separation

---

## Directory Structure

cracker1/
├── cracker1.py

├── wordlist.txt # default wordlist (optional)

├── cripto/ # input hashes

├── des-cripto/ # cracked results


- `cripto/` → input (hashes to crack)
- `des-cripto/` → output (results)
- one file = one SHA-256 hash

---

## Requirements

- Python 3
- tqdm

Install dependencies:

```bash
pip install -r requirements.txt
