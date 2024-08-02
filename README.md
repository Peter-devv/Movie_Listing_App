# Movie Listing API

This project is a movie listing API designed to allow users to list movies, view listed movies, rate them, and add comments. It integrates movie management, user authentication, and rating and commenting features to provide a comprehensive movie catalog experience. The application is secured using JWT (JSON Web Tokens) to ensure that only the user who listed a movie can edit it and is deployed on a cloud platform.

## Technology Used

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

User Authentication
- **User Registration**: Create a new user account.
- **User Login**: Authenticate users and issue JWT tokens.
- **JWT Token Generation**: Secure access to endpoints with JSON Web Tokens.
Movie Listing
- **View All Movies**: Public access to view all listed movies.
- **View a Movie**: Public access to view details of a specific movie.
- **Add a Movie**: Authenticated users can list new movies.
- **Edit a Movie**: Only the user who listed the movie can edit it.
- **Delete a Movie**: Only the user who listed the movie can delete it.
Movie Rating
- **Rate a Movie**: Authenticated users can rate movies.
- **Get Ratings for a Movie**: Public access to view all ratings for a specific movie.
Comments
- **Add a Comment to a Movie**: Authenticated users can add comments to movies.
- **View Comments for a Movie**: Public access to view all comments for a specific movie.
- **Add Nested Comments**: Authenticated users can reply to existing comments.


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