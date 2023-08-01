
# News Site

This project is a news site built with Django. It provides a set of APIs for managing and retrieving news articles.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python
- Docker (optional)

### Installation

1. Clone the repository to your local machine.

2. Navigate to the project directory.

3. You have two options to run the project: 
    - Using Docker:
        ``` docker-compose up --build -d```

    - Using Python:
        - Make migrations and run the project:
            ``` python manage.py migrate```
            ``` python mange.py runserver```

## API Documentation

Once the project is running, navigate to the `/swagger-ui/` endpoint in your web browser to view the API documentation and learn how to use the project endpoints.


