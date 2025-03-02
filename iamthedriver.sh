#!/bin/bash

# Ubuntu command
command="uname -a"

# Execute command and store result
result=$(eval $command)

# Convert result to hexadecimal
hex_output=$(echo -n "$result" | xxd -g 1 -u)

# Display results in columns
echo -e "Ubuntu Command:\n$command\n"
echo -e "Ubuntu Command Result:\n$result\n"
echo -e "Hexadecimal Representation:\n$hex_output\n"

# Display in columns
echo -e "il y a une un hacker dans la gare"
echo -e "Ubuntu Command\t\t\tUbuntu Command Result\t\t\tHexadecimal Representation"
echo -e "$command\t$result\t$(echo -n "$result" | xxd -g 1 -u | awk '{print $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17}')"
echol -e "i am the driver"
