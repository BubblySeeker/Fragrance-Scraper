import pandas as pd
from urllib.parse import quote_plus
import re
from bs4 import BeautifulSoup
import requests
import time
import httpx


# Read the Excel file into a DataFrame
df = pd.read_excel('ULTA_fragrance_data.xlsx')

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15'
}

proxyList = ["http://glkudu6cfrjhykw-odds-5+100:zd10erm8tu4ruay@rp.proxyscrape.com:6060",
             "http://glkudu6cfrjhykw-odds-5+100:zd10erm8tu4ruay@rp.proxyscrape.com:6060",
             "http://glkudu6cfrjhykw-odds-5+100:zd10erm8tu4ruay@rp.proxyscrape.com:6060",
             "http://glkudu6cfrjhykw-odds-5+100:zd10erm8tu4ruay@rp.proxyscrape.com:6060",
             "http://glkudu6cfrjhykw-odds-5+100:zd10erm8tu4ruay@rp.proxyscrape.com:6060",
             "http://glkudu6cfrjhykw-odds-5+100:zd10erm8tu4ruay@rp.proxyscrape.com:6060",
             "http://glkudu6cfrjhykw-odds-5+100:zd10erm8tu4ruay@rp.proxyscrape.com:6060",
             "http://glkudu6cfrjhykw-odds-5+100:zd10erm8tu4ruay@rp.proxyscrape.com:6060",
             "http://glkudu6cfrjhykw-odds-5+100:zd10erm8tu4ruay@rp.proxyscrape.com:6060",
             "http://glkudu6cfrjhykw-odds-5+100:zd10erm8tu4ruay@rp.proxyscrape.com:6060",
             "http://glkudu6cfrjhykw-odds-5+100:zd10erm8tu4ruay@rp.proxyscrape.com:6060",
             "http://glkudu6cfrjhykw-odds-5+100:zd10erm8tu4ruay@rp.proxyscrape.com:6060",
             "http://glkudu6cfrjhykw-odds-5+100:zd10erm8tu4ruay@rp.proxyscrape.com:6060",
             "http://glkudu6cfrjhykw-odds-5+100:zd10erm8tu4ruay@rp.proxyscrape.com:6060",
             "http://glkudu6cfrjhykw-odds-5+100:zd10erm8tu4ruay@rp.proxyscrape.com:6060",
             "http://glkudu6cfrjhykw-odds-5+100:zd10erm8tu4ruay@rp.proxyscrape.com:6060",
             "http://glkudu6cfrjhykw-odds-5+100:zd10erm8tu4ruay@rp.proxyscrape.com:6060"]




proxy_index = 0
count = 0

upcList = []
nameList = []
for i in range(316, 916):
    row = df.iloc[i]

    brand = row['Brand']
    name = row['Name']
    size = row['Size']

    search_query = f"{brand} {name} {size}"

    encoded_query = quote_plus(search_query)



    try:

        # Search the website
        search_url = f"https://www.upcitemdb.com/query?s={encoded_query}&type=2"
        time.sleep(3)

        if count % 70 == 0 and count != 0:
            proxy_index = (proxy_index + 1) % len(proxyList)

        current_proxy = proxyList[proxy_index]

        response = httpx.get(search_url, headers=headers, proxies=current_proxy, timeout=3)

        soup = BeautifulSoup(response.content, 'html.parser')

        text = soup.find('div', class_='page-content')
        message = text.find_all('p', class_='detailtitle')
    except:
        upc = "Not Found"
        name = "Not Found"



    #Case for no results
    if len(message) > 1:

            size_full = row['Size']
            size_match = re.search(r'[\d\.]+', str(size_full))
            if size_match:
                size = size_match.group()
                size = int(float(size))

            # Reconstruct the search query
            search_query = f"{brand} {name} {size}"

            # URL-encode the search query
            encoded_query = quote_plus(search_query)

            # Reconstruct the search URL
            search_url = f"https://www.upcitemdb.com/query?s={encoded_query}&type=2"

    time.sleep(5)
    info = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(info.content, 'lxml')

    try:
        # Find the <a> tag with UPC in its href attribute
        upc_link = soup.find('a', href=True, class_='img')

        # Extract the UPC code from the href attribute
        upc = upc_link['href'].split('/')[-1] if upc_link else None

    except:
        upc = "Not Found"
    try:
        name = soup.find('div', class_='rImage').find('p').text.strip()
    except:
        name = "Not Found"


    print(upc)


    upcList.append(upc)
    nameList.append(name)
    count += 1

df = df.assign(UPC=upcList, ProductName=nameList)


output_path = '/Users/rb/Documents/3520/MBF/UltaScrape/untitled/venv/UPCScrape/venv/ULTA_fragrance_data.xlsx'

df.to_excel(output_path, index=False)