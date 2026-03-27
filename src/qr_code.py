import subprocess
import re
import qrcode
import time

# Start cloudflared in a subprocess and get public URL
process = subprocess.Popen(
    ["cloudflared", "tunnel", "--url", "http://0.0.0.0:8501", "--no-autoupdate"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    universal_newlines=True,
)

# Wait and read lines to extract the URL
public_url = None
for line in process.stdout:
    if "trycloudflare.com" in line:
        match = re.search(r"https://.*?\.trycloudflare.com", line)
        if match:
            public_url = match.group(0)
            print(f"Public URL: {public_url}")

            # Save to file for Streamlit app
            with open("public_url.txt", "w") as f:
                f.write(public_url)

            # Generate QR code
            img = qrcode.make(public_url)
            img.save("qr.png")
            print("QR code saved as qr.png")
            break