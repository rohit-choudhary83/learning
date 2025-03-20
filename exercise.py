import os
import requests as re
#1 

folder = 'mini_dataset'

if not os.path.exists(folder):
    os.makedirs(folder)
    print("folder created!")

# 2

def scrapes_html(URL):
    response = re.get(URL)
    if response.status_code == 200:
        return response.text
    else:
        print(f"cant fatch {URL} status code is : {response.status_code}")
        return None

# 3 

def save_webpage(content, file_name):
    file_path = os.path.join(folder, file_name)
    with open(file_path, 'w' , encoding='utf-8') as file:
        file.write(content)

#4 

url_list = [
    'https://www.youtube.com/',
    'https://www.rgpvdiploma.in/',
    'https://www.tribal.mp.gov.in/MPTAAS',
    'https://google.com',
    'https://mpbooksolution.in/#gsc.tab=0',
    'https://www.facebook.com/',
    'https://www.instagram.com/',
    'https://mpbooksolution.in/class-1st-books-solutions/#gsc.tab=0',
    'https://play.tailwindcss.com/',
    'https://play.tailwindcss.com/X8oHO0Va8k'
]

# 5 

def process_url():
    for i in range(len(url_list)):
        content = scrapes_html(url_list[i])
        if content:
            save_webpage(content, f'website_{i+1}.html')
            print('file Saved!')

# 6 
process_url()