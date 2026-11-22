import glob
import os
import random
from typing import Any

import numpy as np
import plotly.graph_objects as go
import streamlit as st
import tensorflow as tf
from PIL import Image

st.set_page_config(
    page_title="PlantVillage AI - Diagnóstico Foliar",
    page_icon="🌿",
    layout="wide",
)

CLASS_CATALOG: list[dict[str, str]] = [
    {
        "raw": "Pepper__bell___Bacterial_spot",
        "en": "Bell Pepper - Bacterial Spot",
        "es": "Pimiento Morrón - Mancha Bacteriana",
        "status": "Enferma",
        "crop": "Pimiento",
        "crop_icon": "🫑",
    },
    {
        "raw": "Pepper__bell___healthy",
        "en": "Bell Pepper - Healthy",
        "es": "Pimiento Morrón - Sana",
        "status": "Sana",
        "crop": "Pimiento",
        "crop_icon": "🫑",
    },
    {
        "raw": "Potato___Early_blight",
        "en": "Potato - Early Blight",
        "es": "Papa - Tizón Temprano",
        "status": "Enferma",
        "crop": "Papa",
        "crop_icon": "🥔",
    },
    {
        "raw": "Potato___Late_blight",
        "en": "Potato - Late Blight",
        "es": "Papa - Tizón Tardío",
        "status": "Enferma",
        "crop": "Papa",
        "crop_icon": "🥔",
    },
    {
        "raw": "Potato___healthy",
        "en": "Potato - Healthy",
        "es": "Papa - Sana",
        "status": "Sana",
        "crop": "Papa",
        "crop_icon": "🥔",
    },
    {
        "raw": "Tomato_Bacterial_spot",
        "en": "Tomato - Bacterial Spot",
        "es": "Tomate - Mancha Bacteriana",
        "status": "Enferma",
        "crop": "Tomate",
        "crop_icon": "🍅",
    },
    {
        "raw": "Tomato_Early_blight",
        "en": "Tomato - Early Blight",
        "es": "Tomate - Tizón Temprano",
        "status": "Enferma",
        "crop": "Tomate",
        "crop_icon": "🍅",
    },
    {
        "raw": "Tomato_Late_blight",
        "en": "Tomato - Late Blight",
        "es": "Tomate - Tizón Tardío",
        "status": "Enferma",
        "crop": "Tomate",
        "crop_icon": "🍅",
    },
    {
        "raw": "Tomato_Leaf_Mold",
        "en": "Tomato - Leaf Mold",
        "es": "Tomate - Moho de la Hoja",
        "status": "Enferma",
        "crop": "Tomate",
        "crop_icon": "🍅",
    },
    {
        "raw": "Tomato_Septoria_leaf_spot",
        "en": "Tomato - Septoria Leaf Spot",
        "es": "Tomate - Mancha Foliar por Septoria",
        "status": "Enferma",
        "crop": "Tomate",
        "crop_icon": "🍅",
    },
    {
        "raw": "Tomato_Spider_mites_Two_spotted_spider_mite",
        "en": "Tomato - Two-Spotted Spider Mite",
        "es": "Tomate - Araña Roja (Ácaro de Dos Puntos)",
        "status": "Enferma",
        "crop": "Tomate",
        "crop_icon": "🍅",
    },
    {
        "raw": "Tomato__Target_Spot",
        "en": "Tomato - Target Spot",
        "es": "Tomate - Mancha Diana",
        "status": "Enferma",
        "crop": "Tomate",
        "crop_icon": "🍅",
    },
    {
        "raw": "Tomato__Tomato_YellowLeaf__Curl_Virus",
        "en": "Tomato - Yellow Leaf Curl Virus",
        "es": "Tomate - Virus del Rizado Amarillo de la Hoja",
        "status": "Enferma",
        "crop": "Tomate",
        "crop_icon": "🍅",
    },
    {
        "raw": "Tomato__Tomato_mosaic_virus",
        "en": "Tomato - Mosaic Virus",
        "es": "Tomate - Virus del Mosaico del Tomate",
        "status": "Enferma",
        "crop": "Tomate",
        "crop_icon": "🍅",
    },
    {
        "raw": "Tomato_healthy",
        "en": "Tomato - Healthy",
        "es": "Tomate - Sana",
        "status": "Sana",
        "crop": "Tomate",
        "crop_icon": "🍅",
    },
]

