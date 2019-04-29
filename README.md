# HTTP-Server-Client
HTTP Server implemented using Python 3, that handels GET/POST requests from either a web browser or HTTP client

## Getting Started   

### HTTP Server   

**Usage
```
# my_server [port_number]
#  sudo my_server 80
```
HTTP Server will listen on localhost port 80
***HTTP Server support both HTTP/1.0 and HTTP/1.1, its default protocol is HTTP/1.0***


### HTTP Client

**Usage**
```
# my_client [IP_addr] {port_number]
# sudo python my_client 127.0.0.1 80
```
HTTP Client will connect to the sever whose ip is 127.0.0.1 on port 80    

**GET request**

```
> GET file_name Protocol
> Get img1.jpg http/1.0
> GET index.html http/1.1
> get index.html
```
***HTTP Client's default protocol is HTTP/1.0***     


**POST request**

```
> POST file_name 
> Post file1
> post downloads/file1
```
***POST request files are encoded using multipart/form-data***     

**Close Connection**
```
> Exit
```




