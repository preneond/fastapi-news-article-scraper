"""
Setup of a new app.
"""
from src.core import db

if __name__ == "__main__":
    db.create_empty_db()
    print("Created an empty DB")
