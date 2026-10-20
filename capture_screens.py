from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # 1. Login Page
        page.goto('http://127.0.0.1:5000/login')
        page.screenshot(path='screen_login.png')
        
        # Login
        page.fill('input[name="username"]', 'admin')
        page.fill('input[name="password"]', 'admin123')
        page.click('button[type="submit"]')
        page.wait_for_url('http://127.0.0.1:5000/dashboard')
        
        # 2. Dashboard
        page.screenshot(path='screen_dashboard.png', full_page=True)
        
        # 3. Turnos
        page.goto('http://127.0.0.1:5000/turnos')
        page.screenshot(path='screen_turnos.png', full_page=True)

        # 4. Clientes
        page.goto('http://127.0.0.1:5000/clientes')
        page.screenshot(path='screen_clientes.png', full_page=True)
        
        # 5. Reserva Online
        page.goto('http://127.0.0.1:5000/reserva_online')
        page.screenshot(path='screen_reserva.png', full_page=True)
        
        browser.close()

if __name__ == '__main__':
    run()
