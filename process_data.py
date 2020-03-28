"""
Script for processing through the Enron email corpus.
1. Iterate through all files in the `maildir` folder
2. Get the `Message-ID` from the email and ensure that it's not a duplicate of the messages we've already processed
3. Extract who the email was sent from and who it was sent to.
4. Add the list of from and to to our dataframe
5. Output the final dataframe to csv with counts of the emails

Written with python 3.7 using pandas and tqdm packages installed from pip
Run with `python process_data.py`

Output of running the script:
3500it [06:03,  9.64it/s]
"""
import os
import re
import codecs

import pandas as pd
from tqdm import tqdm


def main():
    """
    Handles iterating through the actual files.
    """
    rootdir = "maildir/"
    message_ids = []

    source = []
    target = []

    for subdir, dirs, files in tqdm(os.walk(rootdir)):
        for file in files:
            temp_file = codecs.open(
                os.path.join(subdir, file),
                'r',
                encoding='utf-8',
                errors='ignore'
            )

            from_address, to_addresses, message_ids = process_file(temp_file, message_ids)

            # if we didn't get a from_address from the email, then we can skip this file
            if from_address == "" or from_address is None:
                continue
            elif not check(from_address):
                continue

            for email in to_addresses:
                if check(email):
                    source.append(from_address)
                    target.append(email)

                    assert len(source) == len(target), "len source: {}, len target: {}".format(len(source), len(target))

    df = pd.DataFrame({"source": source, 'target': target})
    df['count'] = 1
    df = df.groupby(['source', 'target'])['count'].sum().reset_index()
    df = df.loc[df['source'] != df['target']]

    df.to_csv('email_adjacency.csv', index = False)


def process_file(in_file: codecs.StreamReaderWriter, message_ids: list) -> tuple:
    """
    Processes an individual file, parsing for the from, to, addresses, and ensuring we haven't already processed the same email to a different user

    Args:
        in_file (codecs.StreamReaderWriter): handle of the input file
        message_ids (list): sorted list of the message ids we've already processed

    Returns:
        tuple: from_address (string), to_addresses (list), message_ids (list)
    """
    from_address = ""
    to_addresses = []
    # iterate through the lines of the file
    for line in in_file:
        if "Message-ID: " in line and len(message_ids) > 1:
            # if we've already processed this message, then we need to skip this email
            if binarySearch(message_ids, line.strip()) != -1:
                return None, None, message_ids

            message_ids.append(line.strip())
            message_ids.sort()

        if "From: " in line and "X-From: " not in line and "@enron.com" in line and from_address == "":
            lst = re.findall('\S+@\S+', line)
            if len(lst) == 0:
                continue

            email = clean_email(lst[0])

            from_address = email

        if "To: " in line and "X-To: " not in line and to_addresses == []:
            lst = re.findall('\S+@\S+', line)

            for email in lst:
                email = clean_email(email)

                to_addresses.append(email)

            to_addresses = list(set(to_addresses))

    return from_address, to_addresses, message_ids


def binarySearch(arr: list, x: str):
    """
    Binary search slightly modified from code I found here:
    https://www.geeksforgeeks.org/python-program-for-binary-search/

    Args:
        arr (list): the list to search - this must be a sorted list
        x (str): the item to find

    Returns:
        int: returns the index of the item in the list, or returns -1 for if it can't be found
    """
    l = 0
    r = len(arr)
    while (l <= r):
        m = l + ((r - l) // 2)

        res = (x == arr[m])

        # Check if x is present at mid
        if (res == 0):
            return m - 1

        # If x greater, ignore left half
        if (res > 0):
            l = m + 1

        # If x is smaller, ignore right half
        else:
            r = m - 1

    return -1


def clean_email(email: str) -> str:
    """
    Cleans the email address being passed,
    based on the variability of what was found in the enron emails

    Args:
        email (str): the dirty email

    Returns:
        str: the cleaned email
    """
    email = email.replace('[mailto:', '').replace(']', '')
    email = email.replace('<mailto:', '').replace('>]', '')
    email = email.replace('mailto:', '')
    email = email.replace('<', '').replace('>', '')
    email = email.replace(',', '')

    return email


def check(email: str) -> bool:
    """
    Basic regex to determine if it's a valid email address, adapted from code found here:
    https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/

    Args:
        email (str): the email to check

    Returns:
        bool: if valid, return true, if not, return false
    """
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if (re.search(regex, email)):
        return True

    else:
        return False


if __name__ == '__main__':
    main()
