from notion.client import NotionClient
from notion.block import PageBlock
from notion.block import TextBlock
from datetime import datetime
from flask import jsonify

def create_page(request):
  if request.method != 'POST':
    return 'Ok'

  request_json = request.get_json()

  token_v2 = request.headers['x-notion']
  client = NotionClient(token_v2=token_v2)

  url = request_json['url']
  page = client.get_block(url)
  print("Found base page!")

  if request_json and 'title' in request_json:
    title = request_json['title']
  else:
    title = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')

  content = request_json['content']
  new_page = page.children.add_new(PageBlock, title=title)
  new_page.children.add_new(TextBlock, title=content)

  print("Created new page!")

  response = {
    url: new_page.get_browseable_url(),
    status: 'done'
  }

  return jsonify(response)
