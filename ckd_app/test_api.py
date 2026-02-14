from fastapi.testclient import TestClient
from app.main import app
import sys
import os

# Add project root to sys.path
sys.path.append(os.getcwd())

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert "Prédiction de la Maladie Rénale Chronique" in response.text

def test_predict_endpoint():
    # Test case 1: Normal values
    payload = {
        "age": 45,
        "sexe": "M",
        "creatinine": 10.5,
        "uree": 0.30,
        "temperature": 37.0,
        "cholesterol_ldl": "Normal",
        "cholesterol_total": "Normal"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "stage" in data
    assert "probabilities" in data
    print(f"Prediction for normal values: Stage {data['stage']}")

    # Test case 2: Abnormal values (high creatinine)
    payload_high = {
        "age": 65,
        "sexe": "F",
        "creatinine": 45.0,
        "uree": 0.80,
        "temperature": 38.5,
        "cholesterol_ldl": "Augmenté",
        "cholesterol_total": "Augmenté"
    }
    response = client.post("/predict", json=payload_high)
    assert response.status_code == 200
    data = response.json()
    print(f"Prediction for high values: Stage {data['stage']}")

if __name__ == "__main__":
    try:
        test_read_main()
        test_predict_endpoint()
        print("All tests passed!")
    except AssertionError as e:
        print(f"Test failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
