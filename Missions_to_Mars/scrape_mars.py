from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


def scrape():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit NASA News on Mars
    url = "https://redplanetscience.com/"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    
    one_title = soup.select_one("div", class_="content_title").get_text()
    print(one_title)
    
    # Collect the latest News Title and Paragraph Text
    news_title = soup.find("div", class_="content_title").get_text()
    news_p = soup.find("div", class_="article_teaser_body").get_text()
    print(f"Title is: {news_title}")
    print(f"Is about: {news_p}")
    
    # Visit Space Images of Mars
    url1 = "https://spaceimages-mars.com/"
    browser.visit(url1)
    
    # Scrape page into Soup
    html1 = browser.html
    jpl_soup = bs(html1, "html.parser")
    
    # Find the image url for the current Featured Mars Image
    image_url = jpl_soup.find("img", class_="headerimage fade-in").get("src")
    print(image_url)
    
    # Save a complete url string for the featured image
    featured_image_url = f"https://spaceimages-mars.com/{image_url}"
    print(featured_image_url)
    
    # Visit the Mars Facts webpage using Pandas to get tables info
    url2 = "https://galaxyfacts-mars.com/"
    tables = pd.read_html(url2)
    tables
    
    # Get Mars data and create a dataframe
    mars_facts = pd.read_html(url2)[0]
    print(mars_facts)
    mars_facts.reset_index(inplace=True)
    mars_facts.columns=["ID", "Properties", "Mars", "Earth"]
    mars_facts
    
    # Convert dataframe into HTML
    html_table = mars_facts.to_html()
    html_table
    
    # Visit Mars Hemispheres webpage
    url3 = "https://marshemispheres.com/"
    browser.visit(url3)
    
    # Scrape page into Soup
    html3 = browser.html
    hemi_soup = bs(html3, "html.parser")
    
    # Create and empty list to store the Hemispheres image URLs
    hemisphere_image_urls =[]

    # Find all the results for the Hemispheres
    results = browser.find_by_tag("a.product-item h3")

    for item in range(len(results)-1):
        hemispheres = {}

        # Find the elements in the loop by clicking
        browser.find_by_tag("a.product-item h3")[item].click()

        # Get Hemisphere Title
        hemispheres["title"] = browser.find_by_tag("h2.title").text

        # Find Sample Image Anchor Tag & Extract <href>
        sample_element = browser.find_link_by_text("Sample").first
        hemispheres["img_url"] = sample_element["href"]

        # Append Hemisphere Object to List
        hemisphere_image_urls.append(hemispheres)

        # Navigate Backwards
        browser.back()
    
    #Image URLs list with keys 'title' and 'img_url'
    hemisphere_image_urls
    
    # Quit the browser after scraping
    browser.quit()

    return_dict = {
        "title": news_title,
        "paragraph": news_p,
        "image_url": featured_image_url,
        "mars_table": html_table,
        "hemispheres": hemisphere_image_urls
    }

    return return_dict

if __name__ == "__main__":
    app.run(debug=True)