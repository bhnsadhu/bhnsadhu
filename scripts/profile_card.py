"""Build assets/profile-card.svg.

Fetches the github-profile-summary-cards "profile details" card in this
profile's colors, then swaps the email line for the location line. The hosted
card always shows the public email when one is set, and the email stays public.
"""
import re
import sys
import urllib.parse
import urllib.request

USERNAME = "bhnsadhu"
LOCATION = "Champaign, Illinois"
RED = "D31D36"
PARAMS = {
    "username": USERNAME,
    "theme": "github_dark",
    "bg_color": "101B30",
    "title_color": RED,
    "icon_color": RED,
    "chart_color": RED,
    "border_color": RED,
    "text_color": "FFFFFF",
}
URL = "https://github-profile-summary-cards.vercel.app/api/cards/profile-details?" + urllib.parse.urlencode(PARAMS)
OUT = "assets/profile-card.svg"

# Octicons used by the card (src/const/icon.ts in github-profile-summary-cards).
EMAIL_D = "M1.75 2A1.75 1.75 0 000 3.75v.736a.75.75 0 000 .027v7.737C0 13.216.784 14 1.75 14h12.5A1.75 1.75 0 0016 12.25v-8.5A1.75 1.75 0 0014.25 2H1.75zM14.5 4.07v-.32a.25.25 0 00-.25-.25H1.75a.25.25 0 00-.25.25v.32L8 7.88l6.5-3.81zm-13 1.74v6.441c0 .138.112.25.25.25h12.5a.25.25 0 00.25-.25V5.809L8.38 9.397a.75.75 0 01-.76 0L1.5 5.809z"
LOCATION_D = "M11.536 3.464a5 5 0 010 7.072L8 14.07l-3.536-3.535a5 5 0 117.072-7.072v.001zm1.06 8.132a6.5 6.5 0 10-9.192 0l3.535 3.536a1.5 1.5 0 002.122 0l3.535-3.536zM8 9a2 2 0 100-4 2 2 0 000 4z"


def main() -> int:
    req = urllib.request.Request(URL, headers={"User-Agent": "profile-card-builder"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        svg = resp.read().decode("utf-8")

    if not svg.lstrip().startswith("<svg") or "Contributions on GitHub" not in svg:
        print("Card fetch did not return the expected SVG; keeping the old card.")
        return 1

    if EMAIL_D in svg:
        svg = svg.replace(EMAIL_D, LOCATION_D, 1)
        # The email line is the only info line whose text contains an "@".
        svg, n = re.subn(r'(<text[^>]*class="gpsc-item"[^>]*>)[^<]*@[^<]*(</text>)',
                         lambda m: m.group(1) + LOCATION + m.group(2), svg, count=1)
        if n != 1:
            print("Found the email icon but not the email text; keeping the old card.")
            return 1
    elif LOCATION not in svg:
        print("Card has neither the email line nor the location; keeping the old card.")
        return 1

    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
