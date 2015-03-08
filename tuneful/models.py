import os.path

from flask import url_for
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import relationship

from tuneful import app
from database import Base, engine


class Song(Base):
	__tablename__= "songs"

	id = Column(Integer, primary_key=True)
	song_file = Column(Integer, ForeignKey("files.id"), nullable=False)

	def as_dictionary(self):
		song_file_info = session.query(File).filter(File.id==self.song_file)
		song = {
					"id": self.id,
					"file": {
						"id": song_file_info.id,
						"name": song_file_info.file_name
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