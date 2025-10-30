#!/usr/bin/env python3
import argparse
import requests
import sys
import csv

# --- Configuration (wired-in constants) ---
BASE_URL = "https://www.phil.muni.cz/matomo/"
SITES = {
        "arnenovak.phil.muni.cz": 5,
        "projectiles.phil.muni.cz": 6,
        "cinematicbrno.phil.muni.cz": 10,
        "digilib.phil.muni.cz": 13,
        "www.beauty-patterns.org": 14,
        "herbaria.phil.muni.cz": 19,
        "digital-humanities.phil.muni.cz": 9
        }
# ------------------------------------------

def fetch_stats(site_id, year, token, segment=None):
    base_params = {
        "module": "API",
        "idSite": site_id,
        "period": "year",
        "date": f"{year}-01-01",
        "format": "JSON",
        "token_auth": token
    }

   
    params_visits = base_params | {"method": "VisitsSummary.get"}
    if segment:
        params_visits["segment"] = segment

    try:
        r1 = requests.get(BASE_URL, params=params_visits, timeout=30)
        r1.raise_for_status()
        visits = r1.json()
    except requests.exceptions.RequestException as e:
        sys.exit(f"Request failed for site {site_id}: {e}")
    except ValueError:
        sys.exit(f"Failed to parse JSON response for site {site_id}")


    params_actions = base_params | {"method": "Actions.get"}
    if segment:
        params_actions["segment"] = segment

    try:
        r2 = requests.get(BASE_URL, params=params_actions, timeout=30)
        r2.raise_for_status()
        actions = r2.json()
    except requests.exceptions.RequestException as e:
        sys.exit(f"Request failed for site {site_id}: {e}")
    except ValueError:
        sys.exit(f"Failed to parse JSON response for site {site_id}")

    return {
        "nb_visits": visits.get("nb_visits", 0),
        "nb_pageviews": actions.get("nb_pageviews", 0),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Fetch Matomo yearly total visits and pageviews per site and segment."
    )
    parser.add_argument("--token", required=True, help="Matomo API token_auth")
    parser.add_argument("--year", required=True, help="Year, e.g. 2025")
    args = parser.parse_args()

    token = args.token
    year = args.year

    writer = csv.writer(sys.stdout)
    writer.writerow([f"Statistics {year}"])
    writer.writerow(["Platform", 
       "Pageviews overall", "Pageviews MUNI", "Pageviews CZ", "Pageviews CZ not MUNI", "Pageviews abroad", 
       "Visits overall", "Visits MUNI", "Visits CZ", "Visits CZ not MUNI", "Visits abroad"])

    for site_name, site_id in SITES.items():
        totals = fetch_stats(site_id, year, token)
        visits_all = totals['nb_visits']
        pageviews_all = totals['nb_pageviews']

        czonly = fetch_stats(site_id, year, token, "countryCode==CZ");
        visits_czonly = czonly['nb_visits']
        pageviews_czonly = czonly['nb_pageviews']

        
        notmuni = fetch_stats(site_id, year, token, "visitIp<100.64.0.0,visitIp>100.127.255.255;visitIp<147.251.0.0,visitIp>147.251.255.255")
        visits_notmuni = notmuni['nb_visits']
        pageviews_notmuni = notmuni['nb_pageviews']

        visits_muni = visits_all - visits_notmuni;
        pageviews_muni = pageviews_all - pageviews_notmuni;

        visits_cznotmuni = visits_czonly - visits_muni;
        pageviews_cznotmuni = pageviews_czonly - pageviews_muni;

        visits_abroad = visits_all - visits_czonly;
        pageviews_abroad = pageviews_all - pageviews_czonly;


        writer.writerow([site_name, pageviews_all, pageviews_muni, pageviews_czonly, pageviews_cznotmuni, pageviews_abroad,
                         visits_all, visits_muni, visits_czonly, visits_cznotmuni, visits_abroad])


if __name__ == "__main__":
    main()

