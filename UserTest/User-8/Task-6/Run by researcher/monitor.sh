#!/bin/bash

# Path to the backup script
SCRIPT_DIR=$(dirname "$0")

# Path to the backup script relative to the current script
BACKUP_SCRIPT_PATH="$SCRIPT_DIR/backup_script.sh"

# Function to check if the backup script is running
check_and_restart_script() {
  while true; do
    # Check if backup_script.sh is running
    if ! pgrep -f "$BACKUP_SCRIPT_PATH" > /dev/null; then
      echo "backup_script.sh is not running. Restarting after 3 minutes..."
      # Wait for 3 minutes
      sleep 180
      # Restart the backup script
      bash "$BACKUP_SCRIPT_PATH" &
    fi
    # Check every minute
    sleep 60
  done
}

# Start the monitoring function
check_and_restart_script
