Welcome to Url data extractor project

Used Python and pip Version

python 3.8


### Installation

Please use the following command to install the dependencies
pip install -r requirements.txt
```
pip install -r requirements.txt

```


### Usage

Please run the following command to run the application
```
python application.py

```
Application will run in localhost:8000 

This application will open the rest endpoint for recieving the
url. Please use POST method to send an url to the application
 
Below example will post an url to the application

```
curl -d "http://www.google.com" -X POST http://localhost:8000/url/
```