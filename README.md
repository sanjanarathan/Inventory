# Inventory Management System

The **Inventory Management System** is a web application built using **Flask**, **SQLite**, and **SQLAlchemy**. It enables users to efficiently manage inventory items with features like adding, updating, deleting, and viewing items. The application also includes a user authentication system to ensure secure access to inventory data.

---

## Features

- **User Authentication**:
  - Register, login, and logout functionalities.
  - Secure password storage using hashing.

- **Inventory Management**:
  - Add new inventory items.
  - Update existing item details.
  - Delete items from the inventory.
  - View all inventory items in a tabular format.

- **Database Integration**:
  - SQLite database for storing user and inventory data.
  - ORM support using SQLAlchemy.

- **Responsive Frontend**:
  - HTML and CSS for a user-friendly interface.

- **Optional Features**:
  - Category-wise organization.
  - Search functionality.
  - Data visualization for inventory trends.

---

## Tech Stack

### Backend
- **Flask**: Micro web framework for building the application.
- **Flask-Login**: User authentication and session management.
- **SQLAlchemy**: ORM for database interactions.
- **SQLite**: Lightweight database for persistent data storage.

### Frontend
- **HTML/CSS**: For structuring and styling the application interface.

---

## Project Structure

```plaintext
inventory_management/
│
├── app.py                      # Main Flask application
├── models.py                   # SQLAlchemy models
├── templates/                  # HTML templates
│   ├── base.html               # Base layout
│   ├── login.html              # Login page
│   ├── register.html           # Registration page
│   ├── inventory.html          # Inventory management page
│   ├── add_item.html           # Add new item page
│   ├── update_item.html        # Update existing item page
├── static/                     # Static files (CSS, JS)
│   ├── styles.css              # Custom styles
├── inventory.db                # SQLite database file
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
