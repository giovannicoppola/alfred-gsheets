# alfred-sheets
 

Inspired by `I-sheet-you-not`, this Workflow provides the means to create new Workflows to access individual Google Sheets.


## Setting up 
### If the Google sheet is public
1. with the spreadsheet open in the frontmost browser, launch Alfred, enter the keyword (default: 'www') or custom hotkey. If this is a Google sheet, two options will appear: 
	1. browse the current sheet in Alfred using default settings
	2. create a new workflos for the current sheet
	
	 
2. 


1. the URL to the sheet
2. the columns to use (default: 1,2,3)
3. the title row (i.e., row with column titles, default: 1)


### If the Google sheet is private

1. Get google authentication

You can do one of three things:

1. Create a new workflow for a particular google sheet
2. in that workflow
	1. get the first three columns in alfred
	2. append a value to the main column


Set up Google Sheets API credentials:

1. Log into your Google account
1. Go to the Google Developers Console (https://console.developers.google.com/)
1. Using the 'Select a project' dropdown menu, select an existing project or create a new one.
1. Click on `ENABLE APIS AND SERVICES`, then select  `Google Sheets API` for your project. Click on `ENABLE`
1. Create credentials: From the API Console, click on `CREATE CREDENTIALS`create a new service account key
	2. select 'application data` 
	3. Are you planning to use this API with Compute Engine, Kubernetes Engine, App Engine, or Cloud Functions? No
2. download the JSON file containing your service account credentials.
1. Share the Google Sheet with the service account email address:
	- The service account email address can be found in the JSON file downloaded in the previous step. Share the Google Sheet with this email address, granting it the appropriate access permissions.

# Roadmap 🛣️
- It might be possible have all the new workflows combined in a single workflow with one cluster of objects per spreadsheet



# Icons
https://www.flaticon.com/free-icon/table-cell_6099818
https://www.flaticon.com/free-icon/add-button_8246338

- 
