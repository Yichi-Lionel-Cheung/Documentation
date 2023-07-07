from datetime import datetime, timedelta
from os.path import exists, basename
from json import dumps
from shutil import rmtree
from pathlib import Path
from collections import OrderedDict
from _code_generation_helpers import SPDB, MHDB, WRITING_ALGORITHMS, get_json_content, get_text_content, MARKET_HOUR
TAG = f'<!-- Code generated by {basename(__file__)} -->\n'

days = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
root = Path("Resources/datasets/market-hours")
root.mkdir(exist_ok=True, parents=True)

def to_title(name):
    return name.replace('-',' ').title().replace('Pre Market', 'Pre-market').replace('Post Market', 'Post-market')

def to_url(parts):
    return '/'.join([x[3:].lower().replace(' ','-') for x in parts])

def __generate_metadata(entry):
    description = entry[MARKET_HOUR.INTRODUCTION][3:-4]
    target = entry['target'].parts
    site_name = target[-1][3:]
    metadata = {
    "type": "metadata",
    "values": {
        "description": description,
        "keywords": "regular trading hours, pre-market hours, post-market hours, extended market hours, holidays, time zone",
        "og:description": description,
        "og:title": f"{site_name} - Documentation QuantConnect.com",
        "og:type": "website",
        "og:site_name": f"{site_name} - QuantConnect.com",
        "og:image": f"https://cdn.quantconnect.com/docs/i/{to_url(target)}.png"
        }
    }
    with open(entry['target'] / 'metadata.json', 'w', encoding='utf-8') as fp:
        fp.write(dumps(metadata, indent=4))
        
def __hours_to_table(category, fullname, timezone, data):
    lines = ''
    for day in days:
        hours = data.get(day)
        if not hours:
            continue
        lines += f'<tr><td>{day.title()}</td><td>{", ".join(hours)}</td></tr>\n'
        
    if not lines:
        return None

    return f'''{TAG}<p>The following table shows the {category} hours for the {fullname} market:</p>
<table class="table qc-table table-reflow">
<thead>
<tr><th style="width: 20%;">Weekday</th><th style="width: 80%;">Time ({timezone})</th></tr>
</thead>
<tbody>
{lines}</tbody>
</table>'''

