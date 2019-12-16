# cs0060_Internship_Tracker

#### authors: jweissko, grusu, drozenb1
#### First deployment: 12/15/2019
#### Hosted currenly on URL: internship.team,
      www.internship.team

##### Instructions for local deplyment:

1. If deploying for use on the same computer, then in main.py, change 'dbserver' to 'localhost' in this line:
     app.config['MONGO_URI'] = 'mongodb://dbserver:27017/logindb'
2. Start the mongodb daemon:
    mongod
3. run the following command to runt the app:
    ./run.sh

##### Instructions for remote deployment using docker and nginx:
0. Make sure that the you have changed back 'localhost' to 'dbserver' in teh line given above in instruction 1 of local deployment
1. Create requirements.txt using capitalization for modules as is correct in the command 'pip3 install <module_name>'
2. Create Dockerfile (see our Dockerfile for an example)
3. Create docker-compose.yaml file
4. Upload the cs0060_Internship_Tracker to server (for example, by using git clone)
6. Run the following command to create the docker images: 
     docker-compose -f docker-compose.yaml build
7. Run the following command to start the docker images:
     docker-compose -f docker-compose.yaml up
8. Exec into the flask container as a root user with the following command:
     docker exec -u 0 -it <container_id> bash
9. Inside the container, go to the home directory, and change the ownership of web recursively to web:
     chown -R web:web web
   Exit the container and enter it again as the default user:
     docker exec -it <container_id> bash 
   Try creating a directory in the web directory to confirm that you have create directory permissions
10. On a web browser, go to internship.team and check that it is connecting. Try loggin in.
Errors to watch out for: 
     If you cannot log in or register, probably the application cannot access Mongo. Check that you have changed localhost to dbserver if using remote deploymen. If that doesn't fix it, then check that the Mongo container is running. 
 
