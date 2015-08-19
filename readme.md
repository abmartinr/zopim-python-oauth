# Oauth Python Script

Basic Script that will use the [authorization code flow](https://developer.zendesk.com/rest_api/docs/zopim/auth#implementing-an-oauth-authorization-flow-in-your-application) to connect to Zopim.

## Settings

Replace the following options with your custom Client Details and Redirect URI. If you are using it on your server just replace localhost:8080 by the server URI. Bear in mind that /handle_user_decision **must** be at the end of the URI for the script to work.

```
CLIENT_ID = ""
CLIENT_SECRET = ""
REDIRECT_URI = "http://localhost:8080/handle_user_decision"
SCOPE = "read write"
```