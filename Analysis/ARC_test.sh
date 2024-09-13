#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 test_condition_file"
    exit 1
fi


# Open file containing info on the test conditions
test_condition=$1
if [ ! -e "$test_condition" ]; then
    echo "Error: File '$test_condition' not found!"
    exit 1
fi

# read steering file name used for simulations
IFS=' ' read -r steering_file detector_file < "$test_condition"
if [ ! -e "$steering_file" ]; then
    echo "Error: Steering file '$steering_file' not found!"
    exit 1
fi
echo "Steering file to be used for simulations: $steering_file"


tail -n +2 "$test_condition" | while IFS= read -r line
do
    # Skip empty lines
    if [ -z "$line" ]; then
        continue
    fi
    
    # Skip lines that start with #
    if [[ $line == \#* ]]; then
        continue
    fi

    # Overwrite steering file with test condition info and run new simulation
    read -r particle energy expect_photon <<< "$line"
    sed -i "s/^SIM.gun.particle = .*/SIM.gun.particle = "\"$particle"\"/" "$steering_file"
    sed -i "s/^SIM.gun.energy = .*/SIM.gun.energy = \""$energy"\"/" "$steering_file"
    outputFile="arc_"$particle"_"${energy/\*/}".root"
    sed -i "s/^SIM.outputFile = .*/SIM.outputFile = \"$outputFile\"/" "$steering_file"
    
    echo "Proceding to run simulation for particle '$particle' at energy '$energy'..."
    ddsim --steeringFile "$steering_file" --compactFile "$detector_file" -N 10 \
          > /dev/null
    
    # Analyze new sim with python script and check if result matches expectations
    echo "Analyze simulation results for particle '$particle' at energy '$energy'..."
    test_output=$(python ARC_test.py -f $outputFile -o Results/ARC/ --no_show)
    if [ "$test_output" != "$expect_photon" ]; then
    	echo "Error: Test failed for particle '$particle' at energy '$energy'!"
    	if [ "$expect_photon" == "True" ]; then
    	    echo "Expected photons but got nothing instead"
    	else
    	    echo "Expected no photons but some were registered"
    	fi
    else
    	echo "Test passed!"
    fi
    
    rm $outputFile 	
done 
