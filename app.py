import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
from modules.risk_analyzer import analyze_risk, analyze_evidence
from modules.db.sqlite_handler import init_db, save_case, save_publicering, get_case_by_lagrum, list_cases, log_event
from datetime import datetime

# Initialisera databasen vid appstart
init_db()

# Sätt upp sidans layout
st.set_page_config(page_title="Juridisk AI-Portal", layout="centered")
st.title("⚖️ Juridisk AI-Portal")
st.markdown("🧠 Intelligent juridisk analys och beslutsstöd")

# Filuppladdning
st.markdown("### 📄 Dokumenthantering")
uploaded_file = st.file_uploader("Välj dokument att analysera", type=["pdf", "docx", "txt", "jpeg", "jpg"])
if uploaded_file is not None:
    document_text = ""
    if uploaded_file.type == "application/pdf":
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            document_text = "".join(page.get_text() for page in doc if page.get_text())
    elif uploaded_file.type in ["image/jpeg", "image/jpg"]:
        image = Image.open(uploaded_file)
        document_text = pytesseract.image_to_string(image)
    else:
        document_text = uploaded_file.read().decode("utf-8")

    st.write("✅ Fil uppladdad:", uploaded_file.name)
    st.write("Dokumentinnehåll:")
    st.text(document_text)
    st.write(f"Felsök: Längd på extraherad text: {len(document_text)} tecken")

    # Spara fall i databasen
    if document_text.strip():
        lagrum = st.text_input("Ange lagrum (t.ex. 12 kap JB)", "12 kap JB")
        beskrivning = st.text_input("Ange beskrivning", f"Fall baserat på {uploaded_file.name}")
        if st.button("Spara fall"):
            save_case(lagrum, beskrivning, datetime.now().strftime("%Y-%m-%d"))
            st.success("⚖️ Fall sparat!")

        # Analysera och spara publicering
        evidence_result = analyze_evidence(document_text)
        st.markdown("### 🔍 Bevisanalys")
        st.json(evidence_result)
        if st.button("Spara bevisanalys"):
            save_publicering(1, str(evidence_result), datetime.now().strftime("%Y-%m-%d"))
            st.success("✅ Bevisanalys sparad!")

        risk_result = analyze_risk(document_text)
        st.markdown("### 📊 Strategiförslag")
        st.json(risk_result)
        if st.button("Spara strategiförslag"):
            save_publicering(1, str(risk_result), datetime.now().strftime("%Y-%m-%d"))
            st.success("✅ Strategiförslag sparat!")

        # Logga händelsen
        log_event(f"Uppladdning av {uploaded_file.name}", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    else:
        st.write("❌ Ingen giltig text extraherad från filen.")
else:
    st.write("Ingen text att analysera. Ladda upp en fil först.")

# Visa listan över fall
st.markdown("### 📋 Lista över fall")
cases = list_cases()
st.write(cases)