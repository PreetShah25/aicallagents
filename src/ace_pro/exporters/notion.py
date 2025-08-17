"""
Notion exporter (skeleton). Requires NOTION_TOKEN and a parent page ID.
We avoid adding SDK dependency; you can use Notion's REST API via requests.
"""
import os, requests

def export_notion_simple(title: str, bullets, transcript: str, parent_page: str):
    token = os.getenv("NOTION_TOKEN")
    if not token: raise RuntimeError("Set NOTION_TOKEN")
    headers = {"Authorization": f"Bearer {token}", "Notion-Version": "2022-06-28", "Content-Type":"application/json"}
    children = [{"object":"block","type":"heading_1","heading_1":{"rich_text":[{"type":"text","text":{"content":"Highlights"}}]}}]
    for b in bullets:
        children.append({"object":"block","type":"bulleted_list_item","bulleted_list_item":{"rich_text":[{"type":"text","text":{"content":b}}]}})
    payload = {"parent":{"page_id": parent_page},"properties":{"title":{"title":[{"type":"text","text":{"content":title}}]}},"children":children}
    resp = requests.post("https://api.notion.com/v1/pages", headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json().get("id")
