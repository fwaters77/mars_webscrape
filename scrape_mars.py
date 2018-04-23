# Dependencies

from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
from selenium import webdriver

def scrape():

    # Mars info dictionary
    mars_scrape = {}
    
    ########################
    ### SCRAPE MARS NEWS ###
    ########################
    
    # Mars news URL
    news_url = "https://mars.nasa.gov/news/"
    
    # Retrieve page
    news_html = requests.get(news_url)
    
    # Create & parse BeautifulSoup object
    soup = BeautifulSoup(news_html.text, 'html.parser')
    
    # Headline of first news article
    news_title = soup.find('div', class_ = "content_title").text.strip("\n")
    mars_scrape['news_title'] = news_title
    
    # Paragraph text of first news article
    news_p = soup.find('div', class_ = "rollover_description_inner").text.strip("\n")
    mars_scrape['news_para'] = news_p
    
    ######################################
    ### SCRAPE JPL FEATURED MARS IMAGE ###
    ######################################
    
    # JPL URL
    pic_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    
    # Navigate to site
    browser = Browser('chrome', headless=False)
    browser.visit(pic_url)
    
    # Click to see full-size image
    browser.click_link_by_partial_text('FULL IMAGE')
    
    # Retrieve page
    pic_html = browser.html
    
    # Create & parse BeautifulSoup object
    soup = BeautifulSoup(pic_html, 'html.parser')
    
    # Image URL
    img = soup.find('a', class_ = 'button fancybox')['data-fancybox-href']
    img_url = "https://www.jpl.nasa.gov" + img
    
    # Add to mars dictionary
    mars_scrape['feat_img'] = img_url
    
    ###########################
    ### SCRAPE MARS WEATHER ###
    ###########################
    
    # Mars news URL
    weath_url = "https://twitter.com/marswxreport?lang=en"
    
    # Retrieve page
    weath_html = requests.get(weath_url)
    
    # Create & parse BeautifulSoup object
    soup = BeautifulSoup(weath_html.text, 'html.parser')
    
    # Grab recent tweets
    tweets = soup.find_all('p')[0:10]
    
    # Grab only weather tweets
    weather_tweets = []
    
    for tweet in tweets:
        split_tweet = tweet.text.split()
        if split_tweet[0] == 'Sol':
            weather_tweet = ' '.join(split_tweet)
            weather_tweets.append(weather_tweet)
            
    # Most recent weather tweet
    mars_weather = weather_tweets[0]
    
    # Add to mars dictionary
    mars_scrape['weather'] = mars_weather
    
    #########################
    ### SCRAPE MARS FACTS ###
    #########################
    
    # URL
    fact_url = "https://space-facts.com/mars/"
    
    # Get table
    table = pd.read_html(fact_url)
    table = pd.DataFrame(table[0]).set_index(0)
    
    # Convert table to HTML string
    table_html = table.to_html(header = False) \
    .replace('\n  ','').replace('<table border="1" class="dataframe">','') \
    .replace('</table','').replace('\n>','')
    
    # Add to mars dictionary
    mars_scrape['facts'] = table_html
    
    ###################################
    ### SCRAPE MARS HEMISPHERE PICS ###
    ###################################
    
    # USGS Astrogeology
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    
    # Navigate to site
    browser = Browser('chrome', headless=False)
    browser.visit(hemi_url)
    
    # Empty list of hemisphere dictionaries
    hemisphere_image_urls = []
    
    # Go through all 4 images
    hemi = 1
    while hemi < 5:
        # Empty dictionary
        hemi_dict = {}
        
        # Click to enhanced image
        browser.click_link_by_partial_text('Hemisphere Enhanced')
        
        # Link of enhanced image page -> soup
        soup = BeautifulSoup(browser.html, 'html.parser')
        
        # Title
        title = soup.find('div', class_ = 'content')
        hemi_dict['title'] = title.find('h2', class_ = 'title').text
        
        # Image
        download_box = soup.find('div', class_ = 'downloads')
        hemi_dict['img_url'] = download_box.find('a')['href']
        
        # Append title and image to dictionary
        hemisphere_image_urls.append(hemi_dict)
        
        browser.back
        
        # Increment hemisphere count
        hemi += 1
    
    # Add to mars dictionary
    mars_scrape['hemis'] = hemisphere_image_urls

    return mars_scrape