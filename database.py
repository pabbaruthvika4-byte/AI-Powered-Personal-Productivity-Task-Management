from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from pathlib import Path


# =====================================================
# DATABASE PATH
# =====================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DATABASE_FILE = DATA_DIR / "productivity.db"

DATABASE_URL = f"sqlite:///{DATABASE_FILE}"


# =====================================================
# DATABASE CONNECTION
# =====================================================

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

Base = declarative_base()

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)


# =====================================================
# TASK TABLE
# =====================================================

class Task(Base):

    __tablename__ = "tasks"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(
        String,
        nullable=False
    )

    description = Column(
        String,
        default=""
    )

    priority = Column(
        String,
        default="Medium"
    )

    status = Column(
        String,
        default="Pending"
    )

    category = Column(
        String,
        default="Other"
    )

    due_date = Column(
        String,
        default=""
    )


# =====================================================
# CREATE DATABASE
# =====================================================

def init_db():

    Base.metadata.create_all(
        bind=engine
    )


# =====================================================
# ADD TASK
# =====================================================

def add_task(
    title,
    description,
    priority,
    category,
    due_date
):

    db = SessionLocal()

    try:

        new_task = Task(
            title=title,
            description=description,
            priority=priority,
            status="Pending",
            category=category,
            due_date=due_date
        )

        db.add(new_task)
        db.commit()

    finally:

        db.close()


# =====================================================
# GET ALL TASKS
# =====================================================

def get_tasks():

    db = SessionLocal()

    try:

        tasks = (
            db.query(Task)
            .order_by(Task.id.desc())
            .all()
        )

        return tasks

    finally:

        db.close()


# =====================================================
# COMPLETE TASK
# =====================================================

def complete_task(task_id):

    db = SessionLocal()

    try:

        task = (
            db.query(Task)
            .filter(Task.id == task_id)
            .first()
        )

        if task:

            task.status = "Completed"

            db.commit()

    finally:

        db.close()


# =====================================================
# DELETE TASK
# =====================================================

def delete_task(task_id):

    db = SessionLocal()

    try:

        task = (
            db.query(Task)
            .filter(Task.id == task_id)
            .first()
        )

        if task:

            db.delete(task)

            db.commit()

    finally:

        db.close()