#!/bin/bash

# Define the directory to be backed up
directory_to_backup="./project_data"

# Define the backup destination directory
backup_destination="."

# Get the current date in YYYY-MM-DD format
current_date=$(date +%Y-%m-%d)

# Create the backup filename with the current date
backup_filename="${backup_destination}/project_data_backup_${current_date}.zip"

# Zip the directory
zip -r "$backup_filename" "$directory_to_backup"

echo "Backup of '$directory_to_backup' completed successfully as '$backup_filename'"

