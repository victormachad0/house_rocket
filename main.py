import streamlit            as st
import pandas               as pd
import numpy                as np
import plotly.graph_objects as go
import plotly.express       as px
import folium
import geopandas

from PIL import Image
from folium.plugins   import MarkerCluster
from streamlit_folium import folium_static
from plotly.subplots  import make_subplots

#layout streamlit
st.set_page_config(page_title= 'House Rocket Project', layout='wide')

st.title("House Rocket Project")
#tabs
tab0, tab1, tab2, tab3 = st.tabs(['๐ Home', '๐ Visao Geral', '๐ Hipoteses', '๐ง Questoes de Negocios'])

#import data
@st.cache( allow_output_mutation=True )
def get_data(path):
    data = pd.read_csv(path)

    return data

@st.cache( allow_output_mutation=True )
def get_geofile( url ):
    geofile = geopandas.read_file( url )

    return geofile

def data_transform(data):

    # Transformation
    data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')
    data['bathrooms'] = data['bathrooms'].astype('int64')
    data['floors'] = data['floors'].astype('int64')

    # Drops
    data.dropna(axis = 0, inplace = True)

    data.drop_duplicates(subset=['id'], keep='first', inplace=True)

    data.loc[data['bedrooms'] == 33, 'bedrooms'] = 3

    data.drop(data.loc[data['bathrooms'] == 0].index, axis = 0, inplace = True)

    # New features
    data['reformado'] = data['yr_renovated'].apply(lambda x: 0 if x == 0 else 1)

    data['conditional_type'] = data['condition'].apply(lambda x: 'bad' if x <= 2 else
                                                                 'regular' if (x == 3) | (x == 4) else
                                                                 'good')

    data['year_month'] = pd.to_datetime(data['date']).dt.strftime('%Y-%m')

    data['month'] = pd.to_datetime(data['date']).dt.month


    data['sazonalidade'] = data['month'].apply(lambda x: 'spring' if (x >= 3) & (x <= 5) else
                                                         'summer' if (x >= 6) & (x <= 8) else
                                                         'autumn' if (x >= 9) & (x <= 11) else
                                                         'winter')

    data['view_type'] = data['view'].apply(lambda x: 'bad' if (x == 0) else
                                                     'regular' if (x == 1) | (x == 2) else
                                                     'good')

    data['menor_1955'] = data['yr_built'].apply(lambda x: 0 if x < 1955 else 1)

    data['porao'] = data['sqft_basement'].apply(lambda x: 'nรฃo' if x == 0 else 'sim')

    data['price_m2'] = data['price'] / data['sqft_lot']

    data['m2'] = data['sqft_lot'] / 10.764

    return data

