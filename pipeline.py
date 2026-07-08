#!/usr/bin/env python
# coding: utf-8

# # Data Extraction (ALMA REPORT API) : Sample XML file

# In[1]:


import xml.etree.ElementTree as ET
import pandas as pd


# In[2]:


all_rows = []
column_mapping = {}


# In[3]:


tree = ET.parse('alma_response.xml')
root = tree.getroot()

# ดึง mapping ของชื่อคอลัมน์จาก Schema
if not column_mapping:
    for e in root.iter():
        if 'name' in e.attrib and e.attrib['name'].startswith('Column'):
            col_id = e.attrib['name']
            col_name = e.attrib.get('{urn:saw-sql}columnHeading')
            if col_name:
                column_mapping[col_id] = col_name

# ดึงข้อมูลแถว
rows = [e for e in root.iter() if e.tag.endswith('Row')]
for row in rows:
    row_data = {}
    for col in row:
        # ตัด namespace ออกเพื่อเอาแค่ชื่อ tag (เช่น Column0, Column1)
        col_name = col.tag.split('}')[-1] if '}' in col.tag else col.tag
        row_data[col_name] = col.text

    if row_data:
        all_rows.append(row_data)


# In[4]:


# นำข้อมูลมาแปลงเป็น DataFrame
if all_rows:
    df = pd.DataFrame(all_rows)

    # เปลี่ยนชื่อคอลัมน์ตามที่ดึงมาจาก XML Schema
    if column_mapping:
        df.rename(columns=column_mapping, inplace=True)


# In[7]:


df


# In[8]:


df.to_excel("test.xlsx")


# In[ ]:




