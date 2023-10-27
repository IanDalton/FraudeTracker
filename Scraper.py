
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By


driver = webdriver.Edge()

driver.get('https://resultados.gob.ar/')
sleep(4)
# click by xpath

driver.find_element(By.XPATH,'//*[@id="root"]/main/div/div[3]/div[1]/nav/div[2]/div/ul/div[1]/div[1]/button').click()
sleep(1)

mesas_set = set()

def search_mesa(categorias:webdriver.Edge):

    secciones = categorias.find_elements(By.TAG_NAME,'li')
    
    secciones[-1].click()
    mesas = secciones[-1].find_elements(By.TAG_NAME,'li')
    

    mesas_set.update([mesa.text for mesa in mesas])


    
def get_mesas_grande(categorias:webdriver.Edge):
    print('grande')
    secciones = categorias.find_elements(By.TAG_NAME,'li')

    secciones[2].click()
    opciones = secciones[2].find_elements(By.TAG_NAME,'li')
    #for _ in range(len(opciones)):
    for i in range(len(opciones)):
        opciones = secciones[2].find_elements(By.TAG_NAME,'li')
        opciones[i].click()
        secciones[3].click()
        opciones = secciones[3].find_elements(By.TAG_NAME,'li')
        for j in range(len(opciones)):
            opciones = secciones[3].find_elements(By.TAG_NAME,'li')
            opciones[j].click()
            search_mesa(categorias)
            secciones[3].click()
        secciones[2].click()
    


def get_mesas_chica(categorias:webdriver.Edge):
    print('chica')
    secciones = categorias.find_elements(By.TAG_NAME,'li')
    secciones[2].click()
    opciones = secciones[2].find_elements(By.TAG_NAME,'li')
    #for _ in range(len(opciones)):
    for i in range(len(opciones)):
        opciones = secciones[2].find_elements(By.TAG_NAME,'li')
        opciones[i].click()
        search_mesa(categorias)
        secciones[2].click()
    

for i in range(24):
    driver.find_element(By.XPATH,'//*[@id="downshift-1-toggle-button"]').click()
    provincias = driver.find_element(By.XPATH,'//*[@id="menu-2"]')
    provincias = provincias.find_elements(By.TAG_NAME,'li')
    print(provincias[i].text)
    provincias[i].click()


    mesas_encontradas = False
    secciones = driver.find_element(By.XPATH,'//*[@id="root"]/main/div/div[3]/div[1]/nav/div[2]/div/ul/div[1]/div[1]/div/div/div[1]/div[1]/ul')
    if len(secciones.find_elements(By.TAG_NAME,'li')) >3:
        get_mesas_grande(secciones)
    else:
        get_mesas_chica(secciones)
    print('done')




with open('mesas.txt','w') as f:
    for mesa in mesas_set:
        f.write(f'{mesa}\n')