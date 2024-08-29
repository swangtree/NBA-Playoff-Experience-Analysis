# 🏀 NBA Playoff Experience Econometrics Analysis

This project was my final project in applying econometrics and machine learning techniques to data (I chose basketball). The project focused on analyzing the impact of player playoff experience on game outcomes using a large dataset of NBA playoff games. The code and analysis were done by me, [Samuel Wang](https://github.com/swangtree).

## Table of Contents

- [About](#about)
- [Configuration](#configuration)
- [Features](#features)
- [Documentation](#documentation)

## About
The aim of this project was to understand how player experience in the playoffs affects the outcomes of NBA games. By leveraging statistical methods and machine learning models, I sought to quantify the impact of playoff experience on game performance and outcomes. 

The analysis revealed that teams with higher average playoff experience among their players tend to perform better, particularly in close games. The machine learning models enhanced the predictive accuracy over traditional regression models, identifying experience as a significant factor in determining game outcomes. The findings suggest that player experience is not only crucial for current performance but also serves as a strategic asset for managing player rotations and development over the course of a season.

Key aspects explored include:
1. **Player Experience as a Predictor** - How does prior playoff experience influence game performance?
2. **Machine Learning Applications** - The use of machine learning to enhance the predictive power of regression models.
3. **Data-Driven Insights** - Insights drawn from the analysis can be valuable for end of season player management for contending NBA teams as well as serve as a basis for the expected progression of NBA teams as players get mroe expererience.

The data was scraped using BeautifulSoup + Selenium and processed with Pandas, while Stata and Sklearn were used for the econometric and machine learning analyses, respectively.

## Configuration

The scripts allow customization of several parameters:

- `scrape_data()` - Modify the range of seasons or specific playoffs to include in the analysis.
- `model_training()` - Configure the machine learning model parameters and features to tune predictions.

For detailed instructions on how to adjust these parameters, refer to the comments in `nba_playoff_analysis.py`.

## Features

Key features of this project:

- Automated data scraping from basketballreference.com for 2,200+ NBA playoff games.
- Statistical analysis using Stata to explore the relationship between player experience and game outcomes.
- Machine learning model implemented with Sklearn to predict game results based on player experience.
- Data visualization to highlight key findings and trends.

The results of this analysis provide valuable insights into the role of experience in high-stakes playoff scenarios, offering potential strategic advantages for teams.

## Documentation

In addition to the resources utilized during this project, such as the official documentation for Stata, Sklearn, and Selenium, the following resources were particularly helpful:

- [Pandas Documentation](https://pandas.pydata.org/)
- [Selenium Documentation](https://selenium.dev/documentation/en/)
- [Sklearn Documentation](https://scikit-learn.org/stable/documentation.html)
