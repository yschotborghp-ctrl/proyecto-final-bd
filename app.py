import psycopg2
from psycopg2 import Error

# =================================================================
# Configuración de la Conexión a la Base de Datos
# NOTA: Estos valores deben ser configurados por el usuario
# =================================================================
DB_HOST = "localhost"
DB_NAME = "proyecto_final_bd"
DB_USER = "postgres"
DB_PASS = "tu_contraseña_segura"
DB_PORT = "5432"

class GestorProductos:
    """
    Clase para gestionar las operaciones CRUD sobre la tabla 'productos'
    en la base de datos PostgreSQL.
    """
    def __init__(self):
        self.conexion = None
        self.cursor = None

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

    def desconectar(self):
        """Cierra la conexión con la base de datos."""
        if self.conexion:
            self.cursor.close()
            self.conexion.close()
            print("Conexión a PostgreSQL cerrada.")

    # =================================================================
    # Operación CREATE (INSERT)
    # =================================================================
    def crear_producto(self, nombre, descripcion, precio, stock):
        """Inserta un nuevo producto en la base de datos."""
        sql_insert = """
            INSERT INTO productos (nombre, descripcion, precio, stock)
            VALUES (%s, %s, %s, %s) RETURNING id;
        """
        try:
            self.cursor.execute(sql_insert, (nombre, descripcion, precio, stock))
            id_producto = self.cursor.fetchone()[0]
            self.conexion.commit()
            print(f"Producto '{nombre}' creado con ID: {id_producto}")
        except Error as e:
            # Manejo de errores de ejecución de sentencia SQL
            self.conexion.rollback()
            print(f"Error al crear producto: {e}")

    # =================================================================
    # Operación READ (SELECT) - Ejemplo de una de las 5 consultas
    # =================================================================
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
            productos = self.cursor.fetchall()
            print(f"\n--- Productos con stock menor a {limite_stock} ---")
            for prod in productos:
                print(f"Nombre: {prod[0]}, Stock: {prod[1]}, Precio: {prod[2]}")
            return productos
        except Error as e:
            print(f"Error al leer productos: {e}")
            return []

    # =================================================================
    # Operación UPDATE
    # =================================================================
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
                self.conexion.commit()
                print(f"Precio del producto ID {id_producto} actualizado a {nuevo_precio}.")
            else:
                print(f"No se encontró producto con ID {id_producto} para actualizar.")
        except Error as e:
            self.conexion.rollback()
            print(f"Error al actualizar producto: {e}")

    # =================================================================
    # Operación DELETE
    # =================================================================
    def eliminar_producto(self, id_producto):
        """Elimina un producto por su ID."""
        sql_delete = """
            DELETE FROM productos
            WHERE id = %s;
        """
        try:
            self.cursor.execute(sql_delete, (id_producto,))
            if self.cursor.rowcount > 0:
                self.conexion.commit()
                print(f"Producto con ID {id_producto} eliminado exitosamente.")
            else:
                print(f"No se encontró producto con ID {id_producto} para eliminar.")
        except Error as e:
            self.conexion.rollback()
            print(f"Error al eliminar producto: {e}")

# =================================================================
# Ejecución de la Aplicación
# =================================================================
if __name__ == "__main__":
    gestor = GestorProductos()

    if gestor.conectar():
        # Ejemplo de uso de las operaciones CRUD

        # 1. CREATE (Insertar un nuevo producto)
        gestor.crear_producto("Webcam HD", "Cámara web para videoconferencias", 35.00, 60)

        # 2. READ (Consultar productos con stock bajo)
        gestor.obtener_productos_stock_bajo(limite_stock=25)

        # 3. UPDATE (Actualizar el precio del producto ID 5 - Disco SSD 1TB)
        gestor.actualizar_precio_producto(id_producto=5, nuevo_precio=105.50)

        # 4. DELETE (Eliminar el producto ID 1 - Laptop Gamer X1)
        # NOTA: Se asume que el ID 1 existe de los datos iniciales del script SQL
        gestor.eliminar_producto(id_producto=1)

        # 5. Intentar una operación con un ID inexistente para mostrar el manejo de errores (implícito en el rowcount)
        gestor.eliminar_producto(id_producto=999)

        gestor.desconectar()
    else:
        print("La aplicación no pudo ejecutarse debido a un error de conexión a la base de datos.")
