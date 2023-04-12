<p>You can use the <code>ObjectStore</code> to preserve the algorithm state across live deployments. In the following example, you will learn how to save and restore the state of the <a href="/docs/v2/writing-algorithms/algorithm-framework/insight-manager">Insight Manager</a> generated in a live deployment.</p>

<ol>
    <li>Create an algorithm, add a data subscription and an <a href="/docs/v2/writing-algorithms/algorithm-framework/alpha/key-concepts">Alpha Model</a>.</li>
    <div class='section-example-container'>
    <pre class='csharp'>public class ObjectStoreChartingAlgorithm : QCAlgorithm
{
    public override void Initialize()
    {
        SetUniverseSelection(new ManualUniverseSelectionModel(QuantConnect.Symbol.Create("SPY", SecurityType.Equity, Market.USA)));
        SetAlpha(new ConstantAlphaModel(InsightType.Price, InsightDirection.Up, TimeSpan.FromDays(5), 0.025, null));    
    }
}</pre>
    <pre class='python'>class ObjectStoreChartingAlgorithm(QCAlgorithm):
    def Initialize(self):
        self.SetUniverseSelection(ManualUniverseSelectionModel([ Symbol.Create("SPY", SecurityType.Equity, Market.USA) ]))
        self.SetAlpha(ConstantAlphaModel(InsightType.Price, InsightDirection.Up, timedelta(5), 0.025, None))</pre>
    </div>

    <p>The algorithm will add the <code>Insight</code> objects generated by the Alpha Model to the Insight Manager (<code class='csharp'>Insights</code><code class='python'>self.Insights</code>).</p>
    
    <li>Get the list of active <code>Insight</code> objects from the <code class='csharp'>Insights</code><code class='python'>self.Insights</code>.</li>
    <div class='section-example-container'>
    <pre class='csharp'>public override void OnEndOfAlgorithm()
{
    var insights = Insights.GetInsights(x => x.IsActive(UtcTime));
}</pre>
    <pre class='python'>def OnEndOfAlgorithm(self):
    insights = self.Insights.GetInsights(lambda x: x.IsActive(self.UtcTime))</pre>
    </div>

    <li>Alternatively, get the list of all <code>Insight</code> objects from the <code class='csharp'>Insights</code><code class='python'>self.Insights</code>.</li>
    <div class='section-example-container'>
    <pre class='csharp'>public override void OnEndOfAlgorithm()
{
    var insights = Insights.GetInsights(x => true);
}</pre>
    <pre class='python'>def OnEndOfAlgorithm(self):
    insights = self.Insights.GetInsights(lambda x: True)</pre>
    </div>

    <li>To store the collected data, call the <code>SaveJson</code> method with a key.</li>
    <div class='section-example-container'>
    <pre class='csharp'>public override void OnEndOfAlgorithm()
{
    ObjectStore.SaveJson($"{ProjectId}/insights", insights);
}</pre>
    <pre class='python'>def OnEndOfAlgorithm(self):
    content = ','.join([JsonConvert.SerializeObject(x) for x in insights])
    self.ObjectStore.Save(f"{self.ProjectId}/insights", f'[{content}]')</pre>
    </div>

    <li>To read the stored data, call the <code>ReadJson</code> method with a key. Populate the Insight Manager with the range of <code>Insight</code> objects, and delete the stored data.</li>
    <div class='section-example-container'>
    <pre class='csharp'>public class ObjectStoreChartingAlgorithm : QCAlgorithm
{
    public override void Initialize()
    {
        var insightsKey = $"{ProjectId}/{_insightsKey}";
        if (ObjectStore.ContainsKey(insightsKey))
        {
            var insights = ObjectStore.ReadJson&lt;List&lt;Insight&gt;&gt;(insightsKey);
            Insights.AddRange(insights);

            ObjectStore.Delete(insightsKey);
        }   
    }
}</pre>
    <pre class='python'>class ObjectStoreChartingAlgorithm(QCAlgorithm):
    def Initialize(self):
        insightsKey = f"{self.ProjectId}/insights"
        if self.ObjectStore.ContainsKey(insightsKey):
            insights = self.ObjectStore.ReadJson[List[Insight]](insightsKey)
            self.Insights.AddRange(insights)

            self.ObjectStore.Delete(insightsKey)</pre>
    </div>
</ol>

<ol class='python'>
    <p>In this example, we use the <code>SaveJson</code> and <code>ReadJson</code> method for convenience, since the serialization process retains all the relevant information. The <code>Insight</code> object is a C# object, thus the algorithm need to import the following C# libraries.</p>
    <div class='section-example-container'>
        <pre class='python'>from Newtonsoft.Json import JsonConvert
from System.Collections.Generic import List</pre>
    </div>
</ol>

<div class="qc-embed-frame" style="display: inline-block; position: relative; width: 100%; min-height: 100px; min-width: 300px;">
    <div class="qc-embed-dummy" style="padding-top: 56.25%;"></div>
    <div class="qc-embed-element" style="position: absolute; top: 0; bottom: 0; left: 0; right: 0;">
    <iframe class="csharp qc-embed-backtest" height="100%" width="100%" style="border: 1px solid #ccc; padding: 0; margin: 0;" src="https://www.quantconnect.com/terminal/processCache?request=embedded_backtest_2c647eaeef59f2db0b9b957e7a4c014f.html"></iframe>
    <iframe class="python qc-embed-backtest" height="100%" width="100%" style="border: 1px solid #ccc; padding: 0; margin: 0;" src="https://www.quantconnect.com/terminal/processCache?request=embedded_backtest_5042a67266802c124cacc99ce9ab2499.html"></iframe>
    </div>
</div>