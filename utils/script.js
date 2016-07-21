function adjustScroll() {
	//Get scroll position and increment it to adjust with the header size
	var doc = document.documentElement;
	var left = (window.pageXOffset || doc.scrollLeft) - (doc.clientLeft || 0);
	var top = (window.pageYOffset || doc.scrollTop)  - (doc.clientTop || 0);
	window.scrollTo(left, top-45);
}

function jumpToImg(event, total) {
	if (event.which == 13 || event.keyCode == 13) {
		var h = document.getElementById("textbox").value;
		if (h > total) {
			h = "bottom";
		} else if (!(h > 1)) {
			h = "top";
		}
		var url = location.href;
		location.href = "#" + h;
		history.replaceState(null, null, url);

		if (h != "bottom") {
			adjustScroll();
		}
	}
}

function startTime() {
	var today = new Date();
	var weekday = new Array(7);
	weekday[0]=  "Sun";
	weekday[1] = "Mon";
	weekday[2] = "Tue";
	weekday[3] = "Wed";
	weekday[4] = "Thu";
	weekday[5] = "Fri";
	weekday[6] = "Sat";

	var d = weekday[today.getDay()]; 
	var h = today.getHours();
	var m = today.getMinutes();
	m = checkTime(m);
	document.getElementById('txt').innerHTML = d + " " + h + ":" + m;
	var t = setTimeout(startTime, 500);
}

function checkTime(i) {
	if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
	return i;
}

function toggleFullscreen(elem) {
	elem = elem || document.documentElement;
	if (!document.fullscreenElement && !document.mozFullScreenElement && !document.webkitFullscreenElement && !document.msFullscreenElement) {
		if (elem.requestFullscreen) {
			elem.requestFullscreen();
		} else if (elem.msRequestFullscreen) {
			elem.msRequestFullscreen();
		} else if (elem.mozRequestFullScreen) {
			elem.mozRequestFullScreen();
		} else if (elem.webkitRequestFullscreen) {
			elem.webkitRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT);
		}
	} else {
		if (document.exitFullscreen) {
			document.exitFullscreen();
		} else if (document.msExitFullscreen) {
			document.msExitFullscreen();
		} else if (document.mozCancelFullScreen) {
			document.mozCancelFullScreen();
		} else if (document.webkitExitFullscreen) {
			document.webkitExitFullscreen();
		}
	}
}

function adjustImgs() {
	var images = document.getElementById("manga").getElementsByTagName("img");
	for (var i = 0; i < images.length; i++) {
		images[i].style.width = 1000;
	}
}

function incImgsSize() {
	var tmp = window.pageYOffset/document.body.scrollHeight;

	var images = document.getElementById("manga").getElementsByTagName("img");
	for (var i = 0; i < images.length; i++) {
		var width = parseInt(images[i].style.width.replace("px", ""));
		if (width >= 1800) {
			break;
		}
		images[i].style.width = width + 100;
	}

	window.scrollTo(0, document.body.scrollHeight*tmp);
}

function decImgsSize() {
	var tmp = window.pageYOffset/document.body.scrollHeight;

	var images = document.getElementById("manga").getElementsByTagName("img");
	for (var i = 0; i < images.length; i++) {
		var width = parseInt(images[i].style.width.replace("px", ""));
		if (width <= 500) {
			break;
		}
		images[i].style.width = width - 100;
	}

	window.scrollTo(0, document.body.scrollHeight*tmp);
}

function keyPress(e) {
	var x = e || window.event;
	var key = (x.keyCode || x.which);
	if (document.activeElement != document.getElementById("textbox")) {
		switch (key) {
			case 78: case 110: //N
				decImgsSize();
				break;
			case 77: case 109: //M
				incImgsSize();
				break;
			case 90: case 122: //Z
				scrollBy(0,65);
				break;
			case 88: case 120: //X
				scrollBy(0,-65);
				break;
			case 65: case 97:  //A
				document.getElementById("dir").click();
				break;
			case 81: case 113: //Q
				document.getElementById("albums").click();
				break;
			case 79: case 111: //O
				document.getElementById("prev").click();
				break;
			case 80: case 112: //P
				document.getElementById("next").click();
				break;
			case 73: case 105: //I
				keyInfo();
				break;
			case 45: //INSERT
				document.getElementById("textbox").focus();
				document.getElementById("textbox").value = "";
				break;
		}
	} else if (key == 45) { //INSERT
		document.getElementById("textbox").blur();
		document.getElementById("textbox").value = "";
	}
}

function keyInfo() {
	alert("Hotkeys:\n\tQ - Go to Albums\n\tA - Show Directory Name\n\tO - Previous Album\n\tP - Next Album\n\tZ - Scroll Down\n\tX - Scroll Up\n\tN - Decrease Image Size\n\tM - Increase Image Size\n\tI - Show This Message\n\tInsert - Focus/Unfocus Textbox");
}

function versionInfo() {
	alert("Thanks for using Heart Viewer!\n\nAuthor: Lucas Pascotti Valem");
}
