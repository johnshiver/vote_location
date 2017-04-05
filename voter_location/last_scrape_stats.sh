#!/bin/bash

SCRAPE_RESULTS="congress_info_scrape_logs"

echo "running congressional district test scrape"

START=$(date +%s.%N)
python manage.py scrape_congressional_district_information --test_run > $SCRAPE_RESULTS
END=$(date +%s.%N)
DIFF=$(echo "Scrape took $END - $START" | bc)
echo $DIFF


echo "Running district url stats"
START=$(date +%s.%N)
python manage.py report_district_url_stats >> $SCRAPE_RESULTS
END=$(date +%s.%N)
DIFF=$(echo "Urls took $END - $START" | bc)
echo $DIFF

echo "Running phone number scrape"
START=$(date +%s.%N)
python manage.py scrape_office_phone_number --test_run >> $SCRAPE_RESULTS
END=$(date +%s.%N)
DIFF=$(echo "Phones took $END - $START" | bc)
echo $DIFF

echo "Finished scrape test!"
cat $SCRAPE_RESULTS
