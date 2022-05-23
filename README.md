## Product Catalog

### Setup instruction

* Create your virtual environment with: `python3 -m venv venv`
* Turn it on: `source venv/bin/activate`
* Install all packages from requirements.txt file by : `pip install -r requirements.txt`
* Create a `.env` file and copy everything from `.sample-env` file
* Create a PostgreSQL db and add all information in `.env` file
* Run migrations by `python manage.py migrate`
* Create a superuser by : `python manage.py createsuperuser`


### Scrap Images
* This application will scrap images from `unsplash.com` with a hard code image type
* In terminal run this management command `python manage.py pull_images` (Make sure your virtual env is running & you did db migration)
* All images can be found to `/media/images/` directory

### How the scraping will work
* Before scrapping we don't know about the image & its size
* We have some pre-defines sizes which are small -> 256, medium -> 1024 , large - 2048
* The scrapping script first pull an image from server & save it as `original` image. Just after that operation the script try to resize the image in 3 different sizes. Small, Medium & Large. The height of image is calculated from the original ration & the ration is same for any size.
* The script only save the original image information in database (In the Image & ImageMetadata table)
* When a user filter `/images` API with size, the system just take the original image & just calculate the width & height & prepare an url for that size. It need not to query in DB for that reason.
* When the script will resize image, it checks the difference of original size & the requested size. If the original size is less then the requested size, the image will be remain same. Which means that, if user filter image by the size & the original size is less than that size, then original image will be shown. 

### API Doc

* Image List API: `/api/v1/images`
* Image by ID: `/api/v1/images/:id` --> This will retrieve a single image information
* Filter by size: `/api/v1/images/?size=medium` --> This will show a list of image with medium size
* Filter by original url: `/api/v1/images/?original_url=` --> This will show a list of image with the original url
* ImageMetadata List API: `/api/v1/image-metadatas/`
* ImageMetadata by ID: `/api/v1/image-metadatas/:id` --> This will retrieve a single image metadata information
* Filter by original url: `/api/v1/image-metadatas/?original_url=` --> This will show a list of image with the original url