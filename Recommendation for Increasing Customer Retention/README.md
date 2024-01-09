# Recommendation for Increasing Customer Retention

Category: Funnel Analysis, RFM Segmentation, Recommendation, Retention Analysis
Oragnization: Personal Project
Tools: Python

- Contents

## Objective

- Implementation of recommendation system to increase customer retention
    - In terms of customer relationship development and cost, retaining existing customers is more crucial than acquiring new ones.
    - By maintaining long-term customer relationships, a company can anticipate stable revenue and secure a foundation for growth.
    - Personalized recommendation based on customer’s preferences can trigger additional purchases and a lock-in effect.

## Tech Stack

- Programming: Python
- Data Analysis and Modeling: Pandas, NumPy, Scikit-learn
- Visualization: Matplotlib, Seaborn

## Dataset

- Source: Fashion Campus from Kaggle
    - Customer dataset: 100,000 lines and 15 variables
    - Product dataset: 44,445 lines and 10 variables
    - Click_stream dataset: 12,833,602 lines and 12 variables
    - Transaction dataset: 1,254,585 lines and 16 variables

## Data Analysis

### 1. EDA(**Exploratory Data Analysis)**

- **New Customer Trend**
    - There is a higher number of new customers in the second half compared to the first half, and there is a consistent surge of new customers every July.
    - The upward trend in 2021 and 2022 is pronounced due to the impact of the COVID-19 pandemic.
    
    ![1. trend.png](Recommendation%20for%20Increasing%20Customer%20Retention%20b6d077c336384de0a571e53c570f395c/1._trend.png)
    

### 2. RFM Analysis

- Method: K-Means clustering
- Result
    - Customers were categorized into three groups based on their level of engagement; Active, Normal, and Non-active groups
    - While the proportions of the three groups are similar, the Active customer group, which has the most significant impact on revenue, has the lowest proportion.
    
    ![3. rfm.png](Recommendation%20for%20Increasing%20Customer%20Retention%20b6d077c336384de0a571e53c570f395c/3._rfm.png)
    

### 3. Retention Analysis

- Customer retention represents in both purchase frequency and retention period. I conducted separate analysis for each.
- **Range Retention** (Cohort by the first purchase date)
    - The recent cohort that made their first purchase exhibited a retention rate approximately 10%p lower compared to other cohorts within the same period.
    - Initially maintained at around 40%, it declines to the 20% range within 18 months. This signifies a decrease in the retention period.
    
    ![4.re_purchase.png](Recommendation%20for%20Increasing%20Customer%20Retention%20b6d077c336384de0a571e53c570f395c/4.re_purchase.png)
    
- **Rolling Retention** (Cohort by retention periods)
    - The retention period is defined as the duration from the signup date to the last login date.
    - Since December 2021, there has been a notable increase in the decline of retention rates.
    - Customers who recently joined have a shorter retention period compared to other cohorts within the same period.
    
    ![5.re_period.png](Recommendation%20for%20Increasing%20Customer%20Retention%20b6d077c336384de0a571e53c570f395c/5.re_period.png)
    

### 3. Funnel Analysis

- Generally, session time is predetermined, and session information is recorded based on key events within the session time. However, in the dataset, session information exists for each unique customer session ID, irrespective of session time. Therefore, funnels are regarded based on the events that occurred.
- Funnel Definition
    - Reclassified 9 events into 4 key events.
    
    | 1. Visit | homepage, search, scroll, click |
    | --- | --- |
    | 2. Interst | item_page |
    | 3. Purchase Intention | add_to_cart, booking |
    | 4. Buy | pay |
- Defining the customer journey from search to purchase, cases where customers directly added to the cart or made a purchase without visiting detailed item pages accounted for 29.5%.
    - There is a limitation in identifying exact funnels as I was unable to check the web pages.
    
    ![6.funnel type.png](Recommendation%20for%20Increasing%20Customer%20Retention%20b6d077c336384de0a571e53c570f395c/6.funnel_type.png)
    
