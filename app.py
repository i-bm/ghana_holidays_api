from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)

def scrape_holidays(year):
    url = f"https://www.officeholidays.com/countries/ghana/{year}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    table = soup.find('table', class_='country-table')
    holidays = []

    if table:
        rows = table.find_all('tr')
        for row in rows[1:]:  # Skip the header row
            cols = row.find_all('td')
            if cols:
                holiday_day = cols[0].text.strip()
                holiday_date = cols[1].text.strip()
                holiday_name = cols[2].text.strip()
                holiday_type = cols[3].text.strip()
                
                # Convert the date to YYYY-MM-DD format
                # try:
                #     day = datetime.strptime(holiday_date, '%B %d, %Y')
                #     formatted_date = day.strftime('%Y-%m-%d')
                # except ValueError:
                #     continue  # Skip if the date format is incorrect
                
                holiday = {
                    'Day': holiday_day,  # Get the day of the week
                    'Date': holiday_date,
                    'Holiday Name': holiday_name,
                    'Type': holiday_type  # You can modify this as needed
                }
                print(holiday)
                holidays.append(holiday)
    
    return holidays

@app.route('/holidays/<int:year>', methods=['GET'])
def get_holidays(year):
    holidays = scrape_holidays(year)
    return jsonify(holidays)

if __name__ == '__main__':
    app.run(debug=True)
