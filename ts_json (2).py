
import os
import re
from bs4 import BeautifulSoup
import pandas as pd
import json


# list of TestLink -TestSuite

# def tl_suite(directory_path):
#     items = os.listdir(directory_path)
#     tst_files=[]
#     # Print the list of items
#     for item in items:
#         tick=item.split(" -",2)
#         tick=tick[0]
#         values_inside_brackets = re.search(r'\[(.*?)\]', tick).group(1)
#         tst_files.append(values_inside_brackets)
#     return tst_files

def read_jira_file(file_path_tl):
    with open(file_path_tl, 'r') as file:
        jira_content = file.read()
    return jira_content

def j_file(file_path_js):
    with open(file_path_js, 'r') as file:
        ut_content = json.load(file)
    return ut_content

##list of JSON -TestSuite

def json_suite(json_path):
    jsn_files=[]
    js = os.listdir(json_path)
    for item in js:
        j=item.split(".",2)
        j=j[0]
        jsn_files.append(j)
    return jsn_files
def tofindtitle_xml(tst):
     element = jira_soup.find('testsuite')
     title_sum= element['name']
     return title_sum

def issuetype():
      
      issue_type=j_soup['issuetype']['name']
      return issue_type

def testlink_id():
     t_id = jira_soup.find('testsuite')
     tt= t_id['id']
     return tt

def matchedcf():
     ct_tags = tst.find_all("custom_field")
     length=len(ct_tags)
     #print(length)
     str2=''
     for ct in ct_tags:
               name=ct.find("name").text
               name_list_tl.append(name)
               ct_values=ct.find("value").text

               if(ct_values is None):
                    value_list_tl.append(str2)
               else:
                    value_list_tl.append(ct_values)

      
      
     tc_dict=dict(zip(name_list_tl,value_list_tl))
     custom_fields_jira=[]

     for element in j_soup:
        if element in csv_jira:
             custom_fields_jira.append(element)
     
     matched_values=[]
     for key,value in tc_dict.items():
                        #print(key,value)
                        if key in  csv_ut :
                            try :
                                    jira_field_index=csv_ut.index(key)
                                    if csv_jira[jira_field_index] in custom_fields_jira :
                                           matched_values.append(csv_ut[jira_field_index])
                                           #print(csv_jira[jira_field_index])
                                    
                            except Exception as e:
                                    print("Not found")                                  

     return matched_values

def tofindcustomfields_xml(tst):
      ct_tags = tst.find_all("custom_field")
      length=len(ct_tags) 
      #print(length)
      str2=''
      for ct in ct_tags:
               name=ct.find("name").text
               name_list_tl.append(name)
               ct_values=ct.find("value").text

               if(ct_values is None):
                    value_list_tl.append(str2)
               else:
                    value_list_tl.append(ct_values)

      
      tc_dict=dict(zip(name_list_tl,value_list_tl))
      return len(tc_dict)

if __name__ == "__main__":
          
        directory_path = '/Users/rukksana/Downloads/test_link testsuite'
        # tl_files= tl_suite(directory_path)
        # print(tl_files)

        json_path = '/Users/rukksana/Downloads/testsuite'  
        js_files=json_suite(json_path)
        print(js_files)
        fl_names=[]
        csv_data=[]

        df = pd.read_csv('/Users/rukksana/Downloads/tc/ts_json/testsuite.csv')
        csv_ut= df['tl_fields'].to_list()
        csv_jira= df['jira_fields'].to_list()
       # Iterate over files in the folder
        for filename in os.listdir( directory_path):
            if filename.endswith(".xml"):  # Filter files with .xml extension
                file_path = os.path.join( directory_path, filename)

                # Parse each XML file
                with open(file_path, "r") as file:
                    xml_data = file.read()
                    soup = BeautifulSoup(xml_data, "xml")

                    print("File:", filename)
                    f=filename.split(" -",2)
                    f=f[0]
                    values_inside_brackets = re.search(r'\[(.*?)\]', f).group(1)
                    fl_names.append(values_inside_brackets)
        
        for element in fl_names:
             if element in js_files:
                  print(element,'Matched')
                  keyword= element
                  for root, dirs, files in os.walk(directory_path):
                      for file_name in files:
                          if keyword in file_name:
                              file_path_tl = os.path.join(root, file_name)
                              jira_content = read_jira_file(file_path_tl)
                              jira_soup = BeautifulSoup(jira_content, "xml")
                              print("File found:", file_path_tl)

                  for root, dirs, files in os.walk(json_path ):
                      for file_name in files:
                          if keyword in file_name:
                              file_path_js = os.path.join(root, file_name)
                              j_soup = j_file(file_path_js)

                              print("File found:", file_path_js)
                  tst_tags = jira_soup.find_all("testsuite")
            
                  name_list_tl=[]
                  value_list_tl=[]
                  st=''
                  matched =[]
                  
                  for tst in tst_tags :
                        jira_title=j_soup['summary']
                        xml_ftitle=tofindtitle_xml(tst)
                        xml_title=xml_ftitle.split(" -")
                        x_ticket=xml_title[0]
                        xt=xml_title[1]
                        if jira_title == xt :
                            csv_data.append([issuetype(),x_ticket,testlink_id(),xml_ftitle,'Matched',len(csv_ut),matchedcf(),len(matchedcf()),matchedcf() is not None])
                            print(tofindcustomfields_xml(tst))
                        

df=pd.DataFrame(csv_data,columns=['Test Type','Jira Ticket Id','TestLink Id','Title','Title Status','Count of Custom Fields','Custom Fields Matched','Matched count','Custom Fields Status'])
        #df = pd.concat([df, new_column], axis=1)
df.to_csv('sample3.csv',index=False)
             