#!/bin/bash

###########################################
# Config Crew Sec Team Loadtesting Script #
###########################################

# This script is intended to be used to test various loads on the Explore California Website.
# To execute the script simply run ./Lab3LoadTest.sh from the Directory the Script is in.
# The script may be run as any user and should only need access to Siege.

# Get the IP Address to Test
read -p $'Please enter \e[34mIP Address\e[0m to Test: ' IP

# Check if Siege is Installed and Exit if not
if ! which siege
then
    printf "Siege is not installed! Try running \e[35msudo yum install siege\e[0m"
    exit 1
fi

# Main Loop
while true
do

    # Ask the User for a Load Code
    read -p $'Please select a load (M for Minimal, E for Expected, O for Overload, or Q for Quit): ' choice

    # Exit if the User Chose to Quit
    if [[ ${choice^^} == "Q" ]]
    then
        exit 0
    fi

    # Delay should Remain Constant for all Loads, 5 Seconds
    # MINIMAL LOAD: Run Siege with 50 Concurrent Users, 100 Reps
    if [[ ${choice^^} == "M" ]]
    then
        printf "Running Siege with \e[31m50\e[0m Concurrent Users, \e[35m15\e[0m Repetitions, and Under \e[34m3\e[0m Second Delay..."
        sleep 3
	siege -c 200 -r 15 -d 3 $IP
    # EXPECTED LOAD: Run Siege with 100 Concurrent Users, 100 Reps
    elif [[ ${choice^^} == "E" ]]
    then
        printf "Running Siege with \e[31m300\e[0m Concurrent Users, \e[35m15\e[0m Repetitions, and Under \e[34m3\e[0m Second Delay..."
        sleep 3
	siege -c 300 -r 15 -d 3 $IP
    # Less Reps for Overload to Keep Script from Taking too Long
    # OVER LOAD: Run Siege with 500 Concurrent Users, 50 Reps
    elif [[ ${choice^^} == "O" ]]
    then
        printf "Running Siege with \e[31m500\e[0m Concurrent Users, \e[35m10\e[0m Repetitions, and Under \e[34m3\e[0m Second Delay..."
        sleep 3
	siege -c 500 -r 10 -d 3 $IP
    # User Entered Invalid Code
    else
        echo "Invalid Load Choice!"
    fi
done
