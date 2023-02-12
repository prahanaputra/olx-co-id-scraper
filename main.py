import scrapper

input_url = input("Input URL : ")

url = scrapper.WebScrapper(input_url)
url.scrape()
url.find_ul_element()
url.loop_element()
url.list_to_csv()