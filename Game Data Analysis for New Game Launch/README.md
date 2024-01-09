# Game Data Analysis for New Game Launch

Category: Data Analysis, Hypothesis Testing
Oragnization: Personal Project
Tools: Python

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
- Need a plan for upcoming game launch in in Q4 2022

### 2. Data Preprocessing(EDA & Data Wrangling)

- Missing values were replaced with data of the same game name
- Inaccurate values in year feature were corrected
- The unit of sales feature was unified
- Total_Sales features was added
- Data in 2017 and 2020 was removed because of the lack of the number of games

### 3. Analysis & Visualization

<aside>
<img src="https://www.notion.so/icons/checkmark_gray.svg" alt="https://www.notion.so/icons/checkmark_gray.svg" width="40px" /> **[Hypothesis 1] There is no difference in the preferred game genre by region.**

- There was a statistically significant difference in the preferred game genre by region.
</aside>

- Overall, action genre accounted for almost 20% of the sales.

![Untitled](Game%20Data%20Analysis%20for%20New%20Game%20Launch%2094e5375865d44239b613415ecf2305f2/Untitled.png)

- In North America, Europe, and other regions, game genres with high total sales were similar: Action, Sports, Shooter in order. However, in Japan, Role-playing game recorded the highest total sales.
    
    ![Untitled](Game%20Data%20Analysis%20for%20New%20Game%20Launch%2094e5375865d44239b613415ecf2305f2/Untitled%201.png)
    
- The result of the chi-squared test of homogeneity rejected null hypothesis because p-value was $4.34 \times 2^{-116}$, which was less than alpha value of 0.05. Therefore, there was a statistically significant difference in the preferred game genre by region.
- In addition, the heat map of correlation in sales between regions showed that more than 0.6 correlation coefficient, a strong correlation, between  North America, Europe, and Other regions, while Japan has less correlation(less than 0.45 correlation coefficient) with them.
    
    ![Untitled](Game%20Data%20Analysis%20for%20New%20Game%20Launch%2094e5375865d44239b613415ecf2305f2/Untitled%202.png)
    

<aside>
<img src="https://www.notion.so/icons/checkmark_gray.svg" alt="https://www.notion.so/icons/checkmark_gray.svg" width="40px" /> **[Hypothesis 2] There is an annual game trend.**

- The distinctive and long-term trends are shown in sales, game genre, and platforms.
</aside>

- Annual Video Game Sales Trend
    - Total sales has increased since 1980, but, has plummeted after 2009. This is because the negative impact of financial crisis in 2008 on the demand and increase in popularity of mobile games.
    
    ![Untitled](Game%20Data%20Analysis%20for%20New%20Game%20Launch%2094e5375865d44239b613415ecf2305f2/Untitled%203.png)
    
- The Best-selling Game Genre by year
    - Action has maintained the highest sales since 2013, with the only exception being 2006, and this tendency is expected to continue.
        
        ![Untitled](Game%20Data%20Analysis%20for%20New%20Game%20Launch%2094e5375865d44239b613415ecf2305f2/Untitled%204.png)
        
- The Best-selling Platforms by year
    - Video game consoles have a conspicuous product life cycle. Every four to six years, the most popular consoles changed. Playstation series have remains No.1 since its launch.
        
        ![Untitled](Game%20Data%20Analysis%20for%20New%20Game%20Launch%2094e5375865d44239b613415ecf2305f2/Untitled%205.png)
        
    

<aside>
<img src="https://www.notion.so/icons/checkmark_gray.svg" alt="https://www.notion.so/icons/checkmark_gray.svg" width="40px" /> **Game Sales Top 50 Analysis**

- The distinctive and long-term trends are shown in sales, game genre, and platforms.
</aside>

- In terms of platforms, the ratio of console games that were over 67.8% surpassed that of portable games.
- Games were highly sold in North America and Europe.
- Especially, 15 games ranked within top 20 sales were series games such as Call of Duty, FiFA, and Pokemon. The series has a low likelihood of failure due to its strong fan base and the steady influx of existing users, which serves as an entry barrier for new game producers.

![Untitled](Game%20Data%20Analysis%20for%20New%20Game%20Launch%2094e5375865d44239b613415ecf2305f2/Untitled%206.png)

![Untitled](Game%20Data%20Analysis%20for%20New%20Game%20Launch%2094e5375865d44239b613415ecf2305f2/Untitled%207.png)

<aside>
<img src="https://www.notion.so/icons/skip-forward_gray.svg" alt="https://www.notion.so/icons/skip-forward_gray.svg" width="40px" /> **Challenges**: The limitation of tracking the latest trends in the video game market due to the absence of recent data beyond 2016

- Supplemented by referencing to the game market trend data in ‘2021 White Paper on Korean Games’ published by the Korea Creative Content Agency
</aside>

- Game sales surged in 2020 due to COVID-19, especially in mobile games. Considering video games can be played in consoles and computers, the prospect of console and PC games are positive.
- Mobile games showed outstanding growth. The growth rate of console games also were 7.2% that was promising.
- The demand for video games is expected to maintain because the characteristics and users of mobile and console games are distinctive.

![Untitled](Game%20Data%20Analysis%20for%20New%20Game%20Launch%2094e5375865d44239b613415ecf2305f2/Untitled%208.png)

![Untitled](Game%20Data%20Analysis%20for%20New%20Game%20Launch%2094e5375865d44239b613415ecf2305f2/Untitled%209.png)

## Result

The new game, set to launch in Q4 2022 will encompass the following features:

- It will be an action genre combined with a storyline secured through intellectual property rights.
- A long-term game storyline will be required to release it as a series.
- It will be developed for Playstation5 platform, aimed to attracting  many users in its initial states.
- The game will be released first in North America, one of the most active gaming market. Since English is used all over the world, games also can be played by users who are proficient in English in regions where the official launch has not yet occurred.