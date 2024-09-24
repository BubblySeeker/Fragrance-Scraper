import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from urllib.parse import unquote, urlparse, parse_qs

#request to send to website
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15'
}


#ulta beauty url
baseurl = "https://www.ulta.com/shop/fragrance/all"


productLink = []

#loop through each page of Ulta
for x in range(1, 19):
    r = requests.get(f'https://www.ulta.com/shop/fragrance/all?page={x}')
    soup = BeautifulSoup(r.content, 'lxml')

    #find all the item card for the fragrances
    productList = soup.find_all('div', class_='ProductCard')


    #loop through each item and get the a link to the product page
    #ProductLink is a list of all the product page Links
    for item in productList:
        for link in item.find_all('a', href = True):
            productLink.append(link['href'])


FragranceList = []
#For each product link extract the info
for product_page_link in productLink:
    r = requests.get(product_page_link, headers=headers)

    soup = BeautifulSoup(r.content, 'lxml')

    #Most products have more link for the sizes
    #sizeLink has the links to all the sizes of the colognes
    sizeLink = []
    sizelist = soup.find_all('ul', class_='PillSelector__pills--inline')

    for item in sizelist:
        for link in item.find_all('a', href = True):
            sizeLink.append(link['href'])



    #Now for each size link retrieve the data
    for link in sizeLink:

        size_page = requests.get(link, headers=headers)
        size_soup = BeautifulSoup(size_page.content, 'lxml')

        brand = size_soup.find('div', class_='ProductInformation').find('span', class_='Text-ds Text-ds--body-1 Text-ds--left Text-ds--black').text.strip()
        name = size_soup.find('div', class_='ProductInformation').find('span', class_='Text-ds Text-ds--title-5 Text-ds--left Text-ds--black').text.strip()
        product_pricing = size_soup.find('div', class_='ProductPricing')
        try:
            price = product_pricing.find(
                'span', class_='Text-ds Text-ds--title-5 Text-ds--left Text-ds--black').text.strip()
        except AttributeError:
            try:
                price = product_pricing.find(
                    'span', class_='Text-ds Text-ds--body-3 Text-ds--left Text-ds--neutral-600 Text-ds--line-through').text.strip()
            except AttributeError:
                price = 'Price not found'

        size_tag = size_soup.find('a', attrs={'aria-current': 'true'})
        size = size_tag.text.strip()


        Fragrance = {
            'Brand': brand,
            'Name': name,
            'Price': price,
            'Size': size,
        }

        FragranceList.append(Fragrance)
        print("Saving:", Fragrance)

df = pd.DataFrame(FragranceList)


df.to_excel('ULTA_fragrance_data.xlsx', index=False)







