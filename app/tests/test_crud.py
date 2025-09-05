from app import crud, models

def test_create_and_get_user(db_session):
    user_id = "user123"
    user = crud.create_user_limit(db_session, user_id)

    assert user.clerk_user_id == user_id
    assert user.message_count == 0

    fetched = crud.get_user_limit(db_session, user_id)
    assert fetched is not None
    assert fetched.clerk_user_id == user_id

def test_save_user_updates_count(db_session):
    user = crud.create_user_limit(db_session, "user456")
    user.message_count = 5
    updated = crud.save_user(db_session, user)

    assert updated.message_count == 5
