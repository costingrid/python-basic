"""
There is a list of most active Stocks on Yahoo Finance https://finance.yahoo.com/most-active.
You need to compose several sheets based on data about companies from this list.
To fetch data from webpage you can use requests lib. To parse html you can use beautiful soup lib or lxml.
Sheets which are needed:
1. 5 stocks with most youngest CEOs and print sheet to output. You can find CEO info in Profile tab of concrete stock.
    Sheet's fields: Name, Code, Country, Employees, CEO Name, CEO Year Born.
2. 10 stocks with best 52-Week Change. 52-Week Change placed on Statistics tab.
    Sheet's fields: Name, Code, 52-Week Change, Total Cash
3. 10 largest holds of Blackrock Inc. You can find related info on the Holders tab.
    Blackrock Inc is an investment management corporation.
    Sheet's fields: Name, Code, Shares, Date Reported, % Out, Value.
    All fields except first two should be taken from Holders tab.


Example for the first sheet (you need to use same sheet format):
==================================== 5 stocks with most youngest CEOs ===================================
| Name        | Code | Country       | Employees | CEO Name                             | CEO Year Born |
---------------------------------------------------------------------------------------------------------
| Pfizer Inc. | PFE  | United States | 78500     | Dr. Albert Bourla D.V.M., DVM, Ph.D. | 1962          |
...

About sheet format:
- sheet title should be aligned to center
- all columns should be aligned to the left
- empty line after sheet

Write at least 2 tests on your choose.
Links:
    - requests docs: https://docs.python-requests.org/en/latest/
    - beautiful soup docs: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
    - lxml docs: https://lxml.de/
"""
import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from tabulate import tabulate

stocks = []
ceos = []

ceo_re = r'(CEO($|,| &| $))|([Cc]hief [Ee]xecutive [Oo]fficer)'


