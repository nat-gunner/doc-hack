doc-hack
========

The goal of this project is to create a tool that will allow for diff analysis on Word documents within GitHub.

These two python scripts demonstrate how to view diffs of docx files in GitHub by comparing different versions of the xml that forms the docx files.

### Step 1

add-file.py instructions:
- create a docx file
- run add-file.py from the console
- enter your GitHub user name and password
- submit the full path to the docx file you created
- write a commit message

add-file.py creates a repo with the filename of the docx file, without the extension.  It then initializes the repo by creating a README file.

Next, the script creates blobs for the docx file, unzips it into its xml components, and creates a blob for the document xml as well.

After that, the script commits the files and registers the commit with the master branch.

### Step 2

commit.py instructions:
- make some changes to the docx file
- run commit.py from the console
- enter your GitHub user name and password
- give the name of the repo created by add-file.py in Step 1
- submit the filename (with extension) of the docx file
- enter the full path (with filename) to the new version of the docx file
- type a commit message

commit.py adds the new version of the docx file and its document xml to GitHub and commits them.

### Step 3

Go to the repository you created and click on the latest commit.  Your changes should be highlighted in the document xml.  

### Results

I ran the scripts on Mac OSX (Mavericks) with Python 2.7.5.  They successfully created a repository in GitHub, added a docx file and its document xml, and commited a new version of each file.  The differences were highlighted in the diff report for the latest commit.

The results can be seen at [this repository](https://github.com/nat-gunner/Test).

### For future development

- Add OAuth
- Combine scripts
- Create GUI
- Write a README file for the repository

NOTE: This code is for demonstration and testing purposes only.  The author makes no claims about its functionality or security, and offers no warranty covering its use.
