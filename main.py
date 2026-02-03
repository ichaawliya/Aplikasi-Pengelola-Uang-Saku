import json
import os
from datetime import datetime

SALDO_FILE = "saldo.json"
saldo = 0
transactions = []  # list to store transaction records

def load_saldo():
    global saldo, transactions
    if os.path.exists(SALDO_FILE):
        try:
            with open(SALDO_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                saldo = float(data.get("saldo", 0))
                transactions = data.get("transactions", []) or []
        except Exception:
            saldo = 0
            transactions = []

def save_saldo():
    try:
        with open(SALDO_FILE, 'w', encoding='utf-8') as f:
            json.dump({"saldo": saldo, "transactions": transactions}, f)
    except Exception:
        print("Gagal menyimpan saldo.")

def tambah_pemasukan():
    global saldo, transactions
    try:
        jumlah = float(input("Masukkan jumlah pemasukan: "))
        if jumlah <= 0:
            print("Jumlah harus lebih dari 0")
            return
        saldo += jumlah
        transactions.append({"type": "pemasukan", "amount": jumlah, "time": datetime.now().isoformat()})
        save_saldo()
        print(f"Pemasukan berhasil ditambahkan. Saldo saat ini: {saldo:.2f}")
    except ValueError:
        print("Input tidak valid. Masukkan angka.")

def tambah_pengeluaran():
    global saldo, transactions
    try:
        jumlah = float(input("Masukkan jumlah pengeluaran: "))
        if jumlah <= 0:
            print("Jumlah harus lebih dari 0")
            return
        if jumlah > saldo:
            print("Saldo tidak cukup")
            return
        saldo -= jumlah
        transactions.append({"type": "pengeluaran", "amount": jumlah, "time": datetime.now().isoformat()})
        save_saldo()
        print(f"Pengeluaran berhasil. Saldo saat ini: {saldo:.2f}")
    except ValueError:
        print("Input tidak valid. Masukkan angka.")

def lihat_saldo():
    print(f"Saldo saat ini: {saldo:.2f}")

def laporan():
    total_in = sum(t.get('amount', 0) for t in transactions if t.get('type') == 'pemasukan')
    total_out = sum(t.get('amount', 0) for t in transactions if t.get('type') == 'pengeluaran')
    print("=== Laporan Rekap ===")
    print(f"Total pemasukan: {total_in:.2f}")
    print(f"Total pengeluaran: {total_out:.2f}")
    print("--- Riwayat transaksi ---")
    if not transactions:
        print("Belum ada transaksi.")
        return
    for i, t in enumerate(transactions, 1):
        ttime = t.get('time', '')
        ttype = t.get('type', '')
        tamount = t.get('amount', 0)
        print(f"{i}. {ttype.capitalize()} - {tamount:.2f} ({ttime})")

def menu():
    print("=== Aplikasi Pengelola Uang Saku ===")
    print("1. Tambah pemasukan")
    print("2. Tambah pengeluaran")
    print("3. Lihat saldo")
    print("4. Keluar")
    print("5. Laporan")

load_saldo()
while True:
    menu()
    pilihan = input("Pilih menu: ")

    if pilihan == "1":
        tambah_pemasukan()
    elif pilihan == "2":
        tambah_pengeluaran()
    elif pilihan == "3":
        lihat_saldo()
    elif pilihan == "4":
        save_saldo()
        print("Terima kasih! Saldo disimpan.")
        break
    elif pilihan == "5":
        laporan()
    else:
        print("Pilihan tidak valid")