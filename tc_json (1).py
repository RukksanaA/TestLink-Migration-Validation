
import os
import re
from bs4 import BeautifulSoup
import pandas as pd
import json

def issuetype():
      
      issue_type=json_data['issuetype']['name']
      return issue_type

def tofindtitle(filename):
     
    folder_path = "/Users/rukksana/Downloads/TC_JIRA"
    file_path = os.path.join(folder_path, filename + ".json")
    
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
            
        # Access objects in the JSON data
        # Example: Assuming the JSON file contains a "title" field
        if "summary" in data:
            print("Title:", data["summary"])
            return data["summary"]
        else:
            print("No title found in the JSON file.")
    else:
        print("File not found.")
def tl_id():
     t_id = soup.find('testcase')
     tt= t_id['internalid']
     return tt


def matchedcf():
     ct_tags = testcase.find_all("custom_field")
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

     for element in json_data:
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
def count_action_testlink(testcase):
       step_tags = testcase.find_all("actions")
       return len(step_tags)

if __name__ == "__main__":
    xml_folder_path = '/Users/rukksana/Downloads/test_link testsuite'  # Replace with the actual path to your XML folder
    json_folder_path = '/Users/rukksana/Downloads/TC_JIRA'  # Replace with the actual path to your JSON folder
    csv_data=[]
    n_tl=[]
    n_j=[]
    t_j=[]
    t_tl=[]
    

    name_list_tl=[]
    value_list_tl=[]

    matching_elements=[]
    tmatching_elements=[]
    df = pd.read_csv('/Users/rukksana/Downloads/testcase.csv')
    csv_ut= df['tl_fields'].to_list()
    csv_jira= df['jira_fields'].to_list()

    # Iterate over JSON files
    for json_filename in os.listdir(json_folder_path):
        if json_filename.endswith('.json'):  # Filter JSON files
            json_file_path = os.path.join(json_folder_path, json_filename)

            # Read and process the JSON file
            with open(json_file_path, 'r') as json_file:
                json_data = json.load(json_file)
            
            
                name_of_jira =json_data['summary']
                n_j.append(name_of_jira)
                j=json_filename.split(".",2)
                jf=j[0]
                t_j.append(jf)

                #t_j.append()
                #print(name_of_jira)

            # Iterate over XML files
        for xml_filename in os.listdir(xml_folder_path):
            if xml_filename.endswith('.xml'):  # Filter XML files
                xml_file_path = os.path.join(xml_folder_path, xml_filename)

                # Read and process the XML file
                with open(xml_file_path, 'r') as xml_file:
                    xml_data = xml_file.read()
                
                # Parse the XML data using Beautiful Soup
                soup = BeautifulSoup(xml_data, 'xml')
                testcases = soup.find_all('testcase')

                # Extract the "name" attribute for each test case
                for testcase in testcases:
                    name_tl = testcase.get('name')
                    tln=name_tl.split(" -",2)
                    #name_of_tl=tln[1]
                    print(tln)
                    ticket=tln[0]
                    act=[]
                    
                    name_of_tl = name_tl.split("] -")[1].strip()
                    n_tl.append(name_of_tl)
                    
                    tt= testcase['internalid']
                    print(name_of_tl)
                    print(name_of_jira)
                    print('Matched')
                    if name_of_tl == name_of_jira:
                       steps = json_data["customfield_24066"]["steps"]
                       actions = [step["fields"]["Action"] for step in steps]
                       for action in actions:
                            act.append(action)
                       csv_data.append([issuetype(),ticket,tt,name_of_tl,'Matched',len(csv_ut),matchedcf(),len(matchedcf()),matchedcf() is not None,act,len(act),count_action_testlink(testcase)])
                       ele = ticket.split("[")[1].split("]")[0]
                       t_tl.append(ele)

    
    # print('tickets in j',len(n_j))
    # print('tickets in tl',len(n_tl))
    # print('tickets in j',len(t_j))
    # print('tickets in tl',len(t_tl))
    # print(t_j)
    # print(t_tl)

    
    not_in_list2 = [element for element in t_j if element not in t_tl]

    for element in not_in_list2:
        print(element)
        csv_data.append([issuetype(),element,None,tofindtitle(element),'Un Matched',None,None])


df=pd.DataFrame(csv_data,columns=['Type','Jira Ticket','Ticket Id','Title','Title Status','Total Count of Custom Fields','Custom Fields Matched','Count of Matched Fields','Custom Field Status','Actions(steps)','Action count Jira','Actions count Testlink'])
        #df = pd.concat([df, new_column], axis=1)
df.to_csv('sampleTC.csv',index=False)
                        

        
        
       
