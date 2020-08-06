#!/usr/bin/env python
# coding: utf-8

# In[70]:


from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv


# In[71]:


def review_clean(text):
    pro = ""
    con = ""
    sents = text.split("\n")
    try:
        pro_index = sents.index("Pros")
        con_index = sents.index("Cons")
    except:
        return pro, con
    for i in range(pro_index+1, con_index):
        pro += sents[i]
    for j in range(con_index+1, len(sents)-1):
        con += sents[j]
    return pro, con


# In[72]:


def scrape(url, pageNum):
    reviews_storage = []
    pros_storage = []
    cons_storage = []
    
    #open the browser and visit the url
    driver = webdriver.Chrome('./chromedriver')
    driver.get(url)
    time.sleep(2)
    print ('attempting to sign in')
            
    driver.find_element_by_id("userEmail").send_keys("gonzalez.o1991@gmail.com")
    driver.find_element_by_id("userPassword").send_keys("SharedPassword1")
    driver.find_element_by_css_selector('button[name="submit"]').click()
    time.sleep(2) 
    
    driver.get('https://www.glassdoor.com/Reviews/Amazon-Reviews-E6036.htm')   
    already_seen=set()#keeps track of reviews we have already seen. 
     
    limit = 0

    reviews=driver.find_elements_by_css_selector('li[class="empReview cf"]')
    print(len(reviews),' Reviews found\n')
    
    while limit < pageNum:
        print("To infinity and beyond! We're getting close, on %d now! page " % (limit))
       
        for review in reviews:
            reviews_storage.append(review)
            pro, con = review_clean(review.text)
            pros_storage.append(pro)
            cons_storage.append(con)
            #print(pro)
            #print(con)
            
        driver.find_element_by_css_selector('a[class="pagination__ArrowStyle__nextArrow  "]').click()
        time.sleep(2)
        print ("entering new page for review mining")
        limit = limit + 1
        reviews=driver.find_elements_by_css_selector('li[class="empReview cf"]')#
        print(len(reviews),' Reviews found\n')

    
    time.sleep(2)
    print('mined all reviews within', pageNum, 'page')
    print(len(reviews_storage), " reviews recorded")
    print(len(pros_storage), " pros recorded")
    print(len(cons_storage), " cons recorded")
    print('done')
    return reviews_storage, pros_storage, cons_storage


# In[73]:


url='https://www.glassdoor.com/profile/login_input.htm?userOriginHook=HEADER_SIGNIN_LINK'
scrape_page = 1
reviews, pros, cons = scrape(url, scrape_page)


# In[ ]:




