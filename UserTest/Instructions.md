# Terminal Efficiency Tasks

## Easy Level Tasks

### Task 1: Create and Rename Files
- **Objective:** Execute basic file operations.
- **Instructions:**
  1. Go to `~/CS889/User-{}/Task-1`.
  2. Create a text file named `project_notes.txt`.
  3. Rename the file to `project_overview.txt`.
- **Required Commands:** `touch`, `mv`

### Task 2: Search for Text within Files
- **Objective:** Search within files for specific text.
- **Instructions:**
  1. Go to `~/CS889/User-{}/Task-2`.
  2. Using the file `~/CS889/User-{}/Task-2/server_logs.txt`, find all lines containing the word "ERROR".
  3. Display these lines on the terminal.
- **Required Commands:** `grep`

### Task 3: List Files with Specific Extensions
- **Objective:** Filter and count files of a specific type.
- **Instructions:**
  1. Go to `~/CS889/User-{}/Task-3`.
  2. List all `.py` files in the current directory.
  3. Count the number of `.py` files listed.
- **Required Commands:** `ls`, `wc`

## Medium Level Tasks

### Task 4: Batch Rename and Move Files
- **Objective:** Automate file management with batch processing.
- **Instructions:**
  1. Go to `~/CS889/User-{}/Task-4`.
  2. Rename all `.txt` files in `~/CS889/User-{}/Task-4` to `.md`.
  3. Move them to a newly created directory within `~/CS889/User-{}/Task-4` named `markdown_files`.
- **Required Commands:** `mkdir`, `mv`, Bash scripting basics

### Task 5: Extract and Process Data from a CSV File
- **Objective:** Manipulate and process data files.
- **Instructions:**
  1. Go to `~/CS889/User-{}/Task-5`.
  2. Extract all email addresses from `~/CS889/User-{}/Task-5/contacts.csv`.
  3. Save these email addresses in `~/CS889/User-{}/Task-5/emails.txt`.
- **Required Tools:** Command line text processing tools (`awk`, `sed`)

### Task 6: Find and Kill a Running Process
- **Objective:** Manage system processes.
- **Instructions:**
  1. Identify the process running `backup_script.sh`.
  2. Terminate this process.
- **Required Commands:** `ps`, `grep`, `kill`

## Hard Level Tasks

### Task 7: Create a Simple Backup Script
- **Objective:** Write scripts for automation tasks.
- **Instructions:**
  1. Go to `~/CS889/User-{}/Task-7`.
  2. Write a bash script named `backup.sh` in `~/CS889/User-{}/Task-7`.
  3. The script should zip the directory `~/CS889/User-{}/project_data` and save it with the current date as the filename.
- **Required Tools:** Bash scripting, `zip`, `date`

### Task 8: Set Up a Local Web Server and Serve a Specific File
- **Objective:** Set up and verify a simple web server.
- **Instructions:**
  1. Go to `~/CS889/User-{}/Task-8`.
  2. Serve files from `~/CS889/User-{}/Task-8/website_files` on port 8000 using Python's HTTP server module.
  3. Verify that `index.html` can be accessed through the browser.
- **Required Tools:** Python

### Task 9: Analyze and Filter Log Files
- **Objective:** Perform complex log analysis.
- **Instructions:**
  1. Analyze `~/CS889/User-{}/Task-9/access_logs.txt`.
  2. Extract requests made from a specific IP address.
  3. Count how many times a particular resource was requested.
- **Required Tools:** Text processing commands (`awk`, `sed`, `cut`)
