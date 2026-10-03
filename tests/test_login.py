"""Caso 4.1 - Login en saucedemo.com."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.helpers import TIMEOUT, login


def test_login_exitoso(driver):
    """Con credenciales válidas se redirige a /inventory.html y se muestra 'Products'."""
    login(driver)

    assert "/inventory.html" in driver.current_url, (
        f"No se redirigió a /inventory.html. URL actual: {driver.current_url}"
    )
    assert driver.title == "Swag Labs", (
        f"Título de ventana esperado 'Swag Labs', obtenido '{driver.title}'"
    )
    titulo = WebDriverWait(driver, TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "div.header_secondary_container .title")
        )
    )
    assert titulo.text == "Products", (
        f"Título de sección esperado 'Products', obtenido '{titulo.text}'"
    )
