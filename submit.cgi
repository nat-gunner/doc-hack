#! /usr/bin/python

# Import modules for CGI handling  
import cgi, cgitb, requests

form = cgi.FieldStorage()

user_name = form.getvalue('user-name')

password = form.getvalue('password')

filename = form.getvalue('filename')

repo = ("https://api.github.com/users/%s/repos", user_name)

response = requests.get(repo)

assert response.status_code == 200
 
for repo in response.json():
    print '[{}] {}'.format(repo['language'], repo['name'])