# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Django 5.1 e-commerce web application ("Trucho") with shopping cart functionality, user authentication, blog/notes system, and contact forms. The project is configured for Spanish language (`LANGUAGE_CODE = 'es-eu'`) and uses SQLite as the database.

**Status:** ✅ Fully optimized and production-ready (with proper environment configuration)

## Development Commands

### First-Time Setup
```bash
# 1. Activate virtual environment (Windows)
venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements-dev.txt  # For development
pip install -r requirements.txt      # For production only

# 3. Copy and configure environment variables
copy .env.example .env  # Edit .env with your values

# 4. Apply migrations
python manage.py makemigrations
python manage.py migrate

# 5. Create superuser
python manage.py createsuperuser
```

### Running the Application
```bash
# Run development server
python manage.py runserver

# Access admin panel: http://127.0.0.1:8000/admin/
# Access debug toolbar: http://127.0.0.1:8000/__debug__/ (DEBUG mode only)
```

### Database Migrations
```bash
# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migration status
python manage.py showmigrations
```

### Testing
```bash
# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test <app_name>

# Run with coverage (requires pytest-cov)
pytest --cov=. --cov-report=html
```

### Code Quality
```bash
# Format code with black
black .

# Sort imports with isort
isort .

# Check code style with flake8
flake8 .
```

### Static Files
```bash
# Collect static files (for production)
python manage.py collectstatic
```

## Architecture

### Django Apps Structure

The project follows a modular Django architecture with 8 specialized apps:

1. **trucho_app** - Main/home app (root URL handler)
2. **tienda** - Product catalog with categories and products
3. **carro** - Shopping cart with session-based storage
4. **pedidos** - Order processing and management
5. **autentificacion** - User login/registration
6. **notas** - Blog/notes system with categories
7. **servicios** - Services display
8. **contacto** - Contact form with email functionality

### Key Architectural Patterns

**Shopping Cart System** (`carro/`):
- ✅ **Optimized:** Session-based cart storage using Decimal for precise calculations
- Cart class in `carro/carro.py` with methods:
  - `agregar()` - Adds product or increments quantity
  - `eliminar()` - Removes product completely
  - `restar_producto()` - Decrements quantity or removes if zero
  - `limpiar_carro()` - Empties cart
  - `get_total()` - Calculates total using Decimal
  - `get_cantidad_total()` - Returns total item count
  - `__iter__()` - Allows iteration with calculated subtotals
- Custom context processor (`carro/context_processors.py`) provides `importe_total_carro` globally
- Cart structure: `{producto_id: {producto_id, nombre, precio_unitario, cantidad, imagen}}`
- ⚠️ **Note:** precio_unitario stored as string in session, converted to Decimal when needed

**Order System** (`pedidos/`):
- ✅ **Optimized:** Uses atomic transactions to ensure data integrity
- `Pedido` model with `@property total` that calculates using aggregation
- `LineaPedido` model stores: user, pedido, producto, cantidad, precio (snapshot at purchase time)
- `LineaPedido.subtotal` property for individual line calculation
- Email confirmation sent after successful order (non-blocking if fails)
- Validates product availability before creating order
- Empty cart validation before processing

**Authentication Flow** (`autentificacion/`):
- Custom auth app handles login/registration
- Uses Django's built-in User model via `get_user_model()`
- Login required decorator on order processing views
- Templates in `autentificacion/templates/login/` and `autentificacion/templates/registro/`

**Email Configuration**:
- ✅ **Secured:** All email settings use environment variables
- SMTP configured for Gmail by default (configurable)
- Contact form and order confirmations use Django email backend
- Logging on email failures
- Template-based HTML emails with plaintext fallback

**Media Files**:
- Uploaded files stored in `media/` directory (gitignored)
- Image uploads organized by app: `tienda/`, `nota/`, `servicios/`
- Media URL pattern configured in `trucho_app/urls.py` for development
- ⚠️ **Production:** Serve media files through web server (nginx/Apache), not Django

### Models Relationships

```
User (Django Auth)
├── Notas (author)
├── Pedido
└── LineaPedido

Producto
├── CategoriaProd (ForeignKey)
└── LineaPedido (ForeignKey)

Notas
└── Categoria (ManyToMany)

Pedido
└── LineaPedido (ForeignKey)
```

### Template System

- Templates organized within each app's `templates/` directory
- Bootstrap 4 integration via static files in `trucho_app/static/`
- Crispy Forms with Bootstrap 4 pack for form rendering
- Custom CSS in `trucho_app/static/trucho_app/css/gestion.css`

## Important Configuration Notes

### Security ✅ FIXED
- ✅ `SECRET_KEY` now uses environment variables via python-decouple
- ✅ `DEBUG` configurable via .env file
- ✅ Email credentials use environment variables
- ✅ `ALLOWED_HOSTS` configurable via .env
- ✅ Security headers configured for production (HSTS, XSS protection, etc.)
- ✅ Logging configured with rotating file handler
- ⚠️ `.env` file created with working credentials - **DO NOT COMMIT TO GIT**

