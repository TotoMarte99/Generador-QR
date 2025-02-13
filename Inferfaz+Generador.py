import os
import qrcode
from PIL import Image, ImageDraw, ImageFont
import tkinter as tk
from tkinter import filedialog, messagebox
from reportlab.pdfgen import canvas
from io import BytesIO
from supabase import create_client, Client


url = "https://ryufhfohuqnvqfvgiliz.supabase.co"  
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ5dWZoZm9odXFudnFmdmdpbGl6Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczODc0ODYxMCwiZXhwIjoyMDU0MzI0NjEwfQ.k6ofELpB51HX4a09JMyhhcwDc-5v9lf-XXfwyESpqp0"  # Cambia esto por tu clave anónima o de servicio

supabase: Client = create_client(url, key)

def generar_qr(texto, nombre_archivo):
    qr = qrcode.make(texto)
    img = qr.convert("RGB")
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), nombre_archivo, font=font)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    img_width, img_height = img.size
    new_img = Image.new("RGB", (img_width, img_height + 20), "white")
    new_img.paste(img, (0, 0))
    draw = ImageDraw.Draw(new_img)
    draw.text(((img_width - text_width) // 2, img_height + 5), nombre_archivo, fill="black", font=font)
    
    return new_img

#Funcion para el boton de generacion
def generar_pdf():
    carpeta = filedialog.askdirectory()
    if not carpeta:
        messagebox.showerror("Error", "No se seleccionó una carpeta")
        return
    
    response = supabase.table("Productos").select("id, nombre, precio").execute()
    productos = response.data
    
    pdf_filename = os.path.join(carpeta, "codigos_qr.pdf")
    c = canvas.Canvas(pdf_filename)
    x_positions = [50, 300]
    y_position = 750
    column = 0
    
    #En este for se va a navegar por cada producto de la lista productos, donde por cada producto se va a generar un qr con la url definida
    for producto in productos:
        qr_text = f"https://tu-sitio.com/producto/{producto['id']}"
        nombre_archivo = f"{producto['id']}_{producto['nombre']}.png"
        img = generar_qr(qr_text, producto['nombre'])
        img_path = os.path.join(carpeta, nombre_archivo)
        img.save(img_path)
        
        # Dibujar en el PDF
        img_bytes = BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        c.drawImage(img_path, x_positions[column], y_position, width=150, height=150)
        
        # Alternar entre columnas
        column = 1 - column
        if column == 0:
            y_position -= 200
        
        if y_position < 100:
            c.showPage()
            y_position = 750
    
    c.save()
    messagebox.showinfo("Éxito", f"PDF generado en: {pdf_filename}")

def iniciar_app():
    root = tk.Tk()
    root.title("Generador de Códigos QR")
    root.geometry("300x200")
    btn_generar = tk.Button(root, text="Generar QR y PDF", command=generar_pdf, height=2, width=20)
    btn_generar.pack(pady=50)
    root.mainloop()

if __name__ == "__main__":
    iniciar_app()
