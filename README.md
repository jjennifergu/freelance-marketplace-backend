# freelance-marketplace-backend

**Circus**
*Welcome to the Circus, you clown 🤡*
*Connecting you with on campus freelancers.*
At the Circus, where Cornell students can post and purchase any jobs they would like to do or be done. For example, a user can offer a haircut for $25 and another user could purchase that service. The gig industry has become exceptionally popular in recent times with the rise of companies such as Uber, Lyft, DoorDash, Fiverr, and such, and we hope to bring this to Cornell.

**Description**
We wrote routes to implement creating, editing, removing, purchasing, and getting listings, only accessible to users who are authenticated. Furthermore, related to users, we wrote routes to create, edit, and getting users (accounts). Authentication is used throughout. To make things easier, we also implemented different ways to getting specific users as well, by session_token, and by username.

We maintain a Users table and a Listings table. A user could be a seller or a buyer. A seller has a one-to-many relationship with listings, as a listing can only have one seller. A buyer has a many-to-many relationship with listings, as a listing could be purchased by multiple buyers and a buyer can purchase multiple listings. Our association table enables the many-to-many relationship. With these relationships established we are also able to allow users to purchase listings as well. 

**The Frontend**
https://github.com/bonytoni/freelance-marketplace-frontend

**User Flow**
*Login*
Opening the app, you are met with a signup or login page. Input your basic information, sign in, and you will be taken to the home page.

*Hompage*
In the homepage, you will see all the listings that you or other users have posted. Each listing is a freelance service with a picture, 


*User Profile*
On the user profile, you can see your profile and the listings you are selling.


*Purchase History*
On another tab on the user profile, you can see your past purchases in case you want to purchase them again.


**Requirements**
At least 4 routes (1 must be GET, 1 must be POST, 1 must be DELETE)

At least 2 tables in database with a relationship between them

API specification explaining each implemented route

Implementation of images and/or authentication (only 1 required)
Authentication is used. Look at the code if you don't believe us. Images are used too in the profile pictures and listing images!


**The Team**
Clara Lee: Product Designer
Jennifer Gu: Full Stack Developer
Tony Chen: Frontend Developer
Benjamin Tang: Backend Developer
Lily Pham: Backend Developer




App Name
App Tagline: short one-liner description of your app


Link(s) to any other public GitHub repo(s) of your app. If you have one repo for iOS / Android and one for Backend, please link to your backend repo in your iOS / Android README, and your iOS / Android repo in your backend README.

Some screenshots of your app (highlight important features)
A short description of your app (its purpose and features)
A list of how your app addresses each of the requirements
Anything else you want your grader to know
Note: The link, screenshots, and description will be used for the Hack Challenge website where we will showcase everyone’s final projects
