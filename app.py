from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'super_secret_key_academica'
DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ----- RUTAS DE AUTENTICACIÓN -----
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db()
        user = conn.execute('SELECT * FROM usuarios WHERE username = ? AND activo = 1', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['rol'] = user['rol']
            return redirect(url_for('dashboard'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ----- DECORADOR PARA PROTEGER RUTAS -----
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('rol') not in ['administrador', 'dueno']:
            flash('Acceso denegado. Permisos insuficientes.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# ----- RUTAS PRINCIPALES -----
@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db()
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Resumen Dashboard
    turnos_hoy = conn.execute('SELECT COUNT(*) FROM turnos WHERE fecha = ? AND estado != "Cancelado"', (today,)).fetchone()[0]
    autos_atendidos = conn.execute('SELECT COUNT(*) FROM turnos WHERE fecha = ? AND estado = "Finalizado"', (today,)).fetchone()[0]
    ingresos = conn.execute('SELECT SUM(monto_abonado) FROM pagos WHERE fecha LIKE ?', (today + '%',)).fetchone()[0] or 0
    pagos_pendientes = conn.execute('SELECT SUM(saldo_pendiente) FROM pagos').fetchone()[0] or 0
    
    # Nuevas métricas
    total_clientes = conn.execute('SELECT COUNT(*) FROM clientes').fetchone()[0]
    total_vehiculos = conn.execute('SELECT COUNT(*) FROM vehiculos').fetchone()[0]
    servicios_realizados = conn.execute('SELECT COUNT(*) FROM turnos WHERE estado = "Finalizado"').fetchone()[0]
    reservas_pendientes = conn.execute('SELECT COUNT(*) FROM reservas WHERE estado = "Pendiente"').fetchone()[0]
    
    # Próximos turnos
    proximos_turnos = conn.execute('''
        SELECT t.id, t.hora, c.nombre || ' ' || c.apellido AS cliente, v.patente, s.nombre AS servicio, t.estado
        FROM turnos t
        JOIN clientes c ON t.cliente_id = c.id
        JOIN vehiculos v ON t.vehiculo_id = v.id
        JOIN servicios s ON t.servicio_id = s.id
        WHERE t.fecha = ? AND t.estado != 'Cancelado'
        ORDER BY t.hora ASC
        LIMIT 5
    ''', (today,)).fetchall()
    
    # Últimos pagos
    ultimos_pagos = conn.execute('''
        SELECT p.id, p.monto_abonado, p.metodo_pago, c.nombre || ' ' || c.apellido AS cliente
        FROM pagos p
        JOIN turnos t ON p.turno_id = t.id
        JOIN clientes c ON t.cliente_id = c.id
        ORDER BY p.id DESC
        LIMIT 5
    ''').fetchall()

    # Últimas reservas online
    ultimas_reservas = conn.execute('''
        SELECT r.id, r.fecha, r.hora, r.cliente_nombre || ' ' || r.cliente_apellido AS cliente, s.nombre AS servicio
        FROM reservas r
        JOIN servicios s ON r.servicio_id = s.id
        WHERE r.estado = 'Pendiente'
        ORDER BY r.fecha ASC, r.hora ASC
        LIMIT 5
    ''').fetchall()
    
    # Datos para gráfico: Ingresos últimos 7 días
    siete_dias = []
    ingresos_siete_dias = []
    for i in range(6, -1, -1):
        dia = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        siete_dias.append(dia[5:]) # MM-DD
        ing = conn.execute('SELECT SUM(monto_abonado) FROM pagos WHERE fecha LIKE ?', (dia + '%',)).fetchone()[0] or 0
        ingresos_siete_dias.append(ing)

    # Servicios más solicitados para el dashboard
    servicios_top = conn.execute('''
        SELECT s.nombre, COUNT(t.id) as cantidad
        FROM turnos t
        JOIN servicios s ON t.servicio_id = s.id
        WHERE t.estado = "Finalizado"
        GROUP BY s.id
        ORDER BY cantidad DESC
        LIMIT 5
    ''').fetchall()
        
    conn.close()
    
    return render_template('dashboard.html', 
                           turnos_hoy=turnos_hoy, 
                           autos_atendidos=autos_atendidos, 
                           ingresos=ingresos, 
                           pagos_pendientes=pagos_pendientes,
                           total_clientes=total_clientes,
                           total_vehiculos=total_vehiculos,
                           servicios_realizados=servicios_realizados,
                           reservas_pendientes=reservas_pendientes,
                           proximos_turnos=proximos_turnos,
                           ultimos_pagos=ultimos_pagos,
                           ultimas_reservas=ultimas_reservas,
                           fechas_grafico=siete_dias,
                           ingresos_grafico=ingresos_siete_dias,
                           servicios_top=servicios_top)

# ----- MÓDULO CLIENTES -----
@app.route('/clientes')
@login_required
def clientes():
    buscar = request.args.get('buscar', '')
    conn = get_db()
    query = 'SELECT * FROM clientes'
    params = []
    
    if buscar:
        query += ' WHERE nombre LIKE ? OR apellido LIKE ? OR telefono LIKE ?'
        params.extend([f'%{buscar}%', f'%{buscar}%', f'%{buscar}%'])
        
    clientes = conn.execute(query, params).fetchall()
    conn.close()
    return render_template('clientes.html', clientes=clientes, buscar=buscar)

@app.route('/cliente/nuevo', methods=['GET', 'POST'])
@login_required
def cliente_nuevo():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        email = request.form['email']
        direccion = request.form['direccion']
        
        conn = get_db()
        conn.execute('INSERT INTO clientes (nombre, apellido, telefono, email, direccion) VALUES (?, ?, ?, ?, ?)',
                     (nombre, apellido, telefono, email, direccion))
        conn.commit()
        conn.close()
        flash('Cliente registrado exitosamente.', 'success')
        return redirect(url_for('clientes'))
        
    return render_template('cliente_form.html', cliente=None)

@app.route('/cliente/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def cliente_editar(id):
    conn = get_db()
    cliente = conn.execute('SELECT * FROM clientes WHERE id = ?', (id,)).fetchone()
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        email = request.form['email']
        direccion = request.form['direccion']
        
        conn.execute('UPDATE clientes SET nombre=?, apellido=?, telefono=?, email=?, direccion=? WHERE id=?',
                     (nombre, apellido, telefono, email, direccion, id))
        conn.commit()
        conn.close()
        flash('Cliente actualizado correctamente.', 'success')
        return redirect(url_for('clientes'))
        
    conn.close()
    return render_template('cliente_form.html', cliente=cliente)

@app.route('/cliente/<int:id>/eliminar')
@login_required
def cliente_eliminar(id):
    conn = get_db()
    conn.execute('DELETE FROM clientes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Cliente eliminado correctamente.', 'success')
    return redirect(url_for('clientes'))

@app.route('/cliente/<int:id>')
@login_required
def cliente_detalle(id):
    conn = get_db()
    cliente = conn.execute('SELECT * FROM clientes WHERE id = ?', (id,)).fetchone()
    vehiculos = conn.execute('SELECT * FROM vehiculos WHERE cliente_id = ?', (id,)).fetchall()
    
    turnos = conn.execute('''
        SELECT t.*, v.patente, s.nombre as servicio
        FROM turnos t 
        JOIN vehiculos v ON t.vehiculo_id = v.id 
        JOIN servicios s ON t.servicio_id = s.id 
        WHERE t.cliente_id = ? ORDER BY t.fecha DESC
    ''', (id,)).fetchall()
    
    conn.close()
    return render_template('cliente_detalle.html', cliente=cliente, vehiculos=vehiculos, turnos=turnos)

# ----- MÓDULO VEHÍCULOS -----
@app.route('/vehiculos')
@login_required
def vehiculos():
    buscar = request.args.get('buscar', '')
    conn = get_db()
    
    query = '''
        SELECT v.*, c.nombre, c.apellido 
        FROM vehiculos v 
        JOIN clientes c ON v.cliente_id = c.id
    '''
    params = []
    
    if buscar:
        query += ' WHERE v.patente LIKE ? OR c.nombre LIKE ? OR c.apellido LIKE ?'
        params.extend([f'%{buscar}%', f'%{buscar}%', f'%{buscar}%'])
        
    vehiculos = conn.execute(query, params).fetchall()
    conn.close()
    return render_template('vehiculos.html', vehiculos=vehiculos, buscar=buscar)

@app.route('/vehiculo/nuevo', methods=['GET', 'POST'])
@login_required
def vehiculo_nuevo():
    conn = get_db()
    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        marca = request.form['marca']
        modelo = request.form['modelo']
        patente = request.form['patente'].upper()
        tipo = request.form['tipo']
        
        try:
            conn.execute('INSERT INTO vehiculos (cliente_id, marca, modelo, patente, tipo) VALUES (?, ?, ?, ?, ?)',
                         (cliente_id, marca, modelo, patente, tipo))
            conn.commit()
            flash('Vehículo registrado correctamente.', 'success')
            return redirect(url_for('vehiculos'))
        except sqlite3.IntegrityError:
            flash('La patente ya existe registrada en el sistema.', 'danger')
        finally:
            conn.close()
            
    clientes = conn.execute('SELECT id, nombre, apellido FROM clientes').fetchall()
    conn.close()
    return render_template('vehiculo_form.html', vehiculo=None, clientes=clientes)

@app.route('/vehiculo/<int:id>/eliminar')
@login_required
def vehiculo_eliminar(id):
    conn = get_db()
    conn.execute('DELETE FROM vehiculos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Vehículo eliminado correctamente.', 'success')
    return redirect(url_for('vehiculos'))

# ----- MÓDULO SERVICIOS -----
@app.route('/servicios')
@login_required
def servicios():
    conn = get_db()
    servicios = conn.execute('SELECT * FROM servicios').fetchall()
    conn.close()
    return render_template('servicios.html', servicios=servicios)

@app.route('/servicio/nuevo', methods=['GET', 'POST'])
@login_required
def servicio_nuevo():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        duracion = request.form['duracion']
        
        conn = get_db()
        conn.execute('INSERT INTO servicios (nombre, descripcion, precio, duracion) VALUES (?, ?, ?, ?)',
                     (nombre, descripcion, precio, duracion))
        conn.commit()
        conn.close()
        flash('Servicio creado correctamente.', 'success')
        return redirect(url_for('servicios'))
        
    return render_template('servicio_form.html', servicio=None)

@app.route('/servicio/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def servicio_editar(id):
    conn = get_db()
    servicio = conn.execute('SELECT * FROM servicios WHERE id = ?', (id,)).fetchone()
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        duracion = request.form['duracion']
        
        conn.execute('UPDATE servicios SET nombre=?, descripcion=?, precio=?, duracion=? WHERE id=?',
                     (nombre, descripcion, precio, duracion, id))
        conn.commit()
        conn.close()
        flash('Servicio actualizado correctamente.', 'success')
        return redirect(url_for('servicios'))
        
    conn.close()
    return render_template('servicio_form.html', servicio=servicio)

@app.route('/servicio/<int:id>/eliminar')
@login_required
def servicio_eliminar(id):
    conn = get_db()
    conn.execute('DELETE FROM servicios WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Servicio eliminado correctamente.', 'success')
    return redirect(url_for('servicios'))

# ----- MÓDULO TURNOS / AGENDA -----
@app.route('/turnos')
@login_required
def turnos():
    fecha_filtro = request.args.get('fecha', datetime.now().strftime('%Y-%m-%d'))
    conn = get_db()
    turnos = conn.execute('''
        SELECT t.*, c.nombre, c.apellido, c.telefono, v.marca, v.modelo, v.patente, s.nombre AS servicio, s.precio
        FROM turnos t
        JOIN clientes c ON t.cliente_id = c.id
        JOIN vehiculos v ON t.vehiculo_id = v.id
        JOIN servicios s ON t.servicio_id = s.id
        WHERE t.fecha = ?
        ORDER BY t.hora ASC
    ''', (fecha_filtro,)).fetchall()
    conn.close()
    return render_template('turnos.html', turnos=turnos, fecha_filtro=fecha_filtro)

@app.route('/turno/nuevo', methods=['GET', 'POST'])
@login_required
def turno_nuevo():
    conn = get_db()
    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        vehiculo_id = request.form['vehiculo_id']
        servicio_id = request.form['servicio_id']
        fecha = request.form['fecha']
        hora = request.form['hora']
        observaciones = request.form['observaciones']
        
        # Validar superposición de turnos
        existente = conn.execute('SELECT id FROM turnos WHERE fecha = ? AND hora = ? AND estado != "Cancelado"', (fecha, hora)).fetchone()
        
        if existente:
            flash('El horario seleccionado ya está ocupado. Por favor, seleccione otro horario.', 'danger')
        else:
            conn.execute('''
                INSERT INTO turnos (cliente_id, vehiculo_id, servicio_id, fecha, hora, estado, observaciones)
                VALUES (?, ?, ?, ?, ?, 'Pendiente', ?)
            ''', (cliente_id, vehiculo_id, servicio_id, fecha, hora, observaciones))
            conn.commit()
            conn.close()
            flash('Turno registrado exitosamente.', 'success')
            return redirect(url_for('turnos', fecha=fecha))
            
    clientes = conn.execute('SELECT id, nombre, apellido FROM clientes').fetchall()
    servicios = conn.execute('SELECT id, nombre, duracion FROM servicios WHERE estado = 1').fetchall()
    # Traer todos los vehiculos para armar la relacion en frontend
    vehiculos = conn.execute('SELECT id, cliente_id, marca, modelo, patente FROM vehiculos').fetchall()
    
    conn.close()
    return render_template('turno_form.html', turno=None, clientes=clientes, servicios=servicios, vehiculos=vehiculos)

@app.route('/turno/<int:id>/estado/<estado>')
@login_required
def turno_cambiar_estado(id, estado):
    conn = get_db()
    conn.execute('UPDATE turnos SET estado = ? WHERE id = ?', (estado, id))
    conn.commit()
    conn.close()
    flash(f'Estado del turno actualizado a {estado}.', 'info')
    return redirect(url_for('turnos'))

# ----- MÓDULO PAGOS -----
@app.route('/pagos')
@login_required
def pagos():
    conn = get_db()
    pagos = conn.execute('''
        SELECT p.*, t.fecha as turno_fecha, t.hora as turno_hora, c.nombre, c.apellido
        FROM pagos p
        JOIN turnos t ON p.turno_id = t.id
        JOIN clientes c ON t.cliente_id = c.id
        ORDER BY p.id DESC
    ''').fetchall()
    conn.close()
    return render_template('pagos.html', pagos=pagos)

@app.route('/pago/nuevo/<int:turno_id>', methods=['GET', 'POST'])
@login_required
def pago_nuevo(turno_id):
    conn = get_db()
    turno = conn.execute('''
        SELECT t.*, c.nombre, c.apellido, v.patente, s.nombre AS servicio_nombre, s.precio
        FROM turnos t
        JOIN clientes c ON t.cliente_id = c.id
        JOIN vehiculos v ON t.vehiculo_id = v.id
        JOIN servicios s ON t.servicio_id = s.id
        WHERE t.id = ?
    ''', (turno_id,)).fetchone()
    
    if request.method == 'POST':
        monto_abonado = float(request.form['monto_abonado'])
        metodo_pago = request.form['metodo_pago']
        
        subtotal = turno['precio']
        tipo_ajuste = request.form.get('tipo_ajuste')
        
        try:
            porcentaje_ajuste = float(request.form.get('porcentaje_ajuste') or 0)
        except ValueError:
            porcentaje_ajuste = 0
            
        monto_ajuste = 0
        monto_total = subtotal

        if tipo_ajuste == 'descuento':
            if porcentaje_ajuste > 100:
                flash('El descuento no puede superar el 100%.', 'danger')
                return redirect(url_for('pago_nuevo', turno_id=turno_id))
            if porcentaje_ajuste < 0:
                flash('El descuento no puede ser negativo.', 'danger')
                return redirect(url_for('pago_nuevo', turno_id=turno_id))
            monto_ajuste = subtotal * (porcentaje_ajuste / 100)
            monto_total = subtotal - monto_ajuste
        elif tipo_ajuste == 'aumento':
            if porcentaje_ajuste < 0:
                flash('El aumento no puede ser negativo.', 'danger')
                return redirect(url_for('pago_nuevo', turno_id=turno_id))
            monto_ajuste = subtotal * (porcentaje_ajuste / 100)
            monto_total = subtotal + monto_ajuste
        else:
            tipo_ajuste = None
            porcentaje_ajuste = 0
            
        saldo_pendiente = monto_total - monto_abonado
        estado = 'Pagado' if saldo_pendiente <= 0 else 'Pago parcial'
        
        conn.execute('''
            INSERT INTO pagos (turno_id, monto_total, monto_abonado, saldo_pendiente, metodo_pago, estado, subtotal, tipo_ajuste, porcentaje_ajuste, monto_ajuste)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (turno_id, monto_total, monto_abonado, saldo_pendiente, metodo_pago, estado, subtotal, tipo_ajuste, porcentaje_ajuste, monto_ajuste))
        
        # Opcional: Actualizar estado del turno
        if estado == 'Pagado':
            conn.execute('UPDATE turnos SET estado = "Finalizado" WHERE id = ?', (turno_id,))
            
        conn.commit()
        conn.close()
        flash('Pago registrado exitosamente.', 'success')
        return redirect(url_for('pagos'))
        
    conn.close()
    return render_template('pago_form.html', turno=turno)

@app.route('/comprobante/<int:pago_id>')
@login_required
def comprobante(pago_id):
    conn = get_db()
    pago = conn.execute('''
        SELECT p.*, t.fecha as turno_fecha, t.hora as turno_hora, 
               c.nombre, c.apellido, v.patente, s.nombre AS servicio_nombre
        FROM pagos p
        JOIN turnos t ON p.turno_id = t.id
        JOIN clientes c ON t.cliente_id = c.id
        JOIN vehiculos v ON t.vehiculo_id = v.id
        JOIN servicios s ON t.servicio_id = s.id
        WHERE p.id = ?
    ''', (pago_id,)).fetchone()
    
    config = conn.execute('SELECT * FROM configuracion').fetchall()
    config_dict = {row['clave']: row['valor'] for row in config}
    conn.close()
    
    return render_template('comprobante.html', pago=pago, config=config_dict)

# ----- MÓDULO REPORTES -----
@app.route('/reportes')
@login_required
def reportes():
    conn = get_db()
    
    # Total recaudado
    total_recaudado = conn.execute('SELECT SUM(monto_abonado) FROM pagos').fetchone()[0] or 0
    
    # Autos atendidos
    autos_atendidos = conn.execute('SELECT COUNT(*) FROM turnos WHERE estado = "Finalizado"').fetchone()[0] or 0
    
    # Servicios más utilizados
    servicios_top = conn.execute('''
        SELECT s.nombre, COUNT(t.id) as cantidad
        FROM turnos t
        JOIN servicios s ON t.servicio_id = s.id
        WHERE t.estado = "Finalizado"
        GROUP BY s.id
        ORDER BY cantidad DESC
        LIMIT 5
    ''').fetchall()
    
    conn.close()
    return render_template('reportes.html', total_recaudado=total_recaudado, autos_atendidos=autos_atendidos, servicios_top=servicios_top)

# ----- MÓDULO USUARIOS (Solo Admin) -----
@app.route('/usuarios')
@admin_required
def usuarios():
    conn = get_db()
    usuarios = conn.execute('SELECT id, username, rol, activo FROM usuarios').fetchall()
    conn.close()
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/usuario/nuevo', methods=['GET', 'POST'])
@admin_required
def usuario_nuevo():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        rol = request.form['rol']
        
        conn = get_db()
        try:
            conn.execute('INSERT INTO usuarios (username, password, rol, activo) VALUES (?, ?, ?, 1)', (username, password, rol))
            conn.commit()
            flash('Usuario creado exitosamente.', 'success')
            return redirect(url_for('usuarios'))
        except sqlite3.IntegrityError:
            flash('El nombre de usuario ya existe.', 'danger')
        finally:
            conn.close()
            
    return render_template('usuario_form.html', usuario=None)

# ----- RESERVA ONLINE PÚBLICA -----
@app.route('/reserva_online', methods=['GET', 'POST'])
def reserva_online():
    conn = get_db()
    if request.method == 'POST':
        cliente_nombre = request.form['cliente_nombre']
        cliente_apellido = request.form['cliente_apellido']
        cliente_telefono = request.form['cliente_telefono']
        vehiculo_marca = request.form['vehiculo_marca']
        vehiculo_modelo = request.form['vehiculo_modelo']
        vehiculo_patente = request.form['vehiculo_patente'].upper()
        servicio_id = request.form['servicio_id']
        fecha = request.form['fecha']
        hora = request.form['hora']
        
        # Check superposicion en turnos y reservas
        exist_turno = conn.execute('SELECT id FROM turnos WHERE fecha = ? AND hora = ? AND estado != "Cancelado"', (fecha, hora)).fetchone()
        exist_reserva = conn.execute('SELECT id FROM reservas WHERE fecha = ? AND hora = ? AND estado != "Cancelado"', (fecha, hora)).fetchone()
        
        if exist_turno or exist_reserva:
            flash('El horario seleccionado ya está ocupado. Intente con otro.', 'danger')
        else:
            conn.execute('''
                INSERT INTO reservas (cliente_nombre, cliente_apellido, cliente_telefono, vehiculo_marca, vehiculo_modelo, vehiculo_patente, servicio_id, fecha, hora)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (cliente_nombre, cliente_apellido, cliente_telefono, vehiculo_marca, vehiculo_modelo, vehiculo_patente, servicio_id, fecha, hora))
            conn.commit()
            conn.close()
            return render_template('reserva_exitosa.html', 
                                   nombre=cliente_nombre, 
                                   fecha=fecha, hora=hora)
            
    servicios = conn.execute('SELECT * FROM servicios WHERE estado = 1').fetchall()
    conn.close()
    return render_template('reserva_online.html', servicios=servicios)

@app.route('/reservas')
@login_required
def reservas_list():
    conn = get_db()
    reservas = conn.execute('''
        SELECT r.*, s.nombre AS servicio
        FROM reservas r
        JOIN servicios s ON r.servicio_id = s.id
        ORDER BY r.fecha ASC, r.hora ASC
    ''').fetchall()
    conn.close()
    return render_template('reservas.html', reservas=reservas)

# ----- MÓDULO PRESUPUESTOS -----
@app.route('/presupuestos')
@login_required
def presupuestos():
    conn = get_db()
    presupuestos_list = conn.execute('''
        SELECT p.*, c.nombre, c.apellido, v.patente 
        FROM presupuestos p 
        JOIN clientes c ON p.cliente_id = c.id 
        JOIN vehiculos v ON p.vehiculo_id = v.id
        ORDER BY p.id DESC
    ''').fetchall()
    conn.close()
    return render_template('presupuestos.html', presupuestos=presupuestos_list)

@app.route('/presupuesto/nuevo', methods=['GET', 'POST'])
@login_required
def presupuesto_nuevo():
    conn = get_db()
    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        vehiculo_id = request.form['vehiculo_id']
        servicios_ids = request.form.getlist('servicios')
        
        if not servicios_ids:
            flash('Debe seleccionar al menos un servicio.', 'danger')
            return redirect(url_for('presupuesto_nuevo'))
            
        # Calcular total
        total = 0
        servicios_data = []
        for s_id in servicios_ids:
            servicio = conn.execute('SELECT precio FROM servicios WHERE id = ?', (s_id,)).fetchone()
            total += servicio['precio']
            servicios_data.append((s_id, servicio['precio']))
            
        # Insertar presupuesto
        cur = conn.cursor()
        cur.execute('INSERT INTO presupuestos (cliente_id, vehiculo_id, total) VALUES (?, ?, ?)', (cliente_id, vehiculo_id, total))
        presupuesto_id = cur.lastrowid
        
        # Insertar detalle
        for s_id, precio in servicios_data:
            cur.execute('INSERT INTO presupuesto_detalle (presupuesto_id, servicio_id, precio) VALUES (?, ?, ?)', (presupuesto_id, s_id, precio))
            
        conn.commit()
        conn.close()
        flash('Presupuesto generado correctamente.', 'success')
        return redirect(url_for('presupuesto_ver', id=presupuesto_id))
        
    clientes = conn.execute('SELECT id, nombre, apellido FROM clientes').fetchall()
    vehiculos = conn.execute('SELECT id, cliente_id, marca, modelo, patente FROM vehiculos').fetchall()
    servicios = conn.execute('SELECT * FROM servicios WHERE estado = 1').fetchall()
    conn.close()
    return render_template('presupuesto_form.html', clientes=clientes, vehiculos=vehiculos, servicios=servicios)

@app.route('/presupuesto/<int:id>')
@login_required
def presupuesto_ver(id):
    conn = get_db()
    presupuesto = conn.execute('''
        SELECT p.*, c.nombre, c.apellido, c.telefono, c.email, v.marca, v.modelo, v.patente 
        FROM presupuestos p 
        JOIN clientes c ON p.cliente_id = c.id 
        JOIN vehiculos v ON p.vehiculo_id = v.id
        WHERE p.id = ?
    ''', (id,)).fetchone()
    
    detalles = conn.execute('''
        SELECT pd.*, s.nombre as servicio_nombre
        FROM presupuesto_detalle pd
        JOIN servicios s ON pd.servicio_id = s.id
        WHERE pd.presupuesto_id = ?
    ''', (id,)).fetchall()
    
    config = conn.execute('SELECT * FROM configuracion').fetchall()
    config_dict = {row['clave']: row['valor'] for row in config}
    
    conn.close()
    return render_template('presupuesto_detalle.html', presupuesto=presupuesto, detalles=detalles, config=config_dict)

# ----- MÓDULO CONFIGURACIÓN -----
@app.route('/configuracion', methods=['GET', 'POST'])
@admin_required
def configuracion():
    conn = get_db()
    
    if request.method == 'POST':
        nombre_lavadero = request.form['nombre_lavadero']
        horario_apertura = request.form['horario_apertura']
        horario_cierre = request.form['horario_cierre']
        
        conn.execute('INSERT OR REPLACE INTO configuracion (clave, valor) VALUES (?, ?)', ('nombre_lavadero', nombre_lavadero))
        conn.execute('INSERT OR REPLACE INTO configuracion (clave, valor) VALUES (?, ?)', ('horario_apertura', horario_apertura))
        conn.execute('INSERT OR REPLACE INTO configuracion (clave, valor) VALUES (?, ?)', ('horario_cierre', horario_cierre))
        
        conn.commit()
        flash('Configuración actualizada correctamente.', 'success')
        
    config = conn.execute('SELECT * FROM configuracion').fetchall()
    config_dict = {row['clave']: row['valor'] for row in config}
    conn.close()
    
    return render_template('configuracion.html', config=config_dict)

if __name__ == '__main__':
    app.run(debug=True)
