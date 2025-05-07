![ERD](https://github.com/user-attachments/assets/227d2b49-b869-497e-9009-e6c5df751fdc)# share-skill-backend 
## 📊 Entity Relationship Diagram (ERD)

> The ERD illustrates the database structure and relationships between core models: `User`, `Category`, `ServiceListing`, `ServiceRequest`, and `Review`.

![ERD](https://github.com/user-attachments/assets/571991ef-2a49-44f0-905a-383d46687285)


---

## 🔗 RESTful Routing Table

### 4.1. Server-Side API Routes (Django REST Framework)

| HTTP Method | Path                                 | Action                               | CRUD     | Authentication Required      |
|-------------|--------------------------------------|--------------------------------------|----------|-------------------------------|
| GET         | `/api/categories/`                   | List all categories                  | Read     | Optional                      |
| POST        | `/api/categories/`                   | Create a new category                | Create   | Admin                         |
| GET         | `/api/categories/{id}/`              | Retrieve category details            | Read     | Optional                      |
| PUT/PATCH   | `/api/categories/{id}/`              | Update category                      | Update   | Admin                         |
| DELETE      | `/api/categories/{id}/`              | Delete category                      | Delete   | Admin                         |
| GET         | `/api/servicelistings/`              | List active service listings         | Read     | Optional                      |
| POST        | `/api/servicelistings/`              | Create a service listing             | Create   | Authenticated (Provider)      |
| GET         | `/api/servicelistings/{id}/`         | Retrieve service listing             | Read     | Optional                      |
| PUT/PATCH   | `/api/servicelistings/{id}/`         | Update service listing               | Update   | Owner                         |
| DELETE      | `/api/servicelistings/{id}/`         | Delete service listing               | Delete   | Owner                         |
| GET         | `/api/servicerequests/`              | List relevant service requests       | Read     | Authenticated                 |
| POST        | `/api/servicerequests/`              | Create a service request             | Create   | Authenticated (Client)        |
| GET         | `/api/servicerequests/{id}/`         | Retrieve request details             | Read     | Involved User                 |
| PATCH       | `/api/servicerequests/{id}/`         | Update request status                | Update   | Provider / Client             |
| DELETE      | `/api/servicerequests/{id}/`         | Cancel/Delete service request        | Delete   | Client / Provider             |
| GET         | `/api/reviews/`                      | List reviews (optionally filtered)   | Read     | Optional                      |
| POST        | `/api/reviews/`                      | Create a review                      | Create   | Authenticated (Client)        |

### 🧑‍💻 Auth Routes

| HTTP Method | Path                     | Action                        | Authentication Required |
|-------------|--------------------------|-------------------------------|--------------------------|
| POST        | `/api/auth/register/`    | Register                      | No                       |
| POST        | `/api/auth/login/`       | Login (get tokens)            | No                       |
| POST        | `/api/auth/logout/`      | Logout (invalidate token)     | Yes                      |
| GET         | `/api/auth/user/`        | Get current user profile      | Yes                      |

---

## 🌐 4.2. Client-Side Routes (React)

| Path                          | Page/Component           | Purpose                                      |
|------------------------------|--------------------------|----------------------------------------------|
| `/`                          | `HomePage`               | Landing page, search                         |
| `/login`                     | `LoginPage`              | User login                                   |
| `/register`                  | `RegisterPage`           | User registration                            |
| `/services`                  | `ServiceListPage`        | Browse/search services                       |
| `/services/{id}`             | `ServiceDetailPage`      | View service details                         |
| `/services/new`              | `ServiceCreatePage`      | Create service listing (Provider)            |
| `/services/{id}/edit`        | `ServiceEditPage`        | Edit service listing (Provider)              |
| `/dashboard`                 | `DashboardPage`          | User dashboard overview                      |
| `/dashboard/my-listings`     | `MyListingsPage`         | Provider's listings                          |
| `/dashboard/requests-received` | `RequestsReceivedPage` | Provider's received requests                 |
| `/dashboard/my-requests`     | `MyRequestsPage`         | Client's sent requests                       |
| `*`                          | `NotFoundPage`           | Catch invalid URLs                           |

---

## 🧑‍💼 5. User Stories

### 🔐 Authentication
- Users can **register**, **log in**, **log out**, and **view/edit their profile**.

### 🔍 Browsing (Client)
- Clients can **browse**, **search**, **filter**, and **view details** of service listings.

### 📢 Service Listing Management (Provider)
- Providers can **create**, **read**, **update**, and **delete** their own listings.

### 📥 Service Request Management (Client & Provider)
- Clients can **create** requests for services.
- Clients & Providers can **view** requests relevant to them.
- Providers can **update** request status.
- Both can **cancel/delete** requests.

### ⭐ Reviews (Optional)
- Clients can **leave reviews** on completed listings.
- Listings display **associated reviews**.

---

