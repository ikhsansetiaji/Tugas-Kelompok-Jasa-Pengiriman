import tkinter as tk
from tkinter import messagebox
import uuid

class Paket:
    def __init__(self, pengirim, penerima, berat, jarak, kurir, kategori, promo=None, asuransi=False):
        self.id = str(uuid.uuid4())[:8]  # Generate unique ID
        self.pengirim = pengirim
        self.penerima = penerima
        self.berat = berat
        self.jarak = jarak
        self.kurir = kurir
        self.kategori = kategori
        self.promo = promo
        self.asuransi = asuransi
        self.status = "Diterima"

    def hitung_biaya(self):
        biaya_tetap = 5000  # Biaya tetap
        biaya_berat = self.berat * 2000  # Biaya per kg
        biaya_jarak = self.jarak * 1000  # Biaya per km

        # Sesuaikan biaya berdasarkan kategori
        if self.kategori == "Reguler":
            pengali_kategori = 1.0
        elif self.kategori == "Ekspres":
            pengali_kategori = 1.5
        elif self.kategori == "Same-Day":
            pengali_kategori = 2.0

        total_biaya = (biaya_tetap + biaya_berat + biaya_jarak) * pengali_kategori

        if self.asuransi:
            total_biaya += 10000  # Biaya asuransi

        if self.promo:
            total_biaya *= (1 - self.promo.diskon)

        return total_biaya

    def perbarui_status(self):
        if self.status == "Diterima":
            self.status = "Dalam Perjalanan"
        elif self.status == "Dalam Perjalanan":
            self.status = "Terkirim"

class Promo:
    def __init__(self, kode, diskon):
        self.kode = kode
        self.diskon = diskon  # Diskon dalam bentuk pecahan (misal, 0.1 untuk 10%)

class Kurir:
    def __init__(self, nama):
        self.id = str(uuid.uuid4())[:8]
        self.nama = nama
        self.paket = []

    def tambah_paket(self, paket):
        self.paket.append(paket)

    def get_riwayat(self):
        return [f"{p.id} - {p.pengirim} ke {p.penerima} ({p.status})" for p in self.paket]

