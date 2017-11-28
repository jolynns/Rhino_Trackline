@ECHO OFF
REM Runs the create Rhino_TracklineAaB.py python script
REM This script takes three options
REM -i is the name of the input csv file < somefile.csv >
REM -o is the name of the output shape file < somefile.shp >
REM -w is the workspce where the input and output files reside < C:\\path\\to\\files\\ >

ECHO running Rhino_Tracks

C:\Python27\ArcGIS10.4\python.exe C:\GIS\Python\Rhino_TracklineAaB.py -i RhinoObservations.csv -o rhinoTracks.shp -w C:\\Users\\jolynn\\Documents\\GIS\\GEOG_485\\Lesson4\\

ECHO Rhino_Track has finished running
PAUSE