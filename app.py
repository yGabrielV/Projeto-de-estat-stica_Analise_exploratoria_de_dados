import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import math

# ==========================
# CONFIGURAÇÃO E DADOS
# ==========================
st.set_page_config(page_title="VGC Ultimate Dashboard", layout="wide", page_icon="⚔️")

# Matriz de Tipos Oficial (Linha: Atacante | Coluna: Defensor)
tipos = ['Normal', 'Fire', 'Water', 'Grass', 'Electric', 'Ice', 'Fighting', 'Poison', 'Ground', 
         'Flying', 'Psychic', 'Bug', 'Rock', 'Ghost', 'Dragon', 'Steel', 'Fairy', 'Dark']

# 1.0: Neutro, 2.0: Super, 0.5: Resistente, 0.0: Imune
type_matrix = np.array([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0.5, 0, 1, 0.5, 1, 1], # Normal
    [1, 0.5, 0.5, 2, 1, 2, 1, 1, 1, 1, 1, 2, 0.5, 1, 0.5, 2, 1, 1], # Fire
    [1, 2, 0.5, 0.5, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 0.5, 1, 1, 1], # Water
    [1, 0.5, 2, 0.5, 1, 1, 1, 0.5, 2, 0.5, 1, 0.5, 2, 1, 0.5, 0.5, 1, 1], # Grass
    [1, 1, 2, 0.5, 0.5, 1, 1, 1, 0, 2, 1, 1, 1, 1, 0.5, 1, 1, 1], # Electric
    [1, 0.5, 0.5, 2, 1, 0.5, 1, 1, 2, 2, 1, 1, 1, 1, 2, 0.5, 1, 1], # Ice
    [2, 1, 1, 1, 1, 2, 1, 0.5, 1, 0.5, 0.5, 0.5, 2, 0, 1, 2, 0.5, 2], # Fighting
    [1, 1, 1, 2, 1, 1, 1, 0.5, 0.5, 1, 1, 1, 0.5, 0.5, 1, 0, 2, 1], # Poison
    [1, 2, 1, 0.5, 2, 1, 1, 2, 1, 0, 1, 0.5, 2, 1, 1, 2, 1, 1], # Ground
    [1, 1, 1, 2, 0.5, 1, 2, 1, 1, 1, 1, 2, 0.5, 1, 1, 0.5, 1, 1], # Flying
    [1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 0.5, 1, 1, 1, 1, 0.5, 1, 0], # Psychic
    [1, 0.5, 1, 2, 1, 1, 0.5, 0.5, 1, 0.5, 2, 1, 1, 0.5, 1, 0.5, 0.5, 2], # Bug
    [1, 2, 1, 1, 1, 2, 0.5, 1, 0.5, 2, 1, 2, 1, 1, 1, 0.5, 1, 1], # Rock
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 0.5], # Ghost
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 0.5, 0, 1], # Dragon
    [1, 0.5, 0.5, 1, 0.5, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0.5, 2, 1], # Steel
    [1, 0.5, 1, 1, 1, 1, 2, 0.5, 1, 1, 1, 1, 1, 1, 2, 0.5, 1, 2], # Fairy
    [1, 1, 1, 1, 1, 1, 0.5, 1, 1, 1, 2, 1, 1, 2, 1, 1, 0.5, 0.5]  # Dark
])

@st.cache_data
def load_data():
    df = pd.read_csv('pokemon_data.csv')
    df['Type 1'] = df['Type 1'].fillna('None')
    df['Type 2'] = df['Type 2'].fillna('None')
    if 'Base_Stats' not in df.columns:
        df['Base_Stats'] = df[['HP', 'Attack', 'Defense', 'Sp. Attack', 'Sp. Defense', 'Speed']].sum(axis=1)
    return df

df_raw = load_data()

# ==========================
# SIDEBAR (FILTROS GERAIS)
# ==========================
with st.sidebar:
    st.header("🔎 Filtros Estratégicos")
    
    todas_gens = sorted(df_raw['gen'].unique().tolist())
    f_gen = st.multiselect("Gerações", todas_gens, default=todas_gens)
    
    todos_tipos = sorted(df_raw['Type 1'].unique().tolist())
    f_tipo = st.multiselect("Tipos", todos_tipos, default=todos_tipos)
    
    st.divider()
    scatter_stat = st.selectbox("Eixo Y da Dispersão", ['Base_Stats', 'Attack', 'Sp. Attack', 'Speed', 'Defense', 'HP'])

