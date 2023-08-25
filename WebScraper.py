# Required Libraries: Selenium, Chrome Driver, and Beautiful Soup. 

# ChromeDriver is a separate executable that Selenium WebDriver uses to control Chrome to scrape websites.
# BeautifulSoup extracts content from HTML pages. 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException
import random
import requests

# Prompting the user to select an interest that will then be compared to a random tweet to see compatibility.
def select_interest():
    print("Please select an interest:")
    print("1. Technology")
    print("2. Music")
    print("3. Movie")
    print("4. Art")
    # Ensures the input is a number between 1 and 4. 
    while True:
        try:
            interest = int(input("Enter the number corresponding to your interest: "))
            if 1 <= interest <= 4:
                return interest
            else:
                print("Invalid selection. Please enter a number between 1 and 4.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

# Display interest options and get user input
interest = select_interest()

# Interest mapping
interest_mapping = {
    1: "Technology",
    2: "Music",
    3: "Movie",
    4: "Art"
}

# Store selected interest and display choice to user 
selected_interest = interest_mapping[interest]
print(f"You've selected {selected_interest}. Please wait for the random tweet to load.")

# Configuring the options for the Chrome WebDriver in Selenium. 
options = Options()
# Runs the browser in "headless" mode, meaning the browser's graphical user interface is not displayed.  
options.add_argument('--headless')
# Opens the browser in incognito mode to avoid tampering with browsing history. 
options.add_argument("--incognito")
# Disables the use of GPU (Graphics Processing Unit) acceleration in the browser  to prevent compatibility issues.
options.add_argument('--disable-gpu')
# Disables the sandboxing of the browser process to avoid issues. 
options.add_argument('--no-sandbox')
# Disables the use of the "/dev/shm" shared memory space to prevent memory allocation issues.
options.add_argument('--disable-dev-shm-usage')
# Twitter uses JavaScript. This option enables JavaScript execution in the browser to ensure the page is functional. 
options.add_argument('--enable-javascript')





# Selecting a random URL to scrape data from. No information about the user is displayed in the output. 
url = "https://twitter.com/TomCruise"
# Establishes chrome driver and leads to URL
driver = webdriver.Chrome(options=options)
driver.get(url)


try:
    # Wait for up to 60 seconds for the presence of a specific element on the page
    WebDriverWait(driver, 60).until(
        # Check for the presence of a tweet
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweet"]'))
    )
except (WebDriverException, TimeoutException) as e:
    # Prints error message if an exception occurs while waiting for the element or if a timeout occurs
    print("An error occurred while waiting for tweets to load:", str(e))
    # Close the browser window (WebDriver)
    driver.quit()
    # Exit the script immediately
    exit()

# Capture HTML after loading
html_content = driver.page_source
soup = BeautifulSoup(html_content, 'html.parser')

# Find all tweet text elements
posts = soup.find_all(attrs={'data-testid': 'tweetText'})

# Display error message if no tweets are found. 
if not posts:
    print("No tweets found.")
else:
    # Choose a random tweet from page
    random_index = random.randint(0, len(posts) - 1)

    # Get text of the randomly chosen tweet
    random_tweet_text = posts[random_index].get_text()

    # Print the random tweet
    print("Random Tweet:")
    print(random_tweet_text)
    print("=" * 50)

# Close the browser window
driver.quit()

# HuggingFace machine learning model that checks if text and a given parameter are related. 
API_URL = "https://api-inference.huggingface.co/models/cross-encoder/nli-deberta-base"

# Set authorization token for API access
headers = {"Authorization": "Bearer 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"}

# Define a function to query the API with payload and return JSON response
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Query the API with random_tweet_text and selected_interest
output = query({
    "inputs": random_tweet_text,
    "parameters": {"candidate_labels": selected_interest},
})

# Check if a compatibility score exists in the output
if "scores" in output and len(output["scores"]) > 0:
    scores = output["scores"]
    print("Score:", scores)

    # Checks if a text/parameter pair yielded a compatibility score greater than 0.5 (50% likelihood that the text and parameter are related)
    if any(score > 0.5 for score in scores):
        print("The random tweet and your interest are related!")
    else:
        print("The random tweet and your interest are not related.")
