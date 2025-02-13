from flask import Flask, render_template, send_file
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import os
import time
import threading
from datetime import datetime

app = Flask(__name__)
CSV_FILE = "gold_prices.csv"

# Ensure CSV file exists
def create_csv():
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=["Date", "Price"])
        df.to_csv(CSV_FILE, index=False)
        print("CSV file created.")

create_csv()

# Function to scrape gold price
def scrape_price():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://auragold.in/")
    time.sleep(5)  # Wait for page to load

    try:
        price_element = driver.find_element(By.CSS_SELECTOR, ".live__price__container .price")
        price = price_element.text.strip()
        driver.quit()
        return price
    except Exception as e:
        print(f"Error extracting price: {e}")
        driver.quit()
        return None

# Function to save price to CSV
def save_to_csv():
    while True:
        price = scrape_price()
        if price:
            date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data = pd.DataFrame([[date_time, price]], columns=["Date", "Price"])
            data.to_csv(CSV_FILE, mode='a', header=not os.path.exists(CSV_FILE), index=False)
            print(f"Saved: {date_time} - {price}")
        else:
            print("Failed to fetch price.")
        time.sleep(600)  # Wait 10 minutes

# Start background scraper
threading.Thread(target=save_to_csv, daemon=True).start()

@app.route('/')
def home():
    try:
        df = pd.read_csv(CSV_FILE)
        latest_price = df.iloc[-1].to_dict() if not df.empty else None
        return render_template("index.html", latest_price=latest_price)
    except Exception as e:
        print(f"Error: {e}")
        return "No data available yet. Please wait..."

@app.route('/download')
def download_csv():
    return send_file(CSV_FILE, as_attachment=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