def primeira_pagina():
    with tab0:
        st.image('./images/houses.png')


        st.info('Nota: Os dados utilizados nesse projeto sรฃo dados ficticios, porem a soluรงรฃo foi desenvolvida pensando em casos reais!')

        st.header("Conhecendo melhor a House Rocket")

        st.markdown("<p style='font-size:18px'>"
                    "A House Rocket รฉ uma empresa localizada em King County, Washington e tem como modelo de negรณcio "
                    "a compra e venda de imรณveis, sua prรญncipal estratรฉgia รฉ a compra de imรณveis com preรงos baixos para posteriormente realizar a venda destes por um preรงo maior."
                    "</p>", unsafe_allow_html=True)

        st.markdown("<p style='font-size:18px'>"
                    "Para auxiliar o time de negรณcios na tomada de decisรตes sobre a compra e venda dos imรณveis, iremos realizar uma analise sobre "
                    "os dados dos imรณveis a venda em King County, pois quanto maior a diferenรงa entre o preรงo de compra e o preรงo de venda, maior "
                    "o lucro da empresa e portanto maior sua receita."
                    "</p>", unsafe_allow_html=True)

        st.subheader("O projeto aborda duas principais questรตes de negรณcios:")

        st.markdown("<ul>"
                    "<li>"
                    "<p style='font-size:18px'>"
                    "Quais imรณveis a House Rocket deveria comprar e por qual preรงo?"
                    "</p>"
                    "</li>"
                    "</ul>", unsafe_allow_html=True)

        st.markdown("<ul>"
                    "<li>"
                    "<p style='font-size:18px'>"
                    "Uma vez comprado, qual o melhor momento para vende-los e por qual preรงo?"
                    "</p>"
                    "</li>"
                    "</ul>", unsafe_allow_html=True)


        st.subheader("Resultados financeiros obtidos:")

        values  = [['$179.537.408,00'], ['$33.658.210,00']]
        values2 = [['$209.320.208,00'], ['$29.782.800,00']]
        values3 = [['outono', 'primavera', 'verรฃo', 'inverno'],
                   ['$49.933.865,00', '$49.399.426,00', '$78.222.913,00', '$31.764.003,00']]

        #table 1
        c1, c2 = st.columns(2)

        table = go.Figure(data=[go.Table(
            columnorder=[1, 2],
            columnwidth=[100, 150],
            header=dict(
                values=[['<b>Gasto na compra dos imรณveis</b>'],
                        ['<b>Economizado</b>']],
                line_color='black',
                fill_color=['#F0F8FF'],
                align=['center', 'center'],
                font=dict(color='black', size=20),
                height=40
            ),
            cells=dict(
                values=values,
                line_color='darkslategray',
                fill=dict(color=['white']),
                align=['center', 'center'],
                font=dict(color=['black'], size=18),
                height=40))])

        table.update_layout(height=160, margin = dict(l=5, r=0, b=1, t=50),  title = 'Valor total gasto na compra dos imรณveis + economias', title_font_size = 25)
        c1.plotly_chart(table, use_container_width=True)

        #table 2
        c1, c2 = st.columns(2)

        table2 = go.Figure(data=[go.Table(
            columnorder=[1, 2],
            columnwidth=[100, 150],
            header=dict(
                values=[['<b>Adquirido na venda dos imรณveis</b>'],
                        ['<b>Lucro</b>']],
                line_color='black',
                fill_color=['#F0F8FF'],
                align=['center', 'center'],
                font=dict(color='black', size=20),
                height=40,
            ),
            cells=dict(
                values=values2,
                line_color='darkslategray',
                fill=dict(color=['white']),
                align=['center', 'center'],
                font=dict(color=['black'], size=18),
                height=40))])

        table2.update_layout(height=150, margin = dict(l=5, r=1, b=1, t=35), title = 'Valor total obtido na venda dos imรณveis + lucro obtido', title_font_size = 25)
        c1.plotly_chart(table2, use_container_width=True)


        #table 3
        c1,c2 = st.columns(2)

        table3 = go.Figure(data=[go.Table(
            columnwidth=[100, 150],
            header=dict(
                values=[['<b>Sazonalidade</b>'],
                        ['<b>Preรงo de venda</b>']],
                line_color='black',
                fill_color=['#F0F8FF'],
                align=['center', 'center'],
                font=dict(color='black', size=20),
                height=40
            ),
            cells=dict(
                values=values3,
                line_color='darkslategray',
                fill=dict(color=['white']),
                align=['center', 'center'],
                font=dict(color=['black'], size=18),
                height=40))])

        table3.update_layout(height=400, margin = dict(l=5, r=1, b=1, t=35),  title = 'Valor total de venda dos imรณveis por sazonalidade', title_font_size = 25)
        c1.plotly_chart(table3, use_container_width=True)

        return None

