# BIA660Project
* python 3.7.4
# Glassdoor reviews scraper and topic analysis
* Scraper: run glassdoorScraper.py
* scrapes k pages reviews from the Glassdoor website
* store full review including review stars, texts, and etc. in 'project_review.txt'; Pros in 'project_pro.txt'; Cons in 'project_con.txt'
* Parameters:
* - url: constant, fixed, the url of the Glassdoor login page
* - email: an registered email address for login
* - password: password for login
* - companyUrl: url of the review page of the company you want to scrape !!! no larger than 64 due to website defense algorithm
*
* Report Top k Comments: run glassdoorTopk.py
* read pros and cons from text files
* generate the topics for each review and classify the documents based on the topics by lda package in python
* choosing the top k prevalent topics
* console print out the top k topics and its corresponding examples
* Parameters:
* - k_user: the value of the k !!! no larger than topic_num
* - topic_num: how many topics generated from the corpus
* - top_topics_num: how many topics a review is assigned to !!! no larger than topic_num
* - top_words_num: how many keywords describes one topic
# Packages
* selenium
* lda
* sklearn
* numpy
# Example Results for Amazon
* prosCapture.png and consCapture.png
* Or check the glassdoorTopk.ipynb including the code and the sample output
# Sample Source Data
* full review including review stars, texts, and etc. in 'project_review.txt'
* Pros in 'project_pro.txt'
* Cons in 'project_con.txt'

