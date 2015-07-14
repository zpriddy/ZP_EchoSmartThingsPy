
# EchoSmartThingsPy
A python based API for integrating the Amazon Echo to SmartThings


## Requirements and setup

### Setting Up Alexa Skills Kit on Amazon

The ASK is available at: https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/getting-started-guide 

2. Sign in or Create an Account. 
2. Go to Apps & Services at the top of the page
2. Click on Alexa
2. Click Add New Skill
2. Fill out the first form:
    * Name: Anything you want it to be - I use SmartThings Control
    * Invocation Name: The hotword to call the app - I have gotten it working with Smart Things
    * Version: 1.0 <- This is hard-coded for now
    * Endpoint: https://alexa.zpriddy.com/alexa/EchoPyAPI
2. Go to the next page and copy the intentSchema.json to the Intent Schema and sampleUtterances.txt to the Sample Utterances
    *  Note: We are going to come back here an update this file in a few minutes. So don't close the window.
2. Go to the next page and select 'My development endpoint has a certificate from a trusted certificate authority (required for certification)'
### Setting Up SmartThings

##### Install the SmartApp
To get PyDash to talk to your SmartThings devices, you need to create a SmartApp that will serve as an API. Navigate to https://graph.api.smartthings.com and log in to your SmartThings IDE account. Select the **'My SmartApps'** tab, and click the **'+ New SmartApp'** button to create a new SmartApp.

Fill in the required information. The **'Name'** and **'Description'** are both required fields, but their values are not important.

Make sure to click the **'Enable OAuth in Smart App'** button to grant REST API access to the new SmartApp. Note the **'OAuth Client ID'** and **'OAuth Client Secret'**. Both will later be required by the Alexa backend to authenticate with the new SmartApp and talk to SmartThings.

Hit the **'Create'** button to get to the code editor. Replace the content of the code editor with the content of the file at: `alexa_access.groovy`

Click the **'Save'** button and then **'Publish -> For Me'**.


##First Run

At this time you will have to go to your Echo and say 'Alexa, Talk to Smart Things' (Replace Smart Things with what the Invocation Name you set). It should say that you are an unautherized Nest user and to check the card in your Echo App. Open the Echo app and look at the card there. It should give you what your UserID is.. 'amzn1.account.XXXXXXXXXXXXXXXXXX' ( This may be easier to get from your computer by going to https://echo.amazon.com)

Go to https://alexa.zpriddy.com/alexa/auth/<UserID\>/<SmartThings OAuth ClientID\>/<SmartThings OAuth ClientSecret\>

This should allow you to authorize it to control SmartThings. Login to your SmartThings account and Authorize it.. It should bring you back to the root Alexa page. 

### Improved Sample Utterances

At this time the App will be able to generate a custom list of sample utterances to give you better support in controling your devices. 

To get this list go to: https://alexa.zpriddy.com/alexa/samples/<UserID\>

Copy the text that is displayed and go back into your Amazon Developer Account. 

3. Go to Apps & Services at the top of the page
3. Click on Alexa
3. Click on Edit for your SmartThings Skill
3. Got to Interaction Model
3. Replace the text in Sample Utterances with the text you the copied. 
3. Click Save


## Have Fun! 



### Notes:



### To Do:
* Add check in time of inbound requests for security.
* Add support for Dimmers
* Add support for Hues
* Improve sample utterances
* Add better help. 

