import getopt
import os
import sys
from selenium.common.exceptions import WebDriverException

from document_generator import generate_document
from scrapper import scrape


def main():
    argumentList = sys.argv[1:]

    # Options
    options = "hu:"

    # Long options
    long_options = ["Help", "Url="]

    url = None

    try:
        # Parsing argument
        arguments, values = getopt.getopt(argumentList, options, long_options)
        
        # Checking each argument
        for currentArgument, currentValue in arguments:
            if currentArgument in ("-h", "--Help"):
                print("Usage: script.py -u <URL>")
                return

            elif currentArgument in ("-u", "--Url"):
                url = currentValue

        if url:
            deck_name = url.split('/')[-1]
            try:
                # Run the scraping function
                print("Starting scrape...")
                scrape(url)
                print("Scrape completed. Generating document...")
                # Run the document generation function
                generate_document(os.path.join("documents", "images", deck_name), deck_name)
                print("Document generation completed.")
            except WebDriverException as e:
                print(f"Error during scraping: {e}")
        else:
            print("URL must be provided. Use -h for help.")

    except getopt.error as err:
        # Output error, and return with an error code
        print(str(err))

if __name__ == "__main__":
    main()
