from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import TimeoutException



# Create a new service
service = Service('C:\Program Files (x86)\chromedriver.exe')

# Start the service
service.start()

# Create a new webdriver instance
driver = webdriver.Remote(service.service_url)


# navigate to the website
driver.get("https://betmines.com/fr")



last_height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")
data_list = []

while True:
    try:
        # wait for the elements with the specified selector to load
        elements = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".tw-justify-center div:nth-of-type(1) p"))
        )

         # loop through each element
        for element in elements:
            # extract the data from the element
            data = element.text

            # check if the extracted data is already in the data list
            if data not in data_list:
                # if not, add it to the data list and print it
                data_list.append(data)
                print("Data: ", data)

        driver.execute_script("window.scrollBy(0, 100)")
        time.sleep(3)
      

    except TimeoutException:
        print("Timed out waiting for elements to load")
        break



# close the browser
driver.quit()


# Stop the service
service.stop()


def calculate_potential_gain(combination_list):
    for combination in combination_list:
        total_odds = 1
        gain_potentiel = 1
        for match in combination:
            total_odds  *= float(match['odds'])
            gain_potentiel *= float(match['odds']) * float(match['probability'].replace("%", "")) / 100

        combination.append(total_odds)
        combination.append(gain_potentiel - 1)
    combination_list.sort(key=lambda x: x[-1], reverse=True)
    with open("output.txt", "w", encoding="utf-8") as f:
        i= 0
        for combination in combination_list:
            i=i+1
            f.write("-----------------fiche" + str(i) + "-----------------------\n")
            for match in combination[:-2]:
                f.write(f"Match: {match['home_team']} vs {match['away_team']} \n")
                f.write(f"Prediction: {match['prediction']} \n")
                f.write(f"Odds: {match['odds']} \n")
                f.write(f"Probability: {match['probability']} \n\n")
            f.write(f"Total Odds: {combination[-2]} \n")
            f.write(f"Potential Gain: {combination[-1]}\n")
            f.write(f"------------------------------------------------\n\n\n")
        f.write("\n\n\nEnd of Combination Results")