def __write_content(exchange, entries):
    
    rows, imax = '', len(entries)

    for i, entry in enumerate(entries.values()):
        fullname = entry['fullname']
        timezone = entry['exchangeTimeZone']

        parts = entry['path'].parts
        if imax > 1 and len(parts) > 5 and parts[3] not in ['cfd', 'forex', 'index', 'indexoption']:
            entry['target'] = entry['target'] / f'{exchange} {parts[4].upper()}'
        
        if parts[-1] != 'generic':
            name = parts[-1].upper()
            entry['target'] = entry['target'] / f'{i+11} {name}'
            href = f'<a href="/docs/v2/{to_url(entry["target"].parts)}">{name}</a>'
            rows += f'<li>{href}</li>\n' if parts[3] == 'forex' \
                else f'<tr><td>{href}</td><td>{entry["name"]}</td></tr>\n'
        elif imax == 1 and parts[3] in ['future']:
            # Generic Future without other assets
            entry['target'] = entry['target'] / f'{exchange} {parts[-2].upper()}'

        entry['path'].mkdir(parents=True, exist_ok=True)
        entry['target'].mkdir(parents=True, exist_ok=True)
        path = '/'.join(parts[1:])

        __generate_metadata(entry)

        with open(entry['path'] / f'{MARKET_HOUR.INTRODUCTION}.html', 'w', encoding='utf-8') as fp:
            fp.write(entry[MARKET_HOUR.INTRODUCTION])
        with open(entry['target'] / f'01 {to_title(MARKET_HOUR.INTRODUCTION)}.php', 'w', encoding='utf-8') as fp:
            fp.write(f'<?php include(DOCS_RESOURCES."/{path}/{MARKET_HOUR.INTRODUCTION}.html"); ?>')
        
        with open(entry['path'] / f'{MARKET_HOUR.TIME_ZONE}.html', 'w', encoding='utf-8') as fp:
            fp.write(TAG + entry[MARKET_HOUR.TIME_ZONE])
        with open(entry['target'] / f'08 {to_title(MARKET_HOUR.TIME_ZONE)}.php', 'w', encoding='utf-8') as fp:
            fp.write(f'<?php include(DOCS_RESOURCES."/{path}/{MARKET_HOUR.TIME_ZONE}.html"); ?>')

        php = f'<?php include(DOCS_RESOURCES."/datasets/market-hours/no-{MARKET_HOUR.REGULAR}.html"); ?>'
        data = entry.pop(MARKET_HOUR.REGULAR, None)
        if data:
            with open(entry['path'] / f'{MARKET_HOUR.REGULAR}.html', 'w', encoding='utf-8') as fp:
                html = data if isinstance(data, str) else \
                    __hours_to_table('regular trading', fullname, timezone, data)
                fp.write(html)
                php = f'<?php include(DOCS_RESOURCES."/{path}/{MARKET_HOUR.REGULAR}.html"); ?>'
        with open(entry['target'] / f'03 {to_title(MARKET_HOUR.REGULAR)}.php', 'w', encoding='utf-8') as fp:
            fp.write(php)

        php = f'<?php include(DOCS_RESOURCES."/datasets/market-hours/no-{MARKET_HOUR.PRE_MARKET}.html"); ?>'
        data = entry.pop(MARKET_HOUR.PRE_MARKET, None)
        if data:
            with open(entry['path'] / f'{MARKET_HOUR.PRE_MARKET}.html', 'w', encoding='utf-8') as fp:
                fp.write(__hours_to_table('pre-market', fullname, timezone, data))
                php = f'<?php include(DOCS_RESOURCES."/{path}/{MARKET_HOUR.PRE_MARKET}.html"); ?>'
        with open(entry['target'] / f'02 {to_title(MARKET_HOUR.PRE_MARKET)}.php', 'w', encoding='utf-8') as fp:
            fp.write(php)

        php = f'<?php include(DOCS_RESOURCES."/datasets/market-hours/no-{MARKET_HOUR.POST_MARKET}.html"); ?>'
        data = entry.pop(MARKET_HOUR.POST_MARKET, None)
        if data:
            with open(entry['path'] / f'{MARKET_HOUR.POST_MARKET}.html', 'w', encoding='utf-8') as fp:
                fp.write(__hours_to_table('post-market', fullname, timezone, data))
                php = f'<?php include(DOCS_RESOURCES."/{path}/{MARKET_HOUR.POST_MARKET}.html"); ?>'
        with open(entry['target'] / f'04 {to_title(MARKET_HOUR.POST_MARKET)}.php', 'w', encoding='utf-8') as fp:
            fp.write(php)

        for j, item in enumerate([MARKET_HOUR.HOLIDAY, MARKET_HOUR.EARLY_CLOSE, MARKET_HOUR.LATE_OPEN]):
            php = f'<?php include(DOCS_RESOURCES."/datasets/market-hours/no-{item}.html"); ?>'
            html = entry.pop(item, None)
            if html:
                with open(entry['path'] / f'{item}.html', 'w', encoding='utf-8') as fp:
                    fp.write(html)
                    php = f'<?php include(DOCS_RESOURCES."/{path}/{item}.html"); ?>'
            elif imax > 1 and j == 0:
                php = f'<?php include(DOCS_RESOURCES."/{"/".join(parts[1:-1])}/generic/{item}.html"); ?>'
            with open(entry['target'] / f'{j+5:02d} {to_title(item)}.php', 'w', encoding='utf-8') as fp:
                fp.write(php)

    if rows:
        entry = entries.get('[*]', None)
        fullname = entry['fullname']
        with open(entry['path'] / 'assets-with-other-hours.html', 'w', encoding='utf-8') as fp:
            if entry['path'].parts[3] == 'forex':
                fp.write(f'''{TAG}<p>The following list shows the pairs that have different trading periods than the overall {fullname} market:</p>
<ul>
{rows}</ul>
</table>''')
            else:
                contract_name = 'indices' if entry['path'].parts[3] == 'index' else 'contracts'
                fp.write(f'''{TAG}<p>The following table shows the {contract_name} that have different trading periods than the overall {fullname} market:</p>
<table class="table qc-table table-reflow">
<thead><tr><th>Symbol</th><th>Name</th></tr></thead>
<tbody>
{rows}</tbody>
</table>''')
        with open(entry['target'] / f'09 Assets With Other Hours.php', 'w', encoding='utf-8') as fp:
            path = '/'.join(entry['path'].parts[1:])
            fp.write(f'<?php include(DOCS_RESOURCES."/{path}/assets-with-other-hours.html"); ?>')

