# The MCMerl Api

This project is an (unofficial) API wrapper for the "Minecraft Support Virtual Agent", also known as Merl. 

**Link to project:** PLACEHOLDER HERE
**Link to the original Minecraft website** https://help.minecraft.net/hc/en-us

## How It's Made:

**Tech used:** Python (version 3.13.2), Requests, Postman

I found the API calls used for Merl on the Minecraft website. Then, after analyzing them on Postman, I created scripts to call these endpoints, found in the 'api.py' file. The first endpoint initializes the conversation with Merl, and returns credentials to use in the second endpoint. The second endpoint allows you to prompt Merl with a question. Instead of returning raw json data, I created several dataclasses to store it, found in the 'datamodels' package. The 'Session' class, found in 'session.py', is the intended way for developers to use this api. It allows you to create a session and prompt away, without making you worry about updating the etag.

