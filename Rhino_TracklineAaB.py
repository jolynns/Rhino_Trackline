#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      jolynn
#
# Created:     28/11/2016
# Copyright:   (c) jolynn 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
def main():
# Set up our basic environment
    import arcpy
    import csv
    import sys, getopt
    arcpy.env.overwriteOutput = True

# get input from command line
    inFile = ''
    polylineFC = ''
    workPath = ''
    Usage = 'Rhino_TracklineAaB.py -i <input CSV File> -o <output Shape file> -w <workspace path>'
# make sure you have the right number of args
    if len(sys.argv) < 7:
        print Usage
        sys.exit()
# gather the args and assign them
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:o:w:")
    except getopt.GetoptError:
        print Usage
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-i"):
            inFile = arg
        elif opt in ("-o"):
            polylineFC = arg
        elif opt in ("-w"):
            workPath = arg

# Define variables for making our shape file
    arcpy.env.workspace = workPath
    geometry = "POLYLINE"
    spatialRef = "4326" # for WGS_1984

# Create a new shapefile and add a name field
    try:
        arcpy.CreateFeatureclass_management(workPath, polylineFC, geometry, spatial_reference = spatialRef)
        arcpy.AddField_management(polylineFC, "NAME", "TEXT", field_length=25)
    except:
        print "error trying to create the feature class %s" % polylineFC

# Define the file we will be reading
    try:
        rhinoTrack = open(workPath + inFile, "r")
    except:
        print "unable to open %s" % inFile

# Set up CSV reader and process the header
    try:
        csvReader = csv.reader(rhinoTrack)
        header = csvReader.next()
        latIndex = header.index("Y")
        lonIndex = header.index("X")
        nameIndex = header.index("Rhino")
    except:
        print "error getting header information from %s" % inFile

# Create an empty dictionary
    rhinoDict = {}

# Loop through the lines in the file and get each coordinate and name
    for row in csvReader:
        try:
            lat = row[latIndex]
            lon = row[lonIndex]
            name = row[nameIndex]

        # Make a point from the coordinates
            rhinoPnt = arcpy.Point(lon,lat)
        except:
            print "unable to make point from coordinates"

        try:
        # check for name in ditionary and append points if it is there
            if name in rhinoDict:
                rhinoDict[name].append( rhinoPnt )
        # if not there create empty array and then append points
            else:
                rhinoDict[name] = arcpy.Array()
                rhinoDict[name].append( rhinoPnt )
        except:
            print "unable to update dictionary with new point"

# Write the array to the feature class as a polyline feature and include name
    try:
        with arcpy.da.InsertCursor(polylineFC, ("SHAPE@", 'NAME')) as cursor:
            allRhinos = rhinoDict.items()
            for rhino, rhinoPL in allRhinos:
                polyline = arcpy.Polyline(rhinoPL, spatialRef)
                cursor.insertRow((polyline, rhino))
    except:
        print "unable to update cursor for %s" % polylineFC

if __name__ == '__main__':
    main()
