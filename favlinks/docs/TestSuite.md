# Test Suite

The Django application comes with the test suite to validate the implementation of business requirements.

```
python manage.py test
```

## favlinks/weblink/tests.py

### 1. User Registration

- the user register to the FavLinks site via a registration form.

UserAccountTestCase is the test class for user registration, login, password reset, etc.

### 2. User Login

- user must authenticate with the site to access his/her content.
- manage my account and favorited URLs.

Obtain JWT token. Use OAuth2.

AppAuthenTestCase - test the authentication method
ManageMyAccountTestCase - test the account management


### 3. Add Favorite URL

- logged-in user can add a new URL to the favorite list.
- the URL has attribute category and tags.
- user can organize web links in his collection.
- the system fetch and display webpage title for the URL automatically.
- when the link is bookmarked successfully there is a response or an indicator.


### 4. Manage Favorite URL

- user can edit details of the URLs in the list.
- user can delete a URL from the list.

### 5. Manage Category and Tag

- user can categorize and tag URLs
- user can see and search for the tag and category.

### 6. Search and Filter Favorites

- using title, URL, category, tags, and timestamp to find a link added to the list.

### 7. URL Validity Check

- the system can periotically check the validity of the URLs in a favorite list.
- invalid of inaccessible URLs should be marked or highlighted.

### 8. Synchronization between User Actions and URL Validity check

- make sure user action and URL validation processes does not have conflict or deadlock.


### 9. Command-Line Interface (CLI)

- provide CLI for power users to interact with the application.



