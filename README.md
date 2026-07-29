# 📊 Dados Eleitorais TSE — Candidatos 2026

Dados abertos dos candidatos das **Eleições Gerais Estaduais 2026**, coletados do [Portal de Dados Abertos do TSE](https://dadosabertos.tse.jus.br/dataset/candidatos-2026).

> ⚠️ **DADOS PRELIMINARES** — As eleições ocorrem em 04/10/2026. Estes dados são atualizados diariamente pelo TSE durante o período de candidaturas. Os números mudam conforme novas candidaturas são registradas, deferidas ou indeferidas.

## 📁 Estrutura

```
tse-candidatos-2026/
├── dados/                  # CSVs originais do TSE (por UF + BRASIL)
│   ├── consulta_cand_2026_*.csv
│   ├── bem_candidato_2026_*.csv
│   ├── consulta_coligacao_2026_*.csv
│   ├── consulta_vagas_2026_*.csv
│   ├── motivo_cassacao_2026_*.csv
│   ├── rede_social_candidato_2026_*.csv
│   ├── consulta_cand_complementar_2026_*.csv
│   └── _manifesto.json     # Metadados da extração
├── graficos/               # 15 gráficos em PNG
├── scripts/
│   ├── coletar_dados.py    # Baixa dados do TSE
│   └── gerar_graficos.py   # Gera todos os gráficos
├── docs/
│   └── dicionario.md       # Dicionário de dados (colunas)
└── README.md
```

## 📊 Gráficos disponíveis

### Demografia
1. `01_candidatos_por_uf.png` — Candidatos por UF
2. `02_candidatos_por_cargo.png` — Por cargo disputado
3. `03_candidatos_por_genero.png` — Por gênero (pizza)
4. `04_candidatos_por_cor_raca.png` — Por cor/raça
5. `05_candidatos_por_partido.png` — Top 15 partidos
6. `06_genero_por_cargo.png` — Gênero por cargo (barras agrupadas)
7. `07_bens_por_tipo.png` — Top 10 tipos de bens por valor
8. `08_candidatos_por_faixa_etaria.png` — Por faixa etária
9. `09_grau_instrucao.png` — Por grau de instrução

### Riqueza/Patrimônio
10. `10_top20_mais_ricos_brasil.png` — Top 20 mais ricos do Brasil
11. `11_top5_ricos_por_uf.png` — Top 5 mais ricos por estado (9 UFs)
12. `12_patrimonio_total_por_uf.png` — Patrimônio total por UF
13. `13_patrimonio_medio_por_uf.png` — Patrimônio médio por candidato por UF
14. `14_top20_municipios_patrimonio.png` — Top 20 municípios por patrimônio
15. `15_top10_ricos_por_cargo.png` — Top 10 mais ricos por cargo

## 🚀 Como usar

### Atualizar dados

```bash
python3 scripts/coletar_dados.py --ano 2026 --output ./dados
```

### Gerar gráficos

```bash
pip install matplotlib seaborn
python3 scripts/gerar_graficos.py --dados ./dados --output ./graficos
```

### Carregar dados em Python

```python
import pandas as pd

# Candidatos (Brasil inteiro)
df = pd.read_csv('dados/consulta_cand_2026_BRASIL.csv', sep=';', encoding='latin-1')

# Bens
bens = pd.read_csv('dados/bem_candidato_2026_BRASIL.csv', sep=';', encoding='latin-1')
bens['VR_BEM_CANDIDATO'] = bens['VR_BEM_CANDIDATO'].str.replace(',', '.').astype(float)

# Filtrar Pernambuco
pe = df[df['SG_UF'] == 'PE']
```

## 📋 Dados incluídos

| Dataset | Descrição |
|---------|-----------|
| Candidatos | Dados pessoais, cargo, partido, situação |
| Informações complementares | E-mail, website, dados adicionais |
| Bens de candidatos | Patrimônio declarado por candidato |
| Coligações | Composição de coligações por partido |
| Vagas | Vagas disponíveis por cargo/UF |
| Motivo de cassação | Motivos de cassação registrados |
| Redes sociais | Links de redes sociais dos candidatos |

## 📈 Resumo (extração de 28/07/2026)

- **1.387 candidatos** registrados
- **975 com bens declarados**
- **27 UFs** com candidatos
- **8 cargos** disputados (Governador, Vice, Senador, Dep. Federal, Dep. Estadual, Dep. Distrital, Suplentes)
- **Top 3 mais ricos:**
  1. Leonardo Melo (MDB/AC) — R$ 2.289M
  2. Antônio Adonis (PRD/MG) — R$ 1.005M
  3. Professora Kátia Paulino (PDT/AP) — R$ 780M

## 🔄 Atualização automática

O repositório pode ser atualizado via GitHub Actions. Veja `.github/workflows/atualizar-dados.yml`.

## 📄 Licença

Dados: **Creative Commons Atribuição** (TSE/AGEL)
Código: MIT

## 🔗 Fontes

- [Portal de Dados Abertos do TSE](https://dadosabertos.tse.jus.br)
- [Dataset Candidatos 2026](https://dadosabertos.tse.jus.br/dataset/candidatos-2026)
- CDN: `https://cdn.tse.jus.br/estatistica/sead/odsele/`