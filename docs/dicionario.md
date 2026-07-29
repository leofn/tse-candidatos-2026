# Dicionário de Dados — Candidatos TSE 2026

## consulta_cand (Candidatos)

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| DT_GERACAO | data | Data de geração do arquivo |
| HH_GERACAO | hora | Hora de geração |
| ANO_ELEICAO | int | Ano da eleição |
| CD_TIPO_ELEICAO | int | Código do tipo de eleição |
| NM_TIPO_ELEICAO | string | Nome do tipo |
| NR_TURNO | int | Número do turno |
| CD_ELEICAO | int | Código da eleição |
| DS_ELEICAO | string | Descrição da eleição |
| DT_ELEICAO | data | Data da eleição |
| TP_ABRANGENCIA | string | Tipo de abrangência (ESTADUAL/FEDERAL) |
| SG_UF | string | Sigla da UF |
| SG_UE | string | Sigla da Unidade Eleitoral |
| NM_UE | string | Nome da Unidade Eleitoral (município/estado) |
| CD_CARGO | int | Código do cargo |
| DS_CARGO | string | Descrição do cargo |
| SQ_CANDIDATO | string | Sequencial único do candidato (chave) |
| NR_CANDIDATO | int | Número do candidato na urna |
| NM_CANDIDATO | string | Nome completo |
| NM_URNA_CANDIDATO | string | Nome de urna |
| NM_SOCIAL_CANDIDATO | string | Nome social |
| NR_CPF_CANDIDATO | string | CPF |
| DS_EMAIL | string | E-mail |
| CD_SITUACAO_CANDIDATURA | int | Código da situação |
| DS_SITUACAO_CANDIDATURA | string | Situação (DEFERIDO/INDEFERIDO/etc) |
| TP_AGREMIACAO | string | Tipo (PARTIDO ISOLADO/COLIGAÇÃO) |
| NR_PARTIDO | int | Número do partido |
| SG_PARTIDO | string | Sigla do partido |
| NM_PARTIDO | string | Nome do partido |
| NR_FEDERACAO | int | Número da federação |
| NM_FEDERACAO | string | Nome da federação |
| SG_FEDERACAO | string | Sigla da federação |
| DS_COMPOSICAO_FEDERACAO | string | Composição da federação |
| SQ_COLIGACAO | string | Sequencial da coligação |
| NM_COLIGACAO | string | Nome da coligação |
| DS_COMPOSICAO_COLIGACAO | string | Composição da coligação |
| SG_UF_NASCIMENTO | string | UF de nascimento |
| DT_NASCIMENTO | data | Data de nascimento |
| NR_TITULO_ELEITORAL | string | Título de eleitor |
| CD_GENERO | int | Código de gênero |
| DS_GENERO | string | Gênero (MASCULINO/FEMININO) |
| CD_GRAU_INSTRUCAO | int | Código de instrução |
| DS_GRAU_INSTRUCAO | string | Grau de instrução |
| CD_ESTADO_CIVIL | int | Código estado civil |
| DS_ESTADO_CIVIL | string | Estado civil |
| CD_COR_RACA | string | Código cor/raça |
| DS_COR_RACA | string | Cor/raça |
| CD_OCUPACAO | int | Código de ocupação |
| DS_OCUPACAO | string | Ocupação |
| CD_SIT_TOT_TURNO | int | Código situação totalização |
| DS_SIT_TOT_TURNO | string | Situação totalização |

## bem_candidato (Bens)

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| SQ_CANDIDATO | string | Chave do candidato |
| NR_ORDEM_BEM_CANDIDATO | int | Ordem do bem |
| CD_TIPO_BEM_CANDIDATO | int | Código do tipo |
| DS_TIPO_BEM_CANDIDATO | string | Descrição do tipo de bem |
| DS_BEM_CANDIDATO | string | Descrição detalhada |
| VR_BEM_CANDIDATO | string | Valor (formato brasileiro: "60000,00") |
| DT_ULT_ATUAL_BEM | data | Data de atualização |

## consulta_coligacao (Coligações)

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| SQ_COLIGACAO | string | Sequencial da coligação |
| NM_COLIGACAO | string | Nome |
| DS_COMPOSICAO_COLIGACAO | string | Composição |
| CD_SITUACAO_LEGENDA | string | Código situação |
| DS_SITUACAO | string | Situação |
| NM_TIPO_DESTINACAO_VOTOS | string | Tipo de destino dos votos |

## consulta_vagas (Vagas)

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| CD_CARGO | int | Código do cargo |
| DS_CARGO | string | Cargo |
| SG_UE | string | Unidade eleitoral |
| NM_UE | string | Nome da UE |
| QT_VAGAS | int | Quantidade de vagas |

## rede_social_candidato (Redes Sociais)

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| SQ_CANDIDATO | string | Chave do candidato |
| DS_URL | string | URL da rede social |
| DSrede_social | string | Tipo de rede social |

## motivo_cassacao (Cassação)

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| SQ_CANDIDATO | string | Chave do candidato |
| CD_MOTIVO_CASSACAO | int | Código do motivo |
| DS_MOTIVO_CASSACAO | string | Descrição do motivo |