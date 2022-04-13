# Summary
When switching over to a new website, a mistake was made in migrating the domain to the new hosting on netlify from wordpress. The sitemap was not collected from wordpress and so the links and SEO was not saved for redirection to the new links.

In my case however, since i had already done the migration, i needed to also get the links that had good SEO value. The way to do this as to use these website that i signed up for a trial and downloaded the CSv report for them. https://tools.cognitiveseo.com/users/dashboard/overview https://analytics.moz.com/pro/link-explorer/home

This was a good site explaining how to get back the links that were lost: https://www.searchenginejournal.com/search-and-rescue-4-ways-to-find-lost-url’s-after-a-bad-website-redesign-or-cms-migration/30385/#closeopen

After collecting the links, the next step was to create a pandas script that would take all the url suffixes, compare them to the existing sitemap, fill in any gaps and save it all to a redirects file.

## How to Use

1. In `csv_files > old_website_links_reports` drop all the report csv files containing the links with high SEO value
2. In `csv_files` drop the current sitemap csv file which has the links of the new website.
3. In `filler_dict.json` add pairs for values that were not captured in the comparisons based on the current site suffixes.
4. Run `pipenv install` then `pipenv run python3 main.py` and it will generate two files. `redirects.csv` and `_redirects`. The former contains all the info in a csv format and the latter contains the information (minus the header) which needs to be placed in th react root folder.
5. To update with new links, add more links of the current sitemap to the current_sitemap.csv and then re-run the script. Then copy over the _redirects file data (minus the header) to the react codebase.