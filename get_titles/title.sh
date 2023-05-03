#!/bin/bash

# Input file name from user
read -p "Enter file name: " file

# Read file line by line
while read url; do
    # Use curl to get the page content and grep the title
    # `-o` to print only matched string,
    # `-P` to use Perl regex
    title=$(curl -s "$url" | grep -oP '(?<=<title>).*?(?=</title>)')

    # Print the title
    echo "Title of $url is: $title"
done < "$file"
