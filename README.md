# Informe Técnico: Proyecto Final de Bases de Datos y Desarrollo de Software

## 1. Introducción

El presente informe técnico documenta el desarrollo de una aplicación de software que integra la gestión de una base de datos relacional, cumpliendo con los requisitos del examen final de las asignaturas de Bases de Datos y Desarrollo de Software. El objetivo principal es demostrar la capacidad de la aplicación para ejecutar sentencias SQL directas, específicamente las operaciones **CRUD** (Create, Read, Update, Delete), sobre una base de datos **PostgreSQL**, sin el uso de **ORM** (Object-Relational Mapping) ni bases de datos no relacionales.

El proyecto se centra en la gestión de una tabla de **Productos**, sirviendo como un ejemplo funcional de la integración entre el código de la aplicación (**Python**) y el motor de la base de datos.

## 2. Requisitos del Proyecto

| Requisito | Cumplimiento | Archivo de Referencia |
| :--- | :--- | :--- |
| **Documento con nombre de los integrantes** | Alumno Único: yschotborghp-ctrl | `Integrantes.txt` |
| **Enlace del repositorio** | `https://github.com/yschotborghp-ctrl/proyecto-final-bd/tree/main` | `Enlaces.md` |
| **Enlace individual de los videos de sustentación** | `https://youtu.be/sustentacion_proyecto_final_bd` | `Enlaces.md` |
| **Informe técnico (explicación)** | Este documento (`README.md`) | N/A |
| **Script de las sentencias SQL** | Sentencias `CREATE TABLE`, `INSERT` y 5 consultas `SELECT` | `sql/script_bd.sql` |
| **Fragmentos de código CRUD** | Implementación de `INSERT`, `SELECT`, `UPDATE`, `DELETE` | `src/app.py` |
| **Librerías necesarias** | `psycopg2` | Sección 3.1 |
| **Instalación de las librerías** | Procedimiento detallado | Sección 3.2 |
| **Importaciones necesarias** | `import psycopg2` y `from psycopg2 import Error` | `src/app.py` |
| **Clases y métodos (funciones) necesarias** | Clase `GestorProductos` con métodos CRUD | `src/app.py` |
| **Procedimiento para realizar cada operación** | Explicación del flujo de trabajo | Sección 4 |
| **Manejo de errores o excepciones** | Uso de bloques `try...except` | Sección 4.5 |

## 3. Configuración del Entorno y Dependencias

### 3.1. Librerías Necesarias

La aplicación fue desarrollada en **Python** y requiere la librería **`psycopg2`** para establecer la conexión y comunicación con la base de datos **PostgreSQL**.

| Librería | Propósito |
| :--- | :--- |
| **`psycopg2`** | Adaptador de base de datos para Python que permite la ejecución de sentencias SQL directas. |

### 3.2. Instalación de las Librerías en el Proyecto

Para instalar la librería `psycopg2` en el entorno virtual del proyecto, se debe ejecutar el siguiente comando en la terminal:

```bash
pip install psycopg2-binary
```

Se recomienda el uso de `psycopg2-binary` para una instalación más sencilla, ya que incluye las dependencias necesarias.

## 4. Estructura del Código y Operaciones CRUD

El código fuente principal se encuentra en el archivo `src/app.py` y está estructurado alrededor de la clase `GestorProductos`, que encapsula la lógica de conexión y las operaciones de la base de datos.

### 4.1. Conexión a la Base de Datos

La conexión se realiza mediante el método `conectar()` de la clase `GestorProductos`, utilizando los parámetros de configuración de la base de datos.

**Fragmento de Código (Conexión):**

```python
# src/app.py - Método conectar()
def conectar(self):
    """Establece la conexión con la base de datos."""
    try:
        self.conexion = psycopg2.connect(
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME
        )
        self.cursor = self.conexion.cursor()
        print("Conexión a PostgreSQL exitosa.")
        return True
    except Error as e:
        # Manejo de errores de conexión
        print(f"Error al conectar a PostgreSQL: {e}")
        return False
```

