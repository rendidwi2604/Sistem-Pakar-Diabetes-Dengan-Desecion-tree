import streamlit as st
import pandas as pd
import joblib
import numpy as np
from fpdf import FPDF
import datetime
import re
import os

# ------------------------------------------
# Konfigurasi
# ------------------------------------------
LOGO_PATH = "logo.png"  # pastikan logo.png ada di folder yang sama
USER_CREDENTIALS = {
    "dr_andika": "password123",
    "dr_maya": "dokterku",
    "syno": "dokter"
}
SOLUSI_DIAGNOSIS = {
    "Diabetes Tipe 1": "Terapi insulin seumur hidup dan pemantauan rutin diperlukan.",
    "Diabetes Tipe 2": "Gaya hidup sehat, olahraga, dan obat oral mungkin diperlukan.",
    "Diabetes Gestasional": "Pemantauan kadar glukosa selama kehamilan sangat penting.",
    "Prediabetes": "Perubahan gaya hidup dapat mencegah perkembangan menjadi diabetes.",
    "Normal": "Tidak ada indikasi diabetes. Tetap jaga gaya hidup sehat."
}

# ------------------------------------------
# Fungsi Pendukung
# ------------------------------------------
def remove_emoji(text):
    return re.sub(r'[^\x00-\x7F]+', '', text)

