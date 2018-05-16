# Crab n' Click

## Summary

Crab n' Click is a Django application designed to assist the NOAA with crab oocyte area analysis. It provides an interactive session for users to click through photos of crab oocytes identify the best among those that an image analysis process has selected as being good. This data is then stored within Socrata, a government cloud storage service.

## Requirements

The following versions and packages are required to properly run Crab n' Click:

1.	Python version >= 3.5
2.	Django version >= 2.0
3.	SodaPy
4.	Psycopg2

## Setup

Populating the system with the appropriate images is critical for Crab n' Click to be of use. To do this, first run the migrations:

`python manage.py migrate`

Then enter the Django shell:

`python manage.py shell`

Next, import the models:

`from crabgame.models import Crab, Image, Oocyte`

Finally, call the Crab class method create_image_instances with a path to a directory:

`Crab.create_image_instances(PATH)`

This path should be a directory that has a structure similar to the example below:

	images
		0
			untitled000_resized.png
			untitled000_labeled.png
			untitled001_resized.png
			untitled001_labeled.png
		1
			untitled000_resized.png
			untitled000_labeled.png
		2
			untitled000_resized.png
			untitled000_labeled.png
		3
			untitled000_resized.png
			untitled000_labeled.png
		4


These images should have been generated by the process_images.py script which the user should also have access to.

In crabgame/models.py, add your Socrata login information to the lines where the api is accessed:

`client = Socrata("noaa-fisheries-afsc.data.socrata.com", "q3DhSQxvyWbtq1kLPs5q7jwQp",  username="<USERNAME>", password = "<PASSWORD>")`

## Usage

To run the server locally, use the standard command:

`python manage.py runserver`
