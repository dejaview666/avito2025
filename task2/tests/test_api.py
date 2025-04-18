import pytest
import requests
import random
import uuid

BASE_URL = "https://qa-internship.avito.com"


class TestAdServiceAPI:
    @pytest.fixture
    def test_ad(self):
        seller_id = random.randint(111111, 999999)
        ad_data = {
            "sellerID": seller_id,
            "name": "Тестовое объявление",
            "price": 1000,
            "statistics": {
                "likes": 10,
                "viewCount": 100,
                "contacts": 5
            }
        }

        response = requests.post(
            f"{BASE_URL}/api/1/item",
            json=ad_data,
            headers={"Accept": "application/json"}
        )
        assert response.status_code == 200
        return response.json()

    def test_create_ad_valid_data(self):
        seller_id = random.randint(111111, 999999)
        ad_data = {
            "sellerID": seller_id,
            "name": "Новый iPhone",
            "price": 99999,
            "statistics": {
                "likes": 0,
                "viewCount": 0,
                "contacts": 0
            }
        }

        response = requests.post(
            f"{BASE_URL}/api/1/item",
            json=ad_data,
            headers={"Accept": "application/json"}
        )

        assert response.status_code == 200
        response_data = response.json()
        assert "status" in response_data
        assert "Сохранили объявление" in response_data["status"]

    def test_get_ad_by_id(self, test_ad):
        status_message = test_ad["status"]
        ad_id = status_message.split(" - ")[-1]

        response = requests.get(
            f"{BASE_URL}/api/1/item/{ad_id}",
            headers={"Accept": "application/json"}
        )

        assert response.status_code == 200
        response_data = response.json()
        assert isinstance(response_data, list)
        assert len(response_data) > 0

    def test_get_nonexistent_ad(self):
        random_id = str(uuid.uuid4())
        response = requests.get(
            f"{BASE_URL}/api/1/item/{random_id}",
            headers={"Accept": "application/json"}
        )
        assert response.status_code == 404

    def test_get_ads_by_seller(self, test_ad):
        seller_id = test_ad.get("sellerId", 123456)
        response = requests.get(
            f"{BASE_URL}/api/1/{seller_id}/item",
            headers={"Accept": "application/json"}
        )

        assert response.status_code == 200
        ads = response.json()
        assert isinstance(ads, list)

    def test_get_ad_statistics(self, test_ad):
        status_message = test_ad["status"]
        ad_id = status_message.split(" - ")[-1]

        for endpoint in ["/api/1/statistic/", "/api/2/statistic/"]:
            response = requests.get(
                f"{BASE_URL}{endpoint}{ad_id}",
                headers={"Accept": "application/json"}
            )

            assert response.status_code == 200
            stats = response.json()
            assert isinstance(stats, list)
            if len(stats) > 0:
                assert "likes" in stats[0]
                assert "viewCount" in stats[0]
                assert "contacts" in stats[0]

    def test_delete_ad(self, test_ad):
        status_message = test_ad["status"]
        ad_id = status_message.split(" - ")[-1]

        response = requests.get(f"{BASE_URL}/api/1/item/{ad_id}")
        assert response.status_code == 200

        response = requests.delete(
            f"{BASE_URL}/api/2/item/{ad_id}",
            headers={"Accept": "application/json"}
        )
        assert response.status_code == 200

        response = requests.get(f"{BASE_URL}/api/1/item/{ad_id}")
        assert response.status_code == 404