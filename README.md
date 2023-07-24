# alfred-sheets
 

Inspired by `I-sheet-you-not` this Workflow provides the means to create new Workflows to access individual Google Sheets.

- If the Google sheet is public, you need
	1. the link to the sheet
	2. the columns to use (default: 1,2,3)
	3. the title row (default: 1)

Get google authentication

You can do one of three things:

1. Create a new workflow for a particular google sheet
2. in that workflow
	1. get the first three columns in alfred
	2. append a value to the main column


Set up Google Sheets API credentials:

Go to the Google Developers Console (https://console.developers.google.com/).
Create a new project or use an existing one.
Enable the Google Sheets API for your project.
Create credentials: From the API Console, create a new service account key and download the JSON file containing your service account credentials.
Share the Google Sheet with the service account email address:
The service account email address can be found in the JSON file downloaded in the previous step. Share the Google Sheet with this email address, granting it the appropriate access permissions.



# Icons
https://www.flaticon.com/free-icon/table-cell_6099818
https://www.flaticon.com/free-icon/add-button_8246338