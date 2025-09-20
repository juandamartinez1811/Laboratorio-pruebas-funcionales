from playwright.sync_api import sync_playwright
import os
import time

casos_prueba = [
    {
        "id": "TC01",
        "descripcion": "Login con contraseña vacía",
        "username": "tomsmith",
        "password": "",
        "capturas": ["1_login_vacio.png", "2_error_vacio.png"],
        "esperado": "Your password is invalid!"
    },
    {
        "id": "TC02",
        "descripcion": "Login exitoso",
        "username": "tomsmith",
        "password": "SuperSecretPassword!",
        "capturas": ["3_login_correcto.png", "4_exito.png"],
        "esperado": "You logged into a secure area!"
    }
]

def run():
    os.makedirs("screenshots", exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        for caso in casos_prueba:
            print(f"\nEjecutando {caso['id']} - {caso['descripcion']}")

            page.goto("https://the-internet.herokuapp.com/login")
            time.sleep(1)

            page.fill("#username", caso["username"])
            page.fill("#password", caso["password"])

            page.screenshot(path=f"screenshots/{caso['capturas'][0]}")

            page.click("button.radius")

            page.wait_for_selector(".flash", timeout=5000)

            page.screenshot(path=f"screenshots/{caso['capturas'][1]}")

            mensaje = page.inner_text(".flash").strip()
            print(f"Resultado obtenido: {mensaje}")

            if caso["esperado"] in mensaje:
                print("✅ Prueba EXITOSA")
            else:
                print("❌ Prueba FALLIDA")

            time.sleep(2)

        browser.close()

run()