def segunda_pagina(data):
    with tab1:
        st.header('Visualizaรงรฃo dos dados')
        st.sidebar.header('Visรฃo Geral')

        # Data Overview
        f_attributes = st.sidebar.multiselect('Selecione a coluna', data.columns)

        f_zipcode = st.sidebar.multiselect('Insira o zipcode', data['zipcode'].unique())

        if (f_zipcode != []) & (f_attributes != []):
            data = data.loc[data['zipcode'].isin(f_zipcode), f_attributes]

        elif (f_zipcode != []) & (f_attributes == []):
            data = data.loc[data['zipcode'].isin(f_zipcode), :]

        elif (f_zipcode == []) & (f_attributes != []):
            data = data.loc[:, f_attributes]

        else:
            data = data.copy()



        st.dataframe(data, width=1344)

        c1, c2 = st.columns((1, 2.38))

        # Average Metrics
        df1 = data[['id', 'zipcode']].groupby('zipcode').count().reset_index()
        df2 = data[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
        df3 = data[['sqft_living', 'zipcode']].groupby('zipcode').mean().reset_index()
        df4 = data[['price_m2', 'zipcode']].groupby('zipcode').mean().reset_index()

        # Merge
        m1 = pd.merge(df1, df2, on='zipcode', how='inner')
        m2 = pd.merge(m1, df3, on='zipcode', how='inner')
        df = pd.merge(m2, df4, on='zipcode', how='inner')
        df.columns = ['zipcode', 'total_casas', 'preรงo', 'espaรงo interno', 'preรงo/m2']

        c1.header('Mรฉdias por regiรฃo')
        c1.dataframe(df, height=450)

        # Statistic Attributes
        num_attributes = data.select_dtypes(include=['int64', 'float64'])

        max_ = pd.DataFrame(num_attributes.apply(np.max))
        min_ = pd.DataFrame(num_attributes.apply(np.min))
        mean = pd.DataFrame(num_attributes.apply(np.mean))
        median = pd.DataFrame(num_attributes.apply(np.median))
        std = pd.DataFrame(num_attributes.apply(np.std))

        statistics_describe = pd.concat([max_, min_, mean, median, std], axis=1).reset_index()
        statistics_describe.columns = ['attributes', 'max', 'min', 'mean', 'median', 'std']

        c2.header('Estatisticas Descritivas')
        c2.dataframe(statistics_describe, height=450)


        # Column description
        fig_values = [['id', 'date', 'price', 'bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors', 'waterfront', 'view', 'conditions',
                       'grade', 'sqft_above', 'sqft_basement', 'yr_built', 'yr_renovated', 'zipcode', 'lat', 'long', 'sqft_living15', 'sqft_lot15'],


                      ['Identificaรงรฃo รบnica de cada imรณvel', 'Data em que o imรณvel foi vendido', 'Preรงo de venda do imรณvel', 'Quantidade de quartos', 'Quantidade de banheiros',
                       'Pรฉs quadrados do espaรงo interior do imรณvel', 'Pรฉs quadrados do espaรงo do terreno', 'Nรบmero de andares de cada imรณvel', 'Informa se o imรณvel possui vista para a agua',
                       'Um indice de 0 a 4 de quรฃo boa รฉ a vista do imรณvel', 'Um indice de 0 a 5 da condiรงรฃo em que o imรณvel se encontra',
                       'รndice de 1 a 13, onde 1-3 fica aquรฉm da construรงรฃo e design de edifรญcios, 7 tem um nรญvel mรฉdio de construรงรฃo e design e 11-13 tem um alto nรญvel de construรงรฃo e design.',
                       'Ano de construรงรฃo do imรณvel', 'Ano em que foi feita a รบltima reforma do imรณvel', 'รrea do codigo postal onde os imรณveis se localizam', 'Latitude', 'Longitude',
                       'Pรฉs quadrados do espaรงo habitacional interior para os 15 vizinhos mais prรณximos', 'Pรฉs quadrados dos lotes dos 15 vizinhos mais prรณximos', 'Sem traduรงรฃo', 'Sem traduรงรฃo']]


        with st.expander("Descriรงรฃo das colunas"):


            fig = go.Figure(data=[go.Table(
                columnwidth=[80, 400],
                header=dict(
                    values=[['<b>Nome</b>'],
                            ['<b>Significado</b>']],
                    line_color='black',
                    fill_color=['#F0F8FF'],
                    align=['left', 'left'],
                    font=dict(color='black', size=20),
                    height=40
                ),
                cells=dict(
                    values=fig_values,
                    line_color='darkslategray',
                    fill=dict(color=['white']),
                    align=['left', 'left'],
                    font=dict(color=['black'], size=18),
                    height=40))])

            fig.update_layout(width = 400, height=1000, margin=dict(l=5, r=5, b=1, t=35))
            st.plotly_chart(fig, use_container_width=True)

    return None

def terceira_pagina(data):
    with tab2:
        st.header('Validaรงรฃo de Hipoteses')

        # Agrupamento dos dados para gerar as hipoteses
        h1 = data[['waterfront', 'price']].groupby('waterfront').mean().reset_index()


        h2 = data[['menor_1955', 'price']].groupby('menor_1955').mean().reset_index()


        h3_bad = data.loc[data['conditional_type'] == 'bad', ['conditional_type', 'year_month', 'price']]
        h3_bad = h3_bad.groupby(['year_month', 'conditional_type']).sum().reset_index()

        h3_regular = data.loc[data['conditional_type'] == 'regular', ['conditional_type', 'year_month', 'price']]
        h3_regular = h3_regular.groupby(['year_month', 'conditional_type']).sum().reset_index()

        h3_good = data.loc[data['conditional_type'] == 'good', ['conditional_type', 'year_month', 'price']]
        h3_good = h3_good.groupby(['year_month', 'conditional_type']).sum().reset_index()


        h4 = data[['porao', 'sqft_lot']].groupby('porao').mean().reset_index()


        h5 = data[['view_type', 'price']].groupby('view_type').mean().sort_values('price', ascending=False).reset_index()


        h6 = data[['sazonalidade', 'price']].groupby('sazonalidade').sum().sort_values('price', ascending=False).reset_index()


        h7 = data[['reformado', 'price']].groupby('reformado').mean().reset_index()


        h8 = data[['sazonalidade', 'year_month', 'price']].groupby(['year_month', 'sazonalidade']).sum().reset_index()


        # Plots
        c1, c2 = st.columns(2)

        c1.subheader('H1: Imรณveis que possuem vista para รกgua sรฃo 30% mais caros, na mรฉdia')

        c1.markdown("<p style='font-size:18px'>"
                    "โ๏ธ<b>Hipotese confirmada:</b> Imรณveis com vista para o mar sรฃo atรฉ 220% mais caros na mรฉdia"
                    "</p>", unsafe_allow_html=True)

        fig1 = px.bar(h1,
                      x='waterfront',
                      y='price',
                      height= 600,
                      color = 'waterfront',
                      color_continuous_scale=['#DECBE4', '#CCEBC5'],
                      )

        fig1.update_layout(coloraxis_showscale=False,
                           xaxis_title="Vista para o mar",
                           yaxis_title="Preรงo",
                           font=dict(size= 15)
                           )

        c1.plotly_chart(fig1, use_container_width=True)



        c2.subheader('H2: Imรณveis com data de construรงรฃo menor que 1955 sรฃo 50% mais baratos, na mรฉdia')

        c2.markdown("<p style='font-size:18px'>"
                    "โ <b>Hipotese refutada:</b> Os imรณveis nรฃo apresentaram mudanรงa na diferenรงa de preรงo, sรฃo equiparรกveis"
                    "</p>", unsafe_allow_html=True)

        fig2 = px.bar(h2,
                      x='menor_1955',
                      y='price',
                      height= 600,
                      color='menor_1955',
                      color_continuous_scale=['#DECBE4', '#CCEBC5'])

        fig2.update_layout(coloraxis_showscale=False,
                           xaxis_title="Imรณveis construรญdos abaixo de 1955",
                           yaxis_title="Preรงo",
                           font=dict(size=15)
                           )

        c2.plotly_chart(fig2, use_container_width=True)


        st.subheader('H3: Independente da condiรงรฃo, os imรณveis valorizam cerca de 10% ao ano')

        st.markdown("<p style='font-size:18px'>"
                    "โ <b>Hipotese refutada:</b> Independente das condiรงรตes, todos os imรณveis apresentaram uma desvalorizaรงรฃo com"
                    "relaรงรฃo ao mesmo mรชs do ano anterior"
                    "</p>", unsafe_allow_html=True)

        fig3 = make_subplots(rows=3, cols=1,
                             specs=[[{}], [{}], [{}]],
                             print_grid=True,
                             subplot_titles=('Variaรงรฃo do preรงo de imรณveis com condiรงรตes ruins ao longo do ano',
                                             'Variaรงรฃo do preรงo de imรณveis com condiรงรตes regulares ao longo do ano',
                                             'Variaรงรฃo do preรงo de imรณveis com condiรงรตes boas ao longo do ano'))


        fig3.add_trace(go.Scatter(x=h3_bad['year_month'], y=h3_bad['price']), row=1, col=1)
        fig3.add_trace(go.Scatter(x=h3_regular['year_month'], y=h3_regular['price']), row=2, col=1)
        fig3.add_trace(go.Scatter(x=h3_good['year_month'], y=h3_good['price']), row=3, col=1)

        fig3.update_layout(showlegend = False, font=dict(size = 15), height = 1000)
        fig3.layout.annotations[0]["font"] = {'size': 20}
        fig3.layout.annotations[1]["font"] = {'size': 20}
        fig3.layout.annotations[2]["font"] = {'size': 20}


        st.plotly_chart(fig3, use_container_width=True)



        c4, c5 = st.columns(2)

        c4.subheader('H4: Imรณveis sem porรฃo possuem terrenos 40% maiores do que com porรฃo')

        c4.markdown("<p style='font-size:18px'>"
                    "โ <b>Hipotese refutada:</b> Imรณveis sem porรฃo possuem terreno atรฉ 22% maiores do que com porรฃo "
                    "</p>", unsafe_allow_html=True)

        fig4 = px.bar(h4,
                      x='porao',
                      y='sqft_lot',
                      height= 600,
                      color='porao',
                      color_discrete_sequence= ['#DECBE4', '#CCEBC5']
                      )

        fig4.update_layout(showlegend = False,
                           xaxis_title="Porรฃo",
                           yaxis_title="Tamanho do terreno",
                           font=dict(size=15)
                           )

        c4.plotly_chart(fig4, use_container_width=True)


        c5.subheader('H5: Imรณveis com vista regular sรฃo 30% mais baratos do que casas com vista boa')

        c5.markdown("<p style='font-size:18px'>"
                    "โ๏ธ<b>Hipotese confirmada:</b> Imรณveis com vista regular sรฃo atรฉ 45% mais baratos do que imรณveis com vista boa"
                    "</p>", unsafe_allow_html=True)

        fig5 = px.bar(h5,
                      x='view_type',
                      y='price',
                      height= 600,
                      color='view_type',
                      color_discrete_sequence= ['#DECBE4', '#CCEBC5', '#B3CDE3']
                      )

        fig5.update_layout(showlegend = False,
                           xaxis_title="Qualidade da vista do imรณvel",
                           yaxis_title="Preรงo",
                           font=dict(size=15)
                           )

        c5.plotly_chart(fig5, use_container_width=True)


        c6, c7 = st.columns(2)

        c6.subheader('H6: No verรฃo os imรณveis tem uma valorizaรงรฃo de 20% com relaรงรฃo a primavera')

        c6.markdown("<p style='font-size:18px'>"
                    "โ <b>Hipotese refutada:</b> Imรณveis no verรฃo tem uma queda nรฃo significativa de 3% com relaรงรฃo a primavera"
                    "</p>", unsafe_allow_html=True)

        fig6 = px.bar(h6,
                      x='sazonalidade',
                      y='price',
                      height= 600,
                      color='sazonalidade',
                      color_discrete_sequence= ['#DECBE4', '#CCEBC5', '#B3CDE3', '#E5D8BD']
                      )

        fig6.update_layout(showlegend = False,
                           xaxis_title="Estaรงรฃo do ano",
                           yaxis_title="Preรงo",
                           font=dict(size=15)
                           )

        c6.plotly_chart(fig6, use_container_width=True)

        c7.subheader('H7: Imรณveis nunca reformados sรฃo 20% mais baratos do que imรณveis jรก reformados')

        c7.markdown("<p style='font-size:18px'>"
                    "โ๏ธ<b>Hipotese confirmada:</b> Imรณveis que nunca foram reformados sรฃo atรฉ 43% mais baratos do que imรณveis jรก reformados"
                    "</p>", unsafe_allow_html=True)

        fig7 = px.bar(h7,
                      x='reformado',
                      y='price',
                      height= 600,
                      color='reformado',
                      color_continuous_scale=['#DECBE4', '#CCEBC5'])

        fig7.update_layout(coloraxis_showscale=False,
                           xaxis_title="Reformado",
                           yaxis_title="Preรงo",
                           font=dict(size=15)
                           )

        c7.plotly_chart(fig7, use_container_width=True)


        st.subheader('H8: Imรณveis no inverno sofrem uma desvalorizaรงรฃo de 20% no preรงo total com relaรงรฃo ao outono')

        st.markdown("<p style='font-size:18px'>"
                    "โ๏ธ<b>Hipotese confirmada:</b> Imรณveis no inverno sofrem uma desvalorizaรงรฃo de quase 30% no preรงo total"
                    "com relaรงรฃo ao outono"
                    "</p>", unsafe_allow_html=True)

        fig8 = px.bar(h8,
                      x='year_month',
                      y='price',
                      color='sazonalidade',
                      color_discrete_sequence=['#DECBE4', '#CCEBC5', '#B3CDE3', '#E5D8BD'],
                      hover_name='sazonalidade',
                      height= 600)

        fig8.update_layout(showlegend = False,
                           xaxis_title="Mรชs do ano",
                           yaxis_title="Preรงo",
                           font=dict(size=15)
                           )
        st.plotly_chart(fig8, use_container_width=True)

    return None

def quarta_pagina(data, geofile):
    with tab3:

        c1, c2 = st.columns(2)

        c1.subheader('Tabela de compra')

        c1.markdown("<p style='font-size:18px'>"
                        "Com as recomendaรงรตes dos melhores imรณveis para compra, onde foi utilizando um critรฉrio de compra para"
                        " imรณveis que estivessem com o preรงo abaixo da mediana da regiรฃo, com condiรงรฃo maior ou igual a trรชs, contendo dois"
                        " ou mais quartos e pisos"
                    "</p>", unsafe_allow_html=True)

        # Separando as variaveis que irei usar para construรงรฃo da minha tabela de compra
        df_compra = data.copy()

        # Encontrando a mediana do preรงo dentro de cada regiรฃo
        df_compra_grouped = df_compra[['zipcode', 'price']].groupby('zipcode').median().reset_index()
        df_compra_grouped.columns = ['zipcode', 'median_price']

        # Juntando meus dataframes
        df_compra = pd.merge(df_compra, df_compra_grouped, on='zipcode', how='inner')

        # Criaรงรฃo da feature que me indicarรก se o imรณvel deve ser comprado ou nรฃo, sendo 1 = comprar e 0 = nรฃo comprar
        df_compra['status'] = 'NA'

        for i in range(len(df_compra)):
            if (df_compra.loc[i, 'price'] < df_compra.loc[i, 'median_price']) & (df_compra.loc[i, 'condition'] >= 4) & (
                    df_compra.loc[i, 'bedrooms'] >= 2) & (df_compra.loc[i, 'floors'] >= 2):
                df_compra.loc[i, 'status'] = 1
            else:
                df_compra.loc[i, 'status'] = 0

        # Criando a feature 'economia' que me indicarรก quanto economizei na compra do imรณvel baseados no preรงo e preรงo mediano
        df_compra['economia'] = df_compra[['price', 'median_price']].apply(lambda x: x['median_price'] - x['price'], axis=1)

        # Selecionando apenas meus imรณveis que estรฃo aptos para compra
        df_compra = df_compra.loc[df_compra['status'] == 1, :].copy()
        tabela_compra = df_compra[['id', 'zipcode', 'price', 'median_price', 'condition', 'status', 'economia']].copy()
        tabela_compra.columns = ['id', 'zipcode', 'preรงo', 'preรงo mediano', 'condiรงรฃo', 'comprar', 'economizado']

        c1.dataframe(tabela_compra)


        c2.subheader('Tabela de Venda')

        c2.markdown("<p style='font-size:18px'>"
                   'O critรฉrio de venda dos imรณveis foi de que imรณveis que estivessem abaixo da mediana da regiรฃo seriam vendidos'
                    ' com adiรงรฃo de 30% do seu valor no preรงo final, e imรณveis que esteajam acima da mediana terรฃo uma adiรงรฃo de 10%'
                    "</p>", unsafe_allow_html=True)

        df_venda = df_compra[['id', 'price', 'zipcode', 'sazonalidade']].copy()

        df_grouped_venda = df_venda[['zipcode', 'sazonalidade', 'price']].groupby(
            ['zipcode', 'sazonalidade']).median().reset_index()
        df_grouped_venda.columns = ['zipcode', 'sazonalidade', 'median_price']

        df_venda = pd.merge(df_venda, df_grouped_venda, on=['zipcode', 'sazonalidade'], how='inner')

        df_venda['preco_venda'] = df_venda[['median_price', 'price']].apply(lambda x:
                                                                            (x['price'] * 1.1) if x['price'] >= x['median_price'] else
                                                                            (x['price'] * 1.3), axis=1)

        df_venda['lucro_venda'] = df_venda['preco_venda'] - df_venda['price']

        lucro_por_estacao = df_venda[['sazonalidade', 'preco_venda']].groupby('sazonalidade').sum().reset_index()

        df_venda.columns = ['id', 'preรงo', 'zipcode', 'sazonalidade', 'preรงo mediano', 'preรงo de venda', 'lucro']
        c2.dataframe(df_venda)


        # Metricas de preรงos de compra e venda dos imรณveis
        c3, c4, c5, c6 = st.columns((13, 30, 13, 30))


        c3.metric(label="Gasto total da compra", value="$179.537.408,00")
        c4.metric(label="Total economizado", value="$33.658.210,00")
        c5.metric(label="Valor total de venda", value="$209.320.208,00")
        c6.metric(label="Lucro total", value="$29.782.800,00")



        c7, c8 = st.columns(2)

        # Mapa de densidade dos imรณveis para compra
        c7.subheader('Portfรณlio de imรณveis para compra')

        df_sample = df_compra.copy()

        # Base map
        density_map = folium.Map(location=[df_sample['lat'].mean(), df_sample['long'].mean()], default_zoom_start=15)

        marker_cluster = MarkerCluster().add_to(density_map)


        for name, row in df_sample.iterrows():
            folium.Marker([row['lat'], row['long']],
                          popup='Sold R${0} on {1}. Features: {2} sqft, {3} bedrooms, {4} bathrooms, year_built: {5}'.format(
                              row['price'],
                              pd.to_datetime(row['date']),
                              row['sqft_living'],
                              row['bedrooms'],
                              row['bathrooms'],
                              row['yr_built'])).add_to(marker_cluster)

        with c7:
            folium_static(density_map)

            # Mapa de calor
            c8.subheader('Mapa de calor do preรงo dos imรณveis')

            heat_map = df_sample[['zipcode', 'price']]
            heat_map.columns = ['ZIP', 'PRICE']

            geofile = geofile[geofile['ZIP'].isin(heat_map['ZIP'].tolist())]

            region_price_map = folium.Map(location=[df_sample['lat'].mean(),
                                                    df_sample['long'].mean()],
                                          default_zoom_start=15)

            region_price_map.choropleth(data=heat_map,
                                        geo_data=geofile,
                                        columns=['ZIP', 'PRICE'],
                                        key_on='feature.properties.ZIP',
                                        fill_color='YlOrRd',
                                        fill_opacity=0.7,
                                        line_opacity=0.2,
                                        legend_name='AVG PRICE')

            with c8:
                folium_static(region_price_map)

    return None


if __name__ == '__main__':
    # get data
    path = './datasets/kc_house_data.csv'
    url = 'https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson'

    data = get_data(path)
    geofile = get_geofile(url)

    # transform
    data = data_transform(data)

    # pages
    primeira_pagina()
    segunda_pagina(data)
    terceira_pagina(data)
    quarta_pagina(data, geofile)