# Get contract name from symbol
contracts_real = {
    'SPX': 'S&P 500 Index',
    'NDX': 'Nasdaq 100 Index',
    'VIX': 'CBOE Volatility Index'
    }
for line in get_text_content(SPDB).split('\n'):
    csv = line.split(',')
    if len(csv) < 4 or csv[0].startswith('market') or csv[2] == "[*]": continue
    i = 0 if csv[1].lower() == 'forex' else 3
    contracts_real[csv[1]] = csv[i].strip()
contracts_real["[*]"] = "generic"

raw_dict = get_json_content(MHDB)
entries = raw_dict["entries"]
sorted_assets = {}

for key, entry in entries.items():

    exceptions = ['base','crypto','index-india','option-india-','fxcm','spxw']
    if any([x in key.lower() for x in exceptions]):
        continue

    tmp = key.split("-")
    
    entry = sorted_assets.setdefault(tmp[0], {}).setdefault(tmp[1], {}).setdefault(tmp[-1], entry)

    name = contracts_real.get(tmp[-1], tmp[-1])
    fullname = {
        'Cfd-oanda-[*]': 'CFD',
        'Equity-usa-[*]': 'US Equity',
        'Equity-india-[*]': 'India Equity',
        'Option-usa-[*]': 'Equity Option',
        'Index-usa-[*]': 'US Indices',
        'IndexOption-usa-[*]': 'US Index Option',
    }.get(key, tmp[0])
    asset_class = tmp[0].replace("Cfd", "CFD").replace("IndexOption", "US Index Option")

    if "[*]" not in tmp[-1]:
        fullname = f'{name} ' + {
            "cfd": f'contract in the {asset_class.upper()}',
            "forex": f'pair in the {asset_class}',
            "index": '',
            "indexoption": f'Option contracts'
        }.get(tmp[0].lower(),
            f'contract in the {tmp[1].upper()} {asset_class}')
    
    if tmp[0::2] == ["Future","[*]"]:
        fullname = f'{tmp[1].upper()} {asset_class}'

    entry['name'] = name
    entry['fullname'] = fullname

    entry['path'] = root / tmp[0].lower()
    if tmp[0].lower() not in ["cfd", "forex"]:
        entry['path'] = entry['path'] / tmp[1]
    entry['path'] = entry['path'] / f'{tmp[-1] if name != "generic" else name}'

    mapping = {
        'equity-usa': '01 US Equity/09',
        'equity-india': '02 India Equity/05',
        'option-usa': '03 Equity Options/04',
        'forex-oanda': '06 Forex/04',
        'index-usa': '09 Index/04',
        'indexoption-usa': '10 Index Options/04',
        'cfd-oanda': '11 CFD/04',
    }.get('-'.join(tmp[0:2]).lower(), '07 Futures/04')
    entry['target'] = Path(f"{WRITING_ALGORITHMS}/03 Securities/99 Asset Classes/{mapping} Market Hours")

    entry[MARKET_HOUR.INTRODUCTION] = f"<p>This page shows the trading hours, holidays, and time zone of the {fullname} market.</p>"

    entry["exchangeTimeZone"] = entry["exchangeTimeZone"].replace("_", " ")
    entry[MARKET_HOUR.TIME_ZONE] = f'<p>The {fullname} market trades in the <code>{entry["exchangeTimeZone"]}</code> time zone.</p>'

    for day in days:
        for x in entry.pop(day, []):
            if x['state'] == "premarket":
                hours = entry.setdefault(MARKET_HOUR.PRE_MARKET, {}).setdefault(day, [])
                hours.append(f'{x["start"]} to {x["end"].replace("1.00", "24")}')
            elif x['state'] == "market":
                hours = entry.setdefault(MARKET_HOUR.REGULAR, {}).setdefault(day, [])
                hours.append(f'{x["start"]} to {x["end"].replace("1.00", "24")}')
            elif x['state'] == "postmarket":
                hours = entry.setdefault(MARKET_HOUR.POST_MARKET, {}).setdefault(day, [])
                hours.append(f'{x["start"]} to {x["end"].replace("1.00", "24")}')

    cutoff = datetime.utcnow() + timedelta(365)
    
    holidays = sorted([datetime.strptime(date, "%m/%d/%Y") for date in entry.pop("holidays", [])
        if datetime.strptime(date, "%m/%d/%Y") < cutoff])   

    early_closes = sorted([(datetime.strptime(date, "%m/%d/%Y"), time) for date, time in entry.pop("earlyCloses", {}).items()
        if datetime.strptime(date, "%m/%d/%Y") < cutoff], key=lambda x: x[0])

    late_opens = sorted([(datetime.strptime(date, "%m/%d/%Y"), time) for date, time in entry.pop("lateOpens", {}).items()
        if datetime.strptime(date, "%m/%d/%Y") < cutoff], key=lambda x: x[0])

    nyse = '' if not key.startswith('Equity-usa-[*]') else \
        "<p>LEAN uses the <a target='_blank' rel='nofollow' href='https://www.nyse.com/markets/hours-calendars'>trading holidays</a> from the NYSE website.</p>\n"

    if holidays:
        rows = ''
        for i in range(0, len(holidays), 5):
            rows += '<tr>' + ''.join([f'<td>{x.strftime("%Y-%m-%d")}</td>' for x in holidays[i:i+5]]) + '</tr>\n' 

        entry[MARKET_HOUR.HOLIDAY] = f'''{TAG}{nyse}<p>The following table shows the dates of holidays for the {fullname} market:</p>
<table class="table qc-table table-reflow">
<thead><tr><th colspan="5">Date (<i>yyyy-mm-dd</i>)</th></tr></thead>
<tbody>
{rows}</tbody>
</table>'''
    else:
        backup, _ = '', entry.pop(MARKET_HOUR.HOLIDAY, None)
        if key in ['Option-usa-[*]', 'Index-usa-[*]']:
            backup = sorted_assets['Equity']['usa']['[*]']            
        if key == 'Option-india-[*]':
            backup = sorted_assets['Equity']['india']['[*]']
        if key.startswith('IndexOption-usa'):
            backup = sorted_assets['Index']['usa'][tmp[2]]
        if backup:
            entry[MARKET_HOUR.HOLIDAY] = backup.get(MARKET_HOUR.HOLIDAY).replace(backup.get('fullname'), fullname)

    if early_closes:
        rows = ''
        for date, time in early_closes:
            rows += f'<tr><td>{date.strftime("%Y-%m-%d")}</td><td>{time}</td></tr>\n'

        entry[MARKET_HOUR.EARLY_CLOSE] = f'''{TAG}<p>The following table shows the early closes for the {fullname} market:</p>                
<table class="table qc-table table-reflow">
<thead>
<tr><th style="width: 50%;">Date (<i>yyyy-mm-dd</i>)</th><th style="width: 50%;">Time Of Market Close ({entry["exchangeTimeZone"]})</th></tr>
</thead>
<tbody>
{rows}</tbody>
</table>'''
    else:
        backup = ''
        if key in ['Option-usa-[*]', 'Index-usa-[*]']:
            backup = sorted_assets['Equity']['usa']['[*]']            
        if key == 'Option-india-[*]':
            backup = sorted_assets['Equity']['india']['[*]']
        if key.startswith('IndexOption-usa'):
            backup = sorted_assets['Index']['usa'][tmp[2]]
        if backup and MARKET_HOUR.EARLY_CLOSE in backup:
            entry[MARKET_HOUR.EARLY_CLOSE] = backup.get(MARKET_HOUR.EARLY_CLOSE).replace(backup.get('fullname'), fullname)

    if late_opens:
        rows = ''
        for date, time in late_opens:
            rows += f'<tr><td>{date.strftime("%Y-%m-%d")}</td><td>{time}</td></tr>\n'

        entry[MARKET_HOUR.LATE_OPEN] = f'''{TAG}<p>The following table shows the late opens for the {fullname} market:</p>
<table class="table qc-table table-reflow">
<thead>
<tr><th style="width: 50%;">Date (<i>yyyy-mm-dd</i>)</th><th style="width: 50%;">Time Of Market Open ({entry["exchangeTimeZone"]})</th></tr>
</thead>
<tbody>
{rows}</tbody>
</table>'''
    else:
        backup = ''
        if key in ['Option-usa-[*]', 'Index-usa-[*]']:
            backup = sorted_assets['Equity']['usa']['[*]']            
        if key == 'Option-india-[*]':
            backup = sorted_assets['Equity']['india']['[*]']
        if key.startswith('IndexOption-usa'):
            backup = sorted_assets['Index']['usa'][tmp[2]]
        if backup and MARKET_HOUR.LATE_OPEN in backup:
            entry[MARKET_HOUR.LATE_OPEN] = backup.get(MARKET_HOUR.LATE_OPEN).replace(backup.get('fullname'), fullname)

    if exists(entry['target']):
        rmtree(entry['target'])

