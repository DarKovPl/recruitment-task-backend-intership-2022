import requests


class ApiRequests:

    def __init__(self):
        super(ApiRequests, self).__init__()
        self.req_get = requests.get

    def get_all_teams(self) -> requests.Response:
        response = self.req_get('https://www.balldontlie.io/api/v1/teams')
        return response

    def get_meta_players_stats_total_pages(self) -> int:
        response = self.req_get('https://www.balldontlie.io/api/v1/players?page=0&per_page=100')
        total_pages = response.json()['meta']['total_pages']
        return total_pages

    def get_player_stats(self) -> str:
        for k in range(1, self.get_meta_players_stats_total_pages() + 1):
            response = self.req_get(f'https://www.balldontlie.io/api/v1/players?page={k}&per_page=100')
            yield response.content.decode('utf-8')
