import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib_venn import venn3

# =========================
# KONFIGURASI HALAMAN
# =========================
st.set_page_config(
    page_title="Sistem Klasifikasi Data Pasien",
    page_icon="🏥",
    layout="wide"
)

# =========================
# JUDUL
# =========================
st.title("🏥 Sistem Klasifikasi Data Pasien Klinik")
st.write(
    "Aplikasi untuk mengklasifikasikan data pasien "
    "menggunakan konsep himpunan."
)

st.divider()

# =========================
# MEMBACA DATASET
# =========================
data = pd.read_csv("dataset.csv")

# =========================
# DATA PASIEN
# =========================
st.subheader("📋 Data Pasien")

st.dataframe(
    data,
    use_container_width=True,
    hide_index=True
)

st.divider()

# =========================
# PEMBENTUKAN HIMPUNAN
# =========================
st.subheader("🎯 Pembentukan Himpunan")

kolom1, kolom2, kolom3 = st.columns(3)

# HIMPUNAN A
with kolom1:
    st.markdown("### Himpunan A")

    pilihan_A = st.selectbox(
        "Jenis Kelamin",
        ["Laki-laki", "Perempuan"]
    )

# HIMPUNAN B
with kolom2:
    st.markdown("### Himpunan B")

    pilihan_B = st.selectbox(
        "Umur",
        ["Umur ≥ 30", "Umur < 30"]
    )

# HIMPUNAN C
with kolom3:
    st.markdown("### Himpunan C")

    pilihan_C = st.selectbox(
        "Poli",
        ["Poli Umum", "Poli Gigi", "Poli Anak"]
    )


# =========================
# MEMBENTUK HIMPUNAN A
# =========================
if pilihan_A == "Laki-laki":
    A = set(data[data["Jenis_Kelamin"] == "L"]["ID"])
else:
    A = set(data[data["Jenis_Kelamin"] == "P"]["ID"])


# =========================
# MEMBENTUK HIMPUNAN B
# =========================
if pilihan_B == "Umur ≥ 30":
    B = set(data[data["Umur"] >= 30]["ID"])
else:
    B = set(data[data["Umur"] < 30]["ID"])


# =========================
# MEMBENTUK HIMPUNAN C
# =========================
if pilihan_C == "Poli Umum":
    C = set(data[data["Poli"] == "Umum"]["ID"])

elif pilihan_C == "Poli Gigi":
    C = set(data[data["Poli"] == "Gigi"]["ID"])

else:
    C = set(data[data["Poli"] == "Anak"]["ID"])


# =========================
# SEMESTA
# =========================
U = set(data["ID"])


# =========================
# HASIL PEMBENTUKAN
# =========================
st.subheader("📊 Hasil Pembentukan Himpunan")

info1, info2, info3 = st.columns(3)

with info1:
    st.metric("Himpunan A", f"{len(A)} pasien")
    st.caption(f"Jenis Kelamin: {pilihan_A}")

with info2:
    st.metric("Himpunan B", f"{len(B)} pasien")
    st.caption(f"Umur: {pilihan_B}")

with info3:
    st.metric("Himpunan C", f"{len(C)} pasien")
    st.caption(f"Poli: {pilihan_C}")


# =========================
# DAFTAR ANGGOTA HIMPUNAN
# =========================
st.subheader("👥 Anggota Himpunan")

anggota1, anggota2, anggota3 = st.columns(3)

with anggota1:
    st.markdown("**A**")
    st.write(", ".join(sorted(A)))

with anggota2:
    st.markdown("**B**")
    st.write(", ".join(sorted(B)))

with anggota3:
    st.markdown("**C**")
    st.write(", ".join(sorted(C)))


st.divider()


# =========================
# DIAGRAM VENN
# =========================
st.subheader("⭕ Diagram Venn")

fig, ax = plt.subplots(figsize=(7, 5))

venn3(
    [A, B, C],
    set_labels=("A", "B", "C"),
    ax=ax
)

ax.set_title("Diagram Venn Himpunan Pasien")

st.pyplot(fig)

plt.close(fig)

st.caption(
    f"A = {pilihan_A} | "
    f"B = {pilihan_B} | "
    f"C = {pilihan_C}"
)

st.divider()


# =========================
# OPERASI HIMPUNAN
# =========================
st.subheader("🔢 Operasi Himpunan")

operasi = st.selectbox(
    "Pilih operasi:",
    [
        "A ∪ B",
        "A ∩ B",
        "A − B",
        "B − C",
        "A ∪ B ∪ C",
        "A ∩ B ∩ C",
        "Aᶜ",
        "Bᶜ",
        "Cᶜ"
    ]
)


# =========================
# PROSES OPERASI
# =========================
if operasi == "A ∪ B":
    hasil = A | B
    keterangan = "Gabungan pasien yang termasuk A atau B."

elif operasi == "A ∩ B":
    hasil = A & B
    keterangan = "Pasien yang termasuk A dan B."

elif operasi == "A − B":
    hasil = A - B
    keterangan = "Pasien yang termasuk A tetapi tidak termasuk B."

elif operasi == "B − C":
    hasil = B - C
    keterangan = "Pasien yang termasuk B tetapi tidak termasuk C."

elif operasi == "A ∪ B ∪ C":
    hasil = A | B | C
    keterangan = "Gabungan pasien yang termasuk A, B, atau C."

elif operasi == "A ∩ B ∩ C":
    hasil = A & B & C
    keterangan = "Pasien yang termasuk A, B, dan C."

elif operasi == "Aᶜ":
    hasil = U - A
    keterangan = "Pasien yang tidak termasuk A."

elif operasi == "Bᶜ":
    hasil = U - B
    keterangan = "Pasien yang tidak termasuk B."

elif operasi == "Cᶜ":
    hasil = U - C
    keterangan = "Pasien yang tidak termasuk C."


# =========================
# HASIL OPERASI
# =========================
st.subheader("📌 Hasil Operasi")

st.info(keterangan)

st.write(f"**Operasi:** {operasi}")
st.write(f"**Jumlah hasil:** {len(hasil)} pasien")

hasil_data = data[data["ID"].isin(hasil)]

if len(hasil_data) > 0:
    st.dataframe(
        hasil_data,
        use_container_width=True,
        hide_index=True
    )
else:
    st.warning("Tidak ada pasien yang memenuhi operasi tersebut.")


st.divider()


# =========================
# KETERANGAN
# =========================
st.subheader("ℹ️ Keterangan Himpunan")

st.write("**A** = Himpunan berdasarkan jenis kelamin")
st.write("**B** = Himpunan berdasarkan umur")
st.write("**C** = Himpunan berdasarkan poli")
st.write("**U** = Seluruh data pasien")