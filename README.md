<h1 align="center">
  House Rocket
</h1>

<h3 align="center">
https://house-rocket-sales.streamlit.app/
</h3>

<h1 align="center">
  <img alt="houserocketlogo" title="#logo" src="./images/houses.png" />
</h1>

## 1. Introduction to the business problem.
    
The House Rocket is a company located in King County, Washington, whose business model is buying and selling real estate.
Its main strategy is to purchase properties at low prices, make basic renovations when necessary, and later sell them for a higher price.
   
To help the business team make decisions regarding the purchase and sale of properties, we are going to analyze data from properties for sale in King County. The greater the difference between the purchase price and the selling price, the higher the company’s profit and, consequently, its revenue.

### 1.1 Business Questions
   - Which properties should House Rocket buy, and at what price?
   - Once purchased, when is the best time to sell them, and for what price?
   
## 2. Business Assumptions
   - Properties with a renovation date equal to 0 are considered properties that were never renovated.
   - Properties with 33 bedrooms were considered a typing error and changed to 3 bedrooms.
   - Properties with 0 bathrooms are not relevant to us and were removed from the analysis.
   - Duplicate IDs were removed, considering only the most recent sale.
   
## 3. Solution Planning
   
  ### 3.1 Final Deliverables
   - A table containing the best properties to purchase within our portfolio.
   - A table indicating the best time to sell the properties, as well as the recommended selling price.
  
  ### 3.2 Tools Used in the project.
   - Python 3.9
   - Jupyter Notebook
   - Pycharm
   - Streamlit
   - Streamlit Cloud
   
  ### 3.3 Process Until the Solution
   - With the cleaned data, a grouping by region was performed, and within each region, the median property price was identified.
      - It was then suggested that properties priced below the median of each region and in good condition should be purchased.
   
   - A new grouping by region and seasonality was performed, and the median prices were recalculated based on these two features:
      
      - If the purchase price is higher than the regional and seasonal average price, the properties will be sold with an additional 10% markup.
      
      - If the purchase price is lower than the regional and seasonal average price, the properties will be sold with an additional 30% markup.
   
## 4. The Five Main Business Insights

   - **H1:** Properties with an ocean view are, on average, 30% more expensive than properties without an ocean view.
      
      ✔️ **True:** Houses with an ocean view are, on average, up to 220% more expensive than other properties.
   
   - **H2:** Properties with a “regular” view are 30% cheaper than properties with a “good” view.
      
      ✔️ **True:** Properties with a regular view are up to 45% cheaper than properties with a good view.
   
   - **H3:** Properties that were never renovated are 20% cheaper than renovated properties.
      
      ✔️ **True:** Properties that were never renovated are up to 43% cheaper than properties that have undergone renovations.
   
   - **H4:** During winter, properties depreciate by approximately 20% compared to autumn.
      
      ✔️ **True:** During winter, properties depreciate by almost 30% compared to autumn.
   
   - **H5:** Properties without a basement have lot sizes (sqft_lot) 40% larger than properties with a basement.
      
      ❌ **False:** Properties without a basement have lot sizes only up to 22% larger than properties with a basement.


## 5. Financial Results for the Business

| Total Purchase Price |  Total Selling Price  |   Total Profit  |
|------------------------|-------------------------|-------------------------|
|     $179.537.408,00    |      $209.320.208,00     |      $29.782.800,00       |



My LinkedIn: https://www.linkedin.com/in/victor-machado1/
