#!/bin/bash

SCRAPE_RESULTS="congress_info_scrape_logs"

found=$(grep 'Couldnt find rep' $SCRAPE_RESULTS | wc -l)
echo "Congressional reps missing:" $found

found=$(grep 'Couldnt find photo' $SCRAPE_RESULTS | wc -l)
echo "Congressional photos missing:" $found