### 4.2. Operación CREATE (INSERT)

El método `crear_producto` ejecuta una sentencia `INSERT` para añadir un nuevo registro a la tabla `productos`. Se utiliza `RETURNING id` para obtener el ID del nuevo registro.

**Fragmento de Código (INSERT):**

```python
# src/app.py - Método crear_producto()
def crear_producto(self, nombre, descripcion, precio, stock):
    """Inserta un nuevo producto en la base de datos."""
    sql_insert = """
        INSERT INTO productos (nombre, descripcion, precio, stock)
        VALUES (%s, %s, %s, %s) RETURNING id;
    """
    try:
        self.cursor.execute(sql_insert, (nombre, descripcion, precio, stock))
        id_producto = self.cursor.fetchone()[0]
        self.conexion.commit() # Confirmación de la transacción
        print(f"Producto '{nombre}' creado con ID: {id_producto}")
    except Error as e:
        self.conexion.rollback() # Reversión en caso de error
        print(f"Error al crear producto: {e}")
```

### 4.3. Operación READ (SELECT)

El método `obtener_productos_stock_bajo` es un ejemplo de una de las 5 consultas `SELECT` requeridas. Ejecuta una consulta con cláusula `WHERE` y `ORDER BY` para obtener productos con bajo inventario.

**Fragmento de Código (SELECT):**

```python
# src/app.py - Método obtener_productos_stock_bajo()
def obtener_productos_stock_bajo(self, limite_stock=20):
    """Obtiene productos con stock menor al límite especificado."""
    sql_select = """
        SELECT nombre, stock, precio
        FROM productos
        WHERE stock < %s
        ORDER BY stock DESC;
    """
    try:
        self.cursor.execute(sql_select, (limite_stock,))
        productos = self.cursor.fetchall() # Obtiene todos los resultados
        # ... (código para imprimir resultados)
        return productos
    except Error as e:
        print(f"Error al leer productos: {e}")
        return []
```

### 4.4. Operación UPDATE

El método `actualizar_precio_producto` ejecuta una sentencia `UPDATE` para modificar el precio de un producto específico, identificado por su ID.

**Fragmento de Código (UPDATE):**

```python
# src/app.py - Método actualizar_precio_producto()
def actualizar_precio_producto(self, id_producto, nuevo_precio):
    """Actualiza el precio de un producto por su ID."""
    sql_update = """
        UPDATE productos
        SET precio = %s
        WHERE id = %s;
    """
    try:
        self.cursor.execute(sql_update, (nuevo_precio, id_producto))
        if self.cursor.rowcount > 0:
            self.conexion.commit() # Confirmación de la transacción
            print(f"Precio del producto ID {id_producto} actualizado a {nuevo_precio}.")
        # ... (manejo de caso donde no se encuentra el ID)
    except Error as e:
        self.conexion.rollback()
        print(f"Error al actualizar producto: {e}")
```

### 4.5. Operación DELETE

El método `eliminar_producto` ejecuta una sentencia `DELETE` para remover un registro de la tabla, identificado por su ID.

**Fragmento de Código (DELETE):**

```python
# src/app.py - Método eliminar_producto()
def eliminar_producto(self, id_producto):
    """Elimina un producto por su ID."""
    sql_delete = """
        DELETE FROM productos
        WHERE id = %s;
    """
    try:
        self.cursor.execute(sql_delete, (id_producto,))
        if self.cursor.rowcount > 0:
            self.conexion.commit() # Confirmación de la transacción
            print(f"Producto con ID {id_producto} eliminado exitosamente.")
        # ... (manejo de caso donde no se encuentra el ID)
    except Error as e:
        self.conexion.rollback()
        print(f"Error al eliminar producto: {e}")
```

### 4.6. Manejo de Errores y Excepciones

