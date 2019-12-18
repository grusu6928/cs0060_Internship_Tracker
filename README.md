# cs0060_Internship_Tracker
##### Hosted at: internship.team
##### authors: jweissko, grusu, drozenb1
##### Version 1.0 date of deployment: 12/15/2019

## Overview 
Web appliation to keep track of internship applications and associated documents.

Pages: 
1. Login/ Register
	Function: 
	* create an password protected user account or login to ecisting account
2. Internships
	Function:
	* Displays internship applications in table, color coded based on the application status (yellow = follow up, blue = no longer applicable, green = received offer, red = has not yet applied and deadline appraoching)
	* Add internships, update internships, and delete internships from table.
3. Documents
	Function:
	* Stores documents relevant to internships applications: most up-to-date job resume, generic cover letter, most-recent transcript for later downloads

### Requirements
Docker
Nginx
Mongodb
Python3 and all Python3 modules listed in requirements.txt

### Instructions for deployment:

##### Local deployment

1. If deploying for use on the same computer, then in main.py, change 'dbserver' to 'localhost' on this line:
     app.config['MONGO_URI'] = 'mongodb://dbserver:27017/logindb'
2. Start the mongodb daemon:
    mongod
3. run the following command to run the app:
    ./run.sh

##### Remote deployment (via Docker, using nginx):
1. Make sure that the line from main.py given instruction 1 of local deployment above says "dbserver" rather than "localhost"
2. Ssh into the remote server and clone the application repository from Github
3. From within the cloned repository Run the following command to create the docker images: 
     docker-compose -f docker-compose.yaml build
4. Run the following command to start the docker images:
     docker-compose -f docker-compose.yaml up
5. Exec into the flask container as a root user with the following command:
     docker exec -u 0 -it <container_id> bash
6. Inside the container, go to the home directory, and change the ownership of web recursively to web:
     chown -R web:web web
   Exit the container and enter it again as the default user:
     docker exec -it <container_id> bash 
   Try creating a directory in the web directory to confirm that you have create directory permissions
7. On a web browser, go to internship.team and check that it is connecting. Try loggin in.
Errors to watch out for: 
     If you cannot log in or register, probably the application cannot access Mongo. Check that you have changed localhost to dbserver if using remote deploymen. If that doesn't fix it, then check that the Mongo container is running. 
 
