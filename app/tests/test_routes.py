def test_send_message_success(client):
    response = client.post("/messages/send/testuser")
    data = response.json()

    assert response.status_code == 200
    assert data["success"] is True
    assert "1/20" in data["usage"]

def test_send_message_hits_limit(client):
    user_id = "limitroute"

    # Hit 20 times
    for _ in range(20):
        client.post(f"/messages/send/{user_id}")

    response = client.post(f"/messages/send/{user_id}")
    data = response.json()

    assert response.status_code == 429
    assert "Message limit exceeded" in data["detail"]
