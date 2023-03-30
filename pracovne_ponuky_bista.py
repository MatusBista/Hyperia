from bs4 import BeautifulSoup
import requests, json


class HyperiaScraper: 
    def __init__(self):
        self.links = []                             
        self.titles = []
        self.places = []
        self.salaries = []
        self.contract_types = []
        self.contact_emails = []
        self.final_info = []
        self.url = "https://www.hyperia.sk/kariera" 

    def main(self):
        self.main_page()
        for i in range(0, len(self.main_page_links)):
            self.get_links(i)

        for url in self.links:
            soup_page = self.requester(url)
            page = soup_page.find_all("p")
            self.places.append(soup_page.find(lambda tag: tag.name == "p" and "práce:" in tag.text).b.string)
            self.get_salary(page)
            self.get_contract(page)
            self.get_email(page)
            self.get_titles(soup_page)
        self.information()

    def main_page(self):
        page = requests.get(self.url).content
        soup_page = BeautifulSoup(page, "html.parser")
        self.main_page_links = soup_page.find_all(class_ = "link_text", limit = 3)

    def get_links(self, i: int):
        self.links.append("https://hyperia.sk" + self.main_page_links[i].attrs["href"])

    def requester(self, url: str):
        page = requests.get(url).content
        soup_page = BeautifulSoup(page, "html.parser") 
        return soup_page
    
    def get_titles(self, soup_page: BeautifulSoup):
        title = soup_page.find("h1").get_text() 
        self.titles.append(title)

    def get_salary(self, page: BeautifulSoup):
        if "Platové ohodnotenie:" in page[1].get_text():
            self.salaries.append(page[1].get_text().split("\n")[1].split(":")[1].strip())
        else:
            self.salaries.append(page[0].get_text().split("\n")[1].split(":")[1].strip())

    def get_contract(self, page: BeautifulSoup):
        if "Typ pracového pomeru:" in page[1].get_text():
            self.contract_types.append(page[1].get_text().split("\n")[-1].split(":")[1].strip())
        else:
            self.contract_types.append(page[0].get_text().split("\n")[-2].split(":")[1].strip())

    def get_email(self, page: list):
        self.contact_emails.append(page[-3].strong.string)

    def information(self):
        for i in range(len(self.titles)):
            self.final_info.append(
                {
                "title ": self.titles[i],
                "place ": self.places[i],
                "salary ": self.salaries[i],
                "contract_type ": self.contract_types[i],
                "contact_email ": self.contact_emails[i],
                }
            )


object = HyperiaScraper()
object.main()
data =  object.final_info

with open("pracovne_ponuky.json", "w", encoding = "utf-8") as f:
    json.dump(data, f, indent = 4, ensure_ascii = False)