from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.core.security import (
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
    create_refresh_token,
    get_password_hash,
    verify_password,
)
from app.models.user import User
from app.schemas.auth import Token, UserCreate, UserLogin, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user.

    - **email**: Valid email address (validated by Pydantic)
    - **password**: Minimum 8 characters (will be hashed with Argon2)
    - **full_name**: Optional user's full name
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_password = get_password_hash(user_data.password)

    new_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # Get the ID and timestamps from database

    return new_user


@router.post("/login", response_model=Token)
def login(
    response: Response,
    user_data: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Login and get JWT tokens.

    - **email**: User's email address
    - **password**: User's password

    Returns access token (JSON) and refresh token (httpOnly cookie).
    """
    # Find user by email
    user = db.query(User).filter(User.email == user_data.email).first()

    # Check if user exists and password is correct
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create tokens
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    # Set refresh token in httpOnly cookie (secure, not accessible via JavaScript)
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,  # Prevents XSS attacks
        secure=False,  # Set to True in production (HTTPS only)
        samesite="lax",  # CSRF protection
        max_age=7 * 24 * 60 * 60,  # 7 days in seconds
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/refresh", response_model=Token)
def refresh(
    response: Response,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token (sliding window).

    Refresh token should be in httpOnly cookie.
    Returns new access token and new refresh token (sliding window).
    """
    # Get refresh token from cookie
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token missing",
        )

    try:
        # Decode and verify refresh token
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str | None = payload.get("sub")
        token_type: str | None = payload.get("type")

        if user_id is None or token_type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        # Verify user still exists
        user = db.query(User).filter(User.id == int(user_id)).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )

        # Create new tokens (sliding window - refresh token gets new expiry)
        new_access_token = create_access_token(data={"sub": str(user.id)})
        new_refresh_token = create_refresh_token(data={"sub": str(user.id)})

        # Update refresh token cookie with new expiry
        response.set_cookie(
            key="refresh_token",
            value=new_refresh_token,
            httponly=True,
            secure=False,  # Set to True in production
            samesite="lax",
            max_age=7 * 24 * 60 * 60,
        )

        return {"access_token": new_access_token, "token_type": "bearer"}

    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        ) from e


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user info.

    Requires valid JWT token in Authorization header.
    """
    return current_user


@router.post("/logout")
def logout(response: Response):
    """
    Logout by clearing refresh token cookie.
    """
    response.delete_cookie(key="refresh_token")
    return {"message": "Logged out successfully"}
