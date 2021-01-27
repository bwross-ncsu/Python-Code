# ---------------------------------------------------------------------------
# ListStreetRanges.py
# Created on 1/27/2021
# Usage:
# - Only change the dataset variables to get it to run
# - Dataset variables are captalization sensitive
# - This is for 2 sided ranges (Left & Right)
# - Need to ensure the low field is always lower or equal to the high field
# - Does not account for GAPS in segements
# ---------------------------------------------------------------------------
          

# Set the ArcPy Environment
import arcpy, csv

# Set Dataset Variables
streetsDataset = "C:\GIS\ProductionData\Zuercher.gdb\Addressing\Centerlines"
lowRangeLFieldName = 'FromAddr_L'
lowRangeRFieldName = 'FromAddr_R'
highRangeLFieldName = 'ToAddr_L'
highRangeRFieldName = 'ToAddr_R'
fullNameFieldName = 'LSt_FullName'
communityFieldLName = 'MSAGComm_L'
communityFieldRName = 'MSAGComm_R'
outputCSV = "C:\Temp\streets.csv"


# Script Variables Do Not Change
nameV = 0
commV = 1
lowV = 2
highV = 3
nameField = 'row.' + fullNameFieldName
lowLField = 'row.' + lowRangeLFieldName
lowRField = 'row.' + lowRangeRFieldName
highLField = 'row.' + highRangeLFieldName
highRField = 'row.' + highRangeRFieldName
commLField = 'row.' + communityFieldLName
commRField = 'row.' + communityFieldRName
ranges = {}

try:
    rows = arcpy.SearchCursor(streetsDataset)
    row = rows.next()

    while row:
        keyL = eval(nameField) + '@' + eval(commLField)
        keyR = eval(nameField) + '@' + eval(commRField)
        
        if keyL not in ranges:
            ranges[keyL] = [eval(nameField),eval(commLField),eval(lowLField),eval(highLField)]
        else:
            if (ranges[keyL][lowV] > eval(lowLField) and eval(lowLField) > 0) or (ranges[keyL][lowV] == 0 and eval(lowLField) != 0):
                ranges[keyL][lowV] = eval(lowLField)
            if ranges[keyL][highV] < eval(highLField):
                ranges[keyL][highV] = eval(highLField)

        if keyR not in ranges:
            ranges[keyR] = [eval(nameField),eval(commRField),eval(lowRField),eval(highRField)]
        else:
            if ranges[keyR][lowV] > eval(lowRField) and eval(lowRField) > 0 or (ranges[keyR][lowV] == 0 and eval(lowRField) != 0):
                ranges[keyR][lowV] = eval(lowRField)
            if ranges[keyR][highV] < eval(highRField):
                ranges[keyR][highV] = eval(highRField)
                       
        row = rows.next()

    with open(outputCSV, mode='w') as csvfile:
        fnames = ['street_name','street_community','low','high']
        writer = csv.DictWriter(csvfile, fieldnames=fnames)
        
        for keys in ranges:
            writer.writerow({'street_name' : str(ranges[keys][nameV]),'street_community' : str(ranges[keys][commV]),'low' : str(ranges[keys][lowV]),'high' : str(ranges[keys][highV])})
                            
                                 
except:
    e = sys.exc_info()[1]
    print(e.args[0])
    arcpy.AddError(e.args[0])
finally:
    print "Finished Running."
