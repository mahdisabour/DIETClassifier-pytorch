from locust import HttpUser, task, between, tag


class RasaUser(HttpUser):
    @task
    def rasa_test(self):
        input_text = "this is test"
        self.client.post(
            f"/detect?input={input_text}",
        )

if __name__ == "__main__":
    import os
    os.system("locust -f locustfile.py")
