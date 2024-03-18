import re
from pandas import DataFrame, read_csv
from requests import get

from Aliex.StorePageSearch import main as sp

from Aliex.SingleProductSearch import main as sps

IDs = []

# Let's use browser like request headers for this scrape to reduce chance of being blocked or asked to solve a captcha
BASE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9,ja;q=0.8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
}

def scrape_products(ids, ng_words):
    """scrape aliexpress products by id"""
    print(f"scraping {len(ids)} products", ng_words, type(ng_words))
    # responses = await asyncio.gather(*[session.get(f"https://ja.aliexpress.com/item/{id_}.html") for id_ in ids])
    # print(f"scraped {len(responses)} products")
    # print(responses)
    results = []
    cnt = 0
    for response in ids:
        result_response = sps(response)
        cnt += 1
        
        if result_response ==  "error":
            print("---------------------%%%%%%%%%%%%エラー!!!!!!!!%%%%%%%%%%%%----------", cnt)
            print("エラー!!!!!!!")
        else:
            print("---------------------%%%%%%%%%%%%O0000kkkkkkK!!!!!!!!%%%%%%%%%%%%----------", cnt)
            results.append(result_response)

    return results

def execute(ng_words):
    # Read the CSV file into a pandas DataFrame
    
    df = read_csv('URL.csv')

    # Get the data from the first column
    url_list = df['URL'].tolist()
    # url_list = ['https://ja.aliexpress.com/w/wholesale-タイヤ.html?spm=a2g0o.home.search.0', 'https://ja.aliexpress.com/w/wholesale-4997284.html?spm=a2g0o.home.search.0']
    print("first_column_data--- ", url_list, type(url_list))
    # first_numbers = [re.search(r'\d+', url).group(0) for url in url_list]
    # print("first_numbers--- ", first_numbers, type(first_numbers))
    id_list = []
    try:
        for url in url_list:
            print("url: ", url)
            if '/item/' in url:
                id = re.search(r'\d+', url).group(0)
                id_list.append(id)
                # print("id_list: ", id_list, len(id_list))
            elif '/store/' in url:
                try:
                    # id = url.split('-')[1].split('.')[0]
                    id = re.search(r'\d+', url).group(0)
                    print("id: ", id)
                    id_counts = sp(id)
                except Exception as e:
                    print('ID gathering Error:', e)
                try:
                    print("ids: ", id_counts)
                    if id_counts == 'error':
                        print("The URL may be invalid: ", url)
                        continue
                    if id_counts == []:
                        print("The URL may be invalid: ", url)
                    else :
                        for element in id_counts:
                            id_list.append(element)
                    print("id_list: ", id_list, len(id_list))
                except Exception as e:
                    print('ID Appending Error:', e)
            else:
                print("The URL may be invalid: ", url)
        if id_list == []:
            return 'error' 
    except Exception as e:
        print('ID listing Error:', e)
        pass

    results = scrape_products(id_list, ng_words)
    if results == 'error':
        print("Error in results: ", results)
        return "error"
    # print("-------------json_result--------------: ", results)

    # print("results: ", results)

    title = []
    images = [[], [], [], [], [], [], [], [], [], []]
    price = []
    description = []
    productId = []
    item_link = []

    # print("Results is ok!!!!!!!!!!!!!!!!!!!!!", results)
    

    if results == []:
        print('No products found')
        return 'No products found'

    ids = [d['id'] for d in results if 'id' in d]

    df1 = [d['title'] for d in results if 'title' in d]
    df2 = [d['img'] for d in results if 'img' in d]
    df3 = [d['price'] for d in results if 'price' in d]
    df5 = [d['description'] for d in results if 'description' in d]

    pre = "<DIV><SPAN><DIV ALIGN=center STYLE='TEXT-ALIGN: CENTER;'><B><FONT SIZE=5 COLOR=#fe2419>※</FONT></B></DIV><DIV ALIGN=center STYLE='TEXT-ALIGN: CENTER;'><B><FONT SIZE=5 COLOR=#fe2419>色やサイズが複数表示されているものは</FONT></B></DIV><DIV ALIGN=center STYLE='TEXT-ALIGN: CENTER;'><B><FONT SIZE=5 COLOR=#fe2419>取引ナビにてご希望するものをご連絡下さい。</FONT></B></DIV></SPAN><DIV STYLE='TEXT-ALIGN: CENTER;'><FONT SIZE=5><SPAN><FONT SIZE=5><FONT SIZE=5><FONT SIZE=5><FONT SIZE=5>ご覧頂きましてありがとうございます！！</FONT></FONT></FONT></FONT></SPAN></FONT></DIV><DIV STYLE='TEXT-ALIGN: CENTER;'><FONT SIZE=5><SPAN><FONT SIZE=5><FONT SIZE=5><FONT SIZE=5><FONT SIZE=5><BR></FONT></FONT></FONT></FONT></SPAN></FONT></DIV><DIV STYLE='TEXT-ALIGN: CENTER;'><FONT SIZE=5><FONT SIZE=5><U><A HREF=https://auctions.yahoo.co.jp/seller/自分のID TARGET=new>他の出品商品も見てみる</A></U></FONT><FONT SIZE=5><FONT SIZE=5><U><FONT SIZE=5><FONT SIZE=5><FONT SIZE=5><FONT SIZE=5><FONT SIZE=5><FONT SIZE=5><FONT SIZE=5><FONT SIZE=5><FONT SIZE=5><FONT SIZE=5><FONT SIZE=5><FONT SIZE=5><BR></FONT></FONT></FONT></FONT></FONT></FONT></FONT></FONT></FONT></FONT></FONT></FONT></U></FONT></FONT></FONT><FONT SIZE=5>もっとショッピングを楽しみたい方はクリック！</FONT></DIV><DIV STYLE='TEXT-ALIGN: CENTER;'><FONT SIZE=5><BR></FONT></DIV><DIV STYLE='TEXT-ALIGN: CENTER;'><FONT SIZE=5><SPAN><FONT SIZE=5><FONT SIZE=5><FONT SIZE=5><FONT SIZE=5>こちらでは海外製品を扱っており、発送連絡から</FONT></FONT></FONT></FONT></SPAN></FONT></DIV><DIV STYLE='TEXT-ALIGN: CENTER;'><FONT SIZE=5><SPAN><FONT SIZE=5><FONT SIZE=5><FONT SIZE=5><FONT SIZE=5>２~４週間頂いております。</FONT></FONT></FONT></FONT></SPAN></FONT></DIV><DIV STYLE='TEXT-ALIGN: CENTER;'><BR></DIV><SPAN><DIV STYLE='TEXT-ALIGN: CENTER;'><DIV ALIGN=left STYLE='TEXT-ALIGN: CENTER;'><FONT SIZE=4><BR></FONT></DIV><DIV ALIGN=left STYLE='TEXT-ALIGN: CENTER;'><IMG SRC=https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQHQQfL1ggrjGTL1MZgLVIML2AC7hxEN2YrXklEM410zrX_P4Sz ALT=「倉庫」の画像検索結果><IMG SRC=https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcSmfRsxtdD53KBUkSDFqgay64suEJ_-gLsYBFnUEav_10L9vJP5 ALT=「海外発送」の画像検索結果></DIV><DIV ALIGN=left STYLE='TEXT-ALIGN: CENTER;'>    海外倉庫より発送依頼をかけさせて頂いております。　　　次に日本に向けて発送させて頂きます。  </DIV><DIV STYLE='TEXT-ALIGN: CENTER;'></DIV><DIV ALIGN=left STYLE='TEXT-ALIGN: CENTER;'><IMG SRC=https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcT5px1uf1rHQmJe8OcrGrfJH3iyF9I75aspR1Hq3IMPVKCuG2NE ALT=「税関」の画像検索結果><IMG SRC=https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcT5dUlNeDZsbfWjg-EFmari2XjVeTGH3FQGc4V0-7f2AIZlNn8T ALT=「検品」の画像検索結果></DIV><DIV ALIGN=left STYLE='TEXT-ALIGN: CENTER;'> 輸入の際に税関のチェックが入ります。　輸入の際に破損等がないか検品させて頂きます。  </DIV><DIV ALIGN=left STYLE='TEXT-ALIGN: CENTER;'><BR></DIV><DIV ALIGN=left STYLE='TEXT-ALIGN: CENTER;'><IMG SRC=https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQEXbYDlBFmGjsEwa86q2nZGelFyANxhIr9gSd61itA_-YoEykP ALT=「受取　宅配」の画像検索結果></DIV><DIV ALIGN=left STYLE='TEXT-ALIGN: CENTER;'>    以上の手順でお客様の元に商品が届きます！  </DIV><DIV ALIGN=left STYLE='TEXT-ALIGN: CENTER;'>    運送手段や、通関時の混雑によりお届け期間が前後  </DIV><DIV ALIGN=left STYLE='TEXT-ALIGN: CENTER;'>    することもございますが、ご了承お願い致します。  </DIV><DIV ALIGN=left><BR></DIV><DIV ALIGN=left><BR></DIV><DIV ALIGN=left><BR></DIV><DIV ALIGN=left><BR></DIV><DIV ALIGN=left><BR></DIV><DIV ALIGN=left><BR></DIV><DIV ALIGN=left><BR></DIV><DIV ALIGN=left><BR></DIV><DIV ALIGN=left><BR></DIV></DIV></SPAN><SPAN><FONT SIZE=5></FONT></SPAN></DIV>"

    after = "<DIV><BR><CENTER><FONT COLOR=#000000 SIZE=5><B></B></FONT><BR><BR><TABLE WIDTH=600 CELLPADDING=2 CELLSPACING=2 BGCOLOR=#DDDDDD><TR><TD BGCOLOR=#FFFFFF><TABLE CELLSPACING=3 CELLPADDING=4 BORDER=0 WIDTH=100%><TR><TD BGCOLOR=#FFCCCC COLSPAN=2 ALIGN=left><B><FONT COLOR=#000000 SIZE=3>          送料について          </FONT></B></TD></TR><TR><TD WIDTH=5%></TD><TD WIDTH=95% ALIGN=left><FONT COLOR=#333333 SIZE=3>          当ショップは全商品が 送料一律1500円です（全国一律）<BR>※在庫の保管状況により、他商品との同梱(同一商品も含む)には対応しておりません。          <BR>（送料は落札された商品ごとに発生します。）          <BR><BR>例）          <BR>当ショップから1つ商品を落札した場合＝送料1500円          <BR>当ショップから2つ商品を落札した場合＝送料3000円            <BR>　　 当ショップから3つ商品を落札した場合＝送料4500円・・・           <BR><BR>必ず下記の内容に同意したうえでご落札お願いします。          </FONT></TD></TR></TABLE><TABLE CELLSPACING=3 CELLPADDING=4 BORDER=0 WIDTH=100%><TR><TD BGCOLOR=#FFFFCC COLSPAN=2 ALIGN=left><B><FONT COLOR=#000000 SIZE=3>          □支払詳細          </FONT></B></TD></TR><TR><TD WIDTH=5%></TD><TD WIDTH=95% ALIGN=left><FONT COLOR=#333333 SIZE=3>          Yahoo!かんたん決済          </FONT></TD></TR></TABLE><TABLE CELLSPACING=3 CELLPADDING=4 BORDER=0 WIDTH=100%><TR><TD BGCOLOR=#CCFFCC COLSPAN=2 ALIGN=left><B><FONT COLOR=#000000 SIZE=3>          □発送詳細          </FONT></B></TD></TR><TR><TD WIDTH=5%></TD><TD WIDTH=95% ALIGN=left><FONT COLOR=#333333 SIZE=3>          ★国際航空便<BR><BR>商品によっては発送通知から商品到着まで最大60日間(2カ月)頂いております。          <BR>※海外の運送会社のため、商品到着まで４週間以上かかることも多々ありますので、ご了承ください。            <BR><BR>また、個人営業のため、入金確認から発送通知まで14日程度頂いております、あらかじめご了承ください。           <BR><BR><BR>★全額返金保障について           <BR><BR>発送より最大60日間(2か月)で商品がお手元に到着しなかった場合、商品代金の全額+送料を確実にお返しいたしますので、ご安心ください。           <BR><BR>今まで、60日間で商品が到着しなかったという前例はありませんので、どうかお気長にお待ちいただければ幸いです。            <BR><BR>到着日数や保証については下記をご参照下さい。            <BR><BR>・当ショップは全商品、追跡サービス（または商品の保証）をお付けしていません。そのため安価でのご提供を実現しておりますので、必ずコチラに同意の上ご落札ください。           <BR><BR>・ 発送前の検品で落札商品に不備があった場合は、商品代金(送料を含む)の全額を返金致します、あらかじめご了承ください。           <BR><BR>・ 配送は全て業者に依頼致しますので、お急ぎの方、到着日数が遅いなど、発送状況や到着日時の頻繁な確認(煽る等)につきましては、お答えできかねますのでご了承ください。            <BR><BR>全商品、海外からの発送のため、安価での提供を実現しております。           <BR><BR>そのため、到着までに少々お時間はかかりますが、最後まで責任を持ってお付き合いさせていただきますのでよろしくお願いします。          <BR><BR>通関手続きや天候の影響で遅れる場合や発送中に問題が発生した場合は迅速に対応をさせて頂きますので、突然の悪い評価でのご連絡はお控え下さい。          </FONT></TD></TR></TABLE><TABLE CELLSPACING=3 CELLPADDING=4 BORDER=0 WIDTH=100%><TR><TD BGCOLOR=#CCCCFF COLSPAN=2 ALIGN=left><B><FONT COLOR=#000000 SIZE=3>          □注意事項          </FONT></B></TD></TR><TR><TD WIDTH=5%></TD><TD WIDTH=95% ALIGN=left><FONT COLOR=#333333 SIZE=3>          ▲注意事項 ・ご落札後、連絡が取れないといったケースが稀にあるため、72時間以内にご入金が可能な方のみのご入札をお願い致します。<BR><BR> ・サイズ・形状の違い、イメージ違い等、お客様都合での返品には対応いたしかねますのでご了承ください。            <BR><BR> ・ご落札後、商品を検品してから発送いたします。商品に不具合等が発生した場合は商品代金の全額(送料も含む)を返金いたしますのでご安心ください。            <BR><BR> 【質問に関して】            <BR>素人の出品ですので、商品説明では書ききれていない点があるかもしれません。 何かご不明な点がありましたら、お気軽に質問してください。            <BR><BR>質問にお答えしやすい時間帯            <BR>※ 平日は22時以降(日本時間) 土日祝は深夜以外でしたらいつでも            <BR><BR> 最後までおよみいただき、ありがとうございました。          </FONT></TD></TR></TABLE></TD></TR></TABLE><SPAN><FONT SIZE=5><SPAN STYLE='TEXT-ALIGN: CENTER;'><FONT SIZE=5><U><A HREF=https://auctions.yahoo.co.jp/seller/自分のID TARGET=new>他の出品商品も見てみる</A></U></FONT></SPAN><FONT SIZE=5><FONT SIZE=5><U><FONT SIZE=5><FONT SIZE=5><FONT SIZE=5><FONT SIZE=5><FONT SIZE=5><FONT SIZE=5><FONT SIZE=5><FONT SIZE=5><FONT SIZE=5><FONT SIZE=5><FONT SIZE=5><FONT SIZE=5><BR></FONT></FONT></FONT></FONT></FONT></FONT></FONT></FONT></FONT></FONT></FONT></FONT></U></FONT></FONT></FONT></SPAN><SPAN><FONT SIZE=5>もっとショッピングを楽しみたい方はクリック！</FONT></SPAN><BR><BR><BR><FONT COLOR=#999999 SIZE=1>+ + + この商品説明は</FONT><A HREF=http://www.auclinks.com/ TARGET=new><FONT COLOR=#666666 SIZE=1>オークションプレートメーカー２</FONT></A><FONT COLOR=#999999 SIZE=1>で作成しました + + +</FONT><FONT COLOR=#FFFFFF SIZE=1><BR>  No.202.001.007</FONT><BR></CENTER></DIV>"

    # print("DF1", df1)
    # print("DF2", df2)
    # print("DF3", df3)
    # print("DF4", df4)
    # print("DF5", df5)
    # with open("data_description.json", "w", encoding="utf-8") as file:
    #     json.dump(df5, file, indent=2, ensure_ascii=False)

    if df1:
        try:
            for i in range(0, len(df1)):

                if len(ng_words) > 0 and any(element in df1[i] for element in ng_words) :
                    print("Fail ng_words: ", df1[i])
                    continue
                print("Pass ng_words: ", df1[i])

                title.append(df1[i])
                productId.append(ids[i])
                item_link.append(f"https://aliexpress.com/item/{ids[i]}.html")
                for img_count in range(10):
                    try:
                        if df2[i][img_count] is not None:
                            down = df2[i][img_count]
                            url = f"{down}"  # Replace with the actual image URL
                            print(url, img_count)
                            response = get(url)

                            if response.status_code == 200:
                                with open(f"result/{i + 1}_{ids[i]}_{img_count + 1}.jpg", "wb") as f:
                                    f.write(response.content)
                                print("Image downloaded successfully")
                                images[img_count].append(f"{i + 1}_{ids[i]}_{img_count + 1}.jpg")
                            else:
                                print("Failed to download image")
                                images[img_count].append("")
                        else :
                            images[img_count].append("")
                    except Exception as e:
                        images[img_count].append("")
                        print("No image!", e)
                        pass
                try:
                    main_description = ''
                    for dp in df5[i]:
                        main_description += f"<TR><TH>{dp[0]}</TH><TD>{dp[1]}</TD></TR>"
                    main_description = '<TABLE CELLSPACING=0>' + main_description + '</TABLE>'
                    description.append(pre + main_description + after)
                except  Exception as e:
                    print("Description Error: ", e)
                    description.append('')
                    pass
                price.append(df3[i])              
            
            # print("%%%%% ", description[0])
            print("productId: ", len(productId))
            df = DataFrame({
                "カテゴリ": productId,
                "タイトル": title,
                "説明": description,
                "開始価格": price,
                "即決価格": price,
                "個数": 1,
                "開催期間": 7,
                "終了時間": 0,
                "JANコード": item_link,
                "画像1": images[0],
                "画像1コメント": '',
                "画像2": images[1],
                "画像2コメント": '',
                "画像3": images[2],
                "画像3コメント": '',
                "画像4": images[3],
                "画像4コメント": '',
                "画像5": images[4],
                "画像5コメント": '',
                "画像6": images[5],
                "画像6コメント": '',
                "画像7": images[6],
                "画像7コメント": '',
                "画像8": images[7],
                "画像8コメント": '',
                "画像9": images[8],
                "画像9コメント": '',
                "画像10": images[9],
                "画像10コメント": '',
                "商品発送元の都道府県": "海外",
                "商品発送元の市区町村": '',
                "送料負担": "落札者",
                "代金支払い": "先払い",
                "Yahoo!かんたん決済": "はい",
                "かんたん取引": "はい",
                "商品代引": "いいえ",
                "商品の状態": "新品",
                "商品の状態備考": "",
                "返品の可否": "返品不可",
                "返品の可否備考": "",
                "入札者評価制限": "はい",
                "悪い評価の割合での制限": "はい",
                "入札者認証制限": "はい",
                "自動延長": "はい",
                "早期終了": "はい",
                "値下げ交渉": "いいえ",
                "自動再出品": 3,
                "自動値下げ": "",
                "自動値下げ価格変更率": "",
                "注目のオークション": "",
                "おすすめコレクション": "",
                "送料固定": "はい",
                "荷物の大きさ": "",
                "荷物の重量": "",
                "ネコポス": "",
                "ネコ宅急便コンパクト": "",
                "ネコ宅急便": "",
                "ゆうパケット": "",
                "ゆうパック": "",
                "ゆうパケットポストmini": "",
                "ゆうパケットプラス": "",
                "発送までの日数": "3日～7日",
                "配送方法1": "国際便（追跡なし）",
                "配送方法1全国一律価格": 1500,
                "北海道料金1": "",
                "沖縄料金1": "",
                "離島料金1": "",
                "配送方法2": "",
                "配送方法2全国一律価格": "",
                "北海道料金2": "",
                "沖縄料金2": "",
                "離島料金2": "",
                "配送方法3": "",
                "配送方法3全国一律価格": "",
                "北海道料金3": "",
                "沖縄料金3": "",
                "離島料金3": "",
                "配送方法4": "",
                "配送方法4全国一律価格": "",
                "北海道料金4": "",
                "沖縄料金4": "",
                "離島料金4": "",
                "配送方法5": "",
                "配送方法5全国一律価格": "",
                "北海道料金5": "",
                "沖縄料金5": "",
                "離島料金5": "",
                "配送方法6": "",
                "配送方法6全国一律価格": "",
                "北海道料金6": "",
                "沖縄料金6": "",
                "離島料金6": "",
                "配送方法7": "",
                "配送方法7全国一律価格": "",
                "北海道料金7": "",
                "沖縄料金7": "",
                "離島料金7": "",
                "配送方法8": "",
                "配送方法8全国一律価格": "",
                "北海道料金8": "",
                "沖縄料金8": "",
                "離島料金8": "",
                "配送方法9": "",
                "配送方法9全国一律価格": "",
                "北海道料金9": "",
                "沖縄料金9": "",
                "離島料金9": "",
                "配送方法10": "",
                "配送方法10全国一律価格": "",
                "北海道料金10": "",
                "沖縄料金10": "",
                "離島料金10": "",
                "受け取り後決済サービス": "いいえ",
                "海外発送": "いいえ",
            })

            df.to_csv('登録.csv', index=False, encoding='shift_jis', errors='ignore')
        except Exception as e:
            return "error"
            print("Data listing Error: ", e)
    else :
        print("数分後にもう一度試してみてください！")
        return "error"

    return "Success"

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(run())

def Aliex_main_id(ng_words):

    result = execute(ng_words)
    print('Scraping result: ', result)

    return result



