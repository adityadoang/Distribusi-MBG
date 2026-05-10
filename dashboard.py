import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurasi Halaman
st.set_page_config(page_title="Dashboard Prioritas MBG", layout="wide")

# Tema warna konsisten untuk ketiga kategori prioritas
COLOR_MAP = {
    "Prioritas Tinggi": "#E53935",
    "Prioritas Sedang": "#FDD835",
    "Prioritas Rendah": "#43A047"
}
PLOTLY_TEMPLATE = "plotly_dark"

# Fungsi untuk memuat data
@st.cache_data
def load_data():
    df = pd.read_csv("hasil_prioritas_mbg.csv")
    return df

df = load_data()

# --- Header ---
st.title("Dashboard Prioritas Distribusi MBG")
st.caption("Hasil analisis K-Means Clustering berdasarkan Stunting, Kemiskinan, dan ketersediaan SPPG pada 38 provinsi di Indonesia.")

# --- Sidebar Filter ---
st.sidebar.header("Filter Data")
prioritas_list = sorted(df['prioritas'].unique().tolist())
selected_prioritas = st.sidebar.multiselect(
    "Pilih Kategori Prioritas:", prioritas_list, default=prioritas_list
)

if selected_prioritas:
    filtered_df = df[df['prioritas'].isin(selected_prioritas)]
else:
    filtered_df = df

# --- Metrik Utama ---
st.markdown("### Ringkasan Data")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Provinsi", len(filtered_df))
col2.metric("Rata-rata Stunting", f"{round(filtered_df['stunting_pct'].mean(), 2)}%")
col3.metric("Rata-rata Kemiskinan", f"{round(filtered_df['kemiskinan_pct'].mean(), 2)}%")
col4.metric("Total Dapur SPPG", f"{int(filtered_df['jumlah_sppg'].sum()):,}")

st.divider()

# --- Baris 1: Dua chart berdampingan ---
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.markdown("#### 10 Provinsi Prioritas Tertinggi")
    tinggi_df = filtered_df[filtered_df['prioritas'] == 'Prioritas Tinggi'].copy()
    if len(tinggi_df) > 0:
        s_min, s_max = df['stunting_pct'].min(), df['stunting_pct'].max()
        k_min, k_max = df['kemiskinan_pct'].min(), df['kemiskinan_pct'].max()
        p_min, p_max = df['jumlah_sppg'].min(), df['jumlah_sppg'].max()
        tinggi_df['skor_prioritas'] = (
            (tinggi_df['stunting_pct'] - s_min) / (s_max - s_min) +
            (tinggi_df['kemiskinan_pct'] - k_min) / (k_max - k_min) +
            1 - (tinggi_df['jumlah_sppg'] - p_min) / (p_max - p_min)
        )
        top10_df = tinggi_df.sort_values(by='skor_prioritas', ascending=False).head(10)
    else:
        top10_df = tinggi_df

    fig_top10 = px.bar(
        top10_df,
        x='skor_prioritas' if 'skor_prioritas' in top10_df.columns else 'stunting_pct',
        y='provinsi',
        orientation='h',
        color='prioritas',
        labels={'skor_prioritas': 'Skor Prioritas', 'stunting_pct': 'Stunting (%)', 'provinsi': ''},
        color_discrete_map=COLOR_MAP,
        template=PLOTLY_TEMPLATE
    )
    fig_top10.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        showlegend=False,
        margin=dict(l=10, r=10, t=10, b=10),
        height=400
    )
    st.plotly_chart(fig_top10, use_container_width=True)

with col_chart2:
    st.markdown("#### Jumlah Provinsi per Kategori")
    count_df = filtered_df['prioritas'].value_counts().reset_index()
    count_df.columns = ['Prioritas', 'Jumlah']

    fig_bar = px.bar(
        count_df,
        x='Prioritas',
        y='Jumlah',
        color='Prioritas',
        text='Jumlah',
        color_discrete_map=COLOR_MAP,
        template=PLOTLY_TEMPLATE
    )
    fig_bar.update_traces(textposition='outside')
    fig_bar.update_layout(
        showlegend=False,
        margin=dict(l=10, r=10, t=10, b=10),
        height=400,
        xaxis_title='',
        yaxis_title=''
    )
    st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

# --- Baris 2: Scatter Plot ---
st.markdown("#### Scatter Plot: Stunting vs Kemiskinan")
fig_scatter = px.scatter(
    filtered_df,
    x='kemiskinan_pct',
    y='stunting_pct',
    color='prioritas',
    text='provinsi',
    hover_name='provinsi',
    hover_data={'jumlah_sppg': True, 'prioritas': False},
    labels={
        'kemiskinan_pct': 'Kemiskinan (%)',
        'stunting_pct': 'Stunting (%)',
        'jumlah_sppg': 'Jumlah SPPG'
    },
    color_discrete_map=COLOR_MAP,
    template=PLOTLY_TEMPLATE,
    height=850,
    width=1400
)
fig_scatter.update_traces(
    marker=dict(size=9, line=dict(width=1, color='rgba(255,255,255,0.3)')),
    textposition='top right',
    textfont=dict(size=7)
)
fig_scatter.update_layout(
    margin=dict(t=30, l=60, r=40, b=60),
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5, title_text='')
)
st.plotly_chart(fig_scatter, use_container_width=False)

st.divider()

# --- Tabel Detail ---
st.markdown("#### Detail Data Provinsi")
st.dataframe(
    filtered_df.sort_values(by='stunting_pct', ascending=False).reset_index(drop=True),
    use_container_width=True,
    height=400
)
