# -*- coding: utf-8 -*-
"""
Application Web d'Analyse du Potentiel Éolien
Avec vidéo locale en arrière-plan - Version Ultra HD
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.special import gamma
from scipy.optimize import fsolve
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import os
from datetime import datetime
import base64
import tempfile

# Note: Pour les rapports PDF, installez fpdf avec: pip install fpdf
# from fpdf import FPDF  # Commenté pour éviter l'erreur

# Configuration de la page
st.set_page_config(
    page_title="YAN - Analyse Éolienne",
    page_icon="🌪️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# THÈME PERSONNALISÉ
# ============================================
st.markdown("""
<style>
    /* Changer les couleurs principales */
    :root {
        --primary-color: #2ecc71;
        --secondary-color: #27ae60;
        --accent-color: #3498db;
    }
    
    /* Boutons */
    .stButton > button {
        background: linear-gradient(135deg, #2ecc71, #27ae60) !important;
        color: white !important;
        border-radius: 25px !important;
        border: none !important;
        font-weight: bold !important;
        padding: 10px 25px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 12px rgba(0,0,0,0.2) !important;
    }
    
    /* Métriques */
    .stMetric {
        background: rgba(255, 255, 255, 0.95) !important;
        padding: 20px !important;
        border-radius: 15px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
        border-left: 5px solid #2ecc71 !important;
        backdrop-filter: blur(2px);
    }
    
    .stMetric label {
        color: #2c3e50 !important;
        font-weight: bold !important;
    }
    
    .stMetric value {
        color: #27ae60 !important;
        font-size: 2.2em !important;
        font-weight: bold !important;
    }
    
    /* Titres */
    h1, h2, h3 {
        color: #27ae60 !important;
        font-weight: bold !important;
        text-shadow: 2px 2px 4px rgba(255,255,255,0.5);
    }
    
    /* Sidebar */
    .css-1d391kg, .st-emotion-cache-1d391kg {
        background: rgba(26, 38, 52, 0.85) !important;
        backdrop-filter: blur(5px);
    }
    
    /* DataFrames */
    .stDataFrame {
        background: rgba(255, 255, 255, 0.95) !important;
        border-radius: 15px !important;
        padding: 10px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
        backdrop-filter: blur(2px);
    }
    
    /* Graphiques */
    .stPlotlyChart, .stPyplot {
        background: rgba(255, 255, 255, 0.95) !important;
        padding: 15px !important;
        border-radius: 15px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
        margin: 15px 0 !important;
        backdrop-filter: blur(2px);
    }
    
    /* Messages */
    .stSuccess, .stInfo {
        border-radius: 10px !important;
        padding: 15px !important;
        font-weight: bold !important;
    }
    
    .stSuccess {
        background: linear-gradient(135deg, #27ae60, #2ecc71) !important;
        color: white !important;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #3498db, #2980b9) !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# VIDÉO EN ARRIÈRE-PLAN (VERSION AMÉLIORÉE)
# ============================================

# Vérifier si la vidéo existe
video_path = "eolienne.mp4"
if os.path.exists(video_path):
    # Lire la vidéo
    with open(video_path, "rb") as f:
        video_bytes = f.read()
    
    # Convertir en base64
    video_base64 = base64.b64encode(video_bytes).decode()
    
    # Afficher la vidéo en arrière-plan
    st.markdown(
        f"""
        <style>
        /* Supprimer le fond par défaut */
        .stApp {{
            background: none !important;
        }}
        
        /* Conteneur vidéo - plein écran */
        .video-background {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -2;
            overflow: hidden;
        }}
        
        /* Style de la vidéo - HD */
        .video-background video {{
            min-width: 100%;
            min-height: 100%;
            width: auto;
            height: auto;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            object-fit: cover;
            opacity: 0.65;
            filter: brightness(1.1) contrast(1.1);
        }}
        
        /* Overlay subtil pour meilleure lisibilité */
        .overlay {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.15);
            z-index: -1;
            pointer-events: none;
        }}
        
        /* Contenu principal - sans flou blanc */
        .main-content {{
            background: transparent;
            padding: 20px;
            border-radius: 15px;
            margin: 10px;
        }}
        
        /* Sidebar avec fond semi-transparent */
        .css-1d391kg, .st-emotion-cache-1d391kg {{
            background: rgba(26, 38, 52, 0.85) !important;
            backdrop-filter: blur(5px);
        }}
        </style>
        
        <div class="video-background">
            <video autoplay loop muted playsinline>
                <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
            </video>
        </div>
        <div class="overlay"></div>
        
        <div class="main-content">
        """,
        unsafe_allow_html=True
    )
else:
    st.warning("⚠️ Vidéo 'eolienne.mp4' non trouvée. L'application fonctionne sans fond vidéo.")
    st.markdown('<div class="main-content">', unsafe_allow_html=True)

# ============================================
# LOGO
# ============================================

st.markdown("""
<div style='text-align: center; padding: 10px;'>
    <div style='display: inline-block; background: linear-gradient(135deg, #2c3e50, #3498db); 
                padding: 15px 30px; border-radius: 50px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);'>
        <span style='font-size: 48px; font-weight: bold; color: white;'>YAN</span>
        <span style='font-size: 36px; color: #ff6b6b;'>🥰🥰</span>
    </div>
    <p style='color: #27ae60; font-size: 18px; margin-top: 10px; font-weight: bold; text-shadow: 2px 2px 4px rgba(255,255,255,0.5);'>
        ⚡ Solutions Énergétiques ⚡
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ============================================
# FONCTIONS DE CALCUL
# ============================================

def load_data(file):
    try:
        df = pd.read_csv(file)
        return df
    except Exception as e:
        st.error(f"Erreur de chargement : {e}")
        return None

def calculate_statistics(speeds):
    return {
        'mean': np.mean(speeds),
        'std': np.std(speeds),
        'min': np.min(speeds),
        'max': np.max(speeds),
        'median': np.median(speeds),
        'q1': np.percentile(speeds, 25),
        'q3': np.percentile(speeds, 75)
    }

def calculate_weibull(speeds):
    v_mean = np.mean(speeds)
    sigma = np.std(speeds)
    
    def equation(k):
        return gamma(1 + 2/k) / (gamma(1 + 1/k))**2 - (1 + (sigma/v_mean)**2)
    
    k = fsolve(equation, 2.0)[0]
    c = v_mean / gamma(1 + 1/k)
    return k, c

def weibull_pdf(v, k, c):
    return (k/c) * (v/c)**(k-1) * np.exp(-(v/c)**k)

def weibull_cdf(v, k, c):
    return 1 - np.exp(-(v/c)**k)

def wind_power_density(speeds, rho=1.225):
    return 0.5 * rho * np.mean(speeds**3)

def turbine_power_curve(v, turbine):
    v_in = turbine['V_demarrage']
    v_rated = turbine['V_nominale']
    v_out = turbine['V_coupure']
    P_rated = turbine['Puissance_MW'] * 1000
    
    if v < v_in or v > v_out:
        return 0
    elif v < v_rated:
        return P_rated * ((v - v_in) / (v_rated - v_in))**3
    else:
        return P_rated

def calculate_turbine_production(wind_data, turbine):
    powers = [turbine_power_curve(v, turbine) for v in wind_data]
    mean_power_kw = np.mean(powers)
    aep_mwh = mean_power_kw * 8760 / 1000
    capacity_factor = (aep_mwh) / (turbine['Puissance_MW'] * 8760) * 100
    return aep_mwh, capacity_factor

# ============================================
# GRAPHIQUES WEIBULL AMÉLIORÉS
# ============================================

def plot_enhanced_weibull(speeds, k, c):
    """Version améliorée avec plus de détails et style pro"""
    
    fig = plt.figure(figsize=(18, 12))
    
    # Style plus professionnel
    plt.style.use('seaborn-v0_8-darkgrid')
    
    # 1. Histogramme interactif
    ax1 = plt.subplot(2, 3, 1)
    n, bins, patches = ax1.hist(speeds, bins=50, density=True, 
                                alpha=0.7, color='#3498db', edgecolor='white', linewidth=0.5)
    
    v_plot = np.linspace(0, 25, 200)
    pdf_vals = weibull_pdf(v_plot, k, c)
    ax1.plot(v_plot, pdf_vals, 'r-', linewidth=3, label=f'Weibull (k={k:.2f}, c={c:.2f})')
    ax1.fill_between(v_plot, 0, pdf_vals, alpha=0.2, color='red')
    ax1.set_xlabel('Vitesse du vent (m/s)', fontsize=12)
    ax1.set_ylabel('Densité de probabilité', fontsize=12)
    ax1.set_title('Distribution de Weibull', fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. Distribution cumulative
    ax2 = plt.subplot(2, 3, 2)
    sorted_speed = np.sort(speeds)
    ecdf = np.arange(1, len(sorted_speed)+1) / len(sorted_speed)
    ax2.plot(sorted_speed, ecdf, 'b-', linewidth=2, label='Données réelles', alpha=0.7)
    
    cdf_vals = 1 - np.exp(-(v_plot/c)**k)
    ax2.plot(v_plot, cdf_vals, 'r--', linewidth=2, label='Weibull théorique')
    ax2.set_xlabel('Vitesse du vent (m/s)', fontsize=12)
    ax2.set_ylabel('Probabilité cumulative', fontsize=12)
    ax2.set_title('Fonction de répartition', fontsize=14, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. QQ-Plot avec ligne de confiance
    ax3 = plt.subplot(2, 3, 3)
    theoretical_quantiles = c * (-np.log(1 - np.linspace(0.01, 0.99, 100)))**(1/k)
    empirical_quantiles = np.percentile(speeds, np.linspace(1, 99, 100))
    
    ax3.scatter(theoretical_quantiles, empirical_quantiles, alpha=0.6, s=30, color='#27ae60')
    ax3.plot([0, 25], [0, 25], 'r--', linewidth=2, label='Parfaite correspondance')
    
    # Intervalle de confiance à 95%
    z = 1.96
    std_err = np.std(empirical_quantiles - theoretical_quantiles)
    ax3.fill_between([0, 25], [0-z*std_err, 25-z*std_err], 
                     [0+z*std_err, 25+z*std_err], alpha=0.1, color='gray')
    
    ax3.set_xlabel('Quantiles théoriques', fontsize=12)
    ax3.set_ylabel('Quantiles empiriques', fontsize=12)
    ax3.set_title('QQ-Plot avec intervalle de confiance', fontsize=14, fontweight='bold')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    ax3.set_xlim(0, 25)
    ax3.set_ylim(0, 25)
    
    # 4. Graphique en radar des classes
    ax4 = plt.subplot(2, 3, 4, projection='polar')
    classes = [0, 3, 6, 9, 12, 15, 25]
    labels = ['0-3 m/s', '3-6 m/s', '6-9 m/s', '9-12 m/s', '12-15 m/s', '15+ m/s']
    freqs = []
    for i in range(len(classes)-1):
        freq = np.mean((speeds >= classes[i]) & (speeds < classes[i+1])) * 100
        freqs.append(freq)
    
    angles = np.linspace(0, 2 * np.pi, len(freqs), endpoint=False).tolist()
    freqs += freqs[:1]
    angles += angles[:1]
    
    ax4.plot(angles, freqs, 'o-', linewidth=2, color='#e74c3c', markersize=8)
    ax4.fill(angles, freqs, alpha=0.25, color='#e74c3c')
    ax4.set_xticks(angles[:-1])
    ax4.set_xticklabels(labels, fontsize=9)
    ax4.set_title('Distribution par classe de vent (%)', fontsize=14, fontweight='bold', pad=20)
    
    # 5. Boxplot horizontal
    ax5 = plt.subplot(2, 3, 5)
    box_data = [speeds]
    bp = ax5.boxplot(box_data, vert=False, patch_artist=True)
    bp['boxes'][0].set_facecolor('#3498db')
    bp['boxes'][0].set_alpha(0.7)
    ax5.set_xlabel('Vitesse du vent (m/s)', fontsize=12)
    ax5.set_title('Boxplot des vitesses', fontsize=14, fontweight='bold')
    ax5.grid(True, alpha=0.3)
    
    # 6. Graphique des probabilités
    ax6 = plt.subplot(2, 3, 6)
    prob_25 = 1 - weibull_cdf(25, k, c)
    prob_20 = 1 - weibull_cdf(20, k, c)
    prob_15 = 1 - weibull_cdf(15, k, c)
    prob_10 = 1 - weibull_cdf(10, k, c)
    prob_5 = 1 - weibull_cdf(5, k, c)
    
    categories = ['V > 5 m/s', 'V > 10 m/s', 'V > 15 m/s', 'V > 20 m/s', 'V > 25 m/s']
    values = [prob_5*100, prob_10*100, prob_15*100, prob_20*100, prob_25*100]
    colors = ['#2ecc71', '#f1c40f', '#e67e22', '#e74c3c', '#c0392b']
    
    bars = ax6.bar(categories, values, color=colors, alpha=0.7)
    ax6.set_ylabel('Probabilité (%)', fontsize=12)
    ax6.set_title('Probabilités de dépassement', fontsize=14, fontweight='bold')
    ax6.grid(True, alpha=0.3, axis='y')
    
    # Ajouter les valeurs sur les barres
    for bar, val in zip(bars, values):
        height = bar.get_height()
        ax6.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{val:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    return fig

# ============================================
# FONCTIONS DE SAUVEGARDE
# ============================================

def save_results(data, filename="resultats.csv"):
    try:
        data.to_csv(filename, index=False)
        st.success(f"✅ Résultats sauvegardés dans {filename}")
        return True
    except Exception as e:
        st.error(f"Erreur de sauvegarde : {e}")
        return False

def generate_report(speeds, k, c, stats, turbine_results):
    report = f"""
========================================
RAPPORT D'ANALYSE ÉOLIENNE - YAN Energy
========================================

Date : {datetime.now().strftime('%d/%m/%Y %H:%M')}

1. STATISTIQUES DU VENT
-----------------------
• Vitesse moyenne : {stats['mean']:.2f} m/s
• Écart-type : {stats['std']:.2f} m/s
• Vitesse max : {stats['max']:.2f} m/s
• Médiane : {stats['median']:.2f} m/s

2. PARAMÈTRES DE WEIBULL
------------------------
• k (facteur de forme) : {k:.3f}
• c (facteur d'échelle) : {c:.3f} m/s

3. POTENTIEL ÉNERGÉTIQUE
------------------------
• Puissance moyenne : {wind_power_density(speeds):.1f} W/m²
• Énergie annuelle : {wind_power_density(speeds) * 8760 / 1000:.0f} kWh/m²/an

4. TOP 3 ÉOLIENNES
------------------
"""
    
    for i, row in turbine_results.head(3).iterrows():
        report += f"""
{i+1}. {row['Turbine']}
   • Production : {row['Production (MWh/an)']:.0f} MWh/an
   • Facteur capacité : {row['Facteur capacité (%)']}%
"""
    
    return report

# ============================================
# BASE DE DONNÉES DES ÉOLIENNES
# ============================================

@st.cache_data
def load_turbines():
    turbines_data = {
        'Nom': [
            'Vestas V90 2.0MW', 'Gamesa G90 2.0MW', 'Siemens SWT-2.3-93',
            'Enercon E70 2.3MW', 'Vestas V80 2.0MW', 'GE 2.5-120',
            'Senvion MM92 2.05MW', 'Nordex N90 2.5MW', 'Vestas V112 3.0MW',
            'Siemens SWT-3.6-120'
        ],
        'Puissance_MW': [2.0, 2.0, 2.3, 2.3, 2.0, 2.5, 2.05, 2.5, 3.0, 3.6],
        'Diametre_m': [90, 90, 93, 70, 80, 120, 92, 90, 112, 120],
        'V_demarrage': [3.0, 3.0, 3.0, 2.5, 4.0, 3.0, 3.0, 3.0, 3.0, 3.0],
        'V_nominale': [12.0, 12.0, 13.0, 13.0, 15.0, 12.0, 13.0, 13.0, 12.0, 13.0],
        'V_coupure': [25.0, 25.0, 25.0, 25.0, 25.0, 25.0, 25.0, 25.0, 25.0, 25.0],
        'Classe_IEC': ['IIIa', 'IIIa', 'IIa', 'IIa', 'Ia', 'IIIb', 'IIa', 'IIa', 'IIIa', 'Ib']
    }
    return pd.DataFrame(turbines_data)

# ============================================
# SIDEBAR
# ============================================

with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 15px; background: rgba(46, 204, 113, 0.2); 
                border-radius: 15px; margin-bottom: 15px; border-left: 5px solid #2ecc71;'>
        <span style='font-size: 30px; font-weight: bold; color: #2ecc71;'>YAN</span>
        <span style='font-size: 24px; color: #ff6b6b;'>🥰🥰</span>
        <p style='color: #ecf0f1; font-size: 11px; margin-top: 5px;'>⚡ Solutions Énergétiques ⚡</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.title("Navigation")
    
    choice = option_menu(
        menu_title=None,
        options=["Import", "Statistiques", "Weibull", "Énergie", "Éoliennes"],
        icons=["cloud-upload", "bar-chart", "graph-up", "lightning", "wind"],
        default_index=0,
    )
    
    st.markdown("---")
    st.markdown("**À propos**")
    st.info("Application d'analyse de sites éoliens - Version 5.0 HD")

# ============================================
# PAGES
# ============================================

if choice == "Import":
    st.header("📂 Import des données")
    
    col1, col2 = st.columns(2)
    
    with col1:
        uploaded_file = st.file_uploader(
            "Choisissez votre fichier CSV",
            type=['csv'],
            help="Format attendu : Date/Time, Wind Speed (m/s), LV ActivePower (kW), ..."
        )
        
        if uploaded_file is not None:
            df = load_data(uploaded_file)
            if df is not None:
                st.session_state['data'] = df
                st.success(f"✅ Fichier chargé : {len(df)} lignes")
    
    with col2:
        if st.button("📊 Utiliser les données exemple (T1.csv)"):
            try:
                df = pd.read_csv('T1.csv')
                st.session_state['data'] = df
                st.success(f"✅ Données exemple chargées : {len(df)} lignes")
            except Exception as e:
                st.error(f"Fichier T1.csv non trouvé : {e}")
    
    if 'data' in st.session_state:
        st.subheader("Aperçu des données")
        df = st.session_state['data']
        st.dataframe(df.head(10), use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Lignes", len(df))
        with col2:
            st.metric("Colonnes", len(df.columns))
        with col3:
            try:
                if 'Date/Time' in df.columns:
                    st.metric("Période", f"{df['Date/Time'].iloc[0][:10]} → {df['Date/Time'].iloc[-1][:10]}")
                else:
                    st.metric("Période", "N/A")
            except:
                st.metric("Période", "N/A")

elif choice == "Statistiques":
    st.header("📊 Statistiques du site")
    
    if 'data' not in st.session_state:
        st.warning("⚠️ Veuillez d'abord importer des données")
    else:
        df = st.session_state['data']
        
        speed_col = None
        for col in df.columns:
            if 'speed' in col.lower() or 'vitesse' in col.lower():
                speed_col = col
                break
        
        if speed_col is None:
            st.error("Colonne de vitesse non trouvée")
        else:
            speeds = df[speed_col].dropna().values
            stats = calculate_statistics(speeds)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Vitesse moyenne", f"{stats['mean']:.2f} m/s")
            with col2:
                st.metric("Écart-type", f"{stats['std']:.2f} m/s")
            with col3:
                st.metric("Vitesse max", f"{stats['max']:.2f} m/s")
            with col4:
                st.metric("Médiane", f"{stats['median']:.2f} m/s")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Histogramme des vitesses")
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.hist(speeds, bins=50, color='#3498db', edgecolor='black', alpha=0.7)
                ax.axvline(stats['mean'], color='red', linestyle='--', linewidth=2, 
                          label=f"Moyenne = {stats['mean']:.2f} m/s")
                ax.set_xlabel("Vitesse du vent (m/s)")
                ax.set_ylabel("Fréquence")
                ax.legend()
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)
                plt.close()
            
            with col2:
                st.subheader("Boxplot")
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.boxplot(speeds)
                ax.set_ylabel("Vitesse du vent (m/s)")
                ax.set_title("Distribution des vitesses")
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)
                plt.close()
            
            stats_df = pd.DataFrame({
                'Statistique': ['Moyenne', 'Écart-type', 'Minimum', 'Maximum', 'Médiane', 'Q1', 'Q3'],
                'Valeur (m/s)': [
                    f"{stats['mean']:.2f}",
                    f"{stats['std']:.2f}",
                    f"{stats['min']:.2f}",
                    f"{stats['max']:.2f}",
                    f"{stats['median']:.2f}",
                    f"{stats['q1']:.2f}",
                    f"{stats['q3']:.2f}"
                ]
            })
            st.dataframe(stats_df, use_container_width=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Sauvegarder les statistiques"):
                    save_results(stats_df, "statistiques.csv")
            with col2:
                if st.button("📄 Préparer rapport"):
                    st.info("Utilisez la page Éoliennes pour le rapport complet")

elif choice == "Weibull":
    st.header("📈 Distribution de Weibull")
    
    if 'data' not in st.session_state:
        st.warning("⚠️ Veuillez d'abord importer des données")
    else:
        df = st.session_state['data']
        
        speed_col = None
        for col in df.columns:
            if 'speed' in col.lower() or 'vitesse' in col.lower():
                speed_col = col
                break
        
        if speed_col is None:
            st.error("Colonne de vitesse non trouvée")
        else:
            speeds = df[speed_col].dropna().values
            k, c = calculate_weibull(speeds)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("k (facteur de forme)", f"{k:.3f}")
            with col2:
                st.metric("c (facteur d'échelle)", f"{c:.3f} m/s")
            with col3:
                if k < 2:
                    qualif = "Vents variables"
                elif k < 3:
                    qualif = "Vents modérés"
                else:
                    qualif = "Vents constants"
                st.metric("Qualification", qualif)
            
            st.subheader("📊 Analyse Weibull détaillée")
            fig = plot_enhanced_weibull(speeds, k, c)
            st.pyplot(fig)
            plt.close()
            
            if st.button("💾 Sauvegarder les paramètres Weibull"):
                weibull_df = pd.DataFrame({'Paramètre': ['k', 'c'], 'Valeur': [k, c]})
                save_results(weibull_df, "parametres_weibull.csv")

elif choice == "Énergie":
    st.header("⚡ Potentiel énergétique")
    
    if 'data' not in st.session_state:
        st.warning("⚠️ Veuillez d'abord importer des données")
    else:
        df = st.session_state['data']
        
        speed_col = None
        for col in df.columns:
            if 'speed' in col.lower() or 'vitesse' in col.lower():
                speed_col = col
                break
        
        if speed_col is None:
            st.error("Colonne de vitesse non trouvée")
        else:
            speeds = df[speed_col].dropna().values
            k, c = calculate_weibull(speeds)
            power_density = wind_power_density(speeds)
            annual_energy = power_density * 8760 / 1000
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Puissance moyenne", f"{power_density:.1f} W/m²")
            with col2:
                st.metric("Énergie annuelle", f"{annual_energy:.0f} kWh/m²/an")
            with col3:
                st.metric("Pour 100m de rotor", f"{annual_energy * 7854 / 1e6:.1f} GWh/an")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Contribution énergétique par classe")
                bins = np.arange(0, 26, 1)
                v_power = 0.5 * 1.225 * (bins[:-1]**3)
                freq, _ = np.histogram(speeds, bins=bins)
                energy_contrib = freq * v_power / 1000
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.bar(bins[:-1], energy_contrib, width=0.8, color='#2ecc71', alpha=0.7, edgecolor='black')
                ax.set_xlabel("Vitesse du vent (m/s)")
                ax.set_ylabel("Énergie totale (kWh)")
                ax.set_title("Contribution par classe de vent")
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)
                plt.close()
            
            with col2:
                st.subheader("Énergie cumulative")
                cumulative = np.cumsum(energy_contrib) / np.sum(energy_contrib) * 100
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.plot(bins[:-1], cumulative, 'r-', linewidth=2, marker='o', markersize=3)
                ax.set_xlabel("Vitesse du vent (m/s)")
                ax.set_ylabel("Énergie cumulative (%)")
                ax.axhline(50, color='gray', linestyle='--', alpha=0.5, label='50%')
                ax.axhline(90, color='gray', linestyle='--', alpha=0.5, label='90%')
                ax.legend()
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)
                plt.close()
            
            if st.button("💾 Sauvegarder le potentiel énergétique"):
                energy_df = pd.DataFrame({
                    'Métrique': ['Puissance moyenne (W/m²)', 'Énergie annuelle (kWh/m²)'],
                    'Valeur': [power_density, annual_energy]
                })
                save_results(energy_df, "potentiel_energetique.csv")

elif choice == "Éoliennes":
    st.header("🏭 Sélection de l'éolienne optimale")
    
    if 'data' not in st.session_state:
        st.warning("⚠️ Veuillez d'abord importer des données")
    else:
        df = st.session_state['data']
        
        speed_col = None
        for col in df.columns:
            if 'speed' in col.lower() or 'vitesse' in col.lower():
                speed_col = col
                break
        
        if speed_col is None:
            st.error("Colonne de vitesse non trouvée")
        else:
            speeds = df[speed_col].dropna().values
            turbines_df = load_turbines()
            stats = calculate_statistics(speeds)
            k, c = calculate_weibull(speeds)
            
            results = []
            for _, turbine in turbines_df.iterrows():
                aep, cf = calculate_turbine_production(speeds, turbine)
                results.append({
                    'Turbine': turbine['Nom'],
                    'Puissance (MW)': turbine['Puissance_MW'],
                    'Diamètre (m)': turbine['Diametre_m'],
                    'Production (MWh/an)': round(aep, 0),
                    'Facteur capacité (%)': round(cf, 1)
                })
            
            results_df = pd.DataFrame(results)
            results_df = results_df.sort_values('Production (MWh/an)', ascending=False)
            
            st.subheader("🏆 Top 3 des éoliennes")
            col1, col2, col3 = st.columns(3)
            
            cols = [col1, col2, col3]
            for i, (idx, row) in enumerate(results_df.head(3).iterrows()):
                with cols[i]:
                    medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉"
                    st.markdown(f"### {medal} {row['Turbine']}")
                    st.markdown(f"**Puissance :** {row['Puissance (MW)']} MW")
                    st.markdown(f"**Diamètre :** {row['Diamètre (m)']} m")
                    st.markdown(f"**Production :** {row['Production (MWh/an)']:,.0f} MWh/an")
                    st.markdown(f"**Facteur capacité :** {row['Facteur capacité (%)']}%")
                    st.markdown("---")
            
            st.subheader("📊 Comparatif complet")
            st.dataframe(results_df, use_container_width=True)
            
            st.subheader("📈 Comparaison des productions")
            fig = px.bar(results_df.head(10), x='Production (MWh/an)', y='Turbine',
                        color='Facteur capacité (%)', color_continuous_scale='viridis')
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
            
            best = results_df.iloc[0]
            st.success(f"""
            **Éolienne recommandée : {best['Turbine']}**
            
            - ✅ Production annuelle : {best['Production (MWh/an)']:,.0f} MWh
            - ✅ Facteur de capacité : {best['Facteur capacité (%)']}%
            - ✅ Diamètre rotor : {best['Diamètre (m)']} m
            - ✅ Puissance : {best['Puissance (MW)']} MW
            """)
            
            st.subheader("💾 Sauvegarder les résultats")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                csv = results_df.to_csv(index=False).encode('utf-8')
                st.download_button(label="📥 Télécharger CSV complet", data=csv,
                                  file_name='comparaison_eoliennes.csv', mime='text/csv')
            
            with col2:
                if st.button("📊 Sauvegarder le top 3"):
                    save_results(results_df.head(3), "top3_eoliennes.csv")
            
            with col3:
                if st.button("📄 Générer rapport texte"):
                    report = generate_report(speeds, k, c, stats, results_df)
                    st.download_button(label="📥 Télécharger le rapport", data=report,
                                      file_name='rapport_eolien.txt', mime='text/plain')

# ============================================
# FERMETURE DE LA DIV PRINCIPALE
# ============================================
st.markdown("</div>", unsafe_allow_html=True)

# ============================================
# PIED DE PAGE
# ============================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px;'>
    <p style='color: #27ae60; font-size: 14px; font-weight: bold; text-shadow: 2px 2px 4px rgba(255,255,255,0.5);'>
        🌪️ <b>YAN</b> - Solutions Énergétiques
    </p>
    <p style='color: #2c3e50; font-size: 12px;'>
        © 2025 - Tous droits réservés
    </p>
</div>
""", unsafe_allow_html=True)