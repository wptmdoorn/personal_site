from parsel import Selector
from playwright.sync_api import sync_playwright
from datetime import datetime
import json


def get_profile(profile: str):
    with sync_playwright() as p:

        profile_data = {
            "basic_info": {},
            "about": {},
            "co_authors": [],
            "publications": [],
        }

        browser = p.chromium.launch(headless=True, slow_mo=20)
        page = browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36")
        page.goto(f"https://www.researchgate.net/profile/{profile}")
        selector = Selector(text=page.content())

        for publication in selector.css("#publications+ .nova-legacy-c-card--elevation-1-above .nova-legacy-o-stack__item"):
            profile_data["publications"].append({
                "title": publication.css(".nova-legacy-v-publication-item__title .nova-legacy-e-link--theme-bare::text").get(),
                "date_published": publication.css(
                    ".nova-legacy-v-publication-item__meta-data-item span::text").get(),
                "authors": publication.css(".nova-legacy-v-person-inline-item__fullname::text").getall(),
                "publication_type": publication.css(".nova-legacy-e-badge--theme-solid::text").get(),
                "description": publication.css(".nova-legacy-v-publication-item__description::text").get(),
                "publication_link": publication.css(".nova-legacy-c-button-group__item .nova-legacy-c-button::attr(href)").get(),
            })

        browser.close()

    # write to data/researchgate_profile.json
    with open(f"app/data/researchgate_profile.json", "w") as f:
        json.dump(profile_data, f, indent=4)


if __name__ == "__main__":
    get_profile("William-Doorn")
