import os
import time
import pandas as pd
from datetime import datetime
from flask import Flask, render_template, send_file
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import threading

app = Flask(__name__)

CSV_FILE = "gold_prices.csv"

# Ensure CSV file exists with headers
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=["Date", "Time", "Price"])
    df.to_csv(CSV_FILE, index=False)

def scrape_price():
    """Scrapes live gold price from auragold.in using Selenium"""
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")  # Bypass sandbox
    options.add_argument("--disable-dev-shm-usage")  # Fix memory issues
    options.binary_location = "/tmp/chrome/chrome-linux64/chrome"  # Update Chromium path

    print("Starting Selenium...")  # Debugging line

    driver = webdriver.Chrome(options=options)
    driver.get("https://auragold.in/")

    time.sleep(5)  # Wait for page to load
    print("Page loaded...")  # Debugging line

    try:
        price_element = driver.find_element(By.CSS_SELECTOR, ".live__price__container .price")
        price = price_element.text.strip()
        driver.quit()
        print(f"Scraped Price: {price}")  # Debugging line
        return price
    except Exception as e:
        print(f"Error extracting price: {e}")
        driver.quit()
        return None



def save_to_csv(price):
    """Saves the latest gold price to CSV"""
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    date, time_str = date_time.split(" ")

    df = pd.DataFrame([[date, time_str, price]], columns=["Date", "Time", "Price"])
    
    # Append data but write headers if the file is empty
    file_exists = os.path.exists(CSV_FILE) and os.path.getsize(CSV_FILE) > 0
    df.to_csv(CSV_FILE, mode="a", header=not file_exists, index=False)
    
    print(f"Saved: {date} {time_str} - ₹{price}/gm")

def update_price():
    """Runs the scraper every 10 minutes in the background"""
    while True:
        price = scrape_price()
        if price:
            save_to_csv(price)
        else:
            print("Failed to get price data.")
        time.sleep(600)  # Wait 10 minutes before next scrape

# Start the scraper in a background thread
threading.Thread(target=update_price, daemon=True).start()

@app.route("/")
def index():
    """Displays the latest gold price on the web page"""
    try:
        df = pd.read_csv(CSV_FILE)
        latest_price = df.iloc[-1].to_dict() if not df.empty else {"Date": "N/A", "Time": "N/A", "Price": "N/A"}
    except Exception as e:
        print(f"Error reading CSV: {e}")
        latest_price = {"Date": "N/A", "Time": "N/A", "Price": "N/A"}

    return render_template("index.html", latest_price=latest_price)

@app.route("/download")
def download_csv():
    """Allows users to download the gold price CSV file"""
    return send_file(CSV_FILE, as_attachment=True)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Use Render's provided port
    app.run(host="0.0.0.0", port=port)
