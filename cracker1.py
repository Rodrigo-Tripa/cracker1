#!/usr/bin/env python3

import argparse
import hashlib
import os
import re
import sys
from tqdm import tqdm

CRIPTO_DIR = "cripto"
DESCRIPTO_DIR = "des-cripto"
DEFAULT_WORDLIST = "wordlist.txt"


def listar_hashes():
    if not os.path.isdir(CRIPTO_DIR):
        print("[-] Pasta cripto/ não existe.")
        sys.exit(1)

    files = sorted(f for f in os.listdir(CRIPTO_DIR) if f.endswith(".txt"))

    if not files:
        print("[-] Nenhum hash encontrado em cripto/")
        sys.exit(1)

    print("[*] Hashes disponíveis:\n")
    for i, f in enumerate(files, 1):
        print(f"  [{i}] {f}")

    return files


def extrair_hash(path):
    with open(path, "r", errors="ignore") as f:
        data = f.read().lower()

    match = re.search(r"\b[a-f0-9]{64}\b", data)
    if not match:
        print("[-] Nenhum SHA-256 válido encontrado.")
        sys.exit(1)

    return match.group()


def crack_hash(target_hash, wordlist_path):
    if not os.path.isfile(wordlist_path):
        print(f"[-] Wordlist não encontrada: {wordlist_path}")
        sys.exit(1)

    with open(wordlist_path, "r", errors="ignore") as f:
        total = sum(1 for _ in f)

    with open(wordlist_path, "r", errors="ignore") as f:
        for line in tqdm(f, total=total, desc="Cracking", unit="pwd"):
            pwd = line.strip()
            if not pwd:
                continue

            if hashlib.sha256(pwd.encode()).hexdigest() == target_hash:
                return pwd

    return None


def guardar_resultado(hash_value, password):
    os.makedirs(DESCRIPTO_DIR, exist_ok=True)
    out = os.path.join(DESCRIPTO_DIR, "resultado.txt")

    with open(out, "w") as f:
        f.write(f"HASH: {hash_value}\n")
        f.write(f"PASSWORD: {password}\n")

    print(f"[+] Resultado guardado em {out}")


def main():
    parser = argparse.ArgumentParser(
        description="Minimal SHA-256 hash cracker"
    )

    parser.add_argument(
        "-crack",
        action="store_true",
        help="Crack SHA-256 hash"
    )

    parser.add_argument(
        "-n",
        metavar="NUMBER",
        type=int,
        help="Número do hash na pasta cripto/"
    )

    parser.add_argument(
        "-f",
        metavar="FILE",
        help="Caminho para ficheiro de hash"
    )

    parser.add_argument(
        "-w",
        metavar="WORDLIST",
        help="Wordlist personalizada"
    )

    args = parser.parse_args()

    if not args.crack:
        parser.print_help()
        sys.exit(0)

    # Escolha da wordlist
    wordlist = args.w if args.w else DEFAULT_WORDLIST

    # Escolha do hash
    if args.f:
        hash_path = args.f

    elif args.n:
        files = listar_hashes()
        if args.n < 1 or args.n > len(files):
            print("[-] Número inválido.")
            sys.exit(1)

        hash_path = os.path.join(CRIPTO_DIR, files[args.n - 1])

    else:
        listar_hashes()
        sys.exit(0)

    target = extrair_hash(hash_path)
    print(f"\n[*] Target: {target}")
    print(f"[*] Wordlist: {wordlist}\n")

    result = crack_hash(target, wordlist)

    if result:
        print(f"\n[+] PASSWORD FOUND: {result}")
        guardar_resultado(target, result)
    else:
        print("\n[-] Hash não quebrado.")


if __name__ == "__main__":
    main()
