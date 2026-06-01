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
tab0, tab1, tab2, tab3 = st.tabs(['🛕 Home', '📜 Overview', '📉 Hypothesis', '🧠Business Questions'])

#import data
@st.cache_data
def get_data(path):
    data = pd.read_csv(path)

    return data

@st.cache_data
def get_geofile(url):
    geofile = geopandas.read_file(url)

    return geofile

def data_transform(data):

    # Transformation
    #data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')
    data['date'] = pd.to_datetime( data['date'] ).dt.strftime( '%Y-%m-%d' )
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

    data['porao'] = data['sqft_basement'].apply(lambda x: 'não' if x == 0 else 'sim')

    data['price_m2'] = data['price'] / data['sqft_lot']

    data['m2'] = data['sqft_lot'] / 10.764

    return data

def primeira_pagina():
    with tab0:
        st.image('./images/houses.png')


        st.info('Note: The data used in this project are fictitious; however, the solution was developed with real-world cases in mind.')

        st.header("Getting to know House Rocket better")

        st.markdown("<p style='font-size:18px'>"
                    "The House Rocket is a company located in King County, Washington, whose business model is buying and selling real estate."
                    "Its main strategy is to purchase properties at low prices, make basic renovations when necessary, and later sell them for a higher price."
                    "</p>", unsafe_allow_html=True)

        st.markdown("<p style='font-size:18px'>"
                    "To help the business team make decisions regarding the purchase and sale of properties, we are going to analyze data from properties for sale in King County."
                    "The greater the difference between the purchase price and the selling price, the higher the company’s profit and, consequently, its revenue."
                    "</p>", unsafe_allow_html=True)

        st.subheader("The project addresses two main business questions:")

        st.markdown("<ul>"
                    "<li>"
                    "<p style='font-size:18px'>"
                    "Which properties should House Rocket buy, and at what price?"
                    "</p>"
                    "</li>"
                    "</ul>", unsafe_allow_html=True)

        st.markdown("<ul>"
                    "<li>"
                    "<p style='font-size:18px'>"
                    "Once purchased, when is the best time to sell them, and for what price?"
                    "</p>"
                    "</li>"
                    "</ul>", unsafe_allow_html=True)


        st.subheader("Financial Results for the Business:")

        values  = [['$179.537.408,00'], ['$33.658.210,00']]
        values2 = [['$209.320.208,00'], ['$29.782.800,00']]
        values3 = [['autumn', 'spring', 'summer', 'winter'],
                   ['$49.933.865,00', '$49.399.426,00', '$78.222.913,00', '$31.764.003,00']]

        #table 1
        c1, c2 = st.columns(2)

        table = go.Figure(data=[go.Table(
            columnorder=[1, 2],
            columnwidth=[100, 150],
            header=dict(
                values=[['<b>Total Purchase Price</b>'],
                        ['<b>Money saved</b>']],
                line_color='black',
                line_width=2,
                fill_color=['#F0F8FF'],
                align=['center', 'center'],
                font=dict(color='black', size=20),
                height=40
            ),
            cells=dict(
                values=values,
                line_color='darkslategray',
                line_width=2,
                fill=dict(color=['white']),
                align=['center', 'center'],
                font=dict(color=['black'], size=18),
                height=40))])

        table.update_layout(height=160, margin = dict(l=5, r=0, b=1, t=50),  title = 'Total amount invested in property purchases + savings', title_font_size = 25)
        c1.plotly_chart(table, use_container_width=True)

        #table 2
        c1, c2 = st.columns(2)

        table2 = go.Figure(data=[go.Table(
            columnorder=[1, 2],
            columnwidth=[100, 150],
            header=dict(
                values=[['<b>Total Selling Price</b>'],
                        ['<b>Total Profit</b>']],
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
        
        table2.update_layout(height=150, margin = dict(l=5, r=1, b=1, t=35), title = 'Total proceeds from property sales + total profit', title_font_size = 25)
        c1.plotly_chart(table2, use_container_width=True)


        #table 3
        c1,c2 = st.columns(2)

        table3 = go.Figure(data=[go.Table(
            columnwidth=[100, 150],
            header=dict(
                values=[['<b>seasonality</b>'],
                        ['<b>Selling price</b>']],
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

        table3.update_layout(height=400, margin = dict(l=5, r=1, b=1, t=35),  title = 'Total property sales amount by seasonality', title_font_size = 25)
        c1.plotly_chart(table3, use_container_width=True)

        return None

def segunda_pagina(data):
    with tab1:
        st.header('Data Visualization')
        st.sidebar.header('Overview')

        # Data Overview
        f_attributes = st.sidebar.multiselect('Select a column', data.columns)

        f_zipcode = st.sidebar.multiselect('Enter the zipcode', data['zipcode'].unique())

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
        df.columns = ['zipcode', 'total_properties', 'price', 'internal_space', 'price_per_m²']

        c1.header('Average by Region')
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

        c2.header('Descriptive Statistics')
        c2.dataframe(statistics_describe, height=450)


        # Column description
        fig_values = [['id', 'date', 'price', 'bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors', 'waterfront', 'view', 'conditions',
                       'grade', 'sqft_above', 'sqft_basement', 'yr_built', 'yr_renovated', 'zipcode', 'lat', 'long', 'sqft_living15', 'sqft_lot15'],


                 ['Unique identifier for each property', 'Date when the property was sold', 'Property selling price', 'Number of bedrooms', 'Number of bathrooms', "Square footage of the property's interior living space",
                  'Square footage of the land area', 'Number of floors in each property', 'Indicates whether the property has a waterfront view', "An index from 0 to 4 representing the quality of the property's view", 'An index from 0 to 5 representing the condition of the property',
                   "An index from 1 to 13, where 1–3 falls below average in construction and design, 7 represents an average level of construction and design, and 11–13 represents a high level of construction and design", 'Year the property was built',
                    "Year of the property's last renovation", 'ZIP code area where the properties are located', 'Latitude', 'Longitude', 'Square footage of the interior living area of the 15 nearest neighboring properties', 'Square footage of the lots of the 15 nearest neighboring properties',
                     'No translation', 'No translation']]

        with st.expander("Columns description"):


            fig = go.Figure(data=[go.Table(
                columnwidth=[80, 400],
                header=dict(
                    values=[['<b>Name</b>'],
                            ['<b>Meaning</b>']],
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
        st.header('Hypothesis Validation')

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

        c1.subheader('H1: Properties with an ocean view are, on average, 30% more expensive than properties without an ocean view.')

        c1.markdown("<p style='font-size:18px'>"
                    "✔️<b>True:</b> Houses with an ocean view are, on average, up to 220% more expensive than other properties."
                    "</p>", unsafe_allow_html=True)

        fig1 = px.bar(h1,
                      x='waterfront',
                      y='price',
                      height= 600,
                      color = 'waterfront',
                      color_continuous_scale=['#DECBE4', '#CCEBC5'],
                      )

        fig1.update_layout(coloraxis_showscale=False,
                           xaxis_title="Ocean view",
                           yaxis_title="Price",
                           font=dict(size= 15)
                           )

        c1.plotly_chart(fig1, use_container_width=True)



        c2.subheader('H2: Properties built before 1955 are, on average, 50% less expensive')

        c2.markdown("<p style='font-size:18px'>"
                    "❌ <b>False:</b> The properties did not show a significant price difference; they are comparable."
                    "</p>", unsafe_allow_html=True)

        fig2 = px.bar(h2,
                      x='before_1955',
                      y='price',
                      height= 600,
                      color='before_1955',
                      color_continuous_scale=['#DECBE4', '#CCEBC5'])

        fig2.update_layout(coloraxis_showscale=False,
                           xaxis_title="Properties built before 1955",
                           yaxis_title="Price",
                           font=dict(size=15)
                           )

        c2.plotly_chart(fig2, use_container_width=True)


        st.subheader('H3: Regardless of their condition, properties increase in value by around 10% per year.')

        st.markdown("<p style='font-size:18px'>"
                    "❌ <b>False:</b> Regardless of their condition, all properties depreciated compared to the same month of the previous year."
                    "</p>", unsafe_allow_html=True)

        fig3 = make_subplots(rows=3, cols=1,
                             specs=[[{}], [{}], [{}]],
                             print_grid=True,
                             subplot_titles=('Price fluctuation of properties in poor condition throughout the year',
                                             'Price fluctuation of properties in regular condition throughout the year',
                                             'Price fluctuation of properties in good condition throughout the year'))


        fig3.add_trace(go.Scatter(x=h3_bad['year_month'], y=h3_bad['price']), row=1, col=1)
        fig3.add_trace(go.Scatter(x=h3_regular['year_month'], y=h3_regular['price']), row=2, col=1)
        fig3.add_trace(go.Scatter(x=h3_good['year_month'], y=h3_good['price']), row=3, col=1)

        fig3.update_layout(showlegend = False, font=dict(size = 15), height = 1000)
        fig3.layout.annotations[0]["font"] = {'size': 20}
        fig3.layout.annotations[1]["font"] = {'size': 20}
        fig3.layout.annotations[2]["font"] = {'size': 20}


        st.plotly_chart(fig3, use_container_width=True)



        c4, c5 = st.columns(2)

        c4.subheader('H4: Properties without basements have 40% larger lots than properties with basements.')

        c4.markdown("<p style='font-size:18px'>"
                    "❌ <b>False:</b> Properties without basements have lots up to 22% larger than those with basements."
                    "</p>", unsafe_allow_html=True)

        fig4 = px.bar(h4,
                      x='basement',
                      y='sqft_lot',
                      height= 600,
                      color='basement',
                      color_discrete_sequence= ['#DECBE4', '#CCEBC5']
                      )

        fig4.update_layout(showlegend = False,
                           xaxis_title="Basement",
                           yaxis_title="Lot size",
                           font=dict(size=15)
                           )

        c4.plotly_chart(fig4, use_container_width=True)


        c5.subheader('H5: Properties with a regular view are 30% cheaper than those with a good view.')

        c5.markdown("<p style='font-size:18px'>"
                    "✔️<b>True:</b> Properties with a regular view are up to 45% cheaper than those with a good view."
                    "</p>", unsafe_allow_html=True)

        fig5 = px.bar(h5,
                      x='view_type',
                      y='price',
                      height= 600,
                      color='view_type',
                      color_discrete_sequence= ['#DECBE4', '#CCEBC5', '#B3CDE3']
                      )

        fig5.update_layout(showlegend = False,
                           xaxis_title="Property View Quality",
                           yaxis_title="Price",
                           font=dict(size=15)
                           )

        c5.plotly_chart(fig5, use_container_width=True)


        c6, c7 = st.columns(2)

        c6.subheader('H6: During the summer, property values are 20% higher than in the spring.')

        c6.markdown("<p style='font-size:18px'>"
                    "❌ <b>False:</b> During the summer, property values show a non-significant 3% decrease compared to the spring."
                    "</p>", unsafe_allow_html=True)

        fig6 = px.bar(h6,
                      x='seasonality',
                      y='price',
                      height= 600,
                      color='seasonality',
                      color_discrete_sequence= ['#DECBE4', '#CCEBC5', '#B3CDE3', '#E5D8BD']
                      )

        fig6.update_layout(showlegend = False,
                           xaxis_title="Season",
                           yaxis_title="Price",
                           font=dict(size=15)
                           )

        c6.plotly_chart(fig6, use_container_width=True)

        c7.subheader('H7: Properties that have never been renovated are up to 20% cheaper than renovated properties.')

        c7.markdown("<p style='font-size:18px'>"
                    "✔️<b>True:</b> Properties that have never been renovated are up to 43% cheaper than renovated properties."
                    "</p>", unsafe_allow_html=True)

        fig7 = px.bar(h7,
                      x='renovated',
                      y='price',
                      height= 600,
                      color='renovated',
                      color_continuous_scale=['#DECBE4', '#CCEBC5'])

        fig7.update_layout(coloraxis_showscale=False,
                           xaxis_title="Renovated",
                           yaxis_title="Price",
                           font=dict(size=15)
                           )

        c7.plotly_chart(fig7, use_container_width=True)


        st.subheader('H8: Property values decrease by 20% during the winter compared to the autumn.')

        st.markdown("<p style='font-size:18px'>"
                    "✔️<b>True:</b> During the winter, property values decrease by almost 30% compared to the autumn."
                    "</p>", unsafe_allow_html=True)

        fig8 = px.bar(h8,
                      x='year_month',
                      y='price',
                      color='seasonality',
                      color_discrete_sequence=['#DECBE4', '#CCEBC5', '#B3CDE3', '#E5D8BD'],
                      hover_name='seasonality',
                      height= 600)

        fig8.update_layout(showlegend = False,
                           xaxis_title="Month of the year",
                           yaxis_title="Price",
                           font=dict(size=15)
                           )
        st.plotly_chart(fig8, use_container_width=True)

    return None

def quarta_pagina(data, geofile):
    with tab3:

        c1, c2 = st.columns(2)

        c1.subheader('Purchases Table')

        c1.markdown("<p style='font-size:18px'>"
                        "With recommendations for the best properties to purchase, using a selection criterion that prioritizes"
                        " properties priced below the regional median, with a condition rating of at least three, and featuring two"
                        " or more bedrooms and floors."
                    "</p>", unsafe_allow_html=True)

        # Separando as variaveis que irei usar para construção da minha tabela de compra
        df_compra = data.copy()

        # Encontrando a mediana do preço dentro de cada região
        df_compra_grouped = df_compra[['zipcode', 'price']].groupby('zipcode').median().reset_index()
        df_compra_grouped.columns = ['zipcode', 'median_price']

        # Juntando meus dataframes
        df_compra = pd.merge(df_compra, df_compra_grouped, on='zipcode', how='inner')

        # Criação da feature que me indicará se o imóvel deve ser comprado ou não, sendo 1 = comprar e 0 = não comprar
        df_compra['status'] = 'NA'

        for i in range(len(df_compra)):
            if (df_compra.loc[i, 'price'] < df_compra.loc[i, 'median_price']) & (df_compra.loc[i, 'condition'] >= 4) & (
                    df_compra.loc[i, 'bedrooms'] >= 2) & (df_compra.loc[i, 'floors'] >= 2):
                df_compra.loc[i, 'status'] = 1
            else:
                df_compra.loc[i, 'status'] = 0

        # Criando a feature 'economia' que me indicará quanto economizei na compra do imóvel baseados no preço e preço mediano
        df_compra['savings'] = df_compra[['price', 'median_price']].apply(lambda x: x['median_price'] - x['price'], axis=1)

        # Selecionando apenas meus imóveis que estão aptos para compra
        df_compra = df_compra.loc[df_compra['status'] == 1, :].copy()
        tabela_compra = df_compra[['id', 'zipcode', 'price', 'median_price', 'condition', 'status', 'savings']].copy()
        tabela_compra.columns = ['id', 'zipcode', 'price', 'median price', 'condition', 'purchase', 'saved']

        c1.dataframe(tabela_compra)


        c2.subheader('Sales table')

        c2.markdown("<p style='font-size:18px'>"
                   'The sales strategy established that properties priced below the regional median would be sold'
                    ' with a 30% increase over their original value, whereas properties priced above the regional median would receive a 10% increase in their final selling price.'
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

        df_venda.columns = ['id', 'preço', 'zipcode', 'seasonality', 'median price', 'sale price', 'profit']
        c2.dataframe(df_venda)


        # Metricas de preços de compra e venda dos imóveis
        c3, c4, c5, c6 = st.columns((13, 30, 13, 30))


        c3.metric(label="Total purchase amount", value="$179.537.408,00")
        c4.metric(label="Total amount saved", value="$33.658.210,00")
        c5.metric(label="Total sales amount", value="$209.320.208,00")
        c6.metric(label="Total profit", value="$29.782.800,00")



        c7, c8 = st.columns(2)

        # Mapa de densidade dos imóveis para compra
        c7.subheader('Property portfolio for purchase')

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
            c8.subheader('Property prices heatmap')

            heat_map = df_sample[['zipcode', 'price']].groupby('zipcode').mean().reset_index()
            heat_map.columns = ['ZIP', 'PRICE']

            geofile = geofile[geofile['ZIP'].isin(heat_map['ZIP'].tolist())]

            region_price_map = folium.Map(location=[df_sample['lat'].mean(),
                                                    df_sample['long'].mean()],
                                          default_zoom_start=15)

           # region_price_map.choropleth(data=heat_map,
           #                             geo_data=geofile,
           #                             columns=['ZIP', 'PRICE'],
           #                             key_on='feature.properties.ZIP',
           #                             fill_color='YlOrRd',
           #                             fill_opacity=0.7,
           #                             line_opacity=0.2,
           #                             legend_name='AVG PRICE')

            folium.Choropleth(geo_data=geofile,
                              data=heat_map,
                              columns=['ZIP', 'PRICE'],
                              key_on='feature.properties.ZIP',
                              fill_color='YlOrRd',
                              fill_opacity=0.7,
                              line_opacity=0.2,
                              legend_name='AVG PRICE').add_to(region_price_map)

        with c8:
            folium_static(region_price_map)

    return None


if __name__ == '__main__':
   
    path = 'datasets/kc_house_data.csv'
    #url = 'https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson'
    url = 'zipcode_area.geojson'

    data = get_data(path)
    geofile = get_geofile(url)
    
    #geofile = get_geofile(url)

    # transform
    data = data_transform(data)
   
    # pages
    primeira_pagina()
    segunda_pagina(data)
    terceira_pagina(data)
    quarta_pagina(data, geofile)
