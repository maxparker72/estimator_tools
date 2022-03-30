import os

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.client_context import UserCredential

test_team_site_url = "https://jedunn.sharepoint.com/sites/1232505342/SitePages/Intel-Homepage.aspx"
user_credentials = UserCredential('max.parker@jedunn.com','Sealant35')
ctx = ClientContext('{url}').with_credentials(user_credentials)

path = "file.txt"
with open(path, 'rb') as content_file:
    file_content = content_file.read()

list_title = "JE Dunn - Private"
target_folder = ctx.web.lists.get_by_title(list_title).root_folder
name = os.path.basename(path)
target_file = target_folder.upload_file(name, file_content).execute_query()
print("File has been uploaded to url: {0}".format(target_file.serverRelativeUrl))