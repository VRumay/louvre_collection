import pandas as pd
import os
import re

clean_results = r"C:\Users\rumay\Desktop\Louvre\louvre_collection\clean_result"
cwd = os.chdir(clean_results)
clean_dir = os.listdir()

def remove_letters(text):
        # Remove letters and specific accented characters
    text = re.sub(r"[a-zA-ZéèêÉÈÊï,;: ()'\.!?]", '', text)
    text = text.replace('--',',-').replace('/',',').replace(',,','')
    text = re.sub(r'(\d+)-', r'\1,', text)

    # Split the string by commas and keep the last two groups
    groups = text.split(',')
    if len(groups) > 2:
        groups = groups[-2:]

    # If the first group has more than 4 digits and the extra digit is not a hyphen, remove it
    if len(groups) > 0 and len(groups[0]) > 4 and groups[0][-5] != '-':
        groups[0] = groups[0][-4:]

    # Join the groups back with commas and handle the case where the result is empty
    result = ','.join(groups)
    if result == ',' or result == ',,':
        return ''
    return result

for i in clean_dir:
    df = pd.read_excel(i)
    print(i)
    dates_only = df[df['label'] == 'Date']
    dates_only['label'] = 'Date Range'
    dates_only['content'] = dates_only['content'].apply(remove_letters)
    print(dates_only[['article_url','content']])
    # Append dates_only to the bottom of the df DataFrame
    result_df = pd.concat([df, dates_only], ignore_index=True)

    # Save the combined DataFrame to the original Excel file, overwriting it
    result_df.to_excel(i, index=False)  # Specify index=False to avoid writing the index column

    

    





