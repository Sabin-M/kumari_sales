# Kumari Sales

A professional Django-based eCommerce platform built for a modern online shopping experience.

## Overview

`Kumari Sales` is a full-featured eCommerce web application developed with Django. It provides customers with an intuitive shopping experience and administrators with the tools needed to manage products, orders, and sales.

## Key Features

- Product browsing with category filtering
- Detailed product pages and image support
- Shopping cart and checkout flow
- Order management and tracking
- Customer registration and authentication
- Responsive design for desktop and mobile

## Project Structure

- `kumari/` — main Django project configuration
- `sales/` — eCommerce application containing models, views, templates, and forms
- `media/` — uploaded product images and assets
- `static/` — CSS, JavaScript, and image assets for the frontend
- `db.sqlite3` — local development database

## Setup Instructions

1. Create and activate a Python virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Apply database migrations:
   ```bash
   python manage.py migrate
   ```
4. Create a superuser for admin access:
   ```bash
   python manage.py createsuperuser
   ```
5. Start the development server:
   ```bash
   python manage.py runserver
   ```

Then open `http://127.0.0.1:8000/` in your browser.

## Notes

- This project uses SQLite for local development. For production, switch to PostgreSQL or another production-ready database.
- Ensure static files are collected and media settings are configured when deploying.

## License

This project is available for development and customization under an open-source-friendly license. Adjust the license details as needed for your release.
