const puppeteer = require("puppeteer");
 
(async () => {
  const browser = await puppeteer.launch({ headless: false }); // Abre Chrome visible
  const page = await browser.newPage();
 
  // Ir a la página
  await page.goto("https://the-internet.herokuapp.com/login", { waitUntil: "networkidle2" });
  await page.waitForTimeout(10000); // 💤 espera 10 segundos
 
  // Escribir usuario
  await page.type("#username", "tomsmith");
  await page.waitForTimeout(10000); // 💤 espera 10 segundos
 
  // Escribir contraseña vacía
  await page.type("#password", "");
  await page.waitForTimeout(10000); // 💤 espera 10 segundos
 
  // Clic en login
  await page.click("button.radius");
  await page.waitForTimeout(10000); // 💤 espera 10 segundos
 
  // Validar mensaje
  try {
    await page.waitForSelector(".flash.success", { timeout: 5000 });
    const successMessage = await page.$eval(".flash.success", el => el.innerText);
    console.log("✔ Login exitoso:", successMessage);
  } catch (e) {
    const errorMessage = await page.$eval(".flash", el => el.innerText);
    console.log("❌ Login fallido:", errorMessage);
  }
 
  await page.waitForTimeout(9000000); // 💤 espera 15 segundos antes de cerrar
  await browser.close();
})();