#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 8 14:44:33 2024
Based on: https://www.kaggle.com/datasets/nelgiriyewithana/top-spotify-songs-2023
Sample input: --filter="ARTIST" --value="Dua Lipa" --order_by="STREAMS" --order="ASC" --limit="6"'
@author: rivera
@author: STUDENT_ID
"""
import pandas as pd
import argparse

def getArgs():

    #Creating parser variable
    parser = argparse.ArgumentParser()

    # Getting the argument names
    parser.add_argument("--data", required=False)
    parser.add_argument("--filter", required=False)
    parser.add_argument("--value", required=False)
    parser.add_argument("--order_by", required=False)
    parser.add_argument("--order", required=False)
    parser.add_argument("--limit", required=False)


    return parser.parse_args()

def sortFile(file, order_by, order)-> list[str]:

    #Chage arg.order_by names into corresponding column names
    if (str(order_by) == "NO_SPOTIFY_PLAYLISTS"): order_by = "in_spotify_playlists"
    if (str(order_by) == "NO_APPLE_PLAYLISTS"): order_by = "in_apple_playlists"
    if (str(order_by) == "STREAMS"): order_by = "streams"

    #Check for ascending or descending order and sort appropriately
    if(str(order) == "DES"):
        sortedFile = file.sort_values(by=order_by, ascending = False)
    else:
        sortedFile = file.sort_values(by=order_by, ascending = True)

    return sortedFile

def findCols(file, colFilter, checkValue)->list[str]:

    #Change arg.filter names into corresponding column names
    if str(colFilter) == "ARTIST":
        filter_by_column = "artist(s)_name"

          #Filter the DataFrame based on the specified column and value
        filtered_data = file[file[filter_by_column].str.contains(checkValue)]


    #Change arg.filter names into corresponding column names
    if str(colFilter) == "YEAR":
        filter_by_column = "released_year"
          #Filter the DataFrame based on the specified column and value
        filtered_data = file[file[filter_by_column] == int(checkValue)]

    
    
    return filtered_data


def changeCols(file, order_by):

    # Convert the the Day, Month, and Year columns into a single column formatted properly
    file['released'] = pd.to_datetime(file['released_year'].astype(str) + '-' + file['released_month'].astype(str) + '-' + file['released_day'].astype(str))
    file['released'] = file['released'].dt.strftime('%A, %B %d, %Y')

    # Get correct order_by name
    if (str(order_by) == "NO_SPOTIFY_PLAYLISTS"): order_by = "in_spotify_playlists"
    if (str(order_by) == "NO_APPLE_PLAYLISTS"): order_by = "in_apple_playlists"
    if (str(order_by) == "STREAMS"): order_by = "streams"

    # Get rid of the non-important files in sortedFile
    sortedFile = file[['released', 'track_name', 'artist(s)_name', order_by]]

    # Remove comma after the year in the released date
    temp=[]
    for line in sortedFile['released']:
        beforeC = line.split(',',1)
        beforeC[0] = beforeC[0][:3]
        temp.append(beforeC[0] + "," + beforeC[1])
    sortedFile.loc[:,'released'] = temp

    return sortedFile


def main():
    """Main entry point of the program."""

    # Get csv file path
    csv_file_path = "data.csv"

    # Read the CSV file into a DataFrame
    file = pd.read_csv(csv_file_path)

    # Get arguments in getArgs function
    arg = getArgs()

    #Put the file in the correct order considering what it should be ordered by
    #and whether its ascending or descending
    sortedFile = sortFile(file, arg.order_by, arg.order)


    #Check if there is a filter
    if(str(arg.filter) != "None"):

        #Find the correct columns based on the filter and value
        sortedFile = findCols(sortedFile, arg.filter, arg.value)

        #Get the properly formatted date and the correct cols
        sortedFile = changeCols(sortedFile, arg.order_by)


        #Check is there is a limit
        if(str(arg.limit) != "None"): 

            #Apply the limit to the sortedFile
            sortedFile = sortedFile.iloc[0:int(arg.limit), :]

            #Put the sortedFile into output.csv
            sortedFile.to_csv("output.csv", index = False)

        
        #If no limit put file directly into output.csv
        else: sortedFile.to_csv("output.csv", index = False)


    #Runs if there is no filter
    else:

        #Get the properly formatted date and the correct cols
        sortedFile = changeCols(sortedFile, arg.order_by)


        #Check for limit
        if(str(arg.limit) != "None"): 

            #Apply limit to sortedFile
            sortedFile = sortedFile.iloc[0:int(arg.limit), :]

            #Put sortedFile into output.csv
            sortedFile.to_csv("output.csv", index = False)


        #If no limit put sortedFile directly into output.csv
        else: sortedFile.to_csv("output.csv", index = False)
        
if __name__ == '__main__':
    main()
