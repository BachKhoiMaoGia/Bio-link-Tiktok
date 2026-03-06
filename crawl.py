import json, urllib.request, urllib.parse

API = "https://collshp.com/api/v3/gql/graphql"
HEADERS = {
    "Content-Type": "application/json",
    "Referer": "https://collshp.com/tieubachmao",
}

# Get all groups
groups_query = '{"query":"{ storefrontGroupList(urlSuffix: \\"tieubachmao\\", uuId: \\"crawl\\", deviceId: \\"crawl\\") { groupList { groupId groupName totalCount } } }"}'
req = urllib.request.Request(API, data=groups_query.encode(), headers=HEADERS, method="POST")
with urllib.request.urlopen(req) as resp:
    groups_data = json.loads(resp.read())

groups = groups_data["data"]["storefrontGroupList"]["groupList"]

all_products = {}
for g in groups:
    gid = g["groupId"]
    gname = g["groupName"]
    total = int(g["totalCount"])
    if total == 0:
        continue
    
    # Fetch all items in this group
    items = []
    offset = 0
    while offset < total:
        q = json.dumps({
            "query": '{ storefrontGroupProductList(urlSuffix: "tieubachmao", groupId: "' + gid + '", uuId: "crawl", deviceId: "crawl", page: {offset: ' + str(offset) + ', limit: 50}) { itemList { linkId link linkName image itemId h5Link itemCard } pagination { totalCount hasMore } } }'
        })
        req2 = urllib.request.Request(API, data=q.encode(), headers=HEADERS, method="POST")
        with urllib.request.urlopen(req2) as resp2:
            data2 = json.loads(resp2.read())
        
        item_list = data2.get("data", {}).get("storefrontGroupProductList", {}).get("itemList", [])
        items.extend(item_list)
        
        pagination = data2.get("data", {}).get("storefrontGroupProductList", {}).get("pagination", {})
        if not pagination.get("hasMore", False):
            break
        offset += 50
    
    if items:
        all_products[gname] = items

# Output as JSON
with open("/workspaces/Bio-link-Tiktok/products.json", "w", encoding="utf-8") as f:
    json.dump(all_products, f, ensure_ascii=False, indent=2)

# Summary
for cat, items in all_products.items():
    print(f"{cat}: {len(items)} sản phẩm")
print(f"\nTổng: {sum(len(v) for v in all_products.values())} sản phẩm")
