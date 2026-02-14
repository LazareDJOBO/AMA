import uvicorn
import os
import sys

# Ensure the current directory is in the python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("Démarrage de l'application CKD Prediction...")
    print("Ouvrez votre navigateur à l'adresse : http://127.0.0.1:8000")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
