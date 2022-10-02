<h1 align="center">
  House Rocket - Projeto de Insights
</h1>

<h3 align="center">
https://victormachad0-house-rocket-project-main-b3isou.streamlitapp.com/
</h3>

<h1 align="center">
  <img alt="houserocketlogo" title="#logo" src="./images/houses.png" />
</h1>

## 1. Introdução ao problema de negócio
    
A House Rocket é uma empresa localizada em King County, Washington e tem como modelo de negócio
a compra e venda de imóveis, sua príncipal estratégia é a compra de imóveis com preços baixos para posteriormente realizar a venda destes por um preço maior.
   
Para auxiliar o time de negócios na tomada de decisões sobre a compra e venda dos imóveis, iremos realizar uma 
analise sobre os dados dos imóveis a venda em King County, pois quanto maior a diferença entre o preço de compra
e o preço de venda, maior o lucro da empresa e portanto maior sua receita.

### 1.1 Questões do negócio
   - Quais imóveis a House Rocket deveria comprar e por qual preço?
   - Uma vez comprado, qual o melhor momento para vende-los e por qual preço?
   
## 2. Premissas do negócio
   - Imóveis com data de reforma igual a 0 são imóveis que nunca foram reformados
   - Imóveis com 33 quartos foram considerados um erro de digitação e alterados para 3 quartos
   - Imóveis com 0 banheiros não nos interessam e foram descartados
   - Id’s duplicados foram removidos, considerando somente a venda mais recente
   
## 3. Planejamento da Solução
   
  ### 3.1 Entrega final
   - Tabela informando quais os melhores imóveis para compra dentro do nosso porfólio
   - Tabela informando qual o melhor momento para vender os imóveis e também o preço recomendado
  
  ### 3.2 Ferramentas utilizadas
   - Python 3.9
   - Jupyter Notebook
   - Pycharm
   - Streamlit
   
  ### 3.3 Processo até a solução
   - Com os dados já tratados, foi feito um agrupamento por região, e dentro de cada região foi identificado o preço mediano dos imóveis. 
      - Foi sugerido então, que imóveis abaixo do preço mediano de cada região e que estivessem em boas condições, fossem comprados.
   
   - Realizar um novo agrupamento por região e sazonalidade, calcular novamente a mediana dos preços baseado nessas duas features e:
      
      - Se o preço de compra estiver maior do que o da média da região + sazonalidade, irei vender os imóveis com um adicional de 10% no preço.
      
      - Se o preço de compra estiver menor do que o da média da região + sazonalidade, irei vender os imóveis com um adicional de 30% no preço.
   
## 4. Os 5 principais insights de negócio

   - **H1:** Imóveis que possuem vista para água, são 30% mais caros, na média.
      
      ✔️ **Verdadeira:** Casas com vista pro mar são até 220% mais caras na media
   
   - **H2:** Imóveis com vista 'regular' são mais são 30% mais baratos do que com vista 'boa'
      
      ✔️ **Verdadeira:** Imóveis com vista regular são até 45% mais baratos do que imóveis com uma vista boa
   
   - **H3:** Imóveis que nunca foram reformados são 20% mais baratos do que imóveis que nunca tiveram reforma
      
      ✔️ **Verdadeira:** Imóveis que nunca foram reformados são até 43% mais baratos do que imóveis que já passaram por alguma reforma
   
   - **H4:** Imóveis no inverno sofrem uma desvalorização de 20% no preço total com relação ao outono
      
      ✔️ **Verdadeira:** Imóveis no inverno sofrem uma desvalorização de quase 30% no preço total com relação ao outono
   
   - **H5:** Imóveis sem porão possuem sqft_lot 40% maiores do que com porão.
      
      ❌ **Falsa:** Imóveis sem porão possuem sqft_lot somente até 22% maiores do que com porão


## 5. Resultados financeiros para o negócio

| Preço total de compra  |  Preço total de venda   |   Lucratividade total   |
|------------------------|-------------------------|-------------------------|
|     $1.318.908.451     |      $1.561.075.462     |      $242.167.011       |



Meu linkedin: https://www.linkedin.com/in/victor-machado1/
