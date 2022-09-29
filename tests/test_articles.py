from app import database,models


def test_get_one_article(client, test_articles, acces_token):
    article = client.get(f"/articles/{test_articles[0].id}", headers={'Authorization':f'Bearer {acces_token}'})

    assert article.status_code == 200
    assert article.json()['id'] ==test_articles[0].id
    assert article.json()['title'] == test_articles[0].title
    assert article.json()['content'] == test_articles[0].content

def test_get_one_article_not_exist(client, acces_token):
    article = client.get(f"/articles/{8888}", headers={'Authorization':f'Bearer {acces_token}'})

    assert article.status_code == 404


def test_get_all_articles(client, test_articles, acces_token):
    articles = client.get("/articles/", headers={'Authorization':f'Bearer {acces_token}'})

    assert articles.status_code == 200
    assert articles.json()[0]['id'] == test_articles[0].id
    assert articles.json()[1]['title'] == test_articles[1].title

def test_get_all_articles_unauthorized_user(client):
    articles = client.get("/articles/")

    assert articles.status_code == 401

def test_create_article(client, acces_token):
    article_data = {'title':'title','content':'content'}
    new_article = client.post("/articles/", headers={'Authorization':f'Bearer {acces_token}'}, json=article_data)

    assert new_article.status_code == 201
    assert new_article.json()['title'] == article_data['title']

def test_update_article(client, acces_token, test_articles, session):
    new_article = {'title':'new title', 'content':'new content'}
    article = client.put(f"/articles/{test_articles[0].id}", headers={'Authorization':f'Bearer {acces_token}'}, json=new_article)

    assert article.json()['title'] == new_article['title']

def test_delete_article(client,test_articles, acces_token):
    article = client.delete(f"/articles/{test_articles[0].id}", headers={'Authorization':f'Bearer {acces_token}'})

    article.status_code == 204



    
   