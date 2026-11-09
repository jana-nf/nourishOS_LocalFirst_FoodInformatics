# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "kagglehub==1.0.3",
# ]
# ///

import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium", auto_download=["html"])


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🥗 NourishOS: Sistema de Informática Alimentar & Bioatividade (Local-First)

    > *"A alimentação deixa de ser interpretada apenas por cultura ou tradição e passa a ser decodificada como um sistema informacional complexo."*

    O **NourishOS** é um sistema de bioinformática e engenharia de dados de ponta a ponta inspirado em iniciativas globais como a **Forager AI (Brightseed)**, o **FooDB** e a **Plant Molecular Taste Database**. O projeto rompe com a visão tradicional da nutrição de macronutrientes, tratando ingredientes como registros estruturados, moléculas como chaves e efeitos biológicos como campos de consulta.

    ---

    ### 🏗️ Pilares da Arquitetura Tecnológica
    * **🧠 DuckDB (OLAP):** Ingestão automatizada e cruzamento relacional de massas de dados moleculares em milissegundos.
    * **🕸️ NetworkX & Plotly:** Mapeamento e visualização interativa da rede de conexões entre alimentos, compostos e classes químicas.
    * **🤖 ChromaDB + ONNX (IA Vetorial):** Indexação semântica local para consultas baseadas em significado e contexto biológico.
    * **⚡ Marimo (Reactive UI):** Painel web dinâmico com filtros em tempo real, indicadores executivos (KPIs) e exportação de dados.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    📦Importação de Bibliotecas
    """)
    return


@app.cell
def _():
    import duckdb
    import pandas as pd
    import networkx as nx
    import chromadb
    import plotly.express as px

    return duckdb, nx, pd, px


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Arquivos CSV
    """)
    return


