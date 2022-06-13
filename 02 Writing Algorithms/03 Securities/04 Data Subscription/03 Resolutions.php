<p>Resolution is the duration of time that's used to sample a data source. </p>

<?php echo file_get_contents(DOCS_RESOURCES."/enumerations/resolution.html"); ?>

<p>To see which resolutions of data are available for a dataset, see the dataset listing in the <a href="/datasets">Data Market</a>. To create custom resolution periods, see <a href='/docs/v2/writing-algorithms/consolidating-data/key-concepts'>Consolidating Data</a>.</p>

<p><span class='new-term'>Data density</span> describes the frequency of entries in a dataset. Datasets at the tick resolution have dense data density. All other resolutions usually have regular data density. If a non-tick resolution dataset doesn’t have an entry at each sampling, it has sparse density.</p>
