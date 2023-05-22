import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv

import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from sqlalchemy import create_engine, text
import sqlalchemy

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()
# Definir os padrões para as configurações do banco de dados
HOST = os.getenv('HOST')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
DATABASE = os.getenv('DATABASE')

# Configurar o Streamlit para o modo wide (largura total) por padrão
st.set_page_config(layout="wide")

@st.cache_data
# Criar conexão com MySQL
def get_data():

    ssl_args = {'ssl_ca': 'cacert-2023-01-10.pem'}
    engine = create_engine(f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:3306/{DATABASE}', connect_args=ssl_args)
    query = 'SELECT * FROM customer_credit_card'
    df = pd.read_sql_query(sql=text(query), con=engine.connect())

    return df

def data_viz():
    # Obter os dados
    df = get_data()

    # selecionar dataframe para visualização de dados
    df_viz = df.set_index('CUST_ID')
    df_viz.drop(['CLUSTER_KMEANS_PCA'],axis=1, inplace=True)

    # Número de clientes segmentados por grupo
    fig = px.bar(df_viz['SEGMENTATION'].value_counts(), title="Número de clientes segmentados por grupo")
    fig.update_layout(xaxis_title="Segmentação", yaxis_title="Número de clientes")
    fig.update_layout(showlegend=False)
    # Renderização do gráfico
    st.plotly_chart(fig)

    # Gráfico de média das variáveis por cluster
    st.markdown(""" #### Visão de segmentação por média das variáveis:""")
    # Seletor de colunas
    selected_columns = st.multiselect("Selecione as variáveis para analisar", df_viz.columns[:-1])
    # Filtra o DataFrame com base nas colunas selecionadas
    df_filtered = df_viz[selected_columns + ['SEGMENTATION']]

    fig = make_subplots(rows=2, cols=2, subplot_titles=df_filtered['SEGMENTATION'].unique(), specs=[[{'type': 'bar'}]*2]*2)
    layoutdict = dict(xaxis=dict(visible=False), yaxis=dict(visible=False))
    row = 1
    col = 1
    colors = ['gold', 'green', 'blue', 'red']
    for i, segment in enumerate(df_filtered['SEGMENTATION'].unique()):
        subset = df_filtered[df_filtered['SEGMENTATION'] == segment]
        data = [np.mean(subset[col]) for col in subset.columns[:-1]]

        fig.add_trace(go.Bar(
            x=selected_columns,
            y=data,
            name="Segmentation: " + segment,
            marker=dict(color=colors[i])
        ), row=row, col=col)

        col += 1
        if col > 2:
            col = 1
            row += 1

    fig.update_layout(
        showlegend=True,
        height=800,
        width=1400,
        template="plotly"
    )

    fig.update_layout(
        font=dict(size=10)
    )

    st.plotly_chart(fig)



    # Tabela Agggrid
    st.markdown(""" #### Base de dados dos clientes que têm cartão de crédito:""")
    # Renderiza o Ag-Grid
    with st.expander("Visualizar e aplicar filtros na tabela"):
        # Define a largura do contêiner da tabela
        st.write(
                f'<style>.st-aggrid-wrapper .stAgGrid > div, .st-aggrid-wrapper .stAgGrid > div .slick-header-columns, '
                f'.st-aggrid-wrapper .stAgGrid > div .slick-viewport {{"width": "100%"}}</style>',
                unsafe_allow_html=True
        )
        # Configurações do AgGrid
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)
        gridOptions = gb.build()
        # Função para aplicar os filtros no DataFrame
        def apply_filters(grid_df):
            filters = []
            for column in grid_df.columns:
                if column in grid_df.select_dtypes(include=["object"]).columns:
                    values = st.multiselect(f"Selecione os valores para '{column}'", grid_df[column].unique().tolist())
                    if values:
                        filters.append(grid_df[column].isin(values))
                else:
                    min_val = grid_df[column].min()
                    max_val = grid_df[column].max()
                    selected_range = st.slider(f"Selecione o intervalo para '{column}'", min_val, max_val, (min_val, max_val))
                    filters.append((grid_df[column] >= selected_range[0]) & (grid_df[column] <= selected_range[1]))
            
            if filters:
                return grid_df.loc[pd.concat(filters, axis=1).all(axis=1)]
            else:
                return grid_df

        # Cria o AgGridWidget com as configurações e os dados iniciais
        grid_response = AgGrid(
            df,
            gridOptions=gridOptions,
            width='100%',
            height='500px',
            enable_enterprise_modules=True,
            allow_unsafe_jscode=True
        )

        # Aplica os filtros e atualiza o grid quando o botão "Filtrar" for pressionado
        if 'event_type' in grid_response and grid_response['event_type'] == 'buttonClicked':
            filtered_df = apply_filters(grid_response['data'])
            grid_response = AgGrid(
                filtered_df,
                gridOptions=gridOptions,
                width='100%',
                height='500px',
                enable_enterprise_modules=True,
                allow_unsafe_jscode=True
            )



# Página principal
def main_page():
    st.title("Segmentação de clientes por uso do cartão de crédito")

    # Chamar a função de visualização de dados
    data_viz()


def main():

    # Definir as rotas
    routes = {"Página Principal": main_page}

    st.sidebar.title("Menu")
    page = st.sidebar.selectbox("Selecione uma página", list(routes.keys()), key="main_page")

    # Executar a página selecionada
    routes[page]()

    # Adicionar imagem na barra lateral
    image = "6155818.jpg"
    st.sidebar.image(image, caption='freepik', use_column_width=True)
    st.sidebar.markdown("---")
    st.sidebar.markdown("Autor: Eric Oliveira")
    st.sidebar.markdown("[LinkedIn](https://www.linkedin.com/in/eric-oliveira-ds/)")


if __name__ == '__main__':
    main()
