""" Run a complete Google spider job in multiple batches """
import os
import subprocess
import pandas as pd

BATCH_SIZE = 5000           # Number of items to scrape per batch
OUTPUT_FILEPATH = 'data/out/google_spider_job_0.csv'
INPUT_FILEPATH = 'data/in/partslink_numbers.csv'


# ------------------------------------------------------- #
#                     Helper Functions                    #
# ------------------------------------------------------- #
def get_item_count():
    """ Get total number of items to scrape from input data file """
    if not os.path.exists(INPUT_FILEPATH):
        raise FileNotFoundError(f'Input file not found: {INPUT_FILEPATH}')
    
    return pd.read_csv(INPUT_FILEPATH, header=None).shape[0]


def delete_duplicate_headers_csv():
    """ Delete duplicates of the first row (headers) in CSV file """
    if not os.path.exists(OUTPUT_FILEPATH):
        raise FileNotFoundError(f'Output file not found: {OUTPUT_FILEPATH}')

    df = pd.read_csv(OUTPUT_FILEPATH)                           # Read CSV file
    df = df.loc[~(df == df.columns.tolist()).all(axis=1)]       # Delete rows that are equal to the header
    df.to_csv(OUTPUT_FILEPATH, index=False)                     # Save to CSV file


def rename_output_file_dynamically():
    """ Iterate through existing output filenames, rename output file to first available filename """
    if not os.path.exists(OUTPUT_FILEPATH):
        raise FileNotFoundError(f'Output file not found: {OUTPUT_FILEPATH}')

    # Search for highest existing filename
    i = 1
    while os.path.exists(f'data/out/google_spider_job_{i}.csv'):
        i += 1

    # Rename output file
    os.rename(OUTPUT_FILEPATH, f'data/out/google_spider_job_{i}.csv')


# ------------------------------------------------------- #
#                      Main Function                      #
# ------------------------------------------------------- #
def main():
    # Change working directory to project root, grandparent directory of current working directory: spiders -> carpart_weight_scraper -> carpart_weight_scraper
    os.chdir(os.path.join(os.getcwd(), os.pardir, os.pardir))

    # Delete existing output file
    if os.path.exists(OUTPUT_FILEPATH):
        os.remove(OUTPUT_FILEPATH)

    # Get total number of items to scrape
    total_items = get_item_count()

    # Loop through batches
    for i in range(0, total_items, BATCH_SIZE):
        # Start & end index of current batch
        start = i
        end = i + BATCH_SIZE

        # Check if end index exceeds total number of items
        if end > total_items:
            end = total_items

        # Print batch info
        batch_number = int(i/BATCH_SIZE) + 1
        number_of_batches = int(total_items/BATCH_SIZE) + 1 if total_items%BATCH_SIZE != 0 else int(total_items/BATCH_SIZE)
        print(f'\nBatch #{batch_number} of {number_of_batches}: Scraping car parts #{start}-{end}\n')

        # Command to run spider, specifies batch start/end & output filename
        command = f'scrapy crawl google_spider -a start={start} -a end={end} -o {OUTPUT_FILEPATH}'

        # Execute command, run spider
        subprocess.call(command, shell=True)
    
    # Clean up output file, after job is complete
    delete_duplicate_headers_csv()
    rename_output_file_dynamically()


# Only run main() if this script is being run directly. Prevents this script from being exceuted multiple times.
if __name__ == "__main__":
    main()