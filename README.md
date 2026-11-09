# 🥑 NourishOS — Food Genome Architecture

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![DuckDB](https://img.shields.io/badge/DuckDB-Analytic%20Engine-FFF000.svg)](https://duckdb.org/)
[![NetworkX](https://img.shields.io/badge/NetworkX-Knowledge%20Graph-orange.svg)](https://networkx.org/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Search-7000FF.svg)](https://www.trychroma.com/)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **NourishOS** é um motor de recomendação e formulação alimentar preditiva que traduz intenções nutricionais e biológicas em prescrições moleculares e harmonização quimiossensorial de sabores (*flavor pairing*). 

O projeto une o conceito de **"Comida como Sistema Informacional"** (inspirado em ecossistemas como *FooDB*, *Plant Molecular Taste Database* e a plataforma *Forager AI* da Brightseed), operando sob uma arquitetura de dados poliglota **100% Open-Source, com Custo Zero de Infraestrutura e execução Serverless no Google Colab**.

---

## 📌 Sumário

- [Visão Geral & Contexto](#-visão-geral--contexto)
- [Arquitetura do Sistema](#-arquitetura-do-sistema)
- [Stack Tecnológica (Zero-Cost / Local-First)](#-stack-tecnológica-zero-cost--local-first)
- [Modelagem de Dados](#-modelagem-de-dados)
  - [1. Camada Relacional Analítica (DuckDB)](#1-camada-relacional-analítica-duckdb)
  - [2. Grafo de Conhecimento (NetworkX)](#2-grafo-de-conhecimento-networkx)
  - [3. Indexação Vetorial Semântica (ChromaDB)](#3-indexação-vetorial-semântica-chromadb)
- [Como Executar o Projeto](#-como-executar-o-projeto)
- [Casos de Uso e Exemplo de Saída](#-casos-de-uso-e-exemplo-de-saída)
- [Considerações Éticas e Governança](#-considerações-éticas-e-governança)
- [Licença](#-licença)

---

## 🥑 Visão Geral & Contexto

Historicamente, a nutrição e o desenvolvimento de produtos alimentícios (P&D) operam sob métricas genéricas (macronutrientes, calorias) e testes empíricos. No entanto, os alimentos contêm dezenas de milhares de **compostos bioativos e voláteis aromáticos** que determinam tanto o seu impacto biológico quanto a sua experiência sensorial.

O **NourishOS** aborda essa fronteira tratando os alimentos como conjuntos de **instruções moleculares**:

1. **Bioatividade:** Mapeamento de pequenas moléculas (ex: quercetina, licopeno, EGCG) e seus efeitos na fisiologia humana.

2. **Sensorialidade:** Indexação de perfis aromáticos e de sabor para evitar que dietas ou formulações funcionais percam a palatabilidade.

3. **Preditividade por IA:** Combinação de busca semântica em linguagem natural com navegação em grafos para recomendações precisas e sem alucinações.

---

## 🏗️ Arquitetura do Sistema

A arquitetura adota uma abordagem **Híbrida (Vector RAG + Knowledge Graph)**, garantindo flexibilidade na entrada de dados em linguagem natural e rigor estrutural na recuperação das moléculas.

```text
               [ ENTRADA DO USUÁRIO / P&D ]
         "Preciso de foco mental e ação antioxidante"
                             │
                             ▼
              ┌─────────────────────────────┐
              │   CHROMADB (Vector Search)  │
              │ Busca Semântica de Intenção │
              └──────────────┬──────────────┘
                             │
                             ▼ (Resultados Relevantes)
              ┌─────────────────────────────┐
              │  NETWORKX (Knowledge Graph) │
              │ Traversal: Alimento ->      │
              │ Molécula -> Efeito/Sensorial│
              └──────────────┬──────────────┘
                             │
                             ▼ (Validação Analítica)
              ┌─────────────────────────────┐
              │    DUCKDB (SQL Analytics)   │
              │ Validação de Concentração   │
              │ e Mapeamento do FooDB       │
              └──────────────┬──────────────┘
                             │
                             ▼
         [ SAÍDA: TABELA DE PRESCRIÇÃO MOLECULAR ]
````

🛠️ Stack Tecnológica (Zero-Cost / Local-First)

Para eliminar a necessidade de instâncias de nuvem pagas (como MongoDB Atlas) e containers pesados em ambiente local (como Docker), o projeto foi projetado utilizando bibliotecas de altíssima performance embutidas (in-process):

| Componente | Tecnologia | Papel no Sistema | Benefício Principal | Ambiente de Execução |
| :--- | :--- | :--- | :--- | :--- |
| **Infraestrutura / Execução** | Google Colab | Pipeline Serverless | Execução gratuita em nuvem, reprodutível com 1 clique. | Google Colab |
| **Banco Analítico (OLAP)** | DuckDB | Ingestão e agregação SQL do FooDB | Processamento vetorial em memória, sem servidor SQL externo. | Local / Google Colab |
| **Grafo de Conhecimento** | NetworkX | Modelagem das relações bioativas/sensoriais | Representação em memória leve e eficiente para navegação de rede. | Local / Google Colab |
| **Banco Vetorial** | ChromaDB | Busca por Embeddings em Linguagem Natural | Banco vetorial in-memory open-source, sem limites de chamadas de API. | Local / Google Colab |
| **Interface / API** | FastAPI | Exposição dos endpoints da Engine | Facilidade de integração com front-ends em React/Streamlit. | Local / Google Colab |

🧬 Modelagem de Dados

1. Camada Relacional Analítica (DuckDB)
Representa a estrutura limpa extraída do ecossistema FooDB, ligando os alimentos às suas concentrações moleculares:

SELECT 
    f.name AS Alimento,
    c.name AS Composto_Bioativo,
    c.class AS Classe_Quimica,
    c.primary_effect AS Efeito_Biologico,
    rc.concentration AS Concentracao_mg_kg
FROM raw_contents rc
JOIN raw_foods f ON rc.food_id = f.food_id
JOIN raw_compounds c ON rc.compound_id = c.compound_id;

2. Grafo de Conhecimento (NetworkX)

Mapeia a ontologia do alimento através de triplas conectadas:

(Alimento: Cacau) ──[CONTÉM {concentracao, perfil_sensorial}]──> (Molécula: Teobromina)
(Molécula: Teobromina) ──[ATIVA {classe_quimica}]──> (Efeito: Foco & Cognição)

3. Indexação Vetorial Semântica (ChromaDB)

Cada tripla é traduzida em um documento sintético para geração de embeddings, permitindo queries como "combate ao estresse oxidativo com aroma terroso".

🚀 Como Executar o Projeto

Você pode rodar este projeto diretamente no Google Colab sem instalar nada na sua máquina física.

Passo 1: Clone ou abra no Google Colab

Clique no botão Open in Colab no topo deste repositório ou abra um novo notebook.

Passo 2: Instale as dependências

!pip install duckdb chromadb networkx pandas sentence-transformers fastapi uvicorn -q

Passo 3: Execute o Script do Core Engine

import duckdb
import networkx as nx
import chromadb
import pandas as pd

# 1. Inicializa Conexões

conn = duckdb.connect("nourish_os.duckdb")

# 2. Carga dos Dados Simulados do FooDB

conn.execute("""
    CREATE OR REPLACE TABLE raw_foods AS SELECT * FROM (VALUES 
        (1, 'Tomate', 'Solanaceae'), (2, 'Cacau', 'Malvaceae'), 
        (3, 'Chá Verde', 'Theaceae'), (4, 'Cúrcuma', 'Zingiberaceae')
    ) AS t(food_id, name, family);

    CREATE OR REPLACE TABLE raw_compounds AS SELECT * FROM (VALUES 
        (101, 'Licopeno', 'Carotenoid', 'Anti-inflamatório'),
        (102, 'Teobromina', 'Alkaloid', 'Foco & Estímulo Cognitivo'),
        (103, 'EGCG', 'Flavanol', 'Neuroproteção'),
        (104, 'Curcumina', 'Polyphenol', 'Inibição Inflamatória (TNF-alfa)')
    ) AS t(compound_id, name, class, primary_effect);

    CREATE OR REPLACE TABLE raw_contents AS SELECT * FROM (VALUES 
        (1, 101, 3010.5), (2, 102, 24000.0), (3, 103, 70000.0), (4, 104, 31400.0)
    ) AS t(food_id, compound_id, concentration);
""")

# 3. Construção do Grafo no NetworkX

G = nx.DiGraph()

df_data = conn.execute("""
    SELECT f.name as food, c.name as molecule, c.class as chem_class, 
           c.primary_effect as effect, rc.concentration
    FROM raw_contents rc
    JOIN raw_foods f ON rc.food_id = f.food_id
    JOIN raw_compounds c ON rc.compound_id = c.compound_id
""").df()

for _, row in df_data.iterrows():
    G.add_edge(row['food'], row['molecule'], concentration=row['concentration'])
    G.add_edge(row['molecule'], row['effect'], chem_class=row['chem_class'])

# 4. Busca Vetorial no ChromaDB

chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection("nourishos")

for _, row in df_data.iterrows():
    doc = f"Alimento {row['food']} com {row['molecule']} para {row['effect']}."
    collection.upsert(documents=[doc], metadatas={"food": row['food']}, ids=[row['food']])

# 5. Execução de Recomendação Híbrida

def recomendar(query_usuario):
    res = collection.query(query_texts=[query_usuario], n_results=1)
    alimento_rec = res['metadatas'][0][0]['food']
    
    # Traversal no Grafo
    molecula = list(G.successors(alimento_rec))[0]
    efeito = list(G.successors(molecula))[0]
    
    return pd.DataFrame([{
        "Ingrediente": alimento_rec,
        "Molécula-Chave": molecula,
        "Efeito Biológico": efeito,
        "Concentração": f"{G[alimento_rec][molecula]['concentration']} mg/kg"
    }])

# Teste

display(recomendar("quero algo para aumentar a concentração mental"))

📈 Casos de Uso e Exemplo de Saída

Caso 1: Formulação de Produtos para P&D (B2B)

Substituição de ingredientes em escassez mantendo a mesma matriz bioativa e sensorial.

Caso 2: Nutrição de Precisão (B2C)

Geração de prescrições alimentares orientadas a biossensores e exames de biomarcadores.

Exemplo de Retorno do Motor Híbrido:

| Ingrediente | Molécula-Chave | Classe Química | Concentração | Perfil Sensorial | Mecanismo Fisiológico |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Cacau** | Teobromina | Alkaloid | 24000.0 mg/kg | Amargo profundo, amadeirado | Estímulo do Foco & Modulação Cognitiva |
| **Chá Verde** | EGCG | Flavanol | 70000.0 mg/kg | Herbáceo, adstringente | Neuroproteção & Ativação Metabólica |

⚖️ Considerações Éticas e Governança

Defesa contra Biopirataria: Protocolos de uso responsável de dados sobre a flora nativa, garantindo que o mapeamento de propriedades botânicas tradicionais respeite licenças de repartição de benefícios.

Privacidade de Dados Biométricos: Dados de biomarcadores e exames de saúde devem ser processados localmente ou anonimizados via Differential Privacy antes da consulta ao sistema.

Mitigação do Reducionismo Nutricional: A plataforma atua como uma ferramenta assistiva para nutricionistas e chefs, sem substituir os aspectos socioculturais e afetivos da alimentação.

📜 Licença

Este projeto está licenciado sob a Licença MIT — consulte o arquivo LICENSE para obter mais detalhes.

Desenvolvido por Janaína Nascimento Feitoza 

Linkedin: www.linkedin.com/in/janainanascimentofeitoza 

---

Este `README.md` serve como documentação de alto nível do seu repositório, deixando evidente seu domínio em **Engenharia de Dados**, **Arquitetura de IA Híbrida (Vector + Graph)** e **Visão Sistêmica de Negócios**.
