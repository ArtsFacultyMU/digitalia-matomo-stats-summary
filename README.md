# Digitalia Statistics

Outputs Digitalia statistics from Matomo for all platforms for defined year. 

## Description

The script __digitalia_stats.py__ serves as a cli tool to get the statistics gathered in Matomo [](https://www.phil.muni.cz/matomo/). It uses Matomo API to get the visitors and pageviews for all of the Digitalia platforms.
The platforms are listed directly in the script. Script outputs to stdout simple CSV file which can be imported to an Excel table.

## Usage

```digitalia_stats.py --year <year> --token <matomo_token>```

The _year_ and _token_ must be specified. _token_ is a matomo token which can be obtained in the Matomo UI.
