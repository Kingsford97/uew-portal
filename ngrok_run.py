from pyngrok import ngrok
import os
import subprocess

# Set your authtoken
ngrok.set_auth_token("cr_3F0y6iqibu1UPjcQMeSJ0wVNdUd")

# Create a tunnel
public_url = ngrok.connect(8000)
print(f"Public URL: {public_url}")

# Run Django server
subprocess.call(["python", "manage.py", "runserver", "127.0.0.1:8000"])