import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
from modules.risk_analyzer import analyze_risk, analyze_evidence
from modules.db.sqlite_handler import (
    init_db, save_case, save_publicering,
    get_case_by_lagrum, list_cases, log_event
)
from modules.puh.analyzer import generate_pm, wrap_pm_with_policy
from modules.puh.rattsfallsanalys import analysera_rattsfall
import datetime

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
            save_case(lagrum, beskrivning, datetime.datetime.now().strftime("%Y-%m-%d"))
            st.success("⚖️ Fall sparat!")

        # Analysera och spara publicering
        evidence_result = analyze_evidence(document_text)
        st.markdown("### 🔍 Bevisanalys")
        st.json(evidence_result)
        if st.button("Spara bevisanalys"):
            save_publicering(1, str(evidence_result), datetime.datetime.now().strftime("%Y-%m-%d"))
            st.success("✅ Bevisanalys sparad!")

        risk_result = analyze_risk(document_text)
        st.markdown("### 📊 Strategiförslag")
        st.json(risk_result)
        if st.button("Spara strategiförslag"):
            save_publicering(1, str(risk_result), datetime.datetime.now().strftime("%Y-%m-%d"))
            st.success("✅ Strategiförslag sparad!")

        log_event(f"Uppladdning av {uploaded_file.name}", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    else:
        st.write("❌ Ingen giltig text extraherad från filen.")
else:
    st.write("Ingen text att analysera. Ladda upp en fil först.")

# Sökfunktion och lista över fall
st.markdown("### 📋 Sök och lista sparade fall")
sokterm = st.text_input("🔍 Sök lagrum eller beskrivning").strip().lower()
cases = list_cases()

if sokterm:
    filtrerade = [case for case in cases if sokterm in case[1].lower() or sokterm in case[2].lower()]
    st.write(f"🔎 {len(filtrerade)} träff(ar):")
    st.write(filtrerade)
else:
    st.write("📁 Alla sparade fall:")
    st.write(cases)

# Välj ett fall för PM-generering
st.markdown("### 🧾 Generera juridiskt PM från rättsfall")
if cases:
    valt_fall = st.selectbox("Välj fall för PM-generering", cases, format_func=lambda x: x[2])
    dummy_data = {
        "rubrik": valt_fall[2],
        "lagrumLista": [valt_fall[1]],
        "avgorandedomstol": "Ej angivet",
        "avgorandedatum": valt_fall[3],
        "referat": f"Text extraherad från fil: {valt_fall[2]}"
    }

    if st.button("🧠 Generera GPT-analyserat PM"):
        resultat = analysera_rattsfall(dummy_data)
        pm = generate_pm(resultat)
        policy_pm = wrap_pm_with_policy(pm)
        st.text_area("📜 PM med GPT-policy", policy_pm, height=500)

        if st.button("💾 Spara PM till fil"):
            filename = f"pm_utskrift_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(policy_pm)
            st.success(f"✅ PM har sparats till {filename}")
else:
    st.warning("❗️Inga sparade fall hittades i databasen.")
