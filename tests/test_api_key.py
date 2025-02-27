import httpx
from dotenv import load_dotenv
import os

load_dotenv()


def test_check_api_key_validity():
    resp = httpx.get('https://api.themoviedb.org/3/movie/top_rated',
                     headers={'Authorization': f'Bearer {os.getenv("API_ACCESS_TOKEN")}'})

    assert 200 == resp.status_code
