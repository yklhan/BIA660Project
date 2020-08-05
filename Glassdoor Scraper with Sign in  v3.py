


from selenium import webdriver
from selenium.webdriver.common.by import By

#from selenium import webdriver
import time
import csv




# Solves for 2

def scrape(url):
    
     #open the browser and visit the url
    driver = webdriver.Chrome('./chromedriver')
    driver.get(url)
    time.sleep(2)
    print ('attempting to sign in')
            
    x = 1
    driver.find_element_by_id("userEmail").send_keys("gonzalez.o1991@gmail.com")
    driver.find_element_by_id("userPassword").send_keys("SharedPassword1")
    driver.find_element_by_css_selector('button[name="submit"]').click()
    time.sleep(2) 
    
    driver.get('https://www.glassdoor.com/Reviews/Amazon-Reviews-E6036.htm')   
    already_seen=set()#keeps track of reviews we have already seen. 
    already_seen2=set()#keeps track of reviews we have already seen.
    
    # Solves for 1, adjusted to write the tweets to a file with comma delimited 
    fw=open('reviews.csv','w',encoding='utf8')
    writer=csv.writer(fw,delimiter = ',',lineterminator='\n')#create a csv writer for this file
    
    a = 0        
    b = 0 
    z = 0 
    limit = 0

    # Click on a link by xpath
    #driver.find_element_by_xpath("//*[@data-hook='see-all-reviews-link-foot']").click()
    #find all elements that have the value "tweet" for the data-testid attribute
    reviews=driver.find_elements_by_css_selector('li[class="empReview cf"]')#
    print(len(reviews),' Reviews found\n')
    
    x = 1
    while limit <3:
        print("To infinity and beyond! We're getting close, on %d now!" % (x))
        x += 1                                                                               
        z = 0 
        print(limit)
       
    #for i in range(2):     
    #for i in range(2):
        for review in reviews:
            print(z)
            z = z + 1 
            if review in already_seen:continue #we have seen this review before while scrolling down, ignore
            already_seen.add(review) #first time we see this review. Mark as seen and process.
                 
            # NEED TO ADD THE EXTRA FUNCTIONS HERE DEPENDONG ON WHATS BEING ASKED TO BE RETURNED. 
            pro,con='NA','NA'
                 
            
                 
                
            try: 
                #txt=review.find_element_by_css_selector('div[data-hook="review-collapsed"]').text
                #pro=review.find_element_by_css_selector('div[class="gdReview"]').text
                pro=review.find_element_by_css_selector('div[class="v2__EIReviewDetailsV2__fullWidth "]').text
                
                    #txt=txt.replace('\n', ' ')
                a = a + 1
                print (a)
                print (pro)
            except: 
                print ('no pro') 
                a = a + 1
                        

            
            try: 
                        
                # star=review.find_element_by_css_selector('i[data-hook="review-star-rating"]').text            
                #star=driver.find_element_by_xpath('//span[@class="a-icon-alt"]')                           
                #star=review.find_element_by_xpath('//p[@class="a-icon-alt"]').get_attribute('innerHTML')
                #star=review.find_element_by_css_selector('span[class="rating"]').get_attribute('innerHTML')            
                #con=review.find_element_by_css_selector('div[class="v2__EIReviewDetailsV2__fullWidth "]').text
                con=review.find_element_by_css_selector('div[class="gdReview"]').text
                #star=review.find_element(By.xpath("//span[@class='a-icon-alt']"))
                #star= stars.getAttribute("innerHTML");
                b = b + 1
                #print (b)
                #print (stars)
                print (con)
                #stard=stars.find_element_by_css_selector('span[class="a-icon-alt"]')
                #for star in stard:
                    #    return (star.text)
            
            
                #code to clean out of 5 stars out. 
                #review_rating = ''.join(raw_review_rating).replace('out of 5 stars','')
            
                           
            except: 
                print ('no con')
                b = b + 1 
                print (b)
                print (con)  
              
            
              
                      
    
            
            if pro!='NA': 
                writer.writerow([pro,con]) 
                
                
            if z == 10:
                driver.find_element_by_css_selector('a[class="pagination__ArrowStyle__nextArrow  "]').click()
                time.sleep(2)
                print ("entering new page for review mining")
                limit = limit + 1
                reviews=driver.find_elements_by_css_selector('li[class="empReview cf"]')#
                print(len(reviews),' Reviews found\n')

    
    time.sleep(2)
    fw.close()
    print('mined all reviews')
    print('done')

    

    
    
    
url='https://www.glassdoor.com/profile/login_input.htm?userOriginHook=HEADER_SIGNIN_LINK'
#url='https://www.amazon.com/dp/B0876VSV95/ref=sspa_dk_detail_1?psc=1&pd_rd_i=B0876VSV95&pd_rd_w=GZzCW&pf_rd_p=a64be657-55f3-4b6a-91aa-17a31a8febb4&pd_rd_wg=2MgPd&pf_rd_r=BZY0S7M2WH90PG1FC57G&pd_rd_r=cb0feeda-ce3b-467d-ab46-ca58c5cd6276&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEzNThJMEpNM0FKQ0xHJmVuY3J5cHRlZElkPUEwMzI3MTE0Mkw2RUQ1SVlFMUtUSyZlbmNyeXB0ZWRBZElkPUEwNDUyMjk1MlFPVlJHVDhPM0FFUSZ3aWRnZXROYW1lPXNwX2RldGFpbF90aGVtYXRpYyZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU='

scrape(url)