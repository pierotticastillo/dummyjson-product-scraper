# DummyJSON Product Scraper

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Un scraper de productos que extrae datos de la API pública [dummyjson.com](https://dummyjson.com/) para análisis y exportación a CSV.

## 📋 Descripción

Este script permite extraer datos de productos de diversas categorías desde una API pública, procesar la información (calcular precios con descuentos), generar análisis estadísticos y exportar los resultados a archivos CSV.

## 🚀 Características

- ✅ Búsqueda de productos por categoría o todos los productos
- ✅ Cálculo automático de precios con descuentos aplicados
- ✅ Análisis estadístico completo (precios, ratings, stock)
- ✅ Exportación a CSV con formato estructurado
- ✅ Manejo robusto de errores (conexión, categorías inválidas)
- ✅ Lista de categorías disponibles
- ✅ Top 5 productos más baratos y mejor valorados

## 📦 Requisitos

- Python 3.7 o superior
- Biblioteca `requests` (se instala automáticamente si no está presente)

## 🛠️ Instalación

1. Clona este repositorio:
```bash
git clone https://github.com/pierotticastillo/dummyjson-product-scraper.git
cd dummyjson-product-scraper
```

2. Instala las dependencias:
```bash
pip install requests
```

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
├── scraper.py          # Script principal
├── README.md           # Este archivo
└── productos_*.csv     # Archivos CSV generados
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

## 🤝 Contribución

Las contribuciones son bienvenidas. Por favor abre un issue o envía un pull request.

## 📜 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

## 🎓 Créditos

- API: [dummyjson.com](https://dummyjson.com/)
- Desarrollado por: [Enrique Alejandro Pierotti Castillo]