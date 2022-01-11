from VidSpace import app


def test_home_route():
    client = app.test_client()
    url = '/'

    response = client.get(url)
    assert response.status_code == 200


def test_watch_route():
    client = app.test_client()
    url = '/watch?v=bpP6Iiymqk1'

    response = client.get(url)
    assert response.status_code == 200


"""Redirect us to signin"""
def test_studio_route():
    client = app.test_client()
    url = '/studio'

    response = client.get(url)
    assert response.status_code == 302


"""Redirect us to signin"""
def test_upload_route():
    client = app.test_client()
    url = '/upload'

    response = client.get(url)
    assert response.status_code == 302


"""Redirect us to signin"""
def test_subscribe_route():
    client = app.test_client()
    url = '/subscribe'

    response = client.get(url)
    assert response.status_code == 302

"""Redirect us to signin"""
def test_library_route():
    client = app.test_client()
    url = '/library'

    response = client.get(url)
    assert response.status_code == 302