@app.cell
def _():
    import kagglehub

    # Download latest version
    path = kagglehub.dataset_download("faresboudelaa/foodb-food-database")

    print("Path to dataset files:", path)
    return (path,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    🗄️Banco Analítico (DuckDB)
    """)
    return


@app.cell
def _(duckdb, path):
    import os
    import glob

    print("📂 Pasta base do Kaggle Hub:", path)

    # Lista todos os arquivos CSV disponíveis na pasta
    all_csvs = glob.glob(os.path.join(path, "**", "*.csv"), recursive=True)
    print("📋 Arquivos CSV disponíveis:", [os.path.basename(f) for f in all_csvs])

    # Função de busca totalmente insensível a maiúsculas/minúsculas (case-insensitive)
    def encontrar_arquivo_flexivel(nome_desejado):
        for caminho in all_csvs:
            if os.path.basename(caminho).lower() == nome_desejado.lower():
                return caminho
        return None

    # Busca pelos arquivos oficiais do FooDB (Food.csv, Compound.csv, Content.csv)
    path_food = encontrar_arquivo_flexivel("food.csv")
    path_compound = encontrar_arquivo_flexivel("compound.csv")
    path_content = encontrar_arquivo_flexivel("content.csv")

    print("✅ Caminho Food:", path_food)
    print("✅ Caminho Compound:", path_compound)
    print("✅ Caminho Content:", path_content)

    # Validação de segurança
    if not all([path_food, path_compound, path_content]):
        raise FileNotFoundError("⚠️ Um ou mais arquivos CSV não foram encontrados. Confira a listagem acima.")

    # Cria conexão in-memory com o DuckDB (recria para garantir estado limpo)
    conn = duckdb.connect()

    # Inspeciona as colunas reais de cada CSV para confirmar nomes exatos
    food_cols = conn.execute(f"SELECT column_name FROM (DESCRIBE SELECT * FROM '{path_food}')").fetchall()
    compound_cols = conn.execute(f"SELECT column_name FROM (DESCRIBE SELECT * FROM '{path_compound}')").fetchall()
    content_cols = conn.execute(f"SELECT column_name FROM (DESCRIBE SELECT * FROM '{path_content}')").fetchall()

    print("🔍 Colunas do Food.csv:", [c[0] for c in food_cols])
    print("🔍 Colunas do Compound.csv:", [c[0] for c in compound_cols])
    print("🔍 Colunas do Content.csv:", [c[0] for c in content_cols])

    # Mapeia colunas para lower-case para busca flexível de nomes reais
    food_cols_map = {c[0].lower(): c[0] for c in food_cols}
    compound_cols_map = {c[0].lower(): c[0] for c in compound_cols}

    # Encontra a coluna de grupo/categoria no Food.csv dinamicamente
    food_group_col = None
    for candidate in ["food_group", "group_name", "group", "category", "food_category"]:
        if candidate in food_cols_map:
            food_group_col = food_cols_map[candidate]
            break

    # Encontra a coluna de classe química no Compound.csv dinamicamente
    chem_class_col = None
    for candidate in ["chem_class", "chemical_class", "class", "compound_class"]:
        if candidate in compound_cols_map:
            chem_class_col = compound_cols_map[candidate]
            break

    print(f"🔧 Coluna de grupo do Food: {food_group_col}")
    print(f"🔧 Coluna de classe do Compound: {chem_class_col}")

    # Ingestão e cruzamento relacional analítico via DuckDB
    # No FooDB, Content.csv usa 'source_id' (não 'compound_id') e 'source_type' para ligar a Compound
    food_group_expr = f"COALESCE(f.\"{food_group_col}\", 'Outros')" if food_group_col else "'Outros'"
    chem_class_expr = f"COALESCE(c.\"{chem_class_col}\", 'Não Classificado')" if chem_class_col else "'Não Classificado'"

    conn.execute(f"""
        CREATE OR REPLACE TABLE clean_food_molecules AS 
        SELECT 
            f.name AS Alimento,
            {food_group_expr} AS Categoria_Alimento,
            c.name AS Composto_Bioativo,
            {chem_class_expr} AS Classe_Quimica,
            CAST(cf.orig_content AS DOUBLE) AS Concentracao,
            COALESCE(cf.orig_unit, 'mg/kg') AS Unidade
        FROM '{path_content}' AS cf
        JOIN '{path_food}' AS f ON cf.food_id = f.id
        JOIN '{path_compound}' AS c ON cf.source_id = c.id
        WHERE cf.orig_content IS NOT NULL 
          AND cf.orig_content > 0
          AND cf.source_type = 'Compound'
        LIMIT 1000;
    """)

    total_linhas = conn.execute("SELECT COUNT(*) FROM clean_food_molecules").fetchone()[0]
    print(f"🚀 Pipeline executado com sucesso! {total_linhas} registros reais carregados no DuckDB.")
    return (conn,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    🧬Modelagem do Grafo de Conhecimento (NetworkX)
    """)
    return


