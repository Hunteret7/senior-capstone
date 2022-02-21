import requests


port = 5440


class Poster:
    @staticmethod
    def post_data(endpoint, data):
        url = "http://localhost:{}/{}".format(port, endpoint)
        response = requests.post(url, data=data)
        return response
