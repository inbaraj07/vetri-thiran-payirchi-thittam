from urllib.parse import quote_plus
PLATFORMS={'Amazon':'https://www.amazon.in/s?k={q}','Flipkart':'https://www.flipkart.com/search?q={q}','IKEA':'https://www.ikea.com/in/en/search/?q={q}','Swiggy':'https://www.swiggy.com/search?query={q}','Zomato':'https://www.zomato.com/search?query={q}','OYO':'https://www.oyorooms.com/search?location={q}'}
def search_url(platform,query): return PLATFORMS.get(platform,PLATFORMS['Amazon']).format(q=quote_plus(query))