- Assuming a sequential experience through the 4-stage funnel, the conversion rate from the product detail page to purchase intent is the lowest at 30%, indicating a declining trend. Improvement is needed in this aspect.
    
    ![7. funnel trend.png](Recommendation%20for%20Increasing%20Customer%20Retention%20b6d077c336384de0a571e53c570f395c/7._funnel_trend.png)
    

### 4. Insights

- **Data analysis summary**
    - RFM segmentation: the non-active group’s ratio(32%) is bigger than the active group(29%)
    - Range retention: decline in repurchase rate
    - Rolling retention: incline in customer churn
    - Purchase behavior: low appeal of detailed item pages
    - Funnel Analysis: low in conversion rate from detailed page to purchase intention(cart or buy)
- **Insights**
    - Customers tended to move from a landing page to purchase behaviors such as putting items into their carts or directly buying them.
    - **Recommendation system is need to customize landing pages.**

## Recommendation System

- Algorithm: **Colaborative Filtering**
- **Setting Preference**
    - Set 'Add to Cart' and 'Purchase' as implicit feedback indicating purchase intent
    - Assigned 1 point for 'Add to Cart,' 2 points for 'Purchase,' and 3 points for both 'Add to Cart' and 'Purchase'
    - Excluded cases where a product is repeatedly purchased, as this may excessively inflate the preference score
- **Modeling**
    
    ![8.rec.png](Recommendation%20for%20Increasing%20Customer%20Retention%20b6d077c336384de0a571e53c570f395c/8.rec.png)
    
    1.  Best-seller based on statistics
        - Sorted products by sales volume and average rating in descending order
        - Removed duplicate values with the same main category and subcategory for diverse product recommendations
        - Filtered a maximum of 5 products per main category based on the customer's gender for the final recommendation
            
            ![스크린샷 2023-03-21 오전 1.23.56.png](Recommendation%20for%20Increasing%20Customer%20Retention%20b6d077c336384de0a571e53c570f395c/%25E1%2584%2589%25E1%2585%25B3%25E1%2584%258F%25E1%2585%25B3%25E1%2584%2585%25E1%2585%25B5%25E1%2586%25AB%25E1%2584%2589%25E1%2585%25A3%25E1%2586%25BA_2023-03-21_%25E1%2584%258B%25E1%2585%25A9%25E1%2584%258C%25E1%2585%25A5%25E1%2586%25AB_1.23.56.png)
            
    2. KNN
        - Predicted ratings based on the ratings of 30 users with high similarity
        - Generated a recommendation list for products that the customer has not added to the cart or purchased
        - Filtered a maximum of 5 products per main category based on the customer's gender for the final recommendation
        
        ![스크린샷 2023-03-21 오전 1.26.04.png](Recommendation%20for%20Increasing%20Customer%20Retention%20b6d077c336384de0a571e53c570f395c/%25E1%2584%2589%25E1%2585%25B3%25E1%2584%258F%25E1%2585%25B3%25E1%2584%2585%25E1%2585%25B5%25E1%2586%25AB%25E1%2584%2589%25E1%2585%25A3%25E1%2586%25BA_2023-03-21_%25E1%2584%258B%25E1%2585%25A9%25E1%2584%258C%25E1%2585%25A5%25E1%2586%25AB_1.26.04.png)
        
    3. SGD
        - Parameters: latent parameter 20, RMSE, learning_rate 0.1 epochs 50
        - Filtered a maximum of 5 products per main category based on the customer's gender for the final recommendation
        
        ![스크린샷 2023-03-21 오전 1.28.24.png](Recommendation%20for%20Increasing%20Customer%20Retention%20b6d077c336384de0a571e53c570f395c/%25E1%2584%2589%25E1%2585%25B3%25E1%2584%258F%25E1%2585%25B3%25E1%2584%2585%25E1%2585%25B5%25E1%2586%25AB%25E1%2584%2589%25E1%2585%25A3%25E1%2586%25BA_2023-03-21_%25E1%2584%258B%25E1%2585%25A9%25E1%2584%258C%25E1%2585%25A5%25E1%2586%25AB_1.28.24.png)