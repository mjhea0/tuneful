import os.path
import json

from flask import request, Response, url_for, send_from_directory
from werkzeug.utils import secure_filename
from jsonschema import validate, ValidationError

import models
import decorators
from tuneful import app
from database import session
from utils import upload_path


# JSON Schema describing the structure of a song
song_schema = {
	"properties": {
		"file": {"type": "string"},
		"id": {"type": "integer"}
	},
	"required": ["id", "song_file"]
}

@app.route("/api/songs", methods=["GET"])
@decorators.accept("application/json")
def get_songs():
	""" Return a list of all the songs as JSON """
	# should we use query string arguments?

	#get the songs from the database
	songs = session.query(models.Song).all()

	#convert the songs to JSON and return a Response
	data = json.dumps([song.as_dictionary() for song in songs])
	return Response(data, 200, mimetype="application/json")

	@app.route("api/songs", methods=["POST"])
	@decorators.accept("application/json")
	@decorators.require("application/json")
	def post_song():
		""" Add a new song """
		data = request.json

		# check that the JSON supplied is valid
		# if not return a 422 Unprocessable Entity
		try:
			validate(data, song_schema)
		except ValidationError as error:
			data = {"message": error.message}
			return Response(json.dumps(data), 422, mimetype="application/json")

		# add the song to the database
		song = models.Song(id=data["id"], song_file=data["song_file"])
		session.add(song)
		session.commit()

		# return a 201 Created, containing the post as JSON and with the
		# location header set to the location of the post
		data = json.dumps(song.as_dictionary())
		headers = {"Location": url_for("get_songs")}
		return Response(data, 201, headers=headers, mimetype="application/json")

