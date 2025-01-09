# User Management Microservice

## Overview
This microservice provides user authentication and management functionality, including user registration, profile updates, account activation/deactivation, and admin-controlled user creation. It is built with **FastAPI** and uses **JWT authentication** and **role-based access control**.

## Features

1. **Authentication**:
   - `POST /token`: Log in and receive an access token.
2. **User Registration**:
   - `POST /register`: Public endpoint for user registration (default role: `user`).
3. **Admin User Creation**:
   - `POST /users/`: Admin-only endpoint for creating users and assigning roles (`user`, `moderator`, `admin`).
4. **Profile Management**:
   - `GET /users/me`: Get the authenticated user's profile.
   - `PUT /users/me`: Update username, email, password, or full name.
   - `DELETE /users/me`: Delete the authenticated user's account.
5. **Admin Actions**:
   - `GET /users/`: Get a list of all users (admin and moderators only).
   - `PUT /users/{user_id}/activate`: Activate a user account.
   - `PUT /users/{user_id}/deactivate`: Deactivate a user account.

## Technologies Used

- **Backend**: FastAPI, SQLAlchemy
- **Authentication**: JWT (JSON Web Tokens)
- **Database**: MySQL (via phpMyAdmin)
- **Security**: bcrypt for password hashing

## Installation Instructions

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd user_management_service
   ```

2. **Set Up Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/MacOS
   venv\Scripts\activate   # On Windows
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Create a `.env` file in the project root and set your configuration:
   ```env
   DATABASE_URL=mysql+mysqlconnector://<username>:<password>@localhost/<database_name>
   SECRET_KEY=your-secret-key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

## Database Setup

1. Open phpMyAdmin and create the database:
   ```sql
   CREATE DATABASE user_db;
   ```

2. Create the `users` table:
   ```sql
   CREATE TABLE users (
       id INT AUTO_INCREMENT PRIMARY KEY,
       username VARCHAR(50) UNIQUE NOT NULL,
       email VARCHAR(100) UNIQUE NOT NULL,
       full_name VARCHAR(100),
       hashed_password VARCHAR(255) NOT NULL,
       disabled BOOLEAN DEFAULT FALSE,
       role VARCHAR(50) DEFAULT 'user'
   );
   ```

3. (Optional) Insert a default admin user:
   ```sql
   INSERT INTO users (username, email, full_name, hashed_password, role, disabled)
   VALUES ('admin', 'admin@example.com', 'Admin User', '<hashed_password>', 'admin', FALSE);
   ```
   Replace `<hashed_password>` with a hashed password.
   
   To generate a hash:
   ```bash
   uvicorn app.main:app --reload
   # Visit: http://127.0.0.1:8000/password/<your-password>
   ```

## Running the Service

1. **Run the FastAPI Server**:
   ```bash
   uvicorn app.main:app --reload
   ```

2. Access the API documentation:
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## API Endpoints

### **Authentication**
- `POST /token`: Get a JWT access token.
  - **Request Body (form-data)**:
    ```json
    {
      "username": "string",
      "password": "string"
    }
    ```

### **User Registration**
- `POST /register`: Public endpoint for user registration.
  - **Request Body**:
    ```json
    {
      "username": "string",
      "email": "user@example.com",
      "full_name": "string",
      "password": "string"
    }
    ```

### **Admin User Creation**
- `POST /users/`: Admin-only endpoint to create users with roles.
  - **Request Body**:
    ```json
    {
      "username": "string",
      "email": "user@example.com",
      "full_name": "string",
      "password": "string",
      "role": "user | moderator | admin"
    }
    ```

### **User Profile Management**
- `GET /users/me`: Get current user profile.
- `PUT /users/me`: Update current user profile.
  - **Request Body** (Optional fields):
    ```json
    {
      "username": "string",
      "email": "user@example.com",
      "full_name": "string",
      "password": "string"
    }
    ```
- `DELETE /users/me`: Delete current user account.

### **Admin Actions**
- `GET /users/`: Get a list of all users (admin and moderators only).
- `PUT /users/{user_id}/activate`: Activate a user account.
- `PUT /users/{user_id}/deactivate`: Deactivate a user account.

## Deployment (Optional)

To deploy the service using **Docker**:

1. **Create `Dockerfile`**:
   ```dockerfile
   FROM python:3.9
   WORKDIR /app
   COPY . /app
   RUN pip install --no-cache-dir -r requirements.txt
   CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

2. **Build and Run**:
   ```bash
   docker build -t user-management-service .
   docker run -d -p 8000:8000 user-management-service
   ```

## Future Improvements

- Add email verification and password reset functionality.
- Implement strong password validation.
- Add pagination to `GET /users/`.

## Contributors
- **Developer:** Ayman Frimane

---
This `README.txt` provides all the information necessary for the DevOps team to run and deploy the User Management Microservice.

