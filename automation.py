from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import TimeoutException
from itertools import combinations



# Create a new service
service = Service('C:\Program Files (x86)\chromedriver.exe')

# Start the service
service.start()

# Create a new webdriver instance
driver = webdriver.Remote(service.service_url)



# Navigate to the website
url = 'https://www.betmines.com/fr/'
driver.get(url)



filter_button = driver.find_element_by_css_selector(".tw-justify-center .primary span")
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".tw-justify-center .primary span"))).click()


matches = []
a = True
while (a==True):
    try:
        # Attendre que les éléments soient chargés
        elements = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.tw-py-2"))
        )

        # Boucle à travers chaque élément
        for element in elements:
            box_match = {}
            # Extraire les données de l'élément
            box_match["home_team"] = element.find_element(By.CSS_SELECTOR, ".tw-justify-center div:nth-of-type(1) p").text
            box_match["away_team"] = element.find_element(By.CSS_SELECTOR, "div.tw-flex:nth-of-type(2) p.tw-text-left").text
            box_match["prediction"] = element.find_element(By.CSS_SELECTOR, ".prediction-item p:nth-of-type(1)").text
            box_match["odds"] = element.find_element(By.CSS_SELECTOR, ".prediction-item p:nth-of-type(2)").text
            box_match["probability"] = element.find_element(By.CSS_SELECTOR, "p:nth-of-type(3)").text

            
    
                
            # Vérifie si le match existe déjà dans la liste des matchs
            if box_match not in matches:
                print(box_match)
                matches.append(box_match)

            if len(matches) == 7:
                a = False


          

        driver.execute_script("window.scrollBy(0, 100)")
        if driver.execute_script("return window.pageYOffset == document.body.scrollHeight"):
            a = False 
        time.sleep(1)   
      

    except TimeoutException:
        print("Timed out waiting for elements to load")
        break


matches.sort(key=lambda x: x['probability'], reverse=True)



# Générer toutes les combinaisons de 3 matchs
combination_list = list(combinations(matches, 3))
combination_list = list(map(list, combination_list))

print()
#print("liste combinaison :\n",combination_list)

# Calculer le gain potentiel pour chaque combinaison
for combination in combination_list:
    total_odds = 1
    gain_potentiel = 1
    for match in combination:
        total_odds  *= float(match['odds'])
        gain_potentiel *= float(match['odds']) * float(match['probability'].replace("%", "")) / 100
        

    #combination = list(combination)
    combination.append(total_odds)
    combination.append(gain_potentiel - 1)

    #print("combination \n",combination)


#combination_list.sort(key=lambda x: x[-1], reverse=True)
#print("combination_list",combination_list)


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



# # Trier les combinaisons par ordre décroissant de gain potentiel
# combination_list.sort(key=lambda x: x[3], reverse=True)

# # Afficher la combinaison la plus rentable
# print("La combinaison la plus rentable est : ", combination_list_with_gain[0])


# Close the browser
driver.quit()

# Stop the service
service.stop()



