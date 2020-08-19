#!/usr/bin/env python
# coding: utf-8

# In[1]:


from sklearn.feature_extraction.text import CountVectorizer
import lda
import numpy as np

k_user = 2

# In[2]:


def read_from_file(file_name):
    with open(file_name, 'r') as reader:
        line_list = reader.readlines()
    line_list = [x.strip() for x in line_list]
    return line_list


# In[3]:


pros =read_from_file('project_pro.txt')
cons = read_from_file('project_con.txt')


# In[4]:


#pre-decided by the requirement of LDA algorithm
topic_num=5

#tokenization
pros_tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
cons_tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')                               

#transform the docs into a count matrix
#get the vocabulary
pros_matrix = pros_tf_vectorizer.fit_transform(pros)
pros_vocab = pros_tf_vectorizer.get_feature_names()

cons_matrix = cons_tf_vectorizer.fit_transform(cons)
cons_vocab = cons_tf_vectorizer.get_feature_names()

#initialize the LDA model
pro_model = lda.LDA(n_topics=topic_num, n_iter=500)
con_model = lda.LDA(n_topics=topic_num, n_iter=500)

#fit the model to the dataset
pro_model.fit(pros_matrix)
con_model.fit(cons_matrix)


# In[5]:


#process pros
topic_keywords = {}
#write the top terms for each topic
#ancillary
top_words_num=3
pro_topic_mixes= pro_model.topic_word_
fw=open('pro_top_terms_per_topic.txt','w')
for i in range(topic_num):#for each topic
    top_indexes=np.argsort(pro_topic_mixes[i])[::-1][:top_words_num]                              
    my_top=''
    for ind in top_indexes:
        my_top+=pros_vocab[ind]+' '
        if i in topic_keywords:
            topic_keywords[i].append(pros_vocab[ind])
        else:
            topic_keywords[i] = [pros_vocab[ind]]
    fw.write('TOPIC: '+str(i)+' --> '+str(my_top)+'\n')
fw.close()

doc_topic = {}
doc_top_topic = {}

#write the top topics for each doc
top_topics_num=3
pro_doc_mixes= pro_model.doc_topic_
fw=open('pro_topic_mixture_per_doc.txt','w')
for i in range(len(pro_doc_mixes)):#for each doc
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
        if i in doc_topic:
            doc_topic[i].append((ind, round(pro_doc_mixes[i][ind], 2)))
        else:
            doc_topic[i] = [(ind, round(pro_doc_mixes[i][ind], 2))]
    doc_top_topic[i] = topic_top
    fw.write('DOC: '+str(i)+' --> '+str(my_top)+'\n')
fw.close()


# In[12]:


#print out the top k pros

invers_count = {}
for key, value in doc_top_topic.items():
    if value in invers_count:
        invers_count[value] += 1
    else:
        invers_count[value] = 1

count_dic = {}
for k,v in invers_count.items():
    count_dic[v] = k

for i in range(k_user):    
    l = len(count_dic.keys())
    i_topicNum = count_dic[sorted(count_dic.keys())[l-i-1]]                
    print("TOP ", i+1, " pro comments' keywords are ", topic_keywords[i_topicNum])
    
    for docj, portion in doc_topic.items():
        for j, posb in portion:
            if j == i_topicNum and posb > 0.8:
                print("e.g. ", pros[docj])


# In[13]:


#process cons
topic_keywords = {}
#write the top terms for each topic
#ancillary
top_words_num=3
con_topic_mixes= con_model.topic_word_
fw=open('con_top_terms_per_topic.txt','w')
for i in range(topic_num):#for each topic
    top_indexes=np.argsort(con_topic_mixes[i])[::-1][:top_words_num]                              
    my_top=''
    for ind in top_indexes:
        my_top+=cons_vocab[ind]+' '
        if i in topic_keywords:
            topic_keywords[i].append(cons_vocab[ind])
        else:
            topic_keywords[i] = [cons_vocab[ind]]
    fw.write('TOPIC: '+str(i)+' --> '+str(my_top)+'\n')
fw.close()

doc_topic = {}
doc_top_topic = {}
#write the top topics for each doc
top_topics_num=3
con_doc_mixes= con_model.doc_topic_
fw=open('con_topic_mixture_per_doc.txt','w')
for i in range(len(con_doc_mixes)):#for each doc
    top_indexes=np.argsort(con_doc_mixes[i])[::-1][:top_topics_num]     
    my_top=''
    for ind in top_indexes:
        temp_topic = ind
        temp_likelihood = round(con_doc_mixes[i][ind], 2)
        likelihood_top = -1
        topic_top = -1
        if temp_likelihood > likelihood_top:
            likelihood_top = temp_likelihood
            topic_top = temp_topic
        my_top+=' '+str(ind)+':'+str(round(con_doc_mixes[i][ind],2))
        if i in doc_topic:
            doc_topic[i].append((ind, round(con_doc_mixes[i][ind], 2)))
        else:
            doc_topic[i] = [(ind, round(con_doc_mixes[i][ind], 2))]
    doc_top_topic[i] = topic_top
    fw.write('DOC: '+str(i)+' --> '+str(my_top)+'\n')
fw.close()

#print out top k cons

invers_count = {}
for key, value in doc_top_topic.items():
    if value in invers_count:
        invers_count[value] += 1
    else:
        invers_count[value] = 1

count_dic = {}
for k,v in invers_count.items():
    count_dic[v] = k

for i in range(k_user):
    l = len(count_dic.keys())
    i_topicNum = count_dic[sorted(count_dic.keys())[l-i-1]]                
    print("TOP ", i+1, " con comments' keywords are ", topic_keywords[i_topicNum])
    
    for docj, portion in doc_topic.items():
        for j, posb in portion:
            if j == i_topicNum and posb > 0.8:
                print("e.g. ", cons[docj])


# In[ ]:




