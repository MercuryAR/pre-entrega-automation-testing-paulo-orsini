"""Caso 4.3 - Interacción con productos: carrito de compras."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.helpers import (TIMEOUT, esperar_elemento_clickeable,
                           esperar_elemento_visible, login, obtener_productos)


def test_agregar_primer_producto_al_carrito(driver):
    """Agrega el primer producto, verifica el contador en 1 y el ítem dentro del carrito."""
    login(driver)

    # 1. Agregar el primer producto con su botón
    primer_producto = obtener_productos(driver)[0]
    nombre_producto = primer_producto.find_element(
        By.CSS_SELECTOR, "div.inventory_item_name"
    ).text
    boton = primer_producto.find_element(By.TAG_NAME, "button")
    boton.click()

    # 2. El contador del carrito debe mostrar "1"
    contador = esperar_elemento_visible(driver, (By.CSS_SELECTOR, ".shopping_cart_badge")).text
    assert contador == "1", f"Contador del carrito esperado '1', obtenido '{contador}'"

    # 3. Navegar al carrito
    esperar_elemento_clickeable(driver, (By.CSS_SELECTOR, ".shopping_cart_link")).click()
    WebDriverWait(driver, TIMEOUT).until(EC.url_contains("/cart.html"))
    assert "/cart.html" in driver.current_url, (
        f"No se redirigió a /cart.html. URL actual: {driver.current_url}"
    )

    # 4. El producto agregado aparece en el carrito
    nombres_en_carrito = [
        elemento.text
        for elemento in driver.find_elements(By.CSS_SELECTOR, "div.inventory_item_name")
    ]
    assert nombre_producto in nombres_en_carrito, (
        f"'{nombre_producto}' no aparece en el carrito. Contenido: {nombres_en_carrito}"
    )
