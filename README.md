# Pre-Entrega – Automation Testing (Talento Tech)

## Propósito
Automatizar flujos básicos de navegación en [saucedemo.com](https://www.saucedemo.com): login, verificación del catálogo y carrito de compras, aplicando esperas explícitas, estrategias de localización y validación de estados.

## Tecnologías
- Python 3
- Selenium WebDriver (Chrome; el driver lo gestiona Selenium Manager)
- Pytest
- pytest-html (reporte HTML)
- Git + GitHub

## Estructura
```
tests/      test_login.py, test_catalogo.py, test_carrito.py
utils/      helpers.py (driver, esperas, login)
reports/    reporte.html, ejecucion.log y capturas de fallos
conftest.py fixture del navegador y captura automática ante fallos
pytest.ini  opciones por defecto (reporte HTML y logs)
```

## Instalación
Requiere Google Chrome instalado.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Ejecución
```bash
pytest -v --html=reports/reporte.html
```
Opcional, sin abrir la ventana del navegador: `pytest --headless`.

## Evidencias
- Reporte HTML: `reports/reporte.html`
- Logs de ejecución: `reports/ejecucion.log`
- Capturas de pantalla automáticas de los tests que fallan: `reports/*.png` (también embebidas en el reporte)

## Casos cubiertos
1. **Login:** credenciales válidas, URL `/inventory.html` y título "Products" / "Swag Labs".
2. **Catálogo:** título, productos visibles, menú/filtro/carrito presentes, nombre y precio del primer producto.
3. **Carrito:** agrega el primer producto, contador en `1` y producto presente en el carrito.

Cada test abre su propio navegador, por lo que son independientes entre sí.
