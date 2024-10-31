# TDS Project1
- Scraped the data using a python [script](https://github.com/21f3000177/tds_project1/blob/main/scraper_gitbub.py) which calls the github REST APIs using python's requests module. The APIs used to scrape the data are
  1. https://api.github.com/search/users?q=location:Zurich+followers:>50
  2. https://api.github.com/users/<username>
  3. https://api.github.com/users/<username>/repos
     
  Scraped the data like this and created users.csv and repositories.csv. Then Analysed the data using Excel features like Pivot tables, =CORREL, Scatterplot etc
- The most interesting and surprising fact I found after analyzing the data is Python is the most popular language among the users.
- An actionable recommendation for developers based on my analysis will be to follow popular repositories to learn more in your interesting language. If developers would like to be hired, the need to create projects and they need to give all the details like email, wiki etc in github.

Reference
Python script created to scrape the data -> https://github.com/21f3000177/tds_project1/blob/main/scraper_gitbub.py
