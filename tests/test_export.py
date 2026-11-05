"""Tests for fetch_all_users — Okta is faked, no network, no token."""
from unittest.mock import MagicMock, patch

import pytest
import requests

from export_users import fetch_all_users


def fake_response(users, next_url=None, status=200):
    """Build a fake requests.Response."""
    r = MagicMock()
    r.json.return_value = users
    r.links = {"next": {"url": next_url}} if next_url else {}
    if status >= 400:
        r.raise_for_status.side_effect = requests.HTTPError(f"{status} error")
    return r


def test_one_page():
    page = [{"id": "u1"}, {"id": "u2"}]
    with patch("export_users.requests.get", return_value=fake_response(page)) as mock_get:
        users = fetch_all_users("https://fake.okta.com/api/v1/users", {})
    assert users == page
    assert mock_get.call_count == 1

def test_two_pages():
    page1 = [{"id": "u1"}, {"id": "u2"}]
    page2 = [{"id": "u3"}]
    responses = [fake_response(page1, next_url="https://fake.okta.com/next"),
                 fake_response(page2)]
    with patch("export_users.requests.get", side_effect=responses) as mock_get:
        users = fetch_all_users("https://fake.okta.com/api/v1/users", {})
    assert users == page1 + page2
    assert mock_get.call_count == 2

def test_empty_org():
    with patch("export_users.requests.get", return_value=fake_response([])) as mock_get:
        users = fetch_all_users("https://fake.okta.com/api/v1/users", {})
    assert users == []
    assert mock_get.call_count == 1

def test_bad_token_raises():
    with patch("export_users.requests.get", return_value=fake_response([], status=401)):
        with pytest.raises(requests.HTTPError):
            fetch_all_users("https://fake.okta.com/api/v1/users", {})

