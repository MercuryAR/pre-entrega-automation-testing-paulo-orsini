"""Fixtures y hooks compartidos por todos los tests."""
import logging
import os
from datetime import datetime

import pytest
from pytest_html import extras

from utils.helpers import crear_driver

CARPETA_REPORTES = os.path.join(os.path.dirname(__file__), "reports")
logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    parser.addoption("--headless", action="store_true", default=False,
                     help="Ejecuta Chrome sin interfaz gráfica")


@pytest.fixture
def driver(request):
    """Abre un navegador nuevo por test (tests independientes) y lo cierra al terminar."""
    navegador = crear_driver(headless=request.config.getoption("--headless"))
    yield navegador
    navegador.quit()
    logger.info("Navegador cerrado")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Si un test falla, guarda una captura en reports/ y la adjunta al reporte HTML."""
    resultado = yield
    reporte = resultado.get_result()
    if reporte.when == "call" and reporte.failed and "driver" in item.funcargs:
        os.makedirs(CARPETA_REPORTES, exist_ok=True)
        marca_tiempo = datetime.now().strftime("%Y%m%d_%H%M%S")
        ruta = os.path.join(CARPETA_REPORTES, f"{item.name}_{marca_tiempo}.png")
        item.funcargs["driver"].save_screenshot(ruta)
        logger.error("Test '%s' falló. Captura guardada en %s", item.name, ruta)
        reporte.extras = getattr(reporte, "extras", []) + [
            extras.png(item.funcargs["driver"].get_screenshot_as_base64())
        ]
