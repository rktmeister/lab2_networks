# Networks Lab 2

## Setup
Make sure you have [docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/) installed. 

Run `docker-compose up` and make sure you get "Welcome to Lab2!" by going to [http://127.0.0.1:8000](http://127.0.0.1:8000).

### Add item
The request (http://127.0.0.1:8000/add_item) uses POST to add key-value pairs into the redis database, these actions can be seen through add_item.http, add_item_2.http and add_item_3.http. If it is successful, it will return "Key value added!"

### Get item
The request (http://127.0.0.1:8000/get_item/{key}) will return the value of the key that is inside the database. If no value is found, it will return a 404 error code. If the key exists, then it will return the key-value pair in json format.

### Delete item
There are two requests (http://127.0.0.1:8000/delete_item/{key}) which is a GET request and (http://127.0.0.1:8000/delete_multiple_items) which is a POST request. 

The GET request will simply delete a key IF it exists within the database. If no key is provided then it will return a 400 error with "Please provide a key!" If a key is provided and is in the database, it will return a "Deleted key and value from database!". If not it will return a 404 response code and return the output "Key ... does not exist!"

[Challenge 1]
The POST request will take in a string which are seperated with commas. If no key is provided, code 400 with "Please provide key(s)!". If a key within the string is not found, the code will return a 404 with "Key ... does not exist!". If it succeeds, then it will delete all of the keys while returning "Deleted multiple keys and values from database!"

### Upload file
[Challenge 2]
The upload file does a POST request in the form of (http://127.0.0.1:8000/upload_file/{key}). If the request fails due to no file being placed, then it will return a 400 error with "Please provide a file!". Else, it will sucessfully set the key-value pair with the value being the content of the file itself along with "File uploaded!"