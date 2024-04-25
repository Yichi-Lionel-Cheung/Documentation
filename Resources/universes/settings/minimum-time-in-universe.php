<p>The <code class="csharp">MinimumTimeInUniverse</code><code class="python">minimum_time_in_universe</code> setting is a <code class='python'>timedelta</code><code class='csharp'>TimeSpan</code> object that defines the minimum amount of time an asset must be in the universe before the universe can remove it. The default value is <code class='csharp'>TimeSpan.FromDays(1)</code><code class='python'>timedelta(1)</code>. To change the minimum time, in the <a href='/docs/v2/writing-algorithms/initialization'>Initialize</a> method, adjust the algorithm's <code class="csharp">UniverseSettings</code><code class="python">universe_settings</code> before you