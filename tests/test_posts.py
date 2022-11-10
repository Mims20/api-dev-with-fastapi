import pytest

from app import schemas


def test_get_all_posts(authorized_client, create_dummy_posts):
    response = authorized_client.get("/posts/")
    # print(response.json())
    assert len(response.json()) == len(create_dummy_posts)
    assert response.status_code == 200


def test_get_one_post(authorized_client, create_dummy_posts):
    response = authorized_client.get(f"/posts/{create_dummy_posts[0].id}")
    post = schemas.PostOut(**response.json())
    # print(post)
    assert int(post.Post.id) == create_dummy_posts[0].id
    assert post.Post.title == create_dummy_posts[0].title
    assert post.Post.content == create_dummy_posts[0].content


def test_get_one_post_not_exist(authorized_client, create_dummy_posts):
    response = authorized_client.get(f"/posts/{12}")
    assert response.status_code == 404


def test_unauthorized_user_get_all_posts(client, create_dummy_posts):
    response = client.get("/posts/")
    assert response.status_code == 401


def test_unauthorized_user_get_one_post(client, create_dummy_posts):
    response = client.get(f"/posts/{create_dummy_posts[0].id}")
    assert response.status_code == 401


@pytest.mark.parametrize("title, content, published", [
    ("new title", "new content", True),
    ("favorite football team", "fc barcelona", False),
    ("favorite player", "xavi", True),
])
def test_create_post(authorized_client, test_user, create_dummy_posts, title, content, published):
    response = authorized_client.post("/posts/",
                                      json={"title": title, "content": content, "published": published})
    created_post = schemas.PostResponse(**response.json())
    assert response.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user["id"]


def test_create_post_default_published_true(authorized_client, test_user, create_dummy_posts):
    response = authorized_client.post("/posts/",
                                      json={"title": "title", "content": "content"})
    created_post = schemas.PostResponse(**response.json())
    assert response.status_code == 201
    assert created_post.title == "title"
    assert created_post.content == "content"
    assert created_post.published == True
    assert created_post.owner_id == test_user["id"]


def test_unauthorized_user_create_post(client, test_user, create_dummy_posts):
    response = client.post("/posts/",
                           json={"title": "title", "content": "content"})
    assert response.status_code == 401


def test_unauthorized_user_delete_post(client, create_dummy_posts):
    response = client.delete(f"/posts/{create_dummy_posts[0].id}")
    assert response.status_code == 401


def test_delete_post_success(authorized_client, create_dummy_posts):
    response = authorized_client.delete(f"/posts/{create_dummy_posts[0].id}")
    assert response.status_code == 204


def test_delete_post_non_exit(authorized_client, create_dummy_posts):
    response = authorized_client.delete("/posts/10")
    assert response.status_code == 404


# try deleting the fourth post belonging to test_user2
def test_delete_other_user_post(authorized_client, test_user, create_dummy_posts):
    response = authorized_client.delete(f"/posts/{create_dummy_posts[3].id}")

    assert response.status_code == 403


def test_update_post(authorized_client, create_dummy_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": create_dummy_posts[0].id
    }
    response = authorized_client.put(f"/posts/{create_dummy_posts[0].id}",
                                     json=data)
    updated_post = schemas.PostResponse(**response.json())
    assert response.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]


def test_update_other_user_post(authorized_client, create_dummy_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": create_dummy_posts[3].id
    }
    response = authorized_client.put(f"/posts/{create_dummy_posts[3].id}",
                                     json=data)
    assert response.status_code == 403


def test_unauthorized_user_update_post(client, create_dummy_posts):
    response = client.put(f"/posts/{create_dummy_posts[0].id}")
    assert response.status_code == 401


def test_update_post_non_exit(authorized_client, create_dummy_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": create_dummy_posts[3].id
    }
    response = authorized_client.put("/posts/10", json=data)
    assert response.status_code == 404
