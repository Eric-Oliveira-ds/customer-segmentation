import pandas as pd
import numpy as np
import joblib
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from sqlalchemy import create_engine, text
import sqlalchemy
import os
from dotenv import load_dotenv

# Autenticação

@st.cache_data
# Criar conexão com MySQL
def get_data():
    engine = create_engine('mysql+pymysql://admin:1234@localhost:3306/Bank_Credit_Card')
    query = 'SELECT * FROM customer_credit_card'
    df = pd.read_sql_query(sql=text(query), con=engine.connect())

    return df


def data_viz():
    # Obter os dados
    df = get_data()

    df_viz = df.set_index('CUST_ID')
    df_viz.drop(['CLUSTER_KMEANS_PCA'],axis=1, inplace=True)

    # Texto que explica a segmentação de cada cluster
    st.markdown(""" 
            #### Vip:
            Pagam legal as faturas e têm maior tempo no banco, além de terem o limite de crédito maior.
            #### Plus:
            Segundos melhores pagadores de fatura do cartão. 
            #### Mid:
            Menor limite de credito, mas ainda assim pagam as faturas em uma taxa mínima.
            #### Low:
            Taxa negativa de pagamento da fatura, clientes problemáticos.
            """)

    # Número de clientes segmentados por grupo
    fig = px.bar(df_viz['SEGMENTATION'].value_counts(), title="Número de clientes segmentados por grupo")
    fig.update_layout(xaxis_title="Segmentação", yaxis_title="Número de clientes")
    fig.update_layout(showlegend=False)
    # Renderização do gráfico
    st.plotly_chart(fig)


    # Gráfico polar de média das variáveis por cluster
    # Seletor de colunas
    selected_column = st.selectbox('Selecione a coluna para analisar o gráfico abaixo:', list(df_viz.columns))
    st.markdown(""" #### Visão de segmentação por média das variáveis:""")
    fig = make_subplots(rows=2, cols=2, subplot_titles=df['SEGMENTATION'].unique(), specs=[[{'type': 'polar'}]*2]*2)

    angles = list(df_viz.columns)
    layoutdict = dict(radialaxis=dict(visible=True, range=[0, 1]))

    row = 1
    col = 1
    colors = ['gold', 'green', 'blue', 'red']
    for i, segment in enumerate(df_viz['SEGMENTATION'].unique()):
        subset = df_viz[df_viz['SEGMENTATION'] == segment]
        data = [np.mean(subset[col]) for col in subset.columns[:-2]]
        data.append(data[0])
        
        fig.add_trace(go.Scatterpolar(
            r=data,
            theta=angles,
            mode = 'markers',
            fill='toself',
            name="Segmentation: " + segment,
            line=dict(color=colors[i])
        ), row=row, col=col)
        
        col += 1
        if col > 2:
            col = 1
            row += 1

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                tickfont=dict(size=6)  
            )
        ),
        showlegend=True,
        height=700,
        width=1100,
        template="plotly"
    )
    
    st.plotly_chart(fig)

    # Tabela Agggrid
    st.markdown(""" #### Amostras segmentadas - Use os filtros para obter insights !""")
    # Adiciona um seletor de quantidade de linhas
    num_rows = st.slider("Selecione o número de linhas", min_value=10, max_value=100, value=10, step=10)

    # Aplica filtros aleatórios ao DataFrame
    filtered_df = df.sample(n=num_rows, random_state=42)
    # Constrói as opções do Ag-Grid
    grid_options_builder = GridOptionsBuilder.from_dataframe(filtered_df)
    grid_options = grid_options_builder.build()

    # Renderiza o Ag-Grid
    with st.expander("Visualizar dados"):
        AgGrid(filtered_df, gridOptions=grid_options)







# Página principals
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

if __name__ == '__main__':
    main()
