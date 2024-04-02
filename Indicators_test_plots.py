# Personal Consumption Expenditures (PCE) Price Index
# PCE Price Index = (Expenditure in current year * Price in base year) / (Expenditure in base year * Price in base year) x 100
# where:
# Expenditure in current year is the total amount spent on personal consumption expenditures in the current year
# Expenditure in base year is the total amount spent on personal consumption expenditures in the base year (usually set as a benchmark year)
# Price in current year is the weighted average of prices for all goods and services purchased in the current year
# Price in base year is the weighted average of prices for all goods and services purchased in the base year


# Mock data used to generate PCE Index
import random

# Generate mock data
years = [2018, 2019, 2020, 2021]
categories = ["Food", "Housing", "Transportation", "Healthcare", "Recreation", "Other"]
data = {category: {year: random.randint(100, 1000) for year in years} for category in categories}

# Calculate the PCE Price Index
pce_weights = {"Food": 0.15, "Housing": 0.33, "Transportation": 0.1, "Healthcare": 0.12, "Recreation": 0.05, "Other": 0.25}
pce_values = {year: sum(data[category][year] * pce_weights[category] for category in categories) for year in years}
pce_price_index = {year: pce_values[year] / pce_values[years[0]] * 100 for year in years}

# Print the results
print("Mock data:")
for category in categories:
    print(f"{category}: {data[category]}")
print()
print("PCE Price Index:")
for year in years:
    print(f"{year}: {pce_price_index[year]}")

# Plot the PCE Price Index data
plt.plot(pce_price_index.keys(), pce_price_index.values())
plt.title("Personal Consumption Expenditures (PCE) Price Index")
plt.xlabel("Year")
plt.ylabel("Index")
plt.show()

#############################################################################################################
# The Non Farm Payrolls (NFP) is a monthly economic indicator released by the US Bureau of Labor Statistics,
# and it represents the total number of paid workers in the U.S. economy, excluding agricultural, government,
# and non-profit employees. The formula for NFP is simply the difference between the number of jobs added or
# lost in the month being reported and the number of jobs added or lost in the previous month.

# NFP = Current month's total number of paid workers - Previous month's total number of paid workers

import random
import matplotlib.pyplot as plt
# Generate mock data
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
data = {month: random.randint(100000, 300000) for month in months}

# Calculate the NFP for each month
nfp = {}
for i in range(1, len(months)):
    nfp[months[i]] = data[months[i]] - data[months[i-1]]

# Print the results
print("Mock data:")
for month in months:
    print(f"{month}: {data[month]}")
print()
print("NFP:")
for month in months[1:]:
    print(f"{month}: {nfp[month]}")
# Plot the NFP data
plt.plot(nfp.keys(), nfp.values())
plt.title("Non Farm Payrolls (NFP)")
plt.xlabel("Month")
plt.ylabel("NFP")
plt.show()

##############################################################################################################
# Inflation rate data is taken from the Unites States Bureau of Labor Statistics (BLS) website. Specifically,
# I take the Consumer Price Index for All Urban Consumers (CPI-U) for all items as it is the commonly used measure
# of inflation in the US
# Inflation Rate = ((CPI in current year - CPI in previous year) / CPI in previous year) x 100
# where:
# CPI in current year is the Consumer Price Index for the current year
# CPI in previous year is the Consumer Price Index for the previous year
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import yfinance

# URL for the BLS CPI-U data
url = 'https://www.bls.gov/cpi/data.htm'

# Make a GET request to the URL
response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table containing the CPI-U data and extract the rows
table = soup.find('table', {'id': 'CPiCtrl_GridView1'})
if table is not None:
    rows = table.find_all('tr')

    # Create a dictionary to store the CPI-U data
    cpi_data = {}

    # Loop through the rows and extract the CPI-U data for each year
    for row in rows[1:]:
        cells = row.find_all('td')
        year = cells[0].text.strip()
        cpi = cells[12].text.strip()
        cpi_data[year] = float(cpi)

    # Calculate the inflation rate for each year
    inflation_rate = {}
    for year in cpi_data:
        if year != '1913':
            inflation_rate[year] = ((cpi_data[year] - cpi_data[str(int(year)-1)]) / cpi_data[str(int(year)-1)]) * 100

    # Plot the inflation rate data
    plt.plot(inflation_rate.keys(), inflation_rate.values())
    plt.title("US Inflation Rate (CPI-U)")
    plt.xlabel("Year")
    plt.ylabel("Inflation Rate (%)")
    plt.show()

