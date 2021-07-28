Nagios Check - verify backup files age
======================================

The script is looking for the most recent file matching pattern in given directory. 
The file age is calculated in hours. Status is related to the file age.

Sample usage:
--------------

python -m cli_check_backups.cli -d /home/Downloads/ -p bak

Help:
--------------

python -m cli_check_backups.cli --help

Options:
--------------

-d DIRECTORY  Directory to review  [required]
-p TEXT       Filename pattern to search for
-w INTEGER    Warning limit in hours - default 25
-c INTEGER    Critical limit in hours - default 50
--help        Show this message and exit.