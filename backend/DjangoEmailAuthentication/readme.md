# Email Authentication Django + React

In this email authentication project, when a user visits the homepage of a site, if the user is not logged in then the user will sign up. 

Sign up brings up form that will take email as username (django) and password. When a user registers then an email (including a verification link) is sent to the email provided in the form.

When a user click on the email verification then the jwt-token is sent to server which decodes the token and authenticate the user. If user is authenticated then user is set to active otherwise not.