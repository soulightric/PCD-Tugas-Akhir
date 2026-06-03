"""
================================================
  APLIKASI PENGOLAHAN CITRA DIGITAL
  Mata Kuliah: Pengolahan Citra Digital
  Prodi Ilmu Komputer - Institut Teknologi BJH
================================================
"""

import streamlit as st
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import io

# ─────────────────────────────────────────────
#  KONFIGURASI HALAMAN
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Pengolahan Citra Digital",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Hide Streamlit default elements
# ==================== HIDE STREAMLIT BRANDING ====================
hide_streamlit_style = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden !important;}
        header {visibility: hidden;}
        .stAppHeader {display: none !important;}
        
        /* Hide fullscreen button and built with text */
        [data-testid="stToolbar"] {display: none !important;}
        [data-testid="stDecoration"] {display: none !important;}
        footer {display: none !important;}
        
        /* Extra safety */
        .css-1rs6os, .css-17ziqus, .st-emotion-cache-1g8v9l0 {display: none !important;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
# ============================================================

# ─────────────────────────────────────────────
#  CSS KUSTOM – TEMA ORANGE PUTIH MODERN
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── ROOT VARIABLES ── */
:root {
    --orange-deep:    #E8500A;
    --orange-mid:     #F97316;
    --orange-bright:  #FB923C;
    --orange-light:   #FED7AA;
    --orange-pale:    #FFF7ED;
    --white:          #FFFFFF;
    --gray-50:        #F9FAFB;
    --gray-100:       #F3F4F6;
    --gray-200:       #E5E7EB;
    --gray-400:       #9CA3AF;
    --gray-600:       #4B5563;
    --gray-800:       #1F2937;
    --shadow-sm:      0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.06);
    --shadow-md:      0 4px 16px rgba(232,80,10,0.12), 0 2px 6px rgba(0,0,0,0.06);
    --shadow-lg:      0 10px 40px rgba(232,80,10,0.15), 0 4px 12px rgba(0,0,0,0.08);
    --radius-sm:      8px;
    --radius-md:      12px;
    --radius-lg:      20px;
    --font:           'Outfit', sans-serif;
    --font-mono:      'JetBrains Mono', monospace;
    --transition:     all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

/* ── GLOBAL ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, .stApp {
    font-family: var(--font) !important;
    background: var(--gray-50) !important;
    color: var(--gray-800) !important;
}

/* Remove Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 1.5rem 2rem !important;
    max-width: 1400px !important;
}

/* ── SIDEBAR ── */
/* ───────────────────────────── SIDEBAR SECTION TITLE ───────────────────────────── */ .sidebar-section { padding: 16px 20px 8px; font-size: 0.72rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.14em; color: #E8500A; } /* ───────────────────────────── SIDEBAR RADIO NAVIGATION ───────────────────────────── */ section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] { gap: 8px !important; padding: 8px 0 !important; display: flex !important; flex-direction: column !important; } /* ITEM DEFAULT */ section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label { background: #FFFFFF !important; border-radius: 14px !important; padding: 14px 18px !important; transition: all 0.25s ease !important; border: 2px solid transparent !important; cursor: pointer !important; color: #E8500A !important; font-size: 0.95rem !important; font-weight: 700 !important; display: flex !important; align-items: center !important; gap: 10px !important; box-shadow: 0 2px 8px rgba(0,0,0,0.04), 0 1px 3px rgba(0,0,0,0.03); position: relative; overflow: hidden; } /* GARIS KIRI */ section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label::before { content: ""; position: absolute; left: 0; top: 0; width: 5px; height: 100%; background: linear-gradient( 180deg, #E8500A, #FB923C ); opacity: 0; transition: all 0.25s ease; } /* HOVER */ section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover { background: #FFF7ED !important; border: 2px solid #FDBA74 !important; color: #C2410C !important; transform: translateX(5px); box-shadow: 0 8px 22px rgba(249,115,22,0.20), 0 2px 6px rgba(0,0,0,0.05); } /* GARIS MUNCUL SAAT HOVER */ section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover::before { opacity: 1; } /* ACTIVE / SELECTED */ section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-checked="true"] { background: linear-gradient( 135deg, #E8500A 0%, #F97316 55%, #FB923C 100% ) !important; color: white !important; border: 2px solid #FED7AA !important; font-weight: 800 !important; transform: translateX(6px); box-shadow: 0 10px 28px rgba(232,80,10,0.35), 0 3px 8px rgba(0,0,0,0.08); } /* ACTIVE LEFT BAR */ section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-checked="true"]::before { opacity: 1; background: rgba(255,255,255,0.8); } /* HIDE RADIO BUTTON */ section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] input[type="radio"] { display: none !important; } /* ───────────────────────────── SIDEBAR CONTAINER ───────────────────────────── */ section[data-testid="stSidebar"] { background: linear-gradient( 180deg, #FFFFFF 0%, #FFF7ED 100% ) !important; border-right: 1px solid #FED7AA !important; box-shadow: 4px 0 25px rgba(232,80,10,0.06) !important; } /* ───────────────────────────── SIDEBAR BRAND ───────────────────────────── */ .sidebar-brand { background: linear-gradient( 135deg, #E8500A 0%, #F97316 60%, #FB923C 100% ); padding: 24px 22px 18px; margin-bottom: 8px; box-shadow: 0 8px 24px rgba(232,80,10,0.25); } .sidebar-brand-title { font-size: 1rem; font-weight: 800; color: white; letter-spacing: -0.02em; } .sidebar-brand-sub { font-size: 0.72rem; color: rgba(255,255,255,0.8); margin-top: 4px; } /* ───────────────────────────── ANIMASI HALUS ───────────────────────────── */ @keyframes glowPulse { 0% { box-shadow: 0 0 0 rgba(249,115,22,0.2); } 50% { box-shadow: 0 0 20px rgba(249,115,22,0.3); } 100% { box-shadow: 0 0 0 rgba(249,115,22,0.2); } } section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-checked="true"] { animation: glowPulse 2.2s infinite; }

/* ── FILE UPLOADER ── */
section[data-testid="stSidebar"] .stFileUploader {
    border: 2px dashed var(--orange-light) !important;
    border-radius: var(--radius-md) !important;
    background: var(--orange-pale) !important;
    padding: 8px !important;
}
section[data-testid="stSidebar"] .stFileUploader:hover {
    border-color: var(--orange-mid) !important;
}

/* ── BUTTONS ── */
.stButton > button {
    background: linear-gradient(135deg, var(--orange-deep) 0%, var(--orange-mid) 100%) !important;
    color: orange !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    font-family: var(--font) !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    padding: 10px 20px !important;
    transition: var(--transition) !important;
    box-shadow: 0 2px 8px rgba(232,80,10,0.3) !important;
    letter-spacing: 0.02em !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(232,80,10,0.4) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── SLIDERS ── */
.stSlider [data-baseweb="slider"] [data-testid="stThumbValue"],
.stSlider [data-baseweb="slider"] div[role="slider"] {
    background: var(--orange-mid) !important;
    border-color: var(--orange-deep) !important;
}

/* ── SELECT/RADIO ── */
.stSelectbox [data-baseweb="select"] {
    border-radius: var(--radius-sm) !important;
    border-color: var(--gray-200) !important;
    font-family: var(--font) !important;
}
.stSelectbox [data-baseweb="select"]:focus-within {
    border-color: var(--orange-mid) !important;
    box-shadow: 0 0 0 3px rgba(249,115,22,0.15) !important;
}

/* ── METRICS ── */
div[data-testid="metric-container"] {
    background: var(--white) !important;
    border: 1px solid var(--gray-200) !important;
    border-radius: var(--radius-md) !important;
    padding: 16px !important;
    box-shadow: var(--shadow-sm) !important;
    transition: var(--transition) !important;
    position: relative !important;
    overflow: hidden !important;
}
div[data-testid="metric-container"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: linear-gradient(180deg, var(--orange-deep), var(--orange-bright));
}
div[data-testid="metric-container"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: var(--shadow-md) !important;
}
div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-size: 1.5rem !important;
    font-weight: 700 !important;
    color: var(--orange-deep) !important;
    font-family: var(--font) !important;
}
div[data-testid="metric-container"] [data-testid="stMetricLabel"] {
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    color: var(--gray-400) !important;
    font-family: var(--font) !important;
}

/* ── IMAGES ── */
div[data-testid="stImage"] img {
    border-radius: var(--radius-md) !important;
    border: 1px solid var(--gray-200) !important;
    box-shadow: var(--shadow-sm) !important;
    transition: var(--transition) !important;
}
div[data-testid="stImage"] img:hover {
    box-shadow: var(--shadow-md) !important;
    transform: scale(1.005) !important;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px !important;
    background: var(--gray-100) !important;
    border-radius: var(--radius-sm) !important;
    padding: 4px !important;
    border: none !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 6px !important;
    font-family: var(--font) !important;
    font-weight: 500 !important;
    font-size: 0.875rem !important;
    color: var(--gray-600) !important;
    padding: 8px 16px !important;
    border: none !important;
    background: transparent !important;
    transition: var(--transition) !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: var(--orange-deep) !important;
    background: var(--white) !important;
}
.stTabs [aria-selected="true"] {
    background: var(--white) !important;
    color: var(--orange-deep) !important;
    font-weight: 600 !important;
    box-shadow: var(--shadow-sm) !important;
}
.stTabs [data-baseweb="tab-highlight"] {
    display: none !important;
}

/* ── CODE BLOCKS ── */
.stCodeBlock, pre, code {
    font-family: var(--font-mono) !important;
    border-radius: var(--radius-sm) !important;
    font-size: 0.8rem !important;
}
.stCode {
    border: 1px solid var(--gray-200) !important;
    border-radius: var(--radius-sm) !important;
}

/* ── EXPANDER ── */
.streamlit-expanderHeader {
    background: var(--white) !important;
    border: 1px solid var(--gray-200) !important;
    border-radius: var(--radius-sm) !important;
    font-family: var(--font) !important;
    font-weight: 600 !important;
    color: var(--gray-800) !important;
    transition: var(--transition) !important;
}
.streamlit-expanderHeader:hover {
    background: var(--orange-pale) !important;
    color: var(--orange-deep) !important;
    border-color: var(--orange-light) !important;
}

/* ── ALERTS / WARNINGS ── */
.stAlert {
    border-radius: var(--radius-sm) !important;
    font-family: var(--font) !important;
    font-size: 0.875rem !important;
}

/* ── DATAFRAME ── */
.stDataFrame {
    border-radius: var(--radius-sm) !important;
    overflow: hidden !important;
    border: 1px solid var(--gray-200) !important;
}

/* ── CUSTOM COMPONENTS ── */

/* Main Header */
.app-header {
    background: linear-gradient(135deg, var(--orange-deep) 0%, var(--orange-mid) 60%, var(--orange-bright) 100%);
    border-radius: var(--radius-lg);
    padding: 28px 36px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
    box-shadow: var(--shadow-lg);
}
.app-header::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    background: rgba(255,255,255,0.08);
    border-radius: 50%;
}
.app-header::after {
    content: '';
    position: absolute;
    bottom: -40px; right: 80px;
    width: 140px; height: 140px;
    background: rgba(255,255,255,0.05);
    border-radius: 50%;
}
.app-header-eyebrow {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.7);
    margin-bottom: 6px;
}
.app-header h1 {
    font-size: 1.75rem;
    font-weight: 800;
    color: white;
    margin: 0 0 6px 0;
    line-height: 1.2;
    letter-spacing: -0.02em;
}
.app-header p {
    font-size: 0.875rem;
    color: rgba(255,255,255,0.8);
    margin: 0;
    font-weight: 400;
}
.header-dot {
    display: inline-block;
    width: 6px; height: 6px;
    background: rgba(255,255,255,0.5);
    border-radius: 50%;
    margin: 0 8px;
    vertical-align: middle;
}

