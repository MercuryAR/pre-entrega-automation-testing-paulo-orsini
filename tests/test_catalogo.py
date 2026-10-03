"""Caso 4.2 - Navegación y verificación del catálogo."""
import logging

import pytest
from selenium.webdriver.common.by import By

from utils.helpers import esperar_elemento_visible, login, obtener_productos

logger = logging.getLogger(__name__)


@pytest.fixture
def inventario(driver):
    """Deja el navegador logueado y posicionado en el inventario."""
    login(driver)
    return driver


def test_titulo_del_inventario(inventario):
    """El título de la ventana y de la sección son los esperados."""
    titulo_seccion = esperar_elemento_visible(
        inventario, (By.CSS_SELECTOR, "div.header_secondary_container .title")
    ).text
    assert inventario.title == "Swag Labs", (
        f"Título de ventana esperado 'Swag Labs', obtenido '{inventario.title}'"
    )
    assert titulo_seccion == "Products", (
        f"Título de sección esperado 'Products', obtenido '{titulo_seccion}'"
    )


def test_hay_productos_visibles(inventario):
    """El catálogo muestra al menos un producto."""
    productos = obtener_productos(inventario)
    assert len(productos) > 0, "No se encontraron productos visibles en el inventario"
    assert productos[0].is_displayed(), "El primer producto no está visible"


def test_elementos_de_interfaz_presentes(inventario):
    """El menú hamburguesa, el filtro y el carrito están presentes y visibles."""
    elementos = {
        "menú hamburguesa": "#react-burger-menu-btn",
        "filtro de orden": "select.product_sort_container",
        "ícono del carrito": ".shopping_cart_link",
    }
    for nombre, selector in elementos.items():
        elemento = esperar_elemento_visible(inventario, (By.CSS_SELECTOR, selector))
        assert elemento.is_displayed(), f"El elemento '{nombre}' no está visible"


def test_nombre_y_precio_del_primer_producto(inventario):
    """Lista nombre y precio del primer producto y valida que no estén vacíos."""
    primero = obtener_productos(inventario)[0]
    nombre = primero.find_element(By.CSS_SELECTOR, "div.inventory_item_name").text
    precio = primero.find_element(By.CSS_SELECTOR, "div.inventory_item_price").text

    logger.info("Primer producto: %s - %s", nombre, precio)
    print(f"Primer producto: {nombre} - {precio}")

    assert nombre, "El nombre del primer producto está vacío"
    assert precio.startswith("$"), f"El precio debería comenzar con '$', obtenido '{precio}'"
