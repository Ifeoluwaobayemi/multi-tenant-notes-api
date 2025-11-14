# Multi-tenant Notes API

This is a simple multi-tenant REST API for creating, viewing, and managing notes. The API is built with FastAPI and uses MongoDB for data storage. Multi-tenancy is achieved by logically separating data for each organization based on an `org_id`.

## Assumptions and Simplifications

*   **Multi-tenancy:** Tenancy is based on a unique organization ID (`org_id`). Data is logically separated within a single MongoDB database. This is a simple approach and for larger-scale applications, a more robust strategy (e.g., database per tenant) might be required.
*   **Authentication:** User authentication is handled via JWT. The token contains the user's ID, organization ID, and role.
*   **Authorization:** Authorization is role-based (e.g., `admin`, `writer`). This is enforced at the endpoint level.
*   **Security:** For simplicity, the `JWT_SECRET` in the setup instructions is a simple string. In a production environment, this should be a securely generated, strong key.
*   **Error Handling:** Basic error handling is in place, but could be extended for more specific use cases.

## Setup Instructions

The application is designed to be run with Docker.

### 1. Environment Variables

Create a `.env` file in the `app` directory. You can copy the example below:

```
# .env

# MongoDB connection string
MONGO_URI="mongodb://mongo:27017"

# The name of the database to use
DATABASE_NAME="multi_tenant_notes"

# Secret key for encoding/decoding JWTs
JWT_SECRET="a-very-secret-key"

# JWT Algorithm
JWT_ALGORITHM="HS256"

# Access token expiration in minutes
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

### 2. Running the Application

With Docker and Docker Compose installed, run the following command from the root of the project (`multi-tenant-notes-api/app`):

```bash
docker-compose up -d
```

The API will be available at `http://localhost:8000`.

### 3. Running Tests

The project includes a suite of tests using `pytest`. To run the tests, execute the following command after starting the application with `docker-compose`:

```bash
# This assumes your web service in docker-compose.yml is named 'web'
docker-compose exec web pytest
```

The tests will run against the database specified in your `.env` file. For a clean test run, the tests will clear all data from the collections at the beginning of the test session.

### 4. API Documentation

The API documentation is automatically generated using FastAPI's Swagger UI. Once the application is running, you can access the interactive documentation at:

[http://localhost:8000/api/docs](http://localhost:8000/api/docs)

Alternatively, you can view the ReDoc documentation at:

[http://localhost:8000/api/redoc](http://localhost:8000/api/redoc)

---

## Example API Requests

Here are some example `cURL` requests to interact with the API.

### Organizations

First, create an organization.

```bash
curl -X POST "http://localhost:8000/organizations/" -H "Content-Type: application/json" -d 
'{'
  "name": "My Awesome Org"
}'
```

The response will contain the new organization's ID. Let's assume the ID is `667d8f3b8e5bf7e6f3f4d4f6`.

### Users

Now, create a user within that organization. Users can have roles like `admin`, `writer`, or `reader`.

```bash
# Replace {org_id} with the actual ID from the previous step
ORG_ID="667d8f3b8e5bf7e6f3f4d4f6"

curl -X POST "http://localhost:8000/organizations/${ORG_ID}/users/" -H "Content-Type: application/json" -d 
'{'
  "username": "testuser",
  "password": "password123",
  "email": "test@example.com",
  "role": "admin"
}'
```

Next, log in as the user to get a JWT access token.

```bash
# Replace {org_id} with your organization ID
ORG_ID="667d8f3b8e5bf7e6f3f4d4f6"

curl -X POST "http://localhost:8000/organizations/${ORG_ID}/users/login" -H "Content-Type: application/json" -d 
'{'
  "username": "testuser",
  "password": "password123"
}'
```

The response will contain an `access_token`. You'll need to use this token in the `Authorization` header for subsequent requests.

```json
{
  "access_token": "your.jwt.token",
  "expires_at": "..."
}
```

### Notes

Now you can perform actions on notes as an authenticated user.

**Export the token to a variable for ease of use:**
```bash
TOKEN="your.jwt.token"
```

**Create a note:**

You must have the `writer` or `admin` role.

```bash
curl -X POST "http://localhost:8000/notes/" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer ${TOKEN}" \
     -d 
'{'
  "title": "My First Note",
  "content": "This is the content of my first note."
}'
```

**List all notes for the organization:**

```bash
curl -X GET "http://localhost:8000/notes/" \
     -H "Authorization: Bearer ${TOKEN}"
```

**Get a specific note by ID:**

```bash
# Replace {note_id} with an actual note ID from the previous responses
NOTE_ID="667d902b8e5bf7e6f3f4d4f8"

curl -X GET "http://localhost:8000/notes/${NOTE_ID}" \
     -H "Authorization: Bearer ${TOKEN}"
```

**Delete a note:**

You must have the `admin` role.

```bash
# Replace {note_id} with an actual note ID
NOTE_ID="667d902b8e5bf7e6f3f4d4f8"

curl -X DELETE "http://localhost:8000/notes/${NOTE_ID}" \
     -H "Authorization: Bearer ${TOKEN}"
```
