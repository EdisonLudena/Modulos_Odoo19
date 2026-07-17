# Guía de Comandos: Odoo 19

```bash
# ==========================================
# 1. PRIMER ARRANQUE E INICIALIZACIÓN
# ==========================================

# Asegurar ubicación y activar el entorno virtual
cd ~/odoo19-dev
source venv/bin/activate

# Inicializar el esquema base de la base de datos (Solo la primera vez)
python odoo/odoo-bin --config=odoo-dev.conf --init=base --database=odoo19_dev --without-demo=False --stop-after-init

# Arrancar el servidor de desarrollo de forma definitiva
python odoo/odoo-bin --config=odoo-dev.conf

# OUTPUT ESPERADO:
# INFO odoo19_dev odoo.service.server: HTTP service (werkzeug) running on 127.0.0.1:8069
# 
# Acceso web: http://localhost:8069
# Usuario: admin
# Contraseña: admin


# ==========================================
# 2. GESTIÓN DE SERVICIOS
# ==========================================

# Matar el servicio del anterior módulo (si el puerto está ocupado)
sudo fuser -k 8069/tcp

# Gestor de bases de datos web:
# http://localhost:8069/web/database/manager


# ==========================================
# 3. CREACIÓN DE MÓDULOS
# ==========================================

# Crear módulo en donde estoy parado
python3 ../odoo/odoo-bin scaffold mi_modulo_2 .


# ==========================================
# 4. FORZAR LA LECTURA / ACTUALIZACIÓN DE MÓDULOS
# ==========================================

# Forzar lectura de un módulo específico (ejemplo principal)
python odoo/odoo-bin --config=odoo-dev.conf -d odoo19_dev -u mi_modulo_2 --stop-after-init

# Otras variantes de actualización:
python3 odoo/odoo-bin -c odoo-dev.conf -d nombre_de_tu_base_de_datos -u mi_modulo_1
python3 odoo/odoo-bin -c odoo-dev.conf -d nombre_base_de_datos -u mi_modulo_2
python3 odoo/odoo-bin -c odoo-dev.conf -d modulo2 -u mi_modulo_2
