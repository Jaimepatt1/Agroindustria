import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from datetime import datetime

# 1. Configuración inicial de la aplicación
st.set_page_config(
    page_title="Agroindustria en Colombia",
    page_icon="📊",
    layout="wide"
)
st.title("📊 Agroindustria en Colombia")
st.sidebar.title("🔍 Opciones de Navegación")

# 2. Generación de Datos Aleatorios
np.random.seed(42)
data = pd.DataFrame({
    "Fecha": pd.date_range(start="2024-01-01", periods=150, freq="D"),
    "Producción_Ton": np.random.randint(100, 2000, size=150),
    "Área_Ha": np.random.randint(50, 500, size=150),
    "Costo_Producción": np.random.uniform(1000, 10000, size=150),
    "Precio_Mercado": np.random.uniform(500, 5000, size=150),
    "Rendimiento": np.random.uniform(0.5, 2.5, size=150),
    "Exportaciones_Ton": np.random.randint(0, 1500, size=150),
    "Región": np.random.choice(["Norte", "Sur", "Este", "Oeste"], size=150),
    "Cultivo": np.random.choice(["Café", "Cacao", "Banano", "Palma"], size=150)
})

# 3. Implementación de la Barra de Navegación
menu = st.sidebar.radio(
    "Selecciona una opción:",
    ["Inicio", "Datos", "Visualización", "Configuración"]
)

# 4. Mostrar los Datos
if menu == "Datos":
    st.subheader("📂 Datos Generados")
    st.dataframe(data)

# 5. Filtrar por Cultivo
filtered_data = data  # Asegurar que filtered_data esté definido en todo el script
if menu == "Visualización":
    st.subheader("📊 Visualización de Datos")
    cultivo = st.sidebar.selectbox("Selecciona un cultivo", data["Cultivo"].unique())
    filtered_data = data[data["Cultivo"] == cultivo]
    st.write(f"Mostrando datos para el cultivo {cultivo}")
    st.dataframe(filtered_data)

    # 6. Filtrar por Producción
    prod_min, prod_max = st.sidebar.slider(
        "Selecciona el rango de producción (Ton):",
        min_value=int(data["Producción_Ton"].min()),
        max_value=int(data["Producción_Ton"].max()),
        value=(int(data["Producción_Ton"].min()), int(data["Producción_Ton"].max()))
    )
    filtered_data = filtered_data[(filtered_data["Producción_Ton"] >= prod_min) & (filtered_data["Producción_Ton"] <= prod_max)]

    # 7. Filtrar por Fecha
    fecha_inicio, fecha_fin = st.sidebar.date_input(
        "Selecciona el rango de fechas:",
        [data["Fecha"].min(), data["Fecha"].max()],
        min_value=data["Fecha"].min(),
        max_value=data["Fecha"].max()
    )
    filtered_data = filtered_data[(filtered_data["Fecha"] >= pd.to_datetime(fecha_inicio)) & (filtered_data["Fecha"] <= pd.to_datetime(fecha_fin))]

    # 8. Botón para Reiniciar Filtros
    if st.sidebar.button("Reiniciar Filtros"):
        filtered_data = data
        st.experimental_rerun()

    # 9. Implementar Pestañas
    st.subheader("📌 Navegación entre Pestañas")
    tab1, tab2, tab3 = st.tabs(["📊 Gráficos", "📂 Datos", "📈 Histograma"])
    with tab1:
        st.subheader("Visualización de Datos")

        # Selección de variables para la figura
        variables = ["Producción_Ton", "Área_Ha", "Costo_Producción", "Precio_Mercado", "Rendimiento", "Exportaciones_Ton"]
        x_var = st.selectbox('Selecciona la variable del eje X', variables)
        y_var = st.selectbox('Selecciona la variable del eje Y', variables)

        fig_plotly = px.scatter(
            filtered_data,
            x=x_var,
            y=y_var,
            color="Región",
            title=f"Relación entre {x_var} y {y_var} por Región",
        )
        st.plotly_chart(fig_plotly)
        
    with tab2:
        st.subheader("Datos Crudos")
        st.dataframe(filtered_data)

    with tab3:
        st.subheader("Histograma")
        hist_var = st.selectbox('Selecciona la variable para el histograma', variables)

        fig, ax = plt.subplots()
        ax.hist(filtered_data[hist_var], bins=20, edgecolor='black')
        ax.set_title(f"Distribución de {hist_var}")
        ax.set_xlabel(hist_var)
        ax.set_ylabel('Frecuencia')
        st.pyplot(fig)

# 10. Mensaje de Confirmación
st.sidebar.success("🎉 Configuración completa")

# 11. Ejecución del Script
if __name__ == "__main__":
    st.sidebar.info("Ejecuta este script con: streamlit run talento-roadmap-app.py")
