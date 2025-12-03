# pip install reportlab

import random
from datetime import date, timedelta
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# ---------- Helper functions ----------

def format_rupiah(amount: int) -> str:
    # Format: Rp 1.234.567
    return "Rp {:,}".format(amount).replace(",", ".")

def random_date(start_year=2024, end_year=2026):
    start = date(start_year, 1, 1)
    end = date(end_year, 12, 31)
    delta_days = (end - start).days
    offset = random.randint(0, delta_days)
    return start + timedelta(days=offset)

def format_tanggal_id(dt: date) -> str:
    bulan_id = [
        "Januari", "Februari", "Maret", "April", "Mei", "Juni",
        "Juli", "Agustus", "September", "Oktober", "November", "Desember"
    ]
    return f"{dt.day} {bulan_id[dt.month - 1]} {dt.year}"

# ---------- Data template ----------

nama_perusahaan = [
    "PT Maju Jaya Sejahtera",
    "PT Nusantara Mandiri",
    "PT Solusi Teknologi Indonesia",
    "PT Karya Abadi Sentosa",
    "PT Sumber Daya Prima",
    "PT Citra Niaga Internasional",
    "PT Mitra Usaha Bersama",
    "PT Harmoni Logistik",
    "PT Bintang Karya Global",
    "PT Sentra Data Nusantara",
]

jenis_layanan = [
    "Layanan Konsultasi Bisnis",
    "Layanan Teknologi Informasi",
    "Layanan Distribusi dan Logistik",
    "Layanan Pemeliharaan Sistem",
    "Layanan Pelatihan dan Pengembangan SDM",
    "Layanan Pengadaan Perangkat Keras",
    "Layanan Pengelolaan Proyek",
    "Layanan Dukungan Teknis",
]

def buat_nama_kontrak():
    return f"Perjanjian Kerja Sama {random.choice(jenis_layanan)}"

def buat_nomor_kontrak(i: int):
    return f"KTR-{date.today().year}-{i:03d}"

# ---------- Generator PDF ----------

def buat_kontrak_pdf(index: int):
    # Data kontrak
    nama_kontrak = buat_nama_kontrak()
    nomor_kontrak = buat_nomor_kontrak(index)
    nilai_kontrak = random.randint(50_000_000, 2_000_000_000)  # 50 juta – 2 M
    tgl_mulai = random_date()
    # Durasi 3–24 bulan
    durasi_hari = random.randint(90, 730)
    tgl_akhir = tgl_mulai + timedelta(days=durasi_hari)

    pihak_1 = random.choice(nama_perusahaan)
    pihak_2 = random.choice([p for p in nama_perusahaan if p != pihak_1])

    # Nama file
    filename = f"kontrak_{index:03d}.pdf"

    # Setup PDF
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Margin & posisi awal teks
    x_margin = 60
    y = height - 80

    # Judul
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, y, "PERJANJIAN KERJA SAMA")
    y -= 25
    c.setFont("Helvetica", 11)
    c.drawCentredString(width / 2, y, f"{nama_kontrak}")
    y -= 40

    # Info dasar kontrak
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x_margin, y, "Nama Kontrak    :")
    c.setFont("Helvetica", 11)
    c.drawString(x_margin + 120, y, nama_kontrak)
    y -= 18

    c.setFont("Helvetica-Bold", 11)
    c.drawString(x_margin, y, "Nomor Kontrak   :")
    c.setFont("Helvetica", 11)
    c.drawString(x_margin + 120, y, nomor_kontrak)
    y -= 18

    c.setFont("Helvetica-Bold", 11)
    c.drawString(x_margin, y, "Nilai Kontrak   :")
    c.setFont("Helvetica", 11)
    c.drawString(x_margin + 120, y, format_rupiah(nilai_kontrak))
    y -= 18

    c.setFont("Helvetica-Bold", 11)
    c.drawString(x_margin, y, "Tanggal Mulai   :")
    c.setFont("Helvetica", 11)
    c.drawString(x_margin + 120, y, format_tanggal_id(tgl_mulai))
    y -= 18

    c.setFont("Helvetica-Bold", 11)
    c.drawString(x_margin, y, "Tanggal Akhir   :")
    c.setFont("Helvetica", 11)
    c.drawString(x_margin + 120, y, format_tanggal_id(tgl_akhir))
    y -= 30

    # Paragraf pembuka (contoh kontrak B2B sederhana)
    c.setFont("Helvetica", 11)
    paragraf = [
        f"Pada hari ini, para pihak yang bertanda tangan di bawah ini sepakat untuk mengikatkan diri",
        f"dalam suatu perjanjian kerja sama bisnis dengan ketentuan sebagai berikut.",
        "",
        f"PIHAK PERTAMA : {pihak_1}",
        f"PIHAK KEDUA   : {pihak_2}",
        "",
        "Para pihak sepakat bahwa PIHAK PERTAMA menunjuk PIHAK KEDUA untuk melaksanakan",
        f"{nama_kontrak.lower()} sesuai ruang lingkup pekerjaan yang akan diatur lebih lanjut",
        "dalam lampiran perjanjian ini.",
        "",
        f"Nilai total pekerjaan sebagaimana disepakati para pihak adalah sebesar",
        f"{format_rupiah(nilai_kontrak)} (termasuk pajak apabila berlaku), dengan jangka waktu",
        f"pelaksanaan sejak {format_tanggal_id(tgl_mulai)} sampai dengan {format_tanggal_id(tgl_akhir)}.",
        "",
        "Ketentuan lebih rinci terkait hak dan kewajiban para pihak, mekanisme pembayaran,",
        "serta pengakhiran perjanjian akan diatur dalam pasal-pasal berikutnya dan/atau lampiran.",
        "",
        "Demikian perjanjian ini dibuat dan ditandatangani secara sah oleh para pihak."
    ]

    for line in paragraf:
        if y < 80:  # halaman baru jika mendekati bawah
            c.showPage()
            y = height - 80
            c.setFont("Helvetica", 11)
        c.drawString(x_margin, y, line)
        y -= 15

    # Ruang tanda tangan
    y -= 30
    c.drawString(x_margin, y, f"{pihak_1}")
    c.drawString(width / 2 + 20, y, f"{pihak_2}")
    y -= 60
    c.drawString(x_margin, y, "(________________________)")
    c.drawString(width / 2 + 20, y, "(________________________)")

    # Simpan PDF
    c.save()
    print(f"Berhasil membuat: {filename}")

def main():
    for i in range(1, 51):  # 1 s.d. 50
        buat_kontrak_pdf(i)

if __name__ == "__main__":
    main()
