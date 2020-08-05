#!/usr/bin/env python3

import argparse
import os
import sys
import re
import urllib.request

def convert_textfile_to_list(file_path):
    """Read text file and return each line in a list.

    Args:
        file_path (str): Full path to the text file.

    Returns:
        list: List where each index is a line from the text file.
    """

    markdown_file = open(file_path, "r")
    markdown_file_lines = markdown_file.readlines()
    
    return markdown_file_lines

def convert_list_to_textfile(line_list, filename, output_folder):
    """Convert list to text file. Each index will be a line in the file.

    Args:
        line_list (list): List with each index being a line of the text file.
        filename (str): Filename of the file to create.
        output_folder (str): Folder to put the created file into.
    """

    # Open file for writing
    
    full_path = output_folder + "/" + filename
    created_textfile = open(full_path, "w")

    # Write all lines
    created_textfile.writelines(line_list)

    # Close file
    created_textfile.close()
    
def print_error_and_exit(error_message):
    """Print error message and exit program.

    Args:
        error_message (str): Error message to print.
    """

    print("Error: " + error_message)
    sys.exit()

def download_image(image_url, destination_folder):
    """Download an image and place it in a specfic folder.

    Args:
        image_url (str): URL of image.
        destination_folder (str): Folder to place image into.
    """
    image_filename = image_url.split("/")[-1]
    urllib.request.urlretrieve(image_url, destination_folder + "/" + image_filename)

def convert_markdown_images(file_path, output_folder):
    """Will convert Markdown to have images locally rather than on Dropbox.

    Args:
        file_path (str): Full path to the text file.
        output_folder (str): Folder to put altered Markdown file and images.
    """

    # Read file to list

    markdown_lines_list = convert_textfile_to_list(file_path)

    # Find the indexes with a match
    
    image_tag_regex = r"^!\[.*\]\(https:\/\/paper-attachments.dropbox.com\/s_[A-Z,0-9]{64}_[0-9]{13}_image.png\)$"
    matched_index_list = []

    for index, line in enumerate(markdown_lines_list):

        if re.match(image_tag_regex, line) != None:
            matched_index_list.append(index)

    # If we have no matches, inform user there is nothing to be done

    if len(matched_index_list) == 0:
        print_error_and_exit("No images where found in file, there is nothing to be done")


    # Alter Markdown File

    image_folder = output_folder + "/img"
    os.mkdir(image_folder)
    
    image_url_regex = r"https:\/\/paper-attachments.dropbox.com\/s_[A-Z,0-9]{64}_[0-9]{13}_image.png"

    for index in matched_index_list:

        # Extract URL of image and download
        image_url_match = re.search(image_url_regex, markdown_lines_list[index]).group(0)
        download_image(image_url_match, image_folder)

        # Replace Dropbox URL with local path
        image_filename = image_url_match.split("/")[-1]
        markdown_lines_list[index] = markdown_lines_list[index].replace(image_url_match, "./img/" + image_filename)

    # Read altered file list to disk

    convert_list_to_textfile(markdown_lines_list, os.path.basename(file_path), output_folder)

def main():

    # Parse the arguments passed

    parser = argparse.ArgumentParser(description='Store Dropbox Paper Images Locally')
    parser.add_argument('-f', '--file', help="Markdown file path.", required=True)
    parser.add_argument('-o', '--output', help="Folder to store altered Markdown file and images.", required=True)

    args = parser.parse_args()

    # Check that Markdown file exists

    if os.path.exists(args.file) == False:
        print_error_and_exit("Specfied markdown file does not exist.")
    elif os.path.isfile(args.file) == False:
        print_error_and_exit("Specfied markdown file is not a file.")

    # Check that output is a valid empty folder

    if os.path.exists(args.output) == False:
        print_error_and_exit("Specfied output folder does not exist.")
    elif os.path.isdir(args.output) == False:
        print_error_and_exit("Specfied output folder is not a folder.")
    elif len(os.listdir(args.output)) != 0:
        # Maybe in future allow it to be non-empty, but ensure an img folder along with Markdown file is not present
        print_error_and_exit("Specfied output folder is not empty")

    # Perform core logic to convert Markdown file

    convert_markdown_images(args.file, args.output)

if __name__ == "__main__":
    main()
