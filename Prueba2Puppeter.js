const puppeteer = require("puppeteer");
const readlineSync = require("readline-sync");
const fs = require("fs");
const path = require("path");

// --- Pedir número de prueba ---
const PRUEBA_NUMERO = readlineSync.questionInt("Ingrese el número de prueba: ");

if (!PRUEBA_NUMERO) {
    console.log("⚠ No se ingresó número de prueba. Saliendo...");
    process.exit();
}

// --- CONFIGURACIÓN ---
const BASE_DIR = "screenshots";
const CARPETA_PRUEBA = path.join(BASE_DIR, `prueba_${PRUEBA_NUMERO}`);

// Función para tomar screenshots
async function takeScreenshot(page, stepName) {
    if (!fs.existsSync(CARPETA_PRUEBA)) {
        fs.mkdirSync(CARPETA_PRUEBA, { recursive: true });
    }
    const filename = `${stepName}_${new Date().toISOString().replace(/[:.]/g, "_")}.png`;
    const filepath = path.join(CARPETA_PRUEBA, filename);
    await page.screenshot({ path: filepath });
    console.log(`[+] Screenshot guardado: ${filepath}`);
}

// --- Flujo principal ---
(async () => {
    const browser = await puppeteer.launch({ headless: false }); // false para ver la ejecución
    const page = await browser.newPage();
    await page.goto("https://testsheepnz.github.io/BasicCalculator.html");

    // ingresar compilación
    await page.select("#selectBuild", "1");
    await takeScreenshot(page, "compilacion");

    // ingresar primer número
    await page.type("#number1Field", "10");
    await takeScreenshot(page, "primer_numero");

    // ingresar segundo número
    await page.type("#number2Field", "8");
    await takeScreenshot(page, "segundo_numero");

    // seleccionar operación
    await page.select("#selectOperationDropdown", "0"); 
    // valores:
    // 0 = Add, 1 = Subtract, 2 = Multiply, 3 = Divide, 4 = Concatenate
    await takeScreenshot(page, "operacion");

    // clic en Calcular
    await page.click("#calculateButton");
    await page.waitForTimeout(1000);
    await takeScreenshot(page, "resultado");

    // leer respuesta
    const respuesta = await page.$eval("#numberAnswerField", el => el.value);
    console.log("Respuesta calculada:", respuesta);

    await browser.close();
})();
