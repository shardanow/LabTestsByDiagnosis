import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import csv

# File path for the output
output_file_path = "./output/tests_list.csv"
completion_flag = './output/processing_done.flag'

# Check if the file already exists
if os.path.exists(output_file_path):
    print(f"File '{output_file_path}' already exists. Skipping parsing.")
else:
    # Selenium setup
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")

    # Use options directly instead of desired_capabilities
    driver = webdriver.Chrome(options=options)

    url = "https://www.synevo.ua/ru/rubricator/substance/blood"

    try:
        # Open the page
        driver.get(url)

        print("Page loaded.")

        # Wait for the table to load
        wait = WebDriverWait(driver, 30)  # Increased timeout
        table = wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='accordion-2__item__content']"))
        )

        print("Table loaded.")

        # Find table rows
        rows = table.find_elements(By.XPATH, "//table[@class='search__results__table']//tr[@class='search__results__table__tr ']")

        print(f"Found {len(rows)} rows.")

        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

        # Open CSV file for writing
        with open(output_file_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Link", "Code", "Name", "Price"])  # Header row

            # Extract data
            for index, row in enumerate(rows, start=1):  # `start=1` makes index 1-based
                print(f"Processing row {index} of {total_rows}...")

                link_tag = row.find_element(By.TAG_NAME, "a")
                link = link_tag.get_attribute("href")
                code_name = link_tag.text

                # Split code and name
                code, name = code_name.split(" ", 1)

                # Extract price
                price_div = row.find_element(By.CLASS_NAME, "search__results__table-price")
                price = price_div.find_element(By.TAG_NAME, "b").text

                # Write to CSV
                writer.writerow([link, code, name, price])

        # Create the completion flag
        with open(completion_flag, 'w') as f:
            f.write("done")

        print(f"Data saved to '{output_file_path}'.")

    except Exception as e:
        # Save a screenshot for debugging
        driver.save_screenshot("debug_screenshot.png")
        print(f"Error: {e}")

    finally:
        driver.quit()
