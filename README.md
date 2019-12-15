# cs0060_Internship_Tracker
authors: jweissko, grusu, drozenb1
First deployment: 12/15/2019

Instructions for local deplyment:

1. If deploying for use on the same computer, then in main.py, change 'dbserver' to 'localhost' in this line:
     app.config['MONGO_URI'] = 'mongodb://dbserver:27017/logindb'
2. Start the mongodb daemon:
    mongod
3. run the following command to runt the app:
    ./run.sh

Instructions for remote deployment using docker and nginx:
1. Create requirements.txt using capitalization for modules as is correct in the command 'pip3 install <module_name>'
2. Create Dockerfile (see our Dockerfile for an example)
3. Create docker-compose.yaml file
4. Upload the cs0060_Internship_Tracker to server (for example, by using git clone)
6. Run the following command to create the docker images: 
     docker-compose -f docker-compose.yaml build
7. Run the following command to start the docker images:
     docker-compose -f docker-compose.yaml up
8. Go to internship.team and check that it is connecting

Basic File Structure

information files:
README.md
db_schema.md

main application files: 
run.sh
main.py

deployment files: 
- Dockerfile
- requirements.txt
- nginx.config
- docker-compose.yaml
 
 Templates
    - layout.html
    - login.html
    - internship.html
    - register.html
    - documents.html
 
 static
    - client
          - clientfolder.txt
    - images
          - favicon.ico
          - pdf_image.jpg
          - pdf_image2.png
    - internship_tracker.css
    
Short overview:
main.py handles the logic for Internship Tracker 
templates directory holds all  HTML files 
static directory holds 2 directories client and images
Client is used to store each user's pdfs upon upload 
Images stores the images we used for our favicon and our internships page 

This general structure is repeated for the branches, with some minor exceptions, such as with the Docker branch containing dockerfiles that should not be present elsewhere 
