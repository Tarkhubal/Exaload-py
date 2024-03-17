import os

for file in os.listdir("."):
    if file.endswith(".svg"):
        new_name = file.replace("logo-", "").replace("-svgrepo-com", "")
    
        os.rename(file, new_name)
    

print("End !")