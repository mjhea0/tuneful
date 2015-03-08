import os.path

from flask import url_for
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import relationship

from tuneful import app
from database import Base, engine


class Song(Base):
	__tablename__= "songs"

	id = Column(Integer, primary_key=True)
	song_file = Column(Integer, ForeignKey("files.id"))

	def as_dictionary(self):
		song = {
					"id": self.id,
					"file": {
						#access dict from File object
					}
		}
		return song

class File(Base):
	__tablename__ = "files"

	id = Column(Integer, primary_key=True)
	file_name = Column(String(128))
	song = relationship("Song", backref="song", uselist=False)

	def as_dictionary(self):
		file_dict = {
						"id": self.id,
						"name": self.file_name
		}
		return file_dict