import streamlit as st
import google.generativeai as genai
from fpdf import FPDF

# 1. Configuración de la página
st.set_page_config(page_title="Generador Educativo", page_icon="🎨")

# 2. Configuración de la API Key (usando Secrets)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # Usamos gemini-1.5-flash que es el modelo más actual y rápido
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("⚠️ Error: Configura tu GOOGLE_API_KEY en los Secrets de Streamlit.")

st.title("🎨 Creador de Guías para Niños")
st.write("Genera contenido educativo fácil de leer y descargar.")

# Entrada del usuario
tema = st.text_input("¿Qué tema quieres explicar hoy?", placeholder="Ej: Las Abejas, El Ciclo del Agua...")

if st.button("✨ ¡Generar Contenido!"):
    if tema:
        # Prompt optimizado para evitar errores en el PDF
        prompt = f"""Actúa como un maestro de primaria. 
        Explica el tema '{tema}' para niños de 6 a 9 años. 
        Usa lenguaje sencillo. Divide en: Título, Explicación (2 párrafos) y Dato Curioso.
        IMPORTANTE: No uses asteriscos, ni emojis, ni símbolos raros."""

        with st.spinner("Preparando el material..."):
            try:
                # Generar texto con la IA
                response = model.generate_content(prompt)
                texto_final = response.text
                
                # Mostrar en pantalla
                st.subheader("Vista previa:")
                st.info(texto_final)

                # --- Lógica del PDF ---
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Helvetica", 'B', 16)
                pdf.cell(0, 10, txt="Guía Educativa Personalizada", ln=True, align='C')
                pdf.ln(10)
                
                pdf.set_font("Helvetica", size=12)
                # Limpiamos el texto por si la IA puso símbolos
                texto_limpio = texto_final.replace("**", "").replace("#", "").replace("*", "")
                
                # Escribimos el contenido en el PDF
                pdf.multi_cell(0, 10, txt=texto_limpio.encode('latin-1', 'replace').decode('latin-1'))
                
                # Botón de descarga
                pdf_output = pdf.output(dest='S')
                st.download_button(
                    label="📩 Descargar PDF listo para imprimir",
                    data=pdf_output,
                    file_name=f"Guia_{tema}.pdf",
                    mime="application/pdf"
                )

            except Exception as e:
                st.error(f"Ocurrió un error inesperado: {e}")
    else:
        st.warning("Por favor, escribe un tema.")
