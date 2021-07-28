import click
import time
import sys
import re
from os import walk, path


def check_files(directory, pattern):
    reference_time = time.time()
    smallest_diff = 99999
    smallest_diff_file_name = 'FILE NOT FOUND'

    filePattern = re.compile(pattern, re.IGNORECASE)

    for (_, _, filenames) in walk(directory):
        for this_file in filenames:
            # print('Checking ', thisFile)
            if filePattern.search(this_file):
                this_file_time = path.getmtime(directory + this_file)
                diff_in_hours = (reference_time - this_file_time) / (60*60)
                if (diff_in_hours < smallest_diff):
                    smallest_diff = diff_in_hours
                    smallest_diff_file_name = this_file
        break

    return smallest_diff, smallest_diff_file_name


def print_file_info(type_to_show, smallest_diff_file_name, smallest_diff):
    print(f"{type_to_show} - {smallest_diff_file_name}; {smallest_diff}h" )


@click.command()
@click.option("-d", "directory", required=True,
                help="Directory to review",
                type=click.Path(exists=True, file_okay=False, dir_okay=True, readable=True) )
@click.option("-p", "pattern", default=".",
                help="Filename pattern to search for")
@click.option("-w", "warning_limit", default="25",
                help="Warning limit in hours - default 25",
                type=click.INT)
@click.option("-c", "critical_limit", default="50",
                    help="Critical limit in hours - default 50",
                    type=click.INT)
def process(directory, pattern, warning_limit, critical_limit):
    """ Checks wether in directory there is a file matching pattern. 
    Once found, checks if modification date exceeds warning or critical limits.

    Sample usage: 

    python -m cli_check_backups.cli -d /home/Downloads/ -p bak
    """
    try:
        smallest_diff, smallest_diff_file_name = check_files(directory, pattern)
        smallest_diff = round(smallest_diff, 1)
        
        if (smallest_diff > critical_limit):
            # critical
            print_file_info("CRITICAL", smallest_diff_file_name, smallest_diff)
            sys.exit(2)
        elif (smallest_diff > warning_limit):
            # warning
            print_file_info("WARNING", smallest_diff_file_name, smallest_diff)
            sys.exit(1)
        else: 
            # OK
            print_file_info("OK", smallest_diff_file_name, smallest_diff)
            sys.exit(0)
        
    except Exception as e:
        print(e)
        sys.exit(3)


if __name__ == "__main__":
    process()