@app.cell
def _(conn, nx):
    # 1. Inicializa o Grafo Direcionado
    G = nx.DiGraph()

    # 2. Extrai os dados consolidados da tabela do DuckDB
    df_graph = conn.execute("""
        SELECT Alimento, Composto_Bioativo, Classe_Quimica, Concentracao, Unidade 
        FROM clean_food_molecules;
    """).df()

    # 3. Popula o grafo iterando sobre o DataFrame relacional
    for _, row in df_graph.iterrows():
        # Relação 1: Alimento -> Contém -> Composto Bioativo (com atributos de concentração)
        G.add_edge(
            row["Alimento"], 
            row["Composto_Bioativo"], 
            relacao="contem", 
            concentracao=row["Concentracao"], 
            unidade=row["Unidade"]
        )

        # Relação 2: Composto Bioativo -> Pertence a -> Classe Química
        G.add_edge(
            row["Composto_Bioativo"], 
            row["Classe_Quimica"], 
            relacao="pertence_a"
        )

    # 4. Métricas estruturais do grafo gerado
    print(f"🕸️ Grafo de Conhecimento construído com sucesso!")
    print(f"   • Total de nós (Alimentos, Compostos e Classes): {G.number_of_nodes():,}")
    print(f"   • Total de arestas (Conexões mapeadas): {G.number_of_edges():,}")
    return (G,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    🧠Indexação Vetorial (ChromaDB)
    """)
    return


@app.cell
def _(conn):
    def inicializar_chromadb():
        import chromadb

        # 1. Inicializa o cliente ChromaDB in-memory
        chroma_client = chromadb.Client()
        col = chroma_client.get_or_create_collection(name="nourishos_semantic_search")

        # 2. Extrai os dados diretamente do DuckDB
        df_chroma = conn.execute("""
            SELECT DISTINCT Alimento, Categoria_Alimento, Composto_Bioativo, Classe_Quimica, Concentracao, Unidade 
            FROM clean_food_molecules 
            LIMIT 200;
        """).df()

        documentos = []
        metadados = []
        ids = []

        # Usamos 'r' em vez de 'row' para evitar qualquer conflito de escopo
        for idx, r in df_chroma.iterrows():
            doc_text = (
                f"O alimento {r['Alimento']} (categoria: {r['Categoria_Alimento']}) "
                f"contém o composto bioativo {r['Composto_Bioativo']}, pertencente à classe química {r['Classe_Quimica']}, "
                f"com concentração de {r['Concentracao']} {r['Unidade']}."
            )
            documentos.append(doc_text)
    
            metadados.append({
                "alimento": str(r["Alimento"]),
                "composto": str(r["Composto_Bioativo"]),
                "classe": str(r["Classe_Quimica"]),
                "concentracao": float(r["Concentracao"]),
                "unidade": str(r["Unidade"])
            })
    
            ids.append(f"doc_{idx}")
    
        # 3. Adiciona os dados na coleção se estiver vazia
        if col.count() == 0 and documentos:
            col.add(
                documents=documentos,
                metadatas=metadados,
                ids=ids
            )
    
        return col

    # Executa a função e expõe apenas a variável limpa 'collection' para as próximas células
    collection = inicializar_chromadb()

    print(f"🧠 ChromaDB alimentado com sucesso!")
    print(f"   • Total de vetores indexados semanticamente: {collection.count():,}")
    return (collection,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    🖥️Interface de Busca Semântica (Marimo UI)
    """)
    return


@app.cell
def _(mo):
    # 1. Campo de texto reativo para a busca semântica
    search_input = mo.ui.text(
        value="composto antioxidante e anti-inflamatório", 
        label="🔍 Buscar no NourishOS por significado:",
        full_width=True
    )

    # Exibe o input na interface
    search_input
    return (search_input,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    📊Resultados Dinâmicos da IA
    """)
    return


@app.cell
def _(collection, mo, pd, search_input):
    # 1. Captura o texto digitado no componente de UI
    termo_busca = search_input.value

    # 2. Realiza a busca semântica vetorial no ChromaDB
    resultados_busca = collection.query(
        query_texts=[termo_busca],
        n_results=5
    )

    # 3. Organiza os resultados em um DataFrame do Pandas (usando o 'pd' já disponível no notebook)
    linhas_resultado = []
    if resultados_busca and resultados_busca.get('metadatas') and len(resultados_busca['metadatas']) > 0:
        for meta, doc in zip(resultados_busca['metadatas'][0], resultados_busca['documents'][0]):
            linhas_resultado.append({
                "Alimento": meta['alimento'],
                "Composto Bioativo": meta['composto'],
                "Classe Química": meta['classe'],
                "Concentração": f"{meta['concentracao']} {meta['unidade']}",
                "Contexto Semântico": doc
            })

    df_resultado_semantico = pd.DataFrame(linhas_resultado)

    # 4. Exibe a tabela interativa usando o Marimo
    mo.ui.table(df_resultado_semantico, pagination=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    📊Gráfico Interativo com Plotly
    """)
    return


