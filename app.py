import streamlit as st
import pandas as pd
from datetime import datetime
import os
import base64
import io
import plotly.express as px

# --- KONFIGURASI HALAMAN (SIDEBAR DI-COLLAPSE/SEMBUNYIKAN) ---
st.set_page_config(
    page_title="SIAP-GEMPITA BANG",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- FILE PENYIMPANAN PERMANEN (LOCAL CSV) ---
DATA_FILE = "data_peserta_gempita.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            df_loaded = pd.read_csv(DATA_FILE)
            return df_loaded.to_dict('records')
        except:
            return []
    return []

def save_data_to_csv(data_list):
    df_save = pd.DataFrame(data_list)
    df_save.to_csv(DATA_FILE, index=False)

# --- INISIALISASI SESSION STATE ---
if 'data_peserta' not in st.session_state:
    st.session_state.data_peserta = load_data()

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'form_counter' not in st.session_state:
    st.session_state.form_counter = 0

if 'success_msg' not in st.session_state:
    st.session_state.success_msg = ""

# --- FUNGSI KONVERSI LOGO KE BASE64 ---
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""

logo_b64 = get_base64_image("logo.png")

# --- BANNER UTAMA ---
banner_bg = "#1e293b"      
border_color = "#334155"   

logo_element = f"<img src='data:image/png;base64,{logo_b64}' style='width: 135px; height: auto; border-radius: 8px; display: block;'/>" if logo_b64 else "<div style='font-size: 60px;'>🏆</div>"

st.markdown(f"""
    <div style="
        background-color: {banner_bg};
        border: 1px solid {border_color};
        padding: 26px 32px;
        border-radius: 12px;
        display: grid;
        grid-template-columns: 135px 1fr;
        align-items: center;
        gap: 28px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    ">
        <div style="display: flex; justify-content: center; align-items: center;">
            {logo_element}
        </div>
        <div style="display: flex; flex-direction: column; justify-content: center;">
            <h1 style="color: #ffffff; margin: 0 0 6px 0; font-size: 34px; font-weight: 800; line-height: 1.1; letter-spacing: 0.5px;">SIAP-GEMPITA BANG</h1>
            <h3 style="color: #38bdf8; margin: 0 0 6px 0; font-size: 17px; font-weight: 700; line-height: 1.2;">Sistem Informasi Administrasi & Pemantauan GEMPITA Cabdin Bangkalan</h3>
            <p style="color: #e2e8f0; margin: 0; font-size: 14px; font-weight: 500; line-height: 1.2;">Ajang Lomba Inovasi GTK (Guru dan Tenaga Kependidikan) Jawa Timur 2026</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- NAVIGASI MENU DI HALAMAN UTAMA ---
menu = st.radio(
    "🧭 Pilih Menu Navigasi", 
    ["Form Pendataan Peserta", "Dashboard & Rekapitulasi Data"], 
    horizontal=True
)
st.markdown("---")

# --- DATA REFERENSI SEKOLAH ---
sma_negeri = [
    'SMA NEGERI 1 AROSBAYA BANGKALAN', 'SMA NEGERI 1 BANGKALAN', 'SMA NEGERI 1 BLEGA BANGKALAN', 
    'SMA NEGERI 1 KAMAL BANGKALAN', 'SMA NEGERI 1 KOKOP BANGKALAN', 'SMA NEGERI 1 KWANYAR BANGKALAN', 
    'SMA NEGERI 1 TANJUNGBUMI BANGKALAN', 'SMA NEGERI 2 BANGKALAN', 'SMA NEGERI 3 BANGKALAN', 'SMA NEGERI 4 BANGKALAN'
]

sma_swasta = [
    'SMA AD-DAMANHURI', 'SMA AL AZHAR', 'SMA AL FATH', 'SMA AL-ASY ARIYAH MUSA', 'SMA AL-MURSYIDIYAH', 
    'SMA AN-NUR NH', 'SMA AN-NURONIYAH', 'SMA ASH-SHAHIHIYAH', 'SMA DARUL HADITS', 'SMA DARUL QORORI', 
    'SMA ISLAM', 'SMA ISLAM AL - FALAH', 'SMA ISLAM IBNU AHMAD MASDUKI', 'SMA KHOLILURROHMAN', 'SMA MUTIARA DT', 
    'SMA NURUD DZOLAM', 'SMA NURUL HUDA', 'SMA NURUL USMANI', 'SMA RAUDLATUL ULUM', 'SMA SABILUSH SHOLIHIN', 
    'SMAS A YUDA NEGARA', 'SMAS AL ANWARI', 'SMAS AL BAKRIYAH', 'SMAS AL HIDAYAH', 'SMAS AL HIKAM', 
    'SMAS AL IHSANI', 'SMAS AL KHATIBIYAH', 'SMAS AL-FURQON', 'SMAS AL-HIDAYAH', 'SMAS AR-RAUDHAH', 
    'SMAS ASSHOMADIYAH', 'SMAS AT TAUFIQIYAH', 'SMAS ATTHOLHAWIYAH', 'SMAS DARUL HIKMAH', 'SMAS DARUL KHOLIL', 
    'SMAS DARUL MUNIR', 'SMAS DARUL MUSTOFA', 'SMAS DARUT TAUHID', 'SMAS DARUZ ZUBAD', 'SMAS IBNU SHOLEH', 
    'SMAS INFORMATIKA', 'SMAS ISLAM ANNAFIIYAH', 'SMAS ISLAM NURUL AMANAH', 'SMAS ISLAM YASI', 'SMAS ISLAM YKHS', 
    'SMAS MAARIF', 'SMAS MAMBAUL ULUM', 'SMAS MANCENGAN DARUSSALAM', 'SMAS MIFTAHUL ULUM', 'SMAS MUHAMMADIYAH', 
    'SMAS NAHDLATUL ATHFAL', 'SMAS NURUL JADID', 'SMAS NURUSSHALEH', 'SMAS PGRI 2 BANGKALAN', 'SMAS SAIDIYAH', 
    'SMAS SUNAN AMPEL', 'SMAS TUNAS HARAPAN'
]

smk_negeri = [
    'SMK NEGERI 1 AROSBAYA BANGKALAN', 'SMK NEGERI 1 BANGKALAN', 'SMK NEGERI 1 BLEGA BANGKALAN', 
    'SMK NEGERI 1 KAMAL BANGKALAN', 'SMK NEGERI 1 KWANYAR BANGKALAN', 'SMK NEGERI 1 LABANG BANGKALAN', 
    'SMK NEGERI 1 SEPULUH BANGKALAN', 'SMK NEGERI 1 TANJUNGBUMI BANGKALAN', 'SMK NEGERI 2 BANGKALAN', 'SMK NEGERI 3 BANGKALAN'
]

smk_swasta = [
    'SMK  AL-ASY`ARI', 'SMK AL - AZIZIYAH KWANYAR', 'SMK AL - KAHFI', 'SMK AL - KHOLILIYAH BANGKALAN', 
    'SMK AL BAHARY MODUNG', 'SMK AL HIKAM KEMAYORAN', 'SMK AL KHATIBIYAH MODUNG', 'SMK AL QOHHARIY', 
    'SMK AL-FADLALY KLAMPIS', 'SMK AL-FURQON', 'SMK AL-HIKMAH KOKOP', 'SMK AL-ROHMANY', 'SMK ASSAIDIYAH', 
    'SMK AT-THOHIRIN', 'SMK BEZAB', 'SMK DARUL FATWA KWANYAR', 'SMK DARUSSALAM', 'SMK DARUSSALAM GEGER', 
    'SMK IFADAH', 'SMK ISLAM AL ALY', 'SMK MANBAUS SALAM', 'SMK MEDIKA ASSARBINI', 'SMK MIFTAHUT THOLIBIN KWANYAR', 
    'SMK NURUL AMANAH', 'SMK NURUL HIKMAH', 'SMK PERMAHISA', 'SMK PGRI 1 BANGKALAN', 'SMK SIRRUL CHOLIL', 
    'SMK SUNAN AMPEL', 'SMK SURAMADU', 'SMK SYAIFUL JAMIL BLEGA', 'SMK TUNAS BANGSA', 'SMK ULUL ALBAB', 
    'SMKS AGUNG MULIA SOCAH', 'SMKS AL AKHYAR LABANG', 'SMKS AL ANWAR', 'SMKS AL BAISUNY', 'SMKS AL HAMIDIYAH', 
    'SMKS AL HIKAM', 'SMKS AL IBRAHIMY', 'SMKS AL MUHAJIRIN', 'SMKS AN NUR FUADI', 'SMKS ASSYARQOWIYAH', 
    'SMKS BRAJAGUNA BANGKALAN', 'SMKS DARUL HIKMAH', 'SMKS DARUL MUSTOFA', 'SMKS IBNU CHOLIL', 
    'SMKS INFORMATIKA AL QALAM', 'SMKS KESEHATAN YANNAS HUSADA', 'SMKS MATHOLIUL ANWAR', 'SMKS MIFTAHUL HUDA', 
    'SMKS NAHDLATUL ULAMA', 'SMKS NURUL HIDAYAH', 'SMKS NURUL HUDA', 'SMKS NURUL JANNAH', 'SMKS NURUL KAROMAH', 
    'SMKS NURUS SHOLEH', 'SMKS NURUSSHALEH', 'SMKS PELAYARAN UJUNG BARU', 'SMKS ROUDLOTUT THOLIBIN', 'SMKS ULUL ALBAB AL HASANY'
]

slb_negeri = [
    'SLB NEGERI KELEYAN BANGKALAN'
]

slb_swasta = [
    'SLB PGRI', 'SLB SAMUDRA LAVENDER', 'SLB SAMUDRA TERRA ATHENA'
]

kategori_lomba_options = [
    "Guru Impresif",
    "Kepala Sekolah Inovatif",
    "Pengawas Sekolah Inspiratif",
    "Tenaga Kependidikan Dedikatif",
    "Apresiasi Penulis Buku (APB)"
]

# --- MENU 1: FORM PENDATAAN PESERTA ---
if menu == "Form Pendataan Peserta":
    st.subheader("📝 Formulir Pendataan Peserta Lomba Inovasi")
    
    if st.session_state.success_msg:
        st.success(st.session_state.success_msg)
        st.balloons()
        st.session_state.success_msg = ""
        
    fc = st.session_state.form_counter  
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### **Informasi Umum**")
        institusi = st.selectbox(
            "Pilih Institusi/Sekolah", 
            ["-- Pilih Kategori Institusi --", "SMA Negeri", "SMA Swasta", "SMK Negeri", "SMK Swasta", "SLB Negeri", "SLB Swasta", "Pengawas Sekolah", "Lainnya"],
            key=f"select_institusi_{fc}"
        )
        
        if institusi == "-- Pilih Kategori Institusi --":
            nama_sekolah = st.selectbox("Pilih Nama Institusi/Sekolah", ["-- Pilih Institusi Terlebih Dahulu --"], key=f"sekolah_empty_{fc}", disabled=True)
        elif institusi == "SMA Negeri":
            nama_sekolah = st.selectbox("Pilih Nama Institusi/Sekolah", ["-- Pilih Nama Sekolah --"] + sma_negeri, key=f"sekolah_sma_n_{fc}")
        elif institusi == "SMA Swasta":
            nama_sekolah = st.selectbox("Pilih Nama Institusi/Sekolah", ["-- Pilih Nama Sekolah --"] + sma_swasta, key=f"sekolah_sma_s_{fc}")
        elif institusi == "SMK Negeri":
            nama_sekolah = st.selectbox("Pilih Nama Institusi/Sekolah", ["-- Pilih Nama Sekolah --"] + smk_negeri, key=f"sekolah_smk_n_{fc}")
        elif institusi == "SMK Swasta":
            nama_sekolah = st.selectbox("Pilih Nama Institusi/Sekolah", ["-- Pilih Nama Sekolah --"] + smk_swasta, key=f"sekolah_smk_s_{fc}")
        elif institusi == "SLB Negeri":
            nama_sekolah = st.selectbox("Pilih Nama Institusi/Sekolah", ["-- Pilih Nama Sekolah --"] + slb_negeri, key=f"sekolah_slb_n_{fc}")
        elif institusi == "SLB Swasta":
            nama_sekolah = st.selectbox("Pilih Nama Institusi/Sekolah", ["-- Pilih Nama Sekolah --"] + slb_swasta, key=f"sekolah_slb_s_{fc}")
        elif institusi == "Pengawas Sekolah":
            nama_sekolah = st.selectbox("Pilih Nama Institusi/Sekolah", ["-- Pilih Nama Sekolah --"] + ["Cabdin Bangkalan"], key=f"sekolah_pengawas_{fc}")
        else:
            nama_sekolah = st.text_input("Ketikkan Nama Institusi/Sekolah", placeholder="Ketikkan nama instansi...", key=f"sekolah_lain_input_{fc}")
            
        nama_peserta = st.text_input("Nama Lengkap Peserta (beserta gelar)", placeholder="Contoh: Yustinus Budi, M.Pd.", key=f"input_nama_peserta_{fc}")
        jabatan = st.selectbox("Jabatan", ["-- Pilih Jabatan --", "Pengawas Sekolah", "Kepala Sekolah", "Guru", "Tendik"], key=f"select_jabatan_{fc}")

    with col2:
        st.markdown("#### **Detail Lomba & Karya**")
        kategori_lomba = st.selectbox("Kategori Lomba", ["-- Pilih Kategori Lomba --"] + kategori_lomba_options, key=f"select_kategori_{fc}")
        judul_karya = st.text_input("Judul Karya", placeholder="Ketikkan judul karya inovasi...", key=f"input_judul_karya_{fc}")
        keterangan = st.selectbox("Keterangan", ["-- Pilih Keterangan --", "Sudah Daftar", "Sudah Upload"], key=f"select_keterangan_{fc}")

    st.markdown("---")
    submit_btn = st.button("💾 Simpan Data Peserta", use_container_width=True)
    
    if submit_btn:
        if institusi == "-- Pilih Kategori Institusi --":
            st.error("Gagal menyimpan! Silakan pilih Kategori Institusi terlebih dahulu.")
        elif not nama_sekolah or nama_sekolah in ["-- Pilih Nama Sekolah --", "-- Pilih Institusi Terlebih Dahulu --"]:
            st.error("Gagal menyimpan! Nama Institusi/Sekolah wajib dipilih/diisi.")
        elif not nama_peserta:
            st.error("Gagal menyimpan! Nama Lengkap Peserta wajib diisi.")
        elif jabatan == "-- Pilih Jabatan --":
            st.error("Gagal menyimpan! Jabatan wajib dipilih.")
        elif kategori_lomba == "-- Pilih Kategori Lomba --":
            st.error("Gagal menyimpan! Kategori Lomba wajib dipilih.")
        elif not judul_karya:
            st.error("Gagal menyimpan! Judul Karya wajib diisi.")
        elif keterangan == "-- Pilih Keterangan --":
            st.error("Gagal menyimpan! Keterangan wajib dipilih.")
        else:
            with st.spinner("Sedang memproses dan menyimpan data peserta, mohon tunggu..."):
                data_baru = {
                    "Waktu Input": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Institusi/Sekolah": institusi,
                    "Nama Institusi/Sekolah": nama_sekolah,
                    "Nama Peserta": nama_peserta,
                    "Jabatan": jabatan,
                    "Kategori Lomba": kategori_lomba,
                    "Judul Karya": judul_karya,
                    "Keterangan": keterangan
                }
                st.session_state.data_peserta.append(data_baru)
                save_data_to_csv(st.session_state.data_peserta)
            
            st.session_state.success_msg = f"✅ Data peserta atas nama **{nama_peserta}** berhasil disimpan secara permanen!"
            st.session_state.form_counter += 1
            st.rerun()

# --- MENU 2: DASHBOARD & REKAPITULASI DATA ---
elif menu == "Dashboard & Rekapitulasi Data":
    if not st.session_state.logged_in:
        st.subheader("🔐 Login Akses Administrator")
        st.info("Menu ini bersifat terbatas. Silakan masukkan kredensial admin untuk mengakses dashboard rekapitulasi.")
        
        with st.form("form_login_admin"):
            username_input = st.text_input("Username")
            password_input = st.text_input("Password", type="password")
            submit_login = st.form_submit_button("Masuk Dashboard", use_container_width=True)
            
            if submit_login:
                if username_input == "Yusbuset" and password_input == "Gempita2026":
                    st.session_state.logged_in = True
                    st.success("Login berhasil! Memuat dashboard...")
                    st.rerun()
                else:
                    st.error("Username atau Password salah!")
    else:
        col_title, col_logout = st.columns([0.8, 0.2])
        with col_title:
            st.subheader("📊 Dashboard Pemantauan & Rekapitulasi Keikutsertaan")
        with col_logout:
            if st.button("🚪 Logout Admin", use_container_width=True):
                st.session_state.logged_in = False
                st.rerun()
                
        if len(st.session_state.data_peserta) == 0:
            st.info("ℹ️ Belum ada data peserta yang dimasukkan.")
        else:
            df = pd.DataFrame(st.session_state.data_peserta)
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Pendaftar", len(df))
            col2.metric("Sudah Upload", len(df[df["Keterangan"] == "Sudah Upload"]))
            col3.metric("Sudah Daftar", len(df[df["Keterangan"] == "Sudah Daftar"]))
            col4.metric("Total Instansi", df["Nama Institusi/Sekolah"].nunique())
            
            st.markdown("---")
            
            st.markdown("### 📈 Grafik Statistik Keikutsertaan")
            col_chart1, col_chart2 = st.columns(2)
            
            with col_chart1:
                st.markdown("##### Peserta Berdasarkan Institusi")
                df_institusi = df["Institusi/Sekolah"].value_counts().reset_index()
                df_institusi.columns = ["Institusi/Sekolah", "Jumlah"]
                fig1 = px.bar(df_institusi, x="Institusi/Sekolah", y="Jumlah", color="Institusi/Sekolah", text="Jumlah")
                fig1.update_layout(showlegend=False, margin=dict(l=20, r=20, t=30, b=20), height=350)
                st.plotly_chart(fig1, use_container_width=True)
                
            with col_chart2:
                st.markdown("##### Peserta Berdasarkan Kategori Lomba")
                df_kategori = df["Kategori Lomba"].value_counts().reset_index()
                df_kategori.columns = ["Kategori Lomba", "Jumlah"]
                fig2 = px.bar(df_kategori, x="Kategori Lomba", y="Jumlah", color="Kategori Lomba", text="Jumlah")
                fig2.update_layout(showlegend=False, margin=dict(l=20, r=20, t=30, b=20), height=350)
                st.plotly_chart(fig2, use_container_width=True)
                
            st.markdown("---")
            st.markdown("### 📋 Daftar Seluruh Peserta Terdaftar")
            
            col_f1, col_f2 = st.columns(2)
            
            with col_f1:
                list_institusi = ["Semua Institusi"] + sorted(list(df["Institusi/Sekolah"].unique()))
                filter_institusi = st.selectbox("Filter Berdasarkan Kategori Institusi", list_institusi)
                
            with col_f2:
                if filter_institusi == "Semua Institusi":
                    list_nama = ["Semua Instansi/Sekolah"] + sorted(list(df["Nama Institusi/Sekolah"].unique()))
                else:
                    filtered_by_inst = df[df["Institusi/Sekolah"] == filter_institusi]
                    list_nama = ["Semua Instansi/Sekolah"] + sorted(list(filtered_by_inst["Nama Institusi/Sekolah"].unique()))
                
                filter_nama_sekolah = st.selectbox("Filter Berdasarkan Nama Spesifik Instansi/Sekolah", list_nama)
                
            df_filtered = df.copy()
            if filter_institusi != "Semua Institusi":
                df_filtered = df_filtered[df_filtered["Institusi/Sekolah"] == filter_institusi]
            if filter_nama_sekolah != "Semua Instansi/Sekolah":
                df_filtered = df_filtered[df_filtered["Nama Institusi/Sekolah"] == filter_nama_sekolah]
                
            df_display = df_filtered.copy()
            df_display.index = range(1, len(df_display) + 1)
            st.dataframe(df_display, use_container_width=True)
            
            # --- EXPORT EXCEL DENGAN AUTO-FIT KOLOM ---
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_filtered.to_excel(writer, index=False, sheet_name='Rekap Peserta Gempita')
                
                # Mengatur lebar kolom agar menyesuaikan isi teks secara otomatis
                worksheet = writer.sheets['Rekap Peserta Gempita']
                for col in worksheet.columns:
                    max_len = 0
                    col_letter = col[0].column_letter
                    for cell in col:
                        if cell.value is not None:
                            max_len = max(max_len, len(str(cell.value)))
                    worksheet.column_dimensions[col_letter].width = max(max_len + 4, 12)
                    
            excel_data = output.getvalue()
            
            st.download_button(
                label="📥 Unduh Data Rekapitulasi (Excel)",
                data=excel_data,
                file_name=f"rekap_gempita_bang_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
            
            # --- FITUR HAPUS DATA PESERTA TERTENTU ---
            st.markdown("---")
            st.markdown("### 🗑️ Hapus Data Peserta Tertentu")
            
            list_pilihan_hapus = [f"{row['Nama Peserta']} — {row['Judul Karya']} ({row['Waktu Input']})" for row in st.session_state.data_peserta]
            peserta_terpilih = st.selectbox("Pilih Data Peserta yang Ingin Dihapus", ["-- Pilih Data --"] + list_pilihan_hapus)
            
            if peserta_terpilih != "-- Pilih Data --":
                if st.button("Hapus Data Terpilih", type="primary", use_container_width=True):
                    st.session_state.data_peserta = [
                        row for row in st.session_state.data_peserta 
                        if f"{row['Nama Peserta']} — {row['Judul Karya']} ({row['Waktu Input']})" != peserta_terpilih
                    ]
                    save_data_to_csv(st.session_state.data_peserta)
                    st.success(f"Data **{peserta_terpilih}** berhasil dihapus!")
                    st.rerun()
            
            st.markdown("---")
            if st.button("🗑️ Hapus Semua Data Tersimpan", type="primary", use_container_width=True):
                st.session_state.data_peserta = []
                if os.path.exists(DATA_FILE):
                    os.remove(DATA_FILE)
                st.success("Semua data berhasil dibersihkan!")
                st.rerun()

# --- FOOTER ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>© 2026 SIAP-GEMPITA BANG — Cabang Dinas Pendidikan Wilayah Kabupaten Bangkalan</p>", unsafe_allow_html=True)
