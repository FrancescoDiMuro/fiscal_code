# fiscal_code

Hi! This is my first public repository, so please be kind if it is not well formatted or it contains errors.  
I started learning Python about two months ago, and I made this script to challenge myself.  
Comments and (good) critism are welcome.  
Thanks!


❓ **What can I do with this repository?**

This repository contains:
 - fiscal_code.py , used to calculate the fiscal code of a person
 - municipilities.csv , used as a database of all municipilites in Italy

❓ **What do I have to do to use these files?**

You just need to download _fiscal_code.py_ and run it.  
The libraries you need to have in order to run this file are:
```python3
import operator as op
import pandas as pd
import re
```  

Inputs that need to be provided are:
- surname
- name
- birth_date (in the format DD/MM/YYYY as specified)
- sex
- city (this is the only case-sensitive parameter)

Cheers 🖖
