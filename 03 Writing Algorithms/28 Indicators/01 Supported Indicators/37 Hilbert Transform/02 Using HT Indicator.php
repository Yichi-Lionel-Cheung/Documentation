<!-- Code generated by indicator_reference_code_generator.py -->
<? 
include(DOCS_RESOURCES."/qcalgorithm-api/_method_container.html");

$hadReference = false;
$hasAutomaticIndicatorHelper = true;
$helperPrefix = '';
$typeName = 'HilbertTransform';
$helperName = 'HT';
$helperArguments = 'symbol, 7, 0.635, 0.338';
$properties = array("InPhase","Quadrature");
$otherProperties = array();
$updateParameterType = 'time/number pair or an <code>IndicatorDataPoint</code>';
$constructorArguments = '7, 0.635, 0.338';
$updateParameterValue = 'bar.EndTime, bar.Close';
$hasMovingAverageTypeParameter = False;
$constructorBox = 'hilbert-transform';
include(DOCS_RESOURCES."/indicators/using-indicator.php");
?>