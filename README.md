# DummyJSON Product Scraper

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Tests](https://img.shields.io/badge/tests-27%20passing-brightgreen.svg)

Un scraper de productos que extrae datos de la API pública [dummyjson.com](https://dummyjson.com/) para análisis, visualización y exportación a CSV.

## 📋 Descripción

Este proyecto permite extraer datos de productos de diversas categorías desde una API pública, procesar la información (calcular precios con descuentos), generar análisis estadísticos, visualizar tendencias, comparar precios en el tiempo y exportar los resultados a archivos CSV.

## 🚀 Características

- ✅ Búsqueda de productos por categoría o todos los productos
- ✅ Cálculo automático de precios con descuentos aplicados
- ✅ Análisis estadístico completo (precios, ratings, stock)
- ✅ Top 5 productos más baratos y mejor valorados
- ✅ Exportación a CSV con formato estructurado
- ✅ Historial de precios y comparación entre fechas (`--comparar`)
- ✅ Gráficos de tendencias de precios en el tiempo (`--tendencias`)
- ✅ Distribución de precios y scatter precio vs rating (gráficos PNG)
- ✅ Manejo robusto de errores (conexión, categorías inválidas)
- ✅ Lista de categorías disponibles

## 📦 Requisitos

- Python 3.7 o superior
- Bibliotecas: `requests`, `matplotlib`

## 🛠️ Instalación

1. Clona este repositorio:
```bash
git clone https://github.com/pierotticastillo/dummyjson-product-scraper.git
cd dummyjson-product-scraper
```

2. Crea y activa un entorno virtual (recomendado):
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Instala las dependencias desde `requirements.txt`:
```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

> Si tu sistema usa Python gestionado por el paquete del sistema (`externally-managed-environment`), no instales paquetes globalmente con `pip install` fuera de un entorno virtual.

## 📖 Uso

### Comandos básicos

```bash
# Buscar smartphones (20 productos por defecto)
python3 scraper.py smartphones

# Buscar laptops con cantidad personalizada
python3 scraper.py laptops --cantidad 10

# Buscar todos los productos
python3 scraper.py

# Listar categorías disponibles
python3 scraper.py --categorias
```

### Ejemplos avanzados

```bash
# Obtener 50 smartphones
python3 scraper.py smartphones --cantidad 50

# Obtener 100 productos de todas las categorías
python3 scraper.py all --cantidad 100

# Comparar precios actuales vs historial guardado
python3 scraper.py smartphones --comparar

# Generar gráfico de tendencias de precios
python3 scraper.py smartphones --tendencias

# Combinar flags
python3 scraper.py laptops --comparar --tendencias --cantidad 30

# Activar logs de depuración
python3 scraper.py smartphones -v
```

### Demo rápido

```bash
# Generar datos de historial simulados y probar comparación
python3 demo_price_comparison.py
python3 scraper.py smartphones --comparar

# O usar datos reales de la API con precios simulados
python3 demo_price_comparison_real.py
python3 scraper.py smartphones --tendencias
```

## 📊 Salida

El script genera:

1. **Resumen estadístico en consola**:
   - Productos analizados
   - Precios (mínimo, máximo, promedio)
   - Rating promedio
   - Stock total
   - Top 5 productos más baratos
   - Top 5 productos mejor valorados

2. **Archivo CSV**:
   - Nombre: `productos_{categoria}_{YYYY-MM-DD}.csv`
   - Campos: título, marca, categoría, precios, descuentos, rating, stock, descripción, fecha

3. **Gráficos PNG** (si `matplotlib` está instalado):
   - Histograma de distribución de precios
   - Scatter precio vs rating
   - Líneas de tendencia de precios en el tiempo (con `--tendencias`)

4. **Historial de precios** (en `price_history/price_history.json`):
   - Almacena precios actuales para comparaciones futuras
   - Se usa con el flag `--comparar`

## 🎯 Ejemplo de salida CSV

El archivo CSV ahora usa punto y coma (`;`) como separador para mejor visualización en editores de texto y programas como Excel/LibreOffice.

Formato:
```
titulo;marca;categoria;precio_usd;descuento_pct;precio_final_usd;rating;stock;descripcion;fecha_busqueda
iPhone 13 Pro;Apple;smartphones;1099.99;9.37;996.92;4.12;56;"The iPhone 13 Pro is a cutting-edge...";2026-05-18 21:10
```

| titulo          | marca   | categoria  | precio_usd | descuento_pct | precio_final_usd | rating | stock | descripcion                          | fecha_busqueda       |
|-----------------|---------|------------|------------|---------------|------------------|--------|-------|--------------------------------------|---------------------|
| iPhone 13 Pro   | Apple   | smartphones| 1099.99    | 9.37          | 996.92           | 4.12   | 56    | The iPhone 13 Pro is a cutting-edge...| 2026-05-18 20:52    |

## 🔧 Estructura del proyecto

```
dummyjson-product-scraper/
├── scraper.py              # Entry point (thin wrapper)
├── src/
│   ├── __init__.py
│   ├── config.py           # Constantes de configuración
│   ├── models.py           # Dataclass Product
│   ├── api.py              # Cliente API dummyjson.com
│   ├── history.py          # Historial y comparación de precios
│   ├── analysis.py         # Estadísticas y resúmenes
│   ├── export.py           # Exportación a CSV
│   ├── visualization.py    # Gráficos con matplotlib
│   └── cli.py              # Interfaz de línea de comandos
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_api.py
│   ├── test_history.py
│   ├── test_analysis.py
│   └── test_export.py
├── demo_price_comparison.py      # Demo con datos simulados
├── demo_price_comparison_real.py # Demo con productos reales de la API
├── README.md
├── requirements.txt
├── .gitignore
├── price_history/                # Historial de precios (generado)
│   └── price_history.json
└── productos_*.csv               # Archivos CSV generados
```

## 📝 Campos del producto

| Campo               | Descripción                                  | Tipo      |
|---------------------|----------------------------------------------|-----------|
| titulo              | Nombre del producto                          | string    |
| marca               | Marca del producto                           | string    |
| categoria           | Categoría del producto                       | string    |
| precio_usd          | Precio original en USD                       | float     |
| descuento_pct       | Porcentaje de descuento                      | float     |
| precio_final_usd    | Precio final con descuento aplicado          | float     |
| rating              | Calificación (0-5)                           | float     |
| stock               | Unidades disponibles                         | integer   |
| descripcion         | Descripción truncada (80 caracteres)          | string    |
| fecha_busqueda      | Fecha y hora de la búsqueda                  | datetime  |

## 🧪 Tests

El proyecto incluye **27 tests unitarios** con pytest:

```bash
# Activar el entorno virtual e instalar dependencias
source .venv/bin/activate
pip install -r requirements.txt

# Ejecutar todos los tests
python3 -m pytest tests/ -v

# Ejecutar tests con cobertura
python3 -m pip install pytest-cov
python3 -m pytest tests/ --cov=src
```

Los tests cubren:
- **models**: creación de `Product` desde API, cálculo de precios con descuento
- **api**: mocking de requests HTTP, manejo de errores (conexión, 404, 500)
- **analysis**: estadísticas descriptivas, top productos
- **history**: comparación de precios entre fechas, productos nuevos/ausentes
- **export**: generación de archivos CSV con contenido correcto

## 🤝 Contribución

Las contribuciones son bienvenidas. Por favor abre un issue o envía un pull request.

## 📜 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

## 🎓 Créditos

- API: [dummyjson.com](https://dummyjson.com/)
- Desarrollado por: [Enrique Alejandro Pierotti Castillo]