#!/bin/bash
#echo $#
#echo $(pwd)
if [ $# -eq 0 ]
   then
       python $(pwd)/src/"linked_in_api".py

elif [ $# -eq 2 ]
   then
       pwd_path=$(pwd)
       bin_path="/bin/"
       output_path="/output_files/"
       output_file_name=$2
       input_file_name=$1
       final_path_file="$pwd_path$bin_path$input_file_name"
       output_path_file="$pwd_path$output_path$output_file_name"
       echo $final_path_file
       python $(pwd)/src/linked_in_api.py $final_path_file $output_path_file

else 
    echo "Wrong Number of Arguments:The Command Should have both Input File which has the linkedin_config paramaters json file and also the output_file to store the output of the python code"
fi 
