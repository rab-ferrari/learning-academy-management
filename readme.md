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