### Environment Variables (.env)
Required variables (see `.env.example`):
```
SECRET_KEY=<generated-key>
DEBUG=True/False
ALLOWED_HOSTS=comma,separated,hosts
EMAIL_HOST_USER=email@gmail.com
EMAIL_HOST_PASSWORD=app-password
```

### Database
- Using SQLite (`db.sqlite3`) - gitignored
- Located in project root
- ⚠️ **Production:** Switch to PostgreSQL or MySQL
- Configuration ready for DATABASE_URL environment variable

### Context Processors
- ✅ **Fixed:** `carro.context_processors.importe_total_carro` properly handles all cases
- Returns Decimal('0') for empty carts or unauthenticated users
- No longer returns error messages as numbers

## URL Structure

```
/                          - Home (trucho_app)
/admin/                    - Django admin
/servicios/                - Services
/notas/                    - Blog/notes
/contacto/                 - Contact form
/tienda/                   - Product catalog
/carro/                    - Shopping cart
/autentificacion/          - Login/registration
/pedidos/                  - Order management
/media/<path>              - Media files (development only)
```

## Dependencies

### Production (requirements.txt)
- Django 5.1 - Web framework
- Pillow 10.4.0 - Image processing
- django-crispy-forms 2.3 - Form rendering
- crispy-bootstrap4 2024.10 - Bootstrap 4 templates
- python-decouple 3.8 - Environment variable management
- asgiref 3.8.1 - ASGI support
- sqlparse 0.5.1 - SQL parsing
- tzdata 2024.1 - Timezone data

### Development (requirements-dev.txt)
Additional tools for development:
- django-debug-toolbar 4.4.6 - Debugging
- pytest 8.3.3 - Testing framework
- pytest-django 4.9.0 - Django integration for pytest
- pytest-cov 5.0.0 - Coverage reporting
- flake8 7.1.1 - Code linting
- black 24.8.0 - Code formatting
- isort 5.13.2 - Import sorting

## Optimizations Implemented ✅

### 1. Model Improvements
- ✅ Fixed `LineaPedido.precio` field (now DecimalField)
- ✅ Changed all price fields from FloatField to DecimalField for precision
- ✅ Fixed `auto_now_add` vs `auto_now` issues in timestamp fields
- ✅ Renamed `update` fields to `updated` for consistency
- ✅ Changed CharField to TextField for content fields (notas, servicios)
- ✅ Added `@property subtotal` to LineaPedido model

### 2. Cart System Improvements
- ✅ Refactored to use Decimal for all calculations
- ✅ Changed from storing total price to storing unit price + quantity
- ✅ Added `__iter__()`, `__len__()` methods for better usability
- ✅ Added `get_total()` and `get_cantidad_total()` helper methods
- ✅ Improved method names and docstrings

### 3. Views Enhancements
- ✅ Added comprehensive error handling with try/except blocks
- ✅ Implemented logging throughout (carro, tienda, pedidos)
- ✅ Changed from `.get()` to `get_object_or_404()` for better errors
- ✅ Added user messages (success, error, warning) for feedback
- ✅ Product availability validation before cart operations
- ✅ Empty cart validation before order processing
- ✅ Atomic transactions for order creation
- ✅ Added query optimization with `select_related('categorias')`
- ✅ Implemented pagination in tienda view (12 items per page)

### 4. Admin Panel Improvements
- ✅ Enhanced ProductoAdmin with list_editable for quick updates
- ✅ Added fieldsets for better organization
- ✅ Created LineaPedidoInline for Pedido admin
- ✅ Added search, filters, and ordering to all admin classes
- ✅ Custom methods to display calculated fields (total, subtotal)

### 5. Security Enhancements
- ✅ All sensitive settings use environment variables
- ✅ Generated new SECRET_KEY
- ✅ Security headers configured for production
- ✅ .gitignore properly configured
- ✅ Created .env.example template

### 6. Development Tools
- ✅ Django Debug Toolbar integrated (DEBUG mode only)
- ✅ Logging configured with file rotation (5MB max, 5 backups)
- ✅ Created requirements-dev.txt with testing/linting tools
- ✅ Added README.md with setup instructions

### 7. Code Quality
- ✅ Added docstrings to all functions and classes
- ✅ Consistent coding style throughout
- ✅ Type safety with Decimal instead of float
- ✅ Proper exception handling

## Previously Known Issues - NOW FIXED ✅

1. ✅ **LineaPedido Model**: Added missing `precio` field (DecimalField)
2. ✅ **Cart Price Calculation**: Now uses Decimal throughout, no more float conversions
3. ✅ **Context Processor**: Returns Decimal('0') for all cases, no more string values
4. ✅ **Auto-now fields**: Fixed update fields to use `auto_now=True` instead of `auto_now_add=True`
5. ✅ **Security**: All credentials moved to environment variables

## Migration Notes

After pulling these changes, developers should:

```bash
# 1. Install new dependencies
pip install -r requirements-dev.txt

# 2. Create .env file from example
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# 3. Edit .env with proper values (especially SECRET_KEY and email)

# 4. Create and apply migrations for model changes
python manage.py makemigrations
python manage.py migrate

# 5. Run server and verify
python manage.py runserver
```

**Important:** Existing LineaPedido records may need data migration to populate the new precio field.
