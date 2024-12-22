# Django JWT Authentication Project

This project is a Django-based API that uses `djangorestframework-simplejwt` for JSON Web Token (JWT) authentication. The configuration sets the access token expiration to 24 hours. The project includes user registration, login, and user profile endpoints.

## Features

- Secure user authentication with JWT.
- 24-hour expiration for access tokens.
- Refresh tokens for prolonged access.
- Easy integration with Django Rest Framework (DRF).
- User registration and login endpoints.
- User profile endpoint for retrieving user information.
- Custom user model for user management.

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations

```bash
python manage.py migrate
```

### 5. Run the Development Server

```bash
python manage.py runserver
```

## Configuration

### JWT Settings

The JWT settings are configured in `settings.py` using the `djangorestframework-simplejwt` library. The access token expiration is set to 24 hours:

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=24),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': 'your-secret-key',
}
```

### Authentication Classes

Ensure `JWTAuthentication` is added to the default authentication classes:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}
```

## Endpoints

### Token Endpoints

| Endpoint              | Method | Description                      |
| --------------------- | ------ | -------------------------------- |
| `/api/token/`         | POST   | Obtain access and refresh tokens |
| `/api/token/refresh/` | POST   | Refresh the access token         |

#### Example Request to Obtain Tokens

```bash
POST /api/token/
{
    "username": "your_username",
    "password": "your_password"
}
```

#### Example Response

```json
{
  "access": "<jwt-access-token>",
  "refresh": "<jwt-refresh-token>"
}
```

## Testing

To verify the expiration and functionality of tokens, use tools like Postman or curl to interact with the API. You can also decode the JWT using [jwt.io](https://jwt.io) to check the `exp` field.

## Dependencies

- Python 3.8+
- Django 4.x
- djangorestframework 3.x
- djangorestframework-simplejwt

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

Happy coding!
