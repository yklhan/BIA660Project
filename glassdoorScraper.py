#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv


# In[2]:


from sklearn.feature_extraction.text import CountVectorizer
import lda
import numpy as np


# In[3]:


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


# In[5]:


url='https://www.glassdoor.com/profile/login_input.htm?userOriginHook=HEADER_SIGNIN_LINK'
scrape_page = 10
reviews, pros, cons = scrape(url, scrape_page)


# In[8]:


topic_num=5

#tokenization
tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
                                
#read the dataset                
#docs=open('news.txt').readlines()

#transform the docs into a count matrix
pros_matrix = tf_vectorizer.fit_transform(pros)
cons_matrix = tf_vectorizer.fit_transform(cons)

#get the vocabulary
vocab=tf_vectorizer.get_feature_names()

#initialize the LDA model
pro_model = lda.LDA(n_topics=topic_num, n_iter=250)
con_model = lda.LDA(n_topics=topic_num, n_iter=250)

#fit the model to the dataset
pro_model.fit(pros_matrix)
con_model.fit(cons_matrix)


# In[15]:


topic_keywords = {}
#write the top terms for each topic
top_words_num=3
pro_topic_mixes= pro_model.topic_word_
fw=open('pro_top_terms_per_topic.txt','w')
for i in range(topic_num):#for each topic
    top_indexes=np.argsort(pro_topic_mixes[i])[::-1][:top_words_num]                              
    my_top=''
    for ind in top_indexes:
        my_top+=vocab[ind]+' '
        #print(i, vocab[ind])
        if i in topic_keywords:
            topic_keywords[i].append(vocab[ind])
        else:
            topic_keywords[i] = [vocab[ind]]
    fw.write('TOPIC: '+str(i)+' --> '+str(my_top)+'\n')
fw.close()

doc_topic = {}
doc_top_topic = {}
#write the top topics for each doc
top_topics_num=1
pro_doc_mixes= pro_model.doc_topic_
fw=open('pro_topic_mixture_per_doc.txt','w')
for i in range(len(doc_mixes)):#for each doc
    top_indexes=np.argsort(pro_doc_mixes[i])[::-1][:top_topics_num]     
    my_top=''
    for ind in top_indexes:
        temp_topic = ind
        temp_likelihood = round(pro_doc_mixes[i][ind], 2)
        likelihood_top = -1
        topic_top = -1
        if temp_likelihood > likelihood_top:
            likelihood_top = temp_likelihood
            topic_top = temp_topic
        my_top+=' '+str(ind)+':'+str(round(pro_doc_mixes[i][ind],2))
        #print(i, ind, round(pro_doc_mixes[i][ind], 2))
        if i in doc_topic:
            doc_topic[i].append((ind, round(pro_doc_mixes[i][ind], 2)))
        else:
            doc_topic[i] = [(ind, round(pro_doc_mixes[i][ind], 2))]
    doc_top_topic[i] = topic_top
    fw.write('DOC: '+str(i)+' --> '+str(my_top)+'\n')
fw.close()


# In[16]:


#for each review, find largest portion topic, and count number of reviews under each topic
#find top k(parameter), sort then loop in k
print(topic_keywords)
print(doc_top_topic)


# In[26]:


k_user = 2 #user parameter
invers_count = {}
for key, value in doc_top_topic.items():
    if value in invers_count:
        invers_count[value] += 1
    else:
        invers_count[value] = 1
print(invers_count)
count_dic = {}
for k,v in invers_count.items():
    count_dic[v] = k
print(count_dic)


# In[27]:


for i in range(k_user):
    print("TOP ", i+1, "comments' keywords are ", topic_keywords[count_dic[sorted(count_dic.keys())[-i]]])
    print("e.g. ", )


# In[ ]:




