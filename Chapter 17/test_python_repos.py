import pytest

from hn_submissions import get_python_repos

def test_python_repos():
    
    response = get_repos_info()

    assert response.status_code == 200
    
def test_items_returned():
    
    
    
def test_total_repositories():
    
    assert  total_repositories =< 500