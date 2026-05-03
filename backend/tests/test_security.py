from app.core.security import get_password_hash, verify_password


def test_password_hashing():
    """Test password hashing and verification."""
    password = "testpassword123"
    hashed = get_password_hash(password)

    # Hash should not equal plain password
    assert hashed != password

    # Should verify correct password
    assert verify_password(password, hashed) is True

    # Should not verify wrong password
    assert verify_password("wrongpassword", hashed) is False


def test_password_hash_is_different_each_time():
    """Test that same password produces different hashes (due to salt)."""
    password = "testpassword123"
    hash1 = get_password_hash(password)
    hash2 = get_password_hash(password)

    # Hashes should be different (random salt)
    assert hash1 != hash2

    # But both should verify the same password
    assert verify_password(password, hash1) is True
    assert verify_password(password, hash2) is True
