# Author: Kaan OZCAN
# Contact: ozcankaan0l@hotmail.com

import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from datetime import datetime
from PIL import Image, ImageTk

class KamyonKayitUygulamasi:
    def __init__(self, root, username, company_code, is_admin=False):
        self.root = root
        self.username = username
        self.company_code = company_code
        self.is_admin = is_admin
        self.root.title("Kamyon Kayıt Programı")

        self.kamyonlar = self.kamyonlari_yukle()
        self.bakim_kayitlari = self.bakim_kayitlarini_yukle()
        self.yakit_kayitlari = self.yakit_kayitlarini_yukle()
        self.suruculer = self.suruculer_yukle()
        self.id_counter = len(self.kamyonlar) + 1

        self.set_icon()
        self.create_widgets()
        self.adjust_window_size()

    def set_icon(self):
        try:
            self.icon_image = ImageTk.PhotoImage(file="icon.png")
            self.root.iconphoto(True, self.icon_image)
        except Exception as e:
            print("Simge yüklenemedi:", e)

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=1, fill='both')

        self.create_welcome_page()

        if not self.is_admin:
            self.create_truck_registration_page()
            self.create_maintenance_page()
            self.create_fuel_tracking_page()
            self.create_driver_management_page()
        else:
            self.create_admin_panel()
            self.create_announcement_edit_page()

    def create_welcome_page(self):
        self.welcome_frame = tk.Frame(self.notebook)
        self.notebook.add(self.welcome_frame, text="Hoşgeldin")

        welcome_label = tk.Label(self.welcome_frame, text=f"Hoşgeldin {self.username}", font=("Helvetica", 18))
        welcome_label.grid(row=0, column=0, columnspan=2, pady=20, padx=10)

        update_label = tk.Label(self.welcome_frame, text="Güncellemeler:", font=("Helvetica", 14))
        update_label.grid(row=1, column=0, sticky="nw", pady=10, padx=10)

        self.update_text = tk.Text(self.welcome_frame, height=10, width=70)
        self.update_text.grid(row=1, column=1, sticky="nsew", pady=10, padx=10)
        self.update_text.insert(tk.END, "1. Yeni özellikler eklendi.\n2. Arayüz iyileştirildi.\n3. Performans arttırıldı.")
        self.update_text.config(state=tk.DISABLED)

        guide_label = tk.Label(self.welcome_frame, text="Uygulama Rehberi:", font=("Helvetica", 14))
        guide_label.grid(row=2, column=0, sticky="nw", pady=10, padx=10)

        self.guide_text = tk.Text(self.welcome_frame, height=10, width=70)
        self.guide_text.grid(row=2, column=1, sticky="nsew", pady=10, padx=10)
        self.guide_text.insert(tk.END, "Bu uygulama ile kamyon kayıt işlemlerinizi gerçekleştirebilirsiniz.\n\n1. Kamyon Ekle: Araç bilgilerini girerek yeni kamyon ekleyebilirsiniz.\n2. Kamyonları Listele: Kayıtlı kamyonları görüntüleyebilirsiniz.\n3. Araç Silme: Kayıtlı kamyonları silebilirsiniz.\n4. Durum Güncelleme: Kamyonların durumunu güncelleyebilirsiniz.")
        self.guide_text.config(state=tk.DISABLED)

        self.welcome_frame.grid_columnconfigure(0, weight=1)
        self.welcome_frame.grid_columnconfigure(1, weight=4)

        self.logout_button = tk.Button(self.root, text="Çıkış Yap", command=self.logout)
        self.logout_button.pack(anchor="ne", padx=10, pady=10)

    def create_truck_registration_page(self):
        self.kayit_frame = tk.Frame(self.notebook)
        self.notebook.add(self.kayit_frame, text="Kamyon Kayıt")

        self.main_frame = tk.Frame(self.kayit_frame)
        self.main_frame.pack(pady=20, padx=30, expand=True, fill='both')

        tk.Label(self.main_frame, text="Kamyon Kayıt Uygulaması", font=("Helvetica", 18)).grid(row=0, columnspan=5, pady=10)
        tk.Label(self.main_frame, text="Yeni Kamyon Ekle", font=("Helvetica", 12)).grid(row=1, columnspan=5, pady=10)
        tk.Label(self.main_frame, text="Araç Model:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.model_entry = tk.Entry(self.main_frame)
        self.model_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
        tk.Label(self.main_frame, text="Araç Plakası:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.plaka_entry = tk.Entry(self.main_frame)
        self.plaka_entry.grid(row=3, column=1, sticky="ew", padx=10, pady=5)
        tk.Label(self.main_frame, text="Araç Kapasitesi (ton):").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.kapasite_entry = tk.Entry(self.main_frame)
        self.kapasite_entry.grid(row=4, column=1, sticky="ew", padx=10, pady=5)
        tk.Button(self.main_frame, text="Kaydet", command=self.yeni_kamyon_gir).grid(row=5, columnspan=5, pady=10)

        tk.Label(self.main_frame, text="Kayıtlı Kamyonlar", font=("Helvetica", 12)).grid(row=6, columnspan=5, pady=10)

        self.tree = ttk.Treeview(self.main_frame, columns=("ID", "Model", "Plaka", "Kapasite", "Durum"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Model", text="Araç Modeli")
        self.tree.heading("Plaka", text="Plaka")
        self.tree.heading("Kapasite", text="Kapasite")
        self.tree.heading("Durum", text="Durum")

        for col in self.tree["columns"]:
            self.tree.column(col, anchor="w")

        self.tree.grid(row=7, column=0, columnspan=5, sticky="nsew", padx=10, pady=10)

        self.scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.scrollbar.grid(row=7, column=5, sticky="ns")
        self.tree.configure(yscroll=self.scrollbar.set)
        tk.Button(self.main_frame, text="Kamyonları Listele", command=self.kamyonlari_listele).grid(row=8, columnspan=5, pady=10)
        self.tree.bind("<Double-Button-1>", self.show_kamyon_detay)
        tk.Button(self.main_frame, text="Seçili Kamyonu Sil", command=self.arac_sil).grid(row=10, columnspan=5, pady=10)

        self.main_frame.grid_rowconfigure(7, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(2, weight=1)
        self.main_frame.grid_columnconfigure(3, weight=1)
        self.main_frame.grid_columnconfigure(4, weight=1)

    def create_maintenance_page(self):
        self.bakim_frame = tk.Frame(self.notebook)
        self.notebook.add(self.bakim_frame, text="Bakım Kayıtları")
        self.bakim_main_frame = tk.Frame(self.bakim_frame)
        self.bakim_main_frame.pack(pady=20, padx=30, expand=True, fill='both')
        tk.Label(self.bakim_main_frame, text="Bakım Kayıtları", font=("Helvetica", 18)).grid(row=0, columnspan=5, pady=10)
        tk.Label(self.bakim_main_frame, text="Yeni Bakım Kaydı Ekle", font=("Helvetica", 12)).grid(row=1, columnspan=5, pady=10)
        tk.Label(self.bakim_main_frame, text="Araç ID:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.bakim_arac_id_entry = tk.Entry(self.bakim_main_frame)
        self.bakim_arac_id_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
        tk.Label(self.bakim_main_frame, text="Bakım Tarihi (YYYY-MM-DD):").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.bakim_tarih_entry = tk.Entry(self.bakim_main_frame)
        self.bakim_tarih_entry.grid(row=3, column=1, sticky="ew", padx=10, pady=5)
        tk.Label(self.bakim_main_frame, text="Bakım Türü:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.bakim_tur_entry = tk.Entry(self.bakim_main_frame)
        self.bakim_tur_entry.grid(row=4, column=1, sticky="ew", padx=10, pady=5)
        tk.Button(self.bakim_main_frame, text="Kaydet", command=self.yeni_bakim_kayit_gir).grid(row=5, columnspan=5, pady=10)
        tk.Label(self.bakim_main_frame, text="Bakım Kayıt Listesi", font=("Helvetica", 12)).grid(row=6, columnspan=5, pady=10)
        self.bakim_tree = ttk.Treeview(self.bakim_main_frame, columns=("Arac ID", "Tarih", "Tür"), show='headings')
        self.bakim_tree.heading("Arac ID", text="Araç ID")
        self.bakim_tree.heading("Tarih", text="Bakım Tarihi")
        self.bakim_tree.heading("Tür", text="Bakım Türü")
        for col in self.bakim_tree["columns"]:
            self.bakim_tree.column(col, anchor="w")
        self.bakim_tree.grid(row=7, column=0, columnspan=5, sticky="nsew", padx=10, pady=10)
        self.bakim_scrollbar = ttk.Scrollbar(self.bakim_main_frame, orient=tk.VERTICAL, command=self.bakim_tree.yview)
        self.bakim_scrollbar.grid(row=7, column=5, sticky="ns")
        self.bakim_tree.configure(yscroll=self.bakim_scrollbar.set)
        tk.Button(self.bakim_main_frame, text="Bakım Kayıtlarını Listele", command=self.bakim_kayitlarini_listele).grid(row=8, columnspan=5, pady=10)
        self.bakim_main_frame.grid_rowconfigure(7, weight=1)
        self.bakim_main_frame.grid_columnconfigure(1, weight=1)
        self.bakim_main_frame.grid_columnconfigure(2, weight=1)
        self.bakim_main_frame.grid_columnconfigure(3, weight=1)
        self.bakim_main_frame.grid_columnconfigure(4, weight=1)

    def create_fuel_tracking_page(self):
        self.yakit_frame = tk.Frame(self.notebook)
        self.notebook.add(self.yakit_frame, text="Yakıt Takibi")
        self.yakit_main_frame = tk.Frame(self.yakit_frame)
        self.yakit_main_frame.pack(pady=20, padx=30, expand=True, fill='both')
        tk.Label(self.yakit_main_frame, text="Yakıt Takibi", font=("Helvetica", 18)).grid(row=0, columnspan=5, pady=10)
        tk.Label(self.yakit_main_frame, text="Yeni Yakıt Kaydı Ekle", font=("Helvetica", 12)).grid(row=1, columnspan=5, pady=10)
        tk.Label(self.yakit_main_frame, text="Araç ID:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.yakit_arac_id_entry = tk.Entry(self.yakit_main_frame)
        self.yakit_arac_id_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
        tk.Label(self.yakit_main_frame, text="Yakıt Tarihi (YYYY-MM-DD):").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.yakit_tarih_entry = tk.Entry(self.yakit_main_frame)
        self.yakit_tarih_entry.grid(row=3, column=1, sticky="ew", padx=10, pady=5)
        tk.Label(self.yakit_main_frame, text="Yakıt Miktarı (litre):").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.yakit_miktar_entry = tk.Entry(self.yakit_main_frame)
        self.yakit_miktar_entry.grid(row=4, column=1, sticky="ew", padx=10, pady=5)
        tk.Label(self.yakit_main_frame, text="Yakıt Maliyeti (TL):").grid(row=5, column=0, sticky="w", padx=10, pady=5)
        self.yakit_maliyet_entry = tk.Entry(self.yakit_main_frame)
        self.yakit_maliyet_entry.grid(row=5, column=1, sticky="ew", padx=10, pady=5)
        tk.Button(self.yakit_main_frame, text="Kaydet", command=self.yeni_yakit_kayit_gir).grid(row=6, columnspan=5, pady=10)
        tk.Label(self.yakit_main_frame, text="Yakıt Kayıt Listesi", font=("Helvetica", 12)).grid(row=7, columnspan=5, pady=10)
        self.yakit_tree = ttk.Treeview(self.yakit_main_frame, columns=("Arac ID", "Tarih", "Miktar", "Maliyet"), show='headings')
        self.yakit_tree.heading("Arac ID", text="Araç ID")
        self.yakit_tree.heading("Tarih", text="Yakıt Tarihi")
        self.yakit_tree.heading("Miktar", text="Yakıt Miktarı")
        self.yakit_tree.heading("Maliyet", text="Yakıt Maliyeti")
        for col in self.yakit_tree["columns"]:
            self.yakit_tree.column(col, anchor="w")
        self.yakit_tree.grid(row=8, column=0, columnspan=5, sticky="nsew", padx=10, pady=10)
        self.yakit_scrollbar = ttk.Scrollbar(self.yakit_main_frame, orient=tk.VERTICAL, command=self.yakit_tree.yview)
        self.yakit_scrollbar.grid(row=8, column=5, sticky="ns")
        self.yakit_tree.configure(yscroll=self.yakit_scrollbar.set)
        tk.Button(self.yakit_main_frame, text="Yakıt Kayıtlarını Listele", command=self.yakit_kayitlarini_listele).grid(row=9, columnspan=5, pady=10)
        self.yakit_main_frame.grid_rowconfigure(8, weight=1)
        self.yakit_main_frame.grid_columnconfigure(1, weight=1)
        self.yakit_main_frame.grid_columnconfigure(2, weight=1)
        self.yakit_main_frame.grid_columnconfigure(3, weight=1)
        self.yakit_main_frame.grid_columnconfigure(4, weight=1)

    def create_driver_management_page(self):
        self.surucu_frame = tk.Frame(self.notebook)
        self.notebook.add(self.surucu_frame, text="Sürücü Yönetimi")
        self.surucu_main_frame = tk.Frame(self.surucu_frame)
        self.surucu_main_frame.pack(pady=20, padx=30, expand=True, fill='both')
        tk.Label(self.surucu_main_frame, text="Sürücü Yönetimi", font=("Helvetica", 18)).grid(row=0, columnspan=5, pady=10)
        tk.Label(self.surucu_main_frame, text="Yeni Sürücü Ekle", font=("Helvetica", 12)).grid(row=1, columnspan=5, pady=10)
        tk.Label(self.surucu_main_frame, text="Sürücü Adı:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.surucu_adi_entry = tk.Entry(self.surucu_main_frame)
        self.surucu_adi_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
        tk.Label(self.surucu_main_frame, text="Sürücü Soyadı:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.surucu_soyadi_entry = tk.Entry(self.surucu_main_frame)
        self.surucu_soyadi_entry.grid(row=3, column=1, sticky="ew", padx=10, pady=5)
        tk.Label(self.surucu_main_frame, text="Telefon Numarası:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.surucu_tel_entry = tk.Entry(self.surucu_main_frame)
        self.surucu_tel_entry.grid(row=4, column=1, sticky="ew", padx=10, pady=5)
        tk.Button(self.surucu_main_frame, text="Kaydet", command=self.yeni_surucu_gir).grid(row=5, columnspan=5, pady=10)
        tk.Label(self.surucu_main_frame, text="Sürücü Listesi", font=("Helvetica", 12)).grid(row=6, columnspan=5, pady=10)
        self.surucu_tree = ttk.Treeview(self.surucu_main_frame, columns=("Adi", "Soyadi", "Telefon"), show='headings')
        self.surucu_tree.heading("Adi", text="Sürücü Adı")
        self.surucu_tree.heading("Soyadi", text="Sürücü Soyadı")
        self.surucu_tree.heading("Telefon", text="Telefon Numarası")
        for col in self.surucu_tree["columns"]:
            self.surucu_tree.column(col, anchor="w")
        self.surucu_tree.grid(row=7, column=0, columnspan=5, sticky="nsew", padx=10, pady=10)
        self.surucu_scrollbar = ttk.Scrollbar(self.surucu_main_frame, orient=tk.VERTICAL, command=self.surucu_tree.yview)
        self.surucu_scrollbar.grid(row=7, column=5, sticky="ns")
        self.surucu_tree.configure(yscroll=self.surucu_scrollbar.set)
        tk.Button(self.surucu_main_frame, text="Sürücüleri Listele", command=self.suruculeri_listele).grid(row=8, columnspan=5, pady=10)
        self.surucu_main_frame.grid_rowconfigure(7, weight=1)
        self.surucu_main_frame.grid_columnconfigure(1, weight=1)
        self.surucu_main_frame.grid_columnconfigure(2, weight=1)
        self.surucu_main_frame.grid_columnconfigure(3, weight=1)
        self.surucu_main_frame.grid_columnconfigure(4, weight=1)

    def create_admin_panel(self):
        self.admin_frame = tk.Frame(self.notebook)
        self.notebook.add(self.admin_frame, text="Yönetici Paneli")
        self.admin_notebook = ttk.Notebook(self.admin_frame)
        self.admin_notebook.pack(expand=1, fill='both')

        self.create_company_management_page()
        self.create_admin_management_page()
        self.create_user_management_page()

    def create_company_management_page(self):
        self.company_frame = tk.Frame(self.admin_notebook)
        self.admin_notebook.add(self.company_frame, text="Şirket Yönetimi")
        self.company_main_frame = tk.Frame(self.company_frame)
        self.company_main_frame.pack(pady=20, padx=30, expand=True, fill='both')
        tk.Label(self.company_main_frame, text="Yeni Şirket Oluştur", font=("Helvetica", 12)).grid(row=0, columnspan=2, pady=10)
        tk.Label(self.company_main_frame, text="Şirket Kodu:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.admin_sirket_kodu_entry = tk.Entry(self.company_main_frame)
        self.admin_sirket_kodu_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
        tk.Label(self.company_main_frame, text="Şirket Adı:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.admin_sirket_adi_entry = tk.Entry(self.company_main_frame)
        self.admin_sirket_adi_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
        tk.Button(self.company_main_frame, text="Şirket Ekle", command=self.yeni_sirket_ekle).grid(row=3, columnspan=2, pady=10)
        
        tk.Label(self.company_main_frame, text="Mevcut Şirketler:", font=("Helvetica", 12)).grid(row=4, columnspan=2, pady=10)
        self.sirket_listbox = tk.Listbox(self.company_main_frame, height=10)
        self.sirket_listbox.grid(row=5, columnspan=2, sticky="nsew", padx=10, pady=10)
        self.load_sirketler()

    def create_admin_management_page(self):
        self.admin_user_frame = tk.Frame(self.admin_notebook)
        self.admin_notebook.add(self.admin_user_frame, text="Yönetici Yönetimi")
        self.admin_user_main_frame = tk.Frame(self.admin_user_frame)
        self.admin_user_main_frame.pack(pady=20, padx=30, expand=True, fill='both')
        tk.Label(self.admin_user_main_frame, text="Yeni Şirket Yöneticisi Hesabı Ekle", font=("Helvetica", 12)).grid(row=0, columnspan=2, pady=10)
        tk.Label(self.admin_user_main_frame, text="Şirket Kodu:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.admin_yonetici_sirket_kodu_entry = tk.Entry(self.admin_user_main_frame)
        self.admin_yonetici_sirket_kodu_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
        tk.Label(self.admin_user_main_frame, text="E-posta:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.admin_yonetici_email_entry = tk.Entry(self.admin_user_main_frame)
        self.admin_yonetici_email_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
        tk.Label(self.admin_user_main_frame, text="Şifre:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.admin_yonetici_sifre_entry = tk.Entry(self.admin_user_main_frame, show='*')
        self.admin_yonetici_sifre_entry.grid(row=3, column=1, sticky="ew", padx=10, pady=5)
        tk.Button(self.admin_user_main_frame, text="Yönetici Hesabı Ekle", command=self.yeni_yonetici_hesabi).grid(row=4, columnspan=2, pady=10)

        tk.Label(self.admin_user_main_frame, text="Mevcut Yöneticiler:", font=("Helvetica", 12)).grid(row=5, columnspan=2, pady=10)
        self.yonetici_listbox = tk.Listbox(self.admin_user_main_frame, height=10)
        self.yonetici_listbox.grid(row=6, columnspan=2, sticky="nsew", padx=10, pady=10)
        self.load_yoneticiler()

    def create_user_management_page(self):
        self.user_management_frame = tk.Frame(self.admin_notebook)
        self.admin_notebook.add(self.user_management_frame, text="Kullanıcı Yönetimi")
        self.user_management_main_frame = tk.Frame(self.user_management_frame)
        self.user_management_main_frame.pack(pady=20, padx=30, expand=True, fill='both')
        tk.Label(self.user_management_main_frame, text="Yeni Kullanıcı Oluştur", font=("Helvetica", 12)).grid(row=0, columnspan=2, pady=10)
        tk.Label(self.user_management_main_frame, text="Şirket Kodu:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.user_sirket_kodu_entry = tk.Entry(self.user_management_main_frame)
        self.user_sirket_kodu_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
        tk.Label(self.user_management_main_frame, text="Kullanıcı Adı:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.user_email_entry = tk.Entry(self.user_management_main_frame)
        self.user_email_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
        tk.Label(self.user_management_main_frame, text="Şifre:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.user_sifre_entry = tk.Entry(self.user_management_main_frame, show='*')
        self.user_sifre_entry.grid(row=3, column=1, sticky="ew", padx=10, pady=5)
        tk.Button(self.user_management_main_frame, text="Kullanıcı Ekle", command=self.yeni_kullanici_ekle).grid(row=4, columnspan=2, pady=10)

    def create_announcement_edit_page(self):
        self.announcement_frame = tk.Frame(self.notebook)
        self.notebook.add(self.announcement_frame, text="Duyuru Düzenle")
        tk.Label(self.announcement_frame, text="Duyuru Düzenleme Sayfası", font=("Helvetica", 18)).grid(row=0, columnspan=2, pady=10, padx=10)
        tk.Label(self.announcement_frame, text="Duyurular:", font=("Helvetica", 14)).grid(row=1, column=0, sticky="nw", pady=10, padx=10)
        self.announcement_text = tk.Text(self.announcement_frame, height=15, width=70)
        self.announcement_text.grid(row=1, column=1, sticky="nsew", pady=10, padx=10)
        self.announcement_text.insert(tk.END, "Duyurular burada düzenlenecek.")
        tk.Button(self.announcement_frame, text="Kaydet", command=self.save_announcements).grid(row=2, columnspan=2, pady=10)

    def save_announcements(self):
        duyurular = self.announcement_text.get("1.0", tk.END).strip()
        with open("duyurular.txt", "w") as f:
            f.write(duyurular)
        messagebox.showinfo("Başarılı", "Duyurular kaydedildi.")

    def yeni_sirket_ekle(self):
        sirket_kodu = self.admin_sirket_kodu_entry.get()
        sirket_adi = self.admin_sirket_adi_entry.get()
        if sirket_kodu and sirket_adi:
            yeni_sirket = {
                "sirket_kodu": sirket_kodu,
                "sirket_adi": sirket_adi
            }
            filename = "sirketler.json"
            if os.path.exists(filename):
                with open(filename, "r") as f:
                    sirketler = json.load(f)
            else:
                sirketler = []
            sirketler.append(yeni_sirket)
            with open(filename, "w") as f:
                json.dump(sirketler, f, indent=4)
            messagebox.showinfo("Başarılı", "Yeni şirket oluşturuldu.")
            self.admin_sirket_kodu_entry.delete(0, tk.END)
            self.admin_sirket_adi_entry.delete(0, tk.END)
            self.load_sirketler()
        else:
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun!")

    def yeni_yonetici_hesabi(self):
        sirket_kodu = self.admin_yonetici_sirket_kodu_entry.get()
        email = self.admin_yonetici_email_entry.get()
        sifre = self.admin_yonetici_sifre_entry.get()
        if sirket_kodu and email and sifre:
            yeni_yonetici = {
                "sirket_kodu": sirket_kodu,
                "email": email,
                "sifre": sifre
            }
            filename = "yonetici_hesaplari.json"
            if os.path.exists(filename):
                with open(filename, "r") as f:
                    yonetici_hesaplari = json.load(f)
            else:
                yonetici_hesaplari = []
            yonetici_hesaplari.append(yeni_yonetici)
            with open(filename, "w") as f:
                json.dump(yonetici_hesaplari, f, indent=4)
            messagebox.showinfo("Başarılı", "Yeni yönetici hesabı oluşturuldu.")
            self.admin_yonetici_sirket_kodu_entry.delete(0, tk.END)
            self.admin_yonetici_email_entry.delete(0, tk.END)
            self.admin_yonetici_sifre_entry.delete(0, tk.END)
            self.load_yoneticiler()
        else:
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun!")

    def yeni_kullanici_ekle(self):
        sirket_kodu = self.user_sirket_kodu_entry.get()
        email = self.user_email_entry.get()
        sifre = self.user_sifre_entry.get()
        if sirket_kodu and email and sifre:
            yeni_kullanici = {
                "sirket_kodu": sirket_kodu,
                "email": email,
                "sifre": sifre
            }
            filename = "kullanicilar.json"
            if os.path.exists(filename):
                with open(filename, "r") as f:
                    kullanicilar = json.load(f)
            else:
                kullanicilar = []
            kullanicilar.append(yeni_kullanici)
            with open(filename, "w") as f:
                json.dump(kullanicilar, f, indent=4)
            messagebox.showinfo("Başarılı", "Yeni kullanıcı oluşturuldu.")
            self.user_sirket_kodu_entry.delete(0, tk.END)
            self.user_email_entry.delete(0, tk.END)
            self.user_sifre_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun!")

    def load_sirketler(self):
        self.sirket_listbox.delete(0, tk.END)
        filename = "sirketler.json"
        if os.path.exists(filename):
            with open(filename, "r") as f:
                sirketler = json.load(f)
                for sirket in sirketler:
                    self.sirket_listbox.insert(tk.END, f"{sirket['sirket_kodu']} - {sirket['sirket_adi']}")

    def load_yoneticiler(self):
        self.yonetici_listbox.delete(0, tk.END)
        filename = "yonetici_hesaplari.json"
        if os.path.exists(filename):
            with open(filename, "r") as f:
                yoneticiler = json.load(f)
                for yonetici in yoneticiler:
                    self.yonetici_listbox.insert(tk.END, f"{yonetici['sirket_kodu']} - {yonetici['email']}")

    def yeni_kamyon_gir(self):
        arac_model = self.model_entry.get().upper()
        arac_plaka = self.plaka_entry.get()
        arac_kapasite = self.kapasite_entry.get()
        if arac_model and arac_plaka and arac_kapasite:
            yeni_kamyon = {
                "ID": self.id_counter,
                "Model": arac_model,
                "Plaka": arac_plaka,
                "Kapasite": arac_kapasite,
                "Durum": "Bekliyor"
            }
            self.kamyonlar.append(yeni_kamyon)
            self.id_counter += 1
            self.kamyonlari_kaydet()
            messagebox.showinfo("Başarılı", "Yeni kamyon kaydedildi.")
            self.model_entry.delete(0, tk.END)
            self.plaka_entry.delete(0, tk.END)
            self.kapasite_entry.delete(0, tk.END)
            self.kamyonlari_listele()
        else:
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun!")

    def kamyonlari_listele(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        if self.kamyonlar:
            for kamyon in self.kamyonlar:
                self.tree.insert("", tk.END, values=(kamyon["ID"], kamyon["Model"], kamyon["Plaka"], kamyon["Kapasite"], kamyon["Durum"]))
                if kamyon["Durum"] == "Arızalı":
                    index = self.tree.get_children()[-1]
                    self.tree.item(index, tags=("arizali",))
            self.tree.tag_configure("arizali", background="red")
        else:
            messagebox.showinfo("Bilgi", "Veritabanında kayıtlı kamyon yok.")
        self.adjust_window_size()

    def yeni_bakim_kayit_gir(self):
        arac_id = self.bakim_arac_id_entry.get()
        bakim_tarih = self.bakim_tarih_entry.get()
        bakim_tur = self.bakim_tur_entry.get()
        if arac_id and bakim_tarih and bakim_tur:
            try:
                datetime.strptime(bakim_tarih, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Hata", "Geçersiz tarih formatı. Lütfen YYYY-MM-DD formatında bir tarih girin.")
                return
            yeni_bakim_kaydi = {
                "Arac ID": arac_id,
                "Tarih": bakim_tarih,
                "Tür": bakim_tur
            }
            self.bakim_kayitlari.append(yeni_bakim_kaydi)
            self.bakim_kayitlarini_kaydet()
            messagebox.showinfo("Başarılı", "Yeni bakım kaydı eklendi.")
            self.bakim_arac_id_entry.delete(0, tk.END)
            self.bakim_tarih_entry.delete(0, tk.END)
            self.bakim_tur_entry.delete(0, tk.END)
            self.bakim_kayitlarini_listele()
        else:
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun!")

    def bakim_kayitlarini_listele(self):
        for item in self.bakim_tree.get_children():
            self.bakim_tree.delete(item)
        if self.bakim_kayitlari:
            for kayit in self.bakim_kayitlari:
                self.bakim_tree.insert("", tk.END, values=(kayit["Arac ID"], kayit["Tarih"], kayit["Tür"]))
        else:
            messagebox.showinfo("Bilgi", "Veritabanında bakım kaydı yok.")
        self.adjust_window_size()

    def yeni_yakit_kayit_gir(self):
        arac_id = self.yakit_arac_id_entry.get()
        yakit_tarih = self.yakit_tarih_entry.get()
        yakit_miktar = self.yakit_miktar_entry.get()
        yakit_maliyet = self.yakit_maliyet_entry.get()
        if arac_id and yakit_tarih and yakit_miktar and yakit_maliyet:
            try:
                datetime.strptime(yakit_tarih, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Hata", "Geçersiz tarih formatı. Lütfen YYYY-MM-DD formatında bir tarih girin.")
                return
            yeni_yakit_kaydi = {
                "Arac ID": arac_id,
                "Tarih": yakit_tarih,
                "Miktar": yakit_miktar,
                "Maliyet": yakit_maliyet
            }
            self.yakit_kayitlari.append(yeni_yakit_kaydi)
            self.yakit_kayitlarini_kaydet()
            messagebox.showinfo("Başarılı", "Yeni yakıt kaydı eklendi.")
            self.yakit_arac_id_entry.delete(0, tk.END)
            self.yakit_tarih_entry.delete(0, tk.END)
            self.yakit_miktar_entry.delete(0, tk.END)
            self.yakit_maliyet_entry.delete(0, tk.END)
            self.yakit_kayitlarini_listele()
        else:
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun!")

    def yakit_kayitlarini_listele(self):
        for item in self.yakit_tree.get_children():
            self.yakit_tree.delete(item)
        if self.yakit_kayitlari:
            for kayit in self.yakit_kayitlari:
                self.yakit_tree.insert("", tk.END, values=(kayit["Arac ID"], kayit["Tarih"], kayit["Miktar"], kayit["Maliyet"]))
        else:
            messagebox.showinfo("Bilgi", "Veritabanında yakıt kaydı yok.")
        self.adjust_window_size()

    def yeni_surucu_gir(self):
        adi = self.surucu_adi_entry.get()
        soyadi = self.surucu_soyadi_entry.get()
        telefon = self.surucu_tel_entry.get()
        if adi and soyadi and telefon:
            yeni_surucu = {
                "Adi": adi,
                "Soyadi": soyadi,
                "Telefon": telefon
            }
            self.suruculer.append(yeni_surucu)
            self.suruculer_kaydet()
            messagebox.showinfo("Başarılı", "Yeni sürücü kaydedildi.")
            self.surucu_adi_entry.delete(0, tk.END)
            self.surucu_soyadi_entry.delete(0, tk.END)
            self.surucu_tel_entry.delete(0, tk.END)
            self.suruculeri_listele()
        else:
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun!")

    def suruculeri_listele(self):
        for item in self.surucu_tree.get_children():
            self.surucu_tree.delete(item)
        if self.suruculer:
            for surucu in self.suruculer:
                self.surucu_tree.insert("", tk.END, values=(surucu["Adi"], surucu["Soyadi"], surucu["Telefon"]))
        else:
            messagebox.showinfo("Bilgi", "Veritabanında sürücü kaydı yok.")
        self.adjust_window_size()

    def on_left_click(self, event):
        region = self.tree.identify_region(event.x, event.y)
        if region == "cell":
            column = self.tree.identify_column(event.x)
            if column == "#5":
                self.selected_item = self.tree.identify_row(event.y)
                self.show_durum_menu(event.x_root, event.y_root)

    def show_durum_menu(self, x, y):
        durum_menu = tk.Menu(self.root, tearoff=0)
        durum_menu.add_command(label="Bekliyor", command=lambda: self.durum_degistir("Bekliyor"))
        durum_menu.add_command(label="Görevde", command=lambda: self.durum_degistir("Görevde"))
        durum_menu.add_command(label="Arızalı", command=lambda: self.durum_degistir("Arızalı"))
        durum_menu.tk_popup(x, y)

    def durum_degistir(self, durum):
        if hasattr(self, 'selected_item'):
            item = self.tree.item(self.selected_item)
            item_values = list(item["values"])
            item_values[4] = durum
            self.tree.item(self.selected_item, values=item_values)
            for kamyon in self.kamyonlar:
                if kamyon["ID"] == item_values[0]:
                    kamyon["Durum"] = durum
                    break
            self.kamyonlari_kaydet()
            self.kamyonlari_listele()

    def show_kamyon_detay(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Uyarı", "Lütfen detaylarını görmek istediğiniz kamyonu seçin.")
            return
        kamyon_id = int(self.tree.item(selected_item[0], "values")[0])
        kamyon = next((k for k in self.kamyonlar if k["ID"] == kamyon_id), None)
        if kamyon is None:
            messagebox.showerror("Hata", "Kamyon bulunamadı.")
            return
        detay_pencere = tk.Toplevel(self.root)
        detay_pencere.title(f"Kamyon Detayları - ID: {kamyon_id}")
        detay_frame = tk.Frame(detay_pencere, padx=10, pady=10)
        detay_frame.pack(expand=True, fill='both')
        tk.Label(detay_frame, text="Kamyon Detayları", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)
        detaylar = [
            ("Araç Modeli", kamyon["Model"]),
            ("Plaka", kamyon["Plaka"]),
            ("Kapasite", kamyon["Kapasite"]),
            ("Durum", kamyon["Durum"])
        ]
        for idx, (label, value) in enumerate(detaylar, start=1):
            tk.Label(detay_frame, text=label + ":", font=("Helvetica", 12)).grid(row=idx, column=0, sticky="w", pady=5)
            tk.Label(detay_frame, text=value, font=("Helvetica", 12)).grid(row=idx, column=1, sticky="w", pady=5)
        tk.Button(detay_frame, text="Kapat", command=detay_pencere.destroy).grid(row=idx + 1, columnspan=2, pady=10)

    def arac_sil(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Uyarı", "Lütfen silmek istediğiniz kamyonu seçin.")
            return
        kamyon_id = int(self.tree.item(selected_item[0], "values")[0])
        sil_message = f"Araç ID: {kamyon_id} silinecek, emin misiniz?"
        if messagebox.askyesno("Onay", sil_message):
            self.tree.delete(selected_item[0])
            self.kamyonlar = [kamyon for kamyon in self.kamyonlar if kamyon["ID"] != kamyon_id]
            self.kamyonlari_kaydet()
            messagebox.showinfo("Başarılı", f"Araç ID: {kamyon_id} silindi.")
        else:
            messagebox.showinfo("İptal", "Silme işlemi iptal edildi.")
        self.adjust_window_size()

    def kamyonlari_yukle(self):
        filename = f"{self.company_code}_kamyonlar.json"
        if os.path.exists(filename):
            with open(filename, "r") as f:
                return json.load(f)
        return []

    def kamyonlari_kaydet(self):
        filename = f"{self.company_code}_kamyonlar.json"
        with open(filename, "w") as f:
            json.dump(self.kamyonlar, f, indent=4)

    def bakim_kayitlarini_yukle(self):
        filename = f"{self.company_code}_bakim_kayitlari.json"
        if os.path.exists(filename):
            with open(filename, "r") as f:
                return json.load(f)
        return []

    def bakim_kayitlarini_kaydet(self):
        filename = f"{self.company_code}_bakim_kayitlari.json"
        with open(filename, "w") as f:
            json.dump(self.bakim_kayitlari, f, indent=4)

    def yakit_kayitlarini_yukle(self):
        filename = f"{self.company_code}_yakit_kayitlari.json"
        if os.path.exists(filename):
            with open(filename, "r") as f:
                return json.load(f)
        return []

    def yakit_kayitlarini_kaydet(self):
        filename = f"{self.company_code}_yakit_kayitlari.json"
        with open(filename, "w") as f:
            json.dump(self.yakit_kayitlari, f, indent=4)

    def suruculer_yukle(self):
        filename = f"{self.company_code}_suruculer.json"
        if os.path.exists(filename):
            with open(filename, "r") as f:
                return json.load(f)
        return []

    def suruculer_kaydet(self):
        filename = f"{self.company_code}_suruculer.json"
        with open(filename, "w") as f:
            json.dump(self.suruculer, f, indent=4)

    def logout(self):
        self.root.destroy()
        root = tk.Tk()
        LoginPaneli(root)
        root.mainloop()

class LoginPaneli:
    def __init__(self, root):
        self.root = root
        self.root.title("Giriş Paneli")
        self.create_widgets()

    def create_widgets(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=20, padx=30, expand=True, fill='both')
        tk.Label(self.main_frame, text="Şirket Kodu:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.sirket_kodu_entry = tk.Entry(self.main_frame)
        self.sirket_kodu_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=5)
        tk.Label(self.main_frame, text="Kullanıcı Adı:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.kullanici_adi_entry = tk.Entry(self.main_frame)
        self.kullanici_adi_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
        tk.Label(self.main_frame, text="Şifre:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.sifre_entry = tk.Entry(self.main_frame, show='*')
        self.sifre_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
        self.remember_me = tk.BooleanVar()
        tk.Checkbutton(self.main_frame, text="Beni Hatırla", variable=self.remember_me).grid(row=3, columnspan=2, pady=10)
        tk.Button(self.main_frame, text="Giriş Yap", command=self.giris_yap).grid(row=4, columnspan=2, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=2)
        self.load_last_login()
        tk.Button(self.main_frame, text="Admin Girişi", command=self.admin_giris).grid(row=5, columnspan=2, pady=10)

    def load_last_login(self):
        if os.path.exists("last_login.json"):
            with open("last_login.json", "r") as f:
                data = json.load(f)
                self.sirket_kodu_entry.insert(0, data.get("sirket_kodu", ""))
                self.kullanici_adi_entry.insert(0, data.get("kullanici_adi", ""))
                self.sifre_entry.insert(0, data.get("sifre", ""))
                self.remember_me.set(data.get("remember_me", False))

    def save_last_login(self, sirket_kodu, kullanici_adi, sifre):
        data = {
            "sirket_kodu": sirket_kodu,
            "kullanici_adi": kullanici_adi,
            "sifre": sifre,
            "remember_me": self.remember_me.get()
        }
        with open("last_login.json", "w") as f:
            json.dump(data, f)

    def giris_yap(self):
        sirket_kodu = self.sirket_kodu_entry.get()
        kullanici_adi = self.kullanici_adi_entry.get()
        sifre = self.sifre_entry.get()
        if self.validate_login(sirket_kodu, kullanici_adi, sifre):
            if self.remember_me.get():
                self.save_last_login(sirket_kodu, kullanici_adi, sifre)
            self.root.destroy()
            ana_pencere = tk.Tk()
            is_admin = self.is_admin_user(sirket_kodu, kullanici_adi, sifre)
            KamyonKayitUygulamasi(ana_pencere, kullanici_adi, sirket_kodu, is_admin)
            ana_pencere.mainloop()
        else:
            messagebox.showerror("Hata", "Geçersiz şirket kodu, kullanıcı adı veya şifre!")

    def validate_login(self, sirket_kodu, kullanici_adi, sifre):
        return self.is_admin_user(sirket_kodu, kullanici_adi, sifre) or (sirket_kodu == "ADMIN" and kullanici_adi == "admin" and sifre == "admin123")

    def is_admin_user(self, sirket_kodu, email, sifre):
        filename = "yonetici_hesaplari.json"
        if os.path.exists(filename):
            with open(filename, "r") as f:
                yonetici_hesaplari = json.load(f)
                for hesap in yonetici_hesaplari:
                    if hesap["sirket_kodu"] == sirket_kodu and hesap["email"] == email and hesap["sifre"] == sifre:
                        return True
        return False

    def admin_giris(self):
        sirket_kodu = self.sirket_kodu_entry.get()
        kullanici_adi = self.kullanici_adi_entry.get()
        sifre = self.sifre_entry.get()
        if sirket_kodu == "ADMIN" and kullanici_adi == "admin" and sifre == "admin123":
            self.root.destroy()
            ana_pencere = tk.Tk()
            KamyonKayitUygulamasi(ana_pencere, "Admin", "ADMIN", True)
            ana_pencere.mainloop()
        else:
            messagebox.showerror("Hata", "Geçersiz yönetici bilgileri!")

if __name__ == "__main__":
    root = tk.Tk()
    LoginPaneli(root)
    root.mainloop()
