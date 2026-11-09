# 🥗 NourishOS: Local-First Food Informatics & Bioactivity System

> *"A alimentação deixa de ser interpretada apenas por cultura ou tradição e passa a ser decodificada como um sistema informacional complexo."*

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![DuckDB](https://img.shields.io/badge/DuckDB-OLAP-yellow?style=for-the-badge&logo=duckdb&logoColor=black)](https://duckdb.org/)
[![NetworkX](https://img.shields.io/badge/NetworkX-Graph_Analytics-orange?style=for-the-badge)](https://networkx.org/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_Search-purple?style=for-the-badge)](https://www.trychroma.com/)
[![Marimo](https://img.shields.io/badge/Marimo-Reactive_App-green?style=for-the-badge)](https://marimo.io/)

---

## 💡 A Tese do Projeto (Contexto)
Inspirado em iniciativas globais como a **Forager AI (Brightseed)**, o **FooDB** e a **Plant Molecular Taste Database**, o **NourishOS** aborda a premissa de que os alimentos não devem ser vistos apenas como macronutrientes, mas como conjuntos de instruções bioativas. O sistema trata ingredientes como registros, moléculas como chaves e efeitos biológicos como campos de consulta estruturados.

---

## 🏗️ Arquitetura e Pipeline Tecnológico
O sistema opera sob o paradigma *Local-First*, integrando engenharia de dados analítica, grafos de conhecimento e IA semântica em uma única aplicação web reativa:

```text
[ Kaggle Hub / FooDB ] 
       │ (Download Programático)
       ▼
[ DuckDB ] ──(Consultas OLAP & Agregações)──> [ KPIs & Modelagem Relacional ]
       │
       ├──> [ NetworkX ] (Rede de Conhecimento / Grafo Bioativo)
       │
       └──> [ ChromaDB + ONNX ] (Busca Vetorial Semântica por IA)
                     │
                     ▼
          [ Marimo Reactive UI ] (Dashboard + Plotly + Exportação CSV)
````

✨ Principais Funcionalidades

🧬 Genoma Químico em Tempo Real (KPI Cards): Métricas instantâneas de alimentos, compostos e classes químicas processadas em memória via DuckDB.

🔍 Busca Semântica por IA: Consulta a base de dados por significado e contexto (ex: "compostos anti-inflamatórios") utilizando embeddings locais com ChromaDB.

🕸️ Rede Bioativa Interativa: Grafo de conhecimento em Plotly/NetworkX mapeando conexões moleculares e identificando hubs químicos.

📊 Filtros Dinâmicos e Exportação: Controles reativos de categoria e concentração mínima com opção de exportação de dados em CSV.

