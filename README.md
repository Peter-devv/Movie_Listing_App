# Movie Listing API

This project is a movie listing API designed to allow users to list movies, view listed movies, rate them, and add comments. It integrates movie management, user authentication, and rating and commenting features to provide a comprehensive movie catalog experience. The application is secured using JWT (JSON Web Tokens) to ensure that only the user who listed a movie can edit it and is deployed on a cloud platform.

## Technical Stack

- **Language**: Python
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **Authentication**: JWT (JSON Web Tokens)
- **ORM**: SQLAlchemy
- **Password Hashing**: Passlib
- **Cloud Platform**: Render
- **Testing**: Pytest
- **Documentation**: OpenAPI/Swagger
- **Environment Variables**: python-dotenv


## Features

- **User Authentication:**
Secure user login and registration using JWT, ensuring that only authenticated users can perform certain actions.

- **CRUD Operations:**
Create, read, update, and delete operations for movies, users, ratings, and comments, with fine-grained control over who can modify or delete content.

- **Movie Management:**
Users can list new movies, search for existing movies by genre or other criteria, and view detailed information about each movie.

- **Rating and Comments:**
Users can rate movies and leave comments, enhancing the interaction within the movie community. Ratings and comments are tied to specific movies and users.

- **Advanced Querying:**
The API supports filtering, pagination, and searching, allowing for efficient retrieval of large datasets with ease.

- **Dependency Injection and Modularity:**
The API leverages FastAPI's dependency injection system to manage resources like database sessions, making it modular, maintainable, and easy to extend.

- **Logging and Error Handling:**
Built-in logging and comprehensive error handling ensure that the API operates smoothly and that any issues can be diagnosed and resolved quickly.


## Use Cases:

- **Movie Listing Platforms:** Ideal for building movie databases or platforms where users can share and discover movies.

- **Review Aggregators:** Can be used for services that aggregate and manage movie ratings and reviews.

- **Content Management Systems (CMS):** Suitable for media-related CMS where movies and related content are core components.

## Getting Started

### Prerequisites

Python 3.12.1
PostgreSQL

## API documentation:

Open your browser and go to http://127.0.0.1:8000/docs to see the interactive API documentation.


### Installation

1. **Clone the repository**:

   ```sh
   git clone https://github.com/Peter-devv/Movie_Listing_App.git
   cd Movie_Listing_App
   ``` 

2. **Install the dependencies**:

    ```sh
    pip install -r requirements.txt
    ```

3. **Set up the database**: 

Create a PostgreSQL database and configure the connection in the `.env` file.
```
SQLALCHEMY_DATABASE_URL=your_database_url  # Replace with your database URL
```

4. **Run database migrations**:

   ```sh
   alembic upgrade head
   ```

5. **Start the application**:

    ```sh
    uvicorn app.main:app --reload
    ```

### Running Tests

To ensure the API functions correctly, we have implemented tests using `pytest`.

1. **Install `pytest`**:

   ```sh
   pip install pytest
   ```

2. **Run the tests**:
   ```sh
   pytest
   ```


## Project Structure

```
MOVIE_API/
├── .pytest_cache/
├── alembic/      
├── app/
│   ├── __pycache__/
│   ├── routers/
│   ├── tests/
│   ├── config.py
|   |── crud.py
│   ├── database.py
│   ├── logger.py
│   ├── main.py
│   ├── models.py
│   ├── oauth2.py
│   ├── schemas.py
│   ├── text.txt
│   ├── utils.py
├── .env
├── .gitignore
├── alembic.ini
├── README.md 
├── requirements.txt

## Contributing

Contributions are welcome! Please create a pull request with a detailed description of your changes.

## Contact

For more information, please contact [peterimade6@gmail.com](mailto:peterimade6@gmail.com).