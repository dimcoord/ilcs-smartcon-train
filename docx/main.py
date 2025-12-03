import os
import random
from datetime import datetime, timedelta

from docx import Document

# ---------- Konfigurasi dasar ----------
JUMLAH_DOKUMEN = 50
OUTPUT_FOLDER = "kontrak_output"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ---------- Data contoh untuk random ----------
jenis_jasa = [
    "Layanan Teknologi Informasi",
    "Pemeliharaan Sistem",
    "Pengembangan Perangkat Lunak",
    "Konsultasi Manajemen",
    "Distribusi Produk",
    "Layanan Logistik",
    "Pelatihan SDM",
    "Layanan Pemasaran Digital",
]

perusahaan_a_list = [
    "PT Nusantara Teknologi",
    "PT Solusi Cerdas Indonesia",
    "PT Mitra Digital Sejahtera",
    "PT Inovasi Mandiri",
]

perusahaan_b_list = [
    "PT Sukses Abadi",
    "PT Maju Bersama",
    "PT Karya Prima",
    "PT Berkah Niaga",
]

bulan_id = {
    1: "Januari",
    2: "Februari",
    3: "Maret",
    4: "April",
    5: "Mei",
    6: "Juni",
    7: "Juli",
    8: "Agustus",
    9: "September",
    10: "Oktober",
    11: "November",
    12: "Desember",
}

# ---------- Fungsi bantu ----------

def format_tanggal_id(dt: datetime) -> str:
    """Mengubah datetime menjadi string tanggal Indonesia, mis. 3 Desember 2025."""
    return f"{dt.day} {bulan_id[dt.month]} {dt.year}"

def format_rupiah(n: int) -> str:
    """Format angka ke format Rupiah sederhana, mis. 150000000 -> Rp 150.000.000,-"""
    s = f"{n:,}".replace(",", ".")
    return f"Rp {s},-"

def generate_random_dates():
    """Generate tanggal mulai dan tanggal akhir secara acak."""
    # tanggal mulai antara 2023–2025
    start_year = random.randint(2023, 2025)
    start_month = random.randint(1, 12)
    start_day = random.randint(1, 28)  # biar aman untuk semua bulan
    t_mulai = datetime(start_year, start_month, start_day)

    durasi_hari = random.randint(30, 365)
    t_akhir = t_mulai + timedelta(days=durasi_hari)

    return t_mulai, t_akhir

def generate_nomor_kontrak():
    """Generate nomor kontrak random bergaya PKS/123/01/2025."""
    nomor_urut = random.randint(100, 999)
    bulan = random.randint(1, 12)
    tahun = random.randint(2023, 2026)
    return f"PKS/{nomor_urut}/{bulan:02d}/{tahun}"

# ---------- Loop pembuatan dokumen ----------

for i in range(1, JUMLAH_DOKUMEN + 1):
    # Data acak
    jasa = random.choice(jenis_jasa)
    nama_kontrak = f"Kontrak {jasa}"
    nomor_kontrak = generate_nomor_kontrak()
    nilai_kontrak_int = random.randint(50_000_000, 1_000_000_000)
    nilai_kontrak = format_rupiah(nilai_kontrak_int)
    t_mulai, t_akhir = generate_random_dates()

    tanggal_mulai_str = format_tanggal_id(t_mulai)
    tanggal_akhir_str = format_tanggal_id(t_akhir)

    pihak_pertama = random.choice(perusahaan_a_list)
    pihak_kedua = random.choice(perusahaan_b_list)

    # Buat dokumen
    doc = Document()

    # Judul
    doc.add_heading(nama_kontrak.upper(), level=1)

    # Info singkat kontrak
    doc.add_paragraph(f"Nomor Kontrak : {nomor_kontrak}")
    doc.add_paragraph(f"Nilai Kontrak  : {nilai_kontrak}")
    doc.add_paragraph(f"Tanggal Mulai  : {tanggal_mulai_str}")
    doc.add_paragraph(f"Tanggal Akhir  : {tanggal_akhir_str}")
    doc.add_paragraph("")

    # Pembukaan
    p1 = doc.add_paragraph()
    p1.add_run("Perjanjian Kerja Sama (\"Kontrak\") ini dibuat dan ditandatangani pada hari ini ")
    p1.add_run(tanggal_mulai_str).bold = True
    p1.add_run(" oleh dan antara:")

    doc.add_paragraph(f"1. {pihak_pertama}, selanjutnya disebut sebagai \"PIHAK PERTAMA\";")
    doc.add_paragraph(f"2. {pihak_kedua}, selanjutnya disebut sebagai \"PIHAK KEDUA\".")
    doc.add_paragraph("")

    # Pasal 1
    doc.add_heading("PASAL 1\nRUANG LINGKUP PEKERJAAN", level=2)
    doc.add_paragraph(
        f"PIHAK PERTAMA menunjuk PIHAK KEDUA untuk melaksanakan "
        f"{jasa.lower()} sesuai dengan ketentuan yang diatur dalam Kontrak ini."
    )

    # Pasal 2
    doc.add_heading("PASAL 2\nNILAI KONTRAK DAN PEMBAYARAN", level=2)
    doc.add_paragraph(
        f"Nilai Kontrak yang disepakati oleh para pihak adalah sebesar {nilai_kontrak} "
        "termasuk pajak apabila berlaku, kecuali disepakati lain secara tertulis."
    )

    # Pasal 3
    doc.add_heading("PASAL 3\nJANGKA WAKTU", level=2)
    doc.add_paragraph(
        f"Kontrak ini berlaku sejak tanggal {tanggal_mulai_str} sampai dengan "
        f"{tanggal_akhir_str}, kecuali apabila diperpanjang atau diakhiri lebih dahulu "
        "berdasarkan kesepakatan tertulis para pihak."
    )

    # Pasal 4
    doc.add_heading("PASAL 4\nKETENTUAN PENUTUP", level=2)
    doc.add_paragraph(
        "Hal-hal yang belum diatur dalam Kontrak ini akan diatur kemudian dalam "
        "addendum atau perjanjian terpisah yang merupakan bagian tidak terpisahkan "
        "dari Kontrak ini."
    )

    doc.add_paragraph("")
    doc.add_paragraph("Demikian Kontrak ini dibuat dan disepakati oleh para pihak:")
    doc.add_paragraph("")
    doc.add_paragraph(f"PIHAK PERTAMA,\n{pihak_pertama}\n\n________________________")
    doc.add_paragraph("")
    doc.add_paragraph(f"PIHAK KEDUA,\n{pihak_kedua}\n\n________________________")

    # Nama file
    safe_name = nama_kontrak.replace(" ", "_")
    filename = os.path.join(OUTPUT_FOLDER, f"{i:02d}_{safe_name}.docx")

    doc.save(filename)

print(f"Selesai membuat {JUMLAH_DOKUMEN} dokumen di folder: {OUTPUT_FOLDER}")
