#!/bin/sh
flag_file="/app/output/processing_done.flag"

echo "Waiting for processing to complete..."
while [ ! -f "$flag_file" ]; do
    sleep 1
done
echo "Processing completed. Starting analysis..."