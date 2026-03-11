from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


def get_engine(connection_string: str) -> Engine:
  """
  Create and return a SQLAlchemy engine.

  Args:
    connection_string: SQLAlchemy-compatible database connection string.

  Returns:
    SQLAlchemy Engine instance.
  """
  if not connection_string:
    raise ValueError("A valid connection string must be provided.")

  return create_engine(connection_string)