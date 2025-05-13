![alt text](<Unlock Community Connections and Services.png>)

## 🛠️ ShareSkill - Backend

### 📝 Brief Description
This is the backend for the Local Services Marketplace application. It handles the server-side logic, API endpoints, database interactions, and authentication for the platform. This part of the project provides the data and services needed by the frontend.

### ℹ️ About This README
This README file provides an overview of the backend application, including the technologies used, database schema (ERD), API routes, and installation instructions. Its purpose is to guide developers in setting up, understanding, and contributing to the backend codebase.

### 🗺️ Planning Materials
Key planning aspects related to the backend include:
*   User authentication (registration, login, logout).
*   API endpoints for managing service categories, listings, requests, and reviews.
*   Database design to support core functionalities and relationships.
*   Ensuring secure and efficient data handling.
 

### 💻 Technologies Used
*   **Django**: A high-level Python web framework that encourages rapid development and clean, pragmatic design.
*   **Django REST Framework**: A powerful and flexible toolkit for building Web APIs.
*   **SQL (PostgreSQL/SQLite)**: Database management system (PostgreSQL for production, SQLite for development).
 

 
### 📊 ERD Diagram

![alt text](ERD.png)

**Note:** The `USER` model here represents a general user. The distinction between 'Client' and 'Provider' roles can be managed via a field within the USER model (e.g., `user_type`) or through relationships if more complex role-based permissions are needed beyond what Django's built-in groups/permissions offer. The relationships shown (e.g., `USER provides SERVICELISTING`) imply the USER in that context is a Provider. Similarly, `USER requests SERVICEREQUEST` implies the USER is a Client.

**Models Overview:**
*   **User (Django Auth)**: Manages user accounts and authentication.
*   **Category**: Defines types of services offered.
*   **ServiceListing**: Represents a specific service offered by a Provider.
*   **ServiceRequest**: Represents a Client's request for a service.
*   **Review**: Allows Clients to review completed services.

### 🌐 API Routes (Django REST Framework)
#### Authentication Routes
| HTTP Method | Path                | Action                      | CRUD | Authentication Required |
| ----------- | ------------------- | --------------------------- | ---- | ----------------------- |
| POST        | `/api/auth/register/` | User Registration           | C    | None                    |
| POST        | `/api/auth/login/`    | User Login (obtain token)   | N/A  | None                    |
| POST        | `/api/auth/logout/`   | User Logout (invalidate token) | N/A  | Authenticated           |
| GET         | `/api/auth/user/`     | Get current logged-in user details | R    | Authenticated           |

#### Category Routes
| HTTP Method | Path                     | Action                             | CRUD | Authentication Required |
| ----------- | ------------------------ | ---------------------------------- | ---- | ----------------------- |
| GET         | `/api/categories/`       | List all categories                | R    | Optional                |
| POST        | `/api/categories/`       | Create a new category              | C    | Admin                   |
| GET         | `/api/categories/{id}/`  | Retrieve details of a specific category | R    | Optional                |
| PUT/PATCH   | `/api/categories/{id}/`  | Update a specific category         | U    | Admin                   |
| DELETE      | `/api/categories/{id}/`  | Delete a specific category         | D    | Admin                   |

#### Service Listing Routes
| HTTP Method | Path                          | Action                                  | CRUD | Authentication Required |
| ----------- | ----------------------------- | --------------------------------------- | ---- | ----------------------- |
| GET         | `/api/servicelistings/`       | List active service listings (filtered) | R    | Optional                |
| POST        | `/api/servicelistings/`       | Create a new service listing            | C    | Authenticated (Provider)|
| GET         | `/api/servicelistings/{id}/`  | Retrieve details of a specific service listing | R    | Optional                |
| PUT/PATCH   | `/api/servicelistings/{id}/`  | Update a specific service listing       | U    | Owner                   |
| DELETE      | `/api/servicelistings/{id}/`  | Delete a specific service listing       | D    | Owner                   |

#### Service Request Routes
| HTTP Method | Path                           | Action                                  | CRUD | Authentication Required |
| ----------- | ------------------------------ | --------------------------------------- | ---- | ----------------------- |
| GET         | `/api/servicerequests/`        | List requests relevant to the current user | R    | Authenticated           |
| POST        | `/api/servicerequests/`        | Create a new service request            | C    | Authenticated (Client)  |
| GET         | `/api/servicerequests/{id}/`   | Retrieve details of a specific request  | R    | Involved User           |
| PATCH       | `/api/servicerequests/{id}/`   | Update request status                   | U    | Provider / Client       |
| DELETE      | `/api/servicerequests/{id}/`   | Delete/Cancel a service request         | D    | Client / Provider       |

#### Review Routes
| HTTP Method | Path                     | Action                                  | CRUD | Authentication Required |
| ----------- | ------------------------ | --------------------------------------- | ---- | ----------------------- |
| GET         | `/api/reviews/`          | List reviews (filtered by listing)      | R    | Optional                |
| POST        | `/api/reviews/`          | Create a new review                     | C    | Authenticated (Client)  |
| GET         | `/api/reviews/{id}/`     | Retrieve details of a specific review   | R    | Optional                |
| PUT/PATCH   | `/api/reviews/{id}/`     | Update a specific review                | U    | Owner                   |
| DELETE      | `/api/reviews/{id}/`     | Delete a specific review                | D    | Owner                   |

### ⚙️ Installation Instructions
To get the backend development environment running:

1.  **Clone the repository:**
    ```bash
     (https://github.com/tunourah/shareskill_back)
    ```
 
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set up the database:**
    *   For SQLite (development): No further setup usually needed, Django will create the file.
    *   For PostgreSQL (production): Ensure PostgreSQL is installed and running. Create a database and user, then update `settings.py` with your database credentials.
    ```python
    # Example DATABASES setting in settings.py for PostgreSQL
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'your_db_name',
            'USER': 'your_db_user',
            'PASSWORD': 'your_db_password',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    ```
5.  **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```
6.  **Create a superuser (optional, for admin access):**
    ```bash
    python manage.py createsuperuser
    ```
7.  **Start the development server:**
    ```bash
    python manage.py runserver
    ```
    The API should now be accessible at `http://127.0.0.1:8000/`.

### 🚀 Running the Application
*   Ensure the virtual environment is activated.
*   Run `python manage.py runserver`.

### 🧪 Running Tests
```bash
python manage.py test
```
### Frontend Link
`https://github.com/tunourah/shareskill_front`

 
