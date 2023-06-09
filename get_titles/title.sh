#!/bin/bash

# Input file name from user
read -p "Enter file name: " file

# Read file line by line
while read url; do
    # Use curl to get the page content and grep the title
    #
    # description:
    #     `-o` to print only matched string,
    #     `-P` to use Perl regex
    #
    #     `'(?<=<title>).*?(?=</title>)'` to extract content from `title` tag.
    #         - `(?<=<title>)`: Find string that just after `<title>`, use Positive Lookbehind.
    #         - `(?=</title>)`: Find string that just before`</title>`, use Positive Lookahead.
    title=$(curl -s "$url" | grep -oP '(?<=<title>).*?(?=</title>)')

    # Print the title
    echo "$url - $title"
done < "$file"
