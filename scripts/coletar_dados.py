#!/usr/bin/env python3
"""
Coletor de dados eleitorais do TSE — Eleições 2026
Baixa, descompacta e organiza todos os datasets de candidatos.

Uso:
    python3 coletar_dados.py [--ano 2026] [--output ./dados]

Fonte: https://dadosabertos.tse.jus.br/dataset/candidatos-2026
Licença: Creative Commons Atribuição (TSE/AGEL)
"""

import os
import sys
import zipfile
import urllib.request
import argparse
from datetime import datetime

# URLs de download direto (CDN TSE)
RECURSOS = {
    'candidatos': {
        'url': 'https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_cand/consulta_cand_{ano}.zip',
        'prefix': 'consulta_cand',
    },
    'info_complementares': {
        'url': 'https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_cand_complementar/consulta_cand_complementar_{ano}.zip',
        'prefix': 'consulta_cand_complementar',
    },
    'bens': {
        'url': 'https://cdn.tse.jus.br/estatistica/sead/odsele/bem_candidato/bem_candidato_{ano}.zip',
        'prefix': 'bem_candidato',
    },
    'coligacoes': {
        'url': 'https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_coligacao/consulta_coligacao_{ano}.zip',
        'prefix': 'consulta_coligacao',
    },
    'vagas': {
        'url': 'https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_vagas/consulta_vagas_{ano}.zip',
        'prefix': 'consulta_vagas',
    },
    'cassacao': {
        'url': 'https://cdn.tse.jus.br/estatistica/sead/odsele/motivo_cassacao/motivo_cassacao_{ano}.zip',
        'prefix': 'motivo_cassacao',
    },
    'redes_sociais': {
        'url': 'https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_cand/rede_social_candidato_{ano}.zip',
        'prefix': 'rede_social_candidato',
    },
}


def baixar(url, destino):
    """Baixa arquivo com progresso."""
    print(f"  Baixando: {url}")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        with open(destino, 'wb') as f:
            while True:
                chunk = resp.read(8192)
                if not chunk:
                    break
                f.write(chunk)
    tamanho = os.path.getsize(destino)
    print(f"  OK: {tamanho:,} bytes")


def descompactar(zip_path, output_dir):
    """Descompacta ZIP mantendo apenas CSVs."""
    with zipfile.ZipFile(zip_path) as z:
        for name in z.namelist():
            if name.endswith('.csv'):
                z.extract(name, output_dir)
                print(f"  Extraído: {name}")
            elif name.endswith('.pdf'):
                z.extract(name, output_dir)


def coletar(ano, output_dir):
    """Coleta todos os recursos do TSE para o ano especificado."""
    os.makedirs(output_dir, exist_ok=True)

    data_extracao = datetime.now().strftime('%Y-%m-%d')
    manifesto = {
        'ano': ano,
        'data_extracao': data_extracao,
        'fonte': 'TSE - Tribunal Superior Eleitoral',
        'url_fonte': f'https://dadosabertos.tse.jus.br/dataset/candidatos-{ano}',
        'licenca': 'Creative Commons Atribuição',
        'recursos': {},
    }

    for nome, info in RECURSOS.items():
        url = info['url'].format(ano=ano)
        zip_name = f"{info['prefix']}_{ano}.zip"
        zip_path = os.path.join(output_dir, zip_name)

        print(f"\n=== {nome.upper()} ===")
        try:
            baixar(url, zip_path)
            descompactar(zip_path, output_dir)

            # Listar CSVs extraídos
            csvs = [f for f in os.listdir(output_dir)
                    if f.startswith(info['prefix']) and f.endswith('.csv')]
            manifesto['recursos'][nome] = {
                'zip': zip_name,
                'csvs': sorted(csvs),
                'tamanho_zip': os.path.getsize(zip_path),
            }
        except Exception as e:
            print(f"  ERRO: {e}")
            manifesto['recursos'][nome] = {'erro': str(e)}

    # Salvar manifesto
    import json
    manifesto_path = os.path.join(output_dir, '_manifesto.json')
    with open(manifesto_path, 'w', encoding='utf-8') as f:
        json.dump(manifesto, f, ensure_ascii=False, indent=2)
    print(f"\nManifesto salvo: {manifesto_path}")
    print(f"Data de extração: {data_extracao}")

    return manifesto


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Coletor de dados eleitorais do TSE')
    parser.add_argument('--ano', type=int, default=2026, help='Ano da eleição')
    parser.add_argument('--output', type=str, default='./dados', help='Diretório de saída')
    args = parser.parse_args()

    coletar(args.ano, args.output)