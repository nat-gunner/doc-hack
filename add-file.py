# Copyright 2014 Kevin Fayle
# See README for details

#! /usr/bin/python

# Import modules   
import requests, getpass, json, zipfile, base64, ntpath

api_root = "https://api.github.com"

# Get basic GitHub authentication info

user_name = raw_input("GitHub User Name: ")
password = getpass.getpass()


# Check credentials

login = requests.get(api_root + '/user', auth=(user_name, password))
assert login.status_code == 200
print "Login accepted!"

# Get the path and filename for the docx file

path = raw_input("What's the path to the docx file (including filename)?: ")
cmt_msg = raw_input("What's the commit message?: ")
# xml_msg = raw_input("What's the commit message for the xml?: ")
filename = ntpath.basename(path)
repo_name = filename[:-5]

# Create a new repository

repo_attr = json.dumps({'name':repo_name})
repo_new = requests.post(api_root + "/user/repos", repo_attr, auth=(user_name, password))

# Check results

if repo_new.status_code == 201:
	print "Repo created!"
else:
	print repo_new.status_code

assert repo_new.status_code == 201

# Initialize the repo

b64rm = base64.b64encode('Placeholder REAME file.')

rm_api = api_root + "/repos/%s/%s/contents/README.md" % (user_name, repo_name)
rm_attr = json.dumps({'message':'initialized', 'content':b64rm})
rm_add = requests.put(rm_api, rm_attr, auth=(user_name, password))

if rm_add.status_code == 201:
	print "Repo initialized!"

else:
	print rm_add.status_code

assert rm_add.status_code == 201

# Get the info for the repo head

head_api = api_root +  "/repos/%s/%s/git/refs/heads/master" % (user_name, repo_name)
head_get = requests.get(head_api)
head_json = json.loads(head_get.text)
head_sha = head_json['object']['sha']
head_url = head_json['object']['url']

# Get the sha and tree info for the latest commit

lastcmt_api = api_root + "/repos/%s/%s/commits" % (user_name, repo_name)
lastcmt_get = requests.get(lastcmt_api)
lastcmt_json = json.loads(lastcmt_get.text)
lastcmt_sha = lastcmt_json[0]['sha']
lastcmt_tree_sha = lastcmt_json[0]['commit']['tree']['sha']
lastcmt_tree_url = lastcmt_json[0]['commit']['tree']['url']

# Read the docx file and convert it to base 64, Github's required encoding

docx = open(path, "rb") # "rb" opens the file in binary mode
binary = docx.read()
docx.close()
b64doc = base64.b64encode(binary)

# Extract the xml files by unzipping the docx, reformat xml for readability

unzipped = zipfile.ZipFile(path)
docx_xml = unzipped.read('word/document.xml')
clean_xml = docx_xml.replace('><', '>\n<')
unzipped.close()

# Convert the xml from unicode to base 64

b64xml = base64.b64encode(clean_xml)

# Create a new docx blob

blob_api = api_root + "/repos/%s/%s/git/blobs" % (user_name, repo_name)

docxblob_attr = json.dumps({'content':b64doc, 'encoding':'base64'})
docxblob_post = requests.post(blob_api, docxblob_attr, auth=(user_name, password))
docxblob_json = json.loads(docxblob_post.text)
docxblob_sha = docxblob_json['sha']

# Create a new xml blob

xmlblob_attr = json.dumps({'content':b64xml, 'encoding':'base64'})
xmlblob_post = requests.post(blob_api, xmlblob_attr, auth=(user_name, password))
xmlblob_json = json.loads(xmlblob_post.text)
xmlblob_sha = xmlblob_json['sha']

# Create new tree with the commit contents

new_tree_api = api_root + "/repos/%s/%s/git/trees" % (user_name, repo_name)
new_tree_attr = json.dumps({'base_tree':lastcmt_tree_sha, 'tree':[{'path':filename, 'mode': "100644", 'type':"blob", 'sha':docxblob_sha}, {'path':'document.xml', 'mode': "100644", 'type':"blob", 'sha':xmlblob_sha}]})
new_tree_post = requests.post(new_tree_api, data=new_tree_attr, auth=(user_name, password))
assert new_tree_post.status_code == 201

# Get sha of new tree

new_tree_json = json.loads(new_tree_post.text)
new_tree_sha = new_tree_json['sha']

# Commit the new file

newcmt_api = api_root + "/repos/%s/%s/git/commits" % (user_name, repo_name)
newcmt_attr = json.dumps({'parents':[lastcmt_sha], 'tree':new_tree_sha, 'message': cmt_msg})
newcmt_post = requests.post(newcmt_api, newcmt_attr, auth=(user_name, password))
assert newcmt_post.status_code == 201

# Retrieve the new commit information

newcmt_json = json.loads(newcmt_post.text)
newcmt_sha = newcmt_json['sha']

# Update the master head with the new commit sha

master_api = api_root + "/repos/%s/%s/git/refs/heads/master" % (user_name, repo_name)
master_attr = json.dumps({'sha':newcmt_sha})
master_patch = requests.patch(master_api, master_attr, auth=(user_name, password))
assert master_patch.status_code == 200

print "File added to repository!"

