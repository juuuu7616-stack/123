"""苗栗美食探索站單元測試。"""
import unittest

from app import app


class MiaoliFoodAppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home_page(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("苗栗美食探索站", resp.get_data(as_text=True))
        self.assertIn("X-Content-Type-Options", resp.headers)

    def test_health_endpoint(self):
        resp = self.client.get("/api/health")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertTrue(data["ok"])
        self.assertGreater(data["count"], 0)

    def test_food_endpoint_default(self):
        resp = self.client.get("/api/food")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertTrue(data["ok"])
        self.assertIn("food", data)
        self.assertIn("name", data["food"])
        self.assertTrue(data["food"]["image_url"].startswith("https://"))

    def test_food_endpoint_filter_by_area(self):
        resp = self.client.get("/api/food?area=大湖")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertTrue(data["ok"])
        self.assertIn("大湖", data["food"]["area"])

    def test_food_endpoint_unknown_area(self):
        resp = self.client.get("/api/food?area=不存在的鄉鎮")
        self.assertEqual(resp.status_code, 404)
        data = resp.get_json()
        self.assertFalse(data["ok"])


if __name__ == "__main__":
    unittest.main()
