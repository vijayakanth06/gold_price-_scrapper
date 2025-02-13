from flask import Flask, render_template, send_file
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import datetime
import os
import time

app = Flask(__name__)

# Ensure CSV file exists
csv_filename = "gold_prices.csv"
if not os.path.exists(csv_filename):
    df = pd.DataFrame(columns=["Date", "Time", "Price"])
    df.to_csv(csv_filename, index=False)

# Function to scrape gold price
def scrape_price():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = "/usr/bin/google-chrome-stable"
    chrome_options.add_argument("--headless")  # No UI mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get("https://auragold.in/")
    time.sleep(5)

    try:
        price_element = driver.find_element(By.CSS_SELECTOR, ".live__price__container .price")
        price = price_element.text.strip()
        driver.quit()
        return price
    except Exception as e:
        print(f"Error extracting price: {e}")
        driver.quit()
        return None

# Function to save data to CSV
def save_to_csv():
    price = scrape_price()
    if price:
        now = datetime.now()
        date, time_str = now.strftime('%Y-%m-%d'), now.strftime('%H:%M:%S')
        df = pd.DataFrame([[date, time_str, price]], columns=["Date", "Time", "Price"])
        df.to_csv(csv_filename, mode='a', header=False, index=False)
        print(f"Saved: {date} {time_str} - {price}")

# Route to display latest price
@app.route("/")
def index():
    df = pd.read_csv(csv_filename)
    if df.empty:
        latest_price = {"Date": "N/A", "Time": "N/A", "Price": "N/A"}
    else:
        latest_price = df.iloc[-1].to_dict()

    return render_template("index.html", latest_price=latest_price)

# Route to download CSV
@app.route("/download")
def download():
    return send_file(csv_filename, as_attachment=True)

# Run the scraper every 10 minutes
import threading

def schedule_scraping():
    while True:
        save_to_csv()
        time.sleep(600)  # 10 minutes

threading.Thread(target=schedule_scraping, daemon=True).start()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