/* Sidebar brand bar */
.sidebar-brand {
    background: linear-gradient(135deg, var(--orange-deep), var(--orange-mid));
    padding: 20px 20px 16px;
    margin-bottom: 4px;
}
.sidebar-brand-title {
    font-size: 0.95rem;
    font-weight: 700;
    color: white;
    letter-spacing: -0.01em;
    line-height: 1.3;
}
.sidebar-brand-sub {
    font-size: 0.7rem;
    color: rgba(255,255,255,0.7);
    margin-top: 2px;
    font-weight: 400;
}

/* Sidebar section labels */
.sidebar-section {
    padding: 16px 20px 6px;
    font-size: 0.65rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--gray-400);
}

/* Sidebar nav wrapper */
.sidebar-nav {
    padding: 4px 12px;
}

/* Info box */
.info-box {
    background: var(--orange-pale);
    border: 1px solid var(--orange-light);
    border-left: 4px solid var(--orange-mid);
    border-radius: var(--radius-sm);
    padding: 14px 18px;
    margin: 12px 0;
    font-size: 0.875rem;
    color: var(--gray-800);
    line-height: 1.6;
}

/* Feature badge */
.feature-badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-left: 10px;
    vertical-align: middle;
}
.badge-wajib {
    background: var(--orange-deep);
    color: white;
}
.badge-opsional {
    background: linear-gradient(135deg, var(--orange-mid), var(--orange-bright));
    color: white;
}

/* Result header */
.result-header {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 16px;
    background: var(--white);
    border: 1px solid var(--gray-200);
    border-left: 3px solid var(--orange-mid);
    border-radius: var(--radius-sm);
    margin-bottom: 10px;
    font-weight: 600;
    font-size: 0.875rem;
    color: var(--gray-800);
}

/* Section divider */
.section-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--gray-200), transparent);
    margin: 24px 0;
}

/* Card grid */
.card {
    background: var(--white);
    border: 1px solid var(--gray-200);
    border-radius: var(--radius-md);
    padding: 20px;
    box-shadow: var(--shadow-sm);
    transition: var(--transition);
}
.card:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-2px);
    border-color: var(--orange-light);
}

