from locust import HttpUser, task, between

class DRFUser(HttpUser):
    wait_time = between(1, 2)  # seconds

    @task
    def list_blogs(self):
        self.client.get("/api/blogs/")  # List all blogs

    # @task
    # def retrieve_blog(self):
    #     self.client.get("/api/blogs/1/")  # Get single blog (ID=1)
