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
in the root directory, we have our main.py which handles the entire logic for Internship Tracker 
In this directory is a templates directory that hosts all of our HTML files 
In the directory above the templates, we have a static directory that hosts 2 directories client and images
Client is used to store each user's pdfs upon upload 
Images stores the images we used for our favicon and our internships page 

This general structure is repeated for the branches, with some minor exceptions, such as with the Docker branch containing dockerfiles that should not be present elsewhere 
