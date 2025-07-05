import streamlit as st
import plotly.graph_objects as go
import numpy as np
from PIL import Image

# Duyguya göre beyin bölgeleri, koordinatları ve nörotransmitter/hormonlar
beyin_bolgeler = {
    'mutluluk': [
        ('Nucleus Accumbens', (0.3, 0.5), '#FF6B6B', 'Dopamin', 'Ödül ve motivasyon merkezi'),
        ('Prefrontal Cortex', (0.5, 0.6), '#FFD93D', 'Serotonin', 'Mutluluk ve huzur hormonu'),
        ('Ventral Tegmental', (0.4, 0.4), '#4ECDC4', 'Dopamin', 'Bağlanma ve güven hormonu')
    ],
    'stres': [
        ('Amygdala', (0.3, 0.5), '#FF4B4B', 'Kortizol', 'Stres hormonu'),
        ('Anterior Insula', (0.5, 0.6), '#6C5CE7', 'Noradrenalin', 'Savaş/kaç tepkisi hormonu'),
        ('Anterior Cingulate', (0.4, 0.4), '#A8E6CF', 'Kortizol', 'Uyarı durumu hormonu')
    ],
    'öfke': [
        ('Amygdala', (0.32, 0.52), '#FF1493', 'Adrenalin', 'Öfke ve saldırganlık'),
        ('Orbitofrontal Cortex', (0.55, 0.65), '#FF8C00', 'Adrenalin', 'Dürtü kontrolü'),
        ('Hypothalamus', (0.47, 0.47), '#A0522D', 'Testosteron', 'Fiziksel tepki')
    ],
    'korku': [
        ('Amygdala', (0.28, 0.48), '#8B0000', 'Adrenalin', 'Korku ve tehdit algısı'),
        ('Periaqueductal Gray', (0.35, 0.3), '#4682B4', 'Noradrenalin', 'Hayatta kalma tepkisi'),
        ('Hippocampus', (0.6, 0.4), '#808000', 'Kortizol', 'Hafıza ve stres')
    ],
    'heyecan': [
        ('Nucleus Accumbens', (0.4, 0.6), '#00CED1', 'Dopamin', 'Haz ve motivasyon'),
        ('Ventral Tegmental', (0.6, 0.4), '#32CD32', 'Dopamin', 'Haz ve motivasyon'),
        ('Locus Coeruleus', (0.5, 0.2), '#0000CD', 'Noradrenalin', 'Uyanıklık ve dikkat')
    ],
    'şaşkınlık': [
        ('Parietal Cortex', (0.7, 0.7), '#B22222', 'Noradrenalin', 'Beklenmedik durumlara tepki'),
        ('Prefrontal Cortex', (0.4, 0.7), '#FFB6C1', 'Dopamin', 'Yorumlama ve analiz')
    ],
    'üzüntü': [
        ('Subgenual Cingulate', (0.5, 0.3), '#9400D3', 'Serotonin', 'Duygu düzenleme'),
        ('Amygdala', (0.3, 0.4), '#4682B4', 'Kortizol', 'Negatif duygular'),
        ('Hippocampus', (0.6, 0.35), '#FFD700', 'Serotonin', 'Hafıza ve duygular')
    ],
    'huzur': [
        ('Prefrontal Cortex', (0.5, 0.8), '#00FA9A', 'Serotonin', 'Duygusal denge'),
        ('Posterior Cingulate', (0.6, 0.7), '#ADD8E6', 'Oksitosin', 'Sosyal bağlılık')
    ],
    'sevgi': [
        ('Ventral Tegmental', (0.45, 0.45), '#FF69B4', 'Oksitosin', 'Bağlanma ve sevgi'),
        ('Nucleus Accumbens', (0.55, 0.55), '#FF6347', 'Dopamin', 'Haz ve motivasyon'),
        ('Prefrontal Cortex', (0.5, 0.6), '#FFD700', 'Serotonin', 'Duygusal denge')
    ],
    'özlem': [
        ('Hippocampus', (0.6, 0.5), '#A9A9F5', 'Serotonin', 'Anılar ve duygusal bağ'),
        ('Prefrontal Cortex', (0.45, 0.7), '#F5A9A9', 'Dopamin', 'Beklenti ve planlama')
    ],
    'neşe': [
        ('Nucleus Accumbens', (0.35, 0.55), '#FFB347', 'Dopamin', 'Haz ve keyif'),
        ('Prefrontal Cortex', (0.55, 0.65), '#B6FFB3', 'Serotonin', 'Olumlu düşünce'),
    ],
    'motivasyon': [
        ('Nucleus Accumbens', (0.6, 0.5), '#00BFFF', 'Dopamin', 'Hedefe yönelik davranış'),
        ('Prefrontal Cortex', (0.4, 0.7), '#32CD32', 'Dopamin', 'Karar verme ve planlama')
    ]
}

