import os

base_html = '<img src="/static/assets/logos/&filename&" alt="&logoname& logo" />'


htmls = ""
for file in os.listdir("."):
    if file.endswith(".svg"):
        htmls += base_html.replace("&filename&", file).replace("&logoname&", file.replace("logo-", "").replace("-svgrepo-com", "").replace(".svg", "")) + "\n"

print(htmls)