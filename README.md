# cs0060_Internship_Tracker
Docker Readme: 
0. Create requirements.txt with list of modules that you will need to import using pip3
1. Create Dockerfile as is done in this directory
2. Create a docker image: 
Ex. 
docker image build -t internship_tracker:0.1 .
  ~check that docker image is created by running docker images
3. run the image: 
Ex. 
docker run --name internship_tracker -p 5000:5000 -e APP_SECRET='test' --rm internship_tracker:0.1
4.  

Notes: if runnign locally, need to use localhost in this line: 
app.config['MONGO_URI'] = 'mongodb://localhost:27017/logindb'

If running on the server for remote access, then change localhost to dbserver. The result should look like this: 
app.config['MONGO_URI'] = 'mongodb://dbserver:27017/logindb'
