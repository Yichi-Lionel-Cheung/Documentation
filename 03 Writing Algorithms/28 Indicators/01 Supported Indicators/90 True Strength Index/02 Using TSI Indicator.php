<!-- Code generated by indicator_reference_code_generator.py -->
<? 
include(DOCS_RESOURCES."/qcalgorithm-api/_method_container.html");

$hadReference = false;
$hasAutomaticIndicatorHelper = true;
$helperPrefix = '';
$typeName = 'TrueStrengthIndex';
$helperName = 'TSI';
$helperArguments = 'symbol, 25, 13, 7, MovingAverageType.Exponential';
$properties = array("Signal");
$otherProperties = array();
$updateParameterType = 'time/number pair or an <code>IndicatorDataPoint</code>';
$constructorArguments = '25, 13, 7, MovingAverageType.Exponential';
$updateParameterValue = 'bar.EndTime, bar.Close';
$hasMovingAverageTypeParameter = True;
$constructorBox = 'true-strength-index';
include(DOCS_RESOURCES."/indicators/using-indicator.php");
?>