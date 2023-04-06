**EcoPOI**

**Alex Thompson**

***Table of Contents***
1.	Introduction
2.	Installation and Setup
3.	Usage
4.	Understanding the Output
5.	Troubleshooting and FAQ

***Introduction***
    
    EcoPOI is a Python application that utilizes the OpenStreetMap API and the OpenAI GPT-4 API to provide users with valuable information about their local environment, including flora, fauna, and nearby points of interest (POIs) related to nature.

    This documentation provides a comprehensive guide on how to set up, run, and understand the output of the EcoPOI application.

***Installation and Setup***
    
    Prerequisites
        • Python 3.6 or higher
        • API key for OpenAI GPT-4
        • Installed packages: geopy, openai, overpy, requests

    Installation
        1. Either input your own OpenAI GPT-4 API key into the api_key variable in main or create a new file named 'API_KEY.py' in the same directory as 'EcoPOI.py'. In this file, add the following line, replacing ‘your_openai_api_key’ with your actual OpenAI GPT-4 API key: 
            a.	api_key = "your_openai_api_key" 
        2. Install the required packages using pip (you may refer to 'EcoPOI_requirements'): 
            a.	pip install geopy openai overpy requests

***Usage***
    
    To run EcoPOI, either run the ‘EcoPOI.py’ file directly or navigate to the directory containing the 'EcoPOI.py' file and execute the following command in the terminal: python EcoPOI.py

    The application will prompt you to choose a method for providing your location. You can either:
        
        1.	Have EcoPOI automatically detect your location using your IP address
        2.	Manually enter a location
    
    After providing your location, the application will display relevant information about the local flora, fauna, and environment/biome at your discretion.
    
    Afterward, you will be prompted to enter a search radius (in meters) for nearby points of interest in nature with the location you provided as the center point. You can either enter a custom value or press 'Enter' to use the default value of 1609 meters (approximately 1 mile).

***Understanding the Output***
    
    The EcoPOI application generates four types of content:
        1.	Local Flora: A numbered list of the 10 most common types of flora in your area, along with a brief description of each plant type (e.g., tree, shrub, etc.).
        2.	Local Fauna: A numbered list of the 10 most common types of fauna in your area.
        3.	Local Environment: A short description of the local environment.
        4.	Nearby Nature POIs: A list of nearby points of interest related to nature, including parks, forests, beaches, and more. The list includes the name, category, and distance from your location for each POI.
    
    You can choose to print each of these content types or skip any of the first three as desired.

***Troubleshooting and FAQ***
    
    Q: I'm receiving an error when trying to run EcoPOI. What should I do?
    A: Ensure that you've installed all required packages and entered your OpenAI GPT-4 API key in the 'API_KEY.py' file or in the api_key variable in main. If the problem persists, check the error message for more information and consult this documentation or online resources for assistance.
    Q: The application isn't finding any points of interest near my location. What should I do?
    A: Try increasing the search radius. If no POIs are found within the specified radius, you might need to expand the radius to find more results.