@app.cell
def _(conn, px):
    # 1. Consulta dados agregados diretamente do DuckDB
    df_plot = conn.execute("""
        SELECT 
            Categoria_Alimento, 
            AVG(Concentracao) AS Media_Concentracao,
            COUNT(DISTINCT Alimento) AS Total_Alimentos
        FROM clean_food_molecules
        GROUP BY Categoria_Alimento
        ORDER BY Media_Concentracao DESC
        LIMIT 10;
    """).df()

    # 2. Cria o gráfico de barras interativo com Plotly Express
    fig = px.bar(
        df_plot,
        x='Categoria_Alimento',
        y='Media_Concentracao',
        text_auto='.2f',
        title='📊 Concentração Média de Compostos Bioativos por Categoria de Alimento',
        labels={
            'Categoria_Alimento': 'Categoria do Alimento', 
            'Media_Concentracao': 'Concentração Média (mg/kg)'
        },
        color='Categoria_Alimento',
        template='plotly_dark'  # Combina perfeitamente com interfaces modernas
    )

    # 3. Ajustes de layout para melhor legibilidade
    fig.update_layout(
        xaxis_tickangle=-30,
        showlegend=False,
        margin=dict(t=50, b=50, l=50, r=50)
    )

    # 4. Exibe o gráfico interativo no Marimo
    fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    🛠️Controles Interativos (mo.ui)
    """)
    return


@app.cell
def _(conn, mo):
    # 1. Busca as categorias únicas diretamente do DuckDB para popular o Dropdown dinamicamente
    categorias_db = conn.execute("""
        SELECT DISTINCT Categoria_Alimento 
        FROM clean_food_molecules 
        ORDER BY Categoria_Alimento;
    """).fetchall()

    lista_categorias = ["Todas"] + [cat[0] for cat in categorias_db]

    # 2. Cria o Dropdown de Categoria
    dropdown_categoria = mo.ui.dropdown(
        options=lista_categorias,
        value="Todas",
        label="📂 **Categoria de Alimento:**"
    )

    # 3. Cria o Slider de Concentração Mínima
    slider_concentracao = mo.ui.slider(
        start=0.0,
        stop=500.0,
        step=5.0,
        value=0.0,
        label="🧪 **Concentração Mínima (mg/kg):**"
    )

    # 4. Organiza e exibe os controles verticalmente na interface
    mo.vstack([dropdown_categoria, slider_concentracao])
    return dropdown_categoria, slider_concentracao


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    📊Consulta e Exibição Reativa
    """)
    return