df_filtered = df_raw[
    (df_raw['gen'].isin(f_gen)) & 
    (df_raw['Type 1'].isin(f_tipo) | df_raw['Type 2'].isin(f_tipo))
]

# ==========================
# UI PRINCIPAL
# ==========================
tab1, tab2, tab3 = st.tabs(["🏠 Dashboard Analítico", "⚔️ Simulador Profissional", "📑 Dados Brutos"])

# --- TAB 1: DASHBOARD ---
with tab1:
    st.title("Insights Competitivos & Meta-Game")
    
    # MATRIZ DE FRAQUEZAS (HEATMAP REAL)
    st.subheader("🎯 Matriz de Eficácia Elemental (Type Chart)")
    fig_matrix = px.imshow(
        type_matrix, x=tipos, y=tipos,
        color_continuous_scale='RdYlGn', text_auto=True,
        labels=dict(x="Defensor", y="Atacante", color="Mult.")
    )
    fig_matrix.update_layout(height=500, margin=dict(l=0,r=0,t=30,b=0))
    st.plotly_chart(fig_matrix, use_container_width=True)
    
    st.divider()
    
    # GRÁFICO DE PIZZA E QUANTIDADE POR GEN
    c1, c2 = st.columns(2)
    with c1:
        st.subheader(" Distribuição de Tipos")
        
        tipos_combinados = pd.concat([df_filtered['Type 1'], df_filtered['Type 2']])
        tipos_combinados = tipos_combinados[tipos_combinados != 'None']
        df_pizza = tipos_combinados.value_counts().reset_index()
        df_pizza.columns = ['Tipo', 'Frequência']
        
        fig_pie = px.pie(df_pizza, values='Frequência', names='Tipo', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with c2:
        st.subheader("📊 Pokémon por Geração")
        fig_bar = px.histogram(df_filtered, x='gen', color='gen', text_auto=True)
        st.plotly_chart(fig_bar, use_container_width=True)
        
    st.divider()
    
    # BOX PLOT (POWER CREEP) E DISPERSÃO
    c3, c4 = st.columns(2)
    with c3:
        st.subheader("📦 Power Creep (BST por Geração)")
        fig_box = px.box(df_filtered, x='gen', y='Base_Stats', color='gen')
        st.plotly_chart(fig_box, use_container_width=True)
    with c4:
        st.subheader(f"🚀 Speed vs {scatter_stat}")
        fig_scatter = px.scatter(df_filtered, x='Speed', y=scatter_stat, color='Type 1', size='Base_Stats', hover_name='Name')
        st.plotly_chart(fig_scatter, use_container_width=True)

# --- TAB 2: CALCULADORA ---
with tab2:
    st.title("Simulador VGC: EVs & Multiplicadores Individuais")

    def calc_stat(base, iv, ev, level, hp=False):
        if hp: return math.floor(((2*base + iv + ev//4)*level)/100) + level + 10
        return math.floor(((2*base + iv + ev//4)*level)/100) + 5

    def pk_ui(side, label, color):
        st.markdown(f"### <span style='color:{color}'>{label}</span>", unsafe_allow_html=True)
        nome = st.selectbox("Pokémon", df_raw['Name'].sort_values(), key=f"n_{side}")
        data = df_raw[df_raw['Name'] == nome].iloc[0]
        
        # --- SEÇÃO DE EVs ---
        st.markdown("#### 🏃 Distribuição de EVs")
        stats_labels = ['HP', 'Attack', 'Defense', 'Sp. Attack', 'Sp. Defense', 'Speed']
        cols_ev = st.columns(6)
        ev_vals = {}
        
        for i, s in enumerate(stats_labels):
            ev_vals[s] = cols_ev[i].number_input(s, 0, 252, 0 if s!='HP' else 252, key=f"ev_{side}_{s}", help="Máximo 252")
        
        total_evs = sum(ev_vals.values())
        falta = 510 - total_evs
        
        if total_evs > 510:
            st.error(f"⚠️ Total: {total_evs}/510 EVs (Limite Excedido!)")
        else:
            st.success(f"✅ Total: {total_evs}/510 EVs (Faltam: {falta})")

        # --- SEÇÃO DE BUFFS (INDIVIDUAIS POR STATUS) ---
        st.markdown("#### ⚡ Buffs de Status (Stages)")
        buff_options = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
        
        c_buff1, c_buff2, c_buff3, c_buff4, c_buff5 = st.columns(5)
        b_atk = c_buff1.select_slider("Atk", options=buff_options, value=1.0, key=f"batk_{side}")
        b_def = c_buff2.select_slider("Def", options=buff_options, value=1.0, key=f"bdef_{side}")
        b_spa = c_buff3.select_slider("SpA", options=buff_options, value=1.0, key=f"bspa_{side}")
        b_spd = c_buff4.select_slider("SpD", options=buff_options, value=1.0, key=f"bspd_{side}")
        b_spe = c_buff5.select_slider("Spe", options=buff_options, value=1.0, key=f"bspe_{side}")
        
        buffs = {'HP': 1.0, 'Attack': b_atk, 'Defense': b_def, 'Sp. Attack': b_spa, 'Sp. Defense': b_spd, 'Speed': b_spe}

        # Cálculo dos Stats Finais
        reais_base = {s: calc_stat(data[s], 31, ev_vals[s], 50, hp=(s=='HP')) for s in stats_labels}
        reais_final = {s: math.floor(reais_base[s] * buffs[s]) for s in stats_labels}

        # Gráfico Radar
        fig_radar = go.Figure(data=go.Scatterpolar(r=[reais_final[s] for s in stats_labels], theta=stats_labels, fill='toself', line_color=color))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=False)), height=280, margin=dict(l=40,r=40,t=20,b=20))
        st.plotly_chart(fig_radar, use_container_width=True)
        
        # Ataque Selecionado
        st.markdown("#### ⚔️ Movimento")
        c_at = st.columns(2)
        m_type = c_at[0].selectbox("Tipo", tipos, key=f"mt_{side}")
        m_cat = c_at[1].radio("Categoria", ["Físico", "Especial"], key=f"mc_{side}", horizontal=True)
        m_pwr = st.number_input("Poder Base", 0, 250, 90, key=f"mp_{side}")
        
        return data, reais_final, m_type, m_cat, m_pwr

    col_a, col_b = st.columns(2)
    with col_a: p1 = pk_ui("a", "🔴 Atacante A", "#EF553B")
    with col_b: p2 = pk_ui("b", "🔵 Atacante B", "#636EFA")

    # Lógica de Dano
    def damage_engine(atk, defe, label):
        d_atk, s_atk, m_type, m_cat, m_pwr = atk
        d_def, s_def, _, _, _ = defe
        
        a = s_atk['Attack' if m_cat == "Físico" else 'Sp. Attack']
        d = s_def['Defense' if m_cat == "Físico" else 'Sp. Defense']
        
        stab = 1.5 if (m_type == d_atk['Type 1'] or m_type == d_atk['Type 2']) else 1.0
        
        idx_atk = tipos.index(m_type)
        eff = 1.0
        for t_def in [d_def['Type 1'], d_def['Type 2']]:
            if t_def in tipos:
                eff *= type_matrix[idx_atk][tipos.index(t_def)]
        
        base = math.floor(math.floor((math.floor((2 * 50) / 5) + 2) * m_pwr * (a / d)) / 50) + 2
        low, high = math.floor(base * 0.85 * stab * eff), math.floor(base * 1.0 * stab * eff)
        p_low, p_high = (low/s_def['HP'])*100, (high/s_def['HP'])*100
        
        st.subheader(label)
        st.write(f"Dano: **{low}-{high}** ({p_low:.1f}% - {p_high:.1f}%)")
        st.progress(min(p_high/100, 1.0))
        if p_low >= 100: st.error("💀 OHKO!")

    st.divider()
    res1, res2 = st.columns(2)
    with res1: damage_engine(p1, p2, "Lado A ataca B")
    with res2: damage_engine(p2, p1, "Lado B ataca A")

# --- TAB 3 ---
with tab3:
    st.dataframe(df_filtered, use_container_width=True)