<p align="center">
  <img src="https://github.com/Ekans111/Aliexpress-Scraping/blob/master/img/interface.jpg?raw=true" alt="animated" />
</p>

# Aliexpress-Scraping

## Description

This project is a web scraper built using Selenium to extract data from AliExpress website.

## Prerequisites

- Python 3.10.9
- Selenium
- Chrome WebDriver

## Installation

1. Clone this repository.
2. Install the required dependencies by running:

## Usage

1. Enter the urls you want to scrap scrape in the `URL.csv` file.
   `https://ja.aliexpress.com/item/33060691049.html?spm=a2g0o.best.moretolove.17.440b1fd3hyIIjK&gatewayAdapt=glo2jpn`

   `https://ja.aliexpress.com/item/4000531935985.html?spm=a2g0o.best.moretolove.11.440b1fd3hyIIjK&gatewayAdapt=glo2jpn`

2. Run the script.
   Only Run the script to start scraping AliExpress data.<br>
   `py main.py`

3. Enter the _`NG` words_ (it means the item that includs one of the `NG` word in its `name` you don't want to scrap.)

4. Click `開始` button.

5. Wait until message the process is done is displayed and click `終了` button.

6. Find the result from `登録.csv`.

   Images can be found in `result` folder.

## Disclaimer

Please make sure to use this scraper responsibly and respect the website's terms of service.

## Author

Ekans111

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
