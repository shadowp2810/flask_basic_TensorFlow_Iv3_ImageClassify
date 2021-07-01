#### Currently Not Operational
Error to fix: json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0) <br>
# flask_basic_TensorFlow_Iv3_ImageClassify
Basic flask web api with a token limit to identify object in image using TensorFlow inception_v3 model as one service, and MongoDB db store as another service. Services managed by Docker.
<br><br>
#### To build and run all services
First we make sure Docker is running or will recieve an error <br>
`docker-compose build` <br>
To run the container <br>
`docker-compose up` <br> <br> <br>

## Notes:
### Note for flask:
On terminal when we hit `flask run`, it sets up a web server for us at local IP 127.0.0.1 and listens on port 5000.<br>
Status code 200 is ok and 404 is not found. We specify custom status codes to return to know the execution scenario we are in.<br>

Resource: What your offering eg: &nbsp; +, &nbsp; -, &nbsp; *, &nbsp; / <br>
Method: GET POST PUT DELETE <br>
Path: Where Resource is located <br>
used for: Description of what Method is going to do <br>
Param: The paramaters that the Path is expecting <br>
on error: the status codes based on user requests <br>

#### Resource Method Chart
| Resource | Method | Path | Used For | Param | On Error |
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| + | POST | /add | adding 2 nums | x:int,y:int | 200 ok, 301 missing argument |
| - | POST | /subtract | subtracting 2 nums | x:int,y:int | 200 ok, 301 missing argument |
| / | POST | /divide | dividing 2 nums | x:int,y:int | 200 ok, 301 missing argument, 302 y is zero |
| * | POST | /multiply | multiply 2 nums | x:int,y:int | 200 ok, 301 missing argument |


Registration of a user <br>
Classify a downloaded image from the web <br>
Refill tokens <br>

Resource <br>
Address <br>
Protocol <br>
Param <br>
Response and Status codes <br>

| Resource | Address | Protocol | Param | Response and Status codes |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| Register User | /register | POST | username:str,pasword:str | 200 ok, 301 invalid username |
| Classify Image | /classify | POST | username:str,pasword:str,url:str | 200 ok, 301 invalid username, 302 invalid password, 303 out of tokens |
| Refill Tokens | /refill | POST | username:str,refillPasword:str,refillAmount:int | 200 ok, 301 invalid username, 304 invalid refillPassword |



### Note to Dockerise Flask and Mongo services:
Navigate to folder with flask python app. <br>
`sudo !!` to run previous command with sudo permissions if you need it <br>
Create a "web" folder for the server or flask app. `mkdir web` <br>
Create a "db" folder for the database. `mkdir db` <br>
Copy the server file into "web" folder. `cp ../app.py` <br>
In the 'web' folder run run `Docker touch` to make a docker file. <br>
Then run `touch requirements.txt` to make requirements.txt file. <br>
In the 'db' folder run run `Docker touch` to make a docker file. <br>

#### In the Dockerfile in web directory <br>
' <br>
FROM python:3  <br>
WORKDIR /usr/src/app <br>
COPY requirements.txt . <br>
RUN pip3 install --no-cache-dir -r requirements.txt <br>
COPY . . <br>
RUN pip3 install ./en_core_web_sm-3.0.0.tar.gz <br>
CMD ["python3", "imgClassify.py"] <br>
' <br>


#### In the requirements.txt file <br>
' <br>
Flask <br>
flask_restful <br>
pymongo <br>
bcrypt <br>
spacy <br>
' <br>

#### In the Dockerfile in db directory <br>
' <br>
FROM mongo:`<VERSION-NO>` <br>
' <br> <br>

#### In the directory containing seach of the services 'web', 'db' 
We make a docker-compose file to control each container <br>
`touch docker-compose.yml` <br>
And in that file we write <br>
' <br>
version: '3' <br>
services: <br>
&emsp; web: <br>
&emsp; &emsp; build: ./web <br>
&emsp; ports: <br>
&emsp; &emsp; - "5000:5000" <br>
&emsp; db: <br>
&emsp; &emsp; build: ./db <br>
' <br>

