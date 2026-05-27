import streamlit as st
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

st.set_page_config(
    page_title=" Image Color Palette",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@700;900&family=Cinzel:wght@400;600&family=Share+Tech+Mono&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background-color: #0a0a14 !important;
    background-image:
        radial-gradient(ellipse at 20% 20%, rgba(100, 60, 180, 0.12) 0%, transparent 60%),
        radial-gradient(ellipse at 80% 80%, rgba(180, 120, 20, 0.10) 0%, transparent 60%),
        repeating-linear-gradient(
            45deg,
            transparent,
            transparent 60px,
            rgba(255,215,0,0.015) 60px,
            rgba(255,215,0,0.015) 61px
        );
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { background: rgba(10, 5, 30, 0.95) !important; }

.main .block-container {
    padding-top: 2rem;
    max-width: 780px;
}

.ygo-hero {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
}

.ygo-hero::before {
    content: "★ ★ ★";
    display: block;
    color: #c9a227;
    font-size: 1.1rem;
    letter-spacing: 12px;
    margin-bottom: 0.6rem;
    opacity: 0.7;
}

.ygo-title {
    font-family: 'Cinzel Decorative', serif;
    font-size: clamp(1.6rem, 4vw, 2.6rem);
    font-weight: 900;
    color: transparent;
    background: linear-gradient(135deg, #ffd700 0%, #fffacd 40%, #c9a227 70%, #ffd700 100%);
    -webkit-background-clip: text;
    background-clip: text;
    line-height: 1.2;
    filter: drop-shadow(0 0 18px rgba(255, 215, 0, 0.4));
    margin: 0;
}

.ygo-subtitle {
    font-family: 'Cinzel', serif;
    font-size: 0.85rem;
    color: #a090c0;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 0.5rem;
}

.ygo-divider {
    border: none;
    height: 2px;
    background: linear-gradient(to right, transparent, #7b4fc4, #c9a227, #7b4fc4, transparent);
    margin: 1.2rem auto 0;
    width: 70%;
    opacity: 0.8;
}

.ygo-card {
    background: linear-gradient(145deg, #12102a 0%, #1a1535 60%, #110f28 100%);
    border: 1px solid rgba(123, 79, 196, 0.45);
    border-radius: 6px;
    padding: 1.4rem 1.6rem;
    margin: 1.2rem 0;
    box-shadow:
        0 0 0 1px rgba(201,162,39,0.12),
        0 4px 30px rgba(0,0,0,0.5),
        inset 0 1px 0 rgba(255,215,0,0.06);
}

.ygo-section-title {
    font-family: 'Cinzel', serif;
    font-size: 0.78rem;
    font-weight: 600;
    color: #c9a227;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 8px;
}

.ygo-section-title::after {
    content: "";
    flex: 1;
    height: 1px;
    background: linear-gradient(to right, rgba(201,162,39,0.4), transparent);
}

[data-testid="stFileUploader"] {
    background: rgba(123, 79, 196, 0.08) !important;
    border: 2px dashed rgba(123, 79, 196, 0.5) !important;
    border-radius: 8px !important;
    transition: border-color 0.3s;
}

[data-testid="stFileUploader"]:hover {
    border-color: rgba(201, 162, 39, 0.7) !important;
}

.stButton > button {
    font-family: 'Cinzel', serif !important;
    background: linear-gradient(135deg, #3d1f8a, #6b3fc4) !important;
    border: 1px solid rgba(201,162,39,0.5) !important;
    color: #ffd700 !important;
    letter-spacing: 2px;
    border-radius: 4px !important;
    transition: all 0.25s;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #6b3fc4, #3d1f8a) !important;
    box-shadow: 0 0 18px rgba(201,162,39,0.35) !important;
    transform: translateY(-1px);
}

[data-testid="stSlider"] > div > div > div > div {
    background: linear-gradient(to right, #7b4fc4, #c9a227) !important;
}

[data-testid="stSlider"] span {
    color: #c9a227 !important;
    font-family: 'Share Tech Mono', monospace !important;
}

[data-testid="stAlert"] {
    background: rgba(10, 5, 30, 0.8) !important;
    border-left: 3px solid #7b4fc4 !important;
    border-radius: 4px !important;
    font-family: 'Cinzel', serif;
    font-size: 0.82rem;
}

[data-testid="stExpander"] {
    background: rgba(18, 15, 42, 0.9) !important;
    border: 1px solid rgba(123, 79, 196, 0.3) !important;
    border-radius: 6px !important;
}

[data-testid="stExpander"] summary {
    font-family: 'Cinzel', serif !important;
    color: #c9a227 !important;
    font-size: 0.83rem;
    letter-spacing: 2px;
}

p, label, .stMarkdown, [data-testid="stMarkdownContainer"] p {
    color: #c8bfe0 !important;
    font-family: 'Cinzel', serif;
    font-size: 0.85rem;
}

.stCaption {
    color: #7a6da0 !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.75rem !important;
}

hr { border-color: rgba(123,79,196,0.3) !important; }

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0a14; }
::-webkit-scrollbar-thumb { background: #3d1f8a; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #c9a227; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="ygo-hero">
    <h1 class="ygo-title">Image Color Palette</h1>
    <p class="ygo-subtitle">Ekstrak Warna Dominan dari Gambar</p>
    <hr class="ygo-divider">
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="ygo-card">
    <div class="ygo-section-title">Tentang Aplikasi</div>
    <p>
    Ekstrak <b style="color:#ffd700">warna dominan</b> dari gambar menggunakan algoritma
    <b style="color:#c9a227">K-Means Clustering</b> dengan <b style="color:#c9a227">Random Pixel Sampling</b>
    untuk hasil yang lebih akurat dan cerah.
    </p>
</div>
""", unsafe_allow_html=True)

@st.cache_data
def get_optimal_k(pixels, max_k=10):
    inertias = []
    for k in range(1, max_k + 1):
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(pixels)
        inertias.append(kmeans.inertia_)
    p1 = np.array([1, inertias[0]])
    p2 = np.array([max_k, inertias[-1]])
    distances = []
    for i in range(len(inertias)):
        p0 = np.array([i + 1, inertias[i]])
        distance = np.abs(np.cross(p2 - p1, p1 - p0)) / np.linalg.norm(p2 - p1)
        distances.append(distance)
    optimal_k = distances.index(max(distances)) + 1
    return optimal_k, inertias

st.markdown('<div class="ygo-section-title" style="font-family:\'Cinzel\',serif;color:#c9a227;letter-spacing:4px;font-size:0.78rem;margin-bottom:0.5rem">Upload Gambar</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Pilih file gambar (JPG / PNG)...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Gambar yang di-upload", use_container_width=True)

    img_array = np.array(image)
    if len(img_array.shape) == 3 and img_array.shape[2] == 4:
        img_array = img_array[:, :, :3]
    pixels = img_array.reshape(-1, 3)

    sample_size = 15000
    if len(pixels) > sample_size:
        rng = np.random.RandomState(42)
        indices = rng.choice(pixels.shape[0], sample_size, replace=False)
        pixels_for_kmeans = pixels[indices]
    else:
        pixels_for_kmeans = pixels

    st.info("menganalisis sampel piksel gambar")

    optimal_k, inertias = get_optimal_k(pixels_for_kmeans)

    st.success(f"Analisis selesai. Terdeteksi **{optimal_k} warna** dominan berdasarkan distribusi piksel.")

    st.markdown('<div class="ygo-section-title" style="font-family:\'Cinzel\',serif;color:#c9a227;letter-spacing:4px;font-size:0.78rem;margin:1.2rem 0 0.3rem">Jumlah Warna</div>', unsafe_allow_html=True)
    final_k = st.slider(
        "Jumlah warna yang ditampilkan:",
        min_value=2,
        max_value=10,
        value=optimal_k,
        help=f"Rekomendasi: {optimal_k} warna"
    )

    kmeans = KMeans(n_clusters=final_k, random_state=42, n_init=10)
    kmeans.fit(pixels_for_kmeans)
    colors = kmeans.cluster_centers_.astype(int)
    labels = kmeans.labels_
    counts = np.bincount(labels)
    sorted_indices = np.argsort(counts)[::-1]
    colors = colors[sorted_indices]
    total = counts.sum()
    counts_sorted = counts[sorted_indices]

    st.markdown("""
    <div class="ygo-section-title" style="font-family:'Cinzel',serif;color:#c9a227;letter-spacing:4px;font-size:0.78rem;margin:1.4rem 0 0.8rem">
        Hasil Palet Warna
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(final_k)
    for i, color in enumerate(colors):
        hex_color = '#%02x%02x%02x' % tuple(color)
        pct = counts_sorted[i] / total * 100
        if i == 0:
            rank_label = "Dominan"
        elif i == 1:
            rank_label = "Sekunder"
        elif i <= 3:
            rank_label = "Aksesori"
        else:
            rank_label = "Minor"

        with cols[i]:
            st.markdown(f"""
                <div style="
                    background: linear-gradient(180deg, {hex_color} 0%, {hex_color}cc 100%);
                    height: 90px;
                    border-radius: 6px;
                    margin-bottom: 6px;
                    box-shadow:
                        0 0 12px {hex_color}66,
                        0 2px 8px rgba(0,0,0,0.5),
                        inset 0 1px 0 rgba(255,255,255,0.15);
                    border: 1px solid rgba(201,162,39,0.3);
                    position: relative;
                    overflow: hidden;
                ">
                    <div style="
                        position: absolute; bottom: 4px; right: 5px;
                        font-family: 'Share Tech Mono', monospace;
                        font-size: 9px; color: rgba(255,255,255,0.5);
                    ">{pct:.1f}%</div>
                </div>
                <div style="text-align:center; font-family:'Share Tech Mono',monospace; font-size:11px; font-weight:bold; color:#ffd700; margin-bottom:2px;">
                    {hex_color.upper()}
                </div>
                <div style="text-align:center; font-family:'Cinzel',serif; font-size:9px; color:#7b5fd4; letter-spacing:1px;">
                    {rank_label}
                </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    with st.expander("📊 Lihat Grafik Analisis Elbow Method"):
        fig, ax = plt.subplots(figsize=(8, 3.5))
        fig.patch.set_facecolor('#0e0c24')
        ax.set_facecolor('#12102a')

        ax.plot(range(1, 11), inertias, marker='o', linestyle='-',
                color='#c9a227', linewidth=2, markersize=7,
                markerfacecolor='#ffd700', markeredgecolor='#0e0c24', markeredgewidth=1.5)
        ax.axvline(x=optimal_k, color='#7b4fc4', linestyle='--', linewidth=1.8,
                   label=f'Rekomendasi (k={optimal_k})')
        ax.axvline(x=final_k, color='#e94a4a', linestyle=':', linewidth=1.5,
                   label=f'Pilihan kamu (k={final_k})')

        ax.set_xlabel('Jumlah Cluster (k)', color='#a090c0', fontsize=10)
        ax.set_ylabel('Inersia', color='#a090c0', fontsize=10)
        ax.set_title('Elbow Method', color='#c9a227', fontsize=11, fontweight='bold', pad=12)

        ax.tick_params(colors='#7a6da0')
        for spine in ax.spines.values():
            spine.set_edgecolor('#2a2050')

        ax.grid(True, linestyle='--', alpha=0.25, color='#5040a0')
        ax.legend(facecolor='#0e0c24', edgecolor='#3d1f8a', labelcolor='#c8bfe0', fontsize=9)
        st.pyplot(fig)