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

## Idempotent routes
Idempotency as defined by Mozilla MDN Web Docs:

"*An HTTP method is idempotent if the intended effect on the server of making a single request is the same as the effect of making several identical requests.*

*This does not necessarily mean that the request does not have any unique side effects: for example, the server may log every request with the time it was received. Idempotency only applies to effects intended by the client: for example, a POST request intends to send data to the server, or a DELETE request intends to delete a resource on the server*.

All ***safe methods are idempotent***, as well as PUT and DELETE. The ***POST method is not idempotent***."

This means the idempotent routes are those that implement safe methods such as **GET** and **DELETE**. This includes (http://127.0.0.1:8000/get_item/{key}), (http://127.0.0.1:8000/delete_item/{key}), and (http://127.0.0.1:8000/list_of_items)

The reason for this is for both (/get_item/{key}) and (/list_of_items) are both GET requests and they do not change the state of the server.

For (/delete_item/{key}) this is safe as when sending the same delete request e.g. (/delete_item/orange), the server will only delete **IF** the item exists within the database.