@st.cache_resource
def get_sentiment_analyzer():
    from transformers import pipeline
    return pipeline("sentiment-analysis", model="savasy/bert-base-turkish-sentiment-cased")

sentiment_analyzer = get_sentiment_analyzer()

def duygu_tespit_et(metin):
    metin = metin.lower()
    if "özledim" in metin or "özlem" in metin:
        return "özlem"
    elif "üzgün" in metin or "ağlamak" in metin or "hüzün" in metin or "yasta" in metin:
        return "üzüntü"
    elif "kızgın" in metin or "sinirli" in metin or "öfke" in metin:
        return "öfke"
    elif "korku" in metin or "korktum" in metin or "korkuyorum" in metin:
        return "korku"
    elif "heyecan" in metin or "heyecanlı" in metin:
        return "heyecan"
    elif "şaşkın" in metin or "şaşırdım" in metin or "şaşkınlık" in metin:
        return "şaşkınlık"
    elif "huzur" in metin or "huzurlu" in metin:
        return "huzur"
    elif "sevgi" in metin or "sevgilim" in metin or "aşk" in metin:
        return "sevgi"
    elif "neşe" in metin or "neşeliyim" in metin or "neşelendim" in metin:
        return "neşe"
    elif "motivasyon" in metin or "motive" in metin:
        return "motivasyon"
    else:
        sonuc = sentiment_analyzer(metin)[0]
        return "mutluluk" if sonuc['label'] == 'positive' else "stres"

def interaktif_beyin_gorsellestirme(duygu, metin):
    gorsel_yolu = r'C:\Users\sudes\OneDrive\Masaüstü\Beyin\beyinson.png'
    fig = go.Figure()
    try:
        img = Image.open(gorsel_yolu)
        img_array = np.array(img)
        fig.add_trace(go.Image(z=img_array))
        h, w = img_array.shape[0], img_array.shape[1]
        bolgeler = beyin_bolgeler.get(duygu, [])
        for bolge, pos_rel, renk, hormon, aciklama in bolgeler:
            x_abs = int(pos_rel[0] * w)
            y_abs = int(pos_rel[1] * h)
            fig.add_trace(
                go.Scatter(
                    x=[x_abs], y=[y_abs],
                    mode="markers",
                    marker=dict(size=24, color=renk, opacity=0.85, line=dict(width=2, color="white")),
                    name=f"{bolge} ({hormon})",
                    hoverinfo="text",
                    hovertext=f"<b>{bolge}</b><br>{hormon}: {aciklama}",
                    hoverlabel=dict(bgcolor=renk)
                )
            )
    except Exception as e:
        st.error(f"Görsel yüklenemedi: {e}")

    fig.update_layout(
        title=f"{duygu.capitalize()} Durumunda Beyin Aktivitesi",
        showlegend=False,
        height=600,
        margin=dict(l=20, r=20, t=100, b=100)
    )
    fig.update_xaxes(showticklabels=False, showgrid=False, zeroline=False)
    fig.update_yaxes(showticklabels=False, showgrid=False, zeroline=False)
    return fig

st.title("Duyguya Göre Beyin Aktivitesi (Cümleyle Otomatik Analiz)")
metin = st.text_input("Bir cümle giriniz:")

if st.button("Analiz Et ve Görselleştir"):
    if metin.strip() == "":
        st.warning("Lütfen bir cümle giriniz.")
    else:
        duygu = duygu_tespit_et(metin)
        try:
            sonuc = sentiment_analyzer(metin)[0]
            st.write(f"Tespit edilen duygu: **{duygu}** (Model etiketi: {sonuc['label']}, Güven skoru: {sonuc['score']:.2f})")
        except Exception:
            st.write(f"Tespit edilen duygu: **{duygu}** (Model çalışmadı, anahtar kelime ile tespit)")
        fig = interaktif_beyin_gorsellestirme(duygu, metin)
        st.plotly_chart(fig, use_container_width=True)
