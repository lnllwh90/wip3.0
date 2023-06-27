
mode=$1

if [ "$mode" = "ctv" ]; then

    #ilf_file_check.csv is meant to validate the files for every hour
    echo "date,hour,count" > ilf_ctv_hourly_check.csv;
    #ilf_file_check_temp.csv will create a temporary file that will eventually....
    echo "date,count" > ilf_ctv_check_temp.csv;

    for hour_dir in ctv/*; do
    #loop through the child directory, 'ctv' must be the parent
        hour="$(basename $hour_dir)";
        #a variable that will contain the hours from each file, 'last two digits'
        for file in "$hour_dir"/*.csv.gz; do
        #loops through each child directory and locates the gunzipped files within each
            date_str="$(echo "$file" | sed -E 's/.*_([0-9]{8}).*/\1/')";
            #a variable that contains the first 8 digits from each of the gunziped files,'20230522'
            formatted_date="${date_str:4:2}/${date_str:6:2}/${date_str:2:2}"
            #variable to reformat the dates. The dates under this variable to be printed to the 'ilf_file_check_temp.csv' so that it is easier to match up with the data exported from the Moat UI
            echo -n "$formatted_date,$hour," >> ilf_ctv_hourly_check.csv;
            # the -n is used to print the date and the hour on one line
            echo -n "$formatted_date," >> ilf_ctv_check_temp.csv;
            zcat "$file" | wc -l >> ilf_ctv_hourly_check.csv && zcat "$file" | wc -l >> ilf_ctv_check_temp.csv;
            # will print the row counts into each of the files for each date. This is used if an IE just wants to confirm if the counts for that date line up with the UI. Will need to account for UTC to EST time difference after connecting to s3

            #the following will run as the script that will concatenate all hourly files into one
            if [ ! -f "ilf_ctv_${date_str}.csv" ]; then
                #"DSCVRL14_DFS_MOATCTV_${date_str}.csv" is the placeholder name for now, but ideally the concatenated files will be appended to a single file with ${date_str} prepended onto each. 
                zcat "$file" | awk -v hour="$hour" 'BEGIN { FS = "," } { if (FNR == 1 && NR == 1) print $0 ",hour"; else print $0 "," hour; } ' > "ilf_ctv_${date_str}.csv";
                #the concatenated file output after the script finishes will have a column added that will contain the hour from which the row of data came from, e.g. the value stored under the hour variable. The values assigned against the hour value should be the last two digits from each of the files which represent the hour in UTC time. the script will also ignore header rows from each of the files if there is already a header row that exists in the concatenated file. 
            else
                zcat "$file" | awk -v hour="$hour" 'BEGIN { FS = "," } FNR == 1 { next; } { print $0 "," hour; }' >> "ilf_ctv_${date_str}.csv";
                #The above is the else statement in which if the header row already exists it will skip over the header row and adds a new column to each subsequent row. The new colums will contain the values from the hour variable.
            fi
            # if [ "$date_str" != "" ]; then
                #This block will be used to validate the concatenated files generated from the above.
                # echo "dkey,hour,count" > ctv_ilf_${date_str}_temp.csv
                # #the ctv_ilf_${date_str}_temp.csv file will be used to validate if the concatenated file matches with the counts from each of the hourly files stored in s3.
                # echo -n "unique_id,$formatted_date,dkey,count" > ctv_ilf_raw_count_${date_str}_temp.csv;
                #the ctv_ilf_raw_count_${date_str}_temp.csv will be used to compare with the rows captured in the UI or exported in Moat reporting. The end result will consist of a columns that contain a unique id which will be formated as (level1-level2-level3-level4-date), a date column, the dkey (the first four columns from the concatenated file(s) separated by a '-' delimeter), and a counts column which will contain unique counts for each of the rows
                # {
                    # cat "$file" | awk -F ',' '{for(i=1;i<=NF;i++) gsub(/"/,"",$i);} { printf("%s-%s-%s-%s-%s\n", $1, $2, $3, $4, $(NF))}' | sed 's/,/-/g' | sort | uniq -c | awk -F '-' '{print "\"" $1"-" $2 "-" $3 "-" $4 "-" $5 "\"," $1}' >> "ctv_ilf_${date_str}_temp.csv"
                    # cat "$file" | awk -F ',' '{for(i=1;i<=NF;i++) gsub(/"/,"",$i);} { printf("%s-%s-%s-%s\n", $1, $2, $3, $4)}' | sed 's/,/-/g' | sort | uniq -c | awk -F '-' '{print "\"" $1"-" $2 "-" $3 "-" $4 "\"," $1}' >> "ctv_ilf_raw_count_${date_str}_temp.csv"
            #         cat "$file" | awk -F ',' '{for(i=1;i<=NF;i++) gsub(/"/,"",$i);} { printf("\"%s\",\"%s\",\"%s\",\"%s\"\n", $2, $1, $3, $4 "-" $5)}' | sort | uniq -c | awk -F ',' '{print $2 "," $1}' >> "ctv_ilf_raw_count_${date_str}_temp.csv"
            #     };
            # fi;
        done;
    done;
    echo "date,count" > ilf_daily.csv;
    #may want to update to include a column that counts the number or rows removed and a second that contains the final number or rows, after concatenating the hourly files from the child directories.
    awk -F, '{count[$1]+=$2} END{for (i in count) print i "," count[i]}'  ilf_ctv_check_temp.csv >> ilf_daily.csv;
    rm -rf ilf_ctv_check_temp.csv;
