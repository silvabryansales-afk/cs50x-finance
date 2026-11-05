# Personal Finance Tracker
#### Video Demo: https://youtu.be/1mWDOcuw81A
#### Description:

The **Personal Finance Tracker** is a full-stack web application designed and implemented as the capstone final project for CS50’s Introduction to Computer Science (CS50x). The core objective of this project is to empower individual users to manage their personal financial activities efficiently, track income and expenses in real-time, maintain budget awareness, and visualize financial summaries through a clean, modern, and responsive user interface.

Financial literacy and organized personal finance management are critical for individual independence. Many existing tools are either overly complex, require paid subscriptions, or expose sensitive personal data to third-party services. This application was built to offer a lightweight, self-hostable, secure, and intuitive solution built on top of robust web standards and micro-framework technologies.

---

### Project Overview and Architecture

The project is architected using the Model-View-Controller (MVC) design pattern, built with Python's Flask framework at the core. Data storage and relational integrity are powered by SQLite3, while the frontend user interface leverages HTML5, CSS3, Jinja2 template inheritance, and Bootstrap 5 for seamless responsiveness across desktop, tablet, and mobile browsers.

Authentication security is paramount. The system implements industry-standard password hashing using Werkzeug security functions, maintaining secure user sessions with HTTP cookies and Flask session objects.

---

### File Structure and Deep Dive into Modules

The directory structure is organized cleanly to separate backend application logic, database schemas, and presentation layers:

* **`app.py`**:
  This file serves as the main controller and application entry point. It initializes the Flask application, registers custom Jinja2 filters for currency formatting, configures database connections, and contains all HTTP route handlers:
  - **`/register`**: Manages user signup. It performs rigorous server-side validation to ensure that all required fields (username, password, confirmation) are provided, checks for password match, and verifies that the selected username does not already exist in the SQLite database. Passwords are securely hashed with `generate_password_hash` before storage.
  - **`/login` and `/logout`**: Handle session initiation and termination. Upon login, credentials are queried from the database and validated using `check_password_hash`. Session user IDs are stored in Flask's session object to control route access.
  - **`/` (Index / Dashboard)**: Serves as the primary user dashboard. It calculates aggregated financial metrics on the fly—including total account balance, total cumulative income, and total cumulative expenses for the active user. It also fetches the most recent transactions to display in an executive overview table.
  - **`/add`**: Renders and processes the transaction entry form. Users can record financial movements by specifying the transaction type (Income or Expense), selecting an associated category, entering a monetary amount, choosing a transaction date, and adding an optional description.
  - **`/history`**: Retrieves and displays the comprehensive, chronologically sorted ledger of all transactions logged by the logged-in user.

* **`finance.db`**:
  A lightweight SQLite database containing three relational tables bound by foreign key constraints:
  - `users`: Stores user identity details (`id` INTEGER PRIMARY KEY, `username` TEXT UNIQUE, `hash` TEXT NOT NULL).
  - `categories`: Contains reference categories for transaction classification (`id` INTEGER PRIMARY KEY, `name` TEXT NOT NULL, `type` TEXT CHECK(type IN ('income', 'expense'))). Pre-populated categories include Salary, Freelance, Groceries, Housing, Utilities, Entertainment, and Transportation.
  - `transactions`: Stores individual financial entries (`id` INTEGER PRIMARY KEY, `user_id` INTEGER NOT NULL, `category_id` INTEGER NOT NULL, `amount` REAL NOT NULL, `type` TEXT NOT NULL, `description` TEXT, `date` DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (`user_id`) REFERENCES `users`(`id`), FOREIGN KEY (`category_id`) REFERENCES `categories`(`id`)).

* **`templates/layout.html`**:
  The foundational Jinja2 base template that establishes the HTML structure, includes meta tags for viewport scaling, imports Bootstrap 5 CSS/JS bundles via CDN, and defines the global navigation bar. The navigation bar dynamically adapts based on session state, displaying navigation links (`Dashboard`, `Add Transaction`, `History`, `Logout`) for authenticated users, or authentication options (`Login`, `Register`) for guests.

* **`templates/index.html`**:
  The dashboard view extending `layout.html`. It features prominent summary cards displaying Current Balance, Total Income, and Total Expenses formatted in currency style. Below the summary cards, a clean Bootstrap table presents recent activity.

* **`templates/add.html`**:
  A streamlined user interface featuring an interactive HTML form for logging new financial transactions with input validation, dynamic dropdown selection for categories, and numeric input constraints.

* **`templates/history.html`**:
  A detailed ledger view presenting all historical records with visual indicators (e.g., green for incoming revenue, red for outgoing expenses) to facilitate auditing and spending analysis.

* **`templates/login.html` & `templates/register.html`**:
  Clean, minimalist authentication interfaces built with Bootstrap card components and floating form labels for an optimal user experience.

* **`templates/apology.html`**:
  A custom error handling template designed to provide user-friendly feedback whenever validation errors or illegal requests occur.

---

### Key Design Choices and Technical Rationale

1. **Choice of SQLite3 Database Engine**: SQLite3 was selected due to its serverless, zero-configuration architecture, making it perfect for lightweight web applications, local development, and seamless deployment within CS50 Codespaces.
2. **Custom Jinja2 Currency Filter**: To enhance user experience, a custom filter named `eur` was implemented in Python to format standard numeric float values into clean monetary strings with proper grouping and currency symbols.
3. **Database Relational Design & Data Integrity**: Utilizing foreign keys and explicit constraints ensures relational integrity. Transactions cannot exist without a valid user ID or category ID, preventing orphan records.
4. **Defense-in-Depth Security**: Passwords are never stored in plain text. Session management prevents unauthenticated users from accessing protected endpoints through route decorating and session validation checks.
5. **Responsive UI with Bootstrap 5**: Utilizing Bootstrap 5 grid layouts and component primitives guaranteed a consistent, mobile-first design without incurring heavy maintenance overhead for custom CSS styles.

---

### Conclusion and Future Roadmap

The Personal Finance Tracker successfully fulfills all architectural and functional goals set for the CS50x final project. Future enhancements may include interactive graphical charts using Chart.js, multi-currency support, automated monthly budget alerts, and data export capabilities to CSV and PDF formats.
