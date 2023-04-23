import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urlparse

"""
Output files:
1- "found-subdomains.csv" includes subdomains WITHOUT redundancy.
2- "all-links.txt" includes all links found.
3- "all-domains.txt" includes all subdomains extracted from links in the pages.

Functions:
1- extract_links() 
2- recursive_extraction()
"""


def extract_links(url):
    src = requests.get(url).content
    soup = BeautifulSoup(src, "lxml")
    anchor_tags = soup.find_all("a")
    links = []
    domainslist = []

    file = open("all-links.txt", "a")
    file_D = open("all-domains.txt", "a")
    for link in anchor_tags:
        href = link.get('href')
        
        parsed_url = urlparse(href)
        domain_name = parsed_url.netloc

        domainslist.append(domain_name)
        for domain in domainslist:
            if "aast" in str(domain):
                file_D.write(domain)
                file_D.write("\n")
        #print (domainslist)
        if href and "aast" in href:
            links.append(href)
        for i in range (len(links)):
            print (links[i])
            file.write(links[i] + "\n")
    return links, domainslist


def recursive_extraction(url, visited_urls=None, extracted_domains=None):

    if visited_urls is None:
        visited_urls = set()
        
    if url in visited_urls:
        return

    visited_urls.add(url)
    links, domainslist = extract_links(url)

    for link in links:
        if link in visited_urls:
            continue

        try:
            src = requests.get(url).content
            soup = BeautifulSoup(src, "lxml")
            if soup.find():
                recursive_extraction(link, visited_urls)
        except:
            continue
            
    if extracted_domains is None:
        extracted_domains = set()
    
    for domain in domainslist:
        if domain in extracted_domains:
            continue
        if "aast" in domain:
            extracted_domains.add(domain)
            with open('./found-subdomains.csv', 'a') as output_file:
                writer = csv.writer(output_file)
                writer.writerow([domain])

recursive_extraction("https://www.aast.edu")
#extract_links("https://www.aast.edu")
