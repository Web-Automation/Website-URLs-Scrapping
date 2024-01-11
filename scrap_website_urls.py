# Use this code for finding all the public facing URLs given in your website that doesn't require user login.
# It uses basic selenium automation for crawling all the URLs find in the starting URL given by user after which it naviagates to other URLs using recursion.
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from urllib.parse import urlparse
import csv


# This parent class which holds multiple functions for navigating all the URLs:
class URL_Locater:
    def __init__(self):
        # To ensure the program don't stuck in a loop by iterating the same URL again and again so here I have define a set that stores all the URLs that has been visited by the program.
        self.visited_links = set()

# This function checks that URLs that're navigating by this program belongs to same domain, it doesn't navigate to other domain which doesn't belong to the parent domain:
# Example URL: "testing.com"(suppose parent domain) then all URLs i.e. test.testing.com, dev.testing.com, uat.testing.com etc..
    def is_same_domain(self, url1, url2):
        domain1 = urlparse(url1).netloc.split('.')[-2:]  # Extract domain components
        domain2 = urlparse(url2).netloc.split('.')[-2:]
        return domain1 == domain2

# In this function the recursion limit is set by "max_links" which as of now iterartes to 3000 links, by default python only allows 1000 recursion limit but I have increase it to 3000, you can set it as per your need and URLs that may be exist in your website.
# Here it is using stack to insert all the URLs found while navigating in a webpage, which will be iterated one by one by poping it from stack. 
    def visit_links_iteratively(self, starting_url, max_links=3000):
        stack = [(starting_url, 1)]
        links_visited = 0

        while stack and links_visited < max_links:
            url, depth = stack.pop()
            if depth > max_links or url in self.visited_links or '#' in url or 'utm_source' in url or url.endswith(".pdf"):
                continue

            self.visited_links.add(url)
            links_visited += 1
            print(f"Visiting: {url}")

            # Set up the webdriver: 
            options = Options()
            options.headless = True
            service = Service('# Replace with your path to chromedriver')  
            driver = webdriver.Chrome(service=service, options=options)
            driver.get(url)

            links = driver.find_elements(By.TAG_NAME, 'a')
            for link in links:
                href = link.get_attribute('href')
                if href and self.is_same_domain(url, href) and not href.endswith(".pdf") and '#' not in href and 'utm_source' not in href:
                    if href not in self.visited_links:
                        stack.append((href, depth + 1))

            driver.quit()

    def visit_links_recursively(self, starting_url, max_links=3000):
        self.visit_links_iteratively(starting_url, max_links)

# This function is sued to store all the visited URLs or the URLs that has been found by the code in a CSV file.
    def save_to_csv(self, file_name):
        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Visited URLs'])
            for url in self.visited_links:
                writer.writerow([url])


# Usage:
crawler = URL_Locater()
starting_url = 'https://testurl.com '
crawler.visit_links_recursively(starting_url)
# You can change the name of the CSV file from "tracked_urls.csv" to any one that you want, this file contains all the URLs that this automation code fetch from the website which belongs to same domain of the 'starting_url'
crawler.save_to_csv('tracked_urls.csv')
