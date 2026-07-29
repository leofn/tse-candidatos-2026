#!/usr/bin/env python3
"""
Gerador de gráficos e análises — Eleições 2026
Lê os CSVs do TSE e gera visualizações em PNG.

Uso:
    python3 gerar_graficos.py [--dados ./dados] [--output ./graficos]
"""

import csv
import os
import sys
import argparse
from collections import Counter, defaultdict
from datetime import datetime

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

sns.set_theme(style="whitegrid", font_scale=1.1)
plt.rcParams['figure.dpi'] = 150

# Paleta institucional
AZUL = '#1a3a5c'
DOURADO = '#c9a227'
VERMELHO = '#991b1b'
VERDE = '#166534'


def carregar_candidatos(dados_dir):
    """Carrega todos os candidatos do arquivo BRASIL."""
    path = os.path.join(dados_dir, 'consulta_cand_2026_BRASIL.csv')
    if not os.path.exists(path):
        # Tentar ano dinâmico
        for f in os.listdir(dados_dir):
            if f.startswith('consulta_cand_') and f.endswith('_BRASIL.csv'):
                path = os.path.join(dados_dir, f)
                break
    cands = []
    with open(path, encoding='latin-1') as f:
        for row in csv.DictReader(f, delimiter=';'):
            cands.append(row)
    print(f"Candidatos carregados: {len(cands)}")
    return cands


def carregar_bens(dados_dir):
    """Carrega bens de candidatos."""
    path = os.path.join(dados_dir, 'bem_candidato_2026_BRASIL.csv')
    if not os.path.exists(path):
        for f in os.listdir(dados_dir):
            if f.startswith('bem_candidato_') and f.endswith('_BRASIL.csv'):
                path = os.path.join(dados_dir, f)
                break
    bens = []
    with open(path, encoding='latin-1') as f:
        for row in csv.DictReader(f, delimiter=';'):
            try:
                val = float(row['VR_BEM_CANDIDATO'].replace(',', '.'))
            except:
                continue
            bens.append({
                'sq': row['SQ_CANDIDATO'],
                'tipo': row['DS_TIPO_BEM_CANDIDATO'][:60],
                'valor': val,
                'uf': row['SG_UF'],
                'municipio': row['NM_UE'],
            })
    print(f"Bens carregados: {len(bens)}")
    return bens