/* Footer */
.app-footer {
    text-align: center;
    padding: 20px;
    font-size: 0.75rem;
    color: var(--gray-400);
    border-top: 1px solid var(--gray-200);
    margin-top: 40px;
    font-weight: 500;
    letter-spacing: 0.02em;
}
.app-footer span {
    color: var(--orange-mid);
    font-weight: 700;
}

/* Pulse animation for upload prompt */
@keyframes pulse-ring {
    0%   { box-shadow: 0 0 0 0 rgba(249,115,22,0.4); }
    70%  { box-shadow: 0 0 0 10px rgba(249,115,22,0); }
    100% { box-shadow: 0 0 0 0 rgba(249,115,22,0); }
}
.pulse { animation: pulse-ring 2s infinite; }

/* Fade-in on load */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}
.fade-in { animation: fadeInUp 0.4s ease both; }
.fade-in-1 { animation-delay: 0.05s; }
.fade-in-2 { animation-delay: 0.10s; }
.fade-in-3 { animation-delay: 0.15s; }
.fade-in-4 { animation-delay: 0.20s; }

/* Slide bar shimmer */
@keyframes shimmer {
    0%   { background-position: -400px 0; }
    100% { background-position: 400px 0; }
}
.shimmer-bar {
    background: linear-gradient(90deg, var(--gray-100) 25%, var(--gray-200) 50%, var(--gray-100) 75%);
    background-size: 800px 100%;
    animation: shimmer 1.5s infinite linear;
    border-radius: 4px;
    height: 6px;
    margin: 8px 0;
}

/* Page title style */
.page-title {
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--gray-800);
    letter-spacing: -0.02em;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.page-title-dot {
    width: 8px; height: 8px;
    background: var(--orange-mid);
    border-radius: 50%;
    flex-shrink: 0;
}
</style>
""", unsafe_allow_html=True)

# ── JavaScript Animasi Interaktif ──
st.markdown("""
<script>
(function() {
    function init() {
        // ── 1. Intersection Observer: fade-in sections on scroll ──
        if ('IntersectionObserver' in window) {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(el => {
                    if (el.isIntersecting) {
                        el.target.style.opacity    = '1';
                        el.target.style.transform  = 'translateY(0)';
                        el.target.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
                        observer.unobserve(el.target);
                    }
                });
            }, { threshold: 0.08 });

            document.querySelectorAll(
                'div[data-testid="metric-container"], div[data-testid="stImage"], .card'
            ).forEach(el => {
                el.style.opacity   = '0';
                el.style.transform = 'translateY(20px)';
                observer.observe(el);
            });
        }

        // ── 2. Sidebar nav active indicator smooth animation ──
        const radioLabels = document.querySelectorAll(
            'section[data-testid="stSidebar"] .stRadio label'
        );
        radioLabels.forEach(lbl => {
            lbl.addEventListener('click', function() {
                radioLabels.forEach(l => l.style.fontWeight = '500');
                this.style.fontWeight = '700';
            });
        });

        // ── 3. Metric counter animation ──
        document.querySelectorAll('[data-testid="stMetricValue"]').forEach(el => {
            const text = el.textContent.trim();
            const num  = parseFloat(text.replace(/[^0-9.-]/g, ''));
            if (!isNaN(num) && num > 0 && num < 100000) {
                let start = 0, duration = 800;
                const step = (timestamp) => {
                    if (!start) start = timestamp;
                    const progress = Math.min((timestamp - start) / duration, 1);
                    const eased = 1 - Math.pow(1 - progress, 3);
                    el.textContent = text.replace(/[0-9.]+/, Math.floor(eased * num).toLocaleString());
                    if (progress < 1) requestAnimationFrame(step);
                };
                requestAnimationFrame(step);
            }
        });

        // ── 4. Button ripple effect ──
        document.querySelectorAll('.stButton > button').forEach(btn => {
            btn.addEventListener('click', function(e) {
                const ripple = document.createElement('span');
                const rect   = this.getBoundingClientRect();
                const size   = Math.max(rect.width, rect.height);
                ripple.style.cssText = `
                    position:absolute;width:${size}px;height:${size}px;
                    border-radius:50%;background:rgba(255,255,255,0.35);
                    transform:scale(0);animation:ripple-anim 0.55s ease-out;
                    left:${e.clientX - rect.left - size/2}px;
                    top:${e.clientY - rect.top  - size/2}px;
                    pointer-events:none;
                `;
                if (!document.querySelector('#ripple-style')) {
                    const s = document.createElement('style');
                    s.id = 'ripple-style';
                    s.textContent = '@keyframes ripple-anim{to{transform:scale(2.5);opacity:0}}';
                    document.head.appendChild(s);
                }
                this.style.position = 'relative';
                this.style.overflow = 'hidden';
                this.appendChild(ripple);
                setTimeout(() => ripple.remove(), 600);
            });
        });

        // ── 5. Image hover zoom cursor ──
        document.querySelectorAll('div[data-testid="stImage"] img').forEach(img => {
            img.style.cursor = 'zoom-in';
        });

        // ── 6. Slider value highlight on change ──
        document.querySelectorAll('input[type="range"]').forEach(slider => {
            slider.addEventListener('input', function() {
                const thumb = this.parentElement.querySelector('[role="slider"]');
                if (thumb) {
                    thumb.style.transform = 'scale(1.3)';
                    setTimeout(() => { thumb.style.transform = 'scale(1)'; }, 200);
                }
            });
        });
    }

    // Run after Streamlit renders
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        setTimeout(init, 500);
    }
    // Re-run on Streamlit re-renders
    const _mut = new MutationObserver(() => setTimeout(init, 300));
    _mut.observe(document.body, { childList: true, subtree: true });
})();
</script>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  HELPER FUNCTIONS
# ─────────────────────────────────────────────
def pil_to_cv(pil_img):
    img = np.array(pil_img.convert("RGB"))
    return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

def cv_to_rgb(cv_img):
    if len(cv_img.shape) == 2:
        return cv_img
    return cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)

def display_pair(col1, col2, img1, label1, img2, label2, use_gray=False):
    with col1:
        st.markdown(f"**{label1}**")
        st.image(img1, use_container_width=True, clamp=True)
    with col2:
        st.markdown(f"**{label2}**")
        st.image(img2, use_container_width=True, clamp=True)

def fig_to_buf(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=120, bbox_inches="tight")
    buf.seek(0)
    return buf

def safe_resize(img, target_shape):
    h, w = target_shape[:2]
    return cv2.resize(img, (w, h))

