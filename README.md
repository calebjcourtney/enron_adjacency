# Enron Adjacency
Python script for looping through the Enron emails and creating an adjacency list of who emailed whom at the company. The primary purpose is to create a directed graph with the list. Here's a copy of the first few rows of the output:

source | target | count
------ | ------ | -----
3e@enron.com | scott.hendrickson@enron.com | 1
4.ews@enron.com | andrew.edison@enron.com | 1
4.ews@enron.com | chris.hilgert@enron.com | 1
40ect@enron.com | Tammy.Gilmore@enron.com | 1
40ees@enron.com | bob.deitz@enron.com | 1

# Install
1. You need to `git clone` the repository.
2. Install `pandas` and `tqdm` using `pip install pandas tqdm` (I recommend using a [virtual environment](https://virtualenv.pypa.io/en/latest/))
3. Extract the tar.gz file using `tar xvzf enron_mail_20150507.tar.gz`

# Run
The process should run with `python process_data.py`, and outputs the `email_adjacency.csv` file, which is the adjacency list intended for a directed graph.
