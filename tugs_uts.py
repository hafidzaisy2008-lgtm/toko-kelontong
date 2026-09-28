import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# =========================================================
# KONFIGURASI
# =========================================================

DB_NAME = "Toko_Kelontong.db"

# WARNA APLIKASI
HIJAU_GELAP = "#1B5E20"
HIJAU = "#2E7D32"
HIJAU_TERANG = "#43A047"

PUTIH = "#FFFFFF"
ABU = "#F5F5F5"
ABU_TUA = "#E0E0E0"
HITAM = "#212121"

KUNING = "#F9A825"
BIRU = "#1565C0"
UNGU = "#6A1B9A"
MERAH = "#C62828"


# =========================================================
# DATABASE
# =========================================================

def koneksi_db():
    return sqlite3.connect(DB_NAME)


def buat_database():
    with koneksi_db() as conn:
        cur = conn.cursor()

        # Tabel user
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        """)

        # Tabel produk
        cur.execute("""
            CREATE TABLE IF NOT EXISTS produk (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_produk TEXT NOT NULL,
                harga_modal INTEGER NOT NULL,
                harga_jual INTEGER NOT NULL,
                stok INTEGER NOT NULL
            )
        """)

        # Tabel transaksi
        cur.execute("""
            CREATE TABLE IF NOT EXISTS transaksi (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tanggal TEXT NOT NULL,
                total_bayar INTEGER NOT NULL
            )
        """)

        # Detail transaksi
        cur.execute("""
            CREATE TABLE IF NOT EXISTS detail_transaksi (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_transaksi INTEGER NOT NULL,
                id_produk INTEGER NOT NULL,
                jumlah INTEGER NOT NULL,
                subtotal INTEGER NOT NULL,
                FOREIGN KEY (id_transaksi) REFERENCES transaksi(id),
                FOREIGN KEY (id_produk) REFERENCES produk(id)
            )
        """)

        # USER ADMIN
        cur.execute("""
            INSERT OR IGNORE INTO users
            (username, password, role)
            VALUES (?, ?, ?)
        """, ("admin", "cristiano rozikin", "admin"))

        # USER KASIR
        cur.execute("""
            INSERT OR IGNORE INTO users
            (username, password, role)
            VALUES (?, ?, ?)
        """, ("kasir", "cr messi", "kasir"))

        # Produk awal
        cur.execute("SELECT COUNT(*) FROM produk")

        if cur.fetchone()[0] == 0:

            produk = [
                ("Beras 5 Kg", 65000, 75000, 20),
                ("Gula 1 Kg", 15000, 18000, 30),
                ("Minyak Goreng", 19000, 22000, 25),
                ("Mie Instan", 2500, 3500, 100),
                ("Marlong", 18000, 20000, 100)
            ]

            cur.executemany("""
                INSERT INTO produk
                (nama_produk, harga_modal, harga_jual, stok)
                VALUES (?, ?, ?, ?)
            """, produk)


# =========================================================
# FORMAT RUPIAH
# =========================================================

def rupiah(angka):
    return "Rp" + f"{angka:,}".replace(",", ".")


# =========================================================
# APLIKASI
# =========================================================

class AplikasiToko:

    def __init__(self, root):

        self.root = root

        self.root.title("SMART-RETAIL - Unsikuy")
        self.root.geometry("900x600")
        self.root.resizable(False, False)
        self.root.configure(bg=ABU)

        self.user = None
        self.keranjang = {}

        # Style Treeview
        self.style = ttk.Style()

        try:
            self.style.theme_use("clam")
        except:
            pass

        self.style.configure(
            "Treeview",
            background=PUTIH,
            foreground=HITAM,
            rowheight=30,
            fieldbackground=PUTIH,
            font=("Arial", 10)
        )

        self.style.configure(
            "Treeview.Heading",
            background=HIJAU,
            foreground=PUTIH,
            font=("Arial", 10, "bold")
        )

        self.style.map(
            "Treeview",
            background=[("selected", HIJAU_TERANG)],
            foreground=[("selected", PUTIH)]
        )

        buat_database()

        self.halaman_login()


    # =====================================================
    # BERSIHKAN HALAMAN
    # =====================================================

    def bersihkan(self):

        for widget in self.root.winfo_children():
            widget.destroy()


    # =====================================================
    # LOGIN
    # =====================================================

    def halaman_login(self):

        self.bersihkan()

        frame = tk.Frame(
            self.root,
            bg=PUTIH,
            bd=2,
            relief="solid"
        )

        frame.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
            width=430,
            height=420
        )

        # Judul
        tk.Label(
            frame,
            text="SMART-RETAIL",
            font=("Arial", 25, "bold"),
            bg=PUTIH,
            fg=HIJAU_GELAP
        ).pack(pady=(35, 5))

        tk.Label(
            frame,
            text="Sistem Kasir Toko Kelontong",
            font=("Arial", 11),
            bg=PUTIH,
            fg="gray"
        ).pack(pady=(0, 30))

        # Username
        tk.Label(
            frame,
            text="Username",
            font=("Arial", 11, "bold"),
            bg=PUTIH,
            fg=HITAM
        ).pack(anchor="w", padx=50)

        self.entry_username = tk.Entry(
            frame,
            font=("Arial", 12),
            bd=1,
            relief="solid"
        )

        self.entry_username.pack(
            padx=50,
            fill="x",
            ipady=7,
            pady=(5, 15)
        )

        # Password
        tk.Label(
            frame,
            text="Password",
            font=("Arial", 11, "bold"),
            bg=PUTIH,
            fg=HITAM
        ).pack(anchor="w", padx=50)

        self.entry_password = tk.Entry(
            frame,
            font=("Arial", 12),
            bd=1,
            relief="solid",
            show="*"
        )

        self.entry_password.pack(
            padx=50,
            fill="x",
            ipady=7,
            pady=(5, 25)
        )

        # Tombol Login
        tk.Button(
            frame,
            text="LOGIN",
            command=self.login,
            bg=HIJAU,
            fg=PUTIH,
            activebackground=HIJAU_TERANG,
            activeforeground=PUTIH,
            font=("Arial", 11, "bold"),
            bd=0,
            cursor="hand2"
        ).pack(
            padx=50,
            fill="x",
            ipady=10
        )

        tk.Label(
            frame,
            text="Admin / Kasir",
            font=("Arial", 9),
            bg=PUTIH,
            fg="gray"
        ).pack(pady=15)


    # =====================================================
    # LOGIN PROSES
    # =====================================================

    def login(self):

        username = self.entry_username.get()
        password = self.entry_password.get()

        with koneksi_db() as conn:

            cur = conn.cursor()

            cur.execute("""
                SELECT username, role
                FROM users
                WHERE username = ?
                AND password = ?
            """, (username, password))

            hasil = cur.fetchone()

        if hasil:

            self.user = {
                "username": hasil[0],
                "role": hasil[1]
            }

            self.halaman_utama()

        else:

            messagebox.showerror(
                "Login Gagal",
                "Username atau password salah!"
            )


    # =====================================================
    # HALAMAN UTAMA
    # =====================================================

    def halaman_utama(self):

        self.bersihkan()

        # Header
        header = tk.Frame(
            self.root,
            bg=HIJAU_GELAP,
            height=90
        )

        header.pack(fill="x")

        tk.Label(
            header,
            text="SMART-RETAIL",
            font=("Arial", 25, "bold"),
            bg=HIJAU_GELAP,
            fg=PUTIH
        ).pack(side="left", padx=30, pady=20)

        tk.Label(
            header,
            text=f"{self.user['username']} | {self.user['role'].upper()}",
            font=("Arial", 11, "bold"),
            bg=HIJAU_GELAP,
            fg=PUTIH
        ).pack(side="right", padx=30)

        # Area menu
        menu = tk.Frame(
            self.root,
            bg=ABU
        )

        menu.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=40
        )

        tk.Label(
            menu,
            text="MENU UTAMA",
            font=("Arial", 20, "bold"),
            bg=ABU,
            fg=HIJAU_GELAP
        ).pack(pady=(0, 25))

        if self.user["role"] == "admin":

            self.tombol_menu(
                menu,
                "KELOLA PRODUK",
                self.halaman_produk,
                HIJAU
            )

        self.tombol_menu(
            menu,
            "TRANSAKSI PENJUALAN",
            self.halaman_transaksi,
            KUNING
        )

        self.tombol_menu(
            menu,
            "RIWAYAT TRANSAKSI",
            self.halaman_riwayat,
            BIRU
        )

        if self.user["role"] == "admin":

            self.tombol_menu(
                menu,
                "LAPORAN PENJUALAN",
                self.halaman_laporan,
                UNGU
            )

        self.tombol_menu(
            menu,
            "LOGOUT",
            self.logout,
            MERAH
        )


    # =====================================================
    # TOMBOL MENU
    # =====================================================

    def tombol_menu(self, parent, text, command, warna):

        tk.Button(
            parent,
            text=text,
            command=command,
            bg=warna,
            fg=PUTIH,
            activebackground=warna,
            activeforeground=PUTIH,
            font=("Arial", 12, "bold"),
            bd=0,
            cursor="hand2"
        ).pack(
            fill="x",
            pady=6,
            ipady=12
        )


    # =====================================================
    # HALAMAN PRODUK
    # =====================================================

    def halaman_produk(self):

        self.bersihkan()

        # Header
        header = tk.Frame(
            self.root,
            bg=HIJAU_GELAP
        )

        header.pack(fill="x")

        tk.Label(
            header,
            text="KELOLA PRODUK",
            font=("Arial", 22, "bold"),
            bg=HIJAU_GELAP,
            fg=PUTIH
        ).pack(pady=20)

        # Form
        form = tk.Frame(
            self.root,
            bg=ABU
        )

        form.pack(
            fill="x",
            padx=30,
            pady=20
        )

        labels = [
            "Nama Produk",
            "Harga Modal",
            "Harga Jual",
            "Stok"
        ]

        self.entry_nama = tk.Entry(form, font=("Arial", 11))
        self.entry_modal = tk.Entry(form, font=("Arial", 11))
        self.entry_jual = tk.Entry(form, font=("Arial", 11))
        self.entry_stok = tk.Entry(form, font=("Arial", 11))

        entries = [
            self.entry_nama,
            self.entry_modal,
            self.entry_jual,
            self.entry_stok
        ]

        for i in range(4):

            tk.Label(
                form,
                text=labels[i],
                bg=ABU,
                fg=HITAM,
                font=("Arial", 10, "bold")
            ).grid(
                row=0,
                column=i,
                padx=5
            )

            entries[i].grid(
                row=1,
                column=i,
                padx=5,
                ipady=5
            )

        tk.Button(
            form,
            text="TAMBAH PRODUK",
            command=self.tambah_produk,
            bg=HIJAU,
            fg=PUTIH,
            font=("Arial", 10, "bold"),
            bd=0,
            cursor="hand2"
        ).grid(
            row=2,
            column=0,
            columnspan=4,
            pady=15,
            ipadx=20,
            ipady=7
        )

        # Tabel
        table_frame = tk.Frame(
            self.root,
            bg=ABU
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=30
        )

        kolom = (
            "ID",
            "Nama",
            "Harga Modal",
            "Harga Jual",
            "Stok"
        )

        self.tree_produk = ttk.Treeview(
            table_frame,
            columns=kolom,
            show="headings"
        )

        for kol in kolom:

            self.tree_produk.heading(
                kol,
                text=kol
            )

        self.tree_produk.column("ID", width=50)
        self.tree_produk.column("Nama", width=250)
        self.tree_produk.column("Harga Modal", width=130)
        self.tree_produk.column("Harga Jual", width=130)
        self.tree_produk.column("Stok", width=80)

        self.tree_produk.pack(
            fill="both",
            expand=True
        )

        # Tombol bawah
        bottom = tk.Frame(
            self.root,
            bg=ABU
        )

        bottom.pack(
            fill="x",
            padx=30,
            pady=15
        )

        tk.Button(
            bottom,
            text="HAPUS PRODUK",
            command=self.hapus_produk,
            bg=MERAH,
            fg=PUTIH,
            font=("Arial", 10, "bold"),
            bd=0,
            cursor="hand2"
        ).pack(side="left", ipadx=15, ipady=7)

        tk.Button(
            bottom,
            text="KEMBALI",
            command=self.halaman_utama,
            bg=HITAM,
            fg=PUTIH,
            font=("Arial", 10, "bold"),
            bd=0,
            cursor="hand2"
        ).pack(side="right", ipadx=15, ipady=7)

        self.tampilkan_produk_gui()


    # =====================================================
    # TAMPILKAN PRODUK
    # =====================================================

    def tampilkan_produk_gui(self):

        for item in self.tree_produk.get_children():

            self.tree_produk.delete(item)

        with koneksi_db() as conn:

            cur = conn.cursor()

            cur.execute("""
                SELECT id, nama_produk, harga_modal,
                       harga_jual, stok
                FROM produk
                ORDER BY id
            """)

            data = cur.fetchall()

        for row in data:

            self.tree_produk.insert(
                "",
                "end",
                values=(
                    row[0],
                    row[1],
                    rupiah(row[2]),
                    rupiah(row[3]),
                    row[4]
                )
            )


    # =====================================================
    # TAMBAH PRODUK
    # =====================================================

    def tambah_produk(self):

        nama = self.entry_nama.get()
        modal = self.entry_modal.get()
        jual = self.entry_jual.get()
        stok = self.entry_stok.get()

        if not nama or not modal or not jual or not stok:

            messagebox.showwarning(
                "Peringatan",
                "Semua data harus diisi!"
            )

            return

        try:

            modal = int(modal)
            jual = int(jual)
            stok = int(stok)

        except ValueError:

            messagebox.showerror(
                "Error",
                "Harga dan stok harus berupa angka!"
            )

            return

        if modal < 0 or jual < 0 or stok < 0:

            messagebox.showerror(
                "Error",
                "Harga dan stok tidak boleh negatif!"
            )

            return

        with koneksi_db() as conn:

            cur = conn.cursor()

            cur.execute("""
                INSERT INTO produk
                (nama_produk, harga_modal, harga_jual, stok)
                VALUES (?, ?, ?, ?)
            """, (
                nama,
                modal,
                jual,
                stok
            ))

        messagebox.showinfo(
            "Berhasil",
            "Produk berhasil ditambahkan!"
        )

        self.entry_nama.delete(0, tk.END)
        self.entry_modal.delete(0, tk.END)
        self.entry_jual.delete(0, tk.END)
        self.entry_stok.delete(0, tk.END)

        self.tampilkan_produk_gui()


    # =====================================================
    # HAPUS PRODUK
    # =====================================================

    def hapus_produk(self):

        selected = self.tree_produk.selection()

        if not selected:

            messagebox.showwarning(
                "Peringatan",
                "Pilih produk terlebih dahulu!"
            )

            return

        data = self.tree_produk.item(selected[0])

        id_produk = data["values"][0]
        nama_produk = data["values"][1]

        yakin = messagebox.askyesno(
            "Konfirmasi",
            f"Hapus produk '{nama_produk}'?"
        )

        if not yakin:
            return

        with koneksi_db() as conn:

            cur = conn.cursor()

            cur.execute(
                "DELETE FROM produk WHERE id = ?",
                (id_produk,)
            )

        self.tampilkan_produk_gui()

        messagebox.showinfo(
            "Berhasil",
            "Produk berhasil dihapus!"
        )


    # =====================================================
    # HALAMAN TRANSAKSI
    # =====================================================

    def halaman_transaksi(self):

        self.bersihkan()

        self.keranjang = {}

        # Header
        header = tk.Frame(
            self.root,
            bg=HIJAU_GELAP
        )

        header.pack(fill="x")

        tk.Label(
            header,
            text="TRANSAKSI PENJUALAN",
            font=("Arial", 22, "bold"),
            bg=HIJAU_GELAP,
            fg=PUTIH
        ).pack(pady=20)

        # Input
        form = tk.Frame(
            self.root,
            bg=ABU
        )

        form.pack(
            fill="x",
            padx=30,
            pady=20
        )

        tk.Label(
            form,
            text="ID Produk",
            bg=ABU,
            font=("Arial", 10, "bold")
        ).pack(side="left")

        self.entry_id_produk = tk.Entry(
            form,
            font=("Arial", 11),
            width=10
        )

        self.entry_id_produk.pack(
            side="left",
            padx=10,
            ipady=5
        )

        tk.Label(
            form,
            text="Jumlah",
            bg=ABU,
            font=("Arial", 10, "bold")
        ).pack(side="left")

        self.entry_jumlah = tk.Entry(
            form,
            font=("Arial", 11),
            width=10
        )

        self.entry_jumlah.pack(
            side="left",
            padx=10,
            ipady=5
        )

        tk.Button(
            form,
            text="TAMBAH",
            command=self.tambah_keranjang,
            bg=HIJAU,
            fg=PUTIH,
            font=("Arial", 10, "bold"),
            bd=0,
            cursor="hand2"
        ).pack(
            side="left",
            ipadx=15,
            ipady=6
        )

        # Keranjang
        frame_table = tk.Frame(
            self.root,
            bg=ABU
        )

        frame_table.pack(
            fill="both",
            expand=True,
            padx=30
        )

        kolom = (
            "ID",
            "Nama",
            "Harga",
            "Jumlah",
            "Subtotal"
        )

        self.tree_keranjang = ttk.Treeview(
            frame_table,
            columns=kolom,
            show="headings"
        )

        for kol in kolom:

            self.tree_keranjang.heading(
                kol,
                text=kol
            )

        self.tree_keranjang.pack(
            fill="both",
            expand=True
        )

        # Total
        self.label_total = tk.Label(
            self.root,
            text="TOTAL: Rp0",
            font=("Arial", 18, "bold"),
            bg=ABU,
            fg=HIJAU_GELAP
        )

        self.label_total.pack(
            pady=10
        )

        # Bayar
        bayar_frame = tk.Frame(
            self.root,
            bg=ABU
        )

        bayar_frame.pack(
            fill="x",
            padx=30,
            pady=10
        )

        tk.Label(
            bayar_frame,
            text="Uang Bayar",
            bg=ABU,
            font=("Arial", 11, "bold")
        ).pack(side="left")

        self.entry_bayar = tk.Entry(
            bayar_frame,
            font=("Arial", 12)
        )

        self.entry_bayar.pack(
            side="left",
            padx=10,
            ipady=5
        )

        tk.Button(
            bayar_frame,
            text="BAYAR",
            command=self.proses_bayar,
            bg=KUNING,
            fg=HITAM,
            font=("Arial", 11, "bold"),
            bd=0,
            cursor="hand2"
        ).pack(
            side="left",
            ipadx=20,
            ipady=7
        )

        tk.Button(
            bayar_frame,
            text="KEMBALI",
            command=self.halaman_utama,
            bg=HITAM,
            fg=PUTIH,
            font=("Arial", 10, "bold"),
            bd=0,
            cursor="hand2"
        ).pack(
            side="right",
            ipadx=15,
            ipady=7
        )


    # =====================================================
    # TAMBAH KERANJANG
    # =====================================================

    def tambah_keranjang(self):

        try:

            id_produk = int(
                self.entry_id_produk.get()
            )

            jumlah = int(
                self.entry_jumlah.get()
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "ID produk dan jumlah harus angka!"
            )

            return

        if jumlah <= 0:

            messagebox.showwarning(
                "Peringatan",
                "Jumlah harus lebih dari 0!"
            )

            return

        with koneksi_db() as conn:

            cur = conn.cursor()

            cur.execute("""
                SELECT nama_produk,
                       harga_jual,
                       stok
                FROM produk
                WHERE id = ?
            """, (id_produk,))

            produk = cur.fetchone()

        if not produk:

            messagebox.showerror(
                "Error",
                "Produk tidak ditemukan!"
            )

            return

        nama, harga, stok = produk

        jumlah_lama = self.keranjang.get(
            id_produk,
            0
        )

        if jumlah_lama + jumlah > stok:

            messagebox.showwarning(
                "Stok Tidak Cukup",
                f"Stok tersedia: {stok}"
            )

            return

        self.keranjang[id_produk] = jumlah_lama + jumlah

        self.tampilkan_keranjang()

        self.entry_id_produk.delete(0, tk.END)
        self.entry_jumlah.delete(0, tk.END)


    # =====================================================
    # TAMPILKAN KERANJANG
    # =====================================================

    def tampilkan_keranjang(self):

        for item in self.tree_keranjang.get_children():

            self.tree_keranjang.delete(item)

        total = 0

        with koneksi_db() as conn:

            cur = conn.cursor()

            for id_produk, jumlah in self.keranjang.items():

                cur.execute("""
                    SELECT nama_produk, harga_jual
                    FROM produk
                    WHERE id = ?
                """, (id_produk,))

                produk = cur.fetchone()

                if produk:

                    nama, harga = produk

                    subtotal = harga * jumlah

                    total += subtotal

                    self.tree_keranjang.insert(
                        "",
                        "end",
                        values=(
                            id_produk,
                            nama,
                            rupiah(harga),
                            jumlah,
                            rupiah(subtotal)
                        )
                    )

        self.label_total.config(
            text=f"TOTAL: {rupiah(total)}"
        )


    # =====================================================
    # PROSES BAYAR
    # =====================================================

    def proses_bayar(self):

        if not self.keranjang:

            messagebox.showwarning(
                "Peringatan",
                "Keranjang masih kosong!"
            )

            return

        try:

            uang_bayar = int(
                self.entry_bayar.get()
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Uang bayar harus berupa angka!"
            )

            return

        total = 0

        with koneksi_db() as conn:

            cur = conn.cursor()

            for id_produk, jumlah in self.keranjang.items():

                cur.execute("""
                    SELECT harga_jual, stok
                    FROM produk
                    WHERE id = ?
                """, (id_produk,))

                data = cur.fetchone()

                if not data:
                    continue

                harga, stok = data

                total += harga * jumlah

                if jumlah > stok:

                    messagebox.showerror(
                        "Error",
                        "Stok produk tidak mencukupi!"
                    )

                    return

        if uang_bayar < total:

            messagebox.showwarning(
                "Uang Kurang",
                f"Total: {rupiah(total)}\n"
                f"Uang: {rupiah(uang_bayar)}"
            )

            return

        kembalian = uang_bayar - total

        tanggal = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        with koneksi_db() as conn:

            cur = conn.cursor()

            # Simpan transaksi
            cur.execute("""
                INSERT INTO transaksi
                (tanggal, total_bayar)
                VALUES (?, ?)
            """, (tanggal, total))

            id_transaksi = cur.lastrowid

            # Detail transaksi
            for id_produk, jumlah in self.keranjang.items():

                cur.execute("""
                    SELECT harga_jual
                    FROM produk
                    WHERE id = ?
                """, (id_produk,))

                harga = cur.fetchone()[0]

                subtotal = harga * jumlah

                cur.execute("""
                    INSERT INTO detail_transaksi
                    (id_transaksi, id_produk, jumlah, subtotal)
                    VALUES (?, ?, ?, ?)
                """, (
                    id_transaksi,
                    id_produk,
                    jumlah,
                    subtotal
                ))

                # Kurangi stok
                cur.execute("""
                    UPDATE produk
                    SET stok = stok - ?
                    WHERE id = ?
                """, (
                    jumlah,
                    id_produk
                ))

        self.cetak_struk(
            id_transaksi,
            total,
            uang_bayar,
            kembalian
        )


    # =====================================================
    # CETAK STRUK
    # =====================================================

    def cetak_struk(
        self,
        id_transaksi,
        total,
        uang_bayar,
        kembalian
    ):

        window = tk.Toplevel(
            self.root
        )

        window.title("Struk Pembelian")
        window.geometry("450x550")

        text = tk.Text(
            window,
            font=("Courier New", 10),
            bg=PUTIH,
            fg=HITAM
        )

        text.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        text.insert(
            tk.END,
            "====================================\n"
        )

        text.insert(
            tk.END,
            "          SMART-RETAIL\n"
        )

        text.insert(
            tk.END,
            "       TOKO KELONTONG\n"
        )

        text.insert(
            tk.END,
            "====================================\n"
        )

        text.insert(
            tk.END,
            f"Transaksi : #{id_transaksi}\n"
        )

        text.insert(
            tk.END,
            f"Tanggal   : {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n"
        )

        text.insert(
            tk.END,
            "------------------------------------\n"
        )

        with koneksi_db() as conn:

            cur = conn.cursor()

            for id_produk, jumlah in self.keranjang.items():

                cur.execute("""
                    SELECT nama_produk, harga_jual
                    FROM produk
                    WHERE id = ?
                """, (id_produk,))

                produk = cur.fetchone()

                if produk:

                    nama, harga = produk

                    subtotal = harga * jumlah

                    text.insert(
                        tk.END,
                        f"{nama}\n"
                    )

                    text.insert(
                        tk.END,
                        f"{jumlah} x {rupiah(harga)}\n"
                    )

                    text.insert(
                        tk.END,
                        f"Subtotal: {rupiah(subtotal)}\n\n"
                    )

        text.insert(
            tk.END,
            "------------------------------------\n"
        )

        text.insert(
            tk.END,
            f"TOTAL     : {rupiah(total)}\n"
        )

        text.insert(
            tk.END,
            f"BAYAR     : {rupiah(uang_bayar)}\n"
        )

        text.insert(
            tk.END,
            f"KEMBALIAN : {rupiah(kembalian)}\n"
        )

        text.insert(
            tk.END,
            "====================================\n"
        )

        text.insert(
            tk.END,
            "        TERIMA KASIH 🙏\n"
        )

        text.insert(
            tk.END,
            "====================================\n"
        )

        text.config(
            state="disabled"
        )

        self.keranjang = {}

        self.halaman_transaksi()


    # =====================================================
    # RIWAYAT TRANSAKSI
    # =====================================================

    def halaman_riwayat(self):

        self.bersihkan()

        header = tk.Frame(
            self.root,
            bg=HIJAU_GELAP
        )

        header.pack(fill="x")

        tk.Label(
            header,
            text="RIWAYAT TRANSAKSI",
            font=("Arial", 22, "bold"),
            bg=HIJAU_GELAP,
            fg=PUTIH
        ).pack(pady=20)

        frame = tk.Frame(
            self.root,
            bg=ABU
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=20
        )

        kolom = (
            "ID",
            "Tanggal",
            "Total"
        )

        tree = ttk.Treeview(
            frame,
            columns=kolom,
            show="headings"
        )

        for kol in kolom:

            tree.heading(
                kol,
                text=kol
            )

        tree.pack(
            fill="both",
            expand=True
        )

        with koneksi_db() as conn:

            cur = conn.cursor()

            cur.execute("""
                SELECT id, tanggal, total_bayar
                FROM transaksi
                ORDER BY id DESC
            """)

            data = cur.fetchall()

        for row in data:

            tree.insert(
                "",
                "end",
                values=(
                    row[0],
                    row[1],
                    rupiah(row[2])
                )
            )

        tk.Button(
            self.root,
            text="KEMBALI",
            command=self.halaman_utama,
            bg=HITAM,
            fg=PUTIH,
            font=("Arial", 10, "bold"),
            bd=0,
            cursor="hand2"
        ).pack(
            pady=15,
            ipadx=20,
            ipady=7
        )


    # =====================================================
    # LAPORAN PENJUALAN
    # =====================================================

    def halaman_laporan(self):

        self.bersihkan()

        header = tk.Frame(
            self.root,
            bg=HIJAU_GELAP
        )

        header.pack(fill="x")

        tk.Label(
            header,
            text="LAPORAN PENJUALAN",
            font=("Arial", 22, "bold"),
            bg=HIJAU_GELAP,
            fg=PUTIH
        ).pack(pady=20)

        frame = tk.Frame(
            self.root,
            bg=ABU
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=50,
            pady=30
        )

        with koneksi_db() as conn:

            cur = conn.cursor()

            # Jumlah transaksi
            cur.execute(
                "SELECT COUNT(*) FROM transaksi"
            )

            jumlah_transaksi = cur.fetchone()[0]

            # Total penjualan
            cur.execute(
                "SELECT COALESCE(SUM(total_bayar), 0) FROM transaksi"
            )

            total_penjualan = cur.fetchone()[0]

            # Produk terlaris
            cur.execute("""
                SELECT p.nama_produk,
                       SUM(d.jumlah) AS total_terjual
                FROM detail_transaksi d
                JOIN produk p
                ON d.id_produk = p.id
                GROUP BY d.id_produk
                ORDER BY total_terjual DESC
                LIMIT 1
            """)

            produk_terlaris = cur.fetchone()

        # Kartu transaksi
        self.kartu_laporan(
            frame,
            "JUMLAH TRANSAKSI",
            str(jumlah_transaksi),
            BIRU
        ).pack(
            fill="x",
            pady=8
        )

        self.kartu_laporan(
            frame,
            "TOTAL PENJUALAN",
            rupiah(total_penjualan),
            HIJAU
        ).pack(
            fill="x",
            pady=8
        )

        if produk_terlaris:

            nama = produk_terlaris[0]
            jumlah = produk_terlaris[1]

        else:

            nama = "-"
            jumlah = 0

        self.kartu_laporan(
            frame,
            "PRODUK TERLARIS",
            f"{nama} ({jumlah} terjual)",
            UNGU
        ).pack(
            fill="x",
            pady=8
        )

        tk.Button(
            self.root,
            text="KEMBALI",
            command=self.halaman_utama,
            bg=HITAM,
            fg=PUTIH,
            font=("Arial", 10, "bold"),
            bd=0,
            cursor="hand2"
        ).pack(
            pady=15,
            ipadx=20,
            ipady=7
        )


    # =====================================================
    # KARTU LAPORAN
    # =====================================================

    def kartu_laporan(
        self,
        parent,
        judul,
        nilai,
        warna
    ):

        frame = tk.Frame(
            parent,
            bg=warna
        )

        tk.Label(
            frame,
            text=judul,
            font=("Arial", 11, "bold"),
            bg=warna,
            fg=PUTIH
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 2)
        )

        tk.Label(
            frame,
            text=nilai,
            font=("Arial", 20, "bold"),
            bg=warna,
            fg=PUTIH
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

        return frame


    # =====================================================
    # LOGOUT
    # =====================================================

    def logout(self):

        yakin = messagebox.askyesno(
            "Logout",
            "Yakin ingin keluar?"
        )

        if yakin:

            self.user = None
            self.keranjang = {}

            self.halaman_login()


# =========================================================
# JALANKAN PROGRAM
# =========================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = AplikasiToko(root)

    root.mainloop()