import pytest

from app import models


@pytest.fixture
def test_vote(db_session, test_user, create_dummy_posts):
    new_vote = models.Vote(post_id=create_dummy_posts[3].id, user_id=test_user["id"])
    db_session.add(new_vote)
    db_session.commit()


def test_vote_on_post(authorized_client, create_dummy_posts):
    response = authorized_client.post("/vote/",
                                      json={"post_id": create_dummy_posts[3].id, "dir": 1})
    assert response.status_code == 201


def test_vote_twice_post(authorized_client, create_dummy_posts, test_vote):
    response = authorized_client.post("/vote/",
                                      json={"post_id": create_dummy_posts[3].id, "dir": 1})
    assert response.status_code == 409


def test_delete_vote(authorized_client, create_dummy_posts, test_vote):
    response = authorized_client.post("/vote/",
                                      json={"post_id": create_dummy_posts[3].id, "dir": 0})
    assert response.status_code == 201


def test_delete_vote_non_exist(authorized_client, create_dummy_posts):
    response = authorized_client.post("/vote/",
                                      json={"post_id": create_dummy_posts[3].id, "dir": 0})
    assert response.status_code == 404


def test_vote_post_non_exist(authorized_client, create_dummy_posts):
    response = authorized_client.post("/vote/",
                                      json={"post_id": 10, "dir": 1})
    assert response.status_code == 404


def test_vote_unauthorized_user(client, create_dummy_posts):
    response = client.post("/vote/",
                           json={"post_id": create_dummy_posts[0].id, "dir": 1})
    assert response.status_code == 401
