import requests


class MozioClient:
    def __init__(self, url, token):
        self._url = url
        self._token = token

    def _request(self, method, endpoint, headers={}, data=None):
        headers["API-KEY"] = self._token
        url = self._url + endpoint
        return requests.request(method, url, headers=headers, data=data)

    def create_search(self, parameters):
        return self._request("POST", "/v2/search/", data=parameters)

    def poll_search(self, search_id):
        return self._request("GET", "/v2/search/" + search_id + "/poll/")

    def create_reservation(self, parameters):
        return self._request("POST", "/v2/reservations/", data=parameters)

    def poll_reservation(self, search_id):
        return self._request("GET", "/v2/reservations/" + search_id + "/poll/")

    def cancel_reservation(self, reservation_id):
        return self._request("DELETE", "/v2/reservations/" + reservation_id + "/")
