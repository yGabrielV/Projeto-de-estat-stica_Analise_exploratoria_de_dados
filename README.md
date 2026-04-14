# Projeto-de-estatstica_Analise_exploratoria_de_dados
⚔️ VGC Ultimate Dashboard & EDA Pro
Este projeto é uma solução completa para análise competitiva de Pokémon (VGC - Video Game Championships). Ele combina uma Análise Exploratória de Dados (EDA) profunda em ambiente Jupyter com um Dashboard Interativo que inclui um simulador de danos avançado e gerenciamento preciso de recursos (EVs e Status).

🚀 Funcionalidades Principais
1. Dashboard Analítico (Streamlit)
Matriz de Eficácia Interativa: Heatmap 18x18 detalhando multiplicadores de dano e imunidades.

Visão de Meta-Game: Gráficos de distribuição real de tipos (unificando Type 1 e Type 2) e análise de Power Creep por geração.

Filtros Estratégicos: Segmentação por geração, tipos e atributos específicos.

2. Simulador VGC Profissional
Calculadora de Danos Dinâmica: Motor de cálculo baseado nas fórmulas oficiais da Gen 9.

Limitador de EVs Realista: * Trava de segurança de 252 EVs por status.

Limite regulamentar de 510 EVs totais por Pokémon.

Indicador visual de saldo de pontos restantes.

Sistema de Buffs Individuais: Seletores de multiplicadores independentes para cada status (de x1.0 a x4.0), permitindo simular estágios de Attack (+2), Defense (+1), etc.

Radar Chart Dinâmico: Visualização geométrica dos status finais após a aplicação de EVs e Buffs.

3. Notebook de Análise Exploratória (app.ipynb)
Uma jornada técnica documentada que cobre:

Limpeza de Dados: Tratamento de nulos e preparação de tipos secundários.

Feature Engineering: Criação da métrica BST (Base Stat Total).

Análise de Raridade: Estudo da hierarquia entre Comuns, Ultra Beasts, Míticos e Lendários.

Correlação de Performance: Gráficos de dispersão focados em Speed vs Offense para identificar Glass Cannons e Trick Room candidates.

🛠️ Tecnologias Utilizadas
Linguagem: Python

Manipulação de Dados: Pandas, NumPy

Visualização Estática: Matplotlib, Seaborn

Visualização Interativa: Plotly (Express & Graph Objects)

Interface Web: Streamlit

Estatística: Scipy, Statsmodels

📂 Estrutura do Projeto
Plaintext
├── app.ipynb              # Notebook com a análise exploratória completa (EDA)
├── dashboard.py           # Código fonte da aplicação Streamlit
├── pokemon_data.csv       # Dataset base com estatísticas e metadados
├── requirements.txt       # Dependências do projeto
└── README.md              # Documentação do projeto
📉 Insights Extraídos
Imunidade como Vantagem: Tipos com imunidades naturais (Ghost/Fairy) apresentam maior consistência defensiva na Matriz de Eficácia.

O Fator Speed: A análise de dispersão revela que o meta é dominado por Pokémon que ocupam os extremos: ou velocidade altíssima para controle, ou velocidade mínima para aproveitamento de Trick Room.

Power Creep: Existe uma tendência estatística de aumento de BST a partir da Geração 7, exigindo que Pokémon de gerações anteriores dependam de itens ou mecânicas externas para se manterem viáveis.

🔧 Como Executar
Clone o repositório:

Bash
git clone https://github.com/yGabrielV/Projeto-de-estat-stica_Analise_exploratoria_de_dados.git
Instale as dependências:

Bash
pip install -r requirements.txt
Execute o Dashboard:

Bash
streamlit run dashboard.py
Explore a Análise:
Abra o arquivo app.ipynb em seu editor favorito (VS Code, Jupyter Lab, Colab).

✒️ Autor
Gabriel Verbicaro da Ponte Souza - Aluno CESUPA 4° semestre de Ciencia da Computação
