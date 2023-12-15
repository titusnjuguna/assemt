## Assemt Repository
it is a django based software that takes two csv file and compare them and finally generate a report out of it.Additonally, there is a test written for this project included in the test directory
### Tech Stack
- Python
- Django
- Docker
- SQLite

## Requirement
- Docker
  

### User Guide
1. ```
   Git clone https://github.com/titusnjuguna/assemt.git
   ```
3. Open your favourite cmd tool
4. Navigate to the root folder of the project
5. Build an image from the docker file provided in the project parent folder
   ````
   docker build --no-cache -t my-django-app .
   ````
6. Get the image name and copy the image id
   ````
   docker images
   ````
7. Run the container
   ````
   docker run -p 8000:8000 <image id goes here>
   ````
8. Open your browser and go to this address:
   ````
   http://localhost:8000/index
   ````
9. Use csv files provided in the project folder to test
