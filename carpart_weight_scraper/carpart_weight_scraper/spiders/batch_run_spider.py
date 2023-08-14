""" Run a spider job in multiple batches """
import os
import subprocess
import pandas as pd


class BatchRunSpider:
    def __init__(self, spider_name, input_filepath, batch_size=10):
        """ Constructor for the BatchRunSpider class.
        :param spider_name: Name of the spider to run.
        :param input_filepath: Path to the input data file.
        :param batch_size: Number of items to scrape per batch. Default is 10.
        """
        self.spider_name = spider_name
        self.input_filepath = input_filepath
        self.batch_size = batch_size
        self.output_filepath = f'data/out/{spider_name}_job_0.csv'


    # ------------------------------------------------------- #
    #                     Helper Functions                    #
    # ------------------------------------------------------- #
    def get_item_count(self):
        """ Get the total number of items to scrape from the input data file.
        :return: Number of items to scrape.
        """
        if not os.path.exists(self.input_filepath):
            raise FileNotFoundError(f'Input file not found: {self.input_filepath}')

        return pd.read_csv(self.input_filepath, header=None).shape[0]


    def delete_duplicate_headers_csv(self):
        """ Delete duplicates of the first row (headers) in the CSV file. """
        if not os.path.exists(self.output_filepath):
            raise FileNotFoundError(f'Output file not found: {self.output_filepath}')

        df = pd.read_csv(self.output_filepath)                           
        df = df.loc[~(df == df.columns.tolist()).all(axis=1)]       
        df.to_csv(self.output_filepath, index=False) 


    def rename_output_file_dynamically(self):
        """ Rename output file to the lowest available filename. """
        if not os.path.exists(self.output_filepath):
            raise FileNotFoundError(f'Output file not found: {self.output_filepath}')

        i = 1
        while os.path.exists(f'data/out/{self.spider_name}_job_{i}.csv'):
            i += 1
        os.rename(self.output_filepath, f'data/out/{self.spider_name}_job_{i}.csv')


    # ------------------------------------------------------- #
    #                       Main Funtion                      #
    # ------------------------------------------------------- #
    def run(self):
        # Get total number of items to scrape
        total_items = self.get_item_count()
        print(f'[{self.spider_name}] Total items to scrape: {total_items}')
        #total_items = 13  # FOR TESTING 

        # Run spider in batches
        for i in range(0, total_items, self.batch_size):
            # Start and end indices for batch
            start = i
            end = i + self.batch_size

            # Check if end index exceeds total number of items
            if end > total_items:
                end = total_items

            # Print progress
            number_of_batches = int(total_items/self.batch_size) + 1 if total_items%self.batch_size != 0 else int(total_items/self.batch_size)
            print(f'\n[{self.spider_name}] Batch #{int(i/self.batch_size) + 1} of {number_of_batches}: Scraping car parts #{start}-{end}\n')

            # Create command to run spider, with start & end indices as arguments
            command = f'scrapy crawl {self.spider_name} -a start={start} -a end={end} -o {self.output_filepath}'

            # Execute command, run spider
            subprocess.call(command, shell=True)

        # Clean up output file, after job is complete
        self.delete_duplicate_headers_csv()
        self.rename_output_file_dynamically()


if __name__ == "__main__":
    # Change working directory to project root
    os.chdir(os.path.join(os.getcwd(), os.pardir, os.pardir))

    # Create batch spider instances
    google_spider = BatchRunSpider('google_spider', 'data/in/partslink_numbers.csv', 5000)
    amazon_spider = BatchRunSpider('amazon_spider', 'data/in/amazon_links.csv', 5000)

    # Run spiders in batches
    google_spider.run()
    #amazon_spider.run()
