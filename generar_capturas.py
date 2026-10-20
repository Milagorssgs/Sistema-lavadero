import os
from playwright.sync_api import sync_playwright

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
BASE_URL = "http://127.0.0.1:5000"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "capturas")

screens = [
    {"name": "pantalla_login", "path": "/login", "auth": False, "filename": "login.png"},
    {"name": "pantalla_reserva_online", "path": "/reserva_online", "auth": False, "filename": "reserva_online.png"},
    {"name": "pantalla_dashboard", "path": "/dashboard", "auth": True, "filename": "dashboard.png"},
    {"name": "pantalla_clientes", "path": "/clientes", "auth": True, "filename": "clientes_lista.png"},
    {"name": "pantalla_cliente_nuevo", "path": "/cliente/nuevo", "auth": True, "filename": "cliente_nuevo.png"},
    {"name": "pantalla_vehiculos", "path": "/vehiculos", "auth": True, "filename": "vehiculos_lista.png"},
    {"name": "pantalla_servicios", "path": "/servicios", "auth": True, "filename": "servicios_lista.png"},
    {"name": "pantalla_turnos", "path": "/turnos", "auth": True, "filename": "turnos_agenda.png"},
    {"name": "pantalla_turno_nuevo", "path": "/turno/nuevo", "auth": True, "filename": "turno_nuevo.png"},
    {"name": "pantalla_reservas", "path": "/reservas", "auth": True, "filename": "reservas_lista.png"},
    {"name": "pantalla_pagos", "path": "/pagos", "auth": True, "filename": "pagos_lista.png"},
    {"name": "pantalla_comprobante", "path": "/comprobante/1", "auth": True, "filename": "comprobante.png"},
    {"name": "pantalla_presupuestos", "path": "/presupuestos", "auth": True, "filename": "presupuestos_lista.png"},
    {"name": "pantalla_presupuesto_nuevo", "path": "/presupuesto/nuevo", "auth": True, "filename": "presupuesto_nuevo.png"},
    {"name": "pantalla_reportes", "path": "/reportes", "auth": True, "filename": "reportes_estadisticas.png"},
    {"name": "pantalla_usuarios", "path": "/usuarios", "auth": True, "filename": "usuarios_lista.png"},
    {"name": "pantalla_configuracion", "path": "/configuracion", "auth": True, "filename": "configuracion.png"},
]

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME_PATH, headless=True)
        context = browser.new_context(viewport={"width": 1366, "height": 768})
        page = context.new_page()

        # Login first to get session
        print("Iniciando sesión como admin...")
        page.goto(f"{BASE_URL}/login")
        page.fill('input[name="username"]', "admin")
        page.fill('input[name="password"]', "admin123")
        page.click('button[type="submit"]')
        page.wait_for_load_state("networkidle")
        print("Sesión iniciada con éxito.")

        for item in screens:
            subfolder = os.path.join(OUTPUT_DIR, item["name"])
            os.makedirs(subfolder, exist_ok=True)
            target_file = os.path.join(subfolder, item["filename"])

            # If page requires not being logged in (like login page itself)
            if item["path"] == "/login":
                unauth_context = browser.new_context(viewport={"width": 1366, "height": 768})
                unauth_page = unauth_context.new_page()
                unauth_page.goto(f"{BASE_URL}/login")
                unauth_page.screenshot(path=target_file, full_page=True)
                unauth_context.close()
            else:
                page.goto(f"{BASE_URL}{item['path']}")
                page.wait_for_load_state("networkidle")
                page.screenshot(path=target_file, full_page=True)

            print(f"Captura guardada: {target_file}")

        browser.close()
    print("Todas las capturas se generaron correctamente.")

if __name__ == "__main__":
    main()
