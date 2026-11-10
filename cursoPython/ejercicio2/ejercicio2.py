# =====================================================================
#  EJERCICIO 2 - Gestión de inventario con POO, validaciones y JSON
# =====================================================================
import json   # libreria estandar para convertir a formato JSON


# Excepción personalizada para controlar el stock inválido
class StockInvalidoError(Exception):
    pass


# ----------------------- Clase base -----------------------
class EquipoEnergetico:
    def __init__(self, codigo: str, nombre: str, precio: float, stock: int):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.__stock = 0                 # encapsulamiento explícito (privado)
        self.asignar_stock(stock)        # valida al asignar

    # setter con validación de stock negativo
    def asignar_stock(self, nuevo_stock):
        if nuevo_stock < 0:
            raise StockInvalidoError("El stock no puede ser negativo")
        self.__stock = nuevo_stock

    # getter del stock privado
    def obtener_stock(self):
        return self.__stock

    def mostrar_ficha_tecnica(self):
        return (f"Codigo: {self.codigo} | Nombre: {self.nombre} | "
                f"Precio: ${self.precio} | Stock: {self.obtener_stock()}")


# ----------------- Clase hija (herencia + polimorfismo) -----------------
class PanelFotovoltaico(EquipoEnergetico):
    def __init__(self, codigo, nombre, precio, stock, potencia_watts, eficiencia):
        super().__init__(codigo, nombre, precio, stock)   # constructor del padre
        self.potencia_watts = potencia_watts
        self.eficiencia = eficiencia

    # polimorfismo: redefine la ficha técnica agregando sus datos propios
    def mostrar_ficha_tecnica(self):
        ficha_base = super().mostrar_ficha_tecnica()
        return (f"{ficha_base} | Potencia: {self.potencia_watts} W | "
                f"Eficiencia: {self.eficiencia}%")


# ----------------- Administrador del catálogo (exporta a JSON) -----------------
class AdministradorCatalogo:
    def guardar_catalogo_json(self, lista_dispositivos, ruta_archivo):
        catalogo = []

        for dispositivo in lista_dispositivos:
            producto = {
                "codigo": dispositivo.codigo,
                "nombre": dispositivo.nombre,
                "precio": dispositivo.precio,
                "stock": dispositivo.obtener_stock()   # usamos el getter (stock es privado)
            }

            # Si es un panel, agregamos sus atributos extra
            if type(dispositivo) == PanelFotovoltaico:
                producto["potencia_watts"] = dispositivo.potencia_watts
                producto["eficiencia"] = dispositivo.eficiencia

            catalogo.append(producto)

        # Guardamos la lista de productos en un archivo JSON
        with open(ruta_archivo, "w", encoding="utf-8") as file:
            json.dump(catalogo, file, indent=4, ensure_ascii=False)

        print("Catalogo guardado correctamente.")


# ----------------------- Bloque principal -----------------------
panel1 = PanelFotovoltaico("PF-001", "Panel Solar Residencial", 250_000, 15, 450, 21.5)
panel2 = PanelFotovoltaico("PF-002", "Panel Solar Industrial", 420_000, 8, 600, 23.5)
equipo1 = EquipoEnergetico("EE-001", "Controlador de Carga", 85_000, 5)

# Caso que DEBE lanzar error: stock negativo al crear el objeto
try:
    panel_invalido = PanelFotovoltaico("PF-003", "Panel Solar Defectuoso", 400_000, -5, 850, 26.5)
except StockInvalidoError as error:
    print(f"Error controlado: {error}")

# Otro caso de error: reasignar un stock negativo
try:
    panel1.asignar_stock(-5)
except StockInvalidoError as error:
    print(f"Error controlado: {error}")

# Mostrar las fichas técnicas (se ve el polimorfismo)
productos = [panel1, panel2, equipo1]
for producto in productos:
    print(producto.mostrar_ficha_tecnica())

# Exportar el catálogo a un archivo JSON
admin_catalogo = AdministradorCatalogo()
admin_catalogo.guardar_catalogo_json(productos, "catalogo.json")
