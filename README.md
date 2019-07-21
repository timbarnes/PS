Project Initialization Application

Implemented in Python 3

ps.py [-i | -d] [-r project_root] [-t] project_data

-i: Show informational messages
-d: Show debug messages
-r path: Change project_root (default is P:)
-t: Test mode - run the functions, but don't actually create or copy files
project_data: 2019.103%Project name%[Revit|CAD|Generic]

For example:
   python ps.py 2019.33%Citra Brewery%Revit
   ...creates a new project, set up for Revit, at location 2019.33 

  python ps.py -t 2019.202%Do not try this%Generic -d
  ...goes through the motions to create a generic project at 2019.202, 
     showing all the debug info, but doesn't actually alter the file system.