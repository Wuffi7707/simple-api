# Simple API
A very simple API for managing Images. Desgined for work in a Docker container.

## env Variable
SECRET_KEY -> Secret Key used for Uploading and Deleting Images
ALLOWED_HOSTS -> Allowed Hosts, that can upload and fetch images
ALLOWED_EDIT_HOSTS -> Allowed Hosts, that can upload images

## Installation
Clone this repository
'''
git clone https://github.com/Wuffi7707/simple-api.git
'''

Navigate into the repository Directory
'''
cd simple-api
'''

Build Docker Image
'''
docker build -t simple-api:latest .
'''

Run the container
'''
docker run -d -p 8000:8000 -e SECRET_KEY=your_secret -e ALLOWED_HOSTS=host1,host2 -e ALLOWED_EDIT_HOSTS=host1,host2 -v /your/volume:/data/images simple-api:latest
'''

## Testing
For testing you can use the `formtest.html`. This file can started localy and don't has to be included in to the Docker container.

(P.S. Pls don't use this in production)