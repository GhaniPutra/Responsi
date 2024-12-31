import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import date
import random

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="retail_db"
    )
    
def generate_random_id():
    return random.randint(10000, 99999)

def admin_menu(parent):
    def fetch_data():
        for i in tree.get_children():
            tree.delete(i)
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM produk")
        rows = cursor.fetchall()
        for row in rows:
            tree.insert("", "end", values=row)
        cursor.close()
        db.close()

    def tambah_produk():
        nama_produk = entry_nama.get()
        harga = entry_harga.get()
        id_produk = generate_random_id()
        
        if nama_produk and harga:
            try:
                db = connect_db()
                cursor = db.cursor()
                
                # Validasi apakah nama produk sudah ada di database
                cursor.execute("SELECT COUNT(*) FROM produk WHERE nama_produk = %s", (nama_produk,))
                result = cursor.fetchone()
                
                if result[0] > 0:
                    messagebox.showwarning("Duplicate Error", "Barang sudah ada.")
                else:
                    # Jika nama produk belum ada, tambahkan ke database
                    query = "INSERT INTO produk (id_produk, nama_produk, harga) VALUES (%s, %s, %s)"
                    cursor.execute(query, (id_produk, nama_produk, harga))
                    db.commit()
                    messagebox.showinfo("Success", f"Produk '{nama_produk}' berhasil ditambahkan.")
                    fetch_data()
                    
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                cursor.close()
                db.close()
        else:
            messagebox.showwarning("Input Error", "Semua kolom harus diisi.")


    def hapus_produk():
        selected_item = tree.selection()
        if selected_item:
            id_produk = tree.item(selected_item, "values")[0]
            try:
                db = connect_db()
                cursor = db.cursor()
                cursor.execute("DELETE FROM produk WHERE id_produk = %s", (id_produk,))
                db.commit()
                messagebox.showinfo("Success", "Produk berhasil dihapus.")
                fetch_data()
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                cursor.close()
                db.close()
        else:
            messagebox.showwarning("Selection Error", "Pilih produk yang akan dihapus.")

    def update_produk():
        selected_item = tree.selection()
        if selected_item:
            id_produk = tree.item(selected_item, "values")[0]
            nama_produk = entry_nama.get()
            harga = entry_harga.get()

            if nama_produk and harga:
                try:
                    db = connect_db()
                    cursor = db.cursor()
                    query = "UPDATE produk SET nama_produk = %s, harga = %s WHERE id_produk = %s"
                    cursor.execute(query, (nama_produk, harga, id_produk))
                    db.commit()
                    messagebox.showinfo("Success", "Produk berhasil diupdate.")
                    fetch_data()
                except Exception as e:
                    messagebox.showerror("Error", str(e))
                finally:
                    cursor.close()
                    db.close()
            else:
                messagebox.showwarning("Input Error", "Semua kolom harus diisi.")
        else:
            messagebox.showwarning("Selection Error", "Pilih produk yang akan diupdate.")

    # Function for handling click on table row
    def on_item_click(event):
        selected_item = tree.selection()
        if selected_item:
            # Ambil data produk dari baris yang dipilih
            id_produk, nama_produk, harga = tree.item(selected_item, "values")
            entry_nama.delete(0, tk.END)
            entry_nama.insert(0, nama_produk)  # Isi nama produk ke input
            entry_harga.delete(0, tk.END)
            entry_harga.insert(0, harga)  # Isi harga ke input

    # Sembunyikan menu utama
    parent.withdraw()

    # GUI Setup for Admin Menu
    root = tk.Toplevel()
    root.title("Admin Menu")
    root.geometry("800x400")
    
    def on_close():
        root.destroy()
        parent.deiconify()

    root.protocol("WM_DELETE_WINDOW", on_close)

    # Input Section
    frame_input = tk.Frame(root)
    frame_input.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

    tk.Label(frame_input, text="Nama Produk:").grid(row=0, column=0, padx=5, pady=5)
    entry_nama = tk.Entry(frame_input)
    entry_nama.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_input, text="Harga:").grid(row=1, column=0, padx=5, pady=5)
    entry_harga = tk.Entry(frame_input)
    entry_harga.grid(row=1, column=1, padx=5, pady=5)

    # Buttons
    btn_tambah = tk.Button(frame_input, text="Tambah", bg="green", fg="white", command=tambah_produk)
    btn_tambah.grid(row=2, column=0, padx=5, pady=5)

    btn_update = tk.Button(frame_input, text="Update", bg="blue", fg="white", command=update_produk)

    btn_update.grid(row=2, column=1, padx=5, pady=5)

    btn_hapus = tk.Button(frame_input, text="Hapus", bg="red", fg="white", command=hapus_produk)
    btn_hapus.grid(row=2, column=2, padx=5, pady=5)

    btn_logout = tk.Button(frame_input, text="Logout", command=on_close, bg="orange", fg="black")
    btn_logout.grid(row=2, column=3, padx=5, pady=5)


    # Data Table
    tree = ttk.Treeview(root, columns=("ID", "Nama Produk", "Harga"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nama Produk", text="Nama Produk")
    tree.heading("Harga", text="Harga")
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    # Bind item click to on_item_click function
    tree.bind("<ButtonRelease-1>", on_item_click)

    fetch_data()
    root.mainloop()

def user_menu(parent):
    def fetch_data():
        # Menghapus semua item di tabel barang
        for i in tree_barang.get_children():
            tree_barang.delete(i)

        # Menghapus semua item di tabel transaksi
        for i in tree_transaksi.get_children():
            tree_transaksi.delete(i)

        db = connect_db()
        cursor = db.cursor()

        try:
            # Mengambil data nama produk untuk dropdown
            cursor.execute("SELECT nama_produk FROM produk")
            rows = cursor.fetchall()
            dropdown_menu['values'] = [row[0] for row in rows]

            # Mengambil data produk untuk ditampilkan di tabel barang
            cursor.execute("SELECT * FROM produk")
            rows = cursor.fetchall()
            for row in rows:
                tree_barang.insert("", "end", values=row)

            # Mengambil data transaksi untuk ditampilkan di tabel transaksi
            cursor.execute("SELECT * FROM transaksi")
            rows = cursor.fetchall()
            for row in rows:
                tree_transaksi.insert("", "end", values=row)

        finally:
            cursor.close()
            db.close()

    def on_item_click(event):
        selected_item = tree_barang.selection()
        if selected_item:
            # Ambil nama produk dari baris yang dipilih
            nama_produk = tree_barang.item(selected_item, "values")[1]
            dropdown_menu.set(nama_produk)

    def beli_produk():
        nama_produk = dropdown_menu.get()
        jumlah = entry_jumlah.get()

        if nama_produk and jumlah:
            try:
                db = connect_db()
                cursor = db.cursor()

                cursor.execute("SELECT id_produk, harga FROM produk WHERE nama_produk = %s", (nama_produk,))
                produk = cursor.fetchone()

                if produk:
                    id_produk, harga = produk
                    total_harga = int(jumlah) * harga
                    tgl_transaksi = date.today()
                    id_transaksi = generate_random_id()

                    query = """
                    INSERT INTO transaksi (id_transaksi, id_produk, jumlah_produk, total_harga, tanggal_transaksi)
                    VALUES (%s, %s, %s, %s, %s)
                    """
                    values = (id_transaksi, id_produk, jumlah, total_harga, tgl_transaksi)
                    cursor.execute(query, values)
                    db.commit()

                    messagebox.showinfo("Success", f"Berhasil membeli {jumlah} {nama_produk} dengan total {total_harga}.")
                    fetch_data()
                else:
                    messagebox.showerror("Error", "Produk tidak ditemukan.")

            except Exception as e:
                messagebox.showerror("Error", str(e))

            finally:
                cursor.close()
                db.close()
        else:
            messagebox.showwarning("Input Error", "Semua kolom harus diisi.")

    def hapus_transaksi():
        selected_item = tree_transaksi.selection()
        if selected_item:
            transaksi_id = tree_transaksi.item(selected_item, "values")[0]
            if messagebox.askyesno("Konfirmasi", f"Yakin ingin menghapus transaksi ID {transaksi_id}?"):
                try:
                    db = connect_db()
                    cursor = db.cursor()

                    # Query untuk menghapus transaksi
                    cursor.execute("DELETE FROM transaksi WHERE id_transaksi = %s", (transaksi_id,))
                    db.commit()

                    messagebox.showinfo("Success", f"Transaksi ID {transaksi_id} berhasil dihapus.")
                    fetch_data()

                except Exception as e:
                    messagebox.showerror("Error", str(e))

                finally:
                    cursor.close()
                    db.close()
        else:
            messagebox.showwarning("Pilih Transaksi", "Silakan pilih transaksi yang ingin dihapus.")

    # Sembunyikan menu utama
    parent.withdraw()

    # GUI Setup
    root = tk.Tk()
    root.title("User Menu")
    root.geometry("800x600")

    def on_close():
        root.destroy()
        parent.deiconify()

    root.protocol("WM_DELETE_WINDOW", on_close)

    # Input Section
    frame_input = tk.Frame(root)
    frame_input.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

    tk.Label(frame_input, text="Nama Produk:").grid(row=0, column=0, padx=5, pady=5)
    dropdown_menu = ttk.Combobox(frame_input)
    dropdown_menu.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_input, text="Jumlah:").grid(row=1, column=0, padx=5, pady=5)
    entry_jumlah = tk.Entry(frame_input)
    entry_jumlah.grid(row=1, column=1, padx=5, pady=5)

    # Tombol "Beli" dan "Hapus Transaksi"
    btn_beli = tk.Button(frame_input, text="Beli", bg="green", fg="white", command=beli_produk)
    btn_beli.grid(row=2, column=0, padx=5, pady=5)

    btn_hapus = tk.Button(frame_input, text="Hapus Transaksi", bg="red", fg="white", command=hapus_transaksi)
    btn_hapus.grid(row=2, column=1, padx=5, pady=5)
    
    btn_logout = tk.Button(frame_input, text="Logout", command=on_close, bg="orange", fg="black")
    btn_logout.grid(row=2, column=3, padx=5, pady=5)

    # Tabel Barang
    tree_barang = ttk.Treeview(root, columns=("ID", "Nama Produk", "Harga"), show="headings")
    tree_barang.heading("ID", text="ID")
    tree_barang.heading("Nama Produk", text="Nama Produk")
    tree_barang.heading("Harga", text="Harga")
    tree_barang.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    # Tabel Transaksi
    tree_transaksi = ttk.Treeview(root, columns=("ID Transaksi", "ID Produk", "Jumlah Produk", "Total Harga", "Tanggal Transaksi"), show="headings")
    tree_transaksi.heading("ID Transaksi", text="ID Transaksi")
    tree_transaksi.heading("ID Produk", text="ID Produk")
    tree_transaksi.heading("Jumlah Produk", text="Jumlah Produk")
    tree_transaksi.heading("Total Harga", text="Total Harga")
    tree_transaksi.heading("Tanggal Transaksi", text="Tanggal Transaksi")
    tree_transaksi.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    tree_barang.bind("<ButtonRelease-1>", on_item_click)
    fetch_data()
    root.mainloop()

def main_menu():
    root = tk.Tk()
    root.title("Main Menu")
    root.geometry("400x300")

    tk.Label(root, text="Main Menu", font=("Arial", 16)).pack(pady=20)

    tk.Button(root, text="Admin Menu", command=lambda: admin_menu(root), width=20).pack(pady=10)
    tk.Button(root, text="User Menu", command=lambda: user_menu(root), width=20).pack(pady=10)
    tk.Button(root, text="Exit", command=root.quit, width=20).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main_menu()
