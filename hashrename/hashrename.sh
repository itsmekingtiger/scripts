#!/bin/bash

DRY_RUN=0

while getopts ":d" opt; do
  case ${opt} in
    d )
      DRY_RUN=1
      ;;
    \? )
      echo "Invalid option: $OPTARG" 1>&2
      exit 1
      ;;
  esac
done
shift $((OPTIND -1))

# Check if any arguments were provided.
if [ $# -eq 0 ]
then
    echo "Usage: $0 [-d] file_or_glob_pattern ..."
    exit 1
fi

# Process the rest of the arguments as files or glob patterns.
for arg in "$@"
do
    # Expand the glob pattern or file name.
    for file in $arg
    do
        # Error handling
        if [ ! -f "$file" ]; then
            echo "File $file does not exist."
            continue
        fi

        if [ ! -r "$file" ]; then
            echo "File $file cannot be read."
            continue
        fi

        # Compute the SHA-256 hash of the file.
        sha256_hash=$(shasum -a 256 "$file" | awk '{print $1}')

        # Get the file extension.
        file_name=$(basename "$file")
        file_dir=$(dirname "$file")
        file_extension="${file_name##*.}"
        file_basename="${file_name%.*}"

        # If the file doesn't have an extension, file_extension will be the same as file_basename.
        # In that case, we don't want to append a dot after the hash.
        if [ "$file_extension" = "$file_basename" ]; then
            new_name="${file_dir}/${sha256_hash}"
        else
            new_name="${file_dir}/${sha256_hash}.${file_extension}"
        fi

        if [ -e "$new_name" ]; then
            echo "File $new_name already exists."
            continue
        fi

        # If this is a dry run, print what would be done.
        if ((DRY_RUN)); then
            echo "$file -> $new_name"
        else
            # Rename the file to its SHA-256 hash, preserving the file extension.
            mv -- "$file" "$new_name"
        fi
    done
done
