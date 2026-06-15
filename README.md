# Cheap Flight Finder - Free API / No Amadeus Version

This is a backend-only Python program that searches flight prices using LetsFG local search.

It does not use Amadeus.

## Why LetsFG?

LetsFG local search can run on your own machine and does not require an API key for searching.

## Install

```bash
pip install -r requirements.txt
```

## Test LetsFG directly first

```bash
letsfg search BER MAA 2026-07-30 --mode fast
```

If that works, run the Python app.

## Run the app

```bash
python app.py --from BER --to MAA --date 2026-07-30 --range 1
```

Search more nearby dates:

```bash
python app.py --from BER --to MAA --date 2026-07-30 --range 3
```

Use full mode:

```bash
python app.py --from BER --to MAA --date 2026-07-30 --range 1 --mode full
```

## Important

Start with:

```bash
--range 1
```

because each date runs a separate flight search. If you use `--range 3`, the program searches 7 dates.

## Files

```text
cheap-flight-finder-free-api/
│
├── app.py
├── flight_service.py
├── date_utils.py
├── requirements.txt
└── README.md
```

## Notes

- This project is backend-only.
- No frontend is included.
- No Amadeus credentials are needed.
- No `.env` file is required.
- This depends on LetsFG local search behavior.
- If LetsFG output format changes, `flight_service.py` may need small parsing changes.

## Example

```bash
python app.py --from BER --to DEL --date 2026-08-01 --range 2
```