@app.cell
def _(conn, dropdown_categoria, mo, slider_concentracao):
    # 1. Captura os valores selecionados nos componentes de UI acima
    cat_escolhida = dropdown_categoria.value
    min_conc = slider_concentracao.value

    # 2. Constrói a query SQL dinamicamente com base nos filtros ativos
    if cat_escolhida == "Todas":
        query_dinamica = f"""
            SELECT Alimento, Categoria_Alimento, Composto_Bioativo, Classe_Quimica, Concentracao, Unidade
            FROM clean_food_molecules
            WHERE Concentracao >= {min_conc}
            ORDER BY Concentracao DESC
            LIMIT 100;
        """
    else:
        query_dinamica = f"""
            SELECT Alimento, Categoria_Alimento, Composto_Bioativo, Classe_Quimica, Concentracao, Unidade
            FROM clean_food_molecules
            WHERE Categoria_Alimento = '{cat_escolhida}'
              AND Concentracao >= {min_conc}
            ORDER BY Concentracao DESC
            LIMIT 100;
        """

    # 3. Executa a query no DuckDB
    df_filtrado = conn.execute(query_dinamica).df()

    # 4. Exibe métrica de resumo e a tabela interativa
    print(f"🔍 Filtro ativo: Categoria = '{cat_escolhida}' | Concentração mínima = {min_conc} mg/kg")
    print(f"📦 Total de registros encontrados: {len(df_filtrado):,}")

    mo.ui.table(df_filtrado, pagination=True)
    return (df_filtrado,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    🕸️Grafo de Conhecimento Interativo com Plotly
    """)
    return


@app.cell
def _(G, nx):
    # Gera o grafo de conhecimento interativo com Plotly
    # Usa o grafo G (NetworkX) já construído em célula anterior

    import plotly.graph_objects as go

    # 1. Calcula layout do grafo
    _pos = nx.spring_layout(G, seed=42, k=0.15)

    # 2. Extrai coordenadas das arestas (linhas entre os nós)
    _edge_x = []
    _edge_y = []
    for _edge in G.edges():
        _x0, _y0 = _pos[_edge[0]]
        _x1, _y1 = _pos[_edge[1]]
        _edge_x.extend([_x0, _x1, None])
        _edge_y.extend([_y0, _y1, None])

    _edge_trace = go.Scatter(
        x=_edge_x, y=_edge_y,
        line=dict(width=0.8, color='#888888'),
        hoverinfo='none',
        mode='lines'
    )

    # 3. Extrai coordenadas e metadados dos nós
    _node_x = []
    _node_y = []
    _node_text = []
    _node_color = []
    _node_size = []

    for _node in G.nodes():
        _x, _y = _pos[_node]
        _node_x.append(_x)
        _node_y.append(_y)
        _node_text.append(str(_node))
        _grau = G.degree(_node)
        _node_color.append(_grau)
        _node_size.append(10 + (_grau * 2))

    _node_trace = go.Scatter(
        x=_node_x, y=_node_y,
        mode='markers',
        hoverinfo='text',
        text=_node_text,
        marker=dict(
            showscale=True,
            colorscale='Viridis',
            reversescale=True,
            color=_node_color,
            size=_node_size,
            colorbar=dict(
                thickness=15,
                title='Grau de Conexões',
                xanchor='left'
            ),
            line_width=2,
            line_color='white'
        )
    )

    # 4. Monta a figura com nome único para evitar conflito
    fig_grafo_interativo = go.Figure(
        data=[_edge_trace, _node_trace],
        layout=go.Layout(
            title='Rede Bioativa Interativa - NourishOS (Alimentos & Compostos)',
            title_font_size=16,
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20, l=20, r=20, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )
    )

    fig_grafo_interativo
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    📊Adicionar os KPI Cards (Indicadores-Chave)
    """)
    return


@app.cell
def _(conn, mo):
    # 1. Calcula as métricas globais diretamente do DuckDB
    kpis = conn.execute("""
        SELECT 
            COUNT(DISTINCT Alimento) AS total_alimentos,
            COUNT(DISTINCT Composto_Bioativo) AS total_compostos,
            COUNT(DISTINCT Classe_Quimica) AS total_classes,
            ROUND(AVG(Concentracao), 2) AS media_concentracao
        FROM clean_food_molecules;
    """).df().iloc[0]

    # 2. Cria cartões estatísticos visuais usando o ecossistema do Marimo
    card_alimentos = mo.stat(
        value=f"{kpis['total_alimentos']:,}",
        label="🥗 Alimentos Catalogados"
    )
    card_compostos = mo.stat(
        value=f"{kpis['total_compostos']:,}",
        label="🧪 Compostos Bioativos"
    )
    card_classes = mo.stat(
        value=f"{kpis['total_classes']:,}",
        label="🧬 Classes Químicas"
    )
    card_media = mo.stat(
        value=f"{kpis['media_concentracao']} mg/kg",
        label="📊 Concentração Média"
    )

    # 3. Organiza os cartões lado a lado em um layout flexível e moderno
    mo.hstack([card_alimentos, card_compostos, card_classes, card_media], justify="space-around")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    📥Adicionar o Botão de Exportação de Dados
    """)
    return


@app.cell
def _(df_filtrado, mo):
    # 1. Converte o DataFrame filtrado atual para formato CSV em bytes
    csv_data = df_filtrado.to_csv(index=False).encode('utf-8')

    # 2. Cria o componente de download do Marimo (mo.download, não mo.ui.download)
    botao_download = mo.download(
        data=csv_data,
        filename="nourishos_dados_filtrados.csv",
        mimetype="text/csv",
        label="📥 Baixar Dados Filtrados (CSV)"
    )

    # 3. Exibe o botão na interface
    botao_download
    return


if __name__ == "__main__":
    app.run()
