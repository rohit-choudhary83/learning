# data collection
import requests as re
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings

# unstructured to structured
from bs4 import BeautifulSoup
import pandas as pd
import feature_extraction as fe
import os

disable_warnings(InsecureRequestWarning)

# Step 1: csv to dataframe


URL_file_name = "verified_online.csv"
data_frame = pd.read_csv(URL_file_name)

 

# retrieve only "url" column and convert it to a list
URL_list = data_frame['url'].to_list()

# restrict the URL count
begin = 19000
end = 21000
collection_list = URL_list[begin:end]

# only for the legitimate
#tag = "https://"
#collection_list = [tag + url for url in collection_list]


#Avoiding Duplicates in CSV

file_path = "phishing_data.csv"
write_header = not os.path.exists(file_path)
 

#data_frame.to_csv(file_path, mode='a', index=False, header=write_header)



# function to scrape the content of the URL and convert to a structured form for each
def create_structured_data(url_list):
    #
    
    data_list = []
    for i in range(0, len(url_list)):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            response = re.get(url_list[i], headers=headers, verify=False, timeout=4)

            if response.status_code != 200:
                print(i, ". HTTP connection was not successful for the URL: ", url_list[i])
            else:
                soup = BeautifulSoup(response.content, "html.parser")
                vector = fe.create_vector(soup)
                vector.append(str(url_list[i]))
                data_list.append(vector)
        except re.exceptions.RequestException as e:
            print(i, " --> ", e)
            continue
    return data_list


data = create_structured_data(collection_list)

columns = [
    'has_title',
    'has_input',
    'has_button',
    'has_image',
    'has_submit',
    'has_link',
    'has_password',
    'has_email_input',
    'has_hidden_element',
    'has_audio',
    'has_video',
    'number_of_inputs',
    'number_of_buttons',
    'number_of_images',
    'number_of_option',
    'number_of_list',
    'number_of_th',
    'number_of_tr',
    'number_of_href',
    'number_of_paragraph',
    'number_of_script',
    'length_of_title',
    'has_h1',
    'has_h2',
    'has_h3',
    'length_of_text',
    'number_of_clickable_button',
    'number_of_a',
    'number_of_img',
    'number_of_div',
    'number_of_figure',
    'has_footer',
    'has_form',
    'has_text_area',
    'has_iframe',
    'has_text_input',
    'number_of_meta',
    'has_nav',
    'has_object',
    'has_picture',
    'number_of_sources',
    'number_of_span',
    'number_of_table',
    'URL'
]

df = pd.DataFrame(data=data, columns=columns)

# labelling
df['label'] = 1

df.to_csv("phishing_data.csv", mode='a', index=False, header=write_header )  # header should be false after the first run

#df.to_csv("structured_data_legitimate.csv", mode='a', index=False, header=False)  # header should be false after the first run