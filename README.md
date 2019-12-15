cs0060-Internship-Tracker
authors: Jweissko, Grusu, Drosen

Notes: if runnign locally, need to use localhost in this line: 
app.config['MONGO_URI'] = 'mongodb://localhost:27017/logindb'

If running on the server for remote access, then change localhost to dbserver. The result should look like this: 
app.config['MONGO_URI'] = 'mongodb://dbserver:27017/logindb'
