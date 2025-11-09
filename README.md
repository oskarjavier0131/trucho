# Trucho - E-commerce Django Application

Una aplicación web de e-commerce construida con Django 5.1, que incluye sistema de carrito de compras, gestión de pedidos, autenticación de usuarios y blog de notas.

## Características

- 🛒 **Carrito de compras** con gestión de sesiones
- 📦 **Sistema de pedidos** con confirmación por email
- 👤 **Autenticación de usuarios** (registro/login)
- 📝 **Sistema de blog/notas** con categorías
- 🏪 **Catálogo de productos** con categorías e imágenes
- 📧 **Formulario de contacto** con envío de emails
- 🔒 **Seguridad mejorada** con variables de entorno
- 📊 **Panel de administración** optimizado

## Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Virtualenv (recomendado)

## Instalación

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd trucho
```

### 2. Crear y activar entorno virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

**Para desarrollo:**
```bash
pip install -r requirements-dev.txt
```

**Para producción:**
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Copia el archivo `.env.example` a `.env` y configura tus valores:

```bash
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac
```

Edita el archivo `.env` con tus configuraciones:

```env
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-contraseña-de-aplicación
```

**Nota:** Para Gmail, necesitas generar una [contraseña de aplicación](https://support.google.com/accounts/answer/185833).

### 5. Aplicar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crear superusuario

```bash
python manage.py createsuperuser
```

### 7. Ejecutar el servidor de desarrollo

```bash
python manage.py runserver
```

La aplicación estará disponible en `http://127.0.0.1:8000/`

## Estructura del Proyecto

```
trucho/
├── autentificacion/    # App de autenticación (login/registro)
├── carro/             # App del carrito de compras
├── contacto/          # App de formulario de contacto
├── media/             # Archivos multimedia subidos
├── notas/             # App de blog/notas
├── pedidos/           # App de gestión de pedidos
├── servicios/         # App de servicios
├── tienda/            # App de catálogo de productos
├── trucho/            # Configuración principal del proyecto
├── trucho_app/        # App principal (home)
├── .env               # Variables de entorno (no versionado)
├── .env.example       # Ejemplo de variables de entorno
├── manage.py          # Script de gestión de Django
└── requirements.txt   # Dependencias del proyecto
```

## Comandos Útiles

### Desarrollo

```bash
# Ejecutar servidor de desarrollo
python manage.py runserver

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Acceder al shell de Django
python manage.py shell

# Ejecutar tests
python manage.py test

# Crear superusuario
python manage.py createsuperuser
```

### Administración

- Panel de administración: `http://127.0.0.1:8000/admin/`
- Debug toolbar (solo en modo DEBUG): `http://127.0.0.1:8000/__debug__/`

## Configuración de Email

Para que el sistema de confirmación de pedidos funcione, necesitas configurar las credenciales de email en el archivo `.env`:

1. Si usas Gmail, habilita la verificación en 2 pasos
2. Genera una contraseña de aplicación
3. Configura `EMAIL_HOST_USER` y `EMAIL_HOST_PASSWORD` en `.env`

## Seguridad

⚠️ **IMPORTANTE para producción:**

1. Cambia `DEBUG=False` en el archivo `.env`
2. Genera una nueva `SECRET_KEY` segura
3. Configura `ALLOWED_HOSTS` con tu dominio
4. Usa HTTPS (configura SSL/TLS)
5. Usa una base de datos de producción (PostgreSQL recomendado)
6. Nunca commitees el archivo `.env` al repositorio

## Tecnologías Utilizadas

- **Django 5.1** - Framework web
- **Bootstrap 4** - Framework CSS
- **Crispy Forms** - Renderizado de formularios
- **Pillow** - Procesamiento de imágenes
- **SQLite** - Base de datos (desarrollo)
- **Django Debug Toolbar** - Herramienta de debugging

## Mejoras Implementadas

✅ Variables de entorno para seguridad
✅ Logging configurado
✅ Manejo de errores robusto
✅ Validaciones en vistas
✅ Optimización de queries (select_related)
✅ Uso de DecimalField para precios
✅ Transacciones atómicas en pedidos
✅ Admin mejorado con inlines y filtros
✅ Debug toolbar para desarrollo

## Contribución

Para contribuir al proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## Licencia

[Especifica tu licencia aquí]

## Soporte

Para reportar bugs o solicitar nuevas características, abre un issue en el repositorio.
