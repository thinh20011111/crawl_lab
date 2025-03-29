from .BaseApi import BaseApi
import logging

class Music_Api(BaseApi):

    def __init__(self):
        super().__init__()
        
    def get_id_music(self, token, expected_status):
        headers = {
            "Authorization": "Bearer " + token
        }
        self.set_headers(headers)
        response = self.get("/musics")
        self.compare_response_status(response, expected_status)
        try:
            response_data = response.json()  # Decode and parse JSON
            return response_data
        except ValueError as e:
            logging.error(f"Failed to decode JSON: {e}")
            return None