# ─────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="app-header fade-in">
    <div class="app-header-eyebrow">Institut Teknologi Bacharuddin Jusuf Habibie</div>
    <h1>Pengolahan Citra Digital</h1>
    <p>Prodi Ilmu Komputer<span class="header-dot"></span>Semester Genap 2023/2024</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-brand-title">Citra Digital</div>
        <div class="sidebar-brand-sub">v1.0 · Python + OpenCV</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">Upload Gambar</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Gambar Utama", type=["jpg", "jpeg", "png", "bmp", "tiff"],
        help="Digunakan untuk semua operasi."
    )
    uploaded_file2 = st.file_uploader(
        "Gambar Kedua (Opsional)",
        type=["jpg", "jpeg", "png", "bmp", "tiff"],
        help="Untuk Operasi Aritmatika & Logika"
    )

    st.markdown('<div class="sidebar-section">Navigasi</div>', unsafe_allow_html=True)

    menu = st.radio(
        "Pilih Fitur",
        [
            "Beranda",
            "Tampilkan Gambar",
            "Grayscale",
            "Citra Biner",
            "Operasi Aritmatika",
            "Operasi Logika",
            "Histogram",
            "Image Filtering",
            "Morfologi",
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown(
        "<div style='padding:0 8px 12px;font-size:0.72rem;color:#9CA3AF;line-height:1.6;'>"
        "Dibuat dengan Python, Streamlit, dan OpenCV"
        "</div>",
        unsafe_allow_html=True
    )

# ─────────────────────────────────────────────
#  LOAD GAMBAR
# ─────────────────────────────────────────────
img_cv   = None
img_rgb  = None
img_gray = None
img_cv2  = None
img_rgb2 = None

if uploaded_file:
    pil1     = Image.open(uploaded_file)
    img_cv   = pil_to_cv(pil1)
    img_rgb  = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    img_gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

if uploaded_file2:
    pil2    = Image.open(uploaded_file2)
    img_cv2 = pil_to_cv(pil2)
    img_rgb2 = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2RGB)

# ─────────────────────────────────────────────
#  HALAMAN: BERANDA
# ─────────────────────────────────────────────
if menu == "Beranda":
    st.markdown("""
    <div class="page-title fade-in">
        <div class="page-title-dot"></div>
        Selamat Datang
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box fade-in fade-in-1">
    Aplikasi ini dibangun menggunakan <b>Python</b>, <b>Streamlit</b>, dan <b>OpenCV</b> sebagai proyek akhir
    mata kuliah <b>Pengolahan Citra Digital</b>. Upload gambar di sidebar kiri untuk memulai.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="card fade-in fade-in-2">
            <div style="font-size:0.65rem;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:#E8500A;margin-bottom:12px;">Fitur Wajib · 40 Poin</div>
        """, unsafe_allow_html=True)
        st.markdown("""
        | No | Fitur | Status |
        |----|-------|--------|
        | 1 | Input & Tampilkan Gambar | ✅ |
        | 2 | Konversi Grayscale | ✅ |
        | 3 | Konversi Citra Biner | ✅ |
        | 4 | Operasi Aritmatika (Add/Sub/Mul) | ✅ |
        | 5 | Operasi Logika (AND/OR/XOR/NOT) | ✅ |
        """)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card fade-in fade-in-3">
            <div style="font-size:0.65rem;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;color:#F97316;margin-bottom:12px;">Fitur Opsional · Bonus</div>
        """, unsafe_allow_html=True)
        st.markdown("""
        | No | Fitur | Poin |
        |----|-------|------|
        | 1 | Histogram Citra | **+10** |
        | 2 | Image Filtering (Blur/Sharpen/Edge) | **+20** |
        | 3 | Morfologi (Dilasi & Erosi, 2+ SE) | **+30** |
        """)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    st.markdown("**Teknologi yang Digunakan**")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""<div class="card fade-in fade-in-1" style="text-align:center;">
            <div style="font-size:1.5rem;margin-bottom:8px;">🐍</div>
            <div style="font-weight:700;color:#1F2937;">Python 3.x</div>
            <div style="font-size:0.8rem;color:#9CA3AF;margin-top:4px;">Bahasa pemrograman utama</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="card fade-in fade-in-2" style="text-align:center;">
            <div style="font-size:1.5rem;margin-bottom:8px;">⚡</div>
            <div style="font-weight:700;color:#1F2937;">Streamlit</div>
            <div style="font-size:0.8rem;color:#9CA3AF;margin-top:4px;">Framework antarmuka web</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class="card fade-in fade-in-3" style="text-align:center;">
            <div style="font-size:1.5rem;margin-bottom:8px;">👁</div>
            <div style="font-weight:700;color:#1F2937;">OpenCV + NumPy</div>
            <div style="font-size:0.8rem;color:#9CA3AF;margin-top:4px;">Library pengolahan citra</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("**Cara Penggunaan**")
    st.markdown("""
    1. **Upload gambar** melalui panel kiri (sidebar).
    2. **Pilih menu** fitur yang ingin digunakan.
    3. **Atur parameter** sesuai kebutuhan.
    4. **Analisis hasil** yang ditampilkan.
    """)

# ─────────────────────────────────────────────
#  HALAMAN: TAMPILKAN GAMBAR
# ─────────────────────────────────────────────
elif menu == "Tampilkan Gambar":
    st.markdown("""<div class="page-title">
        <div class="page-title-dot"></div>Tampilkan Gambar
        <span class="feature-badge badge-wajib">Wajib</span>
    </div>""", unsafe_allow_html=True)

    if img_rgb is None:
        st.warning("Silakan upload gambar terlebih dahulu di sidebar kiri.")
    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Gambar Asli (RGB)**")
            st.image(img_rgb, use_container_width=True)
        with col2:
            st.markdown("**Tampilan Grayscale**")
            st.image(img_gray, use_container_width=True, clamp=True)
        with col3:
            st.markdown("**Channel Decomposition**")
            r = img_rgb[:,:,0]
            g = img_rgb[:,:,1]
            b = img_rgb[:,:,2]
            fig, axes = plt.subplots(1, 3, figsize=(6, 2))
            for ax, ch, color in zip(axes, [r, g, b], ["Reds", "Greens", "Blues"]):
                ax.imshow(ch, cmap=color); ax.axis("off")
            fig.tight_layout(pad=0.5)
            st.pyplot(fig); plt.close(fig)

        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        h, w = img_rgb.shape[:2]
        ch = img_rgb.shape[2] if len(img_rgb.shape) == 3 else 1
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Lebar", f"{w} px")
        c2.metric("Tinggi", f"{h} px")
        c3.metric("Channel", ch)
        c4.metric("Total Piksel", f"{w*h:,}")

        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.markdown("**Sample Nilai Array (50 piksel pertama baris pertama):**")
        st.code(str(img_rgb[0, :50]), language="python")

        if img_rgb2 is not None:
            st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
            st.markdown("**Gambar Kedua**")
            h2, w2 = img_rgb2.shape[:2]
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Gambar Kedua (RGB)**")
                st.image(img_rgb2, use_container_width=True)
            with col2:
                st.metric("Dimensi", f"{w2} × {h2} px")

# ─────────────────────────────────────────────
#  HALAMAN: GRAYSCALE
# ─────────────────────────────────────────────
elif menu == "Grayscale":
    st.markdown("""<div class="page-title">
        <div class="page-title-dot"></div>Konversi Grayscale
        <span class="feature-badge badge-wajib">Wajib</span>
    </div>""", unsafe_allow_html=True)

    if img_rgb is None:
        st.warning("Silakan upload gambar terlebih dahulu.")
    else:
        st.markdown("""
        <div class="info-box">
        <b>Grayscale</b> adalah representasi citra yang hanya memiliki satu channel intensitas (0–255).
        Rumus konversi: <code>Y = 0.299·R + 0.587·G + 0.114·B</code>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Gambar Asli (RGB)**")
            st.image(img_rgb, use_container_width=True)
        with col2:
            st.markdown("**Gambar Grayscale**")
            st.image(img_gray, use_container_width=True, clamp=True)

        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.markdown("**Statistik Grayscale**")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Nilai Min", int(img_gray.min()))
        c2.metric("Nilai Max", int(img_gray.max()))
        c3.metric("Rata-rata", f"{img_gray.mean():.2f}")
        c4.metric("Std Deviasi", f"{img_gray.std():.2f}")

        st.markdown("**Kode Python:**")
        st.code("""import cv2
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)""", language="python")

# ─────────────────────────────────────────────
#  HALAMAN: CITRA BINER
# ─────────────────────────────────────────────
elif menu == "Citra Biner":
    st.markdown("""<div class="page-title">
        <div class="page-title-dot"></div>Konversi Citra Biner
        <span class="feature-badge badge-wajib">Wajib</span>
    </div>""", unsafe_allow_html=True)

    if img_rgb is None:
        st.warning("Silakan upload gambar terlebih dahulu.")
    else:
        st.markdown("""
        <div class="info-box">
        <b>Citra Biner</b> hanya memiliki dua nilai intensitas: <b>0 (hitam)</b> dan <b>255 (putih)</b>.
        Proses konversi dilakukan dengan <b>thresholding</b>: piksel ≥ threshold → putih (255), piksel &lt; threshold → hitam (0).
        </div>
        """, unsafe_allow_html=True)

        method = st.radio("Metode Thresholding:", ["Manual (Global)", "Otsu"], horizontal=True)

        if method == "Manual (Global)":
            thresh_val = st.slider("Nilai Threshold (Ambang Batas):", 0, 255, 127, 1)
            _, biner = cv2.threshold(img_gray, thresh_val, 255, cv2.THRESH_BINARY)
            label = f"Citra Biner (threshold={thresh_val})"
        else:
            ret, biner = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            label = f"Citra Biner – Otsu (threshold={ret:.1f})"

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Gambar Asli**"); st.image(img_rgb, use_container_width=True)
        with col2:
            st.markdown("**Grayscale**"); st.image(img_gray, use_container_width=True, clamp=True)
        with col3:
            st.markdown(f"**{label}**"); st.image(biner, use_container_width=True, clamp=True)

        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        jumlah_putih = int(np.sum(biner == 255))
        jumlah_hitam = int(np.sum(biner == 0))
        total = biner.size
        c1, c2, c3 = st.columns(3)
        c1.metric("Piksel Putih (255)", f"{jumlah_putih:,}")
        c2.metric("Piksel Hitam (0)", f"{jumlah_hitam:,}")
        c3.metric("Persentase Putih", f"{jumlah_putih/total*100:.1f}%")

        if method == "Manual (Global)":
            st.code(f"""gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, biner = cv2.threshold(gray, {thresh_val}, 255, cv2.THRESH_BINARY)""", language="python")
        else:
            st.code("""gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, biner = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)""", language="python")

# ─────────────────────────────────────────────
#  HALAMAN: OPERASI ARITMATIKA
# ─────────────────────────────────────────────
elif menu == "Operasi Aritmatika":
    st.markdown("""<div class="page-title">
        <div class="page-title-dot"></div>Operasi Aritmatika
        <span class="feature-badge badge-wajib">Wajib</span>
    </div>""", unsafe_allow_html=True)

    if img_rgb is None:
        st.warning("Silakan upload gambar terlebih dahulu.")
    else:
        st.markdown("""
        <div class="info-box">
        <b>Operasi Aritmatika</b> dilakukan pada level piksel. Tersedia:
        Penambahan, Pengurangan, Perkalian, Penyesuaian Kecerahan, dan Penyesuaian Kontras.
        </div>
        """, unsafe_allow_html=True)

        op = st.selectbox("Pilih Operasi:", [
            "Penyesuaian Kecerahan (+Konstanta)",
            "Penyesuaian Kontras (×Konstanta)",
            "Citra Negatif",
            "Penambahan 2 Gambar (cv2.add)",
            "Pengurangan 2 Gambar (cv2.subtract)",
            "Penambahan Berbobot (cv2.addWeighted)",
        ])

        result = None
        code_snippet = ""

        if op == "Penyesuaian Kecerahan (+Konstanta)":
            val = st.slider("Nilai Kecerahan (beta):", -255, 255, 80)
            result = cv2.convertScaleAbs(img_cv, alpha=1.0, beta=val)
            code_snippet = f"result = cv2.convertScaleAbs(img, alpha=1.0, beta={val})"

        elif op == "Penyesuaian Kontras (×Konstanta)":
            alpha = st.slider("Nilai Kontras (alpha):", 0.1, 5.0, 1.5, 0.1)
            result = cv2.convertScaleAbs(img_cv, alpha=alpha, beta=0)
            code_snippet = f"result = cv2.convertScaleAbs(img, alpha={alpha}, beta=0)"

        elif op == "Citra Negatif":
            result = cv2.bitwise_not(img_cv)
            code_snippet = "result = cv2.bitwise_not(img)"

        elif op in ["Penambahan 2 Gambar (cv2.add)", "Pengurangan 2 Gambar (cv2.subtract)", "Penambahan Berbobot (cv2.addWeighted)"]:
            if img_cv2 is None:
                st.warning("Upload Gambar Kedua di sidebar untuk operasi ini.")
            else:
                img_b = safe_resize(img_cv2, img_cv.shape)
                if op == "Penambahan 2 Gambar (cv2.add)":
                    result = cv2.add(img_cv, img_b)
                    code_snippet = "result = cv2.add(img1, img2)"
                elif op == "Pengurangan 2 Gambar (cv2.subtract)":
                    result = cv2.subtract(img_cv, img_b)
                    code_snippet = "result = cv2.subtract(img1, img2)"
                else:
                    w1 = st.slider("Bobot Gambar 1 (α):", 0.0, 1.0, 0.5, 0.05)
                    w2 = round(1.0 - w1, 2)
                    result = cv2.addWeighted(img_cv, w1, img_b, w2, 0)
                    code_snippet = f"result = cv2.addWeighted(img1, {w1}, img2, {w2}, 0)"

        if result is not None:
            col1, col2 = st.columns(2)
            result_rgb = cv_to_rgb(result)
            with col1:
                st.markdown("**Gambar Asli**"); st.image(img_rgb, use_container_width=True)
            with col2:
                st.markdown(f"**Hasil: {op}**")
                if len(result_rgb.shape) == 2:
                    st.image(result_rgb, use_container_width=True, clamp=True)
                else:
                    st.image(result_rgb, use_container_width=True)
            if code_snippet:
                st.code(code_snippet, language="python")

# ─────────────────────────────────────────────
#  HALAMAN: OPERASI LOGIKA
# ─────────────────────────────────────────────
elif menu == "Operasi Logika":
    st.markdown("""<div class="page-title">
        <div class="page-title-dot"></div>Operasi Logika
        <span class="feature-badge badge-wajib">Wajib</span>
    </div>""", unsafe_allow_html=True)

    if img_rgb is None:
        st.warning("Silakan upload gambar terlebih dahulu.")
    else:
        st.markdown("""
        <div class="info-box">
        <b>Operasi Logika</b> diterapkan pada setiap bit nilai piksel.
        <b>AND</b> menjaga piksel yang sama, <b>OR</b> menggabungkan, <b>XOR</b> menampilkan perbedaan,
        <b>NOT</b> membalik seluruh nilai piksel.
        </div>
        """, unsafe_allow_html=True)

        op_logika = st.selectbox("Pilih Operasi Logika:", ["NOT (1 Gambar)", "AND", "OR", "XOR"])
        result = None
        code_snippet = ""

        if op_logika == "NOT (1 Gambar)":
            result = cv2.bitwise_not(img_cv)
            code_snippet = "result = cv2.bitwise_not(img)"
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Gambar Asli**"); st.image(img_rgb, use_container_width=True)
            with col2:
                st.markdown("**Hasil NOT**"); st.image(cv_to_rgb(result), use_container_width=True)
        else:
            if img_cv2 is None:
                st.warning("Upload Gambar Kedua di sidebar untuk operasi AND / OR / XOR.")
            else:
                img_b = safe_resize(img_cv2, img_cv.shape)
                if op_logika == "AND":
                    result = cv2.bitwise_and(img_cv, img_b)
                    code_snippet = "result = cv2.bitwise_and(img1, img2)"
                elif op_logika == "OR":
                    result = cv2.bitwise_or(img_cv, img_b)
                    code_snippet = "result = cv2.bitwise_or(img1, img2)"
                elif op_logika == "XOR":
                    result = cv2.bitwise_xor(img_cv, img_b)
                    code_snippet = "result = cv2.bitwise_xor(img1, img2)"

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown("**Gambar 1**"); st.image(img_rgb, use_container_width=True)
                with col2:
                    st.markdown("**Gambar 2**"); st.image(img_rgb2, use_container_width=True)
                with col3:
                    st.markdown(f"**Hasil {op_logika}**")
                    st.image(cv_to_rgb(result), use_container_width=True)

        if code_snippet:
            st.code(code_snippet, language="python")

        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.markdown("**Penjelasan Operasi Logika:**")
        tabel = {
            "Operasi": ["AND", "OR", "XOR", "NOT"],
            "Deskripsi": [
                "Piksel hasil = min(piksel1, piksel2); menjaga area yang tumpang tindih",
                "Piksel hasil = max(piksel1, piksel2); menggabungkan area kedua gambar",
                "Piksel hasil = perbedaan antara kedua gambar",
                "Piksel hasil = 255 - piksel; membalik intensitas"
            ]
        }
        import pandas as pd
        st.dataframe(pd.DataFrame(tabel), use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────
#  HALAMAN: HISTOGRAM  [OPSIONAL +10]
# ─────────────────────────────────────────────
elif menu == "Histogram":
    st.markdown("""<div class="page-title">
        <div class="page-title-dot"></div>Histogram Citra
        <span class="feature-badge badge-opsional">Opsional +10</span>
    </div>""", unsafe_allow_html=True)

    if img_rgb is None:
        st.warning("Silakan upload gambar terlebih dahulu.")
    else:
        st.markdown("""
        <div class="info-box">
        <b>Histogram</b> menunjukkan distribusi intensitas piksel dalam citra.
        Sumbu X = nilai intensitas (0–255), Sumbu Y = jumlah piksel.
        </div>
        """, unsafe_allow_html=True)

        tabs = st.tabs(["Grayscale", "Warna RGB", "Normalisasi", "Ekualisasi"])

        with tabs[0]:
            fig, axes = plt.subplots(1, 2, figsize=(12, 4))
            fig.patch.set_facecolor('#FAFAFA')
            axes[0].imshow(img_gray, cmap="gray"); axes[0].set_title("Citra Grayscale", fontsize=11, fontweight='bold'); axes[0].axis("off")
            hist = cv2.calcHist([img_gray], [0], None, [256], [0, 256])
            axes[1].plot(hist, color="#E8500A", linewidth=1.5)
            axes[1].fill_between(range(256), hist.flatten(), alpha=0.15, color="#E8500A")
            axes[1].set_title("Histogram Grayscale", fontsize=11, fontweight='bold')
            axes[1].set_xlabel("Nilai Piksel"); axes[1].set_ylabel("Jumlah Piksel")
            axes[1].set_xlim([0, 256]); axes[1].grid(alpha=0.2)
            fig.tight_layout(); st.pyplot(fig); plt.close(fig)

        with tabs[1]:
            fig, axes = plt.subplots(1, 2, figsize=(12, 4))
            fig.patch.set_facecolor('#FAFAFA')
            axes[0].imshow(img_rgb); axes[0].set_title("Citra RGB", fontsize=11, fontweight='bold'); axes[0].axis("off")
            channels = cv2.split(img_cv)
            for ch, color, lbl in zip(channels, ("blue","green","red"), ("Blue","Green","Red")):
                hist = cv2.calcHist([ch], [0], None, [256], [0, 256])
                axes[1].plot(hist, color=color, label=lbl, linewidth=1.5, alpha=0.8)
            axes[1].set_title("Histogram Warna (RGB)", fontsize=11, fontweight='bold')
            axes[1].set_xlabel("Nilai Piksel"); axes[1].set_ylabel("Jumlah Piksel")
            axes[1].set_xlim([0, 256]); axes[1].legend(); axes[1].grid(alpha=0.2)
            fig.tight_layout(); st.pyplot(fig); plt.close(fig)

        with tabs[2]:
            st.markdown("**Normalisasi Histogram** – nilai frekuensi dibagi total piksel → distribusi probabilitas [0, 1]")
            h_img, w_img = img_gray.shape
            total_piksel = h_img * w_img
            hist_raw  = cv2.calcHist([img_gray], [0], None, [256], [0, 256])
            hist_norm = hist_raw / total_piksel
            fig, axes = plt.subplots(1, 2, figsize=(12, 4))
            fig.patch.set_facecolor('#FAFAFA')
            axes[0].plot(hist_raw, color="#E8500A", linewidth=1.5)
            axes[0].fill_between(range(256), hist_raw.flatten(), alpha=0.12, color="#E8500A")
            axes[0].set_title("Histogram (Frekuensi)", fontsize=11, fontweight='bold')
            axes[0].set_xlabel("Nilai Piksel"); axes[0].set_ylabel("Jumlah Piksel")
            axes[0].set_xlim([0, 256]); axes[0].grid(alpha=0.2)
            axes[1].plot(hist_norm, color="#F97316", linewidth=1.5)
            axes[1].fill_between(range(256), hist_norm.flatten(), alpha=0.12, color="#F97316")
            axes[1].set_title("Histogram Normalisasi (Probabilitas)", fontsize=11, fontweight='bold')
            axes[1].set_xlabel("Nilai Piksel"); axes[1].set_ylabel("Probabilitas")
            axes[1].set_xlim([0, 256]); axes[1].grid(alpha=0.2)
            fig.tight_layout(); st.pyplot(fig); plt.close(fig)

        with tabs[3]:
            st.markdown("**Ekualisasi Histogram** – meratakan distribusi piksel untuk meningkatkan kontras")
            hist_eq = cv2.equalizeHist(img_gray)
            fig, axes = plt.subplots(2, 2, figsize=(12, 8))
            fig.patch.set_facecolor('#FAFAFA')
            axes[0][0].imshow(img_gray, cmap="gray"); axes[0][0].set_title("Citra Asli", fontweight='bold'); axes[0][0].axis("off")
            axes[0][1].imshow(hist_eq,  cmap="gray"); axes[0][1].set_title("Hasil Ekualisasi", fontweight='bold'); axes[0][1].axis("off")
            h_raw = cv2.calcHist([img_gray], [0], None, [256], [0, 256])
            h_eq  = cv2.calcHist([hist_eq],  [0], None, [256], [0, 256])
            axes[1][0].plot(h_raw, color="#E8500A"); axes[1][0].set_title("Histogram Asli", fontweight='bold'); axes[1][0].set_xlim([0, 256]); axes[1][0].grid(alpha=0.2)
            axes[1][1].plot(h_eq,  color="#F97316"); axes[1][1].set_title("Setelah Ekualisasi", fontweight='bold'); axes[1][1].set_xlim([0, 256]); axes[1][1].grid(alpha=0.2)
            fig.tight_layout(); st.pyplot(fig); plt.close(fig)

# ─────────────────────────────────────────────
#  HALAMAN: IMAGE FILTERING  [OPSIONAL +20]
# ─────────────────────────────────────────────
elif menu == "Image Filtering":
    st.markdown("""<div class="page-title">
        <div class="page-title-dot"></div>Image Filtering
        <span class="feature-badge badge-opsional">Opsional +20</span>
    </div>""", unsafe_allow_html=True)

    if img_rgb is None:
        st.warning("Silakan upload gambar terlebih dahulu.")
    else:
        st.markdown("""
        <div class="info-box">
        <b>Image Filtering</b> menggunakan operasi konvolusi antara citra dan sebuah <b>kernel/mask</b>.
        Tergantung isi kernel, hasilnya bisa berupa penghalusan, penajaman, atau deteksi tepi.
        </div>
        """, unsafe_allow_html=True)

        filter_type = st.selectbox("Pilih Jenis Filter:", [
            "Blur – Kernel Mean (3×3)",
            "Blur – Kernel Mean (5×5)",
            "Blur – Gaussian (3×3)",
            "Blur – Gaussian (5×5)",
            "Blur – Median",
            "Sharpening – Kernel Laplacian",
            "Sharpening – Unsharp Mask",
            "Edge Detection – Kernel Sobel (X)",
            "Edge Detection – Kernel Sobel (Y)",
            "Edge Detection – Canny",
            "Kernel Nol (3×3) – Demo",
        ])

        result = None
        kernel_disp = None
        code_snippet = ""

        if filter_type == "Blur – Kernel Mean (3×3)":
            kernel_disp = np.ones((3, 3), np.float32) / 9
            result = cv2.filter2D(img_cv, -1, kernel_disp)
            code_snippet = "kernel = np.ones((3,3), np.float32)/9\nresult = cv2.filter2D(img, -1, kernel)"
        elif filter_type == "Blur – Kernel Mean (5×5)":
            kernel_disp = np.ones((5, 5), np.float32) / 25
            result = cv2.filter2D(img_cv, -1, kernel_disp)
            code_snippet = "kernel = np.ones((5,5), np.float32)/25\nresult = cv2.filter2D(img, -1, kernel)"
        elif filter_type == "Blur – Gaussian (3×3)":
            kernel_disp = np.array([[1,2,1],[2,4,2],[1,2,1]], np.float32) / 16
            result = cv2.filter2D(img_cv, -1, kernel_disp)
            code_snippet = "kernel = np.array([[1,2,1],[2,4,2],[1,2,1]], np.float32)/16\nresult = cv2.filter2D(img, -1, kernel)"
        elif filter_type == "Blur – Gaussian (5×5)":
            result = cv2.GaussianBlur(img_cv, (5, 5), sigmaX=0, sigmaY=0)
            code_snippet = "result = cv2.GaussianBlur(img, (5,5), sigmaX=0, sigmaY=0)"
        elif filter_type == "Blur – Median":
            k = st.slider("Ukuran Kernel (ganjil):", 3, 15, 5, 2)
            result = cv2.medianBlur(img_cv, k)
            code_snippet = f"result = cv2.medianBlur(img, {k})"
        elif filter_type == "Sharpening – Kernel Laplacian":
            kernel_disp = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]], np.float32)
            result = cv2.filter2D(img_cv, -1, kernel_disp)
            code_snippet = "kernel = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])\nresult = cv2.filter2D(img, -1, kernel)"
        elif filter_type == "Sharpening – Unsharp Mask":
            blurred = cv2.GaussianBlur(img_cv, (5, 5), sigmaX=1)
            result  = cv2.addWeighted(img_cv, 1.5, blurred, -0.5, 0)
            code_snippet = "blurred = cv2.GaussianBlur(img, (5,5), 1)\nresult = cv2.addWeighted(img, 1.5, blurred, -0.5, 0)"
        elif filter_type == "Edge Detection – Kernel Sobel (X)":
            kernel_disp = np.array([[-1,0,1],[-2,0,2],[-1,0,1]], np.float32)
            result = cv2.filter2D(img_cv, -1, kernel_disp)
            code_snippet = "kernel = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])\nresult = cv2.filter2D(img, -1, kernel)"
        elif filter_type == "Edge Detection – Kernel Sobel (Y)":
            kernel_disp = np.array([[-1,-2,-1],[0,0,0],[1,2,1]], np.float32)
            result = cv2.filter2D(img_cv, -1, kernel_disp)
            code_snippet = "kernel = np.array([[-1,-2,-1],[0,0,0],[1,2,1]])\nresult = cv2.filter2D(img, -1, kernel)"
        elif filter_type == "Edge Detection – Canny":
            t1 = st.slider("Threshold Bawah:", 0, 255, 100)
            t2 = st.slider("Threshold Atas:", 0, 255, 200)
            gray_tmp = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
            result = cv2.Canny(gray_tmp, t1, t2)
            code_snippet = f"gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)\nresult = cv2.Canny(gray, {t1}, {t2})"
        elif filter_type == "Kernel Nol (3×3) – Demo":
            kernel_disp = np.zeros((3, 3), np.float32)
            result = cv2.filter2D(img_cv, -1, kernel_disp)
            code_snippet = "kernel = np.zeros((3,3), np.float32)\nresult = cv2.filter2D(img, -1, kernel)"

        if result is not None:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Gambar Asli**"); st.image(img_rgb, use_container_width=True)
            with col2:
                st.markdown(f"**Hasil: {filter_type}**")
                result_show = cv_to_rgb(result) if len(result.shape) == 3 else result
                st.image(result_show, use_container_width=True, clamp=True)

            if kernel_disp is not None:
                with st.expander("Tampilkan Nilai Kernel"):
                    st.dataframe(kernel_disp, use_container_width=False)

            st.code(code_snippet, language="python")

