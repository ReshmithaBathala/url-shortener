import pytest
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'URL Shortener API'


def test_shorten_valid_url(client):
    res = client.post('/api/shorten', json={"url": "https://example.com/test"})
    assert res.status_code == 201
    data = res.get_json()
    assert "short_code" in data
    assert "short_url" in data

def test_shorten_invalid_url(client):
    res = client.post('/api/shorten', json={"url": "not-a-valid-url"})
    assert res.status_code == 400
    assert "error" in res.get_json()

def test_redirect_and_stats(client):
    # Step 1: Shorten a valid URL
    res = client.post('/api/shorten', json={"url": "https://example.com/path"})
    data = res.get_json()
    code = data["short_code"]

    # Step 2: Hit redirect
    redirect = client.get(f'/{code}')
    assert redirect.status_code == 302  # Redirect

    # Step 3: Get stats
    stats = client.get(f'/api/stats/{code}')
    assert stats.status_code == 200
    stat_data = stats.get_json()
    assert stat_data["clicks"] == 1
    assert stat_data["url"] == "https://example.com/path"
    assert "created_at" in stat_data

def test_stats_invalid_code(client):
    res = client.get('/api/stats/fake123')
    assert res.status_code == 404
    assert "error" in res.get_json()