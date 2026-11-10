from sqlalchemy import text

from app.db.session import engine


try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version()"))
        print("Successfully connected to PostgreSQL!")
        print(result.scalar())

except Exception as error:
    print("Database connection error:")
    print(error)

finally:
    engine.dispose()