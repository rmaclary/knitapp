function openPattern(evt, patternType) 
{
	var i, tabcontent, tablinks;
	tabcontent = document.getElementsByClassName("tabcontent")
	for (i=0; i < tabcontent.length; i++)
	{
		tabcontent[i].style.display = "none";
	}
	tablinks = document.getElementsByClassName("tablinks")
	for (i=0; i<tablinks.length; i++)
	{
		tablinks[i].className = tablinks[i].className.replace(" active", "");
	}
	document.getElementById(patternType).style.display = "block";
	evt.currentTarget.className += " active";
}
function showGaugeWindow()
{
	var y = document.getElementById("gauge_swatch");
	var n = document.getElementById("yarn_type");
	if (document.getElementById("yes").checked)
	{
		y.style.display = "inline";
		n.style.display = "none";
		document.getElementById("yarn").removeAttribute("required");
	}
	if (document.getElementById("no").checked)
	{
		n.style.display = "inline";
		y.style.display = "none";
		document.getElementById("rpi").removeAttribute("required");
		document.getElementById("spi").removeAttribute("required");
	}
}
function measureUnit()
{
	if (document.getElementById("cent").checked)
	{   
		document.getElementById("spi_lbl").innerHTML = "Stitches per Centimeters";
		document.getElementById("rpi_lbl").innerHTML = "Rows per Centimeters";
		document.getElementById("measurements_legend").innerHTML = "Measurements (Centimeters)";
	}
	if (document.getElementById("inches").checked)
	{
		document.getElementById("spi_lbl").innerHTML = "Stitches per Inch";
		document.getElementById("rpi_lbl").innerHTML = "Rows per Inch";
		document.getElementById("measurements_legend").innerHTML = "Measurements (Inches)";
	}
}
function showShapingOptions()
{
	var s = document.getElementById("sType");
	if (document.getElementById("yes_shaping").checked)
	{
		s.style.display = "inline";
	}
	else
	{
		s.style.display = "none";
	}
}
function showGaugeWindowSock()
{
	var y = document.getElementById("gauge_swatch1");
	var n = document.getElementById("yarn_type1");
	if (document.getElementById("yes1").checked)
	{
		y.style.display = "inline";
		n.style.display = "none";
		document.getElementById("yarn1").removeAttribute("required");
	}
	if (document.getElementById("no1").checked)
	{
		n.style.display = "inline";
		y.style.display = "none";
		document.getElementById("rpi1").removeAttribute("required");
		document.getElementById("spi1").removeAttribute("required");
	}
}
function measureUnitSock()
{
	if (document.getElementById("cent1").checked)
	{   
		document.getElementById("spi_lbl1").innerHTML = "Stitches per Centimeters";
		document.getElementById("rpi_lbl1").innerHTML = "Rows per Centimeters";
		document.getElementById("measurements_legend1").innerHTML = "Measurements (Centimeters)";
	}
	if (document.getElementById("inches1").checked)
	{
		document.getElementById("spi_lbl1").innerHTML = "Stitches per Inch";
		document.getElementById("rpi_lbl1").innerHTML = "Rows per Inch";
		document.getElementById("measurements_legend1").innerHTML = "Measurements (Inches)";
	}
}
function measureType()
{
	var m = document.getElementById("help");
	var s = document.getElementById("help2");
	if (document.getElementById("footMeas").checked)
	{
		m.style.display = "block";
		s.style.display = "none";
		document.getElementById("ssize").removeAttribute("required");
	}
	if (document.getElementById("shoeSize").checked)
	{
		s.style.display = "block";
		m.style.display = "none";
		document.getElementById("ankle").removeAttribute("required");
		document.getElementById("footLength").removeAttribute("required");
	}
}
function genderCheck()
{
	var ws = document.getElementById("womensize");
	var ms = document.getElementById("mensize");
	
	if (document.getElementById("men").checked)
	{
		ms.style.display = "inline";
		ws.style.display = "none";
		ws.removeAttribute("required");
	}
	if (document.getElementById("women").checked)
	{
		ws.style.display = "inline";
		ms.style.display = "none";
		ms.removeAttribute("required");
	}
}
