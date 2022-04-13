import pandas as pd
from os import listdir, getcwd
import os
import json
import csv

old_links_master_list = []
url_base = "windaid.org"
files_dir = os.path.join(os.getcwd(), "csv_files")

with open(os.path.join(os.getcwd(), 'filler_dict.json')) as json_file:
    data = json.load(json_file)
filler_dict = data

def read_csv_and_return_dataframe(filename: str) -> object:
    with open(filename) as csv_file:
        df = pd.read_csv(filename)
    yield df

def return_links_list(df: object) -> list:
    old_links_list = []
    len_df = df.shape[0]
    for col in df.columns:
        if df[col].str.contains(url_base).sum() == len_df:
            old_links_list = df[col].to_list()
            break
    yield old_links_list

def get_url_suffixes(url_list: list) -> list:
    yield [url.split(url_base)[1].replace("/", "") for url in url_list]

old_links_master_list = []
for f in listdir(os.path.join(files_dir, "old_website_links_reports")):
    df = read_csv_and_return_dataframe(os.path.join(files_dir, "old_website_links_reports", f))
    old_links_master_list.extend(next(return_links_list(next(df))))

old_links_master_list = list(set(old_links_master_list))
old_links_master_list.sort()
old_links_suffixes = next(get_url_suffixes(old_links_master_list))

new_links_master_list = []
df = read_csv_and_return_dataframe(os.path.join(files_dir, "current_sitemap_links.csv"))
new_links_master_list.extend(next(return_links_list(next(df))))
new_links_suffixes = next(get_url_suffixes(new_links_master_list))

redirect = [""]*len(old_links_master_list)
for s in old_links_master_list:
    orig = s.split(url_base)[0]+url_base
    s = s.split(url_base)[1]
    if s:
        split_s = s
        for x in new_links_suffixes:
            if s in new_links_suffixes or split_s.split("-") in new_links_suffixes:
                redirect[old_links_master_list.index(orig+s)] = "https://"+url_base+"/"+x
            if not redirect[old_links_master_list.index(orig+s)] and x:
                if x in s:
                    redirect[old_links_master_list.index(orig+s)] = "https://"+url_base+"/"+x
        for k in filler_dict.keys():
            if not redirect[old_links_master_list.index(orig+s)] and k in s:
                print(k)
                print(filler_dict[k])
                redirect[old_links_master_list.index(orig+s)] = "https://"+url_base+"/"+filler_dict[k]


code = [301]*len(old_links_master_list)
zipped = list(zip(old_links_master_list, redirect, code))
final_df = pd.DataFrame(zipped, columns=['Links', 'Redirect', 'Code'])
# final_df = final_df.replace(r'^s*$', float('NaN'), regex = True)
# final_df.dropna(subset=['Redirect'], inplace=True)
final_df.to_csv(os.path.join(files_dir, "redirects.csv"), index=False)
with open("_redirects", "w") as my_output_file:
    with open(os.path.join(files_dir, "redirects.csv"), "r") as my_input_file:
        [ my_output_file.write(" ".join(row)+'\n') for row in csv.reader(my_input_file)]
    my_output_file.close()