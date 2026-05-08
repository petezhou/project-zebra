def test_register_user(client):
    """Test user registration."""
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123",
            "full_name": "Test User"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"
    assert "id" in data
    assert "created_at" in data
    assert "password" not in data  # Password should not be in response


def test_register_duplicate_email(client):
    """Test that registering with same email twice fails."""
    user_data = {
        "email": "duplicate@example.com",
        "password": "password123",
        "full_name": "Duplicate User"
    }

    # First registration should succeed
    response1 = client.post("/auth/register", json=user_data)
    assert response1.status_code == 201

    # Second registration with same email should fail
    response2 = client.post("/auth/register", json=user_data)
    assert response2.status_code == 400
    assert "already registered" in response2.json()["detail"].lower()


def test_register_invalid_email(client):
    """Test that invalid email is rejected."""
    response = client.post(
        "/auth/register",
        json={
            "email": "not-an-email",
            "password": "password123",
            "full_name": "Test User"
        }
    )

    assert response.status_code == 422  # Validation error


def test_register_short_password(client):
    """Test that password under 8 characters is rejected."""
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "short",
            "full_name": "Test User"
        }
    )

    assert response.status_code == 422  # Validation error


def test_register_missing_full_name(client):
    """Test that missing full_name is rejected."""
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 422  # Validation error
