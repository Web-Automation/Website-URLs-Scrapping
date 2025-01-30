# Website_URLs_Scrapping
This repository contains two automation scripts for web scraping one for scrapping only public-facing URLs i.e. "scrap_website_urls.py" and other one is advance version i.e. "advance_url_scrapper" that scrap all the public-facing URLs as well as URLs that require user login from a website.

**Normal Automation Script**
- The normal automation script is designed to find all the public-facing URLs on a website that do not require user login.
- It uses basic Selenium automation to crawl through all the URLs starting from a given initial URL provided by the user.
- The script avoids certain types of URLs, such as those with 'UTM Source', URLs ending with '.pdf', and URLs pointing to div elements (e.g., '#'), you can even modify it to avoid any certain type of URLs.
- The script limits the recursion to a specified number of links (default set to 3000).

**Advanced Automation Script**
- The advanced automation script extends the normal script's functionality to include URLs requiring user login.
- It incorporates a login function that logs into the website using the provided credentials before initiating the URL crawling process.
- The script does not quit the WebDriver after each iteration to maintain the login session.
- Similar to the normal script, it avoids certain types of URLs and limits the recursion to a specified number of links, you can even modify it to avoid any certain type of URLs.
- Users can provide URLs to be avoided during the crawling process, which is useful for skipping logout URLs or other specific pages.

## Usage
Install dependencies:

-pip install selenium
-pip install webdriver_manager

**Configuration:**
- Replace the placeholder text in the scripts with your specific details:
- Replace 'https://testurl.com' with the starting URL for both scripts.
- For the advanced script, provide a real username and password where indicated.

**Run the Scripts:**
- Execute the scripts according to your needs:
- For the normal script, run "python scrap_website_urls.py"
- For the advanced script, run "python advance_url_scrapper.py"
  
**Output:**
- The scripts will generate a CSV file named tracked_urls.csv containing all the visited URLs from the website that belongs to the same domain.

**Notes:**
- Ensure that you have the appropriate webdriver executable installed (e.g., chromedriver for Chrome) and provide the path explicitly in the script.

**License**
- This project is licensed under the MIT License - see the LICENSE file for details.

**Acknowledgements**
- Special thanks to the developers of Selenium for providing a powerful web automation library.
- Feel free to contribute and report issues!
