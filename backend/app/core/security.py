from passlib.context import CryptContext

# Password hashing context using Argon2
# Argon2 won the Password Hashing Competition (2015)
# More secure than bcrypt against GPU attacks
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """
    Hash a plain password using Argon2.

    Args:
        password: Plain text password

    Returns:
        Hashed password string (includes salt)
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.

    Args:
        plain_password: Plain text password to verify
        hashed_password: Previously hashed password

    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)
