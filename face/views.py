from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from django.http import HttpResponse

from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.storage import staticfiles_storage

from django import forms

from face.result_model import Mlresult

from PIL import Image

import os
import json
import base64
from facetracing.settings import MEDIA_ROOT
# Create your views here.

def get_main_page(request):

	if request.method == "GET":
		return render(request, "face/welcome.html")
	else:
		return HttpResponse("<h1>Invalid HTTP Method</h1>")


def process_request(request):

	if request.method == "GET":
		# Return with invalid HTTP method
		return HttpResponse("<h1>Invalid HTTP Method</h1>")

	# Else it is the POST method
	# Get the files from the request
	# These are the two files gotten from the user
	input_video = None
	input_picture = None

	try:
		# File type: django.core.files.uploadedfile.TemporaryUploadedFile
		input_video = request.FILES["input_video"]
		input_picture = request.FILES["input_picture"]
	except:
		return HttpResponse(status=400) # This is the bad request code

	
	# Hardcoded some result to display
	timeslots = [("00:01:00", "00:01:45"), ("00:02:30", "00:03:12"), ("00:05:57", "00:06:34")]
	images = ["wall7.jpg", "wall7.jpg", "wall8.jpg"]
	# Use the ML models to get the result and get the result
	response_data = {}
	response_data["result"] = []
	for i in range(len(timeslots)):
		ml = Mlresult(timeslots[i], images[i], i+1)
		ml_dicc = {"index":ml.get_index(), "timeslot":ml.get_slot(), 
		"image":"image/" + ml.get_image()}
		# create_base64_img(MEDIA_ROOT + ml.get_image())
		response_data["result"].append(ml_dicc)
	# Return the result
	response_json = json.dumps(response_data)
	print(response_json)

	return HttpResponse(response_json, content_type="application/json")


def create_base64_img(img_url):
	# This is the function to transfer the image file to 64 based encoding code
	base64_str = ""
	html_src = "data:image/png;base64,"
	with open(img_url, "rb") as img:
		base64_str = base64.b64encode(img.read())
	html_src = html_src + base64_str.decode('utf-8')
	return html_src


def get_image(request, img_url):

	# This is the function to retrieve the image resources
	try:
		with open(MEDIA_ROOT + img_url, "rb") as f:
			return HttpResponse(f.read(), content_type="image/jpeg")
	except IOError:
		return HttpResponse(MEDIA_ROOT + "wall7.jpg")

	