# ─────────────────────────────────────────────
#  HALAMAN: MORFOLOGI  [OPSIONAL +30]
# ─────────────────────────────────────────────
elif menu == "Morfologi":
    st.markdown("""<div class="page-title">
        <div class="page-title-dot"></div>Operasi Morfologi
        <span class="feature-badge badge-opsional">Opsional +30</span>
    </div>""", unsafe_allow_html=True)

    if img_rgb is None:
        st.warning("Silakan upload gambar terlebih dahulu.")
    else:
        st.markdown("""
        <div class="info-box">
        <b>Operasi Morfologi</b> bekerja pada <b>citra biner</b> menggunakan <b>Structuring Element (SE)</b>.
        <br>· <b>Dilasi</b>: memperluas objek terang.
        <br>· <b>Erosi</b>: mempersempit objek terang.
        <br>· <b>Opening</b>: Erosi → Dilasi (menghilangkan noise kecil).
        <br>· <b>Closing</b>: Dilasi → Erosi (menutup lubang kecil).
        </div>
        """, unsafe_allow_html=True)

        col_ctrl, col_disp = st.columns([1, 2])

        with col_ctrl:
            st.markdown("**Pengaturan**")
            op_morf = st.selectbox("Operasi:", ["Dilasi", "Erosi", "Opening (Erosi→Dilasi)", "Closing (Dilasi→Erosi)"])
            st.markdown("**Structuring Element (SE):**")
            se_shape = st.selectbox("Bentuk SE:", [
                "Persegi (Rect)", "Silang (Cross)", "Ellips",
                "Segitiga Atas (Custom)", "Garis Horizontal (Custom)",
            ])
            se_size   = st.slider("Ukuran SE:", 3, 15, 5, 2)
            iterasi   = st.slider("Iterasi:", 1, 5, 1)
            thresh_morph = st.slider("Threshold Biner:", 0, 255, 127)

        def get_se(shape, size):
            if shape == "Persegi (Rect)":
                return cv2.getStructuringElement(cv2.MORPH_RECT, (size, size))
            elif shape == "Silang (Cross)":
                return cv2.getStructuringElement(cv2.MORPH_CROSS, (size, size))
            elif shape == "Ellips":
                return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (size, size))
            elif shape == "Segitiga Atas (Custom)":
                se = np.zeros((size, size), np.uint8)
                for i in range(size):
                    start = size // 2 - i // 2
                    end   = size // 2 + i // 2 + 1
                    se[size - 1 - i, max(0, start):min(size, end)] = 1
                return se
            elif shape == "Garis Horizontal (Custom)":
                se = np.zeros((size, size), np.uint8)
                se[size // 2, :] = 1
                return se
            return np.ones((size, size), np.uint8)

        se = get_se(se_shape, se_size)
        _, biner_morph = cv2.threshold(img_gray, thresh_morph, 255, cv2.THRESH_BINARY)

        if op_morf == "Dilasi":
            result = cv2.dilate(biner_morph, se, iterations=iterasi)
            code_snippet = f"se = cv2.getStructuringElement(cv2.MORPH_RECT, ({se_size},{se_size}))\nresult = cv2.dilate(biner, se, iterations={iterasi})"
        elif op_morf == "Erosi":
            result = cv2.erode(biner_morph, se, iterations=iterasi)
            code_snippet = f"se = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, ({se_size},{se_size}))\nresult = cv2.erode(biner, se, iterations={iterasi})"
        elif op_morf == "Opening (Erosi→Dilasi)":
            result = cv2.morphologyEx(biner_morph, cv2.MORPH_OPEN, se, iterations=iterasi)
            code_snippet = f"result = cv2.morphologyEx(biner, cv2.MORPH_OPEN, se, iterations={iterasi})"
        else:
            result = cv2.morphologyEx(biner_morph, cv2.MORPH_CLOSE, se, iterations=iterasi)
            code_snippet = f"result = cv2.morphologyEx(biner, cv2.MORPH_CLOSE, se, iterations={iterasi})"

        with col_disp:
            tabs_m = st.tabs(["Hasil Morfologi", "Tampilan SE", "Semua Operasi"])

            with tabs_m[0]:
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.markdown("**RGB Asli**"); st.image(img_rgb, use_container_width=True)
                with c2:
                    st.markdown("**Citra Biner**"); st.image(biner_morph, use_container_width=True, clamp=True)
                with c3:
                    st.markdown(f"**Hasil {op_morf}**"); st.image(result, use_container_width=True, clamp=True)
                st.code(code_snippet, language="python")

            with tabs_m[1]:
                st.markdown(f"**Structuring Element: {se_shape} ({se_size}×{se_size})**")
                fig, ax = plt.subplots(figsize=(3, 3))
                ax.imshow(se, cmap="Oranges", vmin=0, vmax=1, interpolation="nearest")
                ax.set_xticks(range(se_size)); ax.set_yticks(range(se_size))
                ax.grid(True, color="gray", linewidth=0.5)
                for i in range(se.shape[0]):
                    for j in range(se.shape[1]):
                        ax.text(j, i, str(se[i, j]), ha="center", va="center", fontsize=10, fontweight="bold")
                ax.set_title(f"{se_shape} · {se_size}×{se_size}", fontsize=10)
                fig.tight_layout(); st.pyplot(fig); plt.close(fig)
                st.markdown(f"Elemen aktif (=1): **{se.sum()}** dari **{se_size*se_size}**")

            with tabs_m[2]:
                st.markdown("**Perbandingan Semua Operasi Morfologi:**")
                ops_all = {
                    "Biner Asli": biner_morph,
                    "Dilasi":     cv2.dilate(biner_morph, se, iterations=iterasi),
                    "Erosi":      cv2.erode(biner_morph, se, iterations=iterasi),
                    "Opening":    cv2.morphologyEx(biner_morph, cv2.MORPH_OPEN, se),
                    "Closing":    cv2.morphologyEx(biner_morph, cv2.MORPH_CLOSE, se),
                }
                fig, axes = plt.subplots(1, 5, figsize=(16, 3))
                fig.patch.set_facecolor('#FAFAFA')
                for ax, (lbl, im) in zip(axes, ops_all.items()):
                    ax.imshow(im, cmap="gray"); ax.set_title(lbl, fontsize=9, fontweight='bold'); ax.axis("off")
                fig.tight_layout(); st.pyplot(fig); plt.close(fig)

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="app-footer">
    Aplikasi Pengolahan Citra Digital &nbsp;·&nbsp;
    <span>Python + Streamlit + OpenCV</span> &nbsp;·&nbsp;
    Prodi Ilmu Komputer, Institut Teknologi BJH &nbsp;·&nbsp; 2024
</div>
""", unsafe_allow_html=True)
