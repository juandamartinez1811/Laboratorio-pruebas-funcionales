import tkinter as tk
from tkinter import simpledialog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import os
from datetime import datetime

# --- Pedir número de prueba con Tkinter ---
root = tk.Tk()
root.withdraw()  # Oculta la ventana principal
PRUEBA_NUMERO = simpledialog.askinteger("Número de prueba", "Ingrese el número de prueba:")
root.destroy()

if PRUEBA_NUMERO is None:
    print("⚠ No se ingresó número de prueba. Saliendo...")
    exit()

# --- CONFIGURACIÓN ---
BASE_DIR = "screenshots"
CARPETA_PRUEBA = os.path.join(BASE_DIR, f"prueba_{PRUEBA_NUMERO}")

# Función para tomar screenshots
def take_screenshot(driver, step_name):
    if not os.path.exists(CARPETA_PRUEBA):
        os.makedirs(CARPETA_PRUEBA)
    filename = f"{step_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    path = os.path.join(CARPETA_PRUEBA, filename)
    driver.save_screenshot(path)
    print(f"[+] Screenshot guardado: {path}")

# --- Flujo principal ---
driver = webdriver.Chrome()
driver.get("https://testsheepnz.github.io/BasicCalculator.html")

# ingresar Valor compilacion
driver.find_element(By.ID, "selectBuild").send_keys("10")
take_screenshot(driver, "compilacion")

# ingresar primer número
driver.find_element(By.ID, "number1Field").send_keys("10")
take_screenshot(driver, "primer_numero")

# ingresar segundo número
driver.find_element(By.ID, "number2Field").send_keys("8")
take_screenshot(driver, "segundo_numero")

# seleccionar operación
select = Select(driver.find_element(By.ID, "selectOperationDropdown"))
select.select_by_value("2")  
take_screenshot(driver, "operacion")

# clic en Calcular
driver.find_element(By.ID, "calculateButton").click()
time.sleep(1)  # delay para que cargue la respuesta
take_screenshot(driver, "resultado")

# leer respuesta
respuesta = driver.find_element(By.ID, "numberAnswerField").get_attribute("value")
print("Respuesta calculada:", respuesta)

driver.quit()
