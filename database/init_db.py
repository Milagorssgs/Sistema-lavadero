import sqlite3
import os
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database.db')

def init_db():
    print(f"Creando base de datos en: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Tabla Configuración
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS configuracion (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        clave TEXT UNIQUE NOT NULL,
        valor TEXT NOT NULL
    )
    ''')

    # Tabla Usuarios
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        rol TEXT NOT NULL,
        activo INTEGER DEFAULT 1
    )
    ''')

    # Tabla Clientes
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        apellido TEXT NOT NULL,
        telefono TEXT NOT NULL,
        email TEXT,
        direccion TEXT,
        fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Tabla Vehículos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS vehiculos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL,
        marca TEXT NOT NULL,
        modelo TEXT NOT NULL,
        patente TEXT UNIQUE NOT NULL,
        tipo TEXT NOT NULL,
        FOREIGN KEY (cliente_id) REFERENCES clientes(id)
    )
    ''')

    # Tabla Servicios
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS servicios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT,
        precio REAL NOT NULL,
        duracion INTEGER NOT NULL,
        estado INTEGER DEFAULT 1
    )
    ''')

    # Tabla Turnos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS turnos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL,
        vehiculo_id INTEGER NOT NULL,
        servicio_id INTEGER NOT NULL,
        fecha TEXT NOT NULL,
        hora TEXT NOT NULL,
        estado TEXT NOT NULL DEFAULT 'Pendiente',
        observaciones TEXT,
        FOREIGN KEY (cliente_id) REFERENCES clientes(id),
        FOREIGN KEY (vehiculo_id) REFERENCES vehiculos(id),
        FOREIGN KEY (servicio_id) REFERENCES servicios(id)
    )
    ''')

    # Tabla Reservas Online
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reservas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_nombre TEXT NOT NULL,
        cliente_apellido TEXT NOT NULL,
        cliente_telefono TEXT NOT NULL,
        vehiculo_marca TEXT NOT NULL,
        vehiculo_modelo TEXT NOT NULL,
        vehiculo_patente TEXT NOT NULL,
        servicio_id INTEGER NOT NULL,
        fecha TEXT NOT NULL,
        hora TEXT NOT NULL,
        estado TEXT NOT NULL DEFAULT 'Pendiente',
        fecha_reserva TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (servicio_id) REFERENCES servicios(id)
    )
    ''')

    # Tabla Pagos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pagos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        turno_id INTEGER NOT NULL,
        monto_total REAL NOT NULL,
        monto_abonado REAL NOT NULL,
        saldo_pendiente REAL NOT NULL,
        metodo_pago TEXT NOT NULL,
        estado TEXT NOT NULL,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (turno_id) REFERENCES turnos(id)
    )
    ''')

    # Tabla Presupuestos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS presupuestos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL,
        vehiculo_id INTEGER NOT NULL,
        total REAL NOT NULL,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (cliente_id) REFERENCES clientes(id),
        FOREIGN KEY (vehiculo_id) REFERENCES vehiculos(id)
    )
    ''')

    # Tabla Presupuesto Detalle
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS presupuesto_detalle (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        presupuesto_id INTEGER NOT NULL,
        servicio_id INTEGER NOT NULL,
        precio REAL NOT NULL,
        FOREIGN KEY (presupuesto_id) REFERENCES presupuestos(id),
        FOREIGN KEY (servicio_id) REFERENCES servicios(id)
    )
    ''')

    # CREACIÓN DE ÍNDICES PARA OPTIMIZAR VELOCIDAD
    print("Creando índices...")
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_vehiculos_patente ON vehiculos(patente);')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_vehiculos_cliente ON vehiculos(cliente_id);')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_turnos_fecha_estado ON turnos(fecha, estado);')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_turnos_cliente ON turnos(cliente_id);')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_pagos_turno ON pagos(turno_id);')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_pagos_fecha ON pagos(fecha);')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_reservas_estado ON reservas(estado);')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_clientes_telefono ON clientes(telefono);')

    # INSERTAR DATOS DE PRUEBA
    
    # Configuracion
    cursor.execute("INSERT OR IGNORE INTO configuracion (clave, valor) VALUES ('nombre_lavadero', 'Lavadero AutoLimpio')")
    
    # Usuarios (admin, empleado, dueño)
    admin_pass = generate_password_hash('admin123')
    empleado_pass = generate_password_hash('empleado123')
    dueno_pass = generate_password_hash('dueno123')
    
    cursor.execute("INSERT OR IGNORE INTO usuarios (username, password, rol) VALUES ('admin', ?, 'administrador')", (admin_pass,))
    cursor.execute("INSERT OR IGNORE INTO usuarios (username, password, rol) VALUES ('empleado', ?, 'empleado')", (empleado_pass,))
    cursor.execute("INSERT OR IGNORE INTO usuarios (username, password, rol) VALUES ('dueno', ?, 'dueno')", (dueno_pass,))

    # Clientes
    clientes_data = [
        ('Juan', 'Pérez', '1122334455', 'juan@mail.com', 'Calle Falsa 123'),
        ('María', 'González', '1199887766', 'maria@mail.com', 'Av. Siempre Viva 742'),
        ('Carlos', 'Rodríguez', '1155443322', 'carlos@mail.com', 'Ruta 9 km 45')
    ]
    cursor.executemany("INSERT INTO clientes (nombre, apellido, telefono, email, direccion) SELECT ?, ?, ?, ?, ? WHERE NOT EXISTS(SELECT 1 FROM clientes WHERE telefono=?)", 
                       [(c[0], c[1], c[2], c[3], c[4], c[2]) for c in clientes_data])

    # Vehículos
    vehiculos_data = [
        (1, 'Toyota', 'Corolla', 'AA123BB', 'Auto'),
        (2, 'Volkswagen', 'Gol', 'AB456CC', 'Auto'),
        (3, 'Ford', 'Fiesta', 'AC789DD', 'Auto')
    ]
    cursor.executemany("INSERT OR IGNORE INTO vehiculos (cliente_id, marca, modelo, patente, tipo) VALUES (?, ?, ?, ?, ?)", vehiculos_data)

    # Servicios
    servicios_data = [
        ('Lavado básico', 'Lavado exterior y secado', 5000, 30),
        ('Lavado completo', 'Lavado exterior, interior y aspirado', 8000, 60),
        ('Lavado premium', 'Lavado completo, encerado y limpieza de tapizados', 15000, 120),
        ('Limpieza interior', 'Aspirado profundo y limpieza de plásticos', 4000, 45)
    ]
    cursor.executemany("INSERT INTO servicios (nombre, descripcion, precio, duracion) SELECT ?, ?, ?, ? WHERE NOT EXISTS(SELECT 1 FROM servicios WHERE nombre=?)", 
                       [(s[0], s[1], s[2], s[3], s[0]) for s in servicios_data])

    conn.commit()
    conn.close()
    print("Base de datos inicializada correctamente.")

if __name__ == '__main__':
    init_db()
