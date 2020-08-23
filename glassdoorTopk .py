#!/usr/bin/env python
# coding: utf-8

# In[1]:


from sklearn.feature_extraction.text import CountVectorizer
import lda
import numpy as np


# In[2]:


def read_from_file(file_name):
    with open(file_name, 'r') as reader:
        line_list = reader.readlines()
    line_list = [x.strip() for x in line_list]
    return line_list


# In[9]:


#parameters:
# data_list:a list, elements can be all pro reviews in string or con reviews in string
# flag: indicate data_list is about pros or cons for intermediated data storage: true for pro, false for con
# topic_num: how many topic generated from all pros or cons in total
# top_words_num: how many words used to describe one topic
# top_topics_num: how many topics used to describe one document !!! can not be larger than topic_num
# k_user: number of nost prevelent reviews extracted based on topic, !!! can not be larger than topic_num
# console output
def printTopk(data_list, topic_num, top_words_num, top_topics_num, k_user, flag):
    if k_user > topic_num or top_topics_num > topic_num:
        print("----------------------------------------------")
        print("parameters error.")
        print("----------------------------------------------")
        return
    tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
    
    #transform the docs into a count matrix
    #get the vocabulary
    matrix = tf_vectorizer.fit_transform(data_list)
    vocab = tf_vectorizer.get_feature_names()
    
    #initialize the LDA model
    model = lda.LDA(n_topics=topic_num, n_iter=500)
    
    #fit the model to the dataset
    model.fit(matrix)
    
    if flag:
        term_topic_name = 'pro_top_terms_per_topic.txt'
        topic_doc_name = 'pro_topic_mixture_per_doc.txt'
    else:
        term_topic_name = 'con_top_terms_per_topic.txt'
        topic_doc_name = 'con_topic_mixture_per_doc.txt'
    
    #processing using fitted model
    topic_keywords = {}

    #write the top terms for each topic
    #ancillary
    topic_mixes = model.topic_word_
    fw = open(term_topic_name,'w')
    for i in range(topic_num):#for each topic
        top_indexes=np.argsort(topic_mixes[i])[::-1][:top_words_num]                              
        my_top=''
        for ind in top_indexes:
            my_top += vocab[ind]+' '
            if i in topic_keywords:
                topic_keywords[i].append(vocab[ind])
            else:
                topic_keywords[i] = [vocab[ind]]
        fw.write('TOPIC: '+str(i)+' --> '+str(my_top)+'\n')
    fw.close()

    doc_topic = {}
    doc_top_topic = {}
    #write the top topics for each doc
    doc_mixes= model.doc_topic_
    fw=open(topic_doc_name,'w')
    for i in range(len(doc_mixes)):#for each doc
        top_indexes=np.argsort(doc_mixes[i])[::-1][:top_topics_num]     
        my_top=''
        for ind in top_indexes:
            temp_topic = ind
            temp_likelihood = round(doc_mixes[i][ind], 2)
            likelihood_top = -1
            topic_top = -1
            if temp_likelihood > likelihood_top:
                likelihood_top = temp_likelihood
                topic_top = temp_topic
            my_top+=' '+str(ind)+':'+str(round(doc_mixes[i][ind],2))
            if i in doc_topic:
                doc_topic[i].append((ind, round(doc_mixes[i][ind], 2)))
            else:
                doc_topic[i] = [(ind, round(doc_mixes[i][ind], 2))]
        doc_top_topic[i] = topic_top
        fw.write('DOC: '+str(i)+' --> '+str(my_top)+'\n')
    fw.close()
    
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

    if flag:
        print("Pros:")
    else:
        print("Cons:")
    for i in range(k_user):    
        l = len(count_dic.keys())
        i_topicNum = count_dic[sorted(count_dic.keys())[l-i-1]]  
        print("TOP ", i+1, " comments' keywords are ", topic_keywords[i_topicNum])

        for docj, portion in doc_topic.items():
            for j, posb in portion:
                if j == i_topicNum and posb > 0.8:
                    if flag:
                        print("e.g. ", pros[docj])
                    else:
                        print("e.g. ", cons[docj])


# In[10]:


pros =read_from_file('project_pro.txt')
cons = read_from_file('project_con.txt')
#pre-decided by the requirement of LDA algorithm
topic_num=5
top_words_num=3
top_topics_num=3 #!!! can not be larger than topic_num
k_user = 2 #user parameter !!! can not be larger than topic_num
printTopk(pros, topic_num, top_words_num, top_topics_num, k_user, True)
printTopk(cons, topic_num, top_words_num, top_topics_num, k_user, False)

