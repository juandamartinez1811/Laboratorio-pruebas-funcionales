from playwright.sync_api import sync_playwright
import time
import os
from PIL import Image

PROTOTIPO = ""  

os.makedirs("evidencias", exist_ok=True)

log_file = "registro.txt"
with open(log_file, "w", encoding="utf-8") as f:
    f.write(f"=== Registro de pruebas para prototipo: {PROTOTIPO} ===\n\n")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://testsheepnz.github.io/BasicCalculator.html")

    page.select_option("#selectBuild", label=PROTOTIPO)
    print(f"\n[INFO] Probando prototipo: {PROTOTIPO}\n")

    operaciones = {
        "Add": str(8 + 4),
        "Subtract": str(8 - 4),
        "Multiply": str(8 * 4),
        "Divide": str(8 / 4),
        "Concatenate": "84"
    }

    contador = 1

    for operacion, esperado in operaciones.items():
        # Ingresar números
        page.fill("#number1Field", "8")
        page.fill("#number2Field", "4")

        page.select_option("#selectOperationDropdown", label=operacion)

        page.click("#calculateButton")

        page.wait_for_selector("#numberAnswerField")

        resultado = page.input_value("#numberAnswerField")
        estado = "Éxito ✅" if resultado == esperado else "Fallo ❌"

        nombre = f"evidencias/test_{contador}_{PROTOTIPO}_{operacion}.png"
        page.screenshot(path=nombre)
        print(f"[OK] Pantallazo guardado: {nombre}")

        img = Image.open(nombre)
        img.show()

        print(f"Operación: {operacion} | Esperado: {esperado} | Obtenido: {resultado} | {estado}")

        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"Operación: {operacion}\n")
            f.write(f"  - Números: 8 y 4\n")
            f.write(f"  - Resultado esperado: {esperado}\n")
            f.write(f"  - Resultado obtenido: {resultado}\n")
            f.write(f"  - Estado: {estado}\n\n")

        contador += 1
        time.sleep(1)
        
    time.sleep(5)
    browser.close()

print(f"\n[INFO] Pruebas finalizadas. Registro guardado en: {log_file}")
