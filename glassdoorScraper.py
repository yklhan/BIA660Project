#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.by import By
import time


# In[2]:


#write the content of a list to a txt file with the provided file name
def write_to_file(line_list, file_name):
    with open(file_name, 'w') as writer:
        for line in line_list:
            writer.write(line)
            writer.write('\n')


# In[3]:


#clean the scraped review only keeping the pros and cons seperately
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


# In[4]:


#scrape the reviews of Amazon in n pages
#parameters: url:the login page in Glassdoor website
#            pageNum: how many pages of reviews you want to scrape
def scrape(url, pageNum):
    reviews_storage = []
    pros_storage = []
    cons_storage = []
    
    driver = webdriver.Chrome('./chromedriver')
    driver.get(url)
    time.sleep(2)
    print ('attempting to sign in')
    
    #email and password can be substitued by yours
    driver.find_element_by_id("userEmail").send_keys("gonzalez.o1991@gmail.com")
    driver.find_element_by_id("userPassword").send_keys("SharedPassword1")
    driver.find_element_by_css_selector('button[name="submit"]').click()
    time.sleep(2) 
    
    #the http link can be substitued by the link of another company e.g. Google
    driver.get('https://www.glassdoor.com/Reviews/Amazon-Reviews-E6036.htm')   
    already_seen=set()#keeps track of reviews we have already seen. 
     
    limit = 0

    reviews=driver.find_elements_by_css_selector('li[class="empReview cf"]')
    #print(len(reviews),' Reviews found\n')
    
    while limit < pageNum:
        print("To infinity and beyond! We're getting close, on %d now! page " % (limit))
       
        for review in reviews:
            reviews_storage.append(review.text)
            pro, con = review_clean(review.text)
            pros_storage.append(pro)
            cons_storage.append(con)
            
        driver.find_element_by_css_selector('a[class="pagination__ArrowStyle__nextArrow  "]').click()
        time.sleep(2)
        print ("entering new page for review mining")
        limit = limit + 1
        reviews=driver.find_elements_by_css_selector('li[class="empReview cf"]')#
        #print(len(reviews),' Reviews found\n')

    
    time.sleep(2)
    print('mined all reviews within', pageNum, 'page')
    print(len(reviews_storage), " reviews recorded")
    print(len(pros_storage), " pros recorded")
    print(len(cons_storage), " cons recorded")
    return reviews_storage, pros_storage, cons_storage


# In[5]:


url='https://www.glassdoor.com/profile/login_input.htm?userOriginHook=HEADER_SIGNIN_LINK'
scrape_page = 50 #page number can not be larger than 64 based on test, the scraper is not handling the gmail verification
reviews, pros, cons = scrape(url, scrape_page)


# In[6]:


write_to_file(reviews, 'project_review.txt')
write_to_file(pros, 'project_pro.txt')
write_to_file(cons, 'project_con.txt')


# In[ ]:




