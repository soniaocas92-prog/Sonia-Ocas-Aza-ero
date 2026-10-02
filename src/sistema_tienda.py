"""Sistema de Gestión para una Tienda de Ropa - Semana 07

Alternativa de diseño seleccionada: COMPOSICIÓN.
  Venta  "tiene un"  DetalleVenta (multiplicidad 1 -- 1..*)
  Venta administra los objetos DetalleVenta y calcula el total de la venta.

Mantiene las seis clases del modelo UML validado:
Usuario, Producto, Cliente, Venta, DetalleVenta y Comprobante.
"""
from datetime import date
from decimal import Decimal


class Usuario:
    def __init__(self, id_usuario, nombre, usuario, contraseña, rol):
        self._id_usuario = id_usuario
        self._nombre = nombre
        self._usuario = usuario
        self._contraseña = contraseña
        self._rol = rol

    @property
    def id_usuario(self):
        return self._id_usuario

    @property
    def nombre(self):
        return self._nombre

    @property
    def rol(self):
        return self._rol

    def iniciar_sesion(self, usuario, contraseña):
        return usuario == self._usuario and contraseña == self._contraseña

    def controlar_acceso(self):
        return self._rol in ("Administrador", "Vendedor")


class Cliente:
    def __init__(self, id_cliente, nombres, apellidos, documento, teléfono):
        self._id_cliente = id_cliente
        self._nombres = nombres
        self._apellidos = apellidos
        self._documento = documento
        self._teléfono = teléfono

    @property
    def id_cliente(self):
        return self._id_cliente

    @property
    def nombres(self):
        return self._nombres

    def registrar_cliente(self):
        return f"Cliente {self._nombres} {self._apellidos} registrado."

    def consultar_cliente(self):
        return f"{self._nombres} {self._apellidos} - Doc: {self._documento}"


class Producto:
    def __init__(self, id_producto, nombre, categoría, talla, color, precio, stock):
        self._id_producto = id_producto
        self._nombre = nombre
        self._categoría = categoría
        self._talla = talla
        self._color = color
        self._precio = Decimal(str(precio))   # Decimal para importes
        self._stock = int(stock)

    @property
    def id_producto(self):
        return self._id_producto

    @property
    def nombre(self):
        return self._nombre

    @property
    def precio(self):
        return self._precio

    @property
    def stock(self):
        return self._stock

    def registrar_producto(self):
        return f"Producto {self._nombre} registrado."

    def modificar_producto(self, precio=None, stock=None):
        if precio is not None:
            self._precio = Decimal(str(precio))
        if stock is not None:
            self._stock = int(stock)

    def consultar_producto(self):
        return (f"{self._nombre} | {self._categoría} | Talla {self._talla} | "
                f"{self._color} | Precio {self._precio} | Stock {self._stock}")

    def verificar_disponibilidad(self, cantidad):
        """True si hay stock suficiente para la cantidad solicitada."""
        return self._stock >= cantidad

    def controlar_stock(self, cantidad):
        """Descuenta stock; devuelve False si no alcanza."""
        if cantidad > self._stock:
            return False
        self._stock -= cantidad
        return True


class DetalleVenta:
    def __init__(self, id_detalle, id_venta, producto, cantidad):
        self._id_detalle = id_detalle
        self._id_venta = id_venta
        self._id_producto = producto.id_producto
        self._producto = producto
        self._cantidad = int(cantidad)
        self._precio = producto.precio        # Decimal
        self._subtotal = self.calcular_subtotal()

    @property
    def id_detalle(self):
        return self._id_detalle

    @property
    def cantidad(self):
        return self._cantidad

    @property
    def precio(self):
        return self._precio

    @property
    def subtotal(self):
        return self._subtotal

    def registrar_detalle(self):
        return f"Detalle {self._id_detalle}: {self._cantidad} x {self._producto.nombre}"

    def calcular_subtotal(self):
        return self._precio * self._cantidad


class Venta:
    """La Venta COMPONE sus DetalleVenta: los crea, administra y calcula el total."""

    def __init__(self, id_venta, id_usuario, id_cliente):
        self._id_venta = id_venta
        self._fecha = date.today()
        self._id_usuario = id_usuario
        self._id_cliente = id_cliente
        self._detalles = []                   # composición: 1..* DetalleVenta
        self._total = Decimal("0.00")

    @property
    def id_venta(self):
        return self._id_venta

    @property
    def fecha(self):
        return self._fecha

    @property
    def detalles(self):
        return list(self._detalles)

    @property
    def total(self):
        return self._total

    def agregar_detalle(self, producto, cantidad):
        # Verificación de disponibilidad ANTES de vender
        if not producto.verificar_disponibilidad(cantidad):
            raise ValueError(f"Stock insuficiente para {producto.nombre} "
                             f"(stock={producto.stock}, solicitado={cantidad})")
        detalle = DetalleVenta(len(self._detalles) + 1, self._id_venta, producto, cantidad)
        self._detalles.append(detalle)
        producto.controlar_stock(cantidad)    # Actualización del stock
        self._total = self.calcular_total()
        return detalle

    def calcular_total(self):
        self._total = sum((d.subtotal for d in self._detalles), Decimal("0.00"))
        return self._total

    def registrar_venta(self):
        return f"Venta {self._id_venta} registrada el {self._fecha} por un total de {self._total}"

    def consultar_ventas(self):
        return f"Venta {self._id_venta}: {len(self._detalles)} detalle(s), total {self._total}"


class Comprobante:
    def __init__(self, id_comprobante, venta):
        self._id_comprobante = id_comprobante
        self._id_venta = venta.id_venta
        self._fecha = date.today()
        self._total = venta.total

    @property
    def id_comprobante(self):
        return self._id_comprobante

    @property
    def total(self):
        return self._total

    def generar_comprobante(self):
        return (f"COMPROBANTE N.º {self._id_comprobante} | Venta {self._id_venta} | "
                f"Fecha {self._fecha} | Total {self._total}")

    def conservar_comprobante(self):
        return f"Comprobante {self._id_comprobante} conservado."


if __name__ == "__main__":
    usuario = Usuario(1, "Sonia Ocas", "sonia", "1234", "Vendedor")
    cliente = Cliente(1, "Ana", "Pérez", "12345678", "999888777")
    p001 = Producto(1, "Polo", "Blusas", "M", "Negro", "50.00", 10)
    p002 = Producto(2, "Falda", "Faldas", "S", "Azul", "30.00", 5)

    venta = Venta(1, usuario.id_usuario, cliente.id_cliente)
    venta.agregar_detalle(p001, 2)
    venta.agregar_detalle(p002, 1)

    print("Cantidad de detalles:", len(venta.detalles))
    print("Total:", venta.total)
    print("Stock P001:", p001.stock, "| Stock P002:", p002.stock)
    print(Comprobante(1, venta).generar_comprobante())