fi

if [ "$mode" = "display" ]; then
    echo "date,count" > lld_display_check_temp.csv;

    for file in display/*_UTC.csv.gz;do
        date_str="$(echo "$file" | sed -E 's/.*-([0-9]{4}-[0-9]{2}-[0-9]{2}).*/\1/')";
        formatted_date="${date_str:5:2}/${date_str:8:2}/${date_str:2:2}";
        echo -n "$formatted_date," >> lld_display_check_temp.csv;
        zcat "$file" | wc -l >> lld_display_check_temp.csv;
        zcat "$file" | cut -d ',' -f 1-5 | awk -F ',' '{if ($5 ~ /^[0-9]+$/) print $1 "-" $2 "-" $3 "-" $4 "-" $5; else print $1 "-" $2 "-" $3 "-" $4}' | sort | uniq -c | awk '{print $2 "," $1}' > "lld_display_${date_str}.csv";
    done;
    echo "date,count" > lld_display_check.csv;
    awk -F, '{count[$1]+=$2} END{for (i in count) print i "," count[i]}'  lld_display_check_temp.csv >> lld_display_check.csv;
    rm -rf lld_display_check_temp.csv;
fi

if [ "$mode" = "video" ]; then
    echo "date,count" > lld_video_check_temp.csv;
    for file in video/*_UTC.csv.gz; do
        date_str="$(echo "$file" | sed -E 's/.*-([0-9]{4}-[0-9]{2}-[0-9]{2}).*/\1/')";
        formatted_date="${date_str:5:2}/${date_str:8:2}/${date_str:2:2}";
        echo -n "$formatted_date," >> lld_video_check_temp.csv;
        zcat "$file" | wc -l >> lld_video_check_temp.csv;
        zcat "$file" | cut -d ',' -f 1-4 | awk -F ',' '{ print $1 "-" $2 "-" $3 "-" $4}' | sort | uniq -c | awk '{print $2 "," $1}' > "lld_video_${date_str}.csv";
    done;
    echo "date,count" > lld_video_check.csv;
    awk -F, '{count[$1]+=$2} END{for (i in count) print i "," count[i]}'  lld_video_check_temp.csv >> lld_video_check.csv;
    rm -rf lld_video_check_temp.csv;
fi