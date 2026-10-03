"""Funciones auxiliares compartidas por los tests de saucedemo.com."""
import logging

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logger = logging.getLogger(__name__)

# --- Constantes de la aplicación bajo prueba ---
URL_BASE = "https://www.saucedemo.com/"
USUARIO_VALIDO = "standard_user"
PASSWORD_VALIDA = "secret_sauce"
TIMEOUT = 10  # segundos máximos de espera explícita


def crear_driver(headless: bool = False) -> WebDriver:
    """Crea una instancia de Chrome. Selenium Manager descarga el driver solo."""
    opciones = webdriver.ChromeOptions()
    if headless:
        opciones.add_argument("--headless=new")
    # Evita el popup de "cambiar contraseña" de Chrome que tapa la página
    opciones.add_experimental_option(
        "prefs",
        {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
        },
    )
    opciones.add_argument("--window-size=1280,900")
    driver = webdriver.Chrome(options=opciones)
    logger.info("Navegador Chrome iniciado (headless=%s)", headless)
    return driver


def esperar_elemento_visible(driver: WebDriver, localizador: tuple, timeout: int = TIMEOUT):
    """Espera explícita hasta que el elemento sea visible y lo devuelve."""
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(localizador)
    )


def esperar_elemento_clickeable(driver: WebDriver, localizador: tuple, timeout: int = TIMEOUT):
    """Espera explícita hasta que el elemento sea clickeable y lo devuelve."""
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable(localizador)
    )


def login(driver: WebDriver, usuario: str = USUARIO_VALIDO, password: str = PASSWORD_VALIDA) -> None:
    """Abre saucedemo.com, ingresa las credenciales y espera a la página de inventario."""
    logger.info("Login con el usuario '%s'", usuario)
    driver.get(URL_BASE)
    esperar_elemento_visible(driver, (By.ID, "user-name")).send_keys(usuario)
    driver.find_element(By.ID, "password").send_keys(password)
    esperar_elemento_clickeable(driver, (By.ID, "login-button")).click()
    # Espera explícita a la redirección al inventario
    WebDriverWait(driver, TIMEOUT).until(EC.url_contains("/inventory.html"))
    logger.info("Login exitoso, URL actual: %s", driver.current_url)


def obtener_productos(driver: WebDriver) -> list:
    """Devuelve las tarjetas de producto del inventario (espera a que cargue la primera)."""
    try:
        WebDriverWait(driver, TIMEOUT).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.inventory_item"))
        )
    except TimeoutException:
        return []  # el test que lo use informará que no hay productos
    return driver.find_elements(By.CSS_SELECTOR, "div.inventory_item")
