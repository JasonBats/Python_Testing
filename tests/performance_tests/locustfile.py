import random
import time

from locust import HttpUser, task


class RoutesPerformancesTest(HttpUser):

    @task(2)
    def index(self):
        time.sleep(random.uniform(0, 5))
        self.client.get("/")

    @task(1)
    def display_club_points(self):
        time.sleep(random.uniform(0, 5))
        self.client.get("/display_club_points")

    @task(3)
    def show_summary(self):
        time.sleep(random.uniform(0, 5))
        self.client.post(
            "/show_summary",
            data={"email": "john@simplylift.co"}
        )

    @task(1)
    def book(self):
        time.sleep(random.uniform(0, 5))
        self.client.get("/book/Spring%20Festival/Simply%20Lift")

    @task(2)
    def purchase_places(self):
        time.sleep(random.uniform(0, 5))
        self.client.post(
            "/purchase_places",
            data={
                "club": "Simply Lift",
                "competition": "Spring Festival",
                "places": "1"
            }
        )

# Goes with 100 users, 10 users/second
