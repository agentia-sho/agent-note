"""This script serves as a skeleton template for synchronous AgentQL scripts."""

import logging
import random
import time
import json

import agentql
from agentql.ext.playwright.sync_api import Page
from playwright.sync_api import sync_playwright

# Set up logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Set the URL to the desired website
URL = "https://note.com/search?context=note_for_sale&q=%E5%BE%A9%E7%B8%81&sort=like"


def key_press_end_scroll(page: Page):
    page.keyboard.press("End")
    page.wait_for_page_ready_state()
    time.sleep(random.uniform(0.5, 1.0))  # Add random delay to appear more human-like


def main():
    with sync_playwright() as p, p.chromium.launch(headless=False) as browser:
        # Create a new page in the browser and wrap it to get access to the AgentQL's querying API
        page = agentql.wrap(browser.new_page())

        # Navigate to the desired URL
        page.goto(URL)

        # Scroll multiple times to load more content
        num_scrolls = 7  # Adjust this number based on how many items you want to load
        for i in range(num_scrolls):
            log.info(f"Scrolling to load more content... ({i+1}/{num_scrolls})")
            key_press_end_scroll(page)

        try:
            get_response(page)
            # Used only for demo purposes. It allows you to see the effect of the script.
            page.wait_for_timeout(10000)  # Wait for 10 seconds
        finally:
            browser.close()


def get_response(page: Page):
    query = """
{
  noteCard[] {
    title
    url
    author {
      name
      url
    }
    price
    createdAt
    likeCount
    thumbnailUrl
    remainingCount
  }
}
    """
    
    try:
        response = page.query_data(query, mode="standard")
        # Print the response in a more readable format
        print(json.dumps(response, indent=2, ensure_ascii=False))
    except Exception as e:
        log.error(f"Query failed: {str(e)}")
        log.info(f"Current URL: {page.url}")


if __name__ == "__main__":
    main()
