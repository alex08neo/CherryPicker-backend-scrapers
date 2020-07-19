#!/bin/bash

for py_file in $(find ./Scrapers ! -name '*Class*')
do
    python $py_file &
done

echo "Running scripts in parallel"
wait 
echo "Finished scraping"

python ./Connect-Database/MongoDB-Connection.pyY