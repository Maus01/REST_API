from app import utils
from app import models


def test_create_user(client):
    user_data = {'email':'email@email.com','password':'password'}
    new_user = client.post('/users/', json=user_data)

    assert new_user.status_code == 201

def test_change_password(client, acces_token, session):
    password_data={"old_password":"password", "new_password":"password1"}
    user = client.put("/users/", headers={'Authorization':f'Bearer {acces_token}'}, json=password_data)


    changed_user=session.query(models.Users).filter(models.Users.id == user.json()['id'] ).first()

    assert user.status_code == 200
    assert utils.verify(changed_user.password, password_data['new_password'])