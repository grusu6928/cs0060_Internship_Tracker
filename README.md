# cs0060_Internship_Tracker
Docker Readme: 
1. Create Dockerfile with requirements.txt as is done in this directory
2. Create a docker image: 
docker image build -t internship_tracker:0.1 .
3. run the image: 
docker run --name internship_tracker -p 5000:5000 -e APP_SECRET='test' --rm internship_tracker:0.1
