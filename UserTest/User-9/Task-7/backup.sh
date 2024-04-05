#!/bin/bash

current_date=$(date +%Y-%m-%d)
zip -r "${current_date}_project_data.zip" project_data
