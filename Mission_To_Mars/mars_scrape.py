from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time
import requests as req

def init_browser():
   # @NOTE: Path to my chromedriver in the homework folder
   executable_path = {"executable_path": 'C:/bin/chromedriver'}
   return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser=init_browser()     
    
    ########NASA Mars News
    
    #URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html=browser.html
    time.sleep(4)
    soup = BeautifulSoup(html, 'html.parser')
    time.sleep(10)
    #Latest article title
    news_title =soup.find('div', class_='list_text').find("a")
    print(news_title.text)
    news_p =soup.find ('div', class_='article_teaser_body')
    print(news_p.text)


    
    #JPL Mars Space Images - Featured Image
    # Visit url for JPL Featured Space Image
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)

    # Click FULL IMAGE
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(4)

    # Go to 'more info'
    browser.click_link_by_partial_text('more info')

    # Parse HTML 
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    time.sleep(4)

    # Scrape the URL
    img_sub_url = soup.find('figure', class_='lede').a['href']
    image_full_url = f'https://www.jpl.nasa.gov{img_sub_url}'
    print(image_full_url)   
      
    
    #Mars Weather
    
    tweet_url = "https://twitter.com/marswxreport?lang=en"
    twitter_response = req.get(tweet_url)
    twitter_soup = BeautifulSoup(twitter_response.text, 'html.parser')
    tweets = twitter_soup.find_all('div', class_="js-tweet-text-container")
   
    # Loop through latest tweets and find the tweet that has weather information
    for tweet in tweets: 
       mars_weather = tweet.find('p').text
       if 'sol' and 'pressure' in mars_weather:
          print(mars_weather)
          break
       else: 
          pass          
      
    
    #Mars Fact
    # Visit Mars Facts webpage for interesting facts about Mars
    
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    html = browser.html
    time.sleep(10)
    
    # Use Pandas to scrape the table containing facts about Mars
    
    table = pd.read_html(facts_url)
    time.sleep(5)
    mars_facts_df = table[0]

    # Rename columns
    
    mars_facts_df.columns = ['Category','Value']
    mars_facts_df.set_index("Category", inplace=True)

    # Use Pandas to convert the data to a HTML table string
    html_table = mars_facts_df.to_html(table_id='scrape_table')
    print(html_table)
    

       
    #Mars Hemispheres    
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)

    html = browser.html
    time.sleep(4)
    soup = BeautifulSoup(html, 'html.parser')
    time.sleep(4)

    hemisphere_image_urls = []

    hemisphere_titles = soup.find_all('h3')

    for i in range(len(hemisphere_titles)):
        hemis_title = hemisphere_titles[i].text
        print(hemis_title)
        
        hemis_images = browser.find_by_tag('h3')
        hemis_images[i].click()
        
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        time.sleep(4)
        
        img_url = soup.find('img', class_='wide-image')['src']
        img_url = "https://astrogeology.usgs.gov" + img_url
        print(img_url)
        
        hemis_dict = {"title": hemis_title, "img_url":img_url}
        hemisphere_image_urls.append(hemis_dict)
        
        browser.back()


  # Store data in a dictionary
    mars_data = {
       #News Title
       "news_title": news_title.text,
       #News Title
       "news_p": news_p.text,
       #Featured Image
       "featured_image_url": image_full_url,
       #Mars Weather
       "mars_weather": mars_weather,  
       #Mars Facts
       "html_table":html_table,
       #Mars Four Hemispheres
       "hemisphere_image_urls":hemisphere_image_urls
    }
    print(mars_data)

    browser.quit()
    
    return mars_data