def gerar_todos(cands, bens, out_dir):
    os.makedirs(out_dir, exist_ok=True)

    # ---- 1. Candidatos por UF ----
    ufs = Counter(r['SG_UF'] for r in cands)
    ufs_s = dict(sorted(ufs.items(), key=lambda x: x[1], reverse=True))
    fig, ax = plt.subplots(figsize=(14, 7))
    colors = [AZUL if v >= 100 else DOURADO if v >= 50 else '#6b7280' for v in ufs_s.values()]
    bars = ax.bar(ufs_s.keys(), ufs_s.values(), color=colors, edgecolor='white')
    ax.set_title('Candidatos 2026 por Unidade Federativa', fontsize=18, fontweight='bold', color=AZUL, pad=15)
    ax.set_ylabel('Nº de candidatos', fontsize=12)
    for bar, v in zip(bars, ufs_s.values()):
        ax.text(bar.get_x() + bar.get_width()/2, v + 3, str(v), ha='center', va='bottom', fontsize=10, fontweight='bold')
    ax.set_ylim(0, max(ufs_s.values()) * 1.12)
    sns.despine()
    plt.tight_layout()
    plt.savefig(f'{out_dir}/01_candidatos_por_uf.png', bbox_inches='tight')
    plt.close()
    print("✓ 01_candidatos_por_uf.png")

    # ---- 2. Por Cargo ----
    cargos = Counter(r['DS_CARGO'] for r in cands)
    cargos_s = dict(sorted(cargos.items(), key=lambda x: x[1], reverse=True))
    fig, ax = plt.subplots(figsize=(10, 6))
    colors2 = [AZUL, DOURADO, VERDE, VERMELHO, '#6b7280', '#8b5cf6', '#ec4899', '#14b8a6'][:len(cargos_s)]
    bars = ax.barh(list(cargos_s.keys()), list(cargos_s.values()), color=colors2, edgecolor='white')
    ax.set_title('Candidatos 2026 por Cargo', fontsize=18, fontweight='bold', color=AZUL, pad=15)
    ax.set_xlabel('Nº de candidatos', fontsize=12)
    for bar, v in zip(bars, cargos_s.values()):
        ax.text(v + 5, bar.get_y() + bar.get_height()/2, str(v), va='center', fontsize=11, fontweight='bold')
    ax.set_xlim(0, max(cargos_s.values()) * 1.12)
    ax.invert_yaxis()
    sns.despine()
    plt.tight_layout()
    plt.savefig(f'{out_dir}/02_candidatos_por_cargo.png', bbox_inches='tight')
    plt.close()
    print("✓ 02_candidatos_por_cargo.png")

    # ---- 3. Gênero (pizza) ----
    generos = Counter(r['DS_GENERO'] for r in cands)
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(generos.values(), labels=generos.keys(), autopct='%1.1f%%',
           colors=[AZUL, DOURADO], startangle=90,
           textprops={'fontsize': 14, 'fontweight': 'bold'},
           wedgeprops={'edgecolor': 'white', 'linewidth': 2})
    ax.set_title('Candidatos 2026 por Gênero', fontsize=18, fontweight='bold', color=AZUL, pad=15)
    plt.tight_layout()
    plt.savefig(f'{out_dir}/03_candidatos_por_genero.png', bbox_inches='tight')
    plt.close()
    print("✓ 03_candidatos_por_genero.png")

    # ---- 4. Cor/Raça ----
    cores = Counter(r['DS_COR_RACA'] for r in cands)
    cores_s = dict(sorted(cores.items(), key=lambda x: x[1], reverse=True))
    fig, ax = plt.subplots(figsize=(10, 6))
    colors4 = [AZUL, DOURADO, '#8b5cf6', VERDE, '#ec4899'][:len(cores_s)]
    bars = ax.barh(list(cores_s.keys()), list(cores_s.values()), color=colors4, edgecolor='white')
    ax.set_title('Candidatos 2026 por Cor/Raça', fontsize=18, fontweight='bold', color=AZUL, pad=15)
    ax.set_xlabel('Nº de candidatos', fontsize=12)
    for bar, v in zip(bars, cores_s.values()):
        ax.text(v + 5, bar.get_y() + bar.get_height()/2, str(v), va='center', fontsize=11, fontweight='bold')
    ax.set_xlim(0, max(cores_s.values()) * 1.12)
    ax.invert_yaxis()
    sns.despine()
    plt.tight_layout()
    plt.savefig(f'{out_dir}/04_candidatos_por_cor_raca.png', bbox_inches='tight')
    plt.close()
    print("✓ 04_candidatos_por_cor_raca.png")

    # ---- 5. Top 15 Partidos ----
    partidos = Counter(r['SG_PARTIDO'] for r in cands)
    partidos_s = dict(sorted(partidos.items(), key=lambda x: x[1], reverse=True)[:15])
    fig, ax = plt.subplots(figsize=(12, 8))
    colors5 = sns.color_palette("RdYlBu_r", len(partidos_s))
    bars = ax.barh(list(partidos_s.keys()), list(partidos_s.values()), color=colors5, edgecolor='white')
    ax.set_title('Top 15 Partidos por Nº de Candidatos (2026)', fontsize=18, fontweight='bold', color=AZUL, pad=15)
    ax.set_xlabel('Nº de candidatos', fontsize=12)
    for bar, v in zip(bars, partidos_s.values()):
        ax.text(v + 3, bar.get_y() + bar.get_height()/2, str(v), va='center', fontsize=10, fontweight='bold')
    ax.set_xlim(0, max(partidos_s.values()) * 1.12)
    ax.invert_yaxis()
    sns.despine()
    plt.tight_layout()
    plt.savefig(f'{out_dir}/05_candidatos_por_partido.png', bbox_inches='tight')
    plt.close()
    print("✓ 05_candidatos_por_partido.png")

    # ---- 6. Gênero por Cargo ----
    cargos_list = ['DEPUTADO FEDERAL', 'DEPUTADO ESTADUAL', 'DEPUTADO DISTRITAL', 'SENADOR', 'GOVERNADOR', 'VICE-GOVERNADOR']
    fig, ax = plt.subplots(figsize=(12, 6))
    x = range(len(cargos_list))
    masc = [sum(1 for r in cands if r['DS_CARGO'] == c and r['DS_GENERO'] == 'MASCULINO') for c in cargos_list]
    fem = [sum(1 for r in cands if r['DS_CARGO'] == c and r['DS_GENERO'] == 'FEMININO') for c in cargos_list]
    ax.bar([i - 0.2 for i in x], masc, 0.4, label='Masculino', color=AZUL, edgecolor='white')
    ax.bar([i + 0.2 for i in x], fem, 0.4, label='Feminino', color=DOURADO, edgecolor='white')
    ax.set_xticks(list(x))
    ax.set_xticklabels([c.replace('DEPUTADO ', 'DEP. ').title() for c in cargos_list], rotation=15, ha='right')
    ax.set_title('Candidatos 2026 por Gênero e Cargo', fontsize=18, fontweight='bold', color=AZUL, pad=15)
    ax.set_ylabel('Nº de candidatos', fontsize=12)
    ax.legend(fontsize=12)
    for i, (m, f) in enumerate(zip(masc, fem)):
        ax.text(i - 0.2, m + 3, str(m), ha='center', fontsize=10, fontweight='bold')
        ax.text(i + 0.2, f + 3, str(f), ha='center', fontsize=10, fontweight='bold')
    sns.despine()
    plt.tight_layout()
    plt.savefig(f'{out_dir}/06_genero_por_cargo.png', bbox_inches='tight')
    plt.close()
    print("✓ 06_genero_por_cargo.png")

    # ---- 7. Bens por Tipo (top 10) ----
    tipos_bem = defaultdict(float)
    for b in bens:
        tipos_bem[b['tipo']] += b['valor']
    top_bens = dict(sorted(tipos_bem.items(), key=lambda x: x[1], reverse=True)[:10])
    fig, ax = plt.subplots(figsize=(14, 7))
    colors7 = sns.color_palette("YlOrRd_r", len(top_bens))
    bars = ax.barh(list(top_bens.keys()), [v/1e6 for v in top_bens.values()], color=colors7, edgecolor='white')
    ax.set_title('Top 10 Tipos de Bens por Valor Total (R$ milhões)', fontsize=18, fontweight='bold', color=AZUL, pad=15)
    ax.set_xlabel('Valor (R$ milhões)', fontsize=12)
    for bar, v in zip(bars, top_bens.values()):
        ax.text(v/1e6 + 0.5, bar.get_y() + bar.get_height()/2, f'R$ {v/1e6:.1f}M', va='center', fontsize=10, fontweight='bold')
    ax.invert_yaxis()
    sns.despine()
    plt.tight_layout()
    plt.savefig(f'{out_dir}/07_bens_por_tipo.png', bbox_inches='tight')
    plt.close()
    print("✓ 07_bens_por_tipo.png")

    # ---- 8. Faixa Etária ----
    def idade(dt_str):
        try:
            d, m, y = dt_str.split('/')
            return 2026 - int(y)
        except:
            return None
    idades = [idade(r['DT_NASCIMENTO']) for r in cands]
    idades = [i for i in idades if i and 18 <= i <= 100]
    faixas = {'18-29': 0, '30-39': 0, '40-49': 0, '50-59': 0, '60-69': 0, '70+': 0}
    for i in idades:
        if i < 30: faixas['18-29'] += 1
        elif i < 40: faixas['30-39'] += 1
        elif i < 50: faixas['40-49'] += 1
        elif i < 60: faixas['50-59'] += 1
        elif i < 70: faixas['60-69'] += 1
        else: faixas['70+'] += 1
    fig, ax = plt.subplots(figsize=(10, 6))
    colors8 = [AZUL, '#2d5a8a', DOURADO, '#e0bc4e', VERDE, '#8b5cf6']
    bars = ax.bar(faixas.keys(), faixas.values(), color=colors8, edgecolor='white')
    ax.set_title('Candidatos 2026 por Faixa Etária', fontsize=18, fontweight='bold', color=AZUL, pad=15)
    ax.set_ylabel('Nº de candidatos', fontsize=12)
    for bar, v in zip(bars, faixas.values()):
        ax.text(bar.get_x() + bar.get_width()/2, v + 3, str(v), ha='center', va='bottom', fontsize=12, fontweight='bold')
    ax.set_ylim(0, max(faixas.values()) * 1.12)
    sns.despine()
    plt.tight_layout()
    plt.savefig(f'{out_dir}/08_candidatos_por_faixa_etaria.png', bbox_inches='tight')
    plt.close()
    print("✓ 08_candidatos_por_faixa_etaria.png")

    # ---- 9. Grau de Instrução ----
    instr = Counter(r['DS_GRAU_INSTRUCAO'] for r in cands)
    instr_s = dict(sorted(instr.items(), key=lambda x: x[1], reverse=True))
    fig, ax = plt.subplots(figsize=(12, 6))
    colors9 = sns.color_palette("Blues_r", len(instr_s))
    bars = ax.barh(list(instr_s.keys()), list(instr_s.values()), color=colors9, edgecolor='white')
    ax.set_title('Candidatos 2026 por Grau de Instrução', fontsize=18, fontweight='bold', color=AZUL, pad=15)
    ax.set_xlabel('Nº de candidatos', fontsize=12)
    for bar, v in zip(bars, instr_s.values()):
        ax.text(v + 3, bar.get_y() + bar.get_height()/2, str(v), va='center', fontsize=11, fontweight='bold')
    ax.invert_yaxis()
    sns.despine()
    plt.tight_layout()
    plt.savefig(f'{out_dir}/09_grau_instrucao.png', bbox_inches='tight')
    plt.close()
    print("✓ 09_grau_instrucao.png")

    # ====== RIQUEZA ======

    # Cruzar bens com candidatos
    cands_dict = {r['SQ_CANDIDATO']: r for r in cands}
    patri = defaultdict(lambda: {'total': 0.0, 'bens': 0, 'uf': '', 'municipio': '', 'nome': '', 'urna': '', 'cargo': '', 'partido': ''})
    for b in bens:
        sq = b['sq']
        patri[sq]['total'] += b['valor']
        patri[sq]['bens'] += 1
        patri[sq]['uf'] = b['uf']
        patri[sq]['municipio'] = b['municipio']
        if sq in cands_dict:
            c = cands_dict[sq]
            patri[sq]['nome'] = c['NM_CANDIDATO']
            patri[sq]['urna'] = c['NM_URNA_CANDIDATO']
            patri[sq]['cargo'] = c['DS_CARGO']
            patri[sq]['partido'] = c['SG_PARTIDO']
        else:
            patri[sq]['nome'] = f'Candidato {sq}'
            patri[sq]['urna'] = '?'
            patri[sq]['cargo'] = '?'
            patri[sq]['partido'] = '?'

    # ---- 10. Top 20 mais ricos Brasil ----
    top20 = sorted(patri.values(), key=lambda x: x['total'], reverse=True)[:20]
    fig, ax = plt.subplots(figsize=(14, 10))
    nomes = [f"{c['urna']} ({c['partido']}/{c['uf']})"[:45] for c in top20]
    vals = [c['total']/1e6 for c in top20]
    colors = sns.color_palette("YlOrRd_r", len(top20))
    bars = ax.barh(nomes, vals, color=colors, edgecolor='white')
    ax.set_title('Top 20 Candidatos Mais Ricos — Eleições 2026', fontsize=18, fontweight='bold', color=AZUL, pad=15)
    ax.set_xlabel('Patrimonio declarado (R$ milhoes)', fontsize=12)
    for bar, v in zip(bars, vals):
        ax.text(v + max(vals)*0.01, bar.get_y() + bar.get_height()/2, f'R$ {v:.1f}M', va='center', fontsize=10, fontweight='bold')
    ax.invert_yaxis()
    sns.despine()
    plt.tight_layout()
    plt.savefig(f'{out_dir}/10_top20_mais_ricos_brasil.png', bbox_inches='tight')
    plt.close()
    print("✓ 10_top20_mais_ricos_brasil.png")

    # ---- 11. Top 5 mais ricos por UF (9 UFs com mais patrimonio) ----
    por_uf = defaultdict(list)
    for sq, p in patri.items():
        if p['uf']:
            por_uf[p['uf']].append(p)
    ufs_top = sorted(por_uf.keys(), key=lambda u: sum(c['total'] for c in por_uf[u]), reverse=True)[:9]
    fig, axes = plt.subplots(3, 3, figsize=(20, 18))
    axes = axes.flatten()
    for i, uf in enumerate(ufs_top):
        ax = axes[i]
        top5 = sorted(por_uf[uf], key=lambda x: x['total'], reverse=True)[:5]
        nomes = [f"{c['urna']} ({c['partido']})"[:30] for c in top5]
        vals = [c['total']/1e6 for c in top5]
        colors = sns.color_palette("Blues_r", len(top5))
        bars = ax.barh(nomes, vals, color=colors, edgecolor='white')
        ax.set_title(f'{uf}', fontsize=14, fontweight='bold', color=AZUL)
        ax.set_xlabel('R$ milhoes', fontsize=10)
        for bar, v in zip(bars, vals):
            ax.text(v + max(vals)*0.02 if vals else 0, bar.get_y() + bar.get_height()/2, f'R$ {v:.1f}M', va='center', fontsize=9, fontweight='bold')
        ax.invert_yaxis()
        sns.despine()
    fig.suptitle('Top 5 Candidatos Mais Ricos por Estado — 2026', fontsize=20, fontweight='bold', color=AZUL, y=1.01)
    plt.tight_layout()
    plt.savefig(f'{out_dir}/11_top5_ricos_por_uf.png', bbox_inches='tight')
    plt.close()
    print("✓ 11_top5_ricos_por_uf.png")

    # ---- 12. Patrimônio total por UF ----
    uf_total = {uf: sum(c['total'] for c in cs) for uf, cs in por_uf.items()}
    uf_total_s = dict(sorted(uf_total.items(), key=lambda x: x[1], reverse=True))
    fig, ax = plt.subplots(figsize=(14, 7))
    colors3 = [AZUL if v >= 100e6 else DOURADO if v >= 10e6 else '#6b7280' for v in uf_total_s.values()]
    bars = ax.bar(uf_total_s.keys(), [v/1e6 for v in uf_total_s.values()], color=colors3, edgecolor='white')
    ax.set_title('Patrimonio Total Declarado por UF — 2026', fontsize=18, fontweight='bold', color=AZUL, pad=15)
    ax.set_ylabel('R$ milhoes', fontsize=12)
    for bar, v in zip(bars, uf_total_s.values()):
        ax.text(bar.get_x() + bar.get_width()/2, v/1e6 + max(uf_total_s.values())/1e6 * 0.01, f'{v/1e6:.1f}M', ha='center', va='bottom', fontsize=9, fontweight='bold')
    sns.despine()
    plt.tight_layout()
    plt.savefig(f'{out_dir}/12_patrimonio_total_por_uf.png', bbox_inches='tight')
    plt.close()
    print("✓ 12_patrimonio_total_por_uf.png")

    # ---- 13. Patrimônio médio por candidato por UF ----
    uf_media = {uf: sum(c['total'] for c in cs)/len(cs) for uf, cs in por_uf.items() if cs}
    uf_media_s = dict(sorted(uf_media.items(), key=lambda x: x[1], reverse=True))
    fig, ax = plt.subplots(figsize=(14, 7))
    colors4 = [DOURADO if v >= 1e6 else AZUL if v >= 500e3 else '#6b7280' for v in uf_media_s.values()]
    bars = ax.bar(uf_media_s.keys(), [v/1e3 for v in uf_media_s.values()], color=colors4, edgecolor='white')
    ax.set_title('Patrimonio Medio por Candidato por UF — 2026', fontsize=18, fontweight='bold', color=AZUL, pad=15)
    ax.set_ylabel('R$ mil', fontsize=12)
    for bar, v in zip(bars, uf_media_s.values()):
        ax.text(bar.get_x() + bar.get_width()/2, v/1e3 + max(uf_media_s.values())/1e3 * 0.01, f'R$ {v/1e3:.0f}k', ha='center', va='bottom', fontsize=9, fontweight='bold')
    sns.despine()
    plt.tight_layout()
    plt.savefig(f'{out_dir}/13_patrimonio_medio_por_uf.png', bbox_inches='tight')
    plt.close()
    print("✓ 13_patrimonio_medio_por_uf.png")

    # ---- 14. Top 20 municípios por patrimônio ----
    por_mun = defaultdict(list)
    for sq, p in patri.items():
        if p['municipio']:
            por_mun[p['municipio']].append(p)
    mun_total = {m: sum(c['total'] for c in cs) for m, cs in por_mun.items()}
    mun_top20 = dict(sorted(mun_total.items(), key=lambda x: x[1], reverse=True)[:20])
    fig, ax = plt.subplots(figsize=(14, 10))
    colors5 = sns.color_palette("YlGnBu_r", len(mun_top20))
    bars = ax.barh(list(mun_top20.keys()), [v/1e6 for v in mun_top20.values()], color=colors5, edgecolor='white')
    ax.set_title('Top 20 Municipios/Zonas por Patrimonio Declarado — 2026', fontsize=18, fontweight='bold', color=AZUL, pad=15)
    ax.set_xlabel('R$ milhoes', fontsize=12)
    for bar, v in zip(bars, mun_top20.values()):
        ax.text(v/1e6 + max(mun_total.values())/1e6 * 0.01, bar.get_y() + bar.get_height()/2, f'R$ {v/1e6:.1f}M', va='center', fontsize=10, fontweight='bold')
    ax.invert_yaxis()
    sns.despine()
    plt.tight_layout()
    plt.savefig(f'{out_dir}/14_top20_municipios_patrimonio.png', bbox_inches='tight')
    plt.close()
    print("✓ 14_top20_municipios_patrimonio.png")

    # ---- 15. Top 10 mais ricos por cargo ----
    cargos_principais = ['GOVERNADOR', 'DEPUTADO FEDERAL', 'DEPUTADO ESTADUAL', 'SENADOR']
    fig, axes = plt.subplots(2, 2, figsize=(18, 14))
    axes = axes.flatten()
    for i, cargo in enumerate(cargos_principais):
        ax = axes[i]
        top10 = sorted([p for p in patri.values() if p['cargo'] == cargo], key=lambda x: x['total'], reverse=True)[:10]
        if not top10:
            ax.set_title(f'{cargo} — sem dados', fontsize=14)
            continue
        nomes = [f"{c['urna']} ({c['partido']}/{c['uf']})"[:35] for c in top10]
        vals = [c['total']/1e6 for c in top10]
        colors = sns.color_palette("YlOrRd_r", len(top10))
        bars = ax.barh(nomes, vals, color=colors, edgecolor='white')
        ax.set_title(f'{cargo}', fontsize=14, fontweight='bold', color=AZUL)
        ax.set_xlabel('R$ milhoes', fontsize=10)
        for bar, v in zip(bars, vals):
            ax.text(v + max(vals)*0.02, bar.get_y() + bar.get_height()/2, f'R$ {v:.1f}M', va='center', fontsize=9, fontweight='bold')
        ax.invert_yaxis()
        sns.despine()
    fig.suptitle('Top 10 Candidatos Mais Ricos por Cargo — 2026', fontsize=20, fontweight='bold', color=AZUL, y=1.01)
    plt.tight_layout()
    plt.savefig(f'{out_dir}/15_top10_ricos_por_cargo.png', bbox_inches='tight')
    plt.close()
    print("✓ 15_top10_ricos_por_cargo.png")

    print(f"\n=== {len(os.listdir(out_dir))} graficos gerados em {out_dir} ===")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Gerador de graficos eleitorais')
    parser.add_argument('--dados', type=str, default='./dados', help='Diretorio dos dados')
    parser.add_argument('--output', type=str, default='./graficos', help='Diretorio de saida')
    args = parser.parse_args()

    cands = carregar_candidatos(args.dados)
    bens = carregar_bens(args.dados)
    gerar_todos(cands, bens, args.output)