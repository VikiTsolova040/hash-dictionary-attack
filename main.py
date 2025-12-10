import hashlib
import json
import random
import string
import time
import os


# 1. GENERATOR NA 1 000 000 PAROLI


def generate_password_list(n=1_000_000):
    passwords = []

    common = ["123456", "password", "qwerty", "abc123", "admin",
              "123123", "letmein", "welcome", "iloveyou"]

    passwords.extend(common)

    while len(passwords) < n:
        length = random.randint(6, 12)
        pw = "".join(random.choices(string.ascii_lowercase + string.digits, k=length))
        passwords.append(pw)

    return passwords



# 2. HASHVANE S 5 ALGORITMMA


def hash_password(password, algorithm):
    if algorithm == "md5":
        return hashlib.md5(password.encode()).hexdigest()
    elif algorithm == "sha1":
        return hashlib.sha1(password.encode()).hexdigest()
    elif algorithm == "sha256":
        return hashlib.sha256(password.encode()).hexdigest()
    elif algorithm == "sha512":
        return hashlib.sha512(password.encode()).hexdigest()
    elif algorithm == "sha3_256":
        return hashlib.sha3_256(password.encode()).hexdigest()
    else:
        return None



# 3. GENERACIYA NA HASH TABLICITE


def generate_hash_tables():
    print(">> Generirane na 1 000 000 paroli...")
    passwords = generate_password_list()

    algorithms = ["md5", "sha1", "sha256", "sha512", "sha3_256"]
    tables = {algo: {} for algo in algorithms}

    print(">> Hashvane... (tova moje da otneme 30-60 sekundi)")
    start = time.time()

    for pw in passwords:
        for algo in algorithms:
            tables[algo][hash_password(pw, algo)] = pw

    end = time.time()
    print(f">> Gotovo za {end - start:.2f} sekundi.")

    with open("hash_tables.json", "w", encoding="utf-8") as f:
        json.dump(tables, f)

    print(">> Failut hash_tables.json e zapisан uspeshno!")



# 4. TURSENE NA PAROLA PO HASH


def search_password(h):
    # 1) Proverka dali failut sushtestvuva
    if not os.path.exists("hash_tables.json"):
        print("!! Greshka: purvo generirai hash tablicite (opc. 1).")
        return

    # 2) Proverka dali failut e prazen (0 bytes)
    if os.path.getsize("hash_tables.json") == 0:
        print("!! Greshka: failut hash_tables.json e prazen. Generirai go nanovo (opc. 1).")
        return

    # 3) Opit za chetene
    try:
        with open("hash_tables.json", "r", encoding="utf-8") as f:
            tables = json.load(f)
    except json.JSONDecodeError:
        print("!! Greshka: failut hash_tables.json e povreden. Generirai go nanovo (opc. 1).")
        return

    # 4) Validaciya dali ima vsichki algoritumi
    required = ["md5", "sha1", "sha256", "sha512", "sha3_256"]
    for r in required:
        if r not in tables:
            print("!! Greshka: hash tablicite ne sa pulni. Generirai gi nanovo (opc. 1).")
            return

    # 5) Realno tursene
    for algo, table in tables.items():
        if h in table:
            print(f">> Namereno! Algoritum: {algo.upper()} | Parola: {table[h]}")
            return

    print(">> Nqma namerena parola za tozi hash.")



# 5. MENU


def main():
    while True:
        print("\n=== HASH TOOL ===")
        print("1. Generirai hash tablici (1 000 000 paroli)")
        print("2. Tursi parola po hash")
        print("3. Exit")
        choice = input("Izberi: ")

        if choice == "1":
            generate_hash_tables()
        elif choice == "2":
            h = input("Vuvedi hash: ")
            search_password(h)
        elif choice == "3":
            print("Izliza...")
            break
        else:
            print("Nevaliden izbor!")


if __name__ == "__main__":
    main()
