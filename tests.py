import json
import os
from fastapi.testclient import TestClient
from main import app


class TestApp:

    def setup_class(self):
        self.client = TestClient(app)

        with open("app.log") as f:
            self.original_log = f.read()

        with open("cats.json", "r") as f:
            self.original_file = f.read()

        with open("cats.json", "w") as f:
            json.dump([{
                "id": 1,
                "name": "Fluffy",
                "breed": "Persian",
                "age": 2,
                "image": None
            }], f)

        self.original_images = [images for images in os.listdir("images")]

    def teardown_class(self):
        with open("cats.json", "w") as f:
            f.write(self.original_file)

        with open("app.log", "w") as f:
            f.write(self.original_log)

        for image in os.listdir("images"):
            if image not in self.original_images:
                os.remove(f"images/{image}")

    def test_get_cats(self):
        response = self.client.get("/cats")
        assert response.status_code == 200
        assert response.json()[0]["name"] == "Fluffy"
        assert isinstance(response.json(), list)

    def test_create_cat(self):
        response = self.client.post(
            url="/cats",
            json={
                "name": "Egycica",
                "breed": "Perzsa",
                "age": 444,
            }
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Egycica"
        assert response.json()["age"] == 444
        assert response.json()["breed"] == "Perzsa"

    def test_update_cat(self):
        cat_data = {"name": "Fluffy", "breed": "Persian", "age": 2}
        response = self.client.post("/cats", json=cat_data)
        cat_id = response.json()["id"]
        updated_data = {"name": "Whiskers", "breed": "Siamese", "age": 3}
        response = self.client.put(f"/cats/{cat_id}", json=updated_data)
        assert response.status_code == 200
        assert response.json()["name"] == updated_data["name"]
        assert response.json()["breed"] == updated_data["breed"]
        assert response.json()["age"] == updated_data["age"]

    def test_upload_cat_image(self):
        cat_data = {"name": "Fluffy", "breed": "Persian", "age": 2}
        response = self.client.post("/cats", json=cat_data)
        cat_id = response.json()["id"]
        with open("images/test_image.jpg", "rb") as f:
            response = self.client.post(f"/cats/{cat_id}/image", files={"image": f.read()})
        assert response.status_code == 200
        assert response.json()["message"] == "Image uploaded successfully."

    def test_delete_cat(self):
        cat_data = {"name": "Fluffy", "breed": "Persian", "age": 2}
        response = self.client.post("/cats", json=cat_data)
        cat_id = response.json()["id"]
        response = self.client.delete(f"/cats/{cat_id}")
        assert response.status_code == 200
        assert response.json()["message"] == "Cat deleted successfully."
