import re
<<<<<<< HEAD
import time
import scrapy

from collections import defaultdict
=======

import scrapy
>>>>>>> 29465c6708e6f0e35b0baccb06878080f129b253


class Covid19StatusSpider(scrapy.Spider):
    name = "covid19_status"
    allowed_domains = ["web.archive.org"]
    start_urls = [
        "https://web.archive.org/web/20210907023426/https://ncov.moh.gov.vn/vi/web/guest/dong-thoi-gian"
    ]

<<<<<<< HEAD
    cities = [
        "TP Ho Chi Minh",
        "Ha Noi",
        "Da Nang",
        "Hai Phong",
        "Can Tho",
        "An Giang",
        "Ba Ria - Vung Tau",
        "Bac Giang",
        "Bac Kan",
        "Bac Lieu",
        "Bac Ninh",
        "Ben Tre",
        "Binh Dinh",
        "Binh Duong",
        "Binh Phuoc",
        "Binh Thuan",
        "Ca Mau",
        "Cao Bang",
        "Dak Lak",
        "Dak Nong",
        "Dien Bien",
        "Dong Nai",
        "Dong Thap",
        "Gia Lai",
        "Ha Giang",
        "Ha Nam",
        "Ha Tinh",
        "Hai Duong",
        "Hau Giang",
        "Hoa Binh",
        "Hung Yen",
        "Khanh Hoa",
        "Kien Giang",
        "Kon Tum",
        "Lai Chau",
        "Lam Dong",
        "Lang Son",
        "Lao Cai",
        "Long An",
        "Nam Dinh",
        "Nghe An",
        "Ninh Binh",
        "Ninh Thuan",
        "Phu Tho",
        "Phu Yen",
        "Quang Binh",
        "Quang Nam",
        "Quang Ngai",
        "Quang Ninh",
        "Quang Tri",
        "Soc Trang",
        "Son La",
        "Tay Ninh",
        "Thai Binh",
        "Thai Nguyen",
        "Thanh Hoa",
        "Thua Thien Hue",
        "Tien Giang",
        "Tra Vinh",
        "Tuyen Quang",
        "Vinh Long",
        "Vinh Phuc",
        "Yen Bai",
    ]

    def string_pre_processing(self, text):
        # Function to remove HTML tags
        def no_html_tag(s):
            return re.sub("<.*?>", "", s) if isinstance(s, str) else s

        # Function to remove special characters
        def no_special_characters(s):
            return re.sub(r"\.", "", s) if isinstance(s, str) else s

        # Function to remove Vietnamese accents
        def no_accent_vietnamese(s):
            s = re.sub(r"[àáạảãâầấậẩẫăằắặẳẵ]", "a", s)
            s = re.sub(r"[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]", "A", s)
            s = re.sub(r"[èéẹẻẽêềếệểễ]", "e", s)
            s = re.sub(r"[ÈÉẸẺẼÊỀẾỆỂỄ]", "E", s)
            s = re.sub(r"[òóọỏõôồốộổỗơờớợởỡ]", "o", s)
            s = re.sub(r"[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]", "O", s)
            s = re.sub(r"[ìíịỉĩ]", "i", s)
            s = re.sub(r"[ÌÍỊỈĨ]", "I", s)
            s = re.sub(r"[ùúụủũưừứựửữ]", "u", s)
            s = re.sub(r"[ƯỪỨỰỬỮÙÚỤỦŨ]", "U", s)
            s = re.sub(r"[ỳýỵỷỹ]", "y", s)
            s = re.sub(r"[ỲÝỴỶỸ]", "Y", s)
            s = re.sub(r"[Đ]", "D", s)
            s = re.sub(r"[đ]", "d", s)

            marks_list = [
                "\u0300",
                "\u0301",
                "\u0302",
                "\u0303",
                "\u0306",
                "\u0309",
                "\u0323",
            ]
            for mark in marks_list:
                s = s.replace(mark, "")
            return s

        text_without_html = no_html_tag(text)
        text_without_special_characters = no_special_characters(text_without_html)
        text_without_accent_vietnamese = no_accent_vietnamese(
            text_without_special_characters
        )
        standard_text = text_without_accent_vietnamese
        return standard_text

    def extract_new_cases(self, text):
        """
        TO DO: Query elements to get information about time as well as the number of new cases.
        """
        # Extract numbers from a string with keyword "CA MAC MOI"
        pattern = re.compile(r"(\d+) CA MAC MOI", re.IGNORECASE)
        match = pattern.search(text) if isinstance(text, str) else None
        return int(match.group(1)) if match else None

    def extract_cities_case_detail(self, text):
        """
        TO DO: Extract data to know how many new infections each city has
        """
        start_index = text.find("tai")
        if start_index != -1:
            text = text[start_index + len("tai") :]
            cities_and_cases = re.findall(r"([^\d(]+)\s*\((\d+)\),", text)

            city_cases = []

            for city_and_case in cities_and_cases:
                city_case = {
                    "city": city_and_case[0].strip(),
                    "case": int(city_and_case[1]),
                }
                if city_and_case[0].strip() in self.cities:
                    city_cases.append(city_case)
            return city_cases

    def parse(self, response):
        data_dict = defaultdict(lambda: {"new_case": None, "city_case": None})

        covid_statuses = response.xpath("//div[@class='timeline-detail']")

        for covid_status_detail in covid_statuses:
            date_time = covid_status_detail.xpath(".//div[1]/h3/text()").get()

            for line in range(1, 4):
                status_line = covid_status_detail.xpath(
                    f".//div[2]/p[{line}]/text()"
                ).get()
                if status_line:
                    announcement_standard = self.string_pre_processing(status_line)
                    new_case = self.extract_new_cases(announcement_standard)
                    city_case = self.extract_cities_case_detail(announcement_standard)

                    data_dict[date_time]["new_case"] = (
                        data_dict[date_time]["new_case"] or new_case
                    )
                    data_dict[date_time]["city_case"] = (
                        data_dict[date_time]["city_case"] or city_case
                    )

        for date_time, data in data_dict.items():
            if data["new_case"] and data["city_case"] is not None:
                yield {
                    "time": date_time,
                    "new_case": data["new_case"],
                    "city_case": data["city_case"],
                }
