<p>
    Follow these steps to start local live trading with the <?=$isBrokerage ? "{$brokerageName} brokerage" : "{$dataFeedName} data provider" ?>:
</p>

<ol>
    <li><a href='/docs/v2/lean-cli/initialization/authentication#02-Log-In'>Log in</a> to the CLI if you haven't done so already.</li>        
    <li>Open a terminal in the <a href='/docs/v2/lean-cli/initialization/organization-workspaces'>organization workspace</a> that contains the project.</li>

<?
if ($isBrokerage) {
  $brokerages = array(
      "QuantConnect Paper Trading",
      "Interactive Brokers",
      "Tradier",
      "Oanda",
      "Bitfinex",
      "Coinbase Advanced Trade",
      "Binance",
      "Zerodha",
      "Samco",
      "Terminal Link",
      "Trading Technologies",
      "Kraken",
      "Bybit",
      "TradeStation",
      "Alpaca",
      "Charles Schwab"
  );
  $brokerageNumber = array_search($brokerageName, $brokerages) + 1;
}

$dataProviders = array(
    "Interactive Brokers",
    "Tradier",
    "Oanda",
    "Bitfinex",
    "Coinbase Advanced Trade",
    "Binance",
    "Zerodha",
    "Samco",
    "Terminal Link",
    "Trading Technologies",
    "Kraken",
    "IQFeed",
    "Polygon",
    "IEX Cloud",
    "CoinApi",
    "Custom data only",
    "Bybit",
    "TradeStation",
    "Alpaca",
    "CharlesSchwab"
);
$dataProviderNumber = isset($dataProviderName) ? array_search($dataProviderName, $dataProviders) + 1 : -1;
?>
    
    <li>Run <code>lean live deploy "&lt;projectName&gt;"</code> to start a live deployment wizard for the project in <span class='public-directory-name'>. / &lt;projectName&gt;</span> and then enter <? if ($isBrokerage) { ?> the brokerage number, <span class='key-combinations'><?=$brokerageNumber?></span><? } else { ?>a brokerage number<? } ?>.
    <div class='cli section-example-container'>
<pre>$ lean live deploy "My Project"
Select a brokerage:
1) Paper Trading
2) Interactive Brokers
3) Tradier
4) OANDA
5) Bitfinex
6) Coinbase Advanced Trade
7) Binance
8) Zerodha
9) Samco
10) Terminal Link
11) Trading Technologies
12) Kraken
13) Bybit
14) TradeStation
15) Alpaca
16) Charles Schwab
Enter an option: <?=$isBrokerage ? $brokerageNumber : '1'?></pre>
</div>
</li>

<?=$brokerageDetails ?>

<? if (isset($supportsCashHoldings) && $supportsCashHoldings) { ?> 
    <li>Set your initial cash balance.
        <div class='cli section-example-container'>
        <pre>$ lean live deploy "My Project"
Previous cash balance: [{'currency': 'USD', 'amount': 100000.0}]
Do you want to set a different initial cash balance? [y/N]: y 
Setting initial cash balance...
Currency: USD
Amount: 95800
Cash balance: [{'currency': 'USD', 'amount': 95800.0}]
Do you want to add more currency? [y/N]: n</pre>
        </div>
    </li> 
<? } ?> 
    
<? if (isset($supportedPositionHoldings) && $supportedPositionHoldings) { ?>
    <li>Set your initial portfolio holdings.
        <div class='cli section-example-container'>
        <pre>$ lean live deploy "My Project"
Do you want to set the initial portfolio holdings? [y/N]: y
Do you want to use the last portfolio holdings? [] [y/N]: n
Setting custom initial portfolio holdings...
Symbol: GOOG
Symbol ID: GOOCV VP83T1ZUHROL
Quantity: 10
Average Price: 50
Portfolio Holdings: [{'symbol': 'GOOG', 'symbolId': 'GOOCV VP83T1ZUHROL', 'quantity': 10, 'averagePrice': 50.0}]
Do you want to add more holdings? [y/N]: n</pre>
        </div>
        </li>
<? } ?>

