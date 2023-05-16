#!/bin/bash

# Check if the first argument is --dry.
if [[ $1 == "--dry" ]]
then
    dry_run=true
    shift 1
else
    dry_run=false
fi

# Process the rest of the arguments as files or glob patterns.
for arg in "$@"
do
    # Expand the glob pattern or file name.
    for file in $arg
    do
        # Compute the SHA-256 hash of the file.
        sha256_hash=$(shasum -a 256 "$file" | awk '{print $1}')

        # Get the file extension.
        file_extension="${file##*.}"

        # If this is a dry run, print what would be done.
        if $dry_run
        then
            echo "$file -> ${sha256_hash}.$file_extension"
        else
            # Rename the file to its SHA-256 hash, preserving the file extension.
            mv -- "$file" "${sha256_hash}.$file_extension"
        fi
    done
done