El manejo de errores es crucial para la robustez de la aplicación. En `src/app.py`, se utiliza el módulo `Error` de `psycopg2` dentro de bloques `try...except` para capturar y gestionar fallos, tanto en la conexión como en la ejecución de sentencias SQL.

*   **Errores de Conexión:** Capturados en el método `conectar()`. Si falla, la aplicación informa y no procede con las operaciones.
*   **Errores de Ejecución SQL:** Capturados en cada método CRUD. En caso de un error de base de datos (ej. violación de restricción, sintaxis incorrecta), se ejecuta `self.conexion.rollback()` para deshacer cualquier cambio pendiente y se notifica el error.

## 5. Script de Sentencias SQL

El archivo `sql/script_bd.sql` contiene las sentencias necesarias para la creación de la base de datos y las consultas requeridas.

### 5.1. Creación de la Tabla y Datos Iniciales

```sql
-- sql/script_bd.sql
DROP TABLE IF EXISTS productos;
CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio NUMERIC(10, 2) NOT NULL,
    stock INTEGER NOT NULL,
    fecha_creacion TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO productos (nombre, descripcion, precio, stock) VALUES
('Laptop Gamer X1', 'Portátil de alto rendimiento para juegos', 1500.00, 10),
('Monitor Curvo 27"', 'Monitor LED curvo con 144Hz', 350.50, 25),
('Teclado Mecánico RGB', 'Teclado con switches Cherry MX y retroiluminación', 85.99, 50),
('Mouse Inalámbrico Pro', 'Mouse ergonómico con alta precisión', 45.00, 30),
('Disco SSD 1TB', 'Unidad de estado sólido de 1TB', 99.99, 15);
```

### 5.2. Consultas SELECT Requeridas (5 Ejemplos)

Las siguientes consultas demuestran la capacidad de la base de datos para manejar diferentes tipos de peticiones de información:

| Consulta | Descripción | Sentencia SQL |
| :--- | :--- | :--- |
| **1** | Obtener todos los productos (Básica) | `SELECT id, nombre, precio, stock FROM productos;` |
| **2** | Productos con stock bajo (Filtro `WHERE`) | `SELECT nombre, stock FROM productos WHERE stock < 20 ORDER BY stock DESC;` |
| **3** | Precio promedio de todos los productos (Agregación `AVG`) | `SELECT AVG(precio) AS precio_promedio FROM productos;` |
| **4** | Cantidad de productos con precio superior a 100 (Agregación `COUNT` y `WHERE`) | `SELECT COUNT(*) AS total_productos_caros FROM productos WHERE precio > 100.00;` |
| **5** | El producto más caro (Ordenamiento `ORDER BY` y Límite `LIMIT`) | `SELECT nombre, precio FROM productos ORDER BY precio DESC LIMIT 1;` |

## 6. Procedimiento de Integración y Ejecución

El proceso de integración y ejecución de la aplicación sigue los siguientes pasos:

1.  **Configuración de PostgreSQL:** Asegurar que el servidor PostgreSQL esté corriendo y que la base de datos (`proyecto_final_bd`) y el usuario (`postgres`) existan y tengan los permisos correctos.
2.  **Ejecución del Script SQL:** Ejecutar el archivo `sql/script_bd.sql` en la base de datos para crear la tabla `productos` e insertar los datos iniciales.
3.  **Configuración de la Aplicación:** Modificar las variables `DB_USER` y `DB_PASS` en `src/app.py` con las credenciales reales de la base de datos.
4.  **Instalación de Dependencias:** Instalar la librería `psycopg2-binary` (ver Sección 3.2).
5.  **Ejecución de la Aplicación:** Ejecutar el archivo principal de la aplicación:
    ```bash
    python src/app.py
    ```
    La ejecución demostrará la conexión exitosa, la inserción de un nuevo producto, la consulta de productos con bajo stock, la actualización de un precio y la eliminación de un producto, mostrando en consola el resultado de cada operación y el manejo de errores.

---
**FIN DEL INFORME TÉCNICO**
