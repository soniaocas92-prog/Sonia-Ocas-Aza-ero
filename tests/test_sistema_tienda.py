"""Pruebas de la Semana 07: composición Venta - DetalleVenta.

Ejecutar en PowerShell:
    python -m unittest test_sistema_tienda.py -v
"""
import sys
import unittest
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from sistema_tienda import (
    Usuario, Cliente, Producto, Venta, DetalleVenta, Comprobante,
)


class TestSistemaTienda(unittest.TestCase):
    def setUp(self):
        self.usuario = Usuario(1, "Sonia Ocas", "sonia", "1234", "Vendedor")
        self.cliente = Cliente(1, "Ana", "Pérez", "12345678", "999888777")
        self.p001 = Producto(1, "Polo", "Blusas", "M", "Negro", "50.00", 10)
        self.p002 = Producto(2, "Falda", "Faldas", "S", "Azul", "30.00", 5)
        self.venta = Venta(1, self.usuario.id_usuario, self.cliente.id_cliente)
        self.venta.agregar_detalle(self.p001, 2)
        self.venta.agregar_detalle(self.p002, 1)

    def test_se_agregan_los_detalles(self):
        """La Venta contiene correctamente dos DetalleVenta (composición)."""
        self.assertEqual(len(self.venta.detalles), 2)
        self.assertIsInstance(self.venta.detalles[0], DetalleVenta)

    def test_total_es_130(self):
        """2 x 50.00 + 1 x 30.00 = 130.00, como Decimal."""
        self.assertEqual(self.venta.total, Decimal("130.00"))
        self.assertIsInstance(self.venta.total, Decimal)

    def test_verificacion_disponibilidad(self):
        """Se verifica el stock antes de vender."""
        self.assertTrue(self.p001.verificar_disponibilidad(8))   # quedan 8
        self.assertFalse(self.p001.verificar_disponibilidad(50))
        with self.assertRaises(ValueError):
            self.venta.agregar_detalle(self.p001, 999)

    def test_stock_actualizado(self):
        """El stock se descuenta al agregar cada detalle."""
        self.assertEqual(self.p001.stock, 8)   # 10 - 2
        self.assertEqual(self.p002.stock, 4)   # 5 - 1

    def test_comprobante(self):
        """El comprobante conserva el total de la venta."""
        comprobante = Comprobante(1, self.venta)
        self.assertEqual(comprobante.total, Decimal("130.00"))


if __name__ == "__main__":
    unittest.main()