def top_5_youngest_ceos(driver):
    ceo_birth_years = []
    for stock in stocks[:200]:
        url = f'https://finance.yahoo.com/quote/{stock}/profile'
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        try:
            table = soup.find("table", {"class": "yf-mj92za"}).find('tbody')
        except AttributeError:
            print(stock + " Attribute error")
            continue

        for tr in table.find_all('tr'):
            profile = tr.find_all('td')
            role = profile[1].text
            ceo_name = profile[0].text
            birth_year = profile[4].text

            if re.search(ceo_re, role):
                birth_year = re.sub('\\s+', '', birth_year)
                if not re.fullmatch('[0-9]+', birth_year):
                    break
                ceo_birth_years.append((stock, int(birth_year), ceo_name))

        if stocks.index(stock) % 50 == 0:
            print("Iterated through 50 stocks, resting on {} ...".format(stock))
            time.sleep(10)

    ceo_birth_years = sorted(ceo_birth_years, key=lambda x: x[1], reverse=True)
    print(ceo_birth_years)

    with open('top_5_youngest_ceos_current', "w") as file:
        data = []
        headers = ["Name", "Code", "Country", "Employees", "CEO Name", "CEO Year Born"]
        for ceo in ceo_birth_years[:5]:
            stock_code = ceo[0]
            birth_year = ceo[1]
            ceo_name = ceo[2]
            employees = 0
            url = f'https://finance.yahoo.com/quote/{stock_code}/profile'
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            try:
                info_section = soup.find('section', {"data-testid": "asset-profile"})
                company_name = info_section.find('header').text
                company_details = soup.find('div', {'class': 'company-details yf-wxp4ja'})
                stats = company_details.find('dl', {'class': 'company-stats yf-wxp4ja'}).find_all('div')
            except AttributeError as e:
                print(e.name + stock_code)
                continue

            if len(stats) > 2:
                employees = stats[2].find('dd').text
                employees = re.sub('\\s+', '', employees)
                employees = int(re.sub(',', '', employees))
            else:
                employees = '--'
            country = (company_details.find('div', {'class': 'company-info yf-wxp4ja'})
                       .find('div', {'class': 'address yf-wxp4ja'}).find_all('div')[-1].text)
            data.append([company_name, stock_code, country, employees, ceo_name, birth_year])

        max_company_name = max(len(x[0]) for x in data)
        max_stock_code = max(len(x[1]) for x in data)
        max_country = max(len(x[2]) for x in data)
        max_employees = max(max(len(str(x[3])) for x in data), len("Employees"))
        max_ceo_name = max(len(x[4]) for x in data)
        max_birth_year = len("CEO Year Born")
        whole_len = (max_company_name + max_stock_code + max_country
                     + max_employees + max_ceo_name + max_birth_year + 4 * 5)
        title = "5 stocks with the youngest CEOs"
        title_centered = ("=" * ((whole_len - len(title)) // 2) + " "
                          + title + " " + "=" * ((whole_len - len(title)) // 2))
        file.write(title_centered + '\n')

        table = tabulate(data, headers, tablefmt="grid", colalign=("left", "left", "left", "left", "left", "left"))
        file.write(table + '\n')
        file.write('\n')


def top_10_52_week_changes(driver):
    one_year_changes = []
    for stock in stocks[:200]:
        url = f'https://finance.yahoo.com/quote/{stock}/key-statistics'
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        try:
            table = soup.find_all('table')[7]
        except IndexError:
            print(stock + " not enough tables")
            continue
        change = table.find_all('tr')[1].text
        change = change.strip().split()[-1]
        try:
            change = float(change[:-1])
        except ValueError:
            continue
        one_year_changes.append((stock, change))

        if stocks.index(stock) % 50 == 0:
            print("Iterated through 50 stocks, resting on {} ...".format(stock))
            time.sleep(10)

    one_year_changes = sorted(one_year_changes, key=lambda x: x[1], reverse=True)
    print(one_year_changes)

    with open('top_10_52_week_changes_current', 'w') as file:
        data = []
        headers = ["Name", "Code", "52-Week Change", "Total Cash"]
        for stock in one_year_changes[:10]:
            stock_code = stock[0]
            change = str(stock[1]) + '%'
            company_name = '--'
            total_cash = '--'
            driver.get(f'https://finance.yahoo.com/quote/{stock_code}/key-statistics')
            soup = BeautifulSoup(driver.page_source, "html.parser")

            try:
                company_name = soup.find('h1', {'class': 'yf-3a2v0c'}).text
                company_name = company_name.split('(')[0].strip()
            except AttributeError:
                print("Attribute error name " + stock_code)

            try:
                table = soup.find_all('table')[5]
                total_cash = table.find('tr').text
                total_cash = total_cash.strip().split()[-1]
            except AttributeError:
                print("Attribute error cash " + stock_code)
            except IndexError:
                print("Index error cash " + stock_code)

            data.append([company_name, stock_code, change, total_cash])

        max_company_name = max(len(x[0]) for x in data)
        max_stock_code = max(len(x[1]) for x in data)
        max_change = len("52-Week Change")
        max_cash = len("Total Cash")
        whole_len = (max_company_name + max_stock_code + max_change
                     + max_cash + 4 * 4 + 2)
        title = "10 stocks with the highest change"
        title_centered = ("=" * ((whole_len - len(title)) // 2) + " "
                          + title + " " + "=" * ((whole_len - len(title)) // 2))
        file.write(title_centered + '\n')

        table = tabulate(data, headers, tablefmt="grid", colalign=("left", "left", "left", "left"))
        file.write(table + '\n')
        file.write('\n')


def top_10_blackrock(driver):
    holds = []
    for stock in stocks[:200]:
        url = f'https://finance.yahoo.com/quote/{stock}/holders'
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        try:
            table = soup.find('table', {'class': 'yf-1s2g2l0'}).find('tbody')
        except AttributeError:
            print("Attribute Error " + stock)
            continue

        for tr in table.find_all('tr'):
            holder = tr.find('td').text
            if re.search('Blackrock', holder):
                hold = tr.find_all('td')[-1].text
                hold = re.sub(',', '', hold)
                hold = float(hold)
                holds.append((stock, hold))
                break

        if stocks.index(stock) % 50 == 0:
            print("Iterated through 50 stocks, resting on {} ...".format(stock))
            time.sleep(10)

    holds = sorted(holds, key=lambda x: x[1], reverse=True)

    with open('top_10_blackrock_current', 'w') as file:
        data = []
        headers = ["Name", "Code", "Shares", "Date Reported", "% Out", "Value"]
        for hold in holds[:10]:
            stock_code = hold[0]
            value = "${:,}".format(int(hold[1]))
            company_name = '--'
            shares = '--'
            date_reported = '--'
            percentage = '--'
            driver.get(f'https://finance.yahoo.com/quote/{stock_code}/holders')
            soup = BeautifulSoup(driver.page_source, "html.parser")

            try:
                company_name = soup.find('h1', {'class': 'yf-3a2v0c'}).text
                company_name = company_name.split('(')[0].strip()
            except AttributeError:
                print("Attribute error name " + stock_code)

            try:
                table = soup.find('table', {'class': 'yf-1s2g2l0'}).find('tbody')
                for tr in table.find_all('tr'):
                    holder = tr.find('td').text
                    if re.search('Blackrock', holder):
                        shares = tr.find_all('td')[1].text
                        date_reported = tr.find_all('td')[2].text
                        percentage = tr.find_all('td')[3].text
            except AttributeError:
                print("Attribute error hold " + stock_code)
            except IndexError:
                print("Index error hold" + stock_code)

            data.append([company_name, stock_code, shares, date_reported, percentage, value])

        max_company_name = max(len(x[0]) for x in data)
        max_stock_code = max(len(x[1]) for x in data)
        max_share = max(len(x[2]) for x in data)
        max_date = len("Date Reported")
        max_percentage = max(len(x[4]) for x in data)
        max_value = max(len(x[5]) for x in data)

        whole_len = (max_company_name + max_stock_code + max_share + max_date
                     + max_percentage + max_value + 5 * 4)
        title = "10 largest Blackrock holds"
        title_centered = ("=" * ((whole_len - len(title)) // 2) + " "
                          + title + " " + "=" * ((whole_len - len(title)) // 2))
        file.write(title_centered + '\n')

        table = tabulate(data, headers, tablefmt="grid", colalign=("left", "left", "left", "left", "left", "left"))
        file.write(table + '\n')
        file.write('\n')


def fetch_stocks(driver):
    url = f'https://finance.yahoo.com/most-active?count=100&offset=0'
    driver.get(url)
    driver.maximize_window()
    driver.find_element(By.CLASS_NAME, "scroll-down-arrow").click()
    driver.find_element(By.TAG_NAME, "button").click()
    current = 0
    while True:
        driver.get(f'https://finance.yahoo.com/most-active?count=100&offset={current}')
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        # accept cookies when reopening browser
        if soup.find('html', {'class': 'desktop neo-green dock-upscale'}):
            driver.close()
            driver = webdriver.Firefox()
            driver.get(url)
            driver.maximize_window()
            driver.find_element(By.CLASS_NAME, "scroll-down-arrow").click()
            driver.find_element(By.TAG_NAME, "button").click()
            continue
        table = soup.find('table')
        table_body = table.find('tbody')
        for tr in table_body.find_all('tr'):
            stock = tr.find('td').find('a')
            stock = stock['href']
            stocks.append(stock[7:-1])
        table = driver.find_element(By.ID, "scr-res-table")
        buttons = table.find_elements(By.TAG_NAME, "button")
        button = [but for but in buttons if but.accessible_name == "Next"][0]
        if button.is_enabled():
            # driver.execute_script("arguments[0].click();", button)
            current += 100
        else:
            break

    return driver


if __name__ == "__main__":
    options = Options()
    # options.add_argument("--headless")
    options.add_argument('--disable-notifications')
    driver = webdriver.Firefox(options=options)
    try:
        driver = fetch_stocks(driver)
        print(stocks)
        print(len(stocks))
        # top_5_youngest_ceos(driver)
        # top_10_52_week_changes(driver)
        top_10_blackrock(driver)
    finally:
        driver.quit()