# Clean up Resources
if exists(root):
    rmtree(root)

for security_type, exchanges in sorted_assets.items():
    exchange_names = sorted(exchanges.keys())
    for i, exchange_name in enumerate(exchange_names):
        entries = OrderedDict(sorted(exchanges[exchange_name].items(), key=lambda x: x[1]['path']))
        if len(entries) > 1:
            entry = entries.get('[*]')
            if not entry:
                raise Exception(f'No generic for {exchange_name}')

            all_time_zone = sorted(set(x["exchangeTimeZone"] for x in entries.values())) 
            if len(all_time_zone) > 1:
                time_zone = entry[MARKET_HOUR.TIME_ZONE]
                end = time_zone.index('trades in the') + 14
                entry[MARKET_HOUR.TIME_ZONE] = f'''{time_zone[:end]}following time zones:</p>
<ul>
    <li><code>{"</code></li><li><code>".join(all_time_zone)}</code></li>
</ul>'''
        __write_content(i+11, entries)
    
    if security_type.lower() == 'future':
        with open(entry['target'].parent / '00.json', 'w', encoding='utf-8') as fp:
            fp.write(dumps({
                "type" : "landing",
                "heading" : "Futures",
                "subHeading" : "",
                "content" : "<p>Select one of the following Futures markets to see its operating hours:</p>",
                "featureShortDescription": { i+11: "" for i in range(len(exchange_names)) }
            }, indent=4))

# Generate files for generic case of no information
empty = {
    MARKET_HOUR.PRE_MARKET: "<p>Pre-market trading is not available.</p>",
    MARKET_HOUR.POST_MARKET: "<p>Post-market trading is not available.</p>",
    MARKET_HOUR.HOLIDAY: "<p>There are no holidays for this market.</p>",
    MARKET_HOUR.EARLY_CLOSE: "<p>There are no days with early closes.</p>",
    MARKET_HOUR.LATE_OPEN: "<p>There are no days with late opens.</p>",
}

for item, content in empty.items():
    with open(root / f'no-{item}.html', 'w', encoding='utf-8') as fp:
        fp.write(TAG + content)