else:
    print("Table not found!")
##### Try on another website:
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd

# URL for the BLS CPI-U data
bls_url = 'https://www.bls.gov/cpi/data.htm'

# Make a GET request to the BLS URL
response = requests.get(bls_url)

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table containing the CPI-U data and extract the rows
table = soup.find('table', {'id': 'CPiCtrl_GridView1'})

if table is not None:
    # If the CPI-U table is found on the BLS website, extract the data from the table
    rows = table.find_all('tr')
    cpi_data = {}
    for row in rows[1:]:
        cells = row.find_all('td')
        year = cells[0].text.strip()
        cpi = cells[12].text.strip()
        cpi_data[year] = float(cpi)
else:
    # If the CPI-U table is not found on the BLS website, try to scrape the data from the FRED website
    fred_url = 'https://fred.stlouisfed.org/series/CPIAUCSL'
    fred_response = requests.get(fred_url)
    fred_soup = BeautifulSoup(fred_response.content, 'html.parser')
    fred_table = fred_soup.find('table', {'class': 'series-meta-observation-data'})
    if fred_table is not None:
        df = pd.read_html(str(fred_table))[0]
        cpi_data = {str(int(row['DATE'])): row['VALUE'] for i, row in df.iterrows()}
    else:
        print("CPI data not found on either website.")

if cpi_data:
    # Calculate the inflation rate for each year
    inflation_rate = {}
    for year in cpi_data:
        if year != '1913':
            inflation_rate[year] = ((cpi_data[year] - cpi_data[str(int(year)-1)]) / cpi_data[str(int(year)-1)]) * 100

    # Plot the inflation rate data
    plt.plot(inflation_rate.keys(), inflation_rate.values())
    plt.title("US Inflation Rate (CPI-U)")
    plt.xlabel("Year")
    plt.ylabel("Inflation Rate (%)")
    plt.show()
######## Same as above but with mock data
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd

# URL for the BLS CPI-U data
bls_url = 'https://www.bls.gov/cpi/data.htm'

# Make a GET request to the BLS URL
response = requests.get(bls_url)

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table containing the CPI-U data and extract the rows
table = soup.find('table', {'id': 'CPiCtrl_GridView1'})

if table is not None:
    # If the CPI-U table is found on the BLS website, extract the data from the table
    rows = table.find_all('tr')
    cpi_data = {}
    for row in rows[1:]:
        cells = row.find_all('td')
        year = cells[0].text.strip()
        cpi = cells[12].text.strip()
        cpi_data[year] = float(cpi)
else:
    # If the CPI-U table is not found on the BLS website, try to scrape the data from the FRED website
    fred_url = 'https://fred.stlouisfed.org/series/CPIAUCSL'
    fred_response = requests.get(fred_url)
    fred_soup = BeautifulSoup(fred_response.content, 'html.parser')
    fred_table = fred_soup.find('table', {'class': 'series-meta-observation-data'})
    if fred_table is not None:
        df = pd.read_html(str(fred_table))[0]
        cpi_data = {str(int(row['DATE'])): row['VALUE'] for i, row in df.iterrows()}
    else:
        print("CPI data not found on either website.")
        cpi_data = {}

if cpi_data:
    # Calculate the inflation rate for each year
    inflation_rate = {}
    for year in cpi_data:
        if year != '1913':
            inflation_rate[year] = ((cpi_data[year] - cpi_data[str(int(year)-1)]) / cpi_data[str(int(year)-1)]) * 100

    # Plot the inflation rate data
    plt.plot(inflation_rate.keys(), inflation_rate.values())
    plt.title("US Inflation Rate (CPI-U)")
    plt.xlabel("Year")
    plt.ylabel("Inflation Rate (%)")
    plt.show()

else:
    # If CPI data is not found on either website, generate mock data and plot
    print("Generating mock CPI data...")
    cpi_data = {'2019': 255.657, '2020': 259.101, '2021': 268.551}
    inflation_rate = {'2019': 0, '2020': 1.35, '2021': 3.65}

    # Plot the inflation rate data
    plt.plot(inflation_rate.keys(), inflation_rate.values())
    plt.title("US Inflation Rate (Mock Data)")
    plt.xlabel("Year")
    plt.ylabel("Inflation Rate (%)")
    plt.show()
