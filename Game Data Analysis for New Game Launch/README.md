# Game Data Analysis for New Game Launch

- Category: Data Analysis, Hypothesis Testing   
- Organization: Personal Project   
- Tools: Python   

## Objective

- Data analysis for new game launch in Q4 2022

## Tech Stack

- Programming: Python
- Data Analysis: Pandas, NumPy, SciPy
- Visualization: Matplotlib, Seaborn, Plotly

## Dataset

- Source: Video game sales data provided by Codestates
- 16,598 games and 9 features are included
    - Features: Name, Platform, Year, Genre, Publisher, NA_Sales, EU_Sales, JP_Sales, Other_Sales

## Process

### 1. Situation

The company A, the game producer, does the following:

- Produces console and portable video games.
- Has secured intellectual property rights of popular webtoons and fantasy novels.
- Need a plan for the upcoming game launch in Q4 2022

### 2. Data Preprocessing(EDA & Data Wrangling)

- Missing values were replaced with data of the same game name
- Inaccurate values in the year feature were corrected
- The unit of sales feature was unified
- Total_Sales features were added
- Data in 2017 and 2020 was removed because of the lack of the number of games

### 3. Analysis & Visualization

<aside>
**[Hypothesis 1] There is no difference in the preferred game genre by region.**

- There was a statistically significant difference in the preferred game genre by region.
</aside>

- Overall, the action genre accounted for almost 20% of the sales.

<img width="960" alt="Untitled 1" src="https://github.com/arden333/Data-Projects/assets/110075002/975dc8eb-6dea-41d6-8da6-e54f2cf46b10">

- In North America, Europe, and other regions, game genres with high total sales were similar: Action, Sports, Shooter in order. However, in Japan, Role-playing games recorded the highest total sales.
    
    <img width="388" alt="Untitled 2" src="https://github.com/arden333/Data-Projects/assets/110075002/2e6ab795-0d73-4ad7-9780-bf3c08712b78">
    
- The result of the chi-squared test of homogeneity rejected the null hypothesis because the p-value was $4.34 \times 2^{-116}$, which was less than the alpha value of 0.05. Therefore, there was a statistically significant difference in the preferred game genre by region.
- In addition, the heat map of correlation in sales between regions showed that there is more than 0.6 correlation coefficient, a strong correlation, between  North America, Europe, and Other regions, while Japan has less correlation(less than 0.45 correlation coefficient) with them.
    
    <img width="489" alt="Untitled 3" src="https://github.com/arden333/Data-Projects/assets/110075002/4de1a189-9d34-43f6-9d32-d6c8b14f1684">
    

<aside>
**[Hypothesis 2] There is an annual game trend.**

- The distinctive and long-term trends are shown in sales, game genres, and platforms.
</aside>

- Annual Video Game Sales Trend
    - Total sales have increased since 1980, but, have plummeted after 2009. This is because of the negative impact of the financial crisis in 2008 on the demand and increase in popularity of mobile games.
    
    <img width="592" alt="Untitled 4" src="https://github.com/arden333/Data-Projects/assets/110075002/4c926696-adea-40fd-845d-eb06aea2d5aa">
    
- The Best-selling Game Genre by year
    - Action has maintained the highest sales since 2013, with the only exception being 2006, and this tendency is expected to continue.
        
        <img width="592" alt="Untitled 5" src="https://github.com/arden333/Data-Projects/assets/110075002/4eced400-286c-4c94-b927-66a60557d1da">

        
- The Best-selling Platforms by year
    - Video game consoles have a conspicuous product life cycle. Every four to six years, the most popular consoles change. The Playstation series has remained No.1 since its launch.
        
        <img width="474" alt="Untitled 6" src="https://github.com/arden333/Data-Projects/assets/110075002/d80ddaef-288f-4da6-b113-9dbbe7b08e32">
        
    

<aside>
**Game Sales Top 50 Analysis**

- The distinctive and long-term trends are shown in sales, game genres, and platforms.
</aside>

- In terms of platforms, the ratio of console games that were over 67.8% surpassed that of portable games.
- Games were highly sold in North America and Europe.
- To be specific, 15 games ranked within the top 20 sales were series games such as Call of Duty, FIFA, and Pokemon. The series has a low likelihood of failure due to its strong fan base and the steady influx of existing users, which serves as an entry barrier for new game producers.

<img width="587" alt="Untitled 7" src="https://github.com/arden333/Data-Projects/assets/110075002/2932bb51-28d2-49e8-b652-6180a703af71">

<img width="288" alt="Untitled 8" src="https://github.com/arden333/Data-Projects/assets/110075002/c8b48757-5cb2-4a6c-b7f5-7b89f8d6d05d">

<aside>
**Challenges**: The limitation of tracking the latest trends in the video game market due to the absence of recent data beyond 2016

- Supplemented by reference to the game market trend data in the ‘2021 White Paper on Korean Games’ published by the Korea Creative Content Agency
</aside>

- Game sales surged in 2020 due to COVID-19, especially in mobile games. Considering video games can be played in consoles and computers, the prospect of console and PC games is positive.
- Mobile games showed outstanding growth. The growth rate of console games also was 7.2% which was promising.
- The demand for video games is expected to maintain because the characteristics and users of mobile and console games are distinctive.

<img width="726" alt="Untitled 9" src="https://github.com/arden333/Data-Projects/assets/110075002/37792262-e932-40d7-9061-59079da084d1">

<img width="269" alt="Untitled" src="https://github.com/arden333/Data-Projects/assets/110075002/745ce737-c59f-4ab3-b165-a032199098a9">

## Result

The new game, set to launch in Q4 2022 will encompass the following features:

- It will be an action genre combined with a storyline secured through intellectual property rights.
- A long-term game storyline will be required to release it as a series.
- It will be developed for the Playstation5 platform, aimed at attracting  many users in its initial states.
- The game will be released first in North America, one of the most active gaming markets. Since English is used all over the world, games also can be played by users who are proficient in English in regions where the official launch has not yet occurred.
