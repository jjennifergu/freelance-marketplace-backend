# freelance-marketplace-backend

**App idea**

A freelancing app for Cornell students to post and purchase any jobs they would like to do. For example, a user can offer a haircut for $25 and another user could purchase that service. 

Users will have to sign in to use our app (we haven't decided whether to use Google authentication or to keep our own database yet). There will be a homepage, which will display all the listings. Each user will have a profile, which will include all of their listings and past purchases. Each listing can also be clicked open to display more details and purchase information. 

We will build GET routes for getting all the posts, displaying a user's profile, and showing a listing's details. We will have POST routes for signing up, logging in, posting a listing, and purchasing a listing. We will have a DELETE route for deleting a listing. 

Some possible route ideas to implement if we have time include a POST for editing a listing, DELETE for deleting a profile, and GET/POST for leaving reviews and displaying them. 

We will maintain a Users table and a Listings table. It will be kind of similar to PA4, where a user could be a seller or a buyer. We will have 2 association tables, one for sellers/listings and one for buyers/listings. Since a listing could have multiple buyers and a seller associated with it, the Listing model will have a one to many relationship with the User model.
