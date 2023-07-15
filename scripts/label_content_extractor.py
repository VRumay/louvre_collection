import pandas as pd 
import os
import re

# Create a function to remove all the crap from the inner_html column:
def clean_text(text):
    # Remove HTML tags
    text = re.sub('<.*?>', '', text)
    # Remove line breaks and tabs
    text = re.sub('\n|\r|\t', ' ', text)
    # Remove double spaces
    text = re.sub('  +', ' ', text)
    return text.strip()

cwd = os.chdir(r'C:\Users\rumay\Desktop\Louvre\inventories')
invent_dir = os.listdir() # Uncomment this
#invent_dir = ['inventory-10.xlsx'] # Comment this

for invent in invent_dir: 
    # Load to pandas
    df = pd.read_excel(invent) 
    # Replace relevant HTML tags with "LABEL:" to identify the start of a label, and "|" to separate the label from the content, then remove the ending tag.
    df["clean_html"] = df["inner_html"].str.replace(r'<div\s+class="m-3col\s+part__label">','LABEL:').str.replace(r'<div\s+class="m-7col\s+m-last\s+part__content">', '|').str.replace(r'<div\s+class="row\s+notice__fullcartel__group">', '')
    # Use the clean_text function we created above to the clean_html column
    df["clean_html"] = df["clean_html"].apply(clean_text)
    # Remove everything after the word Bibliography by keeping the first element after a split, we remove this because the Bibliography data is super messy
    df["clean_html"] = df["clean_html"].str.split(" Bibliography ").str[0]
    # Use the "LABEL:" substring we replaced abobe to split the clean_html column into one column for each label. This is saved to a new dataframe named new_df
    new_df = df['clean_html'].str.split('LABEL:', expand=True)
    # Add a prefix to the column names so they are not named as numbers
    new_df = new_df.add_prefix('label_')
    
    # concatenate the old df and the new one horizontally: [] <-> []
    df = pd.concat([df, new_df], axis=1)

    # Use the names of the columns in new_df to create a list of the label columns that will be unpivoted in the next step
    value_vars = new_df.columns.tolist()
    
    # Unpivot the label columns in the df, this basically creates a row for each label column, making the data longer instead of wider
    df = pd.melt(df, id_vars=['article_url','clean_html'], value_vars=value_vars, var_name='label', value_name='content')

    # Remove rows that have empty values in the content column and drop rows that were just blank spaces
    df = df.dropna(subset=['content']).query('content.str.strip() != ""')
   
    # Split the content column using the " |" symbol, the first element goes into the label column and the second one goes into the content column
    df[['label', 'content']] = df['content'].str.split(' \|', n=1, expand=True)
    # Reorder the rows by article_url
    df = df.sort_values(by=['article_url'], ascending=True)
    # Reset the index to get an accurate count of the rows
    df = df.reset_index(drop=True)
    # Save to xlsx
    df.to_excel(fr'C:\Users\rumay\Desktop\Louvre\clean_result\{invent}', index=False)

# Tareas: 
# Escribir algo de Docu
# Ordenar los Archivos en la carpeta de Drive
# Hacer una lista con los tipos de Labels que existen