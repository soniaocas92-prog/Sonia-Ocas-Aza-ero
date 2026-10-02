# Cambios propuestos al informe — Semana 07

*(Trabajar estos cambios sobre una copia del informe. El PDF original en `C:\proyecto` no se modifica.)*

## 1. Sección 8.2 — corregir la representación UML

**Texto original:**

> Representación UML: Venta unn Detalle de Venta

**Texto corregido:**

> Representación UML: `Venta ◆—— Detalle de Venta` (multiplicidad `1 — 1..*`).
> El rombo relleno `◆` se coloca en el extremo de **Venta**, porque Venta es el
> "todo" y cada Detalle de Venta es la "parte". En el código Python esto se
> refleja en que la clase `Venta` crea y administra su lista de objetos
> `DetalleVenta`.

## 2. Sección 8.4 — reemplazar el ejemplo de Python

Reemplazar el bloque de código por la versión ampliada y coherente con el modelo
UML (archivo `sistema_tienda.py` de esta carpeta). Cambios principales:

- Se incluyen las seis clases del modelo: `Usuario`, `Producto`, `Cliente`,
  `Venta`, `DetalleVenta` y `Comprobante`.
- `DetalleVenta` referencia un objeto `Producto` (no un string como `"P001"`).
- `Venta` conserva la **composición**: crea y administra sus `DetalleVenta`.
- Precios, subtotales y totales usan `Decimal` en lugar de enteros/floats.
- `Venta.agregar_detalle` **verifica el stock antes de vender** y
  **descuenta el stock** al confirmar el detalle.
- Se mantiene la salida del ejemplo: 2 detalles y total `130.00`.

## 3. Sección 8.5 — pruebas con `unittest`

**Original:** pruebas con `print` solamente.

**Nuevo (archivo `test_sistema_tienda.py`):**

| Prueba realizada | Resultado esperado | Resultado obtenido |
|---|---|---|
| Registrar dos detalles en una Venta | 2 detalles | 2 detalles ✅ |
| Calcular el total | Decimal("130.00") | Decimal("130.00") ✅ |
| Verificar disponibilidad | Stock suficiente / `ValueError` si no alcanza | Comprobado ✅ |
| Verificar relación todo-parte | Venta administra sus detalles | Comprobado ✅ |
| Stock actualizado | P001: 8, P002: 4 | 8 y 4 ✅ |

## 4. Tabla de correspondencia final — corregir inconsistencia

**Texto original:**

> Con esta sección, el informe integra la actividad de la Semana 07 sobre
> **herencia, abstracción e interfaces**...

**Texto corregido:**

> Con esta sección, el informe integra la actividad de la Semana 07 sobre
> **herencia, composición e interfaces**...

## 5. Elementos que NO se eliminan

- Se conservan las seis entidades, atributos, relaciones y multiplicidades
  validadas en las secciones 3 y 7.
- Se mantiene la justificación de descarte de herencia e interfaz (8.3 y 8.9).
- Se mantienen la bitácora de IA (8.7) y la verificación de consistencia (8.8).
- No se agregan nuevas clases ni relaciones al modelo.
