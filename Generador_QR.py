from supabase import create_client
import qrcode
from reportlab.pdfgen import canvas
from io import BytesIO
from PIL import Image

url = "#"  # Aqui iria la conexion correspondiente
key = "#"

supabase = create_client(url, key)

response = supabase.table("Productos").select("id, nombre, precio").execute()
productos = response.data

# Crear PDF con los códigos QR
pdf = "codigos_qr.pdf"
c = canvas.Canvas(pdf)

y_position = 700  # Posición inicial en el PDF
for producto in productos:
    qr_data = f"https://tu-sitio.com/producto/{producto['id']}"
    qr = qrcode.make(qr_data)
    
    img_bytes = BytesIO()
    qr.save(img_bytes, format="PNG")  # Guardar como PNG
    img_bytes.seek(0)
    
    img = Image.open(img_bytes)
    
    # Dibujar QR en PDF
    c.drawInlineImage(img, 100, y_position, width=150, height=150)
    
    # Agregar texto debajo del QR
    c.setFont("Helvetica", 12)
    c.drawString(120, y_position - 10, f"ID: {producto['id']}")
    c.drawString(120, y_position - 25, f"Nombre: {producto['nombre']}")
    c.drawString(120, y_position - 40, f"Precio: ${producto['precio']}")
    
    y_position -= 200  # Espacio entre QR
    if y_position < 100:
        c.showPage()
        y_position = 700  

c.save()
print(f"PDF '{pdf}' generado con éxito.")
