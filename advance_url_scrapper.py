# Use this automation code for finding all the URLs given in your website after user login so that you can even extract those URLs that need user login for access.
# It uses basic selenium automation for crawling all the URLs found in the starting URL given by the user after which it navigates to other URLs using recursion.
# In this I have even added a login function which will first log into the website after which it will iterate to the URLs and append it to stack.
# It will not quit the driver after each iteration so that the login session doesn't get destroyed.
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
from selenium import webdriver
import csv


# Define the URL_Locater class
# This parent class holds multiple functions for navigating all the URLs:
class URL_Locater:
    def __init__(self):
        self.visited_links = set()
        self.driver = None  # Initialize the driver as a class attribute


    # This function checks that URLs that are navigated by this program belong to same domain, it doesn't navigate to other domains which doesn't belong to the parent domain:
    # Example URL: "testing.com"(suppose parent domain) then all URLs i.e. test.testing.com, dev.testing.com, uat.testing.com etc..
    def is_same_domain(self, url1, url2):
        domain1 = urlparse(url1).netloc.split('.')[-2:]
        domain2 = urlparse(url2).netloc.split('.')[-2:]
        return domain1 == domain2


    # Function to perform login
    def login(self, username, password):
        login_url = 'https://testurl.com/login'
        self.driver.get(login_url)

        # Update the selector to use XPath for both username and password input fields
        username_input = self.driver.find_element(By.XPATH, 'Replace with Xpath of username field')
        password_input = self.driver.find_element(By.XPATH, 'Replace with Xpath of password field')

        username_input.send_keys(username)
        password_input.send_keys(password)

        login_button = self.driver.find_element(By.XPATH, 'Replace with Xpath of LogIn button')
        login_button.click()


    # Function to visit links recursively
    # In this function the recursion limit is set by "max_links" which as of now iterates to 3000 links, by default python only allows a 1000 recursion limit but I have increased it to 3000, you can set it as per your need and URLs that may be exist in your website.
    # Here it uses stack to insert all the URLs found while navigating in a webpage, which will be iterated one by one by popping it from the stack. 
    def visit_links_recursively(self, starting_url, max_links=3000, username=None, password=None, avoid_urls=None):
        
        # Initiate the webdriver: 
        options = Options()
        options.headless = True
        service = Service('# Replace with your path to chromedriver')  
        self.driver = webdriver.Chrome(service=service, options=options)

        if username and password:
            self.login(username, password)

        self.visit_links_iteratively(starting_url, max_links, avoid_urls)


    # Function to visit links iteratively
    def visit_links_iteratively(self, starting_url, max_links=3000, avoid_urls=None):
        stack = [(starting_url, 1)]
        links_visited = 0

        while stack and links_visited < max_links:
            url, depth = stack.pop()
            # It will only visit those URLs which belong to same domain
            # This will avoid visiting those links having 'UTM Source', or ends with (.pdf) or pointing to a div element inside href i.e.(#)[Example: www.testurl.com/gene/example#]
            if (
                depth > max_links
                or url in self.visited_links
                or '#' in url
                or 'utm_source' in url
                or url.endswith(".pdf")
                or (avoid_urls and url in avoid_urls)
            ):
                continue

            # Adding to visiting_link set so that not to visit that URL again:
            self.visited_links.add(url)
            links_visited += 1
            print(f"Visiting: {url}")

            self.driver.get(url)

            links = self.driver.find_elements(By.TAG_NAME, 'a')
            
                #  If links is None, the loop will be skipped, and the code will continue without attempting to iterate over it, preventing the TypeError.
                if links is not None:
                for link in links:
                    href = link.get_attribute('href')
                    # It will only append those URLs which belong to same domain
                    # This will avoid appending those links having 'UTM Source', or ends with (.pdf) or pointing to a div element inside href i.e.(#)[Example: www.testurl.com/gene/example#]
                    if href:
                        # Your existing conditions here
                        if (
                            self.is_same_domain(url, href)
                            and not href.endswith(".pdf")
                            and '#' not in href
                            and 'utm_source' not in href
                            and (avoid_urls is None or href not in avoid_urls)
                        ):
                            if href not in self.visited_links:
                                stack.append((href, depth + 1))

        # Don't quit the driver here to maintain the login session

    
    # Function to save all the visited URLs to a CSV file
    def save_to_csv(self, file_name):
        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Visited URLs'])
            for url in self.visited_links:
                writer.writerow([url])


# Initiate the crawler usage: 
crawler = URL_Locater()
starting_url = 'https://testurl.com'

# Add URLs to avoid in a list if there are multiple, here you can add the URL you need to skip just like the URL which can log-out the user from the login session
avoid_url = 'https://testurl.com/logout'  
crawler.visit_links_recursively(starting_url, username='Replace with real username', password='Replace with real password', avoid_urls=[avoid_url])

# You can change the name of the CSV file from "tracked_urls.csv" to any one that you want, this file contains all the URLs that this automation code fetch from the website which belongs to same domain of the 'starting_url'
crawler.save_to_csv('tracked_urls.csv')
