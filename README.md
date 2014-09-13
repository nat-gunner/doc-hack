doc-hack
========

The goal of this project is to create a tool that will allow for diff analysis on Word documents within GitHub.

These two python scripts demonstrate how to view diffs of docx files in GitHub by comparing different versions of the xml that forms the docx files.

add-file.py instructions:
-- create a docx file
-- run add-file.py from the console
-- enter your GitHub user name and password
-- submit the full path to the docx file you created
-- write a commit message

add-file.py creates a repo with the filename of the docx file, without the extension.  It then initializes the repo by creating a README file.

Next, the script creates blobs for the docx file, unzips it into its xml components, and creates a blob for the document xml as well.

After that, the script commits the files and registers the commit with the master branch.

commit.py instructions:


NOTE: This code is for demonstration and testing purposes only.  The author makes no claims about its functionality or security, and offers no warranty covering its use.

Next Steps: 
-- Add OAuth
-- Combine scripts
-- Create GUI