=======
    # Remove utf-8
    def no_accent_vietnamese(self, s):
        s = re.sub(r"[àáạảãâầấậẩẫăằắặẳẵ]", "a", s)
        s = re.sub(r"[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]", "A", s)
        s = re.sub(r"[èéẹẻẽêềếệểễ]", "e", s)
        s = re.sub(r"[ÈÉẸẺẼÊỀẾỆỂỄ]", "E", s)
        s = re.sub(r"[òóọỏõôồốộổỗơờớợởỡ]", "o", s)
        s = re.sub(r"[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]", "O", s)
        s = re.sub(r"[ìíịỉĩ]", "i", s)
        s = re.sub(r"[ÌÍỊỈĨ]", "I", s)
        s = re.sub(r"[ùúụủũưừứựửữ]", "u", s)
        s = re.sub(r"[ƯỪỨỰỬỮÙÚỤỦŨ]", "U", s)
        s = re.sub(r"[ỳýỵỷỹ]", "y", s)
        s = re.sub(r"[ỲÝỴỶỸ]", "Y", s)
        s = re.sub(r"[Đ]", "D", s)
        s = re.sub(r"[đ]", "d", s)

        marks_list = [
            "\u0300",
            "\u0301",
            "\u0302",
            "\u0303",
            "\u0306",
            "\u0309",
            "\u0323",
        ]
        for mark in marks_list:
            s = s.replace(mark, "")
        return s

    # Remove html-tag
    def no_html_tag(self, status):
        return re.sub("<.*?>", "", status)

    # Remove special characters
    def no_special_characters(self, status):
        return re.sub(r"\.", "", status)

    def extract_number_from_string(self, status):
        pattern = re.compile(r"\b(\d+) CA MAC MOI")
        match = pattern.search(status)
        if match:
            number = int(match.group(1))
            return number
        else:
            return None

    def extract_new_cases(self, status):
        processing_functions = [
            self.no_html_tag,
            self.no_special_characters,
            self.no_accent_vietnamese,
            self.extract_number_from_string,
        ]
        for function in processing_functions:
            status = function(status)
        return status

    def extract_city_case(self, status):
        status = self.no_accent_vietnamese(status)
        start_index = status.find("tai")
        if start_index != -1:
            status = status[start_index + len("tai") :]
        clean_status = re.sub(r"\.", "", status)
        cities_and_cases = re.findall(r"([^\d(]+)\s*\((\d+)\),", clean_status)

        city_cases = []
        for city_and_case in cities_and_cases:
            city_case = {
                "city": city_and_case[0].strip(),
                "case": int(city_and_case[1]),
            }
            city_cases.append(city_case)
        return city_cases

    def parse(self, response):
        datetime_results = {}
        status = response.xpath("//div[@class='timeline-detail']")
        for covid_status_detail in status:
            date_time = covid_status_detail.xpath(".//div[1]/h3/text()").get()
            status_raw = None
            for order in [1, 2, 3]:
                status_raw = covid_status_detail.xpath(
                    f".//div[2]/p[{order}]/text()"
                ).get()
                if status_raw:
                    new_case = self.extract_new_cases(status_raw)
                    if new_case:
                        yield {
                            "time": date_time,
                            "new_case": new_case,
                        }

                    city_case = self.extract_city_case(status_raw)

                    if date_time in datetime_results:
                        if new_case is not None:
                            datetime_results[date_time]["new_case"] += new_case
                        datetime_results[date_time]["city_case"].extend(city_case)
                    else:
                        datetime_results[date_time] = {
                            "new_case": new_case if new_case is not None else 0,
                            "city_case": city_case,
                        }
        filtered_results = {
            date_time: result
            for date_time, result in datetime_results.items()
            if result["new_case"] != 0 or result["city_case"]
        }

        for date_time, result in filtered_results.items():
            yield {
                "time": date_time,
                "new_case": result["new_case"],
                "city_case": result["city_case"],
            }
>>>>>>> 29465c6708e6f0e35b0baccb06878080f129b253

        next_page_path = "//div[@class='clearfix lfr-pagination']/ul/li[2]/a/@href"
        next_page_url = response.xpath(next_page_path).get()
        if next_page_url:
            yield scrapy.Request(url=next_page_url, callback=self.parse)
<<<<<<< HEAD
            time.sleep(3)
=======
>>>>>>> 29465c6708e6f0e35b0baccb06878080f129b253
        else:
            self.log("No next page URL found.")
