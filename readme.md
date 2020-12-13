# FIT Tech Learning Academy - Course Management Interface
This application aims to automate several manual operations performed by FIT staff regarding the management and preparation of Tech Academy courses. It runs entirely on Python 3+ and makes use of several 3rd party APIs to perform operations on external services.

# Requirements
- Windows or Windows Server operating system
- Python 3+
- Python packages defined in the requirements.txt file

# External APIs
- MS Graph - O365 modularization package https://github.com/O365/python-o365
- account configurations on the Microsoft Azure portal https://portal.azure.com/
- Sympla https://developers.sympla.com.br/api-doc/index.html

# Maintenance and Development
Some tips to facilitate the application maintenance and development:
- The main executed script is located at /src/app.py. It initializes several assistance objects to the execution and calls the common.engine.Engine.run() method to initialize all module operations
- Credentials and other secrets must be stored on a .ini file and its path must be passed to the -secrets paremeter
- Each task module is located in the auto.module package. These modules can be called individually by using the application input parameters
- Some complete execution flows have been defined in the assets/flows.json file. These can be also called via input parameters
- Most of the common tools such as logging, API access and main engine are implemented in the common package

## Adding a new module
To perform new simple operations, the developer must:
- Add a new module entry in the assets/modules_auto.json file
- Add the module itself in the auto.module package
- Check if a generalized implementation ins't already available in the auto.module.generic modules

## Key Features for Production Release

### Embedded Sympla monitoring and Event Registering
- Add to the monitoring flow a module that will look for new events in Sympla and automatically register new ones in the database
- Use the event URL as a cross-system unique identifier
- Use the Sympla event description or some other editable field to add the other required information to be parsed and added to the local database (teacher name+email, capacity, art, description)
- Update the poller.py script so it will need only to retrieve the desired flow to be executed from the email content
- Add check on the event creation to only update the event data if it already exists - for future events only

### Email Lists and Whitelist Configuration
- For the pre-release any email can trigger the system reports - only a select whitelist - such as the adm list - should be able to trigger such events

### Production Configuration
Some key steps to correctly configure the production environment release:
- Add a new \[prod\] section to the assets/config.ini and assets/secrets.ini files
- Request with Flex global team a Microsoft service email account either @flex.com or @fit-tecnologia.org.br to be used as the "email bot"
- Configure the API key and services on the Microsoft Azure portal for account user read and offline access, email read/write and calendar read/write (follow configuration instructions on https://pypi.org/project/O365/)
- Retrieve the Sympla API key for the production account
- Update a local secrets.ini file with all secrets on a new \[prod\] section and put it on the src/persistent/ directory on the production server
- Configure the production job on a Jenkins server - similar to the DEV "Poller" job already configured

## Missing features for complete event management flow automation
To completely automate the possible monitoring flow without using any additional technologies (scripts or executables in other languages), only the Zoom operations need to be analyzed:
- Integrate the Zoom API usage with two modules:
  - auto.module.CreateZoomEvent: To be executed before the "CreateEmailEvent" module - for each "zoom unscheduled" meeting, create a new Zoom event, add the teacher as host and update the "location" field in the Database
  - auto.module.CreateEmailEvent: Add the Zoom URL as the Microsoft Calendar location (line 82)

The only required missing operation in the main flow should be to automatically remove the declined or pending users from the Sympla event - since the Sympla API does not allow any "write" operations (eg. removing participants or creating events).

A plausible option would be to:
- Add a module that generates a csv/excel file with fields ("event_url", "participant_email_to_remove") and stores it locally when a given time constraint is achieved (eg. 8 days before the event)
- Add a module that makes an external call to a RPA UI solution that takes the generated csv/excel file as input and removes these emails as participants from the given event (and deletes the file after its done)
- Add both new modules to the monitoring flow "MonitorEventStatus"
The current monitoring flow would then automatically remove the participants, send a notification email to the adm list and event to the Flex communications list so the remaining open spots can be advertised.

If this external RPA solutions isn't added, the remaining activities for the event manager would only be:
- Receive an automated notification 7 or 8 days before the event begins with the list of declined/pending participants
- Access the Sympla UI and remove the those participants
The existing solution will take these changes into account and update the Calendar event accordingly (and notify the Flex communications team).
