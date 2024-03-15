from requests import get
import json
from re import search

target = ["title", "itemDetailUrl", "imagePath"]

BASE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9,ja;q=0.8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
}

def execute(url):
    try:
        r = get(url, headers=BASE_HEADERS )
        match = search(r'data: ({.+})', r.text).group(1)
        data = json.loads(match)
        print("YEs")
        return data
    except Exception:
        return "error"

def parse_product(response):
    """parse product HTML page for product data"""
    data = execute(response)
    if data == "error":
        return "error"
    # print(data)
    try:
        product = {
            "id": data["productInfoComponent"]["idStr"],
            "name": data["productInfoComponent"]["subject"],
            "description_short": data["metaDataComponent"]["description"],
            "images": data["imageComponent"]["imagePathList"],
            "stock": data["inventoryComponent"]["totalAvailQuantity"],
            "variants": data['priceComponent']['skuPriceList'],
            "description": data["productPropComponent"]["props"],
            "fee": data["webGeneralFreightCalculateComponent"]["shippingFeeText"]
        }
    except Exception as e:
        print(e)
        return "error"
    
    with open('request_data.json', 'w', encoding='utf-8') as f:
        json.dump(product, f, ensure_ascii=False, indent=4)
    return product

def main(url):
    # url = "https://ja.aliexpress.com/item/33060691049.html?spm=a2g0o.best.moretolove.17.440b1fd3hyIIjK&gatewayAdapt=glo2jpn"
    return parse_product(url)
