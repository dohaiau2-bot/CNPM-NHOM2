"""
models/__init__.py
Package chứa các Model xử lý dữ liệu
"""

from models.database import Database
from models.book_model import BookModel

__all__ = ['Database', 'BookModel']