IMAGE_SIZE = (128, 128)


def inject_custom_css() -> None:
    """Inject botanical/Agritech custom CSS and hide default Streamlit chrome."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header[data-testid="stHeader"] {background: transparent;}

        .stApp {
            background: linear-gradient(180deg, #F4F9F6 0%, #FFFFFF 45%, #F7FAF8 100%);
            color: #1B4332;
        }

        .hero-banner {
            background: linear-gradient(135deg, #1B4332 0%, #2D6A4F 65%, #40916C 100%);
            border-radius: 20px;
            padding: 2.2rem 2.5rem;
            color: #FFFFFF;
            box-shadow: 0 14px 34px rgba(27, 67, 50, 0.16);
            margin-bottom: 1.75rem;
            position: relative;
            overflow: hidden;
        }

        .hero-badge {
            display: inline-block;
            background: rgba(216, 243, 220, 0.18);
            border: 1px solid rgba(216, 243, 220, 0.4);
            color: #D8F3DC;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            padding: 0.35rem 0.85rem;
            border-radius: 999px;
            margin-bottom: 0.85rem;
        }

        .hero-title {
            font-size: 2.2rem;
            font-weight: 800;
            line-height: 1.15;
            margin: 0 0 0.6rem 0;
            color: #FFFFFF;
        }

        .hero-subtitle {
            font-size: 1.02rem;
            line-height: 1.55;
            color: #E8F5EC;
            margin: 0 0 1.2rem 0;
            max-width: 780px;
        }

        .crop-pills {
            display: flex;
            flex-wrap: wrap;
            gap: 0.6rem;
        }

        .crop-pill {
            background: rgba(255, 255, 255, 0.14);
            border: 1px solid rgba(255, 255, 255, 0.25);
            color: #FFFFFF;
            padding: 0.4rem 0.9rem;
            border-radius: 999px;
            font-size: 0.88rem;
            font-weight: 600;
        }

        .section-card {
            background: #FFFFFF;
            border: 1px solid #E1EFE6;
            border-radius: 16px;
            padding: 1.4rem 1.5rem;
            box-shadow: 0 8px 24px rgba(27, 67, 50, 0.06);
            margin-bottom: 1.25rem;
        }

        .sampler-card {
            background: linear-gradient(135deg, #EDF8F0 0%, #D8F3DC 100%);
            border: 1px solid #B7E4C7;
            border-radius: 16px;
            padding: 1.35rem 1.5rem;
            box-shadow: 0 8px 20px rgba(45, 106, 79, 0.08);
            margin-bottom: 1rem;
        }

        .sampler-title {
            color: #1B4332;
            font-size: 1.08rem;
            font-weight: 700;
            margin: 0 0 0.35rem 0;
        }

        .sampler-desc {
            color: #2D6A4F;
            font-size: 0.93rem;
            margin: 0;
            line-height: 1.45;
        }

        div.stButton > button {
            background: linear-gradient(135deg, #2D6A4F 0%, #1B4332 100%);
            color: #FFFFFF;
            border: none;
            border-radius: 12px;
            padding: 0.65rem 1.2rem;
            font-weight: 600;
            letter-spacing: 0.01em;
            box-shadow: 0 4px 12px rgba(27, 67, 50, 0.18);
            transition: all 0.2s ease;
        }

        div.stButton > button:hover {
            background: linear-gradient(135deg, #40916C 0%, #2D6A4F 100%);
            transform: translateY(-1px);
            box-shadow: 0 6px 16px rgba(27, 67, 50, 0.24);
            color: #FFFFFF;
        }

        div.stButton > button:active {
            transform: translateY(0px);
        }

        .diagnosis-card {
            background: #FFFFFF;
            border: 1px solid #E1EFE6;
            border-radius: 16px;
            padding: 1.5rem 1.65rem;
            box-shadow: 0 10px 28px rgba(27, 67, 50, 0.08);
        }

        .status-badge-healthy {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: linear-gradient(135deg, #D8F3DC 0%, #B7E4C7 100%);
            color: #1B4332;
            border: 1.5px solid #2D6A4F;
            border-radius: 12px;
            padding: 0.65rem 1.1rem;
            font-weight: 800;
            font-size: 0.96rem;
            letter-spacing: 0.03em;
            margin-bottom: 1rem;
        }

        .status-badge-diseased {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: linear-gradient(135deg, #FFF1EB 0%, #FFE0D1 100%);
            color: #9C2B0E;
            border: 1.5px solid #D95D39;
            border-radius: 12px;
            padding: 0.65rem 1.1rem;
            font-weight: 800;
            font-size: 0.96rem;
            letter-spacing: 0.03em;
            margin-bottom: 1rem;
        }

        .diag-es {
            font-size: 1.55rem;
            font-weight: 800;
            color: #1B4332;
            margin: 0.25rem 0 0.2rem 0;
            line-height: 1.25;
        }

        .diag-en {
            font-size: 1.0rem;
            font-weight: 500;
            color: #52796F;
            margin: 0 0 1rem 0;
        }

        .meta-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 0.75rem;
            margin: 0.75rem 0 1.1rem 0;
        }

        .meta-box {
            background: #F6FAF7;
            border: 1px solid #DFEDE4;
            border-radius: 12px;
            padding: 0.75rem 0.95rem;
        }

        .meta-label {
            font-size: 0.76rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: #52796F;
            font-weight: 700;
            margin-bottom: 0.2rem;
        }

        .meta-value {
            font-size: 1.12rem;
            font-weight: 700;
            color: #1B4332;
        }

        .image-frame {
            background: #FFFFFF;
            border: 1px solid #E1EFE6;
            border-radius: 16px;
            padding: 1rem;
            box-shadow: 0 10px 28px rgba(27, 67, 50, 0.08);
        }

        .image-frame img {
            border-radius: 12px !important;
        }

        .source-tag {
            display: inline-block;
            background: #D8F3DC;
            color: #1B4332;
            font-size: 0.82rem;
            font-weight: 700;
            padding: 0.3rem 0.75rem;
            border-radius: 999px;
            margin-top: 0.65rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def find_keras_model() -> str | None:
    """Detect the first .keras model file in the current working directory."""
    candidates = sorted(glob.glob("*.keras"))
    return candidates[0] if candidates else None


@st.cache_resource(show_spinner="Cargando modelo de Deep Learning...")
def load_plant_model(model_path: str) -> Any:
    """Load the Keras model once and cache it across reruns."""
    return tf.keras.models.load_model(model_path)


def get_available_samples() -> list[str]:
    """Return existing sample filenames from 1.jpg through 10.jpg."""
    return [f"{i}.jpg" for i in range(1, 11) if os.path.exists(f"{i}.jpg")]


def preprocess_image(image: Image.Image) -> np.ndarray:
    """Apply the exact training preprocessing pipeline: RGB -> 128x128 -> float32/255 -> (1, 128, 128, 3)."""
    rgb_image = image.convert("RGB")
    resized_image = rgb_image.resize(IMAGE_SIZE)
    normalized = np.array(resized_image, dtype=np.float32) / 255.0
    return np.expand_dims(normalized, axis=0)


def predict_leaf(model: Any, image: Image.Image) -> tuple[int, np.ndarray]:
    """Run model inference and return top class index and probability vector."""
    tensor = preprocess_image(image)
    raw_preds = model.predict(tensor, verbose=0)[0]
    preds = np.asarray(raw_preds, dtype=np.float64)
    if np.any(preds < 0) or not np.isclose(np.sum(preds), 1.0, atol=1e-2):
        preds = tf.nn.softmax(preds).numpy()
    top_idx = int(np.argmax(preds))
    return top_idx, preds


def build_top3_chart(preds: np.ndarray) -> go.Figure:
    """Build a clean horizontal Plotly bar chart for the Top-3 predictions."""
    top3_indices = np.argsort(preds)[-3:][::-1]
    labels = []
    values = []
    colors = []

    for rank, idx in enumerate(top3_indices):
        info = CLASS_CATALOG[idx]
        labels.append(info["es"])
        values.append(float(preds[idx]) * 100.0)
        if rank == 0:
            colors.append("#2D6A4F" if info["status"] == "Sana" else "#C85A32")
        else:
            colors.append("#95D5B2" if info["status"] == "Sana" else "#F4A261")

    labels_rev = labels[::-1]
    values_rev = values[::-1]
    colors_rev = colors[::-1]

    fig = go.Figure(
        go.Bar(
            x=values_rev,
            y=labels_rev,
            orientation="h",
            marker=dict(color=colors_rev, line=dict(width=0)),
            text=[f"{v:.2f}%" for v in values_rev],
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Confianza: %{x:.2f}%<extra></extra>",
        )
    )
    fig.update_layout(
        margin=dict(l=10, r=50, t=10, b=10),
        height=210,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            range=[0, 108],
            showgrid=True,
            gridcolor="#E9F2EC",
            ticksuffix="%",
            title=None,
            zeroline=False,
        ),
        yaxis=dict(
            title=None,
            tickfont=dict(size=12, color="#1B4332"),
        ),
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#1B4332"),
    )
    return fig


def init_session_state() -> None:
    """Initialize session state keys for sample and upload tracking."""
    defaults = {
        "selected_source": None,
        "selected_sample": None,
        "last_random_sample": None,
        "last_uploaded_sig": None,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def main() -> None:
    inject_custom_css()
    init_session_state()

    st.markdown(
        """
        <div class="hero-banner">
            <div class="hero-badge">Laboratorio Botánico Inteligente · PlantVillage AI</div>
            <h1 class="hero-title">🌿 Diagnóstico Foliar de Cultivos</h1>
            <p class="hero-subtitle">
                Analiza hojas de plantas en segundos mediante Deep Learning para detectar enfermedades
                fitopatológicas con precisión clínica y apoyar decisiones agronómicas oportunas.
            </p>
            <div class="crop-pills">
                <span class="crop-pill">🍅 Tomate (10 clases)</span>
                <span class="crop-pill">🥔 Papa (3 clases)</span>
                <span class="crop-pill">🫑 Pimiento Morrón (2 clases)</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    model_path = find_keras_model()
    if model_path is None:
        st.error(
            "No se encontró ningún archivo `.keras` en el directorio actual. "
            "Coloca el modelo entrenado (por ejemplo `plant_village_best.keras`) junto a `app.py`."
        )
        st.stop()

    model = load_plant_model(model_path)
    available_samples = get_available_samples()

    col_upload, col_sampler = st.columns([1.05, 1.15], gap="large")

    with col_upload:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### 📤 Sube la fotografía de una hoja")
        st.caption("Formatos soportados: JPG, JPEG y PNG. Se recomienda buena iluminación y enfoque sobre la hoja.")
        uploaded_file = st.file_uploader(
            "Selecciona o arrastra una imagen foliar",
            type=["jpg", "jpeg", "png"],
            label_visibility="collapsed",
        )
        if uploaded_file is not None:
            sig = f"{uploaded_file.name}:{uploaded_file.size}"
            if sig != st.session_state.last_uploaded_sig:
                st.session_state.last_uploaded_sig = sig
                st.session_state.selected_source = "upload"
        st.markdown("</div>", unsafe_allow_html=True)

    with col_sampler:
        st.markdown(
            """
            <div class="sampler-card">
                <p class="sampler-title">🧪 ¿No tienes una imagen a la mano?</p>
                <p class="sampler-desc">
                    ¿No tienes una imagen a la mano? Prueba nuestro sistema seleccionando una muestra aleatoria de nuestro banco de hojas.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if available_samples:
            if st.button("🎲 Probar con una hoja aleatoria", use_container_width=True):
                prev = st.session_state.last_random_sample
                candidates = [s for s in available_samples if s != prev] or available_samples
                chosen = random.choice(candidates)
                st.session_state.last_random_sample = chosen
                st.session_state.selected_sample = chosen
                st.session_state.selected_source = "sample"

            with st.expander("🖼️ Explorar galería rápida (Muestra 1 a Muestra 10)", expanded=False):
                cols = st.columns(5)
                for idx, sample_name in enumerate(available_samples):
                    with cols[idx % 5]:
                        st.image(sample_name, use_container_width=True)
                        sample_num = sample_name.split(".")[0]
                        if st.button(f"Muestra {sample_num}", key=f"btn_{sample_name}", use_container_width=True):
                            st.session_state.selected_sample = sample_name
                            st.session_state.selected_source = "sample"
        else:
            st.warning("No se encontraron imágenes de muestra (`1.jpg` a `10.jpg`) en la carpeta raíz.")

    active_image: Image.Image | None = None
    source_label = ""

    if st.session_state.selected_source == "upload" and uploaded_file is not None:
        active_image = Image.open(uploaded_file)
        source_label = f"Imagen subida por el usuario: {uploaded_file.name}"
    elif st.session_state.selected_source == "sample" and st.session_state.selected_sample:
        sample_path = st.session_state.selected_sample
        if os.path.exists(sample_path):
            active_image = Image.open(sample_path)
            source_label = f"Muestra del banco de hojas: {sample_path}"
    elif uploaded_file is not None:
        active_image = Image.open(uploaded_file)
        source_label = f"Imagen subida por el usuario: {uploaded_file.name}"

    if active_image is None:
        st.info(
            "👆 Sube una fotografía de una hoja o presiona **🎲 Probar con una hoja aleatoria** para iniciar el diagnóstico."
        )
        return

    top_idx, preds = predict_leaf(model, active_image)
    result = CLASS_CATALOG[top_idx]
    confidence_pct = float(preds[top_idx]) * 100.0
    is_healthy = result["status"] == "Sana"

    st.markdown("---")
    left_col, right_col = st.columns([1, 1.3], gap="large")

    with left_col:
        st.markdown('<div class="image-frame">', unsafe_allow_html=True)
        st.markdown("#### 🔬 Hoja Analizada")
        st.image(active_image, use_container_width=True)
        st.markdown(f'<span class="source-tag">📌 {source_label}</span>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with right_col:
        badge_html = (
            '<div class="status-badge-healthy">✅ PLANTA SANA / HEALTHY</div>'
            if is_healthy
            else '<div class="status-badge-diseased">⚠️ PLANTA ENFERMA / DISEASED</div>'
        )

        st.markdown(
            f"""
            <div class="diagnosis-card">
                {badge_html}
                <div class="diag-es">{result["es"]}</div>
                <div class="diag-en">EN: {result["en"]}</div>
                <div class="meta-grid">
                    <div class="meta-box">
                        <div class="meta-label">Cultivo Identificado</div>
                        <div class="meta-value">{result["crop_icon"]} {result["crop"]}</div>
                    </div>
                    <div class="meta-box">
                        <div class="meta-label">Nivel de Confianza</div>
                        <div class="meta-value">{confidence_pct:.2f}%</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("#### 📊 Top-3 Predicciones Más Probables")
        fig = build_top3_chart(preds)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


if __name__ == "__main__":
    main()
