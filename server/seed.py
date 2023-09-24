#!/usr/bin/env python3

from app import db
from models import Task

if __name__ == '__main__':
    # Create all database tables if they don't exist
    db.create_all()

    # Create and add tasks related to football
    task1 = Task(title='Play Football', description='Play a game of football with friends', done=False)
    task2 = Task(title='Watch Football Match', description='Watch your favorite football team play', done=True)

    db.session.add(task1)
    db.session.add(task2)

    # Commit the changes to the database
    db.session.commit()

    print("Initial data related to football has been added to the database.")

