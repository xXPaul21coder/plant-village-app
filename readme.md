# 🌿 PlantVillage AI — Diagnóstico Foliar con Redes Neuronales Convolucionales (CNN)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow%20%2F%20Keras-2.x-FF6F00?logo=tensorflow&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)
![Status](https://img.shields.io/badge/Estado-Activo-2D6A4F)

Aplicación web interactiva impulsada por **Deep Learning** para la detección y clasificación automática de enfermedades en hojas de cultivos agrícolas (**tomate, papa y pimiento morrón**) a partir de imágenes foliares.

---

## 📋 Descripción del Proyecto

El diagnóstico temprano de enfermedades en cultivos es fundamental para evitar pérdidas agrícolas y optimizar el uso de tratamientos fitosanitarios. Este proyecto implementa una **Red Neuronal Convolucional (CNN)** entrenada con el dataset **PlantVillage**, integrada en una interfaz web desarrollada en **Streamlit** que permite analizar fotografías subidas por el usuario o evaluar muestras precargadas en tiempo real.

### Características Principales
* **Diagnóstico Bilingüe (Español / Inglés):** Identificación clara del cultivo, la patología detectada y su traducción técnica.
* **Semáforo de Estado Sanitario:** Clasificación visual inmediata entre **Planta Sana (`Healthy`)** y **Planta Enferma (`Diseased`)**.
* **Análisis Probabilístico Top-3:** Visualización de la confianza de la predicción principal junto con un gráfico comparativo de las 3 clases más probables.
* **Banco de Muestras Integrado:** Permite probar el modelo al instante con 10 imágenes de muestra (`1.jpg` a `10.jpg`) de forma aleatoria o manual.

---

## 🧠 Especificaciones Técnicas del Modelo (CNN)

El modelo entrenado (`plant_village_best.keras`) sigue un pipeline estricto de preprocesamiento e inferencia:

| Parámetro | Especificación |
| :--- | :--- |
| **Arquitectura** | Red Neuronal Convolucional (CNN) |
| **Dimensiones de Entrada** | $128 \times 128$ píxeles |
| **Espacio de Color** | RGB (3 canales) |
| **Normalización** | Escalado lineal en el rango $[0, 1]$ (`pixel / 255.0`, tipo `float32`) |
| **Tensor de Entrada** | `(1, 128, 128, 3)` |
| **Número de Clases** | 15 categorías (3 cultivos) |

---

## 🌱 Clases Soportadas (15 Categorías)

El modelo clasifica las imágenes en orden alfabético según las siguientes etiquetas del dataset **PlantVillage**:

| Índice | Etiqueta Original | Cultivo | Diagnóstico (Español) | Estado |
| :---: | :--- | :--- | :--- | :---: |
| `0` | `Pepper__bell___Bacterial_spot` | 🫑 Pimiento | Mancha Bacteriana | ⚠️ Enferma |
| `1` | `Pepper__bell___healthy` | 🫑 Pimiento | Planta Sana | ✅ Sana |
| `2` | `Potato___Early_blight` | 🥔 Papa | Tizón Temprano | ⚠️ Enferma |
| `3` | `Potato___Late_blight` | 🥔 Papa | Tizón Tardío | ⚠️ Enferma |
| `4` | `Potato___healthy` | 🥔 Papa | Planta Sana | ✅ Sana |
| `5` | `Tomato_Bacterial_spot` | 🍅 Tomate | Mancha Bacteriana | ⚠️ Enferma |
| `6` | `Tomato_Early_blight` | 🍅 Tomate | Tizón Temprano | ⚠️ Enferma |
| `7` | `Tomato_Late_blight` | 🍅 Tomate | Tizón Tardío | ⚠️ Enferma |
| `8` | `Tomato_Leaf_Mold` | 🍅 Tomate | Moho de la Hoja | ⚠️ Enferma |
| `9` | `Tomato_Septoria_leaf_spot` | 🍅 Tomate | Mancha Foliar por Septoria | ⚠️ Enferma |
| `10` | `Tomato_Spider_mites_Two_spotted_spider_mite` | 🍅 Tomate | Araña Roja (Ácaro de Dos Puntos) | ⚠️ Enferma |
| `11` | `Tomato__Target_Spot` | 🍅 Tomate | Mancha Diana | ⚠️ Enferma |
| `12` | `Tomato__Tomato_YellowLeaf__Curl_Virus` | 🍅 Tomate | Virus del Rizado Amarillo de la Hoja | ⚠️ Enferma |
| `13` | `Tomato__Tomato_mosaic_virus` | 🍅 Tomate | Virus del Mosaico del Tomate | ⚠️ Enferma |
| `14` | `Tomato_healthy` | 🍅 Tomate | Planta Sana | ✅ Sana |

---

## 📁 Estructura del Repositorio

```text
├── app.py                      # Aplicación web principal en Streamlit
├── plant_village_best.keras    # Modelo CNN entrenado y serializado
├── requirements.txt            # Dependencias del proyecto
├── 1.jpg ... 10.jpg            # Banco de 10 imágenes de muestra para pruebas rápidas
└── README.md                   # Documentación del proyecto
```

---

## 🚀 Instalación y Ejecución Local

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/tu-usuario/tu-repositorio.git
   cd tu-repositorio
   ```

2. **Crear y activar un entorno virtual:**
   * En Windows:
     ```bash
     python -m venv .venv
     .venv\Scripts\activate
     ```
   * En macOS / Linux:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Instalar las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la aplicación:**
   ```bash
   streamlit run app.py
   ```

---

## 🛠️ Tecnologías Utilizadas
* **Python** — Lenguaje principal de desarrollo.
* **TensorFlow / Keras** — Entrenamiento e inferencia de la Red Neuronal Convolucional.
* **Streamlit** — Desarrollo y despliegue de la interfaz web interactiva.
* **NumPy & Pillow (PIL)** — Procesamiento y normalización de matrices de imágenes.
* **Plotly** — Visualización interactiva de probabilidades de predicción.