def buat_pdf(nama, id_pasien, diagnosis, confidence, solusi):
    pdf = FPDF()
    pdf.add_page()
    if os.path.exists(LOGO_PATH):
        pdf.image(LOGO_PATH, x=80, y=10, h=25)
 # logo di tengah atas
        pdf.ln(35)

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, txt="Laporan Diagnosis Diabetes", ln=True, align="C")
    pdf.ln(5)

    pdf.set_font("Arial", size=11)
    pdf.cell(0, 8, txt="Klinik Sehat Sentosa", ln=True)
    pdf.cell(0, 8, txt="Jl. Sehat No. 123, Jakarta", ln=True)
    pdf.cell(0, 8, txt="Telp: (021) 12345678 | Email: info@kliniksentosa.co.id", ln=True)
    pdf.cell(0, 8, txt=f"No. Surat: DGN-{datetime.datetime.now().strftime('%Y%m%d%H%M')}", ln=True)
    pdf.cell(0, 8, txt=f"Tanggal: {datetime.date.today().strftime('%d-%m-%Y')}", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Data Pasien:", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.cell(0, 8, f"Nama Pasien: {nama}", ln=True)
    pdf.cell(0, 8, f"ID Pasien: {id_pasien}", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Hasil Diagnosis:", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.cell(0, 8, f"Diagnosis: {diagnosis}", ln=True)
    pdf.cell(0, 8, f"Tingkat Kepercayaan: {confidence:.2f}%", ln=True)
    pdf.multi_cell(0, 8, f"Solusi: {remove_emoji(solusi)}")

    path = f"laporan_{nama}_{id_pasien}.pdf"
    pdf.output(path)
    return path

def label_ya_tidak(label): return 1 if label == "Ya" else 0
ya_tidak = ["Tidak", "Ya"]

# ------------------------------------------
# State Init
# ------------------------------------------
for key in ["logged_in", "username", "diagnosis_result"]:
    if key not in st.session_state:
        st.session_state[key] = None

# ------------------------------------------
# Login Page
# ------------------------------------------
if not st.session_state.logged_in:
   if os.path.exists(LOGO_PATH):
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.image(LOGO_PATH, width=150)

         
    
    st.title("Login Dokter")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
        else:
            st.error("Username atau password salah.")
    st.stop()

# ------------------------------------------
# Halaman Utama
# ------------------------------------------
st.title("Sistem Pakar Diagnosis Diabetes")
st.sidebar.success(f"Login sebagai: {st.session_state.username}")
if st.sidebar.button("Logout"):
    st.session_state.logged_in = None
    st.session_state.username = None
    st.session_state.diagnosis_result = None
    st.rerun()

# ------------------------------------------
# Load Model
# ------------------------------------------
model = joblib.load('diabetes_model.pkl')
le_target = joblib.load('label_encoder.pkl')
le_dict = joblib.load('feature_encoders.pkl')

with st.form("form_diagnosis"):
    st.subheader("Input Data Pasien")
    nama_pasien = st.text_input("Nama Pasien")
    id_pasien = st.text_input("ID Pasien")
    genetic = label_ya_tidak(st.selectbox("Genetik Positif?", ya_tidak))
    autoantibodi = label_ya_tidak(st.selectbox("Autoantibodi Positif?", ya_tidak))
    riwayat_keluarga = label_ya_tidak(st.selectbox("Riwayat Keluarga?", ya_tidak))
    faktor_lingkungan = label_ya_tidak(st.selectbox("Faktor Lingkungan?", ya_tidak))
    insulin = st.number_input("Tingkat Insulin", min_value=0)
    usia = st.number_input("Usia", min_value=0)
    bmi = st.number_input("BMI", min_value=0.0)
    tekanan_darah = st.number_input("Tekanan Darah", min_value=0)
    kolesterol = st.number_input("Kolesterol", min_value=0)
    lingkar_pinggang = st.number_input("Lingkar Pinggang", min_value=0)
    aktivitas = ["Rendah", "Sedang", "Tinggi"].index(st.selectbox("Aktivitas Fisik", ["Rendah", "Sedang", "Tinggi"]))
    diet = label_ya_tidak(st.selectbox("Pola Makan Sehat?", ya_tidak))
    glukosa = st.number_input("Kadar Glukosa Darah", min_value=0)
    gtt = st.number_input("Glucose Tolerance Test", min_value=0)
    etnis = st.selectbox("Etnis", le_dict['Ethnicity'].classes_)
    sosial_eko = st.selectbox("Faktor Sosial Ekonomi", le_dict['Socioeconomic Factors'].classes_)
    rokok = st.selectbox("Status Merokok", le_dict['Smoking Status'].classes_)
    alkohol = label_ya_tidak(st.selectbox("Konsumsi Alkohol?", ya_tidak))
    pcos = label_ya_tidak(st.selectbox("Riwayat PCOS?", ya_tidak))
    gestasional = label_ya_tidak(st.selectbox("Diabetes Gestasional?", ya_tidak))
    hamil = st.selectbox("Riwayat Kehamilan", le_dict['Pregnancy History'].classes_)
    kenaikan_bb = st.number_input("Kenaikan BB saat Hamil", min_value=0)
    bb_lahir = st.number_input("Berat Badan Lahir", min_value=0)
    onset_dini = label_ya_tidak(st.selectbox("Gejala Onset Dini?", ya_tidak))
    tes_genetik = label_ya_tidak(st.selectbox("Tes Genetik Positif?", ya_tidak))
    neuro = ["Normal", "Ringan", "Sedang", "Berat"].index(st.selectbox("Evaluasi Neurologis", ["Normal", "Ringan", "Sedang", "Berat"]))
    pankreas = label_ya_tidak(st.selectbox("Masalah Pankreas?", ya_tidak))
    paru = label_ya_tidak(st.selectbox("Masalah Paru?", ya_tidak))
    fibrosis = label_ya_tidak(st.selectbox("Fibrosis Cystic?", ya_tidak))
    steroid = label_ya_tidak(st.selectbox("Penggunaan Steroid?", ya_tidak))
    hati = label_ya_tidak(st.selectbox("Fungsi Hati Abnormal?", ya_tidak))
    enzim = st.number_input("Tingkat Enzim Pencernaan", min_value=0)
    urin = st.selectbox("Tes Urin", [0.0, 1.0, 2.0, 3.0])

    submitted = st.form_submit_button("Diagnosa Sekarang")

    if submitted:
        try:
            input_data = {
                'Genetic Markers': genetic,
                'Autoantibodies': autoantibodi,
                'Family History': riwayat_keluarga,
                'Environmental Factors': faktor_lingkungan,
                'Insulin Levels': insulin,
                'Age': usia,
                'BMI': bmi,
                'Physical Activity': aktivitas,
                'Dietary Habits': diet,
                'Blood Pressure': tekanan_darah,
                'Cholesterol Levels': kolesterol,
                'Waist Circumference': lingkar_pinggang,
                'Blood Glucose Levels': glukosa,
                'Ethnicity': etnis,
                'Socioeconomic Factors': sosial_eko,
                'Smoking Status': rokok,
                'Alcohol Consumption': alkohol,
                'Glucose Tolerance Test': gtt,
                'History of PCOS': pcos,
                'Previous Gestational Diabetes': gestasional,
                'Pregnancy History': hamil,
                'Weight Gain During Pregnancy': kenaikan_bb,
                'Pancreatic Health': pankreas,
                'Pulmonary Function': paru,
                'Cystic Fibrosis Diagnosis': fibrosis,
                'Steroid Use History': steroid,
                'Genetic Testing': tes_genetik,
                'Neurological Assessments': neuro,
                'Liver Function Tests': hati,
                'Digestive Enzyme Levels': enzim,
                'Urine Test': urin,
                'Birth Weight': bb_lahir,
                'Early Onset Symptoms': onset_dini
            }

            for col, le in le_dict.items():
                input_data[col] = le.transform([input_data[col]])[0]

            input_df = pd.DataFrame([input_data])
            y_pred = model.predict(input_df)[0]
            proba = model.predict_proba(input_df)[0]
            diagnosis = le_target.inverse_transform([y_pred])[0]
            confidence = np.max(proba) * 100
            solusi = SOLUSI_DIAGNOSIS.get(diagnosis, "Silakan konsultasikan lebih lanjut.")
            pdf_path = buat_pdf(nama_pasien, id_pasien, diagnosis, confidence, solusi)

            st.session_state.diagnosis_result = {
                "diagnosis": diagnosis,
                "confidence": confidence,
                "solusi": solusi,
                "proba": proba,
                "pdf_path": pdf_path,
                "nama": nama_pasien,
                "id": id_pasien
            }

        except Exception as e:
            st.error(f"\u274c Terjadi kesalahan saat diagnosis: {e}")

# ------------------------------------------
# Hasil Diagnosis & Download PDF
# ------------------------------------------
result = st.session_state.diagnosis_result
if result:
    st.success(f"Hasil Diagnosis: {result['diagnosis']}")
    st.info(f"Tingkat Kepercayaan: {result['confidence']:.2f}%")
    st.markdown(f"**Solusi:** {result['solusi']}")
    with st.expander("Detail Probabilitas"):
        all_diagnoses = le_target.inverse_transform(model.classes_)
        proba_dict = {d: f"{p*100:.2f}%" for d, p in zip(all_diagnoses, result['proba'])}
        st.table(proba_dict)

    with open(result['pdf_path'], "rb") as f:
       st.download_button("Unduh Laporan PDF", f, file_name=result['pdf_path'], mime="application/pdf")