<?
if ($isBrokerage && $brokerageName == "Terminal Link") {
?>
<li>Enter <span class='key-combinations'>9</span> to select the Terminal Link live data provider.
<div class='cli section-example-container'>
<pre>$ lean live deploy "My Project"
Select a live data provider:
1) Interactive Brokers
2) Tradier
3) Oanda
4) Bitfinex
5) Coinbase Advanced Trade
6) Binance
7) Zerodha
8) Samco
9) Terminal Link
10) Trading Technologies
11) Kraken
12) IQFeed
13) Polygon
14) IEX
15) CoinApi
18) ThetaData
19) Custom data only
20) Bybit
21) TradeStation
22) Alpaca
23) CharlesSchwab

To enter multiple options, separate them with comma: 9</pre>
</div>
</li>   
<?  
} else if (isset($dataProviderName)) {
?>
            <li>Enter <span class='key-combinations'><?=$dataProviderNumber?></span> to select the <?=$dataProviderName?> data provider.</li> 
            <div class='cli section-example-container'>
<pre>$ lean live deploy "My Project"
Select a live data feed:
1) Interactive Brokers
2) Tradier
3) Oanda
4) Bitfinex
5) Coinbase Advanced Trade
6) Binance
7) Zerodha
8) Samco
9) Terminal Link
10) Trading Technologies
11) Kraken
12) IQFeed
13) Polygon
14) IEX
15) CoinApi
16) ThetaData
17) Custom data only
18) Bybit
19) TradeStation
20) Alpaca
21) CharlesSchwab
To enter multiple options, separate them with comma: <?=$dataProviderNumber?></pre>
            </div>
            </li>
<?
    echo $dataProviderDetails;
} else {
?><li>Enter the number of the live data provider(s) to use and then follow the steps required for the data connection.
<div class='cli section-example-container'>
<pre>$ lean live deploy "My Project"
Select a live data provider:
1) Interactive Brokers
2) Tradier
3) Oanda
4) Bitfinex
5) Coinbase Advanced Trade
6) Binance
7) Zerodha
8) Samco
9) Terminal Link
10) Trading Technologies
11) Kraken
12) IQFeed
13) Polygon
14) IEX
15) CoinApi
16) ThetaData
17) Custom data only
18) Bybit
19) TradeStation
20) Alpaca
21) CharlesSchwab
To enter multiple options, separate them with comma:</pre>
</div>
</li>
    <?if ($isBrokerage) {?>
    <p>If you select one of the following data providers, see the respective page for more instructions:</p>
    <ul>
        <li><a href='/docs/v2/lean-cli/live-trading/data-providers/iex-cloud'>IEX Cloud</a></li>
        <li><a href='/docs/v2/lean-cli/live-trading/data-providers/iqfeed'>IQFeed</a></li>
        <li><a href='/docs/v2/lean-cli/live-trading/data-providers/polygon'>Polygon</a></li>
    </ul>
    <? } ?>
<? } ?>


<?=$dataFeedDetails ?>
     
    <li>
        View the result in the <span class='public-directory-name'>&lt;projectName&gt; / live / &lt;timestamp&gt;</span> directory.
        Results are stored in real-time in JSON format.
        You can save results to a different directory by providing the <code>--output &lt;path&gt;</code> option in step 2.
    </li>
</ol>
<p>
    If you already have a live environment configured in your <a href='/docs/v2/lean-cli/initialization/configuration#03-Lean-Configuration'>Lean configuration file</a>, you can skip the interactive wizard by providing the <code>--environment &lt;value&gt;</code> option in step 2.
    The value of this option must be the name of an environment which has <code>live-mode</code> set to <code>true</code>.
</p>
 
