import qrcode
import base64
from io import BytesIO

def generate_qr_code(data):
    img = qrcode.make(data)
        
    # Create a byte stream to hold the image data
    stream = BytesIO()
    img.save(stream, "PNG")
    stream.seek(0)
    
    # Convert the byte stream to a base64-encoded string
    qr_code_data = base64.b64encode(stream.getvalue()).decode()

    return qr_code_data
