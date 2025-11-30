-- =================================================================
-- Script SQL para el Proyecto Final de Bases de Datos
-- SGBD: PostgreSQL
-- =================================================================

-- 1. Creación de la tabla de Productos
DROP TABLE IF EXISTS productos;
CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio NUMERIC(10, 2) NOT NULL,
    stock INTEGER NOT NULL,
    fecha_creacion TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Inserción de datos de prueba (para la operación CREATE/INSERT)
INSERT INTO productos (nombre, descripcion, precio, stock) VALUES
('Laptop Gamer X1', 'Portátil de alto rendimiento para juegos', 1500.00, 10),
('Monitor Curvo 27"', 'Monitor LED curvo con 144Hz', 350.50, 25),
('Teclado Mecánico RGB', 'Teclado con switches Cherry MX y retroiluminación', 85.99, 50),
('Mouse Inalámbrico Pro', 'Mouse ergonómico con alta precisión', 45.00, 30),
('Disco SSD 1TB', 'Unidad de estado sólido de 1TB', 99.99, 15);

-- 3. Consultas SELECT requeridas (al menos 5)

-- Consulta 1: SELECT simple - Obtener todos los productos
SELECT id, nombre, precio, stock FROM productos;

-- Consulta 2: SELECT con WHERE - Productos con stock bajo (menos de 20 unidades)
SELECT nombre, stock
FROM productos
WHERE stock < 20
ORDER BY stock DESC;

-- Consulta 3: SELECT con función de agregación (AVG) - Precio promedio de todos los productos
SELECT AVG(precio) AS precio_promedio
FROM productos;

-- Consulta 4: SELECT con función de agregación (COUNT) y WHERE - Cantidad de productos con precio superior a 100
SELECT COUNT(*) AS total_productos_caros
FROM productos
WHERE precio > 100.00;

-- Consulta 5: SELECT con ORDER BY y LIMIT - El producto más caro
SELECT nombre, precio
FROM productos
ORDER BY precio DESC
LIMIT 1;
