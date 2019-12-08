#### Choice of Database Management System: MongoDB

##### Explanation
1.  Mongo is a lightweight database that is optimal for simple queries and transactions. For our project, we will primarily be using a database to store and retrieve user's login and internship information, and we will not be need to support fancy OLAP queries, so it makes sense for us to use Mongo, so as to reduce the overhead.
2.  Another reason we thing that using Mongo would make sense, is that we intend to have multivalues attributes for internship statuses (applied, pending, dates (deadline for applying, deadline for giving a response) and for internship's related documents, and Mongo managed multivalued attributes well with it's document oriented heirarchical structure that allows different cardinalities for the same attribute of different documents. 

#### DB schema 

##### Diagram
![image of db collections](https://i.imgur.com/TnJm4n2.png)

##### Entities (rectangles):
In this image we have three collections: User, Docs, and Internships. 

##### Relationships (diamonds): 

User relates to Internships in that each document in the internships collection has an associated field with its associated user's user_id. Thus Internship(user\_id) is like a foriegn key referencing User(\_id). Docs relates to internships in that each document in the internships collection which has associated docs has a list of doc ids with which is is associated. Thus, Internship(doc\_id) is like a foreign key referencing Docs(\_id).These relationships are represented by the diamonds and by the ovular fields connected to the diamonds. 

##### Fields (ovals): 

User has the following fields: \_id, user name, email address, and password (after being hashed). 

Docs has the following fields: \_id, name, type (i.e. resume, cover letter, other), contents (in pdf format).

Internships has the following fields: \_id, company name, internship location, position/title, notes, status (i.e. not applied, applied, accepted, rejected, expired), dates (i.e. application deadline, followup deadline)