#### Upon finalization of changes to the docker files or app files we build and run all services
First we make sure Docker is running or will recieve an error <br>
`docker-compose build` <br>
To run the container <br>
`docker-compose up` <br>

### When trying to run locally on localhost:5000 and there is already an app runnin on that port: <br>
To find what's running on port 5000: <br>
`sudo lsof -i :5000` <br><br>
To kill it <br>
`kill -9 <pid>` <br>
<br>

### Note for Mongodb:
_id is a 12 bytes hexadecimal number which assumes the uniqueness of every document. <br>
You can provide _id while inserting the document.   <br>
If you don't provide then Mongodb provides a unique id for every document. <br>
The 12 bytes of _id: <br>
- 4 bytes of current stamp <br>
- Next 3 of machine id <br>
- Next 2 of process id of mongodb server <br>
- Last 3 are incremental value <br> <br>

To have launchd start mongodb/brew/mongodb-community now and restart at login: <br>
&emsp;`brew services start mongodb/brew/mongodb-community` <br>
  or <br>
&emsp;`brew services start mongodb-community@<Version-No>` <br> <br>
If you don't want/need a background service you can just run: <br>
&emsp;`mongod --config /usr/local/etc/mongod.conf` <br> <br>

`mongo` to run mongodb <br>
&emsp;`db.help()` in the `mongo` shell to see all possible commands <br> <br>

Creating a DB: <br>
`use <NAME-OF-DB>` <br>
To check the current selected DB: <br>
`db` <br>
List of all DB:  <br>
`show dbs` <br>
`use <DB-NAME>` to select that DB to use. <br>
If not present in list you need to have atleast one document in DB. <br>
`db.dropDatabase()` to drop existing selected database <br> <br>

`db.createCollection(<NAME>, <OPTIONS>)` to create collection <br>
eg: `db.createCollection("mycol", { capped: true, size: 3, max: 3 })` <br>
`show collections` to show collections <br>
Inserting a document into a collection eg: `db.mycol.insert({"name" : "magicalCollection"})` <br>
For multiple document insertion into a collection `db.mycol.insert([{}, {}, {}, {}])` <br>
`db.<COLLECTION-NAME>.drop()` to delete collection <br> <br>

`db.COLLECTION_NAME.find({}).preety()` to query documents <br>
eg: db.mycol.find({$and:[{"likes":{$gte:50}}, {"title":"MongoDB Overview"}]}).preety() <br>
eg: db.mycol.find({$and:[{"likes":{$gte:50}}, {"likes":{$let:100}}]}).preety() <br>

update() looks for the value and does an in place update. <br>
save() replaces the entire document. <br>
`db.<COLLECTION_NAME>.update(<SELECTION-CRITERIA>,<UPDATED-DATA>)` <br>
eg: `db.mycol.update({'title':'MongoDB Overview'},{$set:{'title':'New MongoDB}})` <br>
By default MongoDB will only update a single document, to update all documents, <br>
eg: `db.mycol.update({'title':'MongoDB Overview'},{$set:{'title':'New MongoDB}},{multi:true})` <br>
To remove a document in a collection: `db.mycol.remove({"title":"MongoDB Overview})` <br><br>

Projection is to select necessary data in a document in a collection. 1 to show and 0 to not. <br>
eg of documents in a collection:  <br>
&emsp; {"_id":ObjectId(598783248985601dfd3),"title":"MongoDB Overview"} <br>
&emsp; {"_id":ObjectId(598783248985601dfd4),"title":"NOSQL Overview"} <br>
`db.mycol.find({},{"title":1,_id:0}).limit(1)` shows {"title":"MongoDB Overview"} <br> <br>

MongoDB sort() medthod to return documents in a collection in accending 1 or decending -1 order. <br>
eg: `db.COLLECTION_NAME.find().sort({"likes":1})` to sort the key "likes" in accending order. <br>
