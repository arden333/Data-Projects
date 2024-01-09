# Digital Contents Subscription Churn Prediction

Category: Supervised Machine Learning   
Oragnization: Personal Project   
Tools: Python  

## Objective

- Prediction subscription churn for customer retention strategies
- Expected benefits:
    - Identification of characteristics of customer churn
    - Clarification of target audience and timing for promotions

## Tech Stack

- Programming: Python
- Data Analysis: Pandas
- Machine Learning: Scikit-learn
- Visualization: Matplotlib

## Dataset

- Source: Customer Subscription Data from Kaggle
- The data is about a subscription-based digital product offering for financial advisory that includes newsletters, webinars, and investment recommendations.
- 508,932 lines with 7 variables

![1.dataset.png](Digital%20Contents%20Subscription%20Churn%20Prediction%20f9aa10267fe542bfbb5e1a21acc58daf/1.dataset.png)

## Process

### 1. Data Analysis

- **Subscription and Cancellation Trend**
    - The number of monthly subscription users has increased annually, while the annual subscription users have been decreasing since 2020. Both annual and monthly subscribers’ cancellation inclined every year. In other words, the number of annual subscribers are decreasing.
    
    ![2.trend.png](Digital%20Contents%20Subscription%20Churn%20Prediction%20f9aa10267fe542bfbb5e1a21acc58daf/2.trend.png)
    
- **The Customer Churn Rate**
    - It is observed that the monthly subscribers have a higher rate compared to the annual subscribers. Then, who are more important for our business among annual subscribers and monthly subscribers?
        
        ![3.churn rate.png](Digital%20Contents%20Subscription%20Churn%20Prediction%20f9aa10267fe542bfbb5e1a21acc58daf/3.churn_rate.png)
        
- **Life Time Value**
    - The average subscription period is 17.5 months for annual users and 12.3 months for monthly users, indicating that the annual subscriptions are slightly longer.
    - The monthly product is priced at $125, while the annual product is priced at $1200 (equivalent to $120 per month). Although the annual product is cheaper than the monthly one, it contributes a larger share to the overall revenue. This is due to the longer subscription duration of the annual product.
    - Consequently, The Lifetime Value (LTV) of annual subscribers consistently exceeded that of monthly subscribers each year. Therefore, annual subscribers are crucial customers for the business, and a promotional strategy is necessary to prevent their loss.
        
        ![5.ltv.png](Digital%20Contents%20Subscription%20Churn%20Prediction%20f9aa10267fe542bfbb5e1a21acc58daf/5.ltv.png)
        

- **Annual Subscribers Who Canceled Analysis**
    - Users tend to unsubscribe in an average 5.2 months after sign-up or extension their subscriptions,
    - I found that these users are the target of retention promotions.
        
        ![5.renewal group.png](Digital%20Contents%20Subscription%20Churn%20Prediction%20f9aa10267fe542bfbb5e1a21acc58daf/5.renewal_group.png)
        

### 3. Modeling

- The initial goal was simply predicting customer churn. However, considering the results of data analysis, I reset the problem **to classify customers who are annual subscribers and have a subscription duration between 3.18 and 4.18 months after renewal**.
- **Modeling outline**
    - Meric: Recall
    - ML Algorithms: Random Forest
        - Compared to XGBoost, which had a recall value of 1, **Random Forest, with a recall value of 0.62**, was considered to be less overfitting.
    - Features of train data: age, gender, channel, subscription period, the number of cases

### 4. Hyperparameter Tuning

- I explored 4 hyperparameters using Randomized Search CV
    - Hyperparameters: criterion, max_depth, min_sample_split, min_samples_leaf

## Result

- **Model performace**
    - Recall value of the validation dataset: 0.83
    - **Generalization performance: 0.81**
        
        ![6. confusion mat.png](Digital%20Contents%20Subscription%20Churn%20Prediction%20f9aa10267fe542bfbb5e1a21acc58daf/6._confusion_mat.png)
        
- **Permutation Importance**
    - The subscription period proved to be the most influential variable in the model.
    
    ![7. p_i.png](Digital%20Contents%20Subscription%20Churn%20Prediction%20f9aa10267fe542bfbb5e1a21acc58daf/7._p_i.png)
