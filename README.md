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
