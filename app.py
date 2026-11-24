
import streamlit as st
import os
import tempfile
import json
from converter import inspect_mod

st.set_page_config(
    page_title="FS26 Mobile Mod Converter",
    page_icon="🚜",
    layout="wide"
)

st.title("🚜 FS26 Mobile Mod Converter")
st.subheader("Konwerter modów FS22 / FS25 → FS26 Mobile")

st.info("Pierwsza wersja: analiza modów ZIP do 500 MB.")

uploaded = st.file_uploader(
    "Wybierz mod ZIP",
    type=["zip"]
)

if uploaded:
    if uploaded.size > 500 * 1024 * 1024:
        st.error("Mod przekracza limit 500 MB.")
    else:
        st.success("Mod został wczytany!")

        if st.button("🔍 ANALIZUJ MOD", type="primary"):
            with tempfile.NamedTemporaryFile(
                suffix=".zip",
                delete=False
            ) as temp:
                temp.write(uploaded.getvalue())
                path = temp.name

            try:
                result = inspect_mod(path)

                st.subheader("Raport analizy")
                st.json(result)

                st.download_button(
                    "Pobierz raport JSON",
                    json.dumps(result, indent=2),
                    file_name="raport_FS26.json"
                )
            finally:
                os.remove(path)
              
