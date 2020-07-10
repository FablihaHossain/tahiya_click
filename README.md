# Tahiya Click: A Photography Site
## Developed by Fabliha Hossain

**Project Objective:** They say that a picture is worth a thousand words. The focus on this project was to develop a web application that allows photographers to share their content and their message to the world. The idea was inspired by my cousin Farhana Sufian, who introduced me to the wonders of photography.

**Welcome Page** A simple welcome page featuring my Sony a6000 Professional Camera. This is the camera I use whenever I travel to new areas or offer my friends photoshoots. 
![Scheme](application/static/images/Welcome_Page.png)

**About Page** The about page features a little description of the application as well as images of myself and my cousin holding professional cameras. Therby emphasizing that the site is for the person behind the camera. 
![Scheme](application/static/images/About_Page.png)

**Login Page** A user must log in with a valid username and password in order to access the rest of the web application. 
![Scheme](application/static/images/Login_Page.png)

**Registration Page** The registration page ensures that there are no duplicate email addresses or usernames between any two registered users. In addition to that, the application hashes the password using Flask-Hashing for security purposes. 
![Scheme](application/static/images/Registration_Page.png)

**Main Albums Page** Based on who logs in, the main albums page filters through all albums in the database. The logged in user can see their own albums on the left side, and the albums of other photographers on the right side. 
![Scheme](application/static/images/Main_Albums_Page.png)

**New Album Form** Currently, in order to create a new album in the site, it must have a unique album name and the images uploaded must have the following extensions: 'jpg', 'jpeg', 'png', 'gif'. Any other extensions will flash an error message for the form to be uploaded again. 
![Scheme](application/static/images/New_Album_Form.png)

**Update Album Form** Only album users can update their own albums. They can choose to update the name, description, and cover image of the album. They could also upload new images and delete images from the album. Security measures are implemented to redirect the user if they try to inject an album id that isn't theirs onto the site link. 
![Scheme](application/static/images/Update_Album_Form.png)

**View Album** Users can view any album they choose in full. However, the 'update album' option will only appear in the albums that they have ownership of. Otherwise, they can simply view the images by clicking on them to be enlarged. 
![Scheme](application/static/images/View_Album_Page.png)
![Scheme](application/static/images/Enlarge_Example.png)

###### Technology Decisions:
* Python Flask
* MongoDB 
* Javascript
	* Bootstrap 4.5
* HTML 


**License Info:** This work is licensed under a *Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License*
https://creativecommons.org/licenses/by-nc-nd/4.0/