class AplikasiLogistik:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Jasa Pengiriman Barang")

        self.paket = []
        self.promos = {
            "DISKON10": Promo("DISKON10", 0.1),
            "DISKON20": Promo("DISKON20", 0.2)
        }
        
        # Inisialisasi kurir
        self.kurir = {
            "Atang": Kurir("Atang"),
            "Asep": Kurir("Asep"),
            "Malik": Kurir("Malik")
        }

        # Komponen GUI
        self.create_widgets()

    def create_widgets(self):
        # Frame untuk input data paket
        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.pack(pady=10)

        tk.Label(frame, text="Nama Pengirim:").grid(row=0, column=0, sticky="w")
        self.pengirim_entry = tk.Entry(frame, width=30)
        self.pengirim_entry.grid(row=0, column=1)

        tk.Label(frame, text="Nama Penerima:").grid(row=1, column=0, sticky="w")
        self.penerima_entry = tk.Entry(frame, width=30)
        self.penerima_entry.grid(row=1, column=1)

        tk.Label(frame, text="Berat (kg):").grid(row=2, column=0, sticky="w")
        self.berat_entry = tk.Entry(frame, width=30)
        self.berat_entry.grid(row=2, column=1)

        tk.Label(frame, text="Kategori Pengiriman:").grid(row=3, column=0, sticky="w")
        self.kategori_var = tk.StringVar(value="Reguler")
        self.kategori_menu = tk.OptionMenu(frame, self.kategori_var, "Reguler", "Ekspres", "Same-Day")
        self.kategori_menu.grid(row=3, column=1, sticky="w")

        tk.Label(frame, text="Jarak (km):").grid(row=4, column=0, sticky="w")
        self.jarak_entry = tk.Entry(frame, width=30)
        self.jarak_entry.grid(row=4, column=1)

        tk.Label(frame, text="Kurir:").grid(row=5, column=0, sticky="w")
        self.kurir_var = tk.StringVar(value="Atang")
        tk.OptionMenu(frame, self.kurir_var, *self.kurir.keys()).grid(row=5, column=1, sticky="w")

        tk.Label(frame, text="Kode Promo:").grid(row=6, column=0, sticky="w")
        self.promo_entry = tk.Entry(frame, width=30)
        self.promo_entry.grid(row=6, column=1)

        self.asuransi_var = tk.BooleanVar()
        tk.Checkbutton(frame, text="Tambahkan Asuransi (Rp 10,000)", variable=self.asuransi_var).grid(row=7, column=0, columnspan=2, sticky="w")

        tk.Button(frame, text="Tambah Paket", command=self.tambah_paket).grid(row=8, column=0, columnspan=2, pady=10)

        # Frame untuk daftar paket
        self.list_frame = tk.Frame(self.root, padx=10, pady=10)
        self.list_frame.pack(pady=10)

        self.daftar_paket = tk.Listbox(self.list_frame, width=80, height=15)
        self.daftar_paket.pack(side=tk.LEFT, fill=tk.BOTH)

        scrollbar = tk.Scrollbar(self.list_frame, orient=tk.VERTICAL, command=self.daftar_paket.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.daftar_paket.config(yscrollcommand=scrollbar.set)

        # Frame untuk tindakan paket
        action_frame = tk.Frame(self.root, padx=10, pady=10)
        action_frame.pack(pady=10)

        tk.Button(action_frame, text="Lacak Paket", command=self.lacak_paket).grid(row=0, column=0, padx=5)
        tk.Button(action_frame, text="Perbarui Status", command=self.perbarui_status_paket).grid(row=0, column=1, padx=5)
        tk.Button(action_frame, text="Hapus Paket", command=self.hapus_paket).grid(row=0, column=2, padx=5)
        tk.Button(action_frame, text="Riwayat Kurir", command=self.riwayat_kurir).grid(row=0, column=3, padx=5)

    def tambah_paket(self):
        pengirim = self.pengirim_entry.get()
        penerima = self.penerima_entry.get()
        try:
            berat = float(self.berat_entry.get())
            jarak = float(self.jarak_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Berat dan jarak harus berupa angka.")
            return

        if not pengirim or not penerima:
            messagebox.showerror("Error", "Nama pengirim dan penerima harus diisi.")
            return

        nama_kurir = self.kurir_var.get()
        kurir = self.kurir[nama_kurir]
        promo_kode = self.promo_entry.get().upper()
        promo = self.promos.get(promo_kode)
        asuransi = self.asuransi_var.get()
        kategori = self.kategori_var.get()

        paket = Paket(pengirim, penerima, berat, jarak, kurir, kategori, promo, asuransi)
        self.paket.append(paket)
        kurir.tambah_paket(paket)

        self.daftar_paket.insert(tk.END, f"{paket.id} - {paket.pengirim} ke {paket.penerima} ({paket.kategori}, {paket.status})")

        self.pengirim_entry.delete(0, tk.END)
        self.penerima_entry.delete(0, tk.END)
        self.berat_entry.delete(0, tk.END)
        self.jarak_entry.delete(0, tk.END)
        self.promo_entry.delete(0, tk.END)
        self.asuransi_var.set(False)

    def lacak_paket(self):
        selected = self.daftar_paket.curselection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih paket untuk dilacak.")
            return

        index = selected[0]
        paket = self.paket[index]
        biaya = paket.hitung_biaya()

        info = (
            f"ID Paket: {paket.id}\n"
            f"Pengirim: {paket.pengirim}\n"
            f"Penerima: {paket.penerima}\n"
            f"Kurir: {paket.kurir.nama}\n"
            f"Kategori: {paket.kategori}\n"
            f"Berat: {paket.berat} kg\n"
            f"Jarak: {paket.jarak} km\n"
            f"Promo: {paket.promo.kode if paket.promo else 'Tidak Ada'}\n"
            f"Asuransi: {'Ya' if paket.asuransi else 'Tidak'}\n"
            f"Status: {paket.status}\n"
            f"Biaya Pengiriman: Rp {biaya:,.0f}"
        )

        messagebox.showinfo("Detail Paket", info)

    def perbarui_status_paket(self):
        selected = self.daftar_paket.curselection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih paket untuk diperbarui statusnya.")
            return

        index = selected[0]
        paket = self.paket[index]
        paket.perbarui_status()

        self.daftar_paket.delete(index)
        self.daftar_paket.insert(index, f"{paket.id} - {paket.pengirim} ke {paket.penerima} ({paket.status})")
        messagebox.showinfo("Sukses", "Status paket berhasil diperbarui.")

    def hapus_paket(self):
        selected = self.daftar_paket.curselection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih paket untuk dihapus.")
            return

        index = selected[0]
        paket = self.paket.pop(index)
        paket.kurir.paket.remove(paket)
        self.daftar_paket.delete(index)
        messagebox.showinfo("Sukses", "Paket berhasil dihapus.")

    def riwayat_kurir(self):
        nama_kurir = self.kurir_var.get()
        kurir = self.kurir[nama_kurir]
        riwayat = kurir.get_riwayat()

        if not riwayat:
            messagebox.showinfo("Riwayat Kurir", f"Kurir {nama_kurir} belum memiliki riwayat pengiriman.")
        else:
            riwayat_str = "\n".join(riwayat)
            messagebox.showinfo("Riwayat Kurir", f"Riwayat pengiriman oleh {nama_kurir}:\n\n{riwayat_str}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AplikasiLogistik(root)
    